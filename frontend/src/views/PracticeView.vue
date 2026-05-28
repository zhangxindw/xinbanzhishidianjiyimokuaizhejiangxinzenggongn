<template>
  <div class="practice-view" :class="eyeProtectionClass">
    <div class="settings-bar">
      <div class="settings-item">
        <span>护眼模式:</span>
        <el-select v-model="eyeProtectionMode" style="width: 120px;" @change="updateEyeProtection">
          <el-option label="关闭" value="none" />
          <el-option label="暖黄" value="warm" />
          <el-option label="浅灰" value="light" />
          <el-option label="深色" value="dark" />
          <el-option label="绿底" value="green" />
        </el-select>
      </div>
      <div class="settings-item">
        <span>字体大小:</span>
        <el-button size="small" @click="decreaseFontSize">-</el-button>
        <el-select v-model="fontSize" style="width: 120px;" @change="updateFontSize">
          <el-option label="极小" :value="12" />
          <el-option label="小" :value="14" />
          <el-option label="标准" :value="16" />
          <el-option label="大" :value="18" />
          <el-option label="特大" :value="20" />
          <el-option label="超大" :value="24" />
          <el-option label="巨大" :value="28" />
          <el-option label="最大" :value="32" />
        </el-select>
        <el-button size="small" @click="increaseFontSize">+</el-button>
      </div>
      <div class="settings-item">
        <span>字体:</span>
        <el-select v-model="fontFamily" style="width: 120px;" @change="updateFontFamily">
          <el-option label="微软雅黑" value="Microsoft YaHei" />
          <el-option label="宋体" value="SimSun" />
          <el-option label="黑体" value="SimHei" />
          <el-option label="仿宋" value="FangSong" />
        </el-select>
      </div>
    </div>

    <div v-if="!practiceStarted" class="start-screen">
      <div class="start-card">
        <h2>{{ practiceModeTitle }}</h2>
        <p>{{ practiceModeDescription }}</p>

        <div v-if="practiceMode === 'memorize' || practiceMode === 'sequential'" class="config-section">
          <div class="config-item">
            <label>选择章节:</label>
            <el-checkbox-group v-model="config.chapterIds">
              <el-checkbox v-for="ch in chapters" :key="ch.id" :label="ch.id">{{ ch.name }}</el-checkbox>
            </el-checkbox-group>
          </div>
        </div>

        <div v-if="practiceMode === 'random'" class="config-section">
          <div class="config-header">
            <h3>⚙️ 抽题设置</h3>
            <span class="config-tip">配置完成后点击开始练习</span>
          </div>

          <div class="config-grid">
            <div class="config-card">
              <div class="config-card-header">
                <el-icon><Document /></el-icon>
                <span>基础设置</span>
              </div>
              <div class="config-card-body">
                <div class="config-item">
                  <label>抽题数量:</label>
                  <el-input-number v-model="config.count" :min="1" style="width: 100%;" />
                </div>

                <div class="config-item">
                  <label>每题分数:</label>
                  <el-input-number v-model="config.score" :min="1" :max="100" style="width: 100%;" />
                </div>

                <div class="config-item">
                  <label>打乱选项:</label>
                  <div class="switch-wrapper">
                    <el-switch v-model="config.shuffleOptions" />
                    <span class="switch-label">{{ config.shuffleOptions ? '已启用' : '已禁用' }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="config-card">
              <div class="config-card-header">
                <el-icon><Folder /></el-icon>
                <span>章节范围</span>
              </div>
              <div class="config-card-body">
                <div class="config-item">
                  <label>选择章节:</label>
                  <div class="chapter-select-controls" style="display: flex; gap: 10px; align-items: center;">
                    <el-select v-model="config.chapterIds" multiple placeholder="选择章节（可选）" style="flex: 1;">
                      <el-option v-for="ch in chapters" :key="ch.id" :label="ch.name" :value="ch.id" />
                    </el-select>
                    <el-button class="chapter-select-btn" @click="selectAllChapters" size="small">全选</el-button>
                    <el-button class="chapter-clear-btn" @click="clearAllChapters" size="small">清空</el-button>
                  </div>
                  <span class="config-hint">不选择则从全部题库抽取</span>
                </div>

                <div v-if="config.chapterIds.length > 0" class="chapter-ratios-section">
                  <label class="ratios-label">各章节抽题比例:</label>
                  <div class="chapter-ratios">
                    <div v-for="chapterId in config.chapterIds" :key="chapterId" class="chapter-ratio-item">
                      <span class="chapter-ratio-label">{{ getChapterName(chapterId) }}</span>
                      <el-slider
                        v-model="config.chapterRatios[chapterId]"
                        :min="0"
                        :max="100"
                        :disabled="totalChapterRatio > 100"
                        show-input
                        style="flex: 1;"
                      />
                    </div>
                  </div>
                  <div class="ratio-summary" :class="{ 'ratio-error': totalChapterRatio > 100, 'ratio-warning': totalChapterRatio > 0 && totalChapterRatio < 100 }">
                    {{ ratioWarning }}
                  </div>
                </div>
              </div>
            </div>

            <div class="config-card">
              <div class="config-card-header">
                <el-icon><WarnTriangleFilled /></el-icon>
                <span>易错题</span>
              </div>
              <div class="config-card-body">
                <div class="config-item">
                  <label class="wrong-ratio-label">易错题比例 (%):</label>
                  <el-slider v-model="config.wrongRatio" :min="0" :max="100" show-input />
                </div>
                <div class="wrong-info-card">
                  <div class="wrong-info-title">📖 易错题说明</div>
                  <div class="wrong-info-content">
                    <ul>
                      <li>从错题本中错误次数大于2的题目中抽取</li>
                      <li>设为0则不抽取易错题</li>
                      <li>若选择了章节，易错题优先从选中章节中抽取</li>
                      <li>易错题数量不足时，自动用普通题目补足</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="config.chapterIds.length > 0" class="preview-card">
            <div class="preview-header">
              <h4>📊 抽题预览</h4>
            </div>
            <div class="preview-content">
              <div class="preview-stat">
                <span class="preview-label">总题数:</span>
                <span class="preview-value">{{ config.count }}</span>
              </div>
              <div class="preview-stat" v-if="config.wrongRatio > 0">
                <span class="preview-label">易错题:</span>
                <span class="preview-value">约 {{ Math.ceil(config.count * config.wrongRatio / 100) }} 题</span>
              </div>
              <div class="preview-chapters" v-if="config.chapterIds.length > 0">
                <span class="preview-label">各章节:</span>
                <div class="chapter-previews">
                  <div v-for="chapterId in config.chapterIds" :key="chapterId" class="chapter-preview">
                    <span class="chapter-name">{{ getChapterName(chapterId) }}</span>
                    <span class="chapter-count">{{ typeof getChapterPreviewCount(chapterId) === 'number' ? '约 ' + getChapterPreviewCount(chapterId) + ' 题' : getChapterPreviewCount(chapterId) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="practiceMode === 'wrong'" class="config-section">
          <p>错题本中共 {{ wrongCount }} 道错题</p>
        </div>

        <el-button type="primary" size="large" @click="startPractice" :disabled="practiceMode === 'sequential' && config.chapterIds.length === 0">
          开始练习
        </el-button>
      </div>
    </div>

    <div v-else class="practice-layout">
      <div class="practice-left" :style="{ width: leftPanelWidth + 'px' }">
        <div class="question-area">
          <div class="question-header">
            <span class="question-type">{{ currentQuestion?.question_type_name || '单选题' }}</span>
            <div class="question-actions">
              <el-button size="small" @click="toggleFavorite" :type="isFavorite ? 'warning' : 'default'">
                <el-icon><Star /></el-icon>
                {{ isFavorite ? '已收藏' : '收藏' }}
              </el-button>
              <el-button size="small" @click="toggleEditMode">
                <el-icon><Edit /></el-icon>
                {{ isEditMode ? '退出编辑' : '编辑题目' }}
              </el-button>
            </div>
            <div class="question-navigation">
              <el-button size="small" @click="prevQuestion" :disabled="currentIndex === 0">上一题</el-button>
              <span class="progress">{{ currentIndex + 1 }} / {{ questions.length }}</span>
              <el-button size="small" @click="nextQuestion" :disabled="currentIndex === questions.length - 1">下一题</el-button>
            </div>
          </div>

          <div v-if="isEditMode" class="edit-mode">
            <div class="editor-toolbar">
              <el-button size="small" @click="formatQuestion('bold')"><strong>B</strong></el-button>
              <el-button size="small" @click="formatQuestion('italic')"><em>I</em></el-button>
              <el-button size="small" @click="formatQuestion('underline')"><u>U</u></el-button>
              <el-button size="small" @click="formatQuestion('highlight-yellow')" style="background: #FFF176;">高亮</el-button>
              <el-button size="small" @click="formatQuestion('highlight-green')" style="background: #A5D6A7;">高亮</el-button>
              <el-color-picker v-model="editColor" size="small" @change="c => formatQuestion('color', c)" />
              <el-button size="small" @click="insertImageQuestion">插入图片</el-button>
              <el-button size="small" @click="insertTableQuestion">插入表格</el-button>
              <el-button size="small" @click="insertFormulaQuestion">插入公式</el-button>
              <el-button type="primary" size="small" @click="saveQuestionEdit">保存题目</el-button>
            </div>
            <div class="editor-content" ref="questionEditorRef" contenteditable></div>
          </div>

          <div v-else class="question-content" :style="contentStyle" v-html="currentQuestion?.stem_html || currentQuestion?.stem"></div>

          <div class="options-list" v-if="currentQuestion?.option_a">
            <div v-for="opt in displayOptions" :key="opt.label"
                 class="option-item"
                 :class="{
                   selected: isSelected(opt.label),
                   correct: (showAnswer || practiceMode === 'memorize') && isCorrectAnswer(opt.label),
                   wrong: showAnswer && isSelected(opt.label) && !isCorrectAnswer(opt.label)
                 }"
                 @click="selectOption(opt.label)">
              <span class="option-label" :style="contentStyle">{{ opt.label }}</span>
              <span class="option-text" :style="contentStyle" v-html="opt.html || opt.content"></span>
            </div>
          </div>

          <div class="question-tabs">
            <div v-for="(q, idx) in questions" :key="q.id || idx"
                 class="question-tab"
                 :class="{
                   active: idx === currentIndex,
                   answered: answeredQuestions[idx] !== undefined,
                   wrong: isWrong(idx)
                 }"
                 @click="goToQuestion(idx)">
              {{ idx + 1 }}
            </div>
          </div>
        </div>
      </div>

      <div class="resize-handle" @mousedown="startResize"></div>

      <div class="practice-right" :style="{ width: rightPanelWidth + 'px' }">
        <div class="answer-section">
          <div class="answer-header">
            <h3>答案解析</h3>
            <el-button size="small" @click="toggleExplanationEdit">
              <el-icon><Edit /></el-icon>
              {{ isExplanationEdit ? '退出编辑' : '编辑解析' }}
            </el-button>
          </div>

          <div class="answer-display" v-if="showAnswer || practiceMode === 'memorize'">
            <div class="answer-result">
              <span class="answer-label">正确答案:</span>
              <span class="answer-text">{{ currentQuestion?.answer }}</span>
            </div>

            <div v-if="isExplanationEdit" class="edit-mode">
              <div class="editor-toolbar">
                <el-button size="small" @click="formatExplanation('bold')"><strong>B</strong></el-button>
                <el-button size="small" @click="formatExplanation('italic')"><em>I</em></el-button>
                <el-button size="small" @click="formatExplanation('underline')"><u>U</u></el-button>
                <el-button size="small" @click="formatExplanation('highlight-yellow')" style="background: #FFF176;">高亮</el-button>
                <el-button size="small" @click="formatExplanation('highlight-green')" style="background: #A5D6A7;">高亮</el-button>
                <el-color-picker v-model="editColor" size="small" @change="c => formatExplanation('color', c)" />
                <el-button size="small" @click="insertImageExplanation">插入图片</el-button>
                <el-button size="small" @click="insertTableExplanation">插入表格</el-button>
                <el-button size="small" @click="insertFormulaExplanation">插入公式</el-button>
                <el-button type="primary" size="small" @click="saveExplanationEdit">保存解析</el-button>
              </div>
              <div class="editor-content" ref="explanationEditorRef" contenteditable></div>
            </div>

            <div v-else class="explanation-content" :style="explanationStyle" v-html="currentQuestion?.explanation_html || currentQuestion?.explanation || '暂无解析'"></div>
          </div>

          <div v-else class="answer-hidden">
            <p>选择选项后查看答案</p>
          </div>

          <div v-if="showAnswer && practiceMode !== 'memorize'" class="action-buttons">
            <el-button v-if="!isInWrongBook(currentQuestion?.id)" type="warning" @click="addToWrongBook">加入错题本</el-button>
            <el-button v-else type="success" @click="removeFromWrongBook">移出错题本</el-button>
            <el-button type="primary" @click="nextQuestion" v-if="currentIndex < questions.length - 1">下一题</el-button>
            <el-button @click="finishPractice">完成练习</el-button>
          </div>

          <div v-if="practiceMode === 'memorize'" class="action-buttons">
            <el-button @click="toggleMastered" :type="isMastered ? 'success' : 'default'">
              {{ isMastered ? '已掌握' : '标记为已掌握' }}
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 图片预览模态框 -->
    <div v-if="showImagePreview" class="image-preview-overlay" @click="closeImagePreview">
      <div class="image-preview-container" @click.stop>
        <div class="image-preview-close" @click="closeImagePreview">×</div>
        <img :src="previewImageUrl" alt="预览图片" class="image-preview-img" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuizStore } from '@/store/quiz'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useQuizStore()

