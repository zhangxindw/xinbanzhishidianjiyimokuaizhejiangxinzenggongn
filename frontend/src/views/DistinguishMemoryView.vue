<template>
  <div class="distinguish-memory">
    <div class="page-header">
      <div class="header-left">
        <div class="title-row">
          <h2>辨析记忆</h2>
          <span class="page-subtitle">艾宾浩斯遗忘曲线</span>
        </div>
        <div class="progress-info" v-if="tasks.length > 0">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: ((currentIndex + 1) / tasks.length * 100) + '%' }"></div>
          </div>
          <span class="progress-text">剩余 {{ tasks.length }} 题</span>
        </div>
      </div>
      <div class="header-right">
        <div class="font-control" v-if="currentTask">
          <span class="font-label">字体</span>
          <div class="font-buttons">
            <button type="button" class="font-btn" @click.stop="decreaseFont">−</button>
            <span class="font-value">{{ fontSize }}px</span>
            <button type="button" class="font-btn" @click.stop="increaseFont">+</button>
            <button type="button" class="font-reset-btn" @click.stop="resetFont" title="重置">↺</button>
          </div>
        </div>
        <button type="button" @click="exitPractice" class="exit-btn">
          <span class="icon-close">✕</span>
          退出
        </button>
      </div>
    </div>

    <div v-if="tasks.length === 0" class="empty-state">
      <div class="empty-content">
        <div class="empty-icon">
          <span class="icon-check">✓</span>
        </div>
        <h3>太棒了！</h3>
        <p>暂无待复习的辨析题</p>
        <button type="button" @click="exitPractice" class="return-btn">
          <span class="icon-arrow-left">←</span>
          返回规划
        </button>
      </div>
    </div>

    <div class="question-card" v-if="currentTask">
      <div class="card-header">
        <div class="tags-row">
          <span class="chapter-tag">{{ currentTask.chapter_name || '未分类' }}</span>
          <span :class="currentTask.status === 'learning' ? 'status-learning' : 'status-reviewing'">
            <span class="icon-clock">⏱</span>
            {{ currentTask.status === 'learning' ? '初学中' : '复习中' }}
          </span>
        </div>
        <div class="card-number">{{ currentIndex + 1 }} / {{ tasks.length }}</div>
      </div>
      
      <div class="question-stem" v-html="currentTask.question_stem_html || currentTask.question_stem" :style="{ fontSize: fontSize + 'px' }"></div>
      
      <div class="option-display">
        <div class="option-badge" :style="{ fontSize: fontSize + 'px' }">{{ currentTask.option_key }}.</div>
        <div class="option-content" :style="{ fontSize: fontSize + 'px' }">{{ currentTask.option_text }}</div>
      </div>

      <div v-if="!answered" class="action-buttons">
        <button type="button" class="action-btn correct-btn" @click="submitAnswer('remembered')">
          <span class="btn-symbol">✓</span>
          <span>正确</span>
        </button>
        <button type="button" class="action-btn wrong-btn" @click="submitAnswer('forgot')">
          <span class="btn-symbol">✗</span>
          <span>错误</span>
        </button>
      </div>

      <div v-if="answered" class="result-section">
        <div :class="isCorrect ? 'result-header correct' : 'result-header wrong'">
          <div class="result-icon">
            <span class="result-symbol">{{ isCorrect ? '✓' : '✗' }}</span>
          </div>
          <div class="result-info">
            <div class="result-title">{{ isCorrect ? '选择正确' : '选择错误' }}</div>
            <div class="result-desc">标准答案：
              <span class="answer-inline" :class="currentTask.is_correct ? 'correct' : 'wrong'">
                {{ currentTask.is_correct ? '正确' : '错误' }}
              </span>
            </div>
          </div>
          <button type="button" @click="nextQuestion" class="next-btn-inline">
            {{ currentIndex < tasks.length - 1 ? '下一题' : '完成' }}
            <span class="icon-arrow-right">→</span>
          </button>
        </div>

        <div v-if="!currentTask.is_correct && currentTask.corrected_text" class="correction-row">
          <div class="correction-tag">
            <span class="tag-icon">✎</span>
            <span class="tag-text">正确表述</span>
          </div>
          <div class="correction-text" :style="{ fontSize: fontSize + 'px' }">{{ currentTask.corrected_text }}</div>
        </div>

        <div v-if="currentTask.question_explanation || currentTask.question_explanation_html" class="explanation-row">
          <div class="explanation-tag">
            <span class="tag-icon">ℹ</span>
            <span class="tag-text">解析</span>
          </div>
          <div class="explanation-content" v-html="currentTask.question_explanation_html || currentTask.question_explanation" :style="{ fontSize: fontSize + 'px' }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import axios from "axios"

