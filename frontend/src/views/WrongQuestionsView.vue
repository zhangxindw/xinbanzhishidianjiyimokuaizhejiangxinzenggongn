<template>
  <div class="wrong-questions-view">
    <div class="page-header" style="display: flex; justify-content: space-between; align-items: center;">
      <div>
        <h2>错题本</h2>
        <p>管理所有答错的题目，方便针对性复习</p>
      </div>
      <div>
        <el-button type="primary" @click="startPractice">
          <el-icon><RefreshRight /></el-icon>
          重新练习
        </el-button>
        <el-button type="danger" @click="clearAll">
          <el-icon><Delete /></el-icon>
          清空错题本
        </el-button>
      </div>
    </div>

    <div class="card">
      <div class="filter-bar" style="display: flex; gap: 15px; flex-wrap: wrap; margin-bottom: 20px;">
        <el-select v-model="filters.chapter_id" placeholder="选择章节" style="width: 150px;" clearable @change="loadWrongQuestions">
          <el-option v-for="ch in chapters" :key="ch.id" :label="ch.name" :value="ch.id" />
        </el-select>
        <el-select v-model="filters.question_type_id" placeholder="选择题型" style="width: 150px;" clearable @change="loadWrongQuestions">
          <el-option v-for="qt in questionTypes" :key="qt.id" :label="qt.name" :value="qt.id" />
        </el-select>
      </div>

      <el-table :data="wrongQuestions" style="width: 100%" v-loading="loading">
        <el-table-column prop="question.id" label="ID" width="80" />
        <el-table-column prop="question.stem" label="题干" min-width="200">
          <template #default="{ row }">
            <div v-html="row.question?.stem_html || row.question?.stem"></div>
          </template>
        </el-table-column>
        <el-table-column prop="question.question_type_name" label="题型" width="100" />
        <el-table-column prop="wrong_count" label="错误次数" width="100">
          <template #default="{ row }">
            <el-tag type="danger">{{ row.wrong_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_wrong_at" label="最近错误" width="160">
          <template #default="{ row }">
            {{ formatTime(row.last_wrong_at) }}
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
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        style="margin-top: 20px; justify-content: center;"
        @current-change="loadWrongQuestions"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuizStore } from '@/store/quiz'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const store = useQuizStore()

const wrongQuestions = ref([])
const chapters = ref([])
const questionTypes = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const filters = ref({
  chapter_id: null,
  question_type_id: null
})

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  return new Date(timeStr).toLocaleString('zh-CN')
}

const loadWrongQuestions = async () => {
  loading.value = true
  try {
    const result = await store.loadWrongQuestions({
      page: currentPage.value,
      per_page: pageSize.value,
      ...filters.value
    })
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

onMounted(() => {
  loadWrongQuestions()
})
</script>

<style scoped>
.wrong-questions-view {
  padding: 20px;
}
</style>
