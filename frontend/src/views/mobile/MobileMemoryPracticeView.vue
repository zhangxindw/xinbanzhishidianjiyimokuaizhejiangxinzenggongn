<template>
  <div class="mobile-memory-practice">
    <!-- 顶部标题栏 -->
    <header class="mobile-header">
      <button class="back-btn" @click="goBack">
        <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg>
      </button>
      <h1>记忆练习</h1>
      <div class="header-right">
        <span class="progress">{{ currentIndex + 1 }}/{{ tasks.length }}</span>
      </div>
    </header>

    <!-- 配置界面 -->
    <div v-if="!practiceStarted" class="config-screen">
      <div class="config-card">
        <h3>练习设置</h3>
        <div class="config-item">
          <label>字体大小</label>
          <div class="font-control">
            <button class="font-btn" @click="updateFontSize(Math.max(12, fontSize - 2))">-</button>
            <span class="font-value">{{ fontSize }}px</span>
            <button class="font-btn" @click="updateFontSize(Math.min(32, fontSize + 2))">+</button>
          </div>
        </div>
      </div>

      <div class="preview-info">
        <span>今日需复习：{{ todayCount }}个知识点</span>
      </div>

      <button class="start-btn" @click="startPractice">开始练习</button>
    </div>

    <!-- 练习界面 -->
    <div v-if="practiceStarted && currentTask" class="practice-screen" :style="`--font-size: ${fontSize}px`">
      <!-- 题目卡片 -->
      <div class="question-card">
        <div class="question-header">
          <span class="priority-tag" :class="getPriorityClass(currentTask.knowledge_point.priority)">
            {{ currentTask.knowledge_point.priority_label }}
          </span>
          <span class="chapter-tag">{{ currentTask.knowledge_point.chapter_name }}</span>
        </div>
        <div class="question-text" v-html="currentTask.knowledge_point.question_html"></div>
      </div>

      <!-- 口诀卡片 -->
      <div class="mnemonic-card" @click="showMnemonic = !showMnemonic">
        <div class="mnemonic-header">
          <span class="mnemonic-label">速记口诀</span>
          <span class="mnemonic-toggle">{{ showMnemonic ? '隐藏' : '查看' }}</span>
        </div>
        <div v-if="showMnemonic && currentTask.knowledge_point.mnemonic" class="mnemonic-content">
          {{ currentTask.knowledge_point.mnemonic }}
        </div>
      </div>

      <!-- 答案列表 -->
      <div class="answers-section">
        <div class="answers-header">
          <h3>答案</h3>
          <button class="reveal-btn" @click="revealAllBlanks">显示挖空</button>
          <button class="hide-btn" @click="hideAllBlanks">隐藏挖空</button>
          <button class="toggle-all-btn" :class="{ active: showAllAnswers }" @click="toggleAllAnswers">
            {{ showAllAnswers ? '隐藏答案' : '显示答案' }}
          </button>
        </div>
        <div class="answers-list">
          <div v-for="(item, index) in currentTask.knowledge_point.items" :key="index" class="answer-item">
            <div class="answer-row">
              <span class="answer-index">{{ index + 1 }}.</span>
              <div class="answer-content-wrap">
                <div 
                  class="answer-content" 
                  :class="{ 'answers-hidden': !showAllAnswers }" 
                  v-html="processAnswerContent(item.content_html || item.content)"
                  @click="handleBlankClick"
                >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button class="remember-btn" @click="handleFeedback('remembered')">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 864a256 256 0 1 0 0-512 256 256 0 0 0 0 512zm0 64a320 320 0 1 1 0-640 320 320 0 0 1 0 640z"></path></svg>
          背出了
        </button>
        <button class="fuzzy-btn" @click="handleFeedback('fuzzy')">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 864a256 256 0 1 0 0-512 256 256 0 0 0 0 512zm0 64a320 320 0 1 1 0-640 320 320 0 0 1 0 640z"></path></svg>
          模糊
        </button>
        <button class="forget-btn" @click="handleFeedback('forgot')">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="m466.752 512-90.496-90.496a32 32 0 0 1 45.248-45.248L512 466.752l90.496-90.496a32 32 0 1 1 45.248 45.248L557.248 512l90.496 90.496a32 32 0 1 1-45.248 45.248L512 557.248l-90.496 90.496a32 32 0 0 1-45.248-45.248z"></path></svg>
          背不出
        </button>
      </div>
    </div>

    <!-- 完成界面 -->
    <div v-if="practiceStarted && !currentTask" class="complete-screen">
      <div class="complete-card">
        <div class="complete-icon">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 864a256 256 0 1 0 0-512 256 256 0 0 0 0 512zm0 64a320 320 0 1 1 0-640 320 320 0 0 1 0 640z"></path></svg>
        </div>
        <h2>练习完成</h2>
        <div class="complete-stats">
          <div class="stat-item">
            <span class="stat-value">{{ tasks.length }}</span>
            <span class="stat-label">总数</span>
          </div>
          <div class="stat-item">
            <span class="stat-value remembered">{{ rememberedCount }}</span>
            <span class="stat-label">记住</span>
          </div>
          <div class="stat-item">
            <span class="stat-value forgotten">{{ tasks.length - rememberedCount }}</span>
            <span class="stat-label">未记住</span>
          </div>
        </div>
        <button class="restart-btn" @click="restartPractice">重新练习</button>
        <button class="home-btn" @click="goHome">返回首页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const fontSize = ref(parseInt(localStorage.getItem('memoryFontSize')) || 16)
