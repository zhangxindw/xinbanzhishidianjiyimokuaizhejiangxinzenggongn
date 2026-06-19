<template>
  <div class="mobile-practice">
    <!-- 顶部标题栏 -->
    <header class="mobile-header">
      <div class="header-content">
        <button class="back-btn" @click="goBack">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg>
        </button>
        <div class="header-title">
          <h1>记忆刷题</h1>
          <span v-if="practiceStarted" class="progress-badge">剩余 {{ memoryRemainCount }} 题</span>
        </div>
      </div>
      <div class="header-right">
        <div class="font-size-controls">
          <span class="font-label">字号</span>
          <div class="font-buttons">
            <button class="font-btn" :class="{ active: fontSize === 'normal' }" @click="setFontSize('normal')">标</button>
            <button class="font-btn" :class="{ active: fontSize === 'large' }" @click="setFontSize('large')">大</button>
            <button class="font-btn" :class="{ active: fontSize === 'xlarge' }" @click="setFontSize('xlarge')">特大</button>
          </div>
        </div>
      </div>
      <div class="header-bg"></div>
    </header>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-screen">
      <div class="loading-spinner"></div>
      <span>正在加载题目...</span>
    </div>

    <!-- 无题目状态 -->
    <div v-else-if="!practiceStarted && tasks.length === 0" class="empty-screen">
      <svg viewBox="0 0 1024 1024" class="empty-icon"><path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768m0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896"></path></svg>
      <h3>暂无刷题任务</h3>
      <p>请先在刷题规划中添加题目</p>
      <button class="action-btn primary" @click="goToPlan">前往刷题规划</button>
    </div>

    <!-- 刷题界面 -->
    <div v-if="practiceStarted && currentQuestion" class="practice-screen" :class="`font-${fontSize}`">
      <!-- 状态指示 -->
      <div class="status-bar">
        <span class="status-badge" :class="currentStatus === 'learning' ? 'learning' : 'reviewing'">
          {{ currentStatus === 'learning' ? '初学中' : '复习中' }}
        </span>
        <span v-if="currentCorrectAtLearning > 0" class="correct-count">已答对 {{ currentCorrectAtLearning }} 次</span>
      </div>

      <!-- 题目卡片 -->
      <div class="question-card">
        <div class="question-header">
          <span class="question-badge">单选题</span>
          <span class="question-id">#{{ currentQuestion.id }}</span>
        </div>
        <div class="question-text" v-html="currentQuestion.stem_html || currentQuestion.stem"></div>
      </div>

      <!-- 选项列表 -->
      <div class="options-list">
        <div v-for="option in currentQuestion.options" :key="option.label" class="option-item" :class="{ selected: selectedOption === option.label, correct: showAnswer && option.label === currentQuestion.answer, wrong: showAnswer && selectedOption === option.label && option.label !== currentQuestion.answer }" @click="selectOption(option.label)">
          <span class="option-label">{{ option.label }}</span>
          <span class="option-text" v-html="option.text"></span>
          <div v-if="showAnswer && option.label === currentQuestion.answer" class="option-icon correct">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768m0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896"></path></svg>
          </div>
          <div v-if="showAnswer && selectedOption === option.label && option.label !== currentQuestion.answer" class="option-icon wrong">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="m466.752 512-90.496-90.496a32 32 0 0 1 45.248-45.248L512 466.752l90.496-90.496a32 32 0 1 1 45.248 45.248L557.248 512l90.496 90.496a32 32 0 1 1-45.248 45.248L512 557.248l-90.496 90.496a32 32 0 0 1-45.248-45.248z"></path></svg>
          </div>
        </div>
      </div>

      <!-- 答案和解析 -->
      <div v-if="showAnswer" class="answer-row">
        <div class="answer-card">
          <div class="answer-header">
            <span class="answer-badge">正确答案</span>
            <span class="answer-value">{{ currentQuestion.answer }}</span>
          </div>
        </div>
        <button class="next-btn" @click="nextQuestion">
          {{ memoryRemainCount > 0 ? '下一题' : '完成练习' }}
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M716.8 537.6a12.8 12.8 0 0 1 0 17.92L332.8 940.8a12.8 12.8 0 0 1-17.92-17.92l371.2-371.2-371.2-371.2a12.8 12.8 0 1 1 17.92-17.92z"></path></svg>
        </button>
      </div>

      <!-- 解析 -->
      <div v-if="showAnswer && (currentQuestion.explanation || currentQuestion.explanation_html)" class="explanation-card" style="margin-top: 12px;">
        <div class="explanation-header">
          <svg class="explanation-icon" viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768m0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896"></path></svg>
          <span>解析</span>
        </div>
        <div class="explanation-text" v-html="currentQuestion.explanation_html || currentQuestion.explanation"></div>
      </div>

      <!-- 提交答案按钮 -->
      <div v-if="!showAnswer" class="action-buttons">
        <button class="submit-btn" @click="submitAnswer" :disabled="!selectedOption">提交答案</button>
      </div>
    </div>

    <!-- 完成界面 -->
    <div v-if="practiceStarted && !currentQuestion" class="complete-screen">
      <div class="result-dialog">
        <div class="result-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2dd 100%)">
          <div class="result-icon">🎉</div>
          <div class="result-title">练习完成</div>
        </div>
        <div class="result-content">
          <div class="tip-card" style="borderLeftColor: #667eea">
            <div class="tip-header">
              <span class="tip-icon">💡</span>
              <span class="tip-title" style="color: #667eea">今日任务已完成</span>
            </div>
            <div class="tip-content">所有题目都已按要求完成，继续保持学习！</div>
          </div>
        </div>
        <div class="result-actions">
          <button class="home-btn" @click="goHome">返回首页</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuizStore } from '@/store/quiz'
