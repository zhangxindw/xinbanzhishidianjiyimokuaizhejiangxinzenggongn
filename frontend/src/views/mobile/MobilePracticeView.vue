<template>
  <div class="mobile-practice">
    <!-- 顶部标题栏 -->
    <header class="mobile-header">
      <div class="header-content">
        <button class="back-btn" @click="goBack">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M340.864 149.312a30.59 30.59 0 0 0 0 42.752L652.736 512 340.864 831.872a30.59 30.59 0 0 0 0 42.752 29.12 29.12 0 0 0 41.728 0L714.24 534.336a32 32 0 0 0 0-44.672L382.592 149.376a29.12 29.12 0 0 0-41.728 0z"></path></svg>
        </button>
        <div class="header-title">
          <h1>{{ modeTitle }}</h1>
          <span v-if="practiceStarted" class="progress-badge">{{ currentIndex + 1 }}/{{ questions.length }}</span>
        </div>
      </div>
      <div class="header-right">
        <div class="font-size-controls">
          <span class="font-label">字号</span>
          <div class="font-buttons">
            <button 
              class="font-btn" 
              :class="{ active: fontSize === 'normal' }"
              @click="setFontSize('normal')"
            >标</button>
            <button 
              class="font-btn" 
              :class="{ active: fontSize === 'large' }"
              @click="setFontSize('large')"
            >大</button>
            <button 
              class="font-btn" 
              :class="{ active: fontSize === 'xlarge' }"
              @click="setFontSize('xlarge')"
            >特大</button>
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
          <div 
            v-for="ch in chapters" 
            :key="ch.id" 
            class="chapter-item"
            :class="{ selected: selectedChapterIds.includes(ch.id) }"
            @click="toggleChapter(ch.id)"
          >
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

      <!-- 随机出题额外配置 -->
      <div v-if="practiceMode === 'random'" class="config-card">
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 1024 1024"><path fill="currentColor" d="M784.512 230.272v-50.56a32 32 0 1 1 64 0v149.056a32 32 0 0 1-32 32H667.52a32 32 0 1 1 0-64h92.992A320 320 0 1 0 524.8 833.152a320 320 0 0 0 320-320h64a384 384 0 0 1-384 384 384 384 0 0 1-384-384 384 384 0 0 1 643.712-282.88"></path></svg>
          <h3>抽题设置</h3>
        </div>
        <div class="config-item">
          <span class="config-label">抽题数量</span>
          <div class="config-value">
            <input type="number" v-model.number="config.count" min="1" max="100" class="config-input" />
          </div>
        </div>
        <div class="config-item">
          <span class="config-label">打乱选项</span>
          <div class="switch" :class="{ active: config.shuffleOptions }" @click="config.shuffleOptions = !config.shuffleOptions">
            <span class="switch-text">{{ config.shuffleOptions ? '开启' : '关闭' }}</span>
          </div>
        </div>
      </div>

      <!-- 错题练习提示 -->
      <div v-if="practiceMode === 'wrong'" class="config-card highlight">
        <div class="card-header">
          <svg class="card-icon danger" viewBox="0 0 1024 1024"><path fill="currentColor" d="M928.99 755.83 574.6 203.25c-12.89-20.16-36.76-32.58-62.6-32.58s-49.71 12.43-62.6 32.58L95.01 755.83c-12.91 20.12-12.9 44.91.01 65.03 12.92 20.12 36.78 32.51 62.59 32.49h708.78c25.82.01 49.68-12.37 62.59-32.49s12.92-44.91.01-65.03"></path></svg>
          <h3>错题练习</h3>
        </div>
        <p class="config-tip">将从所有错题中随机抽取题目进行练习</p>
        <div class="wrong-stats">
          <div class="stat-badge">
            <span class="stat-number">{{ wrongCount }}</span>
            <span class="stat-text">当前错题</span>
          </div>
        </div>
      </div>

      <!-- 通用配置 -->
      <div class="config-card">
        <div class="card-header">
          <svg class="card-icon" viewBox="0 0 1024 1024"><path fill="currentColor" d="M384 96a32 32 0 0 1 64 0v786.752a32 32 0 0 1-54.592 22.656L95.936 608a32 32 0 0 1 0-45.312h.128a32 32 0 0 1 45.184 0L384 805.632zm192 45.248a32 32 0 0 1 54.592-22.592L928.064 416a32 32 0 0 1 0 45.312h-.128a32 32 0 0 1-45.184 0L640 218.496V928a32 32 0 1 1-64 0z"></path></svg>
          <h3>练习设置</h3>
        </div>
        <div class="config-item">
          <span class="config-label">打乱选项</span>
          <div class="switch" :class="{ active: config.shuffleOptions }" @click="config.shuffleOptions = !config.shuffleOptions">
            <span class="switch-text">{{ config.shuffleOptions ? '开启' : '关闭' }}</span>
          </div>
        </div>
        <div class="config-item">
          <span class="config-label">文字大小</span>
          <div class="font-size-selector">
            <button 
              class="font-size-btn" 
              :class="{ active: config.fontSize === 'normal' }"
              @click="config.fontSize = 'normal'"
            >标准</button>
            <button 
              class="font-size-btn" 
              :class="{ active: config.fontSize === 'large' }"
              @click="config.fontSize = 'large'"
            >较大</button>
            <button 
              class="font-size-btn" 
              :class="{ active: config.fontSize === 'xlarge' }"
              @click="config.fontSize = 'xlarge'"
            >特大</button>
          </div>
        </div>
      </div>

      <!-- 预览信息 -->
      <div class="preview-card">
        <div class="preview-info">
          <span class="preview-label">预计题目</span>
          <span class="preview-value">{{ previewCount }}</span>
        </div>
        <button class="start-btn" @click="startPractice">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M640 573.44V128a32 32 0 0 1 64 0v445.44l292.864-292.864a32 32 0 0 1 45.248 45.248L749.248 618.688a32 32 0 0 1 0 45.248l293.824 293.824a32 32 0 0 1-45.248 45.248L640 618.688z"></path></svg>
          开始练习
        </button>
      </div>
    </div>

    <!-- 练习界面 -->
    <div v-if="practiceStarted && currentQuestion" class="practice-screen" :class="'font-' + fontSize">
      <!-- 进度条 -->
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: ((currentIndex + 1) / questions.length * 100) + '%' }"></div>
      </div>

      <!-- 题目卡片 -->
      <div class="question-card">
        <div class="question-meta">
          <span class="question-type">{{ currentQuestion.question_type_name || '单选题' }}</span>
          <span class="question-chapter">{{ currentQuestion.chapter_name }}</span>
        </div>
        <div class="question-content" v-html="currentQuestion.stem_html || currentQuestion.stem"></div>
      </div>

      <!-- 选项列表 -->
      <div class="options-list">
        <div 
          v-for="(option, index) in currentQuestion.options" 
          :key="index"
          class="option-item"
          :class="{ 
            selected: selectedOption === option.label,
            correct: showAnswer && option.label === currentQuestion.answer,
            wrong: showAnswer && selectedOption === option.label && option.label !== currentQuestion.answer
          }"
          @click="selectOption(option.label)"
        >
          <div class="option-label">{{ option.label }}</div>
          <div class="option-text" v-html="option.text"></div>
          <div v-if="showAnswer && option.label === currentQuestion.answer" class="option-icon correct">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M557.248 314.88 384 488.128l-90.496-90.496a32 32 0 0 0-45.248 45.248l121.248 121.248a32 32 0 0 0 45.248 0L557.248 360.128a32 32 0 0 0 0-45.248z"></path></svg>
          </div>
          <div v-if="showAnswer && selectedOption === option.label && option.label !== currentQuestion.answer" class="option-icon wrong">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M557.248 314.88 384 488.128l-90.496-90.496a32 32 0 0 0-45.248 45.248l121.248 121.248a32 32 0 0 0 45.248 0L557.248 360.128a32 32 0 0 0 0-45.248z"></path></svg>
          </div>
        </div>
      </div>

      <!-- 答案显示 -->
      <div v-if="showAnswer" class="answer-section">
        <div class="answer-card">
          <div class="answer-header">
            <span class="answer-badge">正确答案</span>
            <span class="answer-value">{{ currentQuestion.answer }}</span>
          </div>
        </div>
        <div v-if="currentQuestion.explanation || currentQuestion.explanation_html" class="explanation-card">
          <div class="explanation-header">
            <svg class="explanation-icon" viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768m0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896"></path></svg>
            <span>解析</span>
          </div>
          <div class="explanation-text" v-html="currentQuestion.explanation_html || currentQuestion.explanation"></div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <button v-if="!showAnswer" class="submit-btn" @click="submitAnswer" :disabled="!selectedOption">
          提交答案
        </button>
        <button v-if="showAnswer" class="next-btn" @click="nextQuestion">
          {{ currentIndex < questions.length - 1 ? '下一题' : '完成练习' }}
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M716.8 537.6a12.8 12.8 0 0 1 0 17.92L332.8 940.8a12.8 12.8 0 0 1-17.92-17.92l371.2-371.2-371.2-371.2a12.8 12.8 0 1 1 17.92-17.92z"></path></svg>
        </button>
      </div>
    </div>

    <!-- 完成界面 -->
    <div v-if="practiceStarted && !currentQuestion" class="complete-screen">
      <div class="complete-card">
        <div class="complete-icon">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 864a256 256 0 1 0 0-512 256 256 0 0 0 0 512zm0 64a320 320 0 1 1 0-640 320 320 0 0 1 0 640z"></path><path fill="currentColor" d="M384 512a32 32 0 0 1 32-32h192a32 32 0 0 1 32 32v192a32 32 0 0 1-32 32H416a32 32 0 0 1-32-32V512z"></path></svg>
        </div>
        <h2>练习完成</h2>
        <div class="complete-stats">
          <div class="stat-item">
            <span class="stat-value">{{ questions.length }}</span>
            <span class="stat-label">总题数</span>
          </div>
          <div class="stat-item">
            <span class="stat-value correct">{{ correctCount }}</span>
            <span class="stat-label">正确</span>
          </div>
          <div class="stat-item">
            <span class="stat-value wrong">{{ questions.length - correctCount }}</span>
            <span class="stat-label">错误</span>
          </div>
        </div>
        <div class="complete-rate">
          <div class="rate-circle">
            <span class="rate-value">{{ Math.round(correctCount / questions.length * 100) }}%</span>
          </div>
          <span class="rate-label">正确率</span>
        </div>
        <div class="complete-actions">
          <button class="restart-btn" @click="restartPractice">再来一次</button>
          <button class="home-btn" @click="goHome">返回首页</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useQuizStore } from '@/store/quiz'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const store = useQuizStore()