const practiceStarted = ref(false)
const tasks = ref([])
const currentIndex = ref(0)
const currentTask = computed(() => tasks.value[currentIndex.value] || null)
const showMnemonic = ref(false)
const showAllAnswers = ref(false)
const todayCount = ref(0)

// 保存字体大小到 localStorage
const updateFontSize = (newSize) => {
  fontSize.value = newSize
  localStorage.setItem('memoryFontSize', newSize.toString())
}

const getPriorityClass = (priority) => {
  const classes = {
    'must': 'priority-high',
    'important': 'priority-medium',
    'normal': 'priority-low'
  }
  return classes[priority] || 'priority-low'
}

const processAnswerContent = (content) => {
  if (!content) return ''
  
  const blankStyle = 'background: #f0f0f0; color: transparent; cursor: pointer; padding: 2px 6px; border-radius: 4px; border-bottom: 2px dashed #ccc; user-select: none; display: inline;'
  
  // 处理 [[挖空文本]] 格式
  let processed = content.replace(/\[\[(.*?)\]\]/g, `<span style="${blankStyle}" class="blank-hidden">$1</span>`)
  
  // 处理已有的 <span class="blank-hidden"> 标签，添加内联样式
  processed = processed.replace(/<span class="blank-hidden">([^<]*?)<\/span>/g, 
    `<span style="${blankStyle}" class="blank-hidden">$1</span>`)
  
  return processed
}

const revealAllBlanks = () => {
  setTimeout(() => {
    const blankElements = document.querySelectorAll('.answer-content .blank-hidden')
    blankElements.forEach(el => {
      el.classList.add('blank-revealed')
      el.classList.remove('blank-hidden')
      // 设置显示样式
      el.style.background = '#f6ffed'
      el.style.color = '#333'
      el.style.borderBottom = 'none'
    })
  }, 0)
}

const hideAllBlanks = () => {
  setTimeout(() => {
    const revealedElements = document.querySelectorAll('.answer-content .blank-revealed')
    revealedElements.forEach(el => {
      el.classList.remove('blank-revealed')
      el.classList.add('blank-hidden')
      // 恢复隐藏样式
      el.style.background = '#f0f0f0'
      el.style.color = 'transparent'
      el.style.borderBottom = '2px dashed #ccc'
    })
  }, 0)
}

const toggleAllAnswers = () => {
  showAllAnswers.value = !showAllAnswers.value
}

const handleBlankClick = (event) => {
  let target = event.target
  while (target && target !== event.currentTarget) {
    if (target.classList) {
      if (target.classList.contains('blank-hidden')) {
        // 从隐藏切换到显示
        target.classList.remove('blank-hidden')
        target.classList.add('blank-revealed')
        target.style.background = '#f6ffed'
        target.style.color = '#333'
        target.style.borderBottom = 'none'
        return
      } else if (target.classList.contains('blank-revealed')) {
        // 从显示切换到隐藏
        target.classList.remove('blank-revealed')
        target.classList.add('blank-hidden')
        target.style.background = '#f0f0f0'
        target.style.color = 'transparent'
        target.style.borderBottom = '2px dashed #ccc'
        return
      }
    }
    target = target.parentElement
  }
}