import axios from 'axios'

const router = useRouter()
const store = useQuizStore()

const loading = ref(true)
const tasks = ref([])
const questions = ref([])
const currentIndex = ref(0)
const currentQuestion = computed(() => questions.value[currentIndex.value] || null)
const selectedOption = ref('')
const showAnswer = ref(false)
const practiceStarted = ref(false)

// 记忆刷题状态
const memoryQuestionStatus = ref({})
const memoryRemainCount = ref(0)
const fontSize = ref(localStorage.getItem('practiceFontSize') || 'normal')

const currentStatus = computed(() => {
  if (!currentQuestion.value) return 'learning'
  const status = memoryQuestionStatus.value[currentQuestion.value.id]
  return status?.status || 'learning'
})

const currentCorrectAtLearning = computed(() => {
  if (!currentQuestion.value) return 0
  const status = memoryQuestionStatus.value[currentQuestion.value.id]
  return status?.correctAtLearning || 0
})

// 数组洗牌函数
const shuffleArray = (array) => {
  const newArray = [...array]
  for (let i = newArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[newArray[i], newArray[j]] = [newArray[j], newArray[i]]
  }
  return newArray
}

// 打乱选项顺序
const shuffleOptions = (question) => {
  if (!question.options || question.options.length === 0) return question
  
  // 记录原始答案对应的选项文本
  const currentAnswer = question.answer
  const correctOption = question.options.find(opt => opt.label === currentAnswer)
  const correctOptionText = correctOption ? correctOption.text : null
  
  // 打乱选项
  const shuffledOptions = shuffleArray([...question.options])
  const labels = ['A', 'B', 'C', 'D', 'E', 'F']
  
  // 重新分配标签
  let newAnswer = ''
  for (let i = 0; i < shuffledOptions.length; i++) {
    shuffledOptions[i].label = labels[i]
    // 通过文本匹配找到正确答案的新位置
    if (correctOptionText && shuffledOptions[i].text === correctOptionText) {
      newAnswer = labels[i]
    }
  }
  
  question.options = shuffledOptions
  question.answer = newAnswer || currentAnswer
  question.shuffled = true
  
  return question
}

