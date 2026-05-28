<template>
  <div class="questions-view">
    <div class="page-header" style="display: flex; justify-content: space-between; align-items: center;">
      <div>
        <h2>题库管理</h2>
        <p>管理所有题目，支持批量操作</p>
      </div>
      <div>
        <el-button type="primary" @click="$router.push('/questions/new')">
          <el-icon><Plus /></el-icon>
          新建题目
        </el-button>
        <el-button @click="$router.push('/import')">
          <el-icon><Upload /></el-icon>
          Excel导入
        </el-button>
        <el-button @click="exportSelected">
          <el-icon><Download /></el-icon>
          导出选中
        </el-button>
      </div>
    </div>

    <div class="card">
      <div class="filter-bar" style="display: flex; gap: 15px; flex-wrap: wrap; margin-bottom: 20px;">
        <el-input v-model="filters.stem" placeholder="搜索题干" style="width: 200px;" clearable @change="loadQuestions" />
        <el-select v-model="filters.chapter_id" placeholder="选择章节" style="width: 150px;" clearable @change="loadQuestions">
          <el-option v-for="ch in chapters" :key="ch.id" :label="ch.name" :value="ch.id" />
          <el-option label="未分配章节" :value="0" />
        </el-select>
        <el-select v-model="filters.question_type_id" placeholder="选择题型" style="width: 150px;" clearable @change="loadQuestions">
          <el-option v-for="qt in questionTypes" :key="qt.id" :label="qt.name" :value="qt.id" />
        </el-select>
        <el-select v-model="filters.status" placeholder="选择状态" style="width: 120px;" clearable @change="loadQuestions">
          <el-option label="已发布" value="published" />
          <el-option label="草稿" value="draft" />
          <el-option label="隐藏" value="hidden" />
        </el-select>
        <el-select v-model="pageSize" placeholder="每页行数" style="width: 130px;" @change="handlePageSizeChange">
          <el-option label="50行" :value="50" />
          <el-option label="100行" :value="100" />
          <el-option label="150行" :value="150" />
          <el-option label="200行" :value="200" />
          <el-option label="500行" :value="500" />
          <el-option label="1000行" :value="1000" />
        </el-select>
      </div>

      <div style="margin-bottom: 15px;">
        <el-button size="small" @click="batchMoveChapter" :disabled="selectedIds.length === 0">批量移动章节</el-button>
        <el-button size="small" @click="batchChangeType" :disabled="selectedIds.length === 0">批量修改题型</el-button>
        <el-button size="small" @click="batchChangeStatus" :disabled="selectedIds.length === 0">批量修改状态</el-button>
        <el-button size="small" type="danger" @click="batchDelete" :disabled="selectedIds.length === 0">批量删除</el-button>
        <span style="margin-left: 15px; color: #666;">已选中 {{ selectedIds.length }} 项</span>
      </div>

      <el-table ref="tableRef" :data="questions" style="width: 100%" @selection-change="handleSelectionChange" v-loading="loading">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="stem" label="题干" min-width="200">
          <template #default="{ row }">
            <div v-html="row.stem_html || row.stem"></div>
          </template>
        </el-table-column>
        <el-table-column prop="question_type_name" label="题型" width="100" />
        <el-table-column prop="chapter_name" label="章节" width="120" />
        <el-table-column prop="answer" label="答案" width="80">
          <template #default="{ row }">
            <el-tag type="success">{{ row.answer }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'published' ? 'success' : row.status === 'draft' ? 'warning' : 'info'">
              {{ statusMap[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="editQuestion(row.id)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteQuestion(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, sizes, prev, pager, next"
        :page-sizes="[50, 100, 150, 200, 500, 1000]"
        style="margin-top: 20px; justify-content: center;"
        @current-change="loadQuestions"
        @size-change="handlePageSizeChange"
      />
    </div>

    <el-dialog v-model="showBatchDialog" title="批量操作" width="400px">
      <div v-if="batchAction === 'move_chapter'">
        <el-select v-model="batchChapterId" placeholder="选择目标章节" style="width: 100%;">
          <el-option v-for="ch in chapters" :key="ch.id" :label="ch.name" :value="ch.id" />
        </el-select>
      </div>
      <div v-if="batchAction === 'change_type'">
        <el-select v-model="batchTypeId" placeholder="选择目标题型" style="width: 100%;">
          <el-option v-for="qt in questionTypes" :key="qt.id" :label="qt.name" :value="qt.id" />
        </el-select>
      </div>
      <div v-if="batchAction === 'change_status'">
        <el-select v-model="batchStatus" placeholder="选择状态" style="width: 100%;">
          <el-option label="已发布" value="published" />
          <el-option label="草稿" value="draft" />
          <el-option label="隐藏" value="hidden" />
        </el-select>
      </div>
      <template #footer>
        <el-button @click="showBatchDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmBatch">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useQuizStore } from '@/store/quiz'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const store = useQuizStore()

const questions = ref([])
const chapters = ref([])
const questionTypes = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(50)
const total = ref(0)
const selectedIds = ref([])
const tableRef = ref(null)

const filters = ref({
  stem: '',
  chapter_id: null,
  question_type_id: null,
  status: ''
})

const statusMap = {
  published: '已发布',
  draft: '草稿',
  hidden: '隐藏'
}

const showBatchDialog = ref(false)
const batchAction = ref('')
const batchChapterId = ref(null)
const batchTypeId = ref(null)
const batchStatus = ref('')

const handlePageSizeChange = () => {
  currentPage.value = 1
  loadQuestions()
}

const loadQuestions = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value,
      ...filters.value
    }
    const result = await store.loadQuestions(params)
    questions.value = result.data
    total.value = result.total
    chapters.value = store.chapters
    questionTypes.value = store.questionTypes
  } catch (error) {
    ElMessage.error('加载题目失败')
  } finally {
    loading.value = false
  }
}

const handleSelectionChange = (selection) => {
  selectedIds.value = selection.map(item => item.id)
}

const editQuestion = (id) => {
  router.push(`/questions/${id}/edit`)
}

const deleteQuestion = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这道题目吗？', '提示', { type: 'warning' })
    await store.deleteQuestion(id)
    ElMessage.success('删除成功')
    loadQuestions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const batchMoveChapter = () => {
  batchAction.value = 'move_chapter'
  showBatchDialog.value = true
}

const batchChangeType = () => {
  batchAction.value = 'change_type'
  showBatchDialog.value = true
}

const batchChangeStatus = () => {
  batchAction.value = 'change_status'
  showBatchDialog.value = true
}

const confirmBatch = async () => {
  try {
    let data = {
      question_ids: selectedIds.value,
      action: batchAction.value
    }
    if (batchAction.value === 'move_chapter') {
      data.chapter_id = batchChapterId.value
    } else if (batchAction.value === 'change_type') {
      data.question_type_id = batchTypeId.value
    } else if (batchAction.value === 'change_status') {
      data.status = batchStatus.value
    }
    await store.batchOperateQuestions(data)
    ElMessage.success('批量操作成功')
    showBatchDialog.value = false
    loadQuestions()
  } catch (error) {
    ElMessage.error('批量操作失败')
  }
}

const batchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 道题目吗？`, '警告', { type: 'warning' })
    await store.batchOperateQuestions({
      question_ids: selectedIds.value,
      action: 'delete'
    })
    ElMessage.success('批量删除成功')
    loadQuestions()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
    }
  }
}

const exportSelected = async () => {
  await store.exportQuestions(selectedIds.value)
  ElMessage.success('导出成功')
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.questions-view {
  padding: 20px;
}

.filter-bar > * {
  flex-shrink: 0;
}
</style>