const practiceMode = computed(() => {
  const path = route.path
  if (path.includes('memorize')) return 'memorize'
  if (path.includes('sequential')) return 'sequential'
  if (path.includes('random')) return 'random'
  if (path.includes('cross-chapter')) return 'cross-chapter'
  if (path.includes('wrong')) return 'wrong'
  return 'memorize'
})

const practiceModeTitle = computed(() => {
  const titles = {
    memorize: '背题模式',
    sequential: '顺序刷题',
    random: '随机出题',
    wrong: '错题练习'
  }
  return titles[practiceMode.value] || '练习'
})

const practiceModeDescription = computed(() => {
  const descriptions = {
    memorize: '自动展示答案和解析，适合记忆背诵，可选择特定章节',
    sequential: '按章节顺序依次练习题目',
    random: '从题库中随机抽取题目进行练习',
    wrong: '针对错题本中的题目进行专项练习'
  }
  return descriptions[practiceMode.value] || ''
})

const chapters = ref([])

const getChapterName = (chapterId) => {
  const chapter = chapters.value.find(ch => ch.id === chapterId)
  return chapter ? chapter.name : `章节${chapterId}`
}

const questions = ref([])
const currentIndex = ref(0)
const practiceStarted = ref(false)
const showAnswer = ref(false)
const lastAnswerCorrect = ref(false)
const answeredQuestions = ref({})
const isFavorite = ref(false)
const isInWrongBookMap = ref({})
const wrongCount = ref(0)
const totalQuestions = ref(0)