const loadTasks = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/practice-plan/tasks', {
      params: { user_id: store.userId || 'default_user' }
    })
    
    if (res.data.status === 'ok') {
      tasks.value = res.data.data || []
      
      if (tasks.value.length > 0) {
        // 初始化状态
        memoryQuestionStatus.value = {}
        
        for (const t of tasks.value) {
          memoryQuestionStatus.value[t.question_id] = {
            correctAtLearning: t.correct_at_learning_count || 0,
            wrongCount: 0,
            completed: t.completed || false,
            status: t.status || 'learning',
            record_id: t.id
          }
        }
        
        // 构建题目队列 - 直接使用任务数据，因为题目信息已经展开到顶层
        questions.value = tasks.value.map(t => {
          // 构建选项
          const options = []
          const labels = ['A', 'B', 'C', 'D', 'E', 'F']
          const optionKeys = ['option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'option_f']
          const optionHtmlKeys = ['option_a_html', 'option_b_html', 'option_c_html', 'option_d_html', 'option_e_html', 'option_f_html']
          
          for (let i = 0; i < labels.length; i++) {
            const value = t[optionKeys[i]]
            if (value) {
              options.push({
                label: labels[i],
                text: t[optionHtmlKeys[i]] || value
              })
            }
          }
          
          return {
            id: t.question_id,
            stem: t.stem,
            stem_html: t.stem_html,
            answer: t.answer,
            explanation: t.explanation,
            explanation_html: t.explanation_html,
            chapter_name: t.chapter_name,
            question_type_name: t.question_type_name,
            options: options,
            original_answer: t.answer,
            record_id: t.id,
            status: t.status
          }
        }).filter(q => q && q.stem)
        
        // 复习状态的题目打乱选项
        for (const q of questions.value) {
          const status = memoryQuestionStatus.value[q.id]
          if (status?.status === 'reviewing') {
            shuffleOptions(q)
          }
        }
        
        memoryRemainCount.value = questions.value.length
        practiceStarted.value = true
        currentIndex.value = 0
      }
    }
  } catch (e) {
    console.error('Failed to load tasks:', e)
  }
  loading.value = false
}

const selectOption = (label) => {
  if (showAnswer.value) return
  selectedOption.value = label
}

const submitAnswer = async () => {
  if (!selectedOption.value || !currentQuestion.value) return
  
  showAnswer.value = true
  
  const questionId = currentQuestion.value.id
  const status = memoryQuestionStatus.value[questionId]
  const isCorrect = selectedOption.value === currentQuestion.value.answer
  
  // 提交反馈到后端
  try {
    const res = await axios.post('/api/practice-plan/feedback', {
      record_id: status.record_id,
      feedback: isCorrect ? 'correct' : 'wrong',
      user_id: store.userId
    })
    
    if (res.data.status === 'ok') {
      const data = res.data.data
      status.correctAtLearning = data.correct_at_learning_count || 0
      status.completed = data.completed || false
      status.status = data.status || status.status
      
      if (status.completed) {
        memoryRemainCount.value--
      }
    }
  } catch (e) {
    console.error('Submit feedback failed:', e)
  }
  
  // 提交答案记录
  try {
    await store.submitAnswer(currentQuestion.value.id, selectedOption.value, currentQuestion.value.answer)
  } catch (e) {
    console.error('Submit answer failed:', e)
  }
}

