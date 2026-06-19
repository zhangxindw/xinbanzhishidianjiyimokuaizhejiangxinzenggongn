<template>
  <div class="mobile-practice">
    <!-- 顶部标题栏 -->
    <header class="mobile-header">
      <div class="header-content">
        <button class="back-btn" @click="goBack">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg>
        </button>
        <div class="header-title">
          <h1>辨析记忆</h1>
          <span v-if="tasks.length > 0" class="progress-badge">{{ currentIndex + 1 }} / {{ tasks.length }}</span>
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
    <div v-else-if="tasks.length === 0" class="empty-screen">
      <svg viewBox="0 0 1024 1024" class="empty-icon"><path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768m0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896"></path></svg>
      <h3>太棒了！</h3>
      <p>暂无待复习的辨析题</p>
      <button class="action-btn primary" @click="goBack">返回首页</button>
    </div>

    <!-- 刷题界面 -->
    <div v-if="!loading && currentTask" class="practice-screen" :class="`font-${fontSize}`">
      <!-- 状态指示 -->
      <div class="status-bar">
        <span class="status-badge" :class="currentTask.status === 'learning' ? 'learning' : 'reviewing'">
          {{ currentTask.status === 'learning' ? '初学中' : '复习中' }}
        </span>
        <span class="chapter-tag">{{ currentTask.chapter_name || '未分类' }}</span>
      </div>

      <!-- 题目卡片 -->
      <div class="question-card">
        <div class="question-header">
          <span class="question-badge">辨析题</span>
        </div>
        <div class="question-text" v-html="currentTask.question_stem_html || currentTask.question_stem"></div>
      </div>

      <!-- 选项显示 -->
      <div class="option-display-card">
        <div class="option-badge">{{ currentTask.option_key }}.</div>
        <div class="option-text" v-html="currentTask.option_text_html || currentTask.option_text"></div>
      </div>

      <!-- 判断按钮 -->
      <div v-if="!answered" class="judge-buttons">
        <button class="judge-btn correct" @click="submitAnswer('remembered')">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768m0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896"></path></svg>
          <span>正确</span>
        </button>
        <button class="judge-btn wrong" @click="submitAnswer('forgot')">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="m466.752 512-90.496-90.496a32 32 0 0 1 45.248-45.248L512 466.752l90.496-90.496a32 32 0 1 1 45.248 45.248L557.248 512l90.496 90.496a32 32 0 1 1-45.248 45.248L512 557.248l-90.496 90.496a32 32 0 0 1-45.248-45.248z"></path></svg>
          <span>错误</span>
        </button>
      </div>

      <!-- 答案显示 -->
      <div v-if="answered" class="answer-section">
        <div class="answer-result" :class="isCorrect ? 'correct' : 'wrong'">
          <div class="result-icon">
            <svg v-if="isCorrect" viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768m0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896"></path></svg>
            <svg v-else viewBox="0 0 1024 1024"><path fill="currentColor" d="m466.752 512-90.496-90.496a32 32 0 0 1 45.248-45.248L512 466.752l90.496-90.496a32 32 0 1 1 45.248 45.248L557.248 512l90.496 90.496a32 32 0 1 1-45.248 45.248L512 557.248l-90.496 90.496a32 32 0 0 1-45.248-45.248z"></path></svg>
          </div>
          <div class="result-info">
            <div class="result-title">{{ isCorrect ? '判断正确' : '判断错误' }}</div>
            <div class="result-desc">标准答案：<span class="answer-badge" :class="currentTask.is_correct ? 'correct' : 'wrong'">{{ currentTask.is_correct ? '正确' : '错误' }}</span></div>
          </div>
        </div>

        <!-- 修正内容 -->
        <div v-if="!currentTask.is_correct && currentTask.corrected_text" class="correction-card">
          <div class="correction-header">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768m0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896"></path></svg>
            <span>正确表述</span>
          </div>
          <div class="correction-text" v-html="currentTask.corrected_text_html || currentTask.corrected_text"></div>
        </div>

        <!-- 解析 -->
        <div v-if="currentTask.question_explanation" class="explanation-card">
          <div class="explanation-header">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768m0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896"></path></svg>
            <span>解析</span>
          </div>
          <div class="explanation-text" v-html="currentTask.question_explanation_html || currentTask.question_explanation"></div>
        </div>

        <!-- 下一题按钮 -->
        <button class="next-btn" @click="nextQuestion">
          {{ currentIndex < tasks.length - 1 ? '下一题' : '完成练习' }}
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M716.8 537.6a12.8 12.8 0 0 1 0 17.92L332.8 940.8a12.8 12.8 0 0 1-17.92-17.92l371.2-371.2-371.2-371.2a12.8 12.8 0 1 1 17.92-17.92z"></path></svg>
        </button>
      </div>
    </div>

    <!-- 完成界面 -->
    <div v-if="!loading && tasks.length > 0 && currentIndex >= tasks.length" class="complete-screen">
      <div class="result-dialog">
        <div class="result-header" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706dd 100%)">
          <div class="result-icon">🎉</div>
          <div class="result-title">练习完成</div>
        </div>
        <div class="result-content">
          <div class="tip-card" style="borderLeftColor: #f59e0b">
            <div class="tip-header">
              <span class="tip-icon">💡</span>
              <span class="tip-title" style="color: #f59e0b">今日任务已完成</span>
            </div>
            <div class="tip-content">所有辨析题都已按要求完成，继续保持学习！</div>
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
const currentIndex = ref(0)
const currentTask = computed(() => tasks.value[currentIndex.value] || null)
const answered = ref(false)
const isCorrect = ref(false)
const fontSize = ref(localStorage.getItem('practiceFontSize') || 'normal')
const taskRemoved = ref(false)