const startPractice = async () => {
  try {
    const res = await axios.get('/api/memory/today-tasks')
    if (res.data.status === 'ok' && res.data.data.length > 0) {
      tasks.value = res.data.data
      practiceStarted.value = true
      currentIndex.value = 0
      showMnemonic.value = false
      showAllAnswers.value = false
    } else {
      alert('没有可练习的知识点')
    }
  } catch (e) {
    console.error('Failed to start practice:', e)
    alert('加载知识点失败')
  }
}

let isProcessingFeedback = false

const handleFeedback = async (feedback) => {
  if (isProcessingFeedback) {
    console.log('正在处理反馈，请等待...')
    return
  }
  
  if (!currentTask.value) return
  
  isProcessingFeedback = true
  
  showMnemonic.value = false
  showAllAnswers.value = false
  
  const currentIdx = currentIndex.value
  const kpId = currentTask.value.knowledge_point.id
  const currentTaskRef = currentTask.value
  
  try {
    const res = await axios.post('/api/memory/feedback', {
      kp_id: kpId,
      feedback
    })
    
    if (!res || !res.data || res.data.status !== 'ok') {
      alert('提交反馈失败')
      return
    }
    
    const updatedRecord = res.data.data
    
    if (!updatedRecord || typeof updatedRecord !== 'object') {
      alert('提交反馈失败: 服务器返回数据异常')
      return
    }
    
    const recordStatus = updatedRecord.status
    
    if (recordStatus === 'reviewing' && feedback === 'remembered') {
      tasks.value.splice(currentIdx, 1)
      
      if (tasks.value.length === 0) {
        alert('今日记忆任务已完成！')
        await startPractice()
        return
      }
      
      if (currentIndex.value >= tasks.value.length) {
        currentIndex.value = Math.max(0, tasks.value.length - 1)
      }
    } else {
      const remainingCount = tasks.value.length - currentIdx - 1
      const taskId = currentTaskRef.knowledge_point.id
      const effectiveLearningRepetition = Math.max(1, updatedRecord.learning_repetition || 0)
      
      tasks.value.splice(currentIdx, 1)
      
      let newPosition = currentIdx + effectiveLearningRepetition
      
      if (newPosition >= tasks.value.length) {
        tasks.value.push(currentTaskRef)
      } else {
        tasks.value.splice(newPosition, 0, currentTaskRef)
      }
      
      if (currentIndex.value >= tasks.value.length) {
        currentIndex.value = tasks.value.length - 1
      }
    }
    
    currentTaskRef.status = recordStatus
    currentTaskRef.today_consecutive_count = updatedRecord.today_consecutive_count || 0
    currentTaskRef.learning_repetition = updatedRecord.learning_repetition
    
  } catch (e) {
    console.error('Failed to record:', e)
    alert('提交反馈失败')
  } finally {
    isProcessingFeedback = false
  }
}

const restartPractice = () => {
  practiceStarted.value = false
  tasks.value = []
  currentIndex.value = 0
  rememberedCount.value = 0
}

const goBack = () => {
  router.push('/mobile')
}

const goHome = () => {
  router.push('/mobile')
}

onMounted(async () => {
  try {
    const previewRes = await axios.get('/api/memory/preview')
    if (previewRes.data.status === 'ok') {
      todayCount.value = previewRes.data.data.today_review_count || 0
    }
  } catch (e) {
    console.error('Failed to load preview:', e)
  }
})
</script>

<style scoped>
.mobile-memory-practice {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 24px;
  padding-top: 66px;
}

.mobile-header {
  background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);
  color: white;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 56px;
}

.back-btn {
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.back-btn svg {
  width: 20px;
  height: 20px;
}

.mobile-header h1 {
  font-size: 18px;
  margin: 0;
}

.header-right {
  font-size: 14px;
}

.config-screen {
  padding: 16px;
}

.config-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.config-card h3 {
  font-size: 16px;
  margin: 0 0 12px;
  color: #333;
}

.config-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.config-item:last-child {
  border-bottom: none;
}

.config-item label {
  font-size: 14px;
  color: #333;
}

.mode-selector {
  display: flex;
  gap: 8px;
}

.mode-btn {
  padding: 8px 16px;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  font-size: 12px;
  color: #666;
}

.mode-btn.active {
  background: #52c41a;
  color: white;
}

.font-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.font-btn {
  width: 32px;
  height: 32px;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  font-size: 16px;
}

.font-value {
  font-size: 14px;
  color: #333;
}

.preview-info {
  text-align: center;
  font-size: 14px;
  color: #666;
  margin-bottom: 16px;
}

.start-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
}

.practice-screen {
  padding: 16px;
}