const isEditMode = ref(false)
const isExplanationEdit = ref(false)
const questionEditorRef = ref(null)
const explanationEditorRef = ref(null)
const editColor = ref('#000000')
const currentExplanationHtml = ref('')

const eyeProtectionMode = ref('none')
const fontSize = ref(16)
const fontFamily = ref('Microsoft YaHei')
const leftPanelWidth = ref(800)
const rightPanelWidth = ref(400)
const isResizing = ref(false)

// 图片预览相关
const showImagePreview = ref(false)
const previewImageUrl = ref('')

const openImagePreview = (url) => {
  previewImageUrl.value = url
  showImagePreview.value = true
}

const closeImagePreview = () => {
  showImagePreview.value = false
  previewImageUrl.value = ''
}

const startResize = (e) => {
  isResizing.value = true
  document.addEventListener('mousemove', doResize)
  document.addEventListener('mouseup', stopResize)
}

const doResize = (e) => {
  if (!isResizing.value) return
  const container = document.querySelector('.practice-layout')
  if (!container) return
  const containerRect = container.getBoundingClientRect()
  const totalWidth = containerRect.width
  const handleWidth = 8
  
  let newLeftWidth = e.clientX - containerRect.left
  
  if (newLeftWidth < 300) newLeftWidth = 300
  if (newLeftWidth > totalWidth - handleWidth - 250) newLeftWidth = totalWidth - handleWidth - 250
  
  const newRightWidth = totalWidth - newLeftWidth - handleWidth
  
  leftPanelWidth.value = newLeftWidth
  rightPanelWidth.value = newRightWidth
}

const stopResize = () => {
  isResizing.value = false
  document.removeEventListener('mousemove', doResize)
  document.removeEventListener('mouseup', stopResize)
}

const handleWindowResize = () => {
  const container = document.querySelector('.practice-layout')
  if (container) {
    const containerRect = container.getBoundingClientRect()
    const handleWidth = 8
    const totalWidth = containerRect.width
    const currentRatio = leftPanelWidth.value / (leftPanelWidth.value + rightPanelWidth.value + handleWidth)
    let newLeftWidth = totalWidth * currentRatio
    if (newLeftWidth < 300) newLeftWidth = 300
    if (newLeftWidth > totalWidth - handleWidth - 250) newLeftWidth = totalWidth - handleWidth - 250
    const newRightWidth = totalWidth - newLeftWidth - handleWidth
    leftPanelWidth.value = newLeftWidth
    rightPanelWidth.value = newRightWidth
  }
}

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleWindowResize)
  // 保存当前状态
  saveCurrentState()
})

// 监听当前索引变化，自动保存
watch(currentIndex, () => {
  saveCurrentState()
})

// 监听答题情况变化，自动保存
watch(answeredQuestions, () => {
  saveCurrentState()
}, { deep: true })

const config = reactive({
  count: 10,
  score: 5,
  shuffleOptions: true,
  chapterIds: [],
  chapterRatios: {},
  wrongRatio: 20
})

// 全选章节
const selectAllChapters = () => {
  config.chapterIds = chapters.value.map(ch => ch.id)
  // 只选中章节，不设置比例，让用户自己决定是否设置
}

// 清空章节选择
const clearAllChapters = () => {
  config.chapterIds = []
  config.chapterRatios = {}
}

// 检查章节比例总和
const totalChapterRatio = computed(() => {
  return config.chapterIds.reduce((sum, id) => {
    return sum + (config.chapterRatios[id] || 0)
  }, 0)
})

// 判断是否设置了章节比例
const hasChapterRatios = computed(() => {
  return config.chapterIds.some(id => (config.chapterRatios[id] || 0) > 0)
})

// 计算最终各章节比例
const finalChapterRatios = computed(() => {
  const ratios = {}
  if (!config.chapterIds.length) return ratios
  
  if (hasChapterRatios.value) {
    const setChapters = config.chapterIds.filter(id => (config.chapterRatios[id] || 0) > 0)
    const unsetChapters = config.chapterIds.filter(id => (config.chapterRatios[id] || 0) === 0)
    
    // 先设置已配置的比例
    setChapters.forEach(id => {
      ratios[id] = config.chapterRatios[id] || 0
    })
    
    // 分配剩余比例给未设置的章节
    if (unsetChapters.length > 0) {
      const remaining = 100 - Object.values(ratios).reduce((a, b) => a + b, 0)
      if (remaining > 0) {
        const eachRatio = Math.floor(remaining / unsetChapters.length)
        unsetChapters.forEach((id, i) => {
          if (i === unsetChapters.length - 1) {
            ratios[id] = remaining - eachRatio * (unsetChapters.length - 1)
          } else {
            ratios[id] = eachRatio
          }
        })
      }
    }
  }
  
  return ratios
})

