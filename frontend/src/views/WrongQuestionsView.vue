<template>
  <div class="wrong-questions-view">
    <div class="page-header">
      <div class="page-header-left">
        <h2>错题本</h2>
        <p>管理所有答错的题目，方便针对性复习</p>
      </div>
      <div class="page-header-right">
        <el-button type="primary" @click="showChapterSelectDialog">
          <el-icon><RefreshRight /></el-icon>
          刷错题
        </el-button>
        <el-button type="danger" @click="clearAll">
          <el-icon><Delete /></el-icon>
          清空错题本
        </el-button>
      </div>
    </div>

    <!-- 章节选择对话框 -->
    <el-dialog v-model="chapterSelectVisible" title="选择刷错题范围" width="600px">
      <div class="chapter-select-content">
        <div class="chapter-select-header">
          <el-checkbox v-model="selectAllChapters" @change="handleSelectAll" style="font-weight: 500;">
            全选所有章节
          </el-checkbox>
          <span class="selected-count">已选择 {{ selectedChapterCount }} 个章节</span>
        </div>
        <div class="chapter-list">
          <el-checkbox-group v-model="selectedChapterIds">
            <div v-for="chapter in store.chapters" :key="chapter.id" class="chapter-item">
              <el-checkbox :label="chapter.id">
                <span class="chapter-name">{{ chapter.name }}</span>
                <el-tag size="small" type="warning" class="chapter-wrong-count">
                  {{ getChapterWrongCount(chapter.id) }} 错题
                </el-tag>
              </el-checkbox>
            </div>
          </el-checkbox-group>
        </div>
        <div class="shuffle-options-section">
          <el-checkbox v-model="shuffleOptionsInDialog">打乱选项顺序</el-checkbox>
        </div>
      </div>
      <template #footer>
        <el-button @click="chapterSelectVisible = false">取消</el-button>
        <el-button type="primary" @click="startPracticeWithChapters">
          <el-icon><VideoPlay /></el-icon>
          开始练习
        </el-button>
      </template>
    </el-dialog>

    <div class="card">
      <div class="filter-bar">
        <el-select v-model="filters.chapter_id" placeholder="选择章节" style="min-width: 120px; flex: 1; max-width: 180px;" clearable @change="loadWrongQuestions">
          <el-option v-for="ch in chapters" :key="ch.id" :label="ch.name" :value="ch.id" />
        </el-select>
        <el-select v-model="filters.question_type_id" placeholder="选择题型" style="min-width: 120px; flex: 1; max-width: 150px;" clearable @change="loadWrongQuestions">
          <el-option v-for="qt in questionTypes" :key="qt.id" :label="qt.name" :value="qt.id" />
        </el-select>
        <el-select v-model="filters.wrong_count_eq" placeholder="错误次数" style="min-width: 100px; flex: 1; max-width: 130px;" clearable @change="loadWrongQuestions">
          <el-option label="全部" :value="undefined" />
          <el-option label="=1" :value="1" />
          <el-option label="=2" :value="2" />
          <el-option label="=3" :value="3" />
          <el-option label="＞3" :value="4" />
          <el-option label="=4" :value="5" />
          <el-option label="=5" :value="6" />
          <el-option label="＞5" :value="7" />
        </el-select>
        <el-select v-model="filters.min_reappearance_count" placeholder="复现次数" style="min-width: 100px; flex: 1; max-width: 130px;" clearable @change="loadWrongQuestions">
          <el-option label="复现≥5次" :value="5" />
        </el-select>
        <el-button v-if="selectedWrongQuestions.length > 0" type="danger" @click="batchRemove">
          <el-icon><Delete /></el-icon>
          批量移除({{ selectedWrongQuestions.length }})
        </el-button>
        <el-button v-if="selectedWrongQuestions.length > 0" type="primary" @click="batchPractice">
          <el-icon><VideoPlay /></el-icon>
          练习选中({{ selectedWrongQuestions.length }})
        </el-button>
        <el-checkbox v-model="selectAll">全选</el-checkbox>
      </div>

      <el-table :data="wrongQuestions" style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="50" />
        <el-table-column prop="question.id" label="ID" width="80" />
        <el-table-column prop="question.stem" label="题干" min-width="200">
          <template #default="{ row }">
            <div v-html="row.question?.stem_html || row.question?.stem"></div>
          </template>
        </el-table-column>
        <el-table-column prop="question.question_type_name" label="题型" width="100" align="center" />
        <el-table-column prop="wrong_count" label="错误次数" width="100" align="center">
          <template #default="{ row }">
            <el-tag type="warning">{{ row.wrong_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reappearance_count" label="复现次数" width="100" align="center">
          <template #default="{ row }">
            <el-tag type="primary">{{ row.reappearance_count || 0 }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="practiceQuestion(row)">练习</el-button>
            <el-button size="small" type="success" @click="removeQuestion(row)">移除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[20, 50, 80, 100, 200, 500, 1000]"
        :total="total"
        layout="total, sizes, prev, pager, next"
        style="margin-top: 20px; justify-content: center;"
        @current-change="loadWrongQuestions"
        @size-change="handleSizeChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useQuizStore } from '@/store/quiz'
import { ElMessage, ElMessageBox } from 'element-plus'
import { VideoPlay, RefreshRight, Delete } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const store = useQuizStore()

const wrongQuestions = ref([])
const chapters = ref([])
const questionTypes = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const selectedWrongQuestions = ref([])
const selectAll = ref(false)

const filters = ref({
  chapter_id: null,
  question_type_id: null,
  wrong_count_eq: undefined,
  min_reappearance_count: undefined
})

const chapterSelectVisible = ref(false)
const selectAllChapters = ref(false)
const selectedChapterIds = ref([])
const shuffleOptionsInDialog = ref(true)

const selectedChapterCount = computed(() => {
  return selectedChapterIds.value.length
})

const getChapterWrongCount = (chapterId) => {
  const chapterWrongQuestions = wrongQuestions.value.filter(wq => {
    return wq.question && wq.question.chapter_id === chapterId
  })
  return chapterWrongQuestions.length
}

const getWrongCountTagType = (count) => {
  if (count >= 5) return 'danger'
  if (count >= 3) return 'warning'
  return 'info'
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  return new Date(timeStr).toLocaleString('zh-CN')
}

const loadWrongQuestions = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value
    }
    if (filters.value.chapter_id) {
      params.chapter_id = filters.value.chapter_id
    }
    if (filters.value.question_type_id) {
      params.question_type_id = filters.value.question_type_id
    }
    if (filters.value.wrong_count_eq !== undefined) {
      params.wrong_count_eq = filters.value.wrong_count_eq
    }
    if (filters.value.min_reappearance_count) {
      params.min_reappearance_count = filters.value.min_reappearance_count
    }
    
    const result = await store.loadWrongQuestions(params)
    wrongQuestions.value = result.data
    total.value = result.total
    chapters.value = store.chapters
    questionTypes.value = store.questionTypes
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const handleSelectionChange = (selection) => {
  selectedWrongQuestions.value = selection
}

watch(selectAll, (val) => {
  if (val) {
    selectedWrongQuestions.value = [...wrongQuestions.value]
  } else {
    selectedWrongQuestions.value = []
  }
})

const showChapterSelectDialog = async () => {
  selectedChapterIds.value = []
  selectAllChapters.value = false
  await store.loadWrongQuestions({ user_id: store.userId, per_page: 10000 })
  wrongQuestions.value = store.wrongQuestions
  chapterSelectVisible.value = true
}

const handleSelectAll = (checked) => {
  if (checked) {
    selectedChapterIds.value = store.chapters.map(ch => ch.id)
  } else {
    selectedChapterIds.value = []
  }
}

const startPracticeWithChapters = async () => {
  chapterSelectVisible.value = false
  
  if (selectedChapterIds.value.length === 0) {
    ElMessage.warning('请至少选择一个章节')
    return
  }
  
  const chapterIds = selectedChapterIds.value.map(id => parseInt(id))
  const chapterIdsStr = chapterIds.join(',')
  
  router.push({
    path: '/practice/wrong',
    query: { 
      mode: 'wrong',
      chapters: chapterIdsStr,
      shuffle_options: shuffleOptionsInDialog.value ? 'true' : 'false'
    }
  })
}

const startPractice = () => {
  router.push('/practice/wrong')
}

const practiceQuestion = (row) => {
  router.push({ path: '/practice/wrong', query: { questionId: row.question_id } })
}

const removeQuestion = async (row) => {
  try {
    await store.removeFromWrongQuestions(row.id)
    ElMessage.success('已移出错题本')
    loadWrongQuestions()
  } catch (error) {
    ElMessage.error('移除失败')
  }
}

const batchRemove = async () => {
  if (selectedWrongQuestions.value.length === 0) {
    ElMessage.warning('请先选择要移除的题目')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要移除选中的 ${selectedWrongQuestions.value.length} 道错题吗？`,
      '批量移除',
      { type: 'warning' }
    )

    const wrongIds = selectedWrongQuestions.value.map(wq => wq.id)
    await axios.delete('/api/wrong-questions/batch', {
      data: {
        user_id: store.userId,
        wrong_ids: wrongIds
      }
    })

    ElMessage.success(`已移除 ${wrongIds.length} 道错题`)
    selectAll.value = false
    selectedWrongQuestions.value = []
    loadWrongQuestions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('移除失败')
    }
  }
}

const batchPractice = async () => {
  if (selectedWrongQuestions.value.length === 0) {
    ElMessage.warning('请先选择要练习的题目')
    return
  }

  try {
    const wrongIds = selectedWrongQuestions.value.map(wq => wq.id)
    console.log('DEBUG batchPractice: calling API with wrong_ids:', wrongIds)

    const res = await axios.post('/api/wrong-questions/practice', {
      user_id: store.userId,
      shuffle: false,
      wrong_ids: wrongIds
    })
    const result = res.data
    console.log('DEBUG batchPractice: API result:', result)

    if (!result || !result.data || result.data.length === 0) {
      ElMessage.warning('选中的题目不存在或已被移除')
      return
    }

    store.clearSavedPracticeSession('wrong')
    ElMessage.success(`已加载 ${result.data.length} 道错题准备练习`)
    router.push({
      path: '/practice/wrong',
      query: {
        mode: 'wrong_selected',
        sessionId: result.session_id,
        wrongIds: JSON.stringify(wrongIds)
      }
    })
  } catch (error) {
    console.error('DEBUG batchPractice error:', error)
    ElMessage.error('加载练习失败: ' + (error.message || '未知错误'))
  }
}

const clearAll = async () => {
  try {
    await ElMessageBox.confirm('确定要清空错题本吗？此操作不可恢复。', '警告', { type: 'warning' })
    await store.clearWrongQuestions()
    ElMessage.success('已清空')
    loadWrongQuestions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('清空失败')
    }
  }
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  loadWrongQuestions()
}

onMounted(() => {
  loadWrongQuestions()
})
</script>

<style scoped>
.wrong-questions-view {
  padding: 16px;
  max-width: 100%;
  overflow-x: hidden;
  box-sizing: border-box;
}

.chapter-select-content {
  max-height: 400px;
}

.chapter-select-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 6px;
  flex-wrap: wrap;
  gap: 10px;
}

.selected-count {
  font-size: 14px;
  color: #606266;
}

.chapter-list {
  max-height: 300px;
  overflow-y: auto;
}

.chapter-item {
  padding: 10px 15px;
  border-radius: 6px;
  transition: all 0.3s;
}

.chapter-item:hover {
  background: #f5f7fa;
}

.chapter-item .el-checkbox {
  width: 100%;
}

.chapter-name {
  font-size: 14px;
  color: #303133;
  margin-right: 8px;
}

.chapter-question-count {
  float: right;
}

.chapter-wrong-count {
  float: right;
}

.shuffle-options-section {
  margin-top: 15px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 6px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  margin-bottom: 16px;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.page-header-left {
  flex: 1;
  min-width: 150px;
}

.page-header-left h2 {
  margin: 0 0 4px 0;
  font-size: 20px;
  font-weight: 600;
  color: #fff;
  white-space: nowrap;
}

.page-header-left p {
  margin: 0;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.85);
  white-space: nowrap;
}

.page-header-right {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.page-header-right .el-button {
  min-width: auto;
  padding: 8px 12px;
  font-size: 13px;
}

.page-header-right .el-button .el-icon {
  margin-right: 4px;
}

:deep(.card) {
  max-width: 100%;
  overflow-x: hidden;
  box-sizing: border-box;
}

:deep(.el-table) {
  max-width: 100%;
  overflow-x: auto;
}

:deep(.el-table__body-wrapper) {
  overflow-x: auto;
}

:deep(.filter-bar) {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 16px;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  overflow-x: visible;
}

:deep(.filter-bar > *) {
  flex-shrink: 1;
  flex-basis: auto;
}

:deep(.filter-bar .el-select) {
  flex: 1;
  min-width: 100px;
  max-width: 180px;
}

:deep(.filter-bar .el-input) {
  flex: 1;
  min-width: 100px;
  max-width: 180px;
}

:deep(.filter-bar .el-button),
:deep(.filter-bar .el-checkbox) {
  flex-shrink: 0;
  white-space: nowrap;
}

.card {
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  box-sizing: border-box;
}
</style>