const loadTasks = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/distinguish/plan/tasks', {
      params: { t: Date.now() }
    })
    
    if (res.data.status === 'ok') {
      tasks.value = res.data.data || []
    } else {
      tasks.value = res.data.data || []
    }
    currentIndex.value = 0
    answered.value = false
    isCorrect.value = false
    taskRemoved.value = false
  } catch (e) {
    console.error('Failed to load tasks:', e)
  }
  loading.value = false
}

const submitAnswer = async (feedback) => {
  const task = currentTask.value
  if (!task) return
  
  const userChoseCorrect = feedback === 'remembered'
  isCorrect.value = userChoseCorrect === task.is_correct
  
  try {
    const res = await axios.post('/api/distinguish/plan/feedback', {
      record_id: task.id,
      feedback: feedback,
      user_id: store.userId || 'default_user'
    })
    
    const repeatInfo = res.data.repeat_info
    if (repeatInfo && repeatInfo.interval !== undefined) {
      const interval = repeatInfo.interval
      
      tasks.value.splice(currentIndex.value, 1)
      
      const insertPos = currentIndex.value + interval - 1
      
      if (insertPos >= tasks.value.length) {
        tasks.value.push(task)
      } else if (insertPos < 0) {
        tasks.value.unshift(task)
      } else {
        tasks.value.splice(insertPos, 0, task)
      }
      
      if (currentIndex.value >= tasks.value.length) {
        currentIndex.value = 0
      }
      
      taskRemoved.value = true
      answered.value = true
    } else {
      taskRemoved.value = false
      answered.value = true
    }
  } catch (e) {
    console.error('Submit feedback failed:', e)
    answered.value = true
  }
}

const nextQuestion = () => {
  if (taskRemoved.value) {
    taskRemoved.value = false
    answered.value = false
    isCorrect.value = false
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }
  
  if (currentIndex.value + 1 < tasks.value.length) {
    currentIndex.value++
    answered.value = false
    isCorrect.value = false
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } else {
    const hasDuplicates = tasks.value.some((task, index) => {
      return tasks.value.slice(index + 1).some(t => t.id === task.id)
    })
    
    if (hasDuplicates) {
      currentIndex.value = 0
      answered.value = false
      isCorrect.value = false
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } else {
      currentIndex.value = tasks.value.length
    }
  }
}