const tasks = ref([])
const currentIndex = ref(0)
const answered = ref(false)
const isCorrect = ref(false)
const userId = "default_user"

const fontSize = ref(16)
const minFont = 12
const maxFont = 28
const defaultFont = 16

const increaseFont = () => {
  if (fontSize.value < maxFont) {
    fontSize.value += 2
  }
}

const decreaseFont = () => {
  if (fontSize.value > minFont) {
    fontSize.value -= 2
  }
}

const resetFont = () => {
  fontSize.value = defaultFont
}

const currentTask = computed(() => tasks.value[currentIndex.value] || null)

const pendingInterval = ref(null)
const pendingTaskId = ref(null)
const totalUniqueTasks = ref(0)

const loadTasks = async () => {
  try {
    const res = await axios.get("/api/distinguish/plan/tasks", {
      params: { t: Date.now() }
    })
    tasks.value = res.data.data || []
    totalUniqueTasks.value = tasks.value.length
    currentIndex.value = 0
    answered.value = false
    isCorrect.value = false
    pendingInterval.value = null
    pendingTaskId.value = null
  } catch (e) { console.error(e) }
}

const submitAnswer = async (feedback) => {
  const task = currentTask.value
  if (!task) return

  const userChoseCorrect = (feedback === "remembered")
  isCorrect.value = userChoseCorrect === task.is_correct

  // ★★★ 先清除之前的 pendingInterval，防止 API 失败时使用过期数据 ★★★
  pendingInterval.value = null
  pendingTaskId.value = null

  try {
    const res = await axios.post("/api/distinguish/plan/feedback", {
      record_id: task.id,
      feedback: feedback
    })

    const repeatInfo = res.data.repeat_info
    if (repeatInfo && repeatInfo.interval !== undefined) {
      pendingInterval.value = repeatInfo.interval
      pendingTaskId.value = task.id
    } else {
      pendingInterval.value = null
      pendingTaskId.value = null
    }

    answered.value = true
  } catch (e) {
    console.error(e)
    pendingInterval.value = null
    pendingTaskId.value = null
    answered.value = true
  }
}

const nextQuestion = () => {
  const task = currentTask.value

  // ★★★ pendingInterval 必须匹配当前任务 ID，防止过期间隔误用 ★★★
  if (pendingInterval.value !== null && pendingTaskId.value === task?.id) {
    // 需要重新插入：先移除，再随机插入到至少 interval 题之后的位置
    const interval = pendingInterval.value
    pendingInterval.value = null
    pendingTaskId.value = null

    if (task) {
      tasks.value.splice(currentIndex.value, 1)

      // 随机插入到 [currentIndex + interval, tasks.length) 范围内
      // 题目不会固定在同一个位置出现，防止假性记忆
      const minPos = currentIndex.value + interval
      const maxPos = tasks.value.length

      let insertPos
      if (minPos >= maxPos) {
        // 剩余题目不足，放到末尾
        insertPos = maxPos
      } else {
        // 在合法范围内随机选择位置
        insertPos = minPos + Math.floor(Math.random() * (maxPos - minPos))
      }

      if (insertPos >= tasks.value.length) {
        tasks.value.push(task)
      } else {
        tasks.value.splice(insertPos, 0, task)
      }
    }
  } else {
    // 毕业或间隔不匹配：直接移除，不再放回
    pendingInterval.value = null
    pendingTaskId.value = null
    if (task) {
      tasks.value.splice(currentIndex.value, 1)
    }
  }

  answered.value = false
  isCorrect.value = false

  // 所有题目已毕业，返回规划页
  if (tasks.value.length === 0) {
    exitPractice()
    return
  }

  // currentIndex 超出范围则回到开头（处理重新插入的题目）
  if (currentIndex.value >= tasks.value.length) {
    currentIndex.value = 0
  }
}

const exitPractice = () => {
  window.location.href = "/distinguish/plan"
}

onMounted(loadTasks)
</script>

