<template>
  <div class="mobile-view-container">
    <div class="mobile-frame">
      <div class="mobile-header">
        <div class="mobile-notch"></div>
        <div class="mobile-status-bar">
          <span class="time">9:41</span>
          <div class="status-icons">
            <span>📶</span>
            <span>🔋</span>
          </div>
        </div>
      </div>
      
      <div class="mobile-screen">
        <div class="mobile-app-header">
          <div class="header-left" @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
          </div>
          <h2 class="app-title">{{ practiceTitle }}</h2>
          <div class="header-right">
            <span class="progress">{{ currentIndex + 1 }}/{{ totalQuestions }}</span>
          </div>
        </div>
        
        <div class="practice-content" v-if="currentQuestion">
          <div class="question-header">
            <span class="question-type">{{ currentQuestion.type_name }}</span>
            <span class="question-number">第 {{ currentIndex + 1 }} 题</span>
          </div>
          
          <div class="question-content">
            <p>{{ currentQuestion.content }}</p>
          </div>
          
          <div class="options-list">
            <div 
              v-for="(option, index) in currentQuestion.options" 
              :key="index"
              class="option-item"
              :class="{ 
                selected: selectedOption === index,
                correct: showAnswer && isCorrect(index),
                wrong: showAnswer && selectedOption === index && !isCorrect(index)
              }"
              @click="selectOption(index)"
            >
              <span class="option-letter">{{ String.fromCharCode(65 + index) }}</span>
              <span class="option-text">{{ option }}</span>
              <el-icon v-if="showAnswer && isCorrect(index)" class="option-icon correct-icon"><Check /></el-icon>
              <el-icon v-else-if="showAnswer && selectedOption === index" class="option-icon wrong-icon"><Close /></el-icon>
            </div>
          </div>
          
          <div class="answer-section" v-if="showAnswer">
            <div class="answer-card" :class="{ correct: isCorrect(selectedOption), wrong: !isCorrect(selectedOption) }">
              <div class="answer-title">
                <el-icon><InfoFilled /></el-icon>
                <span>{{ isCorrect(selectedOption) ? '回答正确!' : '回答错误' }}</span>
              </div>
              <div class="correct-answer" v-if="!isCorrect(selectedOption)">
                <span>正确答案：{{ String.fromCharCode(65 + currentQuestion.correct_index) }}</span>
              </div>
              <div class="answer-analysis" v-if="currentQuestion.analysis">
                <p>解析：{{ currentQuestion.analysis }}</p>
              </div>
            </div>
          </div>
          
          <div class="action-bar">
            <button 
              v-if="!showAnswer"
              class="submit-btn"
              :disabled="selectedOption === null"
              @click="submitAnswer"
            >
              确认答案
            </button>
            <button 
              v-else
              class="next-btn"
              @click="nextQuestion"
            >
              {{ currentIndex < totalQuestions - 1 ? '下一题' : '完成练习' }}
            </button>
          </div>
        </div>
        
        <div class="empty-state" v-else>
          <div class="empty-icon">📝</div>
          <p>暂无题目</p>
          <button class="back-btn" @click="goBack">返回首页</button>
        </div>
        
        <div class="mobile-footer">
          <div class="home-btn" @click="$router.push('/mobile')">
            <el-icon><HomeFilled /></el-icon>
          </div>
        </div>
      </div>
      
      <div class="mobile-home-indicator"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuizStore } from '@/store/quiz'
import { ArrowLeft, Check, Close, InfoFilled, HomeFilled } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const store = useQuizStore()

const questions = ref([])
const currentIndex = ref(0)
const selectedOption = ref(null)
const showAnswer = ref(false)

const practiceType = computed(() => route.params.type || 'sequential')

const practiceTitle = computed(() => {
  const titles = {
    sequential: '顺序刷题',
    random: '随机出题',
    wrong: '错题练习'
  }
  return titles[practiceType.value] || '刷题练习'
})

const currentQuestion = computed(() => questions.value[currentIndex.value])
const totalQuestions = computed(() => questions.value.length)

const isCorrect = (index) => {
  return currentQuestion.value && currentQuestion.value.correct_index === index
}

const goBack = () => {
  router.push('/mobile')
}

const selectOption = (index) => {
  if (showAnswer.value) return
  selectedOption.value = index
}

