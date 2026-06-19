<template>
  <div class="practice-memory-view" :style="`--dynamic-font-size: ${fontSize}px`">
    <!-- 返回按钮 -->
    <div class="back-header">
      <el-button type="info" @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
        返回刷题规划
      </el-button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>正在加载题目...</span>
    </div>

    <!-- 无题目状态 -->
    <div v-else-if="tasks.length === 0" class="empty-state">
      <el-icon size="64" color="#ccc"><VideoPlay /></el-icon>
      <h3>暂无刷题任务</h3>
      <p>请先在刷题规划中添加题目</p>
      <el-button type="primary" @click="goBack">返回刷题规划</el-button>
    </div>

    <!-- 刷题内容 -->
    <div v-else class="practice-content">
      <!-- 进度信息 -->
      <div class="progress-info">
        <span class="progress-text">
          进度：{{ currentIndex + 1 }} / {{ tasks.length }}
        </span>
        <span class="status-indicator" :class="currentTask?.status === 'learning' ? 'status-learning' : 'status-reviewing'">
          {{ currentTask?.status === 'learning' ? '初学中' : '复习中' }}
        </span>
      </div>

      <!-- 设置栏 -->
      <div class="settings-bar">
        <div class="settings-item">
          <span>字体大小:</span>
          <el-button size="small" @click="decreaseFontSize">-</el-button>
          <span class="font-size-value">{{ fontSize }}px</span>
          <el-button size="small" @click="increaseFontSize">+</el-button>
        </div>
      </div>

      <!-- 题目卡片 -->
      <div v-if="currentTask" class="question-card">
        <div class="question-header">
          <span class="chapter-tag">{{ currentTask.chapter_name }}</span>
          <span class="question-type-tag">{{ currentTask.question_type_name }}</span>
        </div>
        
        <!-- 题干 -->
        <div class="question-stem" :style="{ fontSize: fontSize + 'px' }">
          <span v-html="currentTask.stem_html || currentTask.stem"></span>
        </div>

        <!-- 选项 -->
        <div class="options-container" v-if="currentTask.option_a">
          <div 
            v-for="(label, key) in optionLabels" 
            :key="key"
            class="option-item"
            :class="{ 
              'selected': selectedAnswer === key,
              'correct': showAnswer && key.toUpperCase() === currentTask.answer.toUpperCase(),
              'incorrect': showAnswer && selectedAnswer === key && selectedAnswer !== currentTask.answer
            }"
            @click="selectAnswer(key)"
          >
            <span class="option-label">{{ key }}.</span>
            <span class="option-text" v-html="getOptionHtml(key)"></span>
          </div>
        </div>

        <!-- 答案显示 -->
        <div v-if="showAnswer" class="answer-section">
          <div class="answer-result" :class="isCorrect ? 'correct-answer' : 'wrong-answer'">
            <span v-if="isCorrect" class="result-icon">✓</span>
            <span v-else class="result-icon">✗</span>
            <span class="result-text">{{ isCorrect ? '答案正确' : '答案错误' }}</span>
            <span v-if="!isCorrect" class="correct-answer-text">
              正确答案：{{ currentTask.answer.toUpperCase() }}
            </span>
          </div>
        </div>

        <!-- 解析 -->
        <div v-if="showAnswer && currentTask.explanation" class="explanation-section">
          <div class="explanation-label">解析：</div>
          <div class="explanation-content" :style="{ fontSize: fontSize + 'px' }">
            <span v-html="currentTask.explanation_html || currentTask.explanation"></span>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button 
          v-if="!showAnswer" 
          type="primary" 
          size="large" 
          :disabled="!selectedAnswer"
          @click="submitAnswer"
        >
          确认答案
        </el-button>
        <el-button 
          v-if="showAnswer" 
          type="success" 
          size="large"
          @click="handleFeedback('correct')"
        >
          <span class="btn-icon">✓</span>
          答案正确
        </el-button>
        <el-button 
          v-if="showAnswer" 
          type="danger" 
          size="large"
          @click="handleFeedback('wrong')"
        >
          <span class="btn-icon">✗</span>
          答案错误
        </el-button>
        <el-button 
          v-if="showAnswer && tasks.length > 0" 
          type="primary" 
          size="large"
          @click="nextTask"
        >
          下一题
        </el-button>
      </div>

      <!-- 提示信息 -->
      <div v-if="message" class="message-tip" :class="messageType">
        {{ message }}
      </div>
    </div>

    <!-- 完成弹窗 -->
    <el-dialog v-model="showCompleteDialog" title="刷题完成" width="400px" :close-on-click-modal="false">
      <div class="complete-content">
        <el-icon size="64" color="#52c41a"><SuccessFilled /></el-icon>
        <h3>恭喜！今日刷题任务已完成</h3>
        <p>你已经完成了所有的刷题任务</p>
      </div>
      <template #footer>
        <el-button type="primary" @click="returnToPlan">返回刷题规划</el-button>
        <el-button @click="refreshTasks">继续刷题</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ArrowLeft, Loading, VideoPlay, SuccessFilled } from '@element-plus/icons-vue'