.question-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.question-header {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.priority-tag {
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
}

.priority-high {
  background: #fff1f0;
  color: #ff4d4f;
}

.priority-medium {
  background: #fff7e6;
  color: #fa8c16;
}

.priority-low {
  background: #e6f7ff;
  color: #1890ff;
}

.chapter-tag {
  font-size: 12px;
  color: #999;
}

/* 全局字体大小覆盖 */
.mobile-memory-practice .question-text {
  font-size: var(--font-size, 16px) !important;
}

.mobile-memory-practice .question-text *,
.mobile-memory-practice .question-text span {
  font-size: inherit !important;
}

.mobile-memory-practice .answer-index {
  font-size: var(--font-size, 16px) !important;
}

.mobile-memory-practice .answer-content,
.mobile-memory-practice .answer-content span,
.mobile-memory-practice .answer-content * {
  font-size: var(--font-size, 16px) !important;
}

.question-text {
  line-height: 1.6;
  color: #333;
}

.mnemonic-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.mnemonic-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mnemonic-label {
  font-size: 14px;
  color: #666;
}

.mnemonic-toggle {
  font-size: 12px;
  color: #52c41a;
}

.mnemonic-content {
  margin-top: 12px;
  font-size: 14px;
  color: #333;
  background: #f6ffed;
  padding: 12px;
  border-radius: 8px;
}

.answers-section {
  background: white;
  border-radius: 12px;
  padding: 16px;
}

.answers-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.answers-header h3 {
  font-size: 16px;
  margin: 0;
  color: #333;
}

.reveal-btn, .hide-btn {
  padding: 6px 12px;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  font-size: 12px;
  color: #666;
}

.reveal-btn {
  background: #52c41a;
  color: white;
}

.toggle-all-btn {
  background: #1890ff;
  color: white;
}

.toggle-all-btn.active {
  background: #666;
}

.answers-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.answer-item {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 12px;
}

.answer-row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.answer-index {
  font-weight: bold;
  color: #52c41a;
  flex-shrink: 0;
}

.answer-content-wrap {
  flex: 1;
}

.answer-content {
  color: #333;
  line-height: 1.6;
}

.answer-content span.blank-hidden {
  background: #f0f0f0 !important;
  color: transparent !important;
  cursor: pointer !important;
  padding: 2px 6px !important;
  border-radius: 4px !important;
  border-bottom: 2px dashed #ccc !important;
  user-select: none !important;
  display: inline !important;
}

.answer-content span.blank-hidden:hover,
.answer-content span.blank-hidden:active {
  background: #e0e0e0 !important;
}

.answer-content span.blank-revealed {
  background: #f6ffed !important;
  color: #333 !important;
  padding: 2px 6px !important;
  border-radius: 4px !important;
  display: inline !important;
}

.answer-content.answers-hidden {
  visibility: hidden;
}

.answer-content.answers-hidden .blank-hidden,
.answer-content.answers-hidden .blank-revealed {
  visibility: visible;
}



.action-buttons {
  padding: 16px;
  display: flex;
  gap: 8px;
}

.remember-btn, .fuzzy-btn, .forget-btn {
  flex: 1;
  padding: 14px 8px;
  border: none;
  border-radius: 12px;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.remember-btn {
  background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);
  color: white;
}

.fuzzy-btn {
  background: linear-gradient(135deg, #faad14 0%, #ffc53d 100%);
  color: white;
}

.forget-btn {
  background: linear-gradient(135deg, #ff4d4f 0%, #ff7875 100%);
  color: white;
}

.remember-btn svg, .fuzzy-btn svg, .forget-btn svg {
  width: 18px;
  height: 18px;
}

.complete-screen {
  padding: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}

.complete-card {
  background: white;
  border-radius: 12px;
  padding: 32px;
  text-align: center;
  width: 100%;
}

.complete-icon {
  width: 60px;
  height: 60px;
  background: #f6ffed;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  color: #52c41a;
}

.complete-icon svg {
  width: 32px;
  height: 32px;
}

.complete-card h2 {
  font-size: 20px;
  margin: 0 0 24px;
  color: #333;
}

.complete-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 24px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.stat-value.remembered {
  color: #52c41a;
}

.stat-value.forgotten {
  color: #ff4d4f;
}

.stat-label {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.restart-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  margin-bottom: 12px;
}

.home-btn {
  width: 100%;
  padding: 16px;
  background: white;
  color: #52c41a;
  border: 1px solid #52c41a;
  border-radius: 12px;
  font-size: 16px;
}
</style>