const practiceMode = computed(() => route.params.mode || 'sequential')

const modeTitle = computed(() => {
  const titles = {
    sequential: '顺序刷题',
    random: '随机出题',
    wrong: '错题练习'
  }
  return titles[practiceMode.value] || '刷题练习'
})

const chapters = ref([])
const selectedChapterIds = ref([])
const wrongCount = ref(0)

const config = ref({
  count: 20,
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
const correctCount = ref(0)

const previewCount = computed(() => {
  if (practiceMode.value === 'random') {
    return config.value.count
  }
  if (practiceMode.value === 'wrong') {
    // 如果选择了章节，计算选中章节的错题数之和
    if (selectedChapterIds.value.length > 0) {
      return selectedChapterIds.value.reduce((sum, id) => {
        const ch = chapters.value.find(c => c.id === id)
        return sum + (ch?.question_count || 0)
      }, 0)
    }
    // 否则返回总错题数
    return wrongCount.value
  }
  if (selectedChapterIds.value.length > 0) {
    return selectedChapterIds.value.reduce((sum, id) => {
      const ch = chapters.value.find(c => c.id === id)
      return sum + (ch?.question_count || 0)
    }, 0)
  }
  return store.statistics?.total_questions || 0
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

const startPractice = async () => {
    try {
      let apiUrl = ''
      let params = {}

      if (practiceMode.value === 'sequential') {
        apiUrl = '/api/practice/sequential'
        params = {
          shuffle_options: config.value.shuffleOptions
        }
        if (selectedChapterIds.value.length > 0) {
          params.chapter_ids = selectedChapterIds.value
        }
      } else if (practiceMode.value === 'random') {
        apiUrl = '/api/practice/random'
        params = {
          count: config.value.count,
          shuffle_options: config.value.shuffleOptions
        }
        if (selectedChapterIds.value.length > 0) {
          params.chapter_ids = selectedChapterIds.value
        }
      } else if (practiceMode.value === 'wrong') {
        apiUrl = '/api/wrong-questions/practice'
        params = {
          user_id: store.userId,
          shuffle: true,
          shuffle_options: config.value.shuffleOptions
        }
        // 如果选择了章节，传递章节ID
        if (selectedChapterIds.value.length > 0) {
          params.chapter_ids = selectedChapterIds.value
        }
      }

      const res = await axios.post(apiUrl, params)
      const result = res.data
      
      if (result.data && result.data.length > 0) {
        // 转换后端数据为前端期望的格式
        questions.value = result.data.map(q => {
          // 构建选项数组
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
        practiceStarted.value = true
        currentIndex.value = 0
        correctCount.value = 0
      } else {
        alert('没有可用的题目')
      }
    } catch (e) {
      console.error('Failed to start practice:', e)
      alert('加载题目失败')
    }
  }

const selectOption = async (label) => {
  if (showAnswer.value) return
  selectedOption.value = label
}

const submitAnswer = async () => {
  if (!selectedOption.value || !currentQuestion.value) return
  
  showAnswer.value = true
  
  const isCorrect = selectedOption.value === currentQuestion.value.answer
  if (isCorrect) {
    correctCount.value++
  }

  // 提交答案记录
  try {
    await store.submitAnswer(currentQuestion.value.id, selectedOption.value, currentQuestion.value.answer)
  } catch (e) {
    console.error('Submit answer failed:', e)
  }
}

const nextQuestion = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    selectedOption.value = ''
    showAnswer.value = false
  } else {
    questions.value = []
  }
}

const restartPractice = () => {
  practiceStarted.value = false
  questions.value = []
  currentIndex.value = 0
  selectedOption.value = ''
  showAnswer.value = false
  correctCount.value = 0
}

const goBack = () => {
  router.push('/mobile')
}

const goHome = () => {
  router.push('/mobile')
}

onMounted(async () => {
  // 加载章节列表
  try {
    const res = await axios.get('/api/chapters')
    if (res.data && res.data.data) {
      chapters.value = res.data.data
    }
  } catch (e) {
    console.error('Failed to load chapters:', e)
  }

  // 加载错题数和各章节错题统计
  if (practiceMode.value === 'wrong') {
    try {
      // 获取错题统计
      const statsRes = await axios.get('/api/wrong-questions/stats', {
        params: { user_id: store.userId }
      })
      if (statsRes.data && statsRes.data.data) {
        const stats = statsRes.data.data
        wrongCount.value = stats.total || 0
        // 更新各章节的错题数量
        if (stats.chapter_stats) {
          chapters.value.forEach(ch => {
            ch.question_count = stats.chapter_stats[ch.id] || 0
          })
        }
      }
    } catch (e) {
      console.error('Failed to load wrong count:', e)
    }
  }
})
</script>

<style scoped>
.mobile-practice {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #e8f4f8 100%);
  padding-bottom: 24px;
}

/* 顶部标题栏 */
.mobile-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 16px 20px;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.header-bg {
  position: absolute;
  top: -50%;
  right: -20%;
  width: 200px;
  height: 200px;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
  position: relative;
  z-index: 1;
  flex-shrink: 0;
}

.back-btn {
  width: 36px;
  height: 36px;
  background: rgba(255,255,255,0.2);
  border: none;
  border-radius: 50%;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.3s;
}

.back-btn:active {
  background: rgba(255,255,255,0.3);
}

.back-btn svg {
  width: 18px;
  height: 18px;
}

.header-title {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mobile-header h1 {
  font-size: 18px;
  margin: 0;
  font-weight: 600;
}

.progress-badge {
  font-size: 12px;
  opacity: 0.9;
}

.header-right {
  position: relative;
  z-index: 1;
  flex-shrink: 0;
}

.font-size-controls {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.2);
  padding: 6px 10px;
  border-radius: 20px;
}

.font-label {
  font-size: 12px;
  opacity: 0.9;
}

.font-buttons {
  display: flex;
  gap: 4px;
}

.font-btn {
  padding: 4px 8px;
  background: transparent;
  border: none;
  color: white;
  font-size: 11px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  opacity: 0.7;
}

.font-btn.active {
  background: rgba(255,255,255,0.3);
  opacity: 1;
  font-weight: 600;
}

.font-btn:active {
  background: rgba(255,255,255,0.4);
}

/* 配置界面 */
.config-screen {
  padding: 16px;
}

.config-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.config-card.highlight {
  background: linear-gradient(135deg, #fff5f5 0%, #fff 100%);
  border: 1px solid #ffebeb;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.card-icon {
  width: 20px;
  height: 20px;
  color: #667eea;
}

.card-icon.danger {
  color: #ff4d4f;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
}

.chapter-list {
  max-height: 240px;
  overflow-y: auto;
}

.chapter-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-radius: 12px;
  margin-bottom: 8px;
  background: #f9fafb;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.chapter-item:active {
  transform: scale(0.98);
}

.chapter-item.selected {
  background: #f0f7ff;
  border-color: #667eea;
}

.chapter-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.chapter-name {
  font-size: 14px;
  color: #1a1a1a;
  font-weight: 500;
}

.chapter-count {
  font-size: 12px;
  color: #8c8c8c;
}

.chapter-check {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #667eea;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.chapter-check svg {
  width: 14px;
  height: 14px;
  stroke: white;
  fill: none;
}

.chapter-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.action-btn {
  flex: 1;
  padding: 12px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn.outline {
  background: white;
  color: #667eea;
  border: 1px solid #667eea;
}

.action-btn.outline:active {
  background: #f0f7ff;
}

.config-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid #f0f0f0;
}

.config-item:last-child {
  border-bottom: none;
}

.config-label {
  font-size: 14px;
  color: #333;
}

.config-value {
  display: flex;
  align-items: center;
  gap: 8px;
}

.config-input {
  width: 70px;
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
}

.switch {
  padding: 6px 16px;
  background: #f0f0f0;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.switch.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.switch-text {
  font-size: 12px;
  font-weight: 500;
}

.font-size-selector {
  display: flex;
  gap: 6px;
}

.font-size-btn {
  padding: 6px 12px;
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 12px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.font-size-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: #667eea;
}

.font-size-btn:active {
  transform: scale(0.95);
}

.config-tip {
  font-size: 14px;
  color: #666;
  margin: 0 0 12px 0;
  line-height: 1.5;
}

.wrong-stats {
  margin-top: 8px;
}

.stat-badge {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 20px;
  background: white;
  border-radius: 12px;
  border: 1px solid #ffebeb;
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
  color: #ff4d4f;
}

.stat-text {
  font-size: 12px;
  color: #8c8c8c;
  margin-top: 4px;
}

/* 预览卡片 */
.preview-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.preview-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.preview-label {
  font-size: 12px;
  color: #8c8c8c;
}

.preview-value {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
}

.start-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.start-btn:active {
  transform: scale(0.96);
}

.start-btn svg {
  width: 18px;
  height: 18px;
}

/* 练习界面 */
.practice-screen {
  padding: 16px;
}

/* 文字大小 - 标准 */
.practice-screen.font-normal .question-content {
  font-size: 16px !important;
  line-height: 1.8;
}

.practice-screen.font-normal .option-text {
  font-size: 15px !important;
  line-height: 1.6;
}

/* 解析保持固定大小，不随字号调节变化 */
.practice-screen.font-normal .explanation-text {
  font-size: 14px !important;
  line-height: 1.7;
}

.practice-screen.font-normal .option-item {
  padding: 12px 14px;
}

.practice-screen.font-normal .option-label {
  width: 28px !important;
  height: 28px !important;
  font-size: 13px !important;
}

/* 文字大小 - 较大 */
.practice-screen.font-large .question-content {
  font-size: 19px !important;
  line-height: 1.9;
}

.practice-screen.font-large .option-text {
  font-size: 18px !important;
  line-height: 1.7;
}

/* 解析保持固定大小 */
.practice-screen.font-large .explanation-text {
  font-size: 14px !important;
  line-height: 1.7;
}

.practice-screen.font-large .option-item {
  padding: 16px 18px;
}

.practice-screen.font-large .option-label {
  width: 30px !important;
  height: 30px !important;
  font-size: 14px !important;
}

/* 文字大小 - 特大 */
.practice-screen.font-xlarge .question-content {
  font-size: 22px !important;
  line-height: 2;
}

.practice-screen.font-xlarge .option-text {
  font-size: 21px !important;
  line-height: 1.8;
}

/* 解析保持固定大小 */
.practice-screen.font-xlarge .explanation-text {
  font-size: 14px !important;
  line-height: 1.7;
}

.practice-screen.font-xlarge .option-item {
  padding: 18px 20px;
}

.practice-screen.font-xlarge .option-label {
  width: 32px !important;
  height: 32px !important;
  font-size: 15px !important;
}

.progress-bar {
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  margin-bottom: 16px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.question-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.question-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.question-type {
  font-size: 12px;
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 4px 10px;
  border-radius: 6px;
}

.question-chapter {
  font-size: 12px;
  color: #8c8c8c;
  line-height: 24px;
}

.question-content {
  line-height: 1.7;
  color: #1a1a1a;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-item {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  gap: 12px;
}

.option-item:active {
  transform: scale(0.98);
}

.option-item.selected {
  background: #f0f7ff;
  border-color: #667eea;
}

.option-item.correct {
  background: #f0fff4;
  border-color: #52c41a;
}

.option-item.wrong {
  background: #fff1f0;
  border-color: #ff4d4f;
}

.option-label {
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  flex-shrink: 0;
}

.option-item.selected .option-label {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.option-item.correct .option-label {
  background: #52c41a;
}

.option-item.wrong .option-label {
  background: #ff4d4f;
}

.option-text {
  flex: 1;
  color: #333;
  line-height: 1.5;
}

.option-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.option-icon.correct {
  background: #52c41a;
  color: white;
}

.option-icon.wrong {
  background: #ff4d4f;
  color: white;
}

.option-icon svg {
  width: 14px;
  height: 14px;
}

/* 答案显示 */
.answer-section {
  margin-top: 16px;
}

.answer-card {
  background: #f0fff4;
  border: 1px solid #b7eb8f;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
}

.answer-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.answer-badge {
  font-size: 12px;
  color: #52c41a;
  background: white;
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 500;
}

.answer-value {
  font-size: 20px;
  font-weight: 700;
  color: #52c41a;
}

.explanation-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.explanation-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  color: #8c8c8c;
}

.explanation-icon {
  width: 18px;
  height: 18px;
}

.explanation-header span {
  font-size: 14px;
  font-weight: 500;
}

.explanation-text {
  font-size: 14px;
  color: #333;
  line-height: 1.7;
}

.explanation-text img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 12px 0;
  border-radius: 8px;
}

.explanation-text table {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
  font-size: 14px;
}

.explanation-text th,
.explanation-text td {
  border: 1px solid #e0e0e0;
  padding: 10px;
  text-align: left;
}

.explanation-text th {
  background-color: #f9f9f9;
  font-weight: 600;
}

.explanation-text strong,
.explanation-text b {
  font-weight: bold;
  color: #1a1a1a;
}

.explanation-text mark {
  background-color: #ffff00;
  padding: 0 4px;
}

/* 操作按钮 */
.action-buttons {
  margin-top: 20px;
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.submit-btn:active {
  transform: scale(0.98);
}

.submit-btn:disabled {
  background: #ccc;
  box-shadow: none;
  cursor: not-allowed;
}

.next-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(82, 196, 26, 0.3);
}

.next-btn:active {
  transform: scale(0.98);
}

.next-btn svg {
  width: 18px;
  height: 18px;
}

/* 完成界面 */
.complete-screen {
  padding: 24px 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}

.complete-card {
  background: white;
  border-radius: 20px;
  padding: 32px 24px;
  text-align: center;
  width: 100%;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.complete-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: white;
  box-shadow: 0 8px 24px rgba(82, 196, 26, 0.3);
}

.complete-icon svg {
  width: 40px;
  height: 40px;
}

.complete-card h2 {
  font-size: 24px;
  margin: 0 0 24px;
  color: #1a1a1a;
  font-weight: 600;
}

.complete-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 24px;
  padding: 16px 0;
  border-top: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  display: block;
}

.stat-value.correct {
  color: #52c41a;
}

.stat-value.wrong {
  color: #ff4d4f;
}

.stat-label {
  font-size: 12px;
  color: #8c8c8c;
  margin-top: 4px;
  display: block;
}

.complete-rate {
  margin: 24px 0;
}

.rate-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.rate-value {
  font-size: 24px;
  font-weight: 700;
  color: white;
}

.rate-label {
  font-size: 14px;
  color: #8c8c8c;
}

.complete-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 24px;
}

.restart-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.restart-btn:active {
  transform: scale(0.98);
}

.home-btn {
  width: 100%;
  padding: 14px;
  background: white;
  color: #667eea;
  border: 1px solid #667eea;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.home-btn:active {
  background: #f0f7ff;
}
</style>