const tasks = ref([])
const currentIndex = ref(0)
const selectedAnswer = ref('')
const showAnswer = ref(false)
const isCorrect = ref(false)
const loading = ref(true)
const message = ref('')
const messageType = ref('')
const showCompleteDialog = ref(false)
const fontSize = ref(18)

const optionLabels = {
  'A': 'A',
  'B': 'B',
  'C': 'C',
  'D': 'D',
  'E': 'E',
  'F': 'F'
}

const currentTask = computed(() => {
  if (tasks.value.length === 0 || currentIndex.value >= tasks.value.length) {
    return null
  }
  return tasks.value[currentIndex.value]
})

const goBack = () => {
  window.location.href = '/memory/practice/plan'
}

const returnToPlan = () => {
  showCompleteDialog.value = false
  goBack()
}

const refreshTasks = async () => {
  showCompleteDialog.value = false
  await loadTasks()
}

const getOptionHtml = (key) => {
  if (!currentTask.value) return ''
  const optionKey = `option_${key.toLowerCase()}`
  const htmlKey = `${optionKey}_html`
  return currentTask.value[htmlKey] || currentTask.value[optionKey] || ''
}

const selectAnswer = (key) => {
  if (showAnswer.value) return
  selectedAnswer.value = key
}

const submitAnswer = async () => {
  if (!selectedAnswer.value || !currentTask.value) return
  
  const correct = selectedAnswer.value.toUpperCase() === currentTask.value.answer.toUpperCase()
  isCorrect.value = correct
  showAnswer.value = true
}

const handleFeedback = async (feedback) => {
  if (!currentTask.value) return
  
  const recordId = currentTask.value.id
  
  try {
    const res = await axios.post('/api/practice-plan/feedback?user_id=default_user', {
      record_id: recordId,
      feedback: feedback
    })
    
    if (res.data.status === 'ok') {
      const updatedRecord = res.data.data
      
      if (updatedRecord.completed === true && feedback === 'correct') {
        message.value = '恭喜！该题已完成当次刷题任务'
        messageType.value = 'success'
      } else if (feedback === 'correct') {
        message.value = '正确！请继续答题'
        messageType.value = 'success'
      } else {
        message.value = '错误！该题将在后续继续出现'
        messageType.value = 'error'
      }
      
      setTimeout(() => {
        loadTasks()
      }, 1000)
    }
  } catch (error) {
    console.error('提交反馈失败:', error)
    message.value = '提交反馈失败'
    messageType.value = 'error'
  }
}

const nextTask = () => {
  if (currentIndex.value < tasks.value.length - 1) {
    currentIndex.value++
  } else {
    // 到达末尾，检查是否还有未完成任务
    message.value = '已到最后一道题'
    messageType.value = 'info'
  }
  resetQuestionState()
}