<style scoped>
.distinguish-memory {
  padding: 20px 32px;
  min-height: calc(100vh - 60px);
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
  box-sizing: border-box;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px 24px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 32px;
  flex: 1;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h2 {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.page-subtitle {
  font-size: 12px;
  color: #94a3b8;
  padding: 3px 10px;
  background: #f1f5f9;
  border-radius: 12px;
  font-weight: 500;
}

.progress-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-bar {
  width: 180px;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 3px;
  transition: width 0.4s ease;
}

.progress-text {
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  min-width: 50px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.font-control {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.font-label {
  font-size: 13px;
  color: #475569;
  font-weight: 600;
}

.font-buttons {
  display: flex;
  align-items: center;
  gap: 6px;
}

.font-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: white;
  color: #475569;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  font-size: 16px;
  font-weight: bold;
}

.font-btn:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.font-reset-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: white;
  color: #475569;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  font-size: 16px;
}

.font-reset-btn:hover {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  border-color: transparent;
}

.exit-btn {
  background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
  color: white;
  border: none;
  padding: 8px 18px;
  border-radius: 8px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  cursor: pointer;
}

.exit-btn:hover {
  opacity: 0.9;
}

.icon-close {
  font-size: 16px;
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.empty-content {
  text-align: center;
  padding: 50px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 400px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.icon-check {
  font-size: 48px;
  color: white;
  font-weight: bold;
}

.empty-content h3 {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.empty-content p {
  font-size: 15px;
  color: #64748b;
  margin: 0 0 24px 0;
}

.return-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 10px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
}

.return-btn:hover {
  opacity: 0.9;
}

.icon-arrow-left {
  font-size: 18px;
}

.question-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.tags-row {
  display: flex;
  gap: 10px;
}

.chapter-tag {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1d4ed8;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
}

.status-learning {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #b45309;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}

.status-reviewing {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #059669;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}

.icon-clock {
  font-size: 14px;
}

.card-number {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 700;
}

.question-stem {
  line-height: 1.7;
  color: #1e293b;
  margin-bottom: 16px;
  padding: 18px;
  background: #f8fafc;
  border-radius: 12px;
  font-weight: 500;
  transition: font-size 0.15s ease;
}

.option-display {
  display: flex;
  gap: 14px;
  padding: 20px;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  border-radius: 12px;
  border: 2px solid #cbd5e1;
  line-height: 1.7;
  color: #1e293b;
  font-weight: 500;
  transition: font-size 0.15s ease;
}

.option-badge {
  font-weight: 800;
  color: #475569;
  min-width: 36px;
}

.option-content {
  flex: 1;
}

.action-buttons {
  display: flex;
  gap: 12px;
  margin-top: 18px;
  padding-top: 18px;
  border-top: 1px dashed #e2e8f0;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:active {
  transform: scale(0.98);
}

.btn-symbol {
  font-size: 20px;
  font-weight: bold;
}

.correct-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.correct-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.4);
}

.wrong-btn {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(248, 113, 113, 0.3);
}

.wrong-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(248, 113, 113, 0.4);
}

.result-section {
  margin-top: 18px;
  padding-top: 18px;
  border-top: 1px dashed #e2e8f0;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  margin-bottom: 14px;
}

.result-header.correct {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
}

.result-header.wrong {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
}

.result-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.result-symbol {
  font-size: 28px;
  font-weight: bold;
}

.result-header.correct .result-icon {
  background: rgba(16, 185, 129, 0.3);
  color: #059669;
}

.result-header.correct .result-symbol {
  color: #059669;
}

.result-header.wrong .result-icon {
  background: rgba(239, 68, 68, 0.3);
  color: #dc2626;
}

.result-header.wrong .result-symbol {
  color: #dc2626;
}

.result-info {
  flex: 1;
}

.result-title {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 2px;
}

.result-header.correct .result-title {
  color: #059669;
}

.result-header.wrong .result-title {
  color: #dc2626;
}

.result-desc {
  font-size: 13px;
  color: #475569;
}

.answer-inline {
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  margin-left: 4px;
}

.answer-inline.correct {
  background: rgba(16, 185, 129, 0.2);
  color: #059669;
}

.answer-inline.wrong {
  background: rgba(239, 68, 68, 0.2);
  color: #dc2626;
}

.next-btn-inline {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  cursor: pointer;
}

.next-btn-inline:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.icon-arrow-right {
  font-size: 16px;
}

.correction-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 14px;
  background: #fef2f2;
  border-radius: 10px;
  margin-bottom: 12px;
  border: 1px solid #fecaca;
}

.correction-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: white;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  padding: 4px 10px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  align-self: flex-start;
}

.tag-icon {
  font-size: 12px;
}

.correction-text {
  line-height: 1.7;
  color: #991b1b;
  transition: font-size 0.15s ease;
}

.explanation-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 14px;
  background: #fefce8;
  border-radius: 10px;
  border: 1px solid #fde68a;
}

.explanation-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: white;
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  padding: 4px 10px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  align-self: flex-start;
}

.explanation-content {
  line-height: 1.7;
  color: #475569;
  transition: font-size 0.15s ease;
}

@media (max-width: 768px) {
  .distinguish-memory {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .header-left {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .header-right {
    justify-content: space-between;
  }
  
  .progress-bar {
    width: 100%;
  }
}
</style>