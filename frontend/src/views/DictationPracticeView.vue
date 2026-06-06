<template>
  <div class="dictation-practice-view">
    <div class="page-header">
      <h2>默写练习</h2>
    </div>

    <!-- 配置区域 -->
    <div class="card config-card">
      <h3>练习配置</h3>
      <div class="config-row">
        <div class="config-item">
          <label>选择章节</label>
          <el-select v-model="config.chapter_ids" multiple placeholder="选择章节" @change="updateChapterStats">
            <el-option 
              v-for="chapter in chapters" 
              :key="chapter.id" 
              :label="chapter.name" 
              :value="chapter.id" 
            />
          </el-select>
        </div>
        <!-- 章节统计显示 -->
        <div v-if="config.chapter_ids.length > 0" class="chapter-stats">
          <div class="stat-item total">
            <span class="stat-label">总条数</span>
            <span class="stat-value">{{ chapterStats.total }}</span>
          </div>
          <div class="stat-item must">
            <span class="stat-label">必须背</span>
            <span class="stat-value">{{ chapterStats.must }}</span>
          </div>
          <div class="stat-item important">
            <span class="stat-label">重点背</span>
            <span class="stat-value">{{ chapterStats.important }}</span>
          </div>
          <div class="stat-item normal">
            <span class="stat-label">尽量背</span>
            <span class="stat-value">{{ chapterStats.normal }}</span>
          </div>
        </div>
        <div class="config-item">
          <label>抽查数量</label>
          <el-input-number 
            v-model="config.count" 
            :min="1" 
            :max="100" 
            placeholder="输入数量"
          />
        </div>
        <div class="config-item">
          <label>优先级筛选</label>
          <el-checkbox-group v-model="config.priorities" class="priority-checkbox-group">
            <el-checkbox label="must">必须背</el-checkbox>
            <el-checkbox label="important">重点背</el-checkbox>
            <el-checkbox label="normal">尽量背</el-checkbox>
          </el-checkbox-group>
        </div>
      </div>
      <div class="config-actions">
        <el-button type="primary" @click="startDictation">
          <el-icon><Bell /></el-icon>
          开始默写
        </el-button>
        <el-button type="success" @click="startPlanReview">
          <el-icon><Calendar /></el-icon>
          今日规划内容复习默写
        </el-button>
      </div>
    </div>

    <!-- 练习区域 -->
    <div v-if="isPracticing" class="practice-area">
      <!-- 当前题目 -->
      <div class="question-card">
        <div class="question-header">
          <span>第 {{ currentIndex + 1 }} / {{ questions.length }} 题</span>
          <span :class="getPriorityClass(currentQuestion.priority)">
            {{ currentQuestion.priority_label }}
          </span>
        </div>
        <div class="question-text">{{ currentQuestion.question }}</div>
        
        <!-- 速记口诀 -->
        <div class="mnemonic-section">
          <el-button 
            type="text" 
            @click="showMnemonic = !showMnemonic"
            class="mnemonic-btn"
          >
            <el-icon><Star /></el-icon>
            {{ showMnemonic ? '隐藏口诀' : '偷看口诀' }}
          </el-button>
          <div v-if="showMnemonic" class="mnemonic-content">
            {{ currentQuestion.mnemonic }}
          </div>
        </div>
      </div>

      <!-- 答案输入区域 -->
      <div class="answer-input-area">
        <div class="answer-options">
          <el-checkbox v-model="shuffleOrder" class="shuffle-checkbox">
            打乱顺序（答案顺序打乱也能匹配）
          </el-checkbox>
        </div>
        <div 
          v-for="(item, index) in currentQuestion.items" 
          :key="index" 
          class="answer-item"
        >
          <span class="item-number">{{ index + 1 }}.</span>
          <el-input 
            type="textarea" 
            v-model="userAnswers[index]" 
            :rows="2"
            :placeholder="shuffleOrder ? '输入答案（顺序不限）...' : '输入答案...'"
            class="answer-input"
          />
        </div>
      </div>

      <!-- 导航按钮 -->
      <div class="nav-section">
        <el-button 
          :disabled="currentIndex === 0" 
          @click="prevQuestion"
        >
          <el-icon><ArrowLeft /></el-icon>
          上一题
        </el-button>
        
        <!-- 单题提交按钮 -->
        <el-button 
          type="success"
          @click="submitCurrentQuestion"
          :loading="isSubmitting"
        >
          <el-icon><Check /></el-icon>
          提交本题
        </el-button>
        
        <el-button 
          v-if="currentIndex < questions.length - 1"
          @click="nextQuestion"
        >
          下一题
          <el-icon><ArrowRight /></el-icon>
        </el-button>
        <el-button 
          v-else 
          type="primary" 
          @click="showSummary"
          :disabled="!allQuestionsAnswered"
        >
          <el-icon><Finished /></el-icon>
          查看结果
        </el-button>
      </div>
      
      <!-- 已批改结果预览 -->
      <div v-if="questionResults.length > 0" class="results-preview">
        <h4>已批改题目</h4>
        <div class="preview-list">
          <div 
            v-for="(result, idx) in questionResults" 
            :key="idx"
            class="preview-item"
            :class="{ correct: result.isCorrect, wrong: !result.isCorrect }"
          >
            <span class="preview-number">第 {{ result.index + 1 }} 题</span>
            <span class="preview-status">{{ result.isCorrect ? '✓ 正确' : '✗ 错误' }}</span>
            <span class="preview-score">{{ result.score }}%</span>
          </div>
        </div>
      </div>
      
      <!-- 答案显示区域 -->
      <div v-if="showAnswerSection" class="answer-reveal-section">
        <h4>本题答案</h4>
        <div class="reveal-item" v-for="(item, idx) in currentQuestion.items" :key="idx">
          <span class="reveal-number">{{ idx + 1 }}.</span>
          <span class="reveal-content" v-html="cleanupHtmlStyles(item.content_html) || item.content"></span>
          <span v-if="isItemCorrect(idx)" class="reveal-check correct">✓</span>
          <span v-else class="reveal-check wrong">✗</span>
        </div>
      </div>
    </div>

    <!-- 结果展示 -->
    <div v-if="showResult" class="result-area">
      <div class="result-card">
        <div class="result-header">
          <h3>默写结果</h3>
          <div class="score-circle">
            <span class="score-value">{{ score }}%</span>
          </div>
        </div>
        <div class="result-stats">
          <div class="stat-item">
            <span class="stat-label">正确题数</span>
            <span class="stat-value correct">{{ correctCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">错误题数</span>
            <span class="stat-value wrong">{{ questions.length - correctCount }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">正确率</span>
            <span class="stat-value">{{ score }}%</span>
          </div>
        </div>
        
        <!-- 题目详情 -->
        <div class="questions-detail">
          <h4>答题详情</h4>
          <div 
            v-for="(q, idx) in questions" 
            :key="idx" 
            class="detail-item"
            :class="{ correct: results[idx], wrong: !results[idx] }"
          >
            <div class="detail-header">
              <span class="detail-number">第 {{ idx + 1 }} 题</span>
              <span :class="results[idx] ? 'result-correct' : 'result-wrong'">
                {{ results[idx] ? '正确' : '错误' }}
              </span>
            </div>
            <div class="detail-question">{{ q.question }}</div>
            <div class="detail-answers">
              <div class="answer-section">
                <span class="answer-label">你的答案：</span>
                <div v-for="(ans, aidx) in userAnswersList[idx]" :key="aidx" class="answer-text">
                  {{ ans || '(未作答)' }}
                </div>
              </div>
              <div class="answer-section">
                <span class="answer-label">正确答案：</span>
                <div v-for="(item, aidx) in q.items" :key="aidx" class="answer-text correct-text">
                  {{ item.content }}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="result-actions">
          <el-button @click="resetPractice">重新练习</el-button>
          <el-button type="primary" @click="goBack">返回配置</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { Bell, Star, ArrowLeft, ArrowRight, Camera, Check, Finished, Calendar } from '@element-plus/icons-vue'

const chapters = ref([])
const config = reactive({
  chapter_ids: [],
  count: 10,
  priorities: []
})

// 章节统计
const chapterStats = reactive({
  total: 0,
  must: 0,
  important: 0,
  normal: 0
})

// 更新章节统计
const updateChapterStats = async () => {
  if (config.chapter_ids.length === 0) {
    chapterStats.total = 0
    chapterStats.must = 0
    chapterStats.important = 0
    chapterStats.normal = 0
    return
  }
  
  try {
    // 获取选中章节的所有知识点
    const params = new URLSearchParams()
    params.set('page', 1)
    params.set('per_page', 10000)  // 获取所有
    config.chapter_ids.forEach(id => params.append('chapter_ids', id))
    
    const res = await axios.get(`/api/knowledge-points?${params}`)
    const kps = res.data.data || []
    
    // 统计各优先级数量
    chapterStats.total = kps.length
    chapterStats.must = kps.filter(kp => kp.priority === 'must').length
    chapterStats.important = kps.filter(kp => kp.priority === 'important').length
    chapterStats.normal = kps.filter(kp => kp.priority === 'normal').length
  } catch (error) {
    console.error('获取章节统计失败:', error)
  }
}

const isPracticing = ref(false)
const showResult = ref(false)
const questions = ref([])
const currentIndex = ref(0)
const showMnemonic = ref(false)
const userAnswers = ref([])
const userAnswersList = ref([])
const results = ref([])
const score = ref(0)
const correctCount = ref(0)
const shuffleOrder = ref(false)
const isSubmitting = ref(false)
const questionResults = ref([]) // 存储每题批改结果
const answeredQuestions = ref(new Set()) // 已批改的题目索引

const currentQuestion = computed(() => questions.value[currentIndex.value])

const allQuestionsAnswered = computed(() => {
  return answeredQuestions.value.size === questions.value.length
})

const loadChapters = async () => {
  const res = await axios.get('/api/chapters')
  chapters.value = res.data.data || []
}

const startDictation = async () => {
  const params = new URLSearchParams()
  params.set('count', config.count)
  if (config.chapter_ids.length > 0) {
    config.chapter_ids.forEach(id => params.append('chapter_id', id))
  }
  if (config.priorities.length > 0) {
    config.priorities.forEach(p => params.append('priority', p))
  }

  const res = await axios.get(`/api/knowledge-points/random?${params}`)
  questions.value = res.data.data || []
  
  if (questions.value.length === 0) {
    alert('没有符合条件的知识点')
    return
  }

  userAnswers.value = new Array(questions.value[0].items.length).fill('')
  userAnswersList.value = []
  results.value = []
  questionResults.value = []
  answeredQuestions.value = new Set()
  currentIndex.value = 0
  showMnemonic.value = false
  shuffleOrder.value = false
  isPracticing.value = true
  showResult.value = false
}

// 今日规划内容复习默写
const startPlanReview = async () => {
  try {
    // 获取今日需要复习的知识点
    const res = await axios.get('/api/memory/today-review')
    const reviewData = res.data.data || []
    
    if (reviewData.length === 0) {
      alert('今日没有需要复习的知识点')
      return
    }
    
    // 今日规划复习默写不受抽查数量限制，直接返回所有相关题目
    questions.value = [...reviewData].sort(() => Math.random() - 0.5)
    
    if (questions.value.length === 0) {
      alert('没有需要复习的知识点')
      return
    }

    userAnswers.value = new Array(questions.value[0].items.length).fill('')
    userAnswersList.value = []
    results.value = []
    questionResults.value = []
    answeredQuestions.value = new Set()
    currentIndex.value = 0
    showMnemonic.value = false
    shuffleOrder.value = false
    isPracticing.value = true
    showResult.value = false
  } catch (e) {
    console.error('获取复习数据失败', e)
    alert('获取复习数据失败')
  }
}

const getPriorityClass = (priority) => {
  const classes = {
    'must': 'priority-must',
    'important': 'priority-important',
    'normal': 'priority-normal'
  }
  return classes[priority] || 'priority-normal'
}

const prevQuestion = () => {
  if (currentIndex.value > 0) {
    // 保存当前答案
    userAnswersList.value[currentIndex.value] = [...userAnswers.value]
    currentIndex.value--
    // 恢复上一题答案
    userAnswers.value = [...(userAnswersList.value[currentIndex.value] || new Array(questions.value[currentIndex.value].items.length).fill(''))]
    showMnemonic.value = false
  }
}

const nextQuestion = () => {
  if (currentIndex.value < questions.value.length - 1) {
    // 保存当前答案
    userAnswersList.value[currentIndex.value] = [...userAnswers.value]
    currentIndex.value++
    // 初始化或恢复答案
    userAnswers.value = [...(userAnswersList.value[currentIndex.value] || new Array(questions.value[currentIndex.value].items.length).fill(''))]
    showMnemonic.value = false
  }
}

// 单题批改函数
const submitCurrentQuestion = () => {
  isSubmitting.value = true
  
  // 保存当前答案
  userAnswersList.value[currentIndex.value] = [...userAnswers.value]
  
  const q = questions.value[currentIndex.value]
  const userAns = userAnswersList.value[currentIndex.value] || []
  let itemScore = 0
  const totalItems = q.items.length
  
  if (shuffleOrder.value) {
    // 打乱顺序模式：智能匹配
    const userTexts = userAns.map(t => t.trim().toLowerCase()).filter(t => t)
    const correctTexts = q.items.map(item => stripHtmlTags(item.content_html || item.content).trim().toLowerCase())
    
    // 匹配正确的数量
    let matched = 0
    userTexts.forEach(userText => {
      // 检查是否完全匹配
      if (correctTexts.includes(userText)) {
        matched++
      } else {
        // 检查是否包含匹配
        const found = correctTexts.findIndex(ct => 
          ct.includes(userText) || userText.includes(ct)
        )
        if (found !== -1) {
          matched += 0.5
        }
      }
    })
    
    itemScore = matched
  } else {
    // 顺序模式：必须一一对应
    q.items.forEach((item, i) => {
      const userText = (userAns[i] || '').trim()
      const correctText = stripHtmlTags(item.content_html || item.content).trim()
      
      if (userText.toLowerCase() === correctText.toLowerCase()) {
        itemScore += 1
      } else if (userText.includes(correctText) || correctText.includes(userText)) {
        itemScore += 0.5
      }
    })
  }
  
  const questionScore = Math.round((itemScore / totalItems) * 100)
  const isCorrect = questionScore === 100
  
  // 保存结果
  results.value[currentIndex.value] = isCorrect
  answeredQuestions.value.add(currentIndex.value)
  
  // 添加到已批改列表
  questionResults.value.push({
    index: currentIndex.value,
    score: questionScore,
    isCorrect: isCorrect
  })
  
  isSubmitting.value = false
  
  // 显示反馈
  if (isCorrect) {
    ElMessage.success('正确！')
  } else {
    ElMessage.error(`错误！得分 ${questionScore}%`)
  }
  
  // 显示答案
  showAnswerSection.value = true
}

// 显示答案区域
const showAnswerSection = ref(false)

// 判断某一项是否正确
// 去除HTML标签的纯文本
const stripHtmlTags = (html) => {
  if (!html) return ''
  // 创建一个临时元素来解析HTML
  const temp = document.createElement('div')
  temp.innerHTML = html
  return temp.textContent || temp.innerText || ''
}

// 清理HTML中的内联字体大小样式（用于显示）
const cleanupHtmlStyles = (html) => {
  if (!html) return ''
  return html.replace(/style="[^"]*font-size[^"]*"/g, '')
}

const isItemCorrect = (itemIndex) => {
  const userAns = userAnswersList.value[currentIndex.value] || []
  const userText = (userAns[itemIndex] || '').trim().toLowerCase()
  // 去除HTML标签后比较
  const correctText = stripHtmlTags(currentQuestion.value.items[itemIndex].content_html || currentQuestion.value.items[itemIndex].content).trim().toLowerCase()
  
  if (shuffleOrder.value) {
    // 打乱模式：检查是否包含在任何位置
    return currentQuestion.value.items.some(item => 
      stripHtmlTags(item.content_html || item.content).trim().toLowerCase() === userText
    )
  } else {
    // 顺序模式：必须完全匹配
    return userText === correctText
  }
}

// 查看总结（所有题目批改完成后）
const showSummary = () => {
  // 确保最后一题已保存
  userAnswersList.value[currentIndex.value] = [...userAnswers.value]
  
  // 计算总分
  let totalScore = 0
  let correct = 0
  
  questions.value.forEach((q, idx) => {
    const userAns = userAnswersList.value[idx] || []
    let itemScore = 0
    const totalItems = q.items.length
    
    if (shuffleOrder.value) {
      // 打乱顺序模式
      const userTexts = userAns.map(t => t.trim().toLowerCase()).filter(t => t)
      const correctTexts = q.items.map(item => stripHtmlTags(item.content_html || item.content).trim().toLowerCase())
      
      let matched = 0
      userTexts.forEach(userText => {
        if (correctTexts.includes(userText)) {
          matched++
        } else {
          const found = correctTexts.findIndex(ct => 
            ct.includes(userText) || userText.includes(ct)
          )
          if (found !== -1) matched += 0.5
        }
      })
      itemScore = matched
    } else {
      // 顺序模式
      q.items.forEach((item, i) => {
        const userText = (userAns[i] || '').trim()
        const correctText = stripHtmlTags(item.content_html || item.content).trim()
        
        if (userText.toLowerCase() === correctText.toLowerCase()) {
          itemScore += 1
        } else if (userText.includes(correctText) || correctText.includes(userText)) {
          itemScore += 0.5
        }
      })
    }
    
    const questionScore = Math.round((itemScore / totalItems) * 100)
    totalScore += questionScore
    if (questionScore === 100) correct++
    results.value[idx] = questionScore === 100
  })
  
  score.value = Math.round(totalScore / questions.value.length)
  correctCount.value = correct
  
  showResult.value = true
  isPracticing.value = false
}

// 保留原来的submitAnswers作为备用
const submitAnswers = () => {
  showSummary()
}

const resetPractice = () => {
  startDictation()
}

const goBack = () => {
  isPracticing.value = false
  showResult.value = false
  questions.value = []
}

onMounted(async () => {
  await loadChapters()
})
</script>

<style scoped>
.dictation-practice-view {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.config-card {
  margin-bottom: 20px;
}

.config-card h3 {
  margin-bottom: 20px;
}

.config-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.config-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.config-item label {
  font-weight: bold;
  color: #666;
}

.config-item .el-select {
  width: 200px;
}

/* 章节统计样式 */
.chapter-stats {
  display: flex;
  gap: 16px;
  align-items: center;
  padding: 8px 16px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-left: 16px;
}

.chapter-stats .stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.chapter-stats .stat-label {
  font-size: 13px;
  color: #909399;
}

.chapter-stats .stat-value {
  font-size: 16px;
  font-weight: bold;
}

.chapter-stats .stat-item.total .stat-value {
  color: #409eff;
}

.chapter-stats .stat-item.must .stat-value {
  color: #f56c6c;
}

.chapter-stats .stat-item.important .stat-value {
  color: #e6a23c;
}

.chapter-stats .stat-item.normal .stat-value {
  color: #67c23a;
}

.config-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.priority-checkbox-group {
  display: flex;
  gap: 16px;
}

.priority-checkbox-group .el-checkbox {
  margin-right: 0;
}

.shuffle-checkbox {
  margin-bottom: 12px;
  color: #409eff;
  font-weight: 500;
}

.results-preview {
  margin-top: 24px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.results-preview h4 {
  margin-bottom: 12px;
  color: #333;
}

.preview-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.preview-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
}

.preview-item.correct {
  background: #e1f3d8;
  color: #67c23a;
}

.preview-item.wrong {
  background: #fef0f0;
  color: #f56c6c;
}

.preview-number {
  font-weight: 500;
}

.preview-status {
  font-weight: bold;
}

.preview-score {
  color: #909399;
}

.answer-reveal-section {
  margin-top: 24px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.answer-reveal-section h4 {
  margin-bottom: 16px;
  color: #333;
  font-size: 16px;
}

.reveal-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  background: #f5f7fa;
  border-radius: 6px;
  margin-bottom: 8px;
}

.reveal-number {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #409eff;
  color: white;
  border-radius: 50%;
  font-size: 13px;
  font-weight: bold;
  margin-right: 12px;
}

.reveal-content {
  flex: 1;
  color: #333;
  font-size: 15px;
}

.reveal-check {
  font-size: 18px;
  font-weight: bold;
  margin-left: 12px;
}

.reveal-check.correct {
  color: #67c23a;
}

.reveal-check.wrong {
  color: #f56c6c;
}

.practice-area {
  max-width: 800px;
  margin: 0 auto;
}

.question-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.priority-must {
  background: #ff4d4f;
  color: white;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.priority-important {
  background: #faad14;
  color: white;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.priority-normal {
  background: #52c41a;
  color: white;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.question-text {
  font-size: 18px;
  line-height: 1.8;
  color: #333;
}

.mnemonic-section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed #e0e0e0;
}

.mnemonic-btn {
  padding: 0;
  color: #faad14;
}

.mnemonic-content {
  margin-top: 10px;
  font-weight: bold;
  color: #fa8c16;
  font-size: 16px;
}

.answer-input-area {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.answer-item {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.answer-item:last-child {
  margin-bottom: 0;
}

.item-number {
  font-weight: bold;
  color: #1890ff;
  min-width: 28px;
  padding-top: 6px;
}

.answer-input {
  flex: 1;
}

.nav-section {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.result-area {
  max-width: 800px;
  margin: 0 auto;
}

.result-card {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.score-value {
  font-size: 32px;
  font-weight: bold;
  color: white;
}

.result-stats {
  display: flex;
  justify-content: center;
  gap: 60px;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  color: #666;
  font-size: 14px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.stat-value.correct {
  color: #52c41a;
}

.stat-value.wrong {
  color: #ff4d4f;
}

.questions-detail {
  margin-bottom: 24px;
}

.questions-detail h4 {
  margin-bottom: 16px;
}

.detail-item {
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  border-left: 4px solid;
}

.detail-item.correct {
  background: #f6ffed;
  border-color: #52c41a;
}

.detail-item.wrong {
  background: #fff2f0;
  border-color: #ff4d4f;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.detail-number {
  font-weight: bold;
  color: #333;
}

.result-correct {
  color: #52c41a;
  font-weight: bold;
}

.result-wrong {
  color: #ff4d4f;
  font-weight: bold;
}

.detail-question {
  color: #666;
  margin-bottom: 12px;
}

.detail-answers {
  display: flex;
  gap: 32px;
}

.answer-section {
  flex: 1;
}

.answer-label {
  display: block;
  color: #999;
  font-size: 14px;
  margin-bottom: 8px;
}

.answer-text {
  padding: 8px 12px;
  background: white;
  border-radius: 4px;
  margin-bottom: 4px;
}

.answer-text.correct-text {
  background: #f6ffed;
  color: #52c41a;
}

.result-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}
</style>

<!-- 全局样式用于v-html渲染的内容 -->
<style>
/* 默写练习模块中 - 正常显示所有内容（挖空也显示），批改时用stripHtmlTags比较 */

/* 首先覆盖所有可能的内联字体大小 */
.dictation-practice-view .reveal-content,
.dictation-practice-view .reveal-content * {
  font-size: inherit !important;
  font-size: 15px !important;
  line-height: inherit !important;
}

/* 覆盖blank-hidden及其内部所有元素的字体大小 */
.dictation-practice-view .reveal-content .blank-hidden,
.dictation-practice-view .reveal-content .blank-hidden *,
.dictation-practice-view .reveal-content .blank-hidden span,
.dictation-practice-view .reveal-content .blank-hidden b,
.dictation-practice-view .reveal-content .blank-hidden u,
.dictation-practice-view .reveal-content .blank-hidden i {
  font-size: inherit !important;
  background: transparent !important;
  color: inherit !important;
  padding: 0 !important;
  border: none !important;
  border-radius: 0 !important;
  cursor: default !important;
  margin: 0 !important;
  user-select: text !important;
  min-width: unset !important;
  display: inline !important;
  vertical-align: baseline !important;
  font-weight: normal !important;
  text-decoration: none !important;
  line-height: inherit !important;
}

/* 确保b/u/i标签也继承字体大小 */
.dictation-practice-view .reveal-content b,
.dictation-practice-view .reveal-content u,
.dictation-practice-view .reveal-content i {
  font-size: inherit !important;
  line-height: inherit !important;
}
</style>