const resetQuestionState = () => {
  selectedAnswer.value = ''
  showAnswer.value = false
  isCorrect.value = false
  message.value = ''
}

const increaseFontSize = () => {
  if (fontSize.value < 28) {
    fontSize.value += 2
  }
}

const decreaseFontSize = () => {
  if (fontSize.value > 12) {
    fontSize.value -= 2
  }
}

const loadTasks = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/practice-plan/tasks?user_id=default_user')
    tasks.value = res.data.data || []
    currentIndex.value = 0
    resetQuestionState()
  } catch (error) {
    console.error('加载任务失败:', error)
    tasks.value = []
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadTasks()
})
</script>

<style scoped>
.practice-memory-view {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.back-header {
  margin-bottom: 20px;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 0;
  color: #666;
}

.empty-state h3 {
  margin: 20px 0 10px;
  color: #333;
}

.empty-state p {
  color: #999;
  margin-bottom: 20px;
}

.practice-content {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.progress-text {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.status-indicator {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
}

.status-indicator.status-learning {
  background: #fffbe6;
  color: #faad14;
}

.status-indicator.status-reviewing {
  background: #f6ffed;
  color: #52c41a;
}

.settings-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.settings-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #666;
}

.font-size-value {
  min-width: 45px;
  text-align: center;
}

.question-card {
  margin-bottom: 20px;
}

.question-header {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.chapter-tag,
.question-type-tag {
  padding: 4px 10px;
  background: #f0f0f0;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
}

.question-stem {
  line-height: 1.8;
  margin-bottom: 20px;
  color: #333;
}

.options-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.option-item {
  display: flex;
  align-items: flex-start;
  padding: 15px;
  background: #f9f9f9;
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.option-item:hover {
  background: #f0f0f0;
}

.option-item.selected {
  border-color: #1890ff;
  background: #e6f7ff;
}

.option-item.correct {
  border-color: #52c41a;
  background: #f6ffed;
}

.option-item.incorrect {
  border-color: #ff4d4f;
  background: #fff2f0;
}

.option-label {
  font-weight: bold;
  margin-right: 10px;
  color: #333;
}

.option-text {
  flex: 1;
  line-height: 1.6;
}

.answer-section {
  margin-bottom: 20px;
}

.answer-result {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 8px;
  gap: 10px;
}

.answer-result.correct-answer {
  background: #f6ffed;
  border: 1px solid #b7eb8f;
}

.answer-result.wrong-answer {
  background: #fff2f0;
  border: 1px solid #ffccc7;
}

.result-icon {
  font-size: 24px;
  font-weight: bold;
}

.correct-answer .result-icon {
  color: #52c41a;
}

.wrong-answer .result-icon {
  color: #ff4d4f;
}

.result-text {
  font-size: 18px;
  font-weight: 500;
}

.correct-answer-text {
  margin-left: auto;
  color: #52c41a;
  font-weight: 500;
}

.explanation-section {
  background: #fafafa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.explanation-label {
  font-weight: 500;
  color: #333;
  margin-bottom: 10px;
}

.explanation-content {
  line-height: 1.8;
  color: #666;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
}

.action-buttons .el-button {
  min-width: 120px;
}

.btn-icon {
  margin-right: 5px;
}

.message-tip {
  text-align: center;
  padding: 10px;
  margin-top: 15px;
  border-radius: 4px;
}

.message-tip.success {
  background: #f6ffed;
  color: #52c41a;
}

.message-tip.error {
  background: #fff2f0;
  color: #ff4d4f;
}

.message-tip.info {
  background: #e6f7ff;
  color: #1890ff;
}

.complete-content {
  text-align: center;
  padding: 20px 0;
}

.complete-content h3 {
  margin: 15px 0 10px;
  color: #333;
}

.complete-content p {
  color: #666;
}
</style>