const goBack = () => {
  router.push('/mobile')
}

const goHome = () => {
  router.push('/mobile')
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
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
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

.chapter-tag {
  font-size: 13px;
  padding: 6px 12px;
  border-radius: 8px;
  background: white;
  color: #64748b;
  border: 1px solid #e2e8f0;
}

/* 选项显示卡片优化 */
.option-display-card {
  background: linear-gradient(135deg, #fff 0%, #f8fafc 100%);
  border-radius: 16px;
  padding: 20px;
  margin: 16px 0;
  display: flex;
  gap: 16px;
  align-items: flex-start;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.option-badge {
  font-size: 18px;
  font-weight: 700;
  color: #f59e0b;
  padding: 6px 12px;
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 112, 6, 0.1) 100%);
  border-radius: 8px;
  flex-shrink: 0;
}

.option-text {
  font-size: 16px;
  color: #334155;
  line-height: 1.7;
}

/* 判断按钮优化 */
.judge-buttons {
  display: flex;
  gap: 20px;
  margin: 24px 0;
}

.judge-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px 20px;
  border-radius: 16px;
  border: 2px solid;
  background: #fff;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.judge-btn:active {
  transform: scale(0.98);
}

.judge-btn svg {
  width: 40px;
  height: 40px;
}

.judge-btn span {
  font-size: 17px;
  font-weight: 600;
}

.judge-btn.correct {
  border-color: #10b981;
  color: #10b981;
  background: linear-gradient(135deg, #fff 0%, #f0fff4 100%);
}

.judge-btn.correct:active {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.judge-btn.wrong {
  border-color: #ef4444;
  color: #ef4444;
  background: linear-gradient(135deg, #fff 0%, #fff1f0 100%);
}

.judge-btn.wrong:active {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
}

/* 答案显示优化 */
.answer-section {
  margin-top: 16px;
}

.answer-result {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.answer-result.correct {
  background: linear-gradient(135deg, #f0fff4 0%, #dcfce7 100%);
  border: 1px solid #10b981;
}

.answer-result.wrong {
  background: linear-gradient(135deg, #fff1f0 0%, #fee2e2 100%);
  border: 1px solid #ef4444;
}

.result-icon svg {
  width: 24px;
  height: 24px;
}

.answer-result.correct .result-icon svg {
  color: #10b981;
}

.answer-result.wrong .result-icon svg {
  color: #ef4444;
}

.result-info {
  flex: 1;
}

.result-title {
  font-size: 16px;
  font-weight: 600;
}

.answer-result.correct .result-title {
  color: #10b981;
}

.answer-result.wrong .result-title {
  color: #ef4444;
}

.result-desc {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}

.answer-badge {
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: 600;
}

.answer-badge.correct {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.answer-badge.wrong {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

/* 修正内容优化 */
.correction-card {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(217, 112, 6, 0.05) 100%);
  border-radius: 12px;
  padding: 14px 16px;
  margin-bottom: 12px;
  border-left: 3px solid #f59e0b;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.correction-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #f59e0b;
  margin-bottom: 10px;
}

.correction-header svg {
  width: 18px;
  height: 18px;
}

.correction-text {
  font-size: 14px;
  color: #334155;
  line-height: 1.6;
}

/* 解析优化 */
.explanation-card {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  padding: 14px 16px;
  margin-bottom: 12px;
  border: 1px solid #e2e8f0;
}

.explanation-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 10px;
}

.explanation-header svg {
  width: 18px;
  height: 18px;
}

.explanation-text {
  font-size: 14px;
  color: #334155;
  line-height: 1.6;
}

/* 下一题按钮优化 */
.next-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  margin-top: 16px;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
  transition: all 0.3s;
}

.next-btn:active {
  transform: scale(0.98);
}

.next-btn svg {
  width: 18px;
  height: 18px;
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
  border-top-color: #f59e0b;
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
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
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
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.home-btn:active {
  transform: scale(0.98);
}
</style>