const submitAnswer = async () => {
  if (selectedOption.value === null) return
  
  showAnswer.value = true
  
  if (currentQuestion.value) {
    const isCorrectAnswer = isCorrect(selectedOption.value)
    await store.submitAnswer(
      currentQuestion.value.id,
      String.fromCharCode(65 + selectedOption.value),
      String.fromCharCode(65 + currentQuestion.value.correct_index)
    )
  }
}

const nextQuestion = () => {
  if (currentIndex.value < totalQuestions.value - 1) {
    currentIndex.value++
    selectedOption.value = null
    showAnswer.value = false
  } else {
    router.push('/mobile')
  }
}

const loadQuestions = async () => {
  try {
    let result = null
    
    if (practiceType.value === 'sequential') {
      result = await store.getQuestions({ per_page: 100 })
    } else if (practiceType.value === 'random') {
      result = await store.getQuestions({ per_page: 100, shuffle: true })
    } else if (practiceType.value === 'wrong') {
      result = await store.getWrongQuestions()
    }
    
    if (result && result.data) {
      questions.value = result.data.map(q => ({
        ...q,
        options: q.options || []
      }))
    }
  } catch (error) {
    console.error('加载题目失败:', error)
  }
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.mobile-view-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.mobile-frame {
  width: 375px;
  height: 812px;
  background: #1c1c1e;
  border-radius: 40px;
  padding: 20px;
  box-sizing: border-box;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  position: relative;
}

.mobile-header {
  text-align: center;
  margin-bottom: 10px;
}

.mobile-notch {
  width: 150px;
  height: 30px;
  background: #1c1c1e;
  border-radius: 0 0 20px 20px;
  margin: 0 auto -10px;
  position: relative;
  z-index: 10;
}

.mobile-status-bar {
  display: flex;
  justify-content: space-between;
  padding: 0 20px;
  color: #fff;
  font-size: 14px;
}

.status-icons {
  display: flex;
  gap: 8px;
}

.mobile-screen {
  background: linear-gradient(180deg, #f5f5f7 0%, #e8e8ed 100%);
  border-radius: 30px;
  height: calc(100% - 60px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.mobile-app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 15px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left, .header-right {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.header-left {
  cursor: pointer;
}

.app-title {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.progress {
  font-size: 14px;
  font-weight: 500;
}

.practice-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.question-type {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 12px;
}

.question-number {
  font-size: 14px;
  color: #8e8e93;
}

.question-content {
  background: #fff;
  padding: 15px;
  border-radius: 12px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.question-content p {
  margin: 0;
  font-size: 16px;
  line-height: 1.6;
  color: #333;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-item {
  background: #fff;
  padding: 15px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.option-item:active {
  transform: scale(0.98);
}

.option-item.selected {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.option-item.selected .option-letter,
.option-item.selected .option-text {
  color: #fff;
}

.option-item.correct {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.option-item.wrong {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.option-letter {
  width: 32px;
  height: 32px;
  background: #f0f0f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  color: #666;
}

.option-item.selected .option-letter {
  background: rgba(255, 255, 255, 0.3);
}

.option-text {
  flex: 1;
  font-size: 15px;
  color: #333;
}

.option-icon {
  font-size: 18px;
}

.correct-icon {
  color: #43e97b;
}

.wrong-icon {
  color: #fa709a;
}

.answer-section {
  margin-top: 20px;
}

.answer-card {
  background: #fff;
  border-radius: 12px;
  padding: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.answer-card.correct {
  border-left: 4px solid #43e97b;
}

.answer-card.wrong {
  border-left: 4px solid #fa709a;
}

.answer-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  margin-bottom: 10px;
}

.correct-answer {
  font-size: 14px;
  color: #43e97b;
  margin-bottom: 10px;
  font-weight: 500;
}

.answer-analysis p {
  margin: 0;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.action-bar {
  padding: 20px 0;
}

.submit-btn, .next-btn {
  width: 100%;
  padding: 15px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.submit-btn:active {
  transform: scale(0.98);
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.next-btn {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.next-btn:active {
  transform: scale(0.98);
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.empty-icon {
  font-size: 60px;
}

.empty-state p {
  font-size: 16px;
  color: #8e8e93;
}

.back-btn {
  padding: 12px 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.mobile-footer {
  background: #fff;
  padding: 15px;
  border-top: 1px solid #e0e0e0;
}

.home-btn {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  color: #fff;
  font-size: 20px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.mobile-home-indicator {
  width: 134px;
  height: 6px;
  background: #3c3c3c;
  border-radius: 3px;
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
}
</style>