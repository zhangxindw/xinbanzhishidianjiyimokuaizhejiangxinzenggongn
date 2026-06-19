<template>
  <div class="mobile-practice">
    <!-- 顶部标题栏 -->
    <header class="mobile-header">
      <div class="header-content">
        <button class="back-btn" @click="goBack">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg>
        </button>
        <div class="header-title">
          <h1>疯狂刷题</h1>
          <span v-if="practiceStarted" class="progress-badge">剩余 {{ crazyTotalCount - crazyCompletedCount }} 题</span>
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

    <!-- 配置界面 -->
    <div v-if="!practiceStarted" class="config-screen">
      <!-- 章节选择卡片 -->
      <div class="config-card">
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 1024 1024"><path fill="currentColor" d="M384 96a32 32 0 0 1 64 0v786.752a32 32 0 0 1-54.592 22.656L95.936 608a32 32 0 0 1 0-45.312h.128a32 32 0 0 1 45.184 0L384 805.632z"></path></svg>
          <h3>章节选择</h3>
        </div>
        <div class="chapter-list">
          <div v-for="ch in chapters" :key="ch.id" class="chapter-item" :class="{ selected: selectedChapterIds.includes(ch.id) }" @click="toggleChapter(ch.id)">
            <div class="chapter-info">
              <span class="chapter-name">{{ ch.name }}</span>
              <span class="chapter-count">{{ ch.question_count || 0 }} 题目</span>
            </div>
            <div class="chapter-check">
              <svg v-if="selectedChapterIds.includes(ch.id)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
          </div>
        </div>
        <div class="chapter-actions">
          <button class="action-btn outline" @click="selectAllChapters">全选</button>
          <button class="action-btn outline" @click="clearAllChapters">清空</button>
        </div>
      </div>

      <!-- 疯狂刷题配置 -->
      <div class="config-card highlight">
        <div class="card-header">
          <svg class="card-icon crazy" viewBox="0 0 1024 1024"><path fill="currentColor" d="M288 671.36v64.128A239.81 239.81 0 0 1 63.744 496.192a240.32 240.32 0 0 1 199.488-236.8 256.128 256.128 0 0 1 487.872-30.976A256.064 256.064 0 0 1 736 734.016v-64.768a192 192 0 0 0 3.328-377.92l-35.2-6.592-12.8-33.408a192.064 192.064 0 0 0-365.952 23.232l-9.92 40.896-41.472 7.04a176.32 176.32 0 0 0-146.24 173.568c0 91.968 70.464 167.36 160.256 175.232z"></path><path fill="currentColor" d="M416 736a32 32 0 0 1-27.776-47.872l128-224a32 32 0 1 1 55.552 31.744L471.168 672H608a32 32 0 0 1 27.776 47.872l-128 224a32 32 0 1 1-55.68-31.744L552.96 736z"></path></svg>
          <h3>疯狂刷题规则</h3>
        </div>
        <div class="crazy-rules">
          <ul>
            <li>每道题需连续答对两次才能完成</li>
            <li>答错的题目会重新插入队列</li>
            <li>答对一次后题目会再次出现验证</li>
            <li>完成所有题目才算通关</li>
          </ul>
        </div>
        <div class="config-item">
          <span class="config-label">打乱选项</span>
          <div class="switch" :class="{ active: config.shuffleOptions }" @click="config.shuffleOptions = !config.shuffleOptions">
            <span class="switch-text">{{ config.shuffleOptions ? '开启' : '关闭' }}</span>
          </div>
        </div>
      </div>

      <!-- 开始按钮 -->
      <button class="start-btn" @click="startPractice">
        <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768m0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896"></path></svg>
        开始练习
      </button>
    </div>

    <!-- 刷题界面 -->
    <div v-if="practiceStarted && currentQuestion" class="practice-screen" :class="`font-${fontSize}`">
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
          <div class="status-info">
            <span v-if="currentQuestionStatus.correctCount === 1" class="status-badge pending">已答对1次，还需答对1次</span>
            <span v-else-if="currentQuestionStatus.completed" class="status-badge completed">已完成</span>
            <span v-else class="status-badge new">答错，需重新答对2次</span>
          </div>
        </div>
        <button class="next-btn" @click="nextQuestion">
          {{ crazyCompletedCount < crazyTotalCount ? '下一题' : '完成练习' }}
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
        <div class="result-header" style="background: linear-gradient(135deg, #ec4899 0%, #f43f5edd 100%)">
          <div class="result-icon">🏆</div>
          <div class="result-title">通关成功</div>
        </div>
        <div class="result-content">
          <div class="stats-grid">
            <div class="stat-card stat-total">
              <div class="stat-value">{{ crazyTotalCount }}</div>
              <div class="stat-label">总题数</div>
            </div>
            <div class="stat-card stat-completed">
              <div class="stat-value">{{ crazyCompletedCount }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </div>
          <div class="tip-card" style="borderLeftColor: #ec4899">
            <div class="tip-header">
              <span class="tip-icon">💡</span>
              <span class="tip-title" style="color: #ec4899">恭喜通关</span>
            </div>
            <div class="tip-content">所有题目都连续答对两次，太棒了！继续保持！</div>
          </div>
        </div>
        <div class="result-actions">
          <button class="restart-btn" @click="restartPractice">再来一次</button>
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

const chapters = ref([])
const selectedChapterIds = ref([])
const config = ref({
  shuffleOptions: true,
  fontSize: localStorage.getItem('practiceFontSize') || 'normal'
})

const fontSize = ref(localStorage.getItem('practiceFontSize') || 'normal')

const setFontSize = (size) => {
  fontSize.value = size
  config.value.fontSize = size
  localStorage.setItem('practiceFontSize', size)
}

const questions = ref([])
const currentIndex = ref(0)
const currentQuestion = computed(() => questions.value[currentIndex.value] || null)
const selectedOption = ref('')
const showAnswer = ref(false)
const practiceStarted = ref(false)

// 疯狂刷题状态
const crazyQuestionStatus = ref({})
const crazyCompletedCount = ref(0)
const crazyTotalCount = ref(0)

const currentQuestionStatus = computed(() => {
  if (!currentQuestion.value) return { correctCount: 0, wrongCount: 0, completed: false }
  return crazyQuestionStatus.value[currentQuestion.value.id] || { correctCount: 0, wrongCount: 0, completed: false }
})

const toggleChapter = (id) => {
  const index = selectedChapterIds.value.indexOf(id)
  if (index > -1) {
    selectedChapterIds.value.splice(index, 1)
  } else {
    selectedChapterIds.value.push(id)
  }
}

const selectAllChapters = () => {
  selectedChapterIds.value = chapters.value.map(ch => ch.id)
}

const clearAllChapters = () => {
  selectedChapterIds.value = []
}

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

const startPractice = async () => {
  try {
    let apiUrl = '/api/practice/sequential'
    let params = {
      shuffle_options: config.value.shuffleOptions
    }
    if (selectedChapterIds.value.length > 0) {
      params.chapter_ids = selectedChapterIds.value
    }
    
    const res = await axios.post(apiUrl, params)
    const result = res.data
    
    if (result.data && result.data.length > 0) {
      // 获取题目列表
      let questionList = result.data.map(q => {
        const options = []
        const labels = ['A', 'B', 'C', 'D', 'E', 'F']
        const optionKeys = ['option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'option_f']
        const optionHtmlKeys = ['option_a_html', 'option_b_html', 'option_c_html', 'option_d_html', 'option_e_html', 'option_f_html']
        
        for (let i = 0; i < labels.length; i++) {
          const value = q[optionKeys[i]]
          if (value) {
            options.push({
              label: labels[i],
              text: q[optionHtmlKeys[i]] || value
            })
          }
        }
        
        return {
          ...q,
          options: options
        }
      })
      
      // 打乱题目顺序
      questionList = shuffleArray(questionList)
      
      // 如果需要打乱选项
      if (config.value.shuffleOptions) {
        questionList = questionList.map(q => shuffleOptions(q))
      }
      
      questions.value = questionList
      practiceStarted.value = true
      currentIndex.value = 0
      
      // 初始化疯狂刷题状态
      crazyQuestionStatus.value = {}
      for (const q of questionList) {
        crazyQuestionStatus.value[q.id] = {
          correctCount: 0,
          wrongCount: 0,
          completed: false
        }
      }
      crazyTotalCount.value = questionList.length
      crazyCompletedCount.value = 0
    } else {
      alert('没有可用的题目')
    }
  } catch (e) {
    console.error('Failed to start practice:', e)
    alert('加载题目失败')
  }
}

const selectOption = (label) => {
  if (showAnswer.value) return
  selectedOption.value = label
}

const submitAnswer = async () => {
  if (!selectedOption.value || !currentQuestion.value) return
  
  showAnswer.value = true
  
  const questionId = currentQuestion.value.id
  const status = crazyQuestionStatus.value[questionId]
  const isCorrect = selectedOption.value === currentQuestion.value.answer
  
  if (isCorrect) {
    status.correctCount++
    if (status.correctCount >= 2) {
      status.completed = true
      crazyCompletedCount.value++
    }
  } else {
    status.correctCount = 0
    status.wrongCount++
    // 答错的题目重新插入队列末尾
    const questionCopy = JSON.parse(JSON.stringify(currentQuestion.value))
    if (config.value.shuffleOptions) {
      shuffleOptions(questionCopy)
    }
    questions.value.push(questionCopy)
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
    if (!crazyQuestionStatus.value[nextQ.id]?.completed) {
      currentIndex.value = nextIdx
      selectedOption.value = ''
      showAnswer.value = false
      window.scrollTo({ top: 0, behavior: 'smooth' })
      return
    }
    nextIdx++
  }
  
  // 检查是否还有未完成的题目
  if (crazyCompletedCount.value < crazyTotalCount.value) {
    // 从头开始找未完成的题目
    for (let i = 0; i < questions.value.length; i++) {
      if (!crazyQuestionStatus.value[questions.value[i].id]?.completed) {
        currentIndex.value = i
        selectedOption.value = ''
        showAnswer.value = false
        window.scrollTo({ top: 0, behavior: 'smooth' })
        return
      }
    }
  }
  
  // 所有题目都完成了
  questions.value = []
}

const restartPractice = () => {
  practiceStarted.value = false
  questions.value = []
  currentIndex.value = 0
  selectedOption.value = ''
  showAnswer.value = false
  crazyQuestionStatus.value = {}
  crazyCompletedCount.value = 0
  crazyTotalCount.value = 0
}

const goBack = () => {
  router.push('/mobile')
}

const goHome = () => {
  router.push('/mobile')
}

onMounted(async () => {
  try {
    const res = await axios.get('/api/chapters')
    chapters.value = res.data.data || []
  } catch (e) {
    console.error('Failed to load chapters:', e)
  }
})
</script>

<style scoped>
@import './MobilePracticeView.css';

.crazy-rules {
  background: rgba(236, 72, 153, 0.1);
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
}

.crazy-rules ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.crazy-rules li {
  padding: 6px 0;
  font-size: 13px;
  color: #666;
  position: relative;
  padding-left: 20px;
}

.crazy-rules li::before {
  content: '⚡';
  position: absolute;
  left: 0;
  color: #ec4899;
}

.card-icon.crazy {
  color: #ec4899;
}

.status-info {
  margin-top: 8px;
}

.status-badge {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
}

.status-badge.pending {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.status-badge.completed {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.status-badge.new {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.stat-completed .stat-value {
  color: #10b981;
}
</style>