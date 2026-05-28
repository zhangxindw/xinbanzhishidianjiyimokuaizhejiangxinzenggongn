<template>
  <div class="favorites-view">
    <div class="page-header">
      <h2>收藏夹</h2>
      <p>收藏的重要题目，方便反复学习</p>
    </div>

    <div class="card">
      <el-table :data="favorites" style="width: 100%" v-loading="loading">
        <el-table-column prop="question.id" label="ID" width="80" />
        <el-table-column prop="question.stem" label="题干" min-width="200">
          <template #default="{ row }">
            <div v-html="row.question?.stem_html || row.question?.stem"></div>
          </template>
        </el-table-column>
        <el-table-column prop="question.question_type_name" label="题型" width="100" />
        <el-table-column prop="question.answer" label="答案" width="80">
          <template #default="{ row }">
            <el-tag type="success">{{ row.question?.answer }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="收藏时间" width="160">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" type="text" @click="viewQuestion(row)">查看</el-button>
            <el-button size="small" type="text" danger @click="removeFavorite(row)">取消收藏</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        style="margin-top: 20px; justify-content: center;"
        @current-change="loadFavorites"
      />
    </div>

    <el-dialog v-model="dialogVisible" title="题目详情" width="700px">
      <div v-if="currentQuestion" class="question-detail">
        <div class="detail-stem" v-html="currentQuestion.stem_html || currentQuestion.stem"></div>
        <div class="detail-options">
          <div v-for="(label, idx) in ['A', 'B', 'C', 'D', 'E', 'F']" :key="label" class="detail-option">
            <span class="option-label">{{ label }}</span>
            <span v-html="currentQuestion[`option_${label.toLowerCase()}_html`] || currentQuestion[`option_${label.toLowerCase()}`]"></span>
          </div>
        </div>
        <div class="detail-answer">
          <strong>答案：</strong>{{ currentQuestion.answer }}
        </div>
        <div class="detail-explanation" v-if="currentQuestion.explanation">
          <strong>解析：</strong>
          <div v-html="currentQuestion.explanation_html || currentQuestion.explanation"></div>
        </div>
      </div>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuizStore } from '@/store/quiz'
import { ElMessage } from 'element-plus'

const store = useQuizStore()

const favorites = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const dialogVisible = ref(false)
const currentQuestion = ref(null)

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  return new Date(timeStr).toLocaleString('zh-CN')
}

const loadFavorites = async () => {
  loading.value = true
  try {
    const result = await store.loadFavorites({
      page: currentPage.value,
      per_page: pageSize.value
    })
    favorites.value = result.data
    total.value = result.total
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const viewQuestion = (row) => {
  currentQuestion.value = row.question
  dialogVisible.value = true
}

const removeFavorite = async (row) => {
  try {
    await store.removeFromFavorites(row.id)
    ElMessage.success('已取消收藏')
    loadFavorites()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  loadFavorites()
})
</script>

<style scoped>
.favorites-view {
  padding: 20px;
}

.question-detail {
  padding: 20px;
}

.detail-stem {
  font-size: 16px;
  line-height: 1.8;
  margin-bottom: 20px;
}

.detail-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.detail-option {
  display: flex;
  gap: 10px;
  padding: 10px;
  background: #f8f8ff;
  border-radius: 4px;
}

.detail-option .option-label {
  font-weight: bold;
  color: #667eea;
}

.detail-answer {
  margin-bottom: 15px;
  color: #52c41a;
}

.detail-explanation {
  color: #666;
  line-height: 1.8;
}
</style>