const nextQuestion = () => {
  // 找下一个未完成的题目
  let nextIdx = currentIndex.value + 1
  while (nextIdx < questions.value.length) {
    const nextQ = questions.value[nextIdx]
    if (!memoryQuestionStatus.value[nextQ.id]?.completed) {
      currentIndex.value = nextIdx
      selectedOption.value = ''
      showAnswer.value = false
      // 复习状态或初学阶段第二次出现时重新打乱选项
      const status = memoryQuestionStatus.value[nextQ.id]
      if (status?.status === 'reviewing' || (status?.status === 'learning' && status?.correctAtLearning >= 1)) {
        shuffleOptions(questions.value[nextIdx])
      }
      window.scrollTo({ top: 0, behavior: 'smooth' })
      return
    }
    nextIdx++
  }
  
  // 检查是否还有未完成的题目
  if (memoryRemainCount.value > 0) {
    for (let i = 0; i < questions.value.length; i++) {
      if (!memoryQuestionStatus.value[questions.value[i].id]?.completed) {
        currentIndex.value = i
        selectedOption.value = ''
        showAnswer.value = false
        // 复习状态或初学阶段第二次出现时重新打乱选项
        const status = memoryQuestionStatus.value[questions.value[i].id]
        if (status?.status === 'reviewing' || (status?.status === 'learning' && status?.correctAtLearning >= 1)) {
          shuffleOptions(questions.value[i])
        }
        window.scrollTo({ top: 0, behavior: 'smooth' })
        return
      }
    }
  }
  
  // 所有题目都完成了
  questions.value = []
}

const goBack = () => {
  router.push('/mobile')
}

const goHome = () => {
  router.push('/mobile')
}

const goToPlan = () => {
  router.push('/memory/practice/plan')
}

const setFontSize = (size) => {
  fontSize.value = size
  localStorage.setItem('practiceFontSize', size)
}

onMounted(async () => {
  await loadTasks()
})
</script>

<style scoped>
@import './MobilePracticeView.css';

/* 状态栏优化 */
.status-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  margin-bottom: 16px;
  border: 1px solid #e2e8f0;
}

.status-badge {
  font-size: 13px;
  padding: 6px 14px;
  border-radius: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-badge.learning {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.status-badge.learning::before {
  content: '📚';
}

.status-badge.reviewing {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.status-badge.reviewing::before {
  content: '🔄';
}

.correct-count {
  font-size: 13px;
  color: #64748b;
  background: white;
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

/* 加载状态优化 */
.loading-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  padding: 40px;
  text-align: center;
  background: linear-gradient(180deg, #f8fafc 0%, #fff 100%);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

.loading-screen span {
  font-size: 15px;
  color: #64748b;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 空状态优化 */
.empty-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  padding: 40px;
  text-align: center;
  background: linear-gradient(180deg, #f8fafc 0%, #fff 100%);
}

.empty-icon {
  width: 80px;
  height: 80px;
  color: #94a3b8;
  margin-bottom: 20px;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.empty-screen h3 {
  font-size: 20px;
  color: #334155;
  margin-bottom: 10px;
  font-weight: 600;
}

.empty-screen p {
  font-size: 15px;
  color: #64748b;
  margin-bottom: 28px;
  line-height: 1.5;
}

.empty-screen .action-btn.primary {
  padding: 14px 28px;
  font-size: 15px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.empty-screen .action-btn.primary:active {
  transform: scale(0.98);
}

/* 完成界面优化 */
.complete-screen {
  padding: 20px;
  min-height: calc(100vh - 100px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #f8fafc 0%, #fff 100%);
}

.result-dialog {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-header {
  padding: 36px 24px;
  text-align: center;
  color: white;
  position: relative;
}

.result-icon {
  font-size: 56px;
  margin-bottom: 16px;
  animation: bounce 1s ease infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.result-title {
  font-size: 22px;
  font-weight: 600;
}

.result-content {
  padding: 28px 24px;
}

.tip-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 16px;
  padding: 20px;
  border-left: 4px solid;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.tip-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.tip-icon {
  font-size: 20px;
}

.tip-title {
  font-size: 16px;
  font-weight: 600;
}

.tip-content {
  font-size: 15px;
  color: #64748b;
  line-height: 1.6;
}

.result-actions {
  padding: 20px 24px 28px;
  display: flex;
  gap: 12px;
}

.home-btn {
  flex: 1;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.home-btn:active {
  transform: scale(0.98);
}
</style>