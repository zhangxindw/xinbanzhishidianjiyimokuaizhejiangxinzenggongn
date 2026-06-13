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
          <h2 class="app-title">记忆练习</h2>
          <div class="header-right">
            <span class="progress">{{ currentIndex + 1 }}/{{ totalQuestions }}</span>
          </div>
        </div>
        
        <div class="memory-content" v-if="currentQuestion">
          <div class="question-header">
            <span class="question-number">第 {{ currentIndex + 1 }} 题</span>
          </div>
          
          <div class="flash-card" :class="{ flipped: showAnswer }" @click="toggleAnswer">
            <div class="card-front">
              <div class="card-icon">📝</div>
              <p class="card-text">{{ currentQuestion.content }}</p>
              <div class="tap-hint">点击查看答案</div>
            </div>
            <div class="card-back">
              <div class="card-icon">💡</div>
              <p class="card-text">{{ currentQuestion.answer }}</p>
              <div class="card-meta">
                <span v-if="currentQuestion.chapter_name" class="chapter-tag">{{ currentQuestion.chapter_name }}</span>
              </div>
            </div>
          </div>
          
          <div class="rating-section" v-if="showAnswer">
            <div class="rating-label">掌握程度</div>
            <div class="rating-stars">
              <button 
                v-for="i in 5" 
                :key="i"
                class="star-btn"
                :class="{ active: rating >= i }"
                @click="setRating(i)"
              >
                <el-icon><Star /></el-icon>
              </button>
            </div>
          </div>
          
          <div class="action-bar">
            <button 
              class="next-btn"
              @click="nextQuestion"
            >
              {{ currentIndex < totalQuestions - 1 ? '下一题' : '完成练习' }}
            </button>
          </div>
        </div>
        
        <div class="empty-state" v-else>
          <div class="empty-icon">📚</div>
          <p>暂无记忆题目</p>
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
import { useRouter } from 'vue-router'
import { useQuizStore } from '@/store/quiz'
import { ArrowLeft, Star, HomeFilled } from '@element-plus/icons-vue'

const router = useRouter()
const store = useQuizStore()

const questions = ref([])
const currentIndex = ref(0)
const showAnswer = ref(false)
const rating = ref(0)

const currentQuestion = computed(() => questions.value[currentIndex.value])
const totalQuestions = computed(() => questions.value.length)

const goBack = () => {
  router.push('/mobile')
}

const toggleAnswer = () => {
  showAnswer.value = !showAnswer.value
}

const setRating = (level) => {
  rating.value = level
}

const nextQuestion = () => {
  if (currentIndex.value < totalQuestions.value - 1) {
    currentIndex.value++
    showAnswer.value = false
    rating.value = 0
  } else {
    router.push('/mobile')
  }
}

const loadQuestions = async () => {
  try {
    const result = await store.getQuestions({ per_page: 50, shuffle: true })
    if (result && result.data) {
      questions.value = result.data.map(q => ({
        ...q,
        answer: q.options && q.options[q.correct_index] || '暂无答案'
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
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
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
  color: #666;
}

.header-left {
  cursor: pointer;
}

.app-title {
  color: #666;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.progress {
  font-size: 14px;
  font-weight: 500;
}

.memory-content {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.question-header {
  width: 100%;
  margin-bottom: 20px;
}

.question-number {
  font-size: 14px;
  color: #8e8e93;
}

.flash-card {
  width: 100%;
  height: 300px;
  perspective: 1000px;
  cursor: pointer;
}

.flash-card.flipped .card-inner {
  transform: rotateY(180deg);
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.card-front, .card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
}

.card-front {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-back {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  transform: rotateY(180deg);
}

.card-icon {
  font-size: 50px;
  margin-bottom: 20px;
}

.card-text {
  color: #fff;
  font-size: 18px;
  text-align: center;
  line-height: 1.6;
  margin: 0;
}

.card-back .card-text {
  color: #333;
}

.tap-hint {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  margin-top: 20px;
}

.card-meta {
  margin-top: 20px;
}

.chapter-tag {
  background: rgba(255, 255, 255, 0.3);
  padding: 5px 15px;
  border-radius: 15px;
  font-size: 12px;
  color: #333;
}

.rating-section {
  margin-top: 30px;
  width: 100%;
  text-align: center;
}

.rating-label {
  font-size: 14px;
  color: #8e8e93;
  margin-bottom: 15px;
}

.rating-stars {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.star-btn {
  background: none;
  border: none;
  font-size: 36px;
  cursor: pointer;
  color: #ddd;
  transition: all 0.2s ease;
}

.star-btn.active {
  color: #ffd700;
}

.star-btn:active {
  transform: scale(0.9);
}

.action-bar {
  width: 100%;
  padding: 20px 0;
}

.next-btn {
  width: 100%;
  padding: 15px;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  cursor: pointer;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: #666;
  transition: all 0.2s ease;
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