// 比例警告
const ratioWarning = computed(() => {
  const total = totalChapterRatio.value
  if (!hasChapterRatios.value) return '未设置章节比例，将从选中章节随机抽取'
  if (total > 100) return `比例总和超过100% (${total}%)，请调整`
  if (total < 100) return `剩余 ${100 - total}% 将分配给未设置比例的章节`
  return '比例总和100%，完全按章节比例抽取'
})

// 计算各章节抽题数量预览
const getChapterPreviewCount = (chapterId) => {
  if (!hasChapterRatios.value) {
    return '随机'
  }
  const ratio = finalChapterRatios.value[chapterId] || 0
  return Math.ceil(config.count * ratio / 100)
}

// 保存当前刷题状态
const saveCurrentState = () => {
  if (practiceStarted.value) {
    store.savePracticeSession(practiceMode.value, {
      questions: questions.value,
      currentIndex: currentIndex.value,
      practiceStarted: practiceStarted.value,
      showAnswer: showAnswer.value,
      answeredQuestions: answeredQuestions.value,
      config: { ...config }
    })
  }
}

// 恢复保存的刷题状态
const restoreSavedState = async () => {
  const saved = store.getSavedPracticeSession(practiceMode.value)
  if (saved && saved.practiceStarted) {
    try {
      const { value } = await ElMessageBox.confirm(
        '检测到您有未完成的刷题进程，是否继续？',
        '提示',
        {
          confirmButtonText: '继续',
          cancelButtonText: '重新开始',
          type: 'info'
        }
      )
      if (value) {
        // 恢复状态
        questions.value = saved.questions
        currentIndex.value = saved.currentIndex
        practiceStarted.value = saved.practiceStarted
        showAnswer.value = saved.showAnswer
        answeredQuestions.value = saved.answeredQuestions
        config.count = saved.config?.count || 10
        config.chapterIds = saved.config?.chapterIds || []
        return true
      } else {
        // 清除保存的状态
        store.clearSavedPracticeSession(practiceMode.value)
      }
    } catch (error) {
      // 用户点击取消或关闭
      store.clearSavedPracticeSession(practiceMode.value)
    }
  }
  return false
}

const eyeProtectionClass = computed(() => {
  if (eyeProtectionMode.value === 'none') return ''
  return `eye-protection-${eyeProtectionMode.value}`
})

const contentStyle = computed(() => ({
  fontSize: fontSize.value + 'px !important',
  fontFamily: fontFamily.value + ' !important'
}))

// 解析内容的字体大小，最多只到24px
const explanationStyle = computed(() => ({
  fontSize: Math.min(fontSize.value, 24) + 'px !important',
  fontFamily: fontFamily.value + ' !important'
}))

const currentQuestion = computed(() => {
  return questions.value[currentIndex.value] || null
})

const displayOptions = computed(() => {
  if (!currentQuestion.value) return []
  if (currentQuestion.value.shuffled_options) {
    return currentQuestion.value.shuffled_options
  }
  const optionKeys = ['option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'option_f']
  const labels = ['A', 'B', 'C', 'D', 'E', 'F']
  return optionKeys.map((key, i) => {
    const q = currentQuestion.value
    return {
      label: labels[i],
      content: q[key],
      html: q[`${key}_html`]
    }
  }).filter(opt => opt.content)
})

const isSelected = (label) => {
  return answeredQuestions.value[currentIndex.value] === label
}

const isCorrectAnswer = (label) => {
  const answer = currentQuestion.value?.answer || currentQuestion.value?.shuffled_answer || ''
  return answer.toUpperCase().includes(label.toUpperCase())
}

const isWrong = (idx) => {
  if (answeredQuestions.value[idx] === undefined) return false
  const q = questions.value[idx]
  const answer = answeredQuestions.value[idx]
  return !q?.answer?.toUpperCase().includes(answer?.toUpperCase())
}

const isMastered = computed(() => {
  return false
})

const selectOption = async (label) => {
  if (practiceMode.value === 'memorize' || showAnswer.value) return

  answeredQuestions.value[currentIndex.value] = label
  showAnswer.value = true

  const questionId = currentQuestion.value.id
  try {
    const result = await store.submitAnswer(questionId, label)
    lastAnswerCorrect.value = result.is_correct

    if (!result.is_correct) {
      isInWrongBookMap.value[questionId] = true
    }
  } catch (error) {
    console.error('Submit answer failed:', error)
  }
}

const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    resetQuestionState()
  }
}

const nextQuestion = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    resetQuestionState()
  }
}

const goToQuestion = (index) => {
  currentIndex.value = index
  resetQuestionState()
}

const resetQuestionState = () => {
  showAnswer.value = answeredQuestions.value[currentIndex.value] !== undefined
  checkFavorite()
}

const startPractice = async () => {
  try {
    // 先尝试恢复保存的状态
    const restored = await restoreSavedState()
    if (restored) {
      totalQuestions.value = questions.value.length
      await checkFavorite()
      return
    }

    let result
    if (practiceMode.value === 'memorize') {
      const params = { per_page: 10000 }
      if (config.chapterIds.length > 0) {
        params.chapter_id = config.chapterIds[0]
      }
      result = await store.practiceMemorize(params)
      questions.value = result.data
    } else if (practiceMode.value === 'sequential') {
      result = await store.practiceSequential({
        chapter_ids: config.chapterIds
      })
      questions.value = result.data
    } else if (practiceMode.value === 'random') {
      result = await store.practiceRandom({
        count: config.count,
        score: config.score,
        shuffle_options: config.shuffleOptions,
        chapter_ids: config.chapterIds,
        chapter_ratios: config.chapterRatios,
        wrong_ratio: config.wrongRatio
      })
      questions.value = result.data
    } else if (practiceMode.value === 'wrong') {
      result = await store.practiceWrongQuestions({ shuffle: true })
      questions.value = result.data
    }

    practiceStarted.value = true
    totalQuestions.value = result.total || questions.value.length
    showAnswer.value = practiceMode.value === 'memorize'
    await checkFavorite()
  } catch (error) {
    ElMessage.error('加载题目失败')
  }
}

const checkFavorite = async () => {
  if (!currentQuestion.value?.id) return
  try {
    isFavorite.value = await store.checkFavorite(currentQuestion.value.id)
  } catch (error) {
    isFavorite.value = false
  }
}

const toggleFavorite = async () => {
  if (!currentQuestion.value?.id) return
  try {
    if (isFavorite.value) {
      await store.removeFromFavorites(currentQuestion.value.id)
      isFavorite.value = false
      ElMessage.success('已取消收藏')
    } else {
      await store.addToFavorites(currentQuestion.value.id)
      isFavorite.value = true
      ElMessage.success('已添加收藏')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const isInWrongBook = (questionId) => {
  return isInWrongBookMap.value[questionId] || false
}

const addToWrongBook = async () => {
  if (!currentQuestion.value?.id) return
  try {
    await store.addToWrongQuestions(currentQuestion.value.id)
    isInWrongBookMap.value[currentQuestion.value.id] = true
    ElMessage.success('已加入错题本')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const removeFromWrongBook = async () => {
  if (!currentQuestion.value?.id) return
  try {
    const wrongQ = store.wrongQuestions.find(wq => wq.question_id === currentQuestion.value.id)
    if (wrongQ) {
      await store.removeFromWrongQuestions(wrongQ.id)
    }
    isInWrongBookMap.value[currentQuestion.value.id] = false
    ElMessage.success('已移出错题本')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const toggleMastered = () => {
  ElMessage.info('已掌握状态标记')
}

const finishPractice = () => {
  const correctCount = Object.values(answeredQuestions.value).filter((answer, idx) => {
    return questions.value[idx]?.answer?.toUpperCase() === answer?.toUpperCase()
  }).length

  ElMessageBox.alert(
    `练习完成！<br>正确率: ${correctCount}/${Object.keys(answeredQuestions.value).length}`,
    '练习结果',
    { confirmButtonText: '确定', type: 'success', dangerouslyUseHTMLString: true }
  ).then(() => {
    // 清除保存的状态
    store.clearSavedPracticeSession(practiceMode.value)
    router.push('/home')
  })
}

const toggleEditMode = async () => {
  isEditMode.value = !isEditMode.value
  if (isEditMode.value) {
    await nextTick()
    if (questionEditorRef.value && currentQuestion.value) {
      questionEditorRef.value.innerHTML = currentQuestion.value.stem_html || currentQuestion.value.stem || ''
    }
  }
}

const toggleExplanationEdit = async () => {
  isExplanationEdit.value = !isExplanationEdit.value
  if (isExplanationEdit.value) {
    await nextTick()
    if (explanationEditorRef.value && currentQuestion.value) {
      explanationEditorRef.value.innerHTML = currentQuestion.value.explanation_html || currentQuestion.value.explanation || ''
    }
  }
}

const formatText = (editor, command, value = null) => {
  if (!editor) return
  editor.focus()
  if (command === 'color') {
    document.execCommand('foreColor', false, value)
  } else if (command.startsWith('highlight-')) {
    const selection = window.getSelection()
    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0)
      const span = document.createElement('span')
      span.className = command
      range.surroundContents(span)
    }
  } else {
    document.execCommand(command, false, value)
  }
}

const formatQuestion = (command, value = null) => {
  formatText(questionEditorRef.value, command, value)
}

const formatExplanation = (command, value = null) => {
  formatText(explanationEditorRef.value, command, value)
}

const insertImageQuestion = () => {
  if (!questionEditorRef.value) return
  const url = prompt('请输入图片URL:')
  if (url) {
    document.execCommand('insertImage', false, url)
  }
}

const insertImageExplanation = () => {
  if (!explanationEditorRef.value) return
  const url = prompt('请输入图片URL:')
  if (url) {
    document.execCommand('insertImage', false, url)
  }
}

const insertTableQuestion = () => {
  if (!questionEditorRef.value) return
  const tableHtml = '<table border="1" style="border-collapse: collapse;"><tr><td>单元格</td><td>单元格</td></tr><tr><td>单元格</td><td>单元格</td></tr></table>'
  document.execCommand('insertHTML', false, tableHtml)
}

const insertTableExplanation = () => {
  if (!explanationEditorRef.value) return
  const tableHtml = '<table border="1" style="border-collapse: collapse;"><tr><td>单元格</td><td>单元格</td></tr><tr><td>单元格</td><td>单元格</td></tr></table>'
  document.execCommand('insertHTML', false, tableHtml)
}

const insertFormulaQuestion = () => {
  if (!questionEditorRef.value) return
  const formula = prompt('请输入LaTeX公式:')
  if (formula) {
    const html = `<span class="formula">$$${formula}$$</span>`
    document.execCommand('insertHTML', false, html)
  }
}

const insertFormulaExplanation = () => {
  if (!explanationEditorRef.value) return
  const formula = prompt('请输入LaTeX公式:')
  if (formula) {
    const html = `<span class="formula">$$${formula}$$</span>`
    document.execCommand('insertHTML', false, html)
  }
}

const saveQuestionEdit = async () => {
  if (!currentQuestion.value?.id || !questionEditorRef.value) return
  try {
    await store.updateQuestion(currentQuestion.value.id, {
      stem_html: questionEditorRef.value.innerHTML
    })
    currentQuestion.value.stem_html = questionEditorRef.value.innerHTML
    isEditMode.value = false
    ElMessage.success('题目已更新')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const saveExplanationEdit = async () => {
  if (!currentQuestion.value?.id || !explanationEditorRef.value) return
  try {
    await store.updateQuestion(currentQuestion.value.id, {
      explanation_html: explanationEditorRef.value.innerHTML
    })
    currentQuestion.value.explanation_html = explanationEditorRef.value.innerHTML
    isExplanationEdit.value = false
    ElMessage.success('解析已更新')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const updateEyeProtection = () => {
  store.updatePreferences({ eye_protection_mode: eyeProtectionMode.value })
}

const updateFontSize = () => {
  store.updatePreferences({ font_size: fontSize.value })
}

const updateFontFamily = () => {
  store.updatePreferences({ font_family: fontFamily.value })
}

const increaseFontSize = () => {
  if (fontSize.value < 40) {
    fontSize.value += 2
    updateFontSize()
  }
}

const decreaseFontSize = () => {
  if (fontSize.value > 8) {
    fontSize.value -= 2
    updateFontSize()
  }
}

onMounted(async () => {
  try {
    await store.loadChapters()
    chapters.value = store.chapters
    await store.loadWrongQuestions({ user_id: store.userId })
    wrongCount.value = store.wrongQuestions.length
    await store.loadQuestions()
    totalQuestions.value = store.questions.length

    const prefs = store.preferences
    eyeProtectionMode.value = prefs.eye_protection_mode || 'none'
    fontSize.value = prefs.font_size || 16
    fontFamily.value = prefs.font_family || 'Microsoft YaHei'

    await nextTick()
    const container = document.querySelector('.practice-layout')
    if (container) {
      const containerRect = container.getBoundingClientRect()
      const handleWidth = 8
      const totalWidth = containerRect.width
      leftPanelWidth.value = Math.max(300, totalWidth * 0.65)
      rightPanelWidth.value = Math.max(250, totalWidth - leftPanelWidth.value - handleWidth)
    }
    
    window.addEventListener('resize', handleWindowResize)
    
    // 初始绑定图片点击事件
    bindImageClickEvents()
  } catch (error) {
    console.error('初始化失败:', error)
    ElMessage.error('页面加载失败，请刷新重试')
  }
})

// 监听刷题模式变化，重置组件状态
watch(practiceMode, (newMode, oldMode) => {
  if (newMode !== oldMode) {
    // 重置所有状态
    questions.value = []
    currentIndex.value = 0
    practiceStarted.value = false
    showAnswer.value = false
    answeredQuestions.value = {}
    isFavorite.value = false
    isInWrongBookMap.value = {}
    totalQuestions.value = store.questions.length
    config.count = 10
    config.chapterIds = []
    isEditMode.value = false
    isExplanationEdit.value = false
  }
})

watch(() => store.preferences, (prefs) => {
  if (prefs) {
    eyeProtectionMode.value = prefs.eye_protection_mode || 'none'
    fontSize.value = prefs.font_size || 16
    fontFamily.value = prefs.font_family || 'Microsoft YaHei'
  }
}, { deep: true })

// 监听题目变化，为图片绑定点击事件
watch(currentQuestion, () => {
  nextTick(() => {
    bindImageClickEvents()
  })
})

const bindImageClickEvents = () => {
  const images = document.querySelectorAll('.question-content img, .option-text img, .explanation-content img')
  images.forEach(img => {
    // 移除之前的事件监听器（避免重复绑定）
    img.style.cursor = 'zoom-in'
    img.onclick = (e) => {
      e.stopPropagation()
      openImagePreview(img.src)
    }
  })
}
</script>

<style scoped>
.practice-view {
  padding: 20px;
  min-height: 100vh;
  background: #ffffff; /* 默认白色背景 */
  font-size: 14px; /* 默认字体大小，确保子元素不继承内容区域的字体 */
}

.settings-bar {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  font-size: 14px !important; /* 强制设置字体大小，不继承 */
}

.settings-bar * {
  font-size: 14px !important; /* 确保设置栏内所有元素都使用固定字体 */
}

.settings-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.start-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  font-size: 16px;
}

.start-screen * {
  font-size: inherit !important;
}

.start-card {
  background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
  padding: 48px;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(0, 0, 0, 0.04);
  text-align: center;
  max-width: 500px;
  border: 1px solid #f3f4f6;
}

.start-card h2 {
  font-size: 28px !important;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 12px;
}

.start-card > p {
  color: #6b7280;
  font-size: 15px;
  margin-bottom: 32px;
}

.start-card .el-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  padding: 16px 48px;
  font-size: 16px;
  font-weight: 700;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.start-card .el-button--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
}

.chapter-select-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
  color: white;
  font-weight: 600;
  padding: 8px 20px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.chapter-select-btn:hover {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.chapter-clear-btn {
  background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
  border: none;
  color: white;
  font-weight: 600;
  padding: 8px 20px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.chapter-clear-btn:hover {
  background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(75, 85, 99, 0.3);
}

.ratios-label {
  display: block;
  margin-bottom: 12px;
  font-weight: 700;
  color: #0369a1;
  font-size: 14px;
}

.wrong-ratio-label {
  display: block;
  margin-bottom: 12px;
  font-weight: 700;
  color: #92400e;
  font-size: 14px;
}

.config-section {
  margin: 20px 0;
  text-align: left;
  font-size: 14px !important;
}

.config-section * {
  font-size: 14px !important;
}

.config-item {
  margin-bottom: 20px;
}

.config-item:last-child {
  margin-bottom: 0;
}

.config-item label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.chapter-ratios {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  padding: 20px;
  border-radius: 12px;
  margin-top: 16px;
  border: 1px solid #bae6fd;
}

.chapter-ratio-item {
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.chapter-ratio-item:last-child {
  margin-bottom: 0;
}

.chapter-ratio-label {
  min-width: 150px;
  font-weight: 600;
  color: #0369a1;
  font-size: 14px;
}

.ratio-summary {
  margin-top: 16px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border-radius: 8px;
  color: #166534;
  font-size: 13px;
  font-weight: 500;
  border: 1px solid #86efac;
}

.ratio-summary.ratio-error {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
  border-color: #fca5a5;
}

.ratio-summary.ratio-warning {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border-color: #fcd34d;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.config-card {
  background: #ffffff;
  border-radius: 16px;
  border: none;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.config-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12), 0 4px 12px rgba(0, 0, 0, 0.08);
}

.config-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #a855f7 100%);
  color: white;
  font-weight: 700;
  font-size: 15px;
  letter-spacing: 0.3px;
}

.config-card-header .el-icon {
  font-size: 20px;
}

.config-card-body {
  padding: 24px;
  background: #fafbfc;
}

.config-hint {
  font-size: 12px !important;
  color: #6b7280;
  margin-top: 8px;
  padding: 8px 12px;
  background: #f3f4f6;
  border-radius: 6px;
  border-left: 3px solid #9ca3af;
}

.switch-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.switch-label {
  font-size: 14px;
  color: #4b5563;
  font-weight: 500;
}

.wrong-info-card {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 12px;
  padding: 18px;
  margin-top: 18px;
  border: 1px solid #fbbf24;
}

.wrong-info-title {
  font-weight: 700;
  color: #92400e;
  margin-bottom: 12px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.wrong-info-content ul {
  margin: 0;
  padding-left: 20px;
}

.wrong-info-content li {
  margin-bottom: 8px;
  color: #78350f;
  font-size: 13px !important;
  line-height: 1.6;
}

.preview-card {
  background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #a5b4fc;
  box-shadow: 0 4px 20px rgba(79, 70, 229, 0.1);
}

.preview-header {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.preview-header h4 {
  margin: 0;
  font-size: 17px;
  color: #3730a3;
  font-weight: 700;
}

.preview-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.preview-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
}

.preview-label {
  font-weight: 600;
  color: #4b5563;
  font-size: 14px;
}

.preview-value {
  font-weight: 700;
  color: #4f46e5;
  font-size: 15px;
}

.preview-chapters {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chapter-previews {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chapter-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 18px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.chapter-preview:hover {
  border-color: #a5b4fc;
  transform: translateX(4px);
}

.chapter-name {
  font-weight: 600;
  color: #1f2937;
  font-size: 14px;
}

.chapter-count {
  color: #4f46e5;
  font-weight: 700;
  font-size: 14px;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 18px;
  border-bottom: 2px solid #f3f4f6;
}

.config-header h3 {
  margin: 0;
  font-size: 20px;
  color: #111827;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
}

.config-tip {
  font-size: 13px !important;
  color: #6b7280;
  padding: 8px 14px;
  background: #f3f4f6;
  border-radius: 20px;
  font-weight: 500;
}

.start-card {
  max-width: 1200px;
}

.practice-layout {
  display: flex;
  width: 100%;
  max-width: 100%;
  overflow: hidden;
}

.practice-left {
  min-width: 300px;
  max-width: calc(100% - 258px);
  flex-shrink: 0;
}

.practice-right {
  min-width: 250px;
  max-width: calc(100% - 308px);
  flex-shrink: 0;
  overflow: hidden;
  width: var(--right-panel-width, 400px);
}

/* 最强约束：解析框内所有元素都不允许超出 */
.answer-section,
.answer-display,
.explanation-content {
  width: 100% !important;
  max-width: 100% !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
}

/* 终极约束：解析框内的图片必须完全适应 */
.explanation-content img {
  width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
  display: block !important;
  margin: 10px 0 !important;
  box-sizing: border-box !important;
  object-fit: contain !important;
}

.resize-handle {
  width: 8px;
  cursor: col-resize;
  background: transparent;
  transition: background 0.2s;
  flex-shrink: 0;
}

.resize-handle:hover {
  background: #667eea;
}

.question-area {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  font-size: 14px; /* 基础字体大小 */
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  font-size: 14px !important;
  gap: 15px;
  flex-wrap: wrap;
}

.question-header .question-type {
  order: 1;
}

.question-header .question-actions {
  order: 2;
}

.question-header .question-navigation {
  order: 3;
  margin-left: auto;
}

.question-header * {
  font-size: 14px !important;
}

.question-type {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 14px !important;
  flex-shrink: 0;
}

.question-actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.question-navigation {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 14px !important;
  flex-shrink: 0;
}

.question-content {
  line-height: 1.8;
  margin-bottom: 30px;
  /* 字体大小通过内联样式控制，不在这里设置 */
}

/* 确保题干内图片完全自适应 */
.question-content img {
  max-width: 100% !important;
  width: 100% !important;
  height: auto !important;
  display: block;
  margin: 10px 0;
  box-sizing: border-box;
}

.options-list {
  margin: 20px 0;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  margin: 10px 0;
  border: 3px solid #a3d5a3; /* 更清晰的绿色系边框 */
  border-radius: 10px;
  background: linear-gradient(145deg, #f0fdf0, #e6f7e6); /* 浅绿渐变背景 */
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px !important;
}

.option-item:hover {
  border-color: #7cb87c;
  background: linear-gradient(145deg, #d4f4d4, #c4ecc4);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(100, 180, 100, 0.2);
}

.option-item.selected {
  border-color: #667eea;
  background: linear-gradient(145deg, #f0f3ff, #e6ebff);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.option-item.correct {
  border-color: #1890ff;
  background: linear-gradient(145deg, #e6f7ff, #d6f0ff);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.2);
}

.option-item.wrong {
  border-color: #ff4d4f;
  background: linear-gradient(145deg, #fff0f0, #ffe1e1);
  box-shadow: 0 4px 12px rgba(255, 77, 79, 0.2);
}

.option-label {
  font-weight: bold;
  min-width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #5a5a5a 0%, #3a3a3a 100%);
  color: white;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(90, 90, 90, 0.3);
  flex-shrink: 0;
  /* 字体大小通过内联样式控制 */
}

.option-text {
  flex: 1;
  /* 字体大小通过内联样式控制 */
}

.progress {
  font-size: 14px !important;
  font-weight: 500;
}

.question-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
  padding: 20px;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  background: #fafafa;
}

.question-tab {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #e0e0e0;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px !important;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.question-tab:hover {
  border-color: #667eea;
  background: #f5f3ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.question-tab.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
}

.question-tab.answered {
  border-color: #67c23a;
  background: #f0f9eb;
  color: #67c23a;
}

.question-tab.wrong {
  border-color: #f56c6c;
  background: #fef0f0;
  color: #f56c6c;
}

.answer-section {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  height: fit-content;
  overflow: hidden;
  box-sizing: border-box;
  width: 100%;
}

.answer-section .answer-header,
.answer-section .answer-result,
.answer-section .answer-label,
.answer-section .answer-text,
.answer-section .action-buttons,
.answer-section .el-button {
  font-size: 14px !important;
}

.answer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.answer-header h3 {
  font-size: 18px !important;
}

.answer-display {
  margin-top: 20px;
}

/* 确保解析内容区域的其他样式 */
/* 题干和选项内的图片也保持约束 */
.question-content img,
.option-text img {
  max-width: 100% !important;
  width: auto !important;
  height: auto !important;
  display: inline-block !important;
  margin: 10px 0 !important;
  box-sizing: border-box !important;
}

/* 确保题干、选项、解析内的所有富文本元素都正确继承字体大小 */
.question-content *,
.option-text *,
.explanation-content * {
  font-size: inherit !important;
  font-family: inherit !important;
}

/* 确保加粗、下划线等富文本元素也继承字体大小 */
.question-content b,
.question-content strong,
.question-content u,
.question-content span,
.question-content div,
.option-text b,
.option-text strong,
.option-text u,
.option-text span,
.option-text div,
.explanation-content b,
.explanation-content strong,
.explanation-content u,
.explanation-content span,
.explanation-content div {
  font-size: inherit !important;
  font-family: inherit !important;
}

.answer-result {
  padding: 15px;
  background: #f0f9ff;
  border-radius: 8px;
  margin-bottom: 20px;
}

.answer-label {
  font-weight: 500;
  color: #1890ff;
}

.answer-text {
  font-weight: bold;
  color: #67c23a;
  margin-left: 10px;
}

.explanation-content {
  line-height: 1.8;
  color: #333;
  /* 字体大小通过内联样式控制 */
  overflow: hidden;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  position: relative;
}

.answer-hidden {
  text-align: center;
  padding: 40px;
  color: #999;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.edit-mode {
  margin: 15px 0;
}

.editor-toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
  padding: 10px;
  background: #f5f5f5;
  border-radius: 6px;
  flex-wrap: wrap;
}

.editor-content {
  min-height: 150px;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  outline: none;
}

.eye-protection-warm {
  background: #fdf6e3;
}

.eye-protection-warm .settings-bar {
  background: #fff9f0;
  border: 2px solid #f0e0c8;
}

.eye-protection-warm .start-card {
  background: #fff9f0;
  border: 2px solid #f0e0c8;
}

.eye-protection-warm .config-section {
  background: #fff5e6;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #f0e0c8;
}

.eye-protection-warm .question-area {
  background: #fff9f0;
  border: 2px solid #f0e0c8;
}

.eye-protection-warm .question-content,
.eye-protection-warm .option-text,
.eye-protection-warm .explanation-content {
  color: #5a4a3a;
}

.eye-protection-warm .option-item {
  background: #ffffff;
  border: 2px solid #e8d8c8;
}

.eye-protection-warm .option-item:hover {
  background: #fff5e6;
  border-color: #d4a574;
}

.eye-protection-warm .option-label {
  background: linear-gradient(135deg, #8b7355, #6b5344);
}

.eye-protection-warm .answer-section {
  background: #fff9f0;
  border: 2px solid #f0e0c8;
}

.eye-protection-warm .answer-result {
  background: #fff5e6;
  border-left: 4px solid #d4a574;
}

.eye-protection-light {
  background: #f5f5f5;
}

.eye-protection-light .settings-bar {
  background: #ffffff;
  border: 2px solid #e0e0e0;
}

.eye-protection-light .start-card {
  background: #ffffff;
  border: 2px solid #e0e0e0;
}

.eye-protection-light .config-section {
  background: #fafafa;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.eye-protection-light .question-area {
  background: #ffffff;
  border: 2px solid #e0e0e0;
}

.eye-protection-light .question-content,
.eye-protection-light .option-text,
.eye-protection-light .explanation-content {
  color: #333333;
}

.eye-protection-light .option-item {
  background: #ffffff;
  border: 2px solid #d0d0d0;
}

.eye-protection-light .option-item:hover {
  background: #f8f8f8;
  border-color: #909090;
}

.eye-protection-light .option-label {
  background: linear-gradient(135deg, #606060, #404040);
}

.eye-protection-light .answer-section {
  background: #ffffff;
  border: 2px solid #e0e0e0;
}

.eye-protection-light .answer-result {
  background: #f5f5f5;
  border-left: 4px solid #606060;
}

.eye-protection-dark {
  background: #1e1e1e;
}

.eye-protection-dark .settings-bar {
  background: #2a2a2a;
  border: 2px solid #3a3a3a;
}

.eye-protection-dark .start-card {
  background: #2a2a2a;
  border: 2px solid #3a3a3a;
}

.eye-protection-dark .config-section {
  background: #252525;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #3a3a3a;
}

.eye-protection-dark .question-area {
  background: #2a2a2a;
  border: 2px solid #3a3a3a;
  color: #d4d4d4;
}

.eye-protection-dark .question-content,
.eye-protection-dark .option-text,
.eye-protection-dark .explanation-content {
  color: #d4d4d4;
}

.eye-protection-dark .option-item {
  background: #2d2d2d;
  border: 2px solid #4a4a4a;
  color: #d4d4d4;
}

.eye-protection-dark .option-item:hover {
  background: #353535;
  border-color: #606060;
}

.eye-protection-dark .option-label {
  background: linear-gradient(135deg, #5a5a5a, #3a3a3a);
  color: #d4d4d4;
}

.eye-protection-dark .answer-section {
  background: #2a2a2a;
  border: 2px solid #3a3a3a;
  color: #d4d4d4;
}

.eye-protection-dark .answer-result {
  background: #252525;
  border-left: 4px solid #5a5a5a;
}

.eye-protection-dark .answer-label,
.eye-protection-dark .answer-text {
  color: #d4d4d4;
}

.eye-protection-green {
  background: #c8e4c8;
}

.eye-protection-green .settings-bar {
  background: #d8edd8;
  border: 2px solid #a8d8a8;
}

.eye-protection-green .start-card {
  background: #d8edd8;
  border: 2px solid #a8d8a8;
}

.eye-protection-green .config-section {
  background: #e0f0e0;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #a8d8a8;
}

.eye-protection-green .question-area {
  background: #d8edd8;
  border: 2px solid #a8d8a8;
  color: #1a3a1a;
}

.eye-protection-green .question-content,
.eye-protection-green .option-text,
.eye-protection-green .explanation-content {
  color: #1a3a1a;
}

.eye-protection-green .option-item {
  background: #e8f5e8;
  border: 2px solid #98d898;
}

.eye-protection-green .option-item:hover {
  background: #d0f0d0;
  border-color: #70c070;
}

.eye-protection-green .option-label {
  background: linear-gradient(135deg, #4a7a4a, #2a5a2a);
}

.eye-protection-green .answer-section {
  background: #d8edd8;
  border: 2px solid #a8d8a8;
  color: #1a3a1a;
}

.eye-protection-green .answer-result {
  background: #e8f5e8;
  border-left: 4px solid #70c070;
}

.eye-protection-green .answer-label {
  color: #2a6a2a;
}

.eye-protection-green .answer-text {
  color: #1a5a1a;
}

.eye-protection-green .question-area,
.eye-protection-green .answer-section {
  background: rgb(207, 232, 204);
  color: #000000;
}

.eye-protection-green .question-content,
.eye-protection-green .explanation-content {
  color: #000000;
}

.eye-protection-green .option-item.correct {
  border: 4px solid #1890ff !important;
  background: linear-gradient(145deg, #e6f7ff, #d6f0ff) !important;
  box-shadow: 0 0 20px rgba(24, 144, 255, 0.4), inset 0 0 15px rgba(24, 144, 255, 0.2) !important;
  transform: scale(1.02);
}

.eye-protection-green .option-label {
  background: linear-gradient(135deg, #5a5a5a, #3a3a3a) !important;
  box-shadow: 0 3px 10px rgba(90, 90, 90, 0.4) !important;
}

.highlight-yellow {
  background: #FFF176;
  padding: 2px 4px;
  border-radius: 3px;
}

.highlight-green {
  background: #A5D6A7;
  padding: 2px 4px;
  border-radius: 3px;
}

/* 图片预览样式 */
.image-preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: zoom-out;
}

.image-preview-container {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  cursor: default;
}

.image-preview-close {
  position: absolute;
  top: 10px;
  right: 15px;
  font-size: 32px;
  color: white;
  cursor: pointer;
  z-index: 10;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
  line-height: 1;
}

.image-preview-close:hover {
  color: #ff6b6b;
}

.image-preview-img {
  max-width: 100%;
  max-height: 90vh;
  display: block;
  width: auto;
  height: auto;
  object-fit: contain;
}
</style>
