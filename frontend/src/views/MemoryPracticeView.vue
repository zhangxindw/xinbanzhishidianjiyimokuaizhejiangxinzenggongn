<template>
  <div class="memory-practice-view" :style="`--dynamic-font-size: ${fontSize}px`">
    <div class="page-header">
      <h2>记忆练习 - 挖空模式</h2>
      <div class="header-info">
        <span>当前进度：{{ currentIndex + 1 }} / {{ tasks.length }}</span>
      </div>
    </div>

    <div class="settings-bar">
      <div class="settings-item">
        <span>字体大小:</span>
        <button size="small" @click="decreaseFontSize" class="el-button el-button--small">-</button>
        <span class="font-size-value">{{ fontSize }}px</span>
        <button size="small" @click="increaseFontSize" class="el-button el-button--small">+</button>
      </div>
    </div>

    <div v-if="currentTask" class="practice-content">
      <!-- 返回按钮（从关联跳转时显示） -->
      <div v-if="isJumped" class="jump-source-info">
        <el-button type="info" @click="goBack" class="back-btn">
          <el-icon><ArrowLeft /></el-icon>
          返回原题
        </el-button>
        <div class="source-detail">
          <span class="source-chapter">{{ jumpSourceInfo?.chapter }}</span>
          <span class="source-question">{{ jumpSourceInfo?.question?.substring(0, 50) }}{{ jumpSourceInfo?.question?.length > 50 ? '...' : '' }}</span>
          <span v-if="jumpSourceInfo?.sourceItem" class="source-item">
            关联答案：{{ jumpSourceInfo.sourceItem.content }}
          </span>
        </div>
      </div>
      
      <div class="question-card">
        <div class="question-header">
          <span :class="getPriorityClass(currentTask.knowledge_point.priority)">
            {{ currentTask.knowledge_point.priority_label }}
          </span>
          <span class="chapter-tag">{{ currentTask.knowledge_point.chapter_name }}</span>
          <span :class="getStatusClass(currentTask)" class="status-tag">
            {{ getStatusText(currentTask) }}
          </span>
          <el-button size="small" type="primary" @click="startQuestionEdit" class="edit-btn">
            <el-icon><Edit /></el-icon>
            编辑题目
          </el-button>
        </div>
        <!-- 题目编辑模式 -->
        <div v-if="isQuestionEditing" class="edit-mode" @click.stop>
          <div class="edit-toolbar" @click.stop>
            <button type="button" class="toolbar-btn" :class="{ active: currentTextStyle.bold }" @click="applyStyle('bold')">
              <b>B</b>
            </button>
            <button type="button" class="toolbar-btn" :class="{ active: currentTextStyle.underline }" @click="applyStyle('underline')">
              <u>U</u>
            </button>
            <button type="button" class="toolbar-btn" :class="{ active: currentTextStyle.highlight }" @click="applyStyle('highlight')">
              <span style="background: yellow;">高亮</span>
            </button>
          </div>
          <textarea
            ref="questionTextarea"
            v-model="editingQuestionHtml"
            class="edit-textarea"
            :rows="3"
            placeholder="请输入题目内容"
          ></textarea>
          <div class="edit-actions">
            <el-button type="success" size="small" @click="saveQuestionEdit">保存</el-button>
            <el-button type="info" size="small" @click="cancelQuestionEdit">取消</el-button>
          </div>
        </div>
        <!-- 题目显示模式 -->
        <div v-else class="question-text" :style="{ fontSize: fontSize + 'px' }" v-html="currentTask.knowledge_point.question_html"></div>
      </div>

      <div class="mnemonic-card">
        <el-button 
          type="text" 
          @click="showMnemonic = !showMnemonic"
          class="mnemonic-btn"
        >
          <el-icon><Star /></el-icon>
          {{ showMnemonic ? '隐藏口诀' : '偷看口诀' }}
        </el-button>
        <div v-if="showMnemonic" class="mnemonic-content">
          <span class="mnemonic-label">速记口诀：</span>
          <span class="mnemonic-text">{{ currentTask.knowledge_point.mnemonic }}</span>
        </div>
      </div>

      <div class="answers-section">
        <div class="answers-header">
          <h3>答案：</h3>
          <div class="blank-control">
            <el-button v-if="!isAnswerEditing" size="small" type="warning" @click="startAnswerEdit(-1)">
              <el-icon><Edit /></el-icon>
              编辑答案
            </el-button>
            <el-button v-if="isAnswerEditing" size="small" type="success" @click="saveAnswerEdit">
              <el-icon><Check /></el-icon>
              保存
            </el-button>
            <el-button v-if="isAnswerEditing" size="small" type="info" @click="cancelAnswerEdit">
              <el-icon><Close /></el-icon>
              取消
            </el-button>
            <el-button size="small" type="primary" @click="revealAllBlanks">
              <el-icon><View /></el-icon>
              一键显示挖空
            </el-button>
            <el-button size="small" type="info" @click="hideAllBlanks">
              <el-icon><Hide /></el-icon>
              一键隐藏挖空
            </el-button>
            <el-button size="small" :type="showAllAnswers ? 'primary' : 'success'" @click="toggleAllAnswers">
              <el-icon><View v-if="!showAllAnswers" /><Hide v-else /></el-icon>
              {{ showAllAnswers ? '隐藏全部答案' : '显示全部答案' }}
            </el-button>
          </div>
        </div>

        <!-- 答案编辑模式工具栏 -->
        <div v-if="isAnswerEditing" class="edit-mode answer-edit-toolbar" @click.stop>
          <div class="edit-toolbar" @click.stop>
            <button type="button" class="toolbar-btn" :class="{ active: currentTextStyle.bold }" @click="applyStyle('bold')" title="加粗">
              <b>B</b>
            </button>
            <button type="button" class="toolbar-btn" :class="{ active: currentTextStyle.underline }" @click="applyStyle('underline')" title="下划线">
              <u>U</u>
            </button>
            <button type="button" class="toolbar-btn" :class="{ active: currentTextStyle.highlight }" @click="applyStyle('highlight')" title="高亮">
              <span style="background: yellow;">高亮</span>
            </button>
            <button type="button" class="toolbar-btn" @click="insertBlank" title="插入挖空标记">
              <span style="color: #e6a23c;">[__]</span>
            </button>
          </div>
          <div class="edit-hint">
            <small>提示：用[[文字]]表示挖空内容，如：答案是[[这个]]</small>
          </div>
        </div>

        <div 
          v-for="(segments, index) in currentTaskSegments" 
          :key="index" 
          class="answer-item"
        >
          <span class="item-number">{{ index + 1 }}.</span>
          
          <!-- 答案编辑模式 -->
          <div v-if="isAnswerEditing" class="edit-mode-inline">
            <textarea
              v-model="editingAnswers[index]"
              class="edit-textarea"
              :rows="2"
              placeholder="请输入答案内容，用[[文字]]表示挖空"
              @focus="activeAnswerIndex = index"
            ></textarea>
          </div>
          
          <!-- 答案显示模式 - 使用v-html渲染content_html -->
          <div v-else class="item-content" :class="{ 'answers-hidden': !showAllAnswers }" :style="{ fontSize: fontSize + 'px' }" v-html="currentTask.knowledge_point.items[index].content_html || currentTask.knowledge_point.items[index].content">
          </div>
          <el-button 
            v-if="!isAnswerEditing && currentTask.knowledge_point.items[index].relations?.length > 0"
            size="small" 
            type="primary" 
            @click="handleRelationClick(currentTask.knowledge_point.items[index])"
            class="relation-btn"
          >
            <el-icon><Link /></el-icon>
            关联({{ currentTask.knowledge_point.items[index].relations?.length }})
          </el-button>
        </div>
      </div>

      <div class="feedback-section">
        <el-button type="success" @click.stop="handleFeedback('remembered')">
          <el-icon><VideoPlay /></el-icon>
          背出了
        </el-button>
        <el-button type="warning" @click.stop="handleFeedback('fuzzy')">
          <el-icon><Clock /></el-icon>
          模糊
        </el-button>
        <el-button type="danger" @click.stop="handleFeedback('forgot')">
          <el-icon><Delete /></el-icon>
          背不出
        </el-button>
      </div>

      <div class="nav-section">
        <el-button 
          :disabled="currentIndex === 0" 
          @click="prevTask"
        >
          <el-icon><RefreshRight /></el-icon>
          上一题
        </el-button>
        <el-button 
          :disabled="currentIndex === tasks.length - 1" 
          @click="nextTask"
        >
          下一题
          <el-icon><RefreshRight /></el-icon>
        </el-button>
      </div>
    </div>

    <div v-else class="empty-state">
      <el-icon size="48" color="#ccc"><Document /></el-icon>
      <p>暂无待练习的知识点</p>
      <el-button type="primary" @click="goToKnowledgePoints">
        <el-icon><Plus /></el-icon>
        添加知识点到记忆规划
      </el-button>
    </div>

    <el-dialog title="关联知识点" v-model="relationDialogVisible" width="600px">
      <el-input 
        v-model="relationSearch" 
        placeholder="搜索知识点"
        @keyup.enter="searchRelations"
      >
        <template #append>
          <el-button @click="searchRelations"><el-icon><Search /></el-icon></el-button>
        </template>
      </el-input>
      <el-table :data="relationList" border style="width: 100%; margin-top: 15px;">
        <el-table-column prop="question" label="知识点" />
        <el-table-column prop="chapter_name" label="章节" />
        <el-table-column label="操作">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="confirmRelation(row)">关联</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { Star, RefreshRight, VideoPlay, Delete, Clock, Document, Plus, Search, Link, View, Hide, ArrowLeft, Edit, Check, Close } from '@element-plus/icons-vue'

const tasks = ref([])
const currentIndex = ref(0)
const showMnemonic = ref(false)
const showAllAnswers = ref(false)  // 全部答案默认隐藏
const relationDialogVisible = ref(false)
const relationSearch = ref('')
const relationList = ref([])
const revealedBlanks = ref(new Map())
const fontSize = ref(18)  // 默认字体大小
const blankStates = ref(new Map())  // 用于跟踪每个挖空的状态

// 返回栈：记录跳转前的题目信息
const navigationHistory = ref([])
const isJumped = ref(false)  // 是否从关联跳转而来
const jumpSourceInfo = ref(null)  // 来源信息
const currentRelationItem = ref(null)  // 当前正在跳转的条目

// 编辑功能状态
const isQuestionEditing = ref(false)  // 题目是否处于编辑模式
const isAnswerEditing = ref(false)  // 答案是否处于编辑模式
const editingQuestionHtml = ref('')  // 编辑中的题目HTML
const editingAnswers = ref([])  // 编辑中的所有答案内容数组
const activeAnswerIndex = ref(0)  // 当前正在编辑的答案索引

// 富文本样式状态
const currentTextStyle = ref({
  bold: false,
  underline: false,
  highlight: false,
  color: '#333333'
})

const currentTask = computed(() => tasks.value[currentIndex.value])

// 计算属性：当前任务的所有答案片段
const currentTaskSegments = computed(() => {
  if (!currentTask.value || !currentTask.value.knowledge_point.items) {
    return []
  }
  
  return currentTask.value.knowledge_point.items.map((item, itemIndex) => {
    const content = item.content || ''
    const segments = []
    const regex = /\[\[(.*?)\]\]/g
    let lastEnd = 0
    let blankIndex = 0
    let match
    
    while ((match = regex.exec(content)) !== null) {
      if (match.index > lastEnd) {
        segments.push({
          text: content.substring(lastEnd, match.index),
          isBlank: false
        })
      }
      
      const key = `${currentIndex.value}-${itemIndex}-${blankIndex}`
      segments.push({
        text: match[1],
        isBlank: true,
        key: key,
        revealed: revealedBlanks.value.has(key)
      })
      
      lastEnd = match.index + match[0].length
      blankIndex++
    }
    
    if (lastEnd < content.length) {
      segments.push({
        text: content.substring(lastEnd),
        isBlank: false
      })
    }
    
    if (segments.length === 0) {
      segments.push({ text: content, isBlank: false })
    }
    
    return segments
  })
})

// 一键显示所有挖空
const revealAllBlanks = () => {
  // 直接在DOM中查找所有blank-hidden元素并添加blank-revealed class
  setTimeout(() => {
    const blankElements = document.querySelectorAll('.item-content .blank-hidden')
    blankElements.forEach(el => {
      el.classList.add('blank-revealed')
    })
  }, 0)
}

// 一键隐藏所有挖空
const hideAllBlanks = () => {
  // 直接在DOM中移除所有blank-revealed class
  setTimeout(() => {
    const revealedElements = document.querySelectorAll('.item-content .blank-revealed')
    revealedElements.forEach(el => {
      el.classList.remove('blank-revealed')
    })
  }, 0)
}

// 切换全部答案显示/隐藏
const toggleAllAnswers = () => {
  showAllAnswers.value = !showAllAnswers.value
}

// 初始化挖空点击事件（使用事件委托）
const initBlankClickEvents = () => {
  document.addEventListener('click', (e) => {
    // 检查是否点击了反馈按钮或其子元素，如果是则不处理
    let target = e.target
    while (target && target !== document) {
      if (target.classList && (
        target.classList.contains('feedback-section') ||
        target.classList.contains('el-button--success') ||
        target.classList.contains('el-button--warning') ||
        target.classList.contains('el-button--danger')
      )) {
        return // 点击的是反馈按钮区域，不处理
      }
      target = target.parentElement
    }
    
    // 检查是否点击了blank-hidden元素
    if (e.target.classList.contains('blank-hidden')) {
      e.target.classList.toggle('blank-revealed')
    }
  })
}

// 在组件挂载时初始化
onMounted(() => {
  initBlankClickEvents()
})

// 字体大小控制
const increaseFontSize = () => {
  console.log('increaseFontSize called, current:', fontSize.value)
  if (fontSize.value < 32) {
    fontSize.value += 2
    console.log('fontSize after:', fontSize.value)
  }
}

const decreaseFontSize = () => {
  console.log('decreaseFontSize called, current:', fontSize.value)
  if (fontSize.value > 12) {
    fontSize.value -= 2
    console.log('fontSize after:', fontSize.value)
  }
}

// ==================== 编辑功能 ====================

// 开始编辑题目
const startQuestionEdit = () => {
  if (!currentTask.value) return
  editingQuestionHtml.value = currentTask.value.knowledge_point.question_html || ''
  isQuestionEditing.value = true
}

// 保存题目编辑
const saveQuestionEdit = async () => {
  if (!currentTask.value) return
  try {
    console.log('保存题目，content:', editingQuestionHtml.value)
    const res = await axios.put(
      `/api/knowledge-points/${currentTask.value.knowledge_point.id}`,
      { question_html: editingQuestionHtml.value }
    )
    console.log('保存题目响应:', res.data)
    if (res.data.status === 'ok') {
      currentTask.value.knowledge_point.question_html = editingQuestionHtml.value
      isQuestionEditing.value = false
    }
  } catch (error) {
    console.error('保存题目失败:', error)
    alert('保存失败: ' + (error.response?.data?.message || error.message))
  }
}

// 取消题目编辑
const cancelQuestionEdit = () => {
  isQuestionEditing.value = false
  editingQuestionHtml.value = ''
}

// 开始编辑所有答案
const startAnswerEdit = () => {
  if (!currentTask.value) return
  // 初始化所有答案内容到编辑数组
  editingAnswers.value = currentTask.value.knowledge_point.items.map(
    item => item.content || ''
  )
  isAnswerEditing.value = true
}

// 保存所有答案编辑
const saveAnswerEdit = async () => {
  if (!currentTask.value) return
  try {
    console.log('开始保存答案，数量:', editingAnswers.value.length)
    // 遍历保存所有答案
    for (let i = 0; i < editingAnswers.value.length; i++) {
      console.log(`保存答案${i}:`, editingAnswers.value[i])
      const res = await axios.put(
        `/api/knowledge-points/${currentTask.value.knowledge_point.id}/items/${i}`,
        { 
          content: editingAnswers.value[i],
          content_html: editingAnswers.value[i]  // 同时发送HTML内容
        }
      )
      console.log(`答案${i}响应:`, res.data)
      if (res.data.status === 'ok') {
        currentTask.value.knowledge_point.items[i].content = editingAnswers.value[i]
        currentTask.value.knowledge_point.items[i].content_html = editingAnswers.value[i]
      }
    }
    isAnswerEditing.value = false
    console.log('答案保存完成')
  } catch (error) {
    console.error('保存答案失败:', error)
    alert('保存失败: ' + (error.response?.data?.message || error.message))
  }
}

// 取消答案编辑
const cancelAnswerEdit = () => {
  isAnswerEditing.value = false
  editingAnswers.value = []
}

// 应用富文本样式到选中文本（使用HTML标签）
const applyStyle = (style) => {
  console.log('applyStyle called with:', style)
  
  // 首先尝试获取当前聚焦的 textarea
  const focusedTextarea = document.querySelector('.edit-mode-inline .edit-textarea:focus')
  
  // 确定当前是编辑题目还是编辑答案
  const questionTextarea = document.querySelector('.edit-mode .edit-textarea')
  const allAnswerTextareas = document.querySelectorAll('.edit-mode-inline .edit-textarea')
  
  let textarea = null
  let isQuestionEdit = false
  let answerIndex = -1
  
  // 检查题目编辑模式
  if (questionTextarea && questionTextarea.offsetParent !== null) {
    textarea = questionTextarea
    isQuestionEdit = true
  }
  // 检查答案编辑模式
  else if (focusedTextarea) {
    textarea = focusedTextarea
    isQuestionEdit = false
    // 找出这个 textarea 对应的索引
    allAnswerTextareas.forEach((t, i) => {
      if (t === focusedTextarea) answerIndex = i
    })
  }
  // 如果没有聚焦的 textarea，使用 activeAnswerIndex
  else if (allAnswerTextareas.length > 0) {
    textarea = allAnswerTextareas[activeAnswerIndex.value]
    answerIndex = activeAnswerIndex.value
    isQuestionEdit = false
  }
  
  if (textarea) {
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    let selectedText = textarea.value.substring(start, end)
    
    console.log('选中文本:', JSON.stringify(selectedText), 'start:', start, 'end:', end, 'answerIndex:', answerIndex)
    
    if (selectedText) {
      let formattedText = selectedText
      let wrapperOpen = ''
      let wrapperClose = ''
      
      // 检查是否已经被这个样式包裹了，如果是则移除
      if (style === 'bold') {
        // 检查是否已经被<b>包裹
        if (selectedText.startsWith('<b') && selectedText.match(/^<b[^>]*>/)) {
          // 移除<b>标签
          formattedText = selectedText.replace(/^<b[^>]*>/, '').replace(/<\/b>$/, '')
        } else {
          wrapperOpen = '<b>'
          wrapperClose = '</b>'
        }
      } else if (style === 'underline') {
        // 检查是否已经被<u>包裹
        if (selectedText.startsWith('<u') && selectedText.match(/^<u[^>]*>/)) {
          formattedText = selectedText.replace(/^<u[^>]*>/, '').replace(/<\/u>$/, '')
        } else {
          wrapperOpen = '<u>'
          wrapperClose = '</u>'
        }
      } else if (style === 'highlight') {
        // 检查是否已经被高亮包裹
        if (selectedText.startsWith('<span') && selectedText.match(/^<span[^>]*style="background:/)) {
          formattedText = selectedText.replace(/^<span[^>]*>/, '').replace(/<\/span>$/, '')
        } else {
          wrapperOpen = '<span style="background: yellow;">'
          wrapperClose = '</span>'
        }
      }
      
      formattedText = wrapperOpen + formattedText + wrapperClose
      
      // 更新 Vue 响应式数据
      if (isQuestionEdit) {
        editingQuestionHtml.value = textarea.value.substring(0, start) + formattedText + textarea.value.substring(end)
      } else if (answerIndex >= 0) {
        editingAnswers.value[answerIndex] = textarea.value.substring(0, start) + formattedText + textarea.value.substring(end)
        console.log('更新editingAnswers[' + answerIndex + ']:', editingAnswers.value[answerIndex])
      }
      
      // 重新设置光标位置
      setTimeout(() => {
        textarea.focus()
        textarea.setSelectionRange(start, start + formattedText.length)
      }, 0)
    } else {
      console.log('没有选中文本，可能是因为点击按钮时textarea失去了焦点')
    }
  } else {
    console.log('没有找到可用的textarea')
    console.log('focusedTextarea:', focusedTextarea)
    console.log('questionTextarea:', questionTextarea)
    console.log('allAnswerTextareas:', allAnswerTextareas.length)
  }
  
  // 切换按钮状态（用于视觉反馈）
  if (style === 'bold') {
    currentTextStyle.value.bold = !currentTextStyle.value.bold
  } else if (style === 'underline') {
    currentTextStyle.value.underline = !currentTextStyle.value.underline
  } else if (style === 'highlight') {
    currentTextStyle.value.highlight = !currentTextStyle.value.highlight
  } else if (style === 'color') {
    currentTextStyle.value.color = currentTextStyle.value.color === '#333333' ? '#ff0000' : '#333333'
  }
  console.log('currentTextStyle now:', currentTextStyle.value)
}

// 插入样式标签
const insertStyleTags = (content, style) => {
  let result = content
  if (style.bold) {
    result = `**${result}**`
  }
  if (style.underline) {
    result = `__${result}__`
  }
  if (style.highlight) {
    result = `==${result}==`
  }
  if (style.color !== '#333333') {
    result = `<span style="color: ${style.color}">${result}</span>`
  }
  return result
}

// 获取答案片段的样式
const getSegmentStyle = (segment) => {
  const style = {}
  // 检查文本是否被**包裹（加粗）
  if (segment.text.startsWith('**') && segment.text.endsWith('**')) {
    style.fontWeight = 'bold'
  }
  // 检查文本是否被__包裹（下划线）
  if (segment.text.startsWith('__') && segment.text.endsWith('__')) {
    style.textDecoration = 'underline'
  }
  // 检查文本是否被==包裹（高亮）
  if (segment.text.startsWith('==') && segment.text.endsWith('==')) {
    style.backgroundColor = 'yellow'
  }
  // 检查是否有内联颜色样式
  const colorMatch = segment.text.match(/<span style="color: ([^"]+)">/)
  if (colorMatch) {
    style.color = colorMatch[1]
  }
  return style
}

// 插入挖空到当前编辑的答案（使用HTML）
const insertBlank = () => {
  // 首先尝试获取当前聚焦的 textarea
  const focusedTextarea = document.querySelector('.edit-mode-inline .edit-textarea:focus')
  const allAnswerTextareas = document.querySelectorAll('.edit-mode-inline .edit-textarea')
  
  let answerTextarea = null
  let answerIndex = -1
  
  if (focusedTextarea) {
    answerTextarea = focusedTextarea
    allAnswerTextareas.forEach((t, i) => {
      if (t === focusedTextarea) answerIndex = i
    })
  } else if (allAnswerTextareas.length > 0) {
    answerTextarea = allAnswerTextareas[activeAnswerIndex.value]
    answerIndex = activeAnswerIndex.value
  }
  
  if (answerTextarea) {
    const start = answerTextarea.selectionStart
    const end = answerTextarea.selectionEnd
    const selectedText = answerTextarea.value.substring(start, end)
    
    // 使用HTML标签表示挖空
    const blankContent = selectedText || ''
    const blankText = `<span class="blank-hidden">${blankContent}</span>`
    
    // 更新 Vue 响应式数据：before + blankText + after
    if (answerIndex >= 0) {
      const before = answerTextarea.value.substring(0, start)
      const after = answerTextarea.value.substring(end)
      editingAnswers.value[answerIndex] = before + blankText + after
      console.log('insertBlank: before=', before, 'blankText=', blankText, 'after=', after)
      console.log('insertBlank result:', editingAnswers.value[answerIndex])
    }
    
    // 设置光标位置
    setTimeout(() => {
      answerTextarea.focus()
      const newPos = start + blankText.length
      answerTextarea.setSelectionRange(newPos, newPos)
    }, 0)
  }
}

const loadTasks = async () => {
  try {
    const res = await axios.get('/api/memory/today-tasks?user_id=default_user')
    tasks.value = res.data.data || []
    
    // 初始化当前任务的状态
    tasks.value.forEach(task => {
      // 确保有learning_repetition字段
      if (task.learning_repetition === undefined) {
        task.learning_repetition = 0
      }
      // 初始化连续背出计数
      task.consecutiveRemembered = 0
    })
    
    console.log('加载的任务:', tasks.value)
  } catch (error) {
    console.error('加载任务失败:', error)
    alert('加载任务失败: ' + (error.response?.data?.message || error.message))
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

const getStatusClass = (task) => {
  if (!task) return 'status-learning'
  if (task.status === 'learning') {
    // 初学中状态
    if (task.today_consecutive_count > 0) {
      return 'status-learning-progress'
    }
    return 'status-learning'
  }
  // 复习中状态
  return 'status-reviewing'
}

const getStatusText = (task) => {
  if (!task) return '未知'
  if (task.status === 'learning') {
    // 初学中状态
    if (task.today_consecutive_count > 0) {
      return `初学中 (今日第${task.today_consecutive_count}次)`
    }
    return '初学中'
  }
  // 复习中状态
  return '复习中'
}

const toggleBlank = (key) => {
  if (revealedBlanks.value.has(key)) {
    revealedBlanks.value.delete(key)
  } else {
    revealedBlanks.value.set(key, true)
  }
  // 强制响应式更新
  revealedBlanks.value = new Map(revealedBlanks.value)
}

const handleFeedback = async (feedback) => {
  if (!currentTask.value) return
  
  // 立即重置显示状态（实时隐藏答案）
  showMnemonic.value = false
  showAllAnswers.value = false
  revealedBlanks.value = new Map()
  
  const currentIdx = currentIndex.value
  const kpId = currentTask.value.knowledge_point.id
  const currentTaskRef = currentTask.value  // 保存引用，避免后续操作影响
  
  // 调用后端API记录反馈
  try {
    const res = await axios.post('/api/memory/feedback?user_id=default_user', {
      kp_id: kpId,
      feedback
    })
    
    // 严格检查响应
    if (!res || !res.data) {
      console.error('API响应为空', res)
      alert('提交反馈失败: 网络响应异常')
      return
    }
    
    if (res.data.status !== 'ok') {
      console.error('API返回错误', res.data)
      alert('提交反馈失败: ' + (res.data.message || '未知错误'))
      return
    }
    
    const updatedRecord = res.data.data
    
    // 严格空值检查
    if (!updatedRecord || typeof updatedRecord !== 'object') {
      console.error('API返回数据为空或无效', res.data)
      alert('提交反馈失败: 服务器返回数据异常')
      return
    }
    
    // 安全访问status属性
    const recordStatus = updatedRecord.status
    const recordLearningRepetition = updatedRecord.learning_repetition
    const recordTodayConsecutiveCount = updatedRecord.today_consecutive_count
    
    // 根据后端返回的状态决定是否移除任务
    if (recordStatus === 'reviewing' && feedback === 'remembered') {
      // 进入复习状态，从当前任务列表中移除
      tasks.value.splice(currentIdx, 1)
      
      if (tasks.value.length === 0) {
        alert('今日记忆任务已完成！')
        await loadTasks()
        return
      }
      
      // 如果当前索引超出范围，调整索引
      if (currentIndex.value >= tasks.value.length) {
        currentIndex.value = Math.max(0, tasks.value.length - 1)
      }
    } else {
      // 初学中状态
      // 需求：安排在3个题目之后再次出现，如果没有题目则反复显示
      // 策略：每次点击背不出，learning_repetition = 3
      //       如果remainingCount < 3，移到末尾（反复循环）
      //       如果remainingCount >= 3，移到指定位置之后
      
      const remainingCount = tasks.value.length - currentIdx - 1
      
      console.log('当前任务处理 - kpId:', kpId, 'currentIdx:', currentIdx, 'remainingCount:', remainingCount, 'learning_repetition:', recordLearningRepetition)
      
      // 保存当前任务的ID
      const taskId = currentTaskRef.knowledge_point.id
      
      // 计算新位置
      let newPosition = currentIdx + recordLearningRepetition
      
      // 如果新位置超出范围，说明需要循环
      if (newPosition >= tasks.value.length) {
        // 需要循环：将任务移到末尾
        tasks.value.splice(currentIdx, 1)
        tasks.value.push(currentTaskRef)
        console.log('任务移到末尾，列表长度:', tasks.value.length)
      } else {
        // 不需要循环：直接移动到指定位置之后
        tasks.value.splice(currentIdx, 1)
        tasks.value.splice(newPosition, 0, currentTaskRef)
        console.log('任务移到位置', newPosition, '，列表长度:', tasks.value.length)
      }
      
      // 确保currentIndex有效
      if (currentIndex.value >= tasks.value.length) {
        currentIndex.value = tasks.value.length - 1
      }
    }
    
    // 更新当前任务的显示状态（用于UI反馈）
    currentTaskRef.status = recordStatus
    currentTaskRef.today_consecutive_count = recordTodayConsecutiveCount || 0
    currentTaskRef.learning_repetition = recordLearningRepetition
    
    console.log('反馈后 - tasks.length:', tasks.value.length, 'currentIndex:', currentIndex.value)
    
    // 每练习一个题目后，调用advance-repetition更新所有初学中的任务
    await updateLearningRepetitions()
    
  } catch (error) {
    console.error('提交反馈失败:', error)
    
    // 提取错误信息
    let errorMessage = '提交反馈失败'
    
    if (error.response) {
      // 服务器返回了错误状态码（4xx, 5xx）
      const status = error.response.status
      const data = error.response.data
      
      if (status === 404) {
        errorMessage = '该知识点未在记忆规划中，请先添加到记忆规划'
      } else if (data && data.message) {
        errorMessage = '提交反馈失败: ' + data.message
      } else {
        errorMessage = '提交反馈失败: 服务器错误 (' + status + ')'
      }
    } else if (error.request) {
      // 请求已发送但没有收到响应
      errorMessage = '提交反馈失败: 服务器无响应，请检查网络连接'
    } else {
      // 请求配置出错
      errorMessage = '提交反馈失败: ' + error.message
    }
    
    alert(errorMessage)
  }
}

// 更新所有初学中任务的learning_repetition（每完成一个题目就减1）
const updateLearningRepetitions = async () => {
  // 遍历所有任务，更新learning_repetition
  for (let i = tasks.value.length - 1; i >= 0; i--) {
    const task = tasks.value[i]
    
    // 只有初学中且learning_repetition > 0的任务才需要减1
    if (task.status === 'learning' && task.learning_repetition > 0) {
      try {
        await axios.post('/api/memory/advance-repetition?user_id=default_user', {
          kp_id: task.knowledge_point.id
        })
        
        // 更新本地任务状态
        task.learning_repetition -= 1
        
        console.log('更新任务', task.knowledge_point.id, '的learning_repetition:', task.learning_repetition)
      } catch (e) {
        console.error('更新循环进度失败', e)
      }
    }
  }
  
  // 不要过滤任何任务！所有任务都应该保留
  // 初学中的任务会循环出现，直到连续2次背出
  // 复习中的任务会按间隔出现
}

const prevTask = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    showMnemonic.value = false
    showAllAnswers.value = false
    revealedBlanks.value = new Map()
  }
}

const nextTask = () => {
  if (currentIndex.value < tasks.value.length - 1) {
    currentIndex.value++
    showMnemonic.value = false
    showAllAnswers.value = false
    revealedBlanks.value = new Map()
  }
}

const handleRelationClick = async (item) => {
  // 如果有关联信息，直接跳转或显示选择
  if (item.relations && item.relations.length > 0) {
    if (item.relations.length === 1) {
      // 只有一个关联，直接跳转（传递当前item作为来源）
      jumpToKnowledgePoint(item.relations[0].id, item)
    } else {
      // 多个关联，显示选择对话框
      currentRelationItem.value = item  // 保存当前条目
      relationList.value = item.relations
      relationDialogVisible.value = true
    }
  } else {
    // 没有关联，提示用户
    alert('该条目暂无关联知识点')
  }
}

const jumpToKnowledgePoint = async (kpId, sourceItem = null) => {
  // 保存当前任务信息到返回栈
  if (currentTask.value) {
    navigationHistory.value.push({
      index: currentIndex.value,
      task: currentTask.value,
      sourceItem: sourceItem
    })
  }
  
  // 查找任务列表中是否有该知识点
  const targetIndex = tasks.value.findIndex(t => t.knowledge_point.id === kpId)
  
  if (targetIndex !== -1) {
    // 在当前任务列表中，直接跳转
    currentIndex.value = targetIndex
    revealedBlanks.value = new Map()  // 重置挖空状态
    showMnemonic.value = false
    isJumped.value = true
    // 设置来源信息
    jumpSourceInfo.value = {
      chapter: currentTask.value.knowledge_point.chapter_name,
      question: currentTask.value.knowledge_point.question,
      sourceItem: sourceItem
    }
  } else {
    // 不在任务列表中，加载该知识点并添加到任务列表
    try {
      const res = await axios.get(`/api/knowledge-points/${kpId}`)
      const kp = res.data.data
      
      // 创建临时任务对象
      const tempTask = {
        knowledge_point: kp,
        consecutiveRemembered: 0
      }
      
      // 添加到当前任务后面
      tasks.value.splice(currentIndex.value + 1, 0, tempTask)
      
      // 跳转到新任务
      currentIndex.value = currentIndex.value + 1
      revealedBlanks.value = new Map()
      showMnemonic.value = false
      isJumped.value = true
      // 设置来源信息
      jumpSourceInfo.value = {
        chapter: navigationHistory.value.length > 0 
          ? navigationHistory.value[navigationHistory.value.length - 1].task.knowledge_point.chapter_name 
          : '',
        question: navigationHistory.value.length > 0 
          ? navigationHistory.value[navigationHistory.value.length - 1].task.knowledge_point.question 
          : '',
        sourceItem: sourceItem
      }
      
      console.log('已跳转到关联知识点:', kp.question.substring(0, 30))
    } catch (e) {
      console.error('跳转失败', e)
      alert('跳转失败: ' + (e.response?.data?.message || e.message))
    }
  }
  
  relationDialogVisible.value = false
}

// 返回函数
const goBack = () => {
  if (navigationHistory.value.length > 0) {
    const lastHistory = navigationHistory.value.pop()
    currentIndex.value = lastHistory.index
    tasks.value[currentIndex.value] = lastHistory.task
    revealedBlanks.value = new Map()
    showMnemonic.value = false
    isJumped.value = navigationHistory.value.length > 0
    jumpSourceInfo.value = null
  }
}

const searchRelations = async () => {
  const params = new URLSearchParams()
  if (relationSearch.value) params.set('keyword', relationSearch.value)
  const res = await axios.get('/api/knowledge-points?' + params)
  relationList.value = res.data.data || []
}

const confirmRelation = async (row) => {
  jumpToKnowledgePoint(row.id, currentRelationItem.value)
}

const goToKnowledgePoints = () => {
  window.location.href = '/knowledge-points'
}

onMounted(async () => {
  await loadTasks()
})
</script>

<style scoped>
.memory-practice-view {
  padding: 20px;
}

.settings-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.settings-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.font-size-value {
  min-width: 50px;
  text-align: center;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.practice-content {
  max-width: 900px;
  margin: 0 auto;
}

/* 编辑模式样式 */
.edit-mode {
  background: #f5f5f5;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
}

.edit-toolbar {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  align-items: center;
  flex-wrap: wrap;
  position: relative;
  z-index: 10;
}

.toolbar-btn {
  min-width: 36px;
  height: 32px;
  padding: 0 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.toolbar-btn:hover {
  border-color: #409eff;
  color: #409eff;
}

.toolbar-btn.active {
  background: #409eff;
  border-color: #409eff;
  color: #fff;
}

.color-picker-wrapper {
  position: relative;
  display: inline-flex;
}

.color-picker-wrapper .el-color-picker {
  position: relative;
  z-index: 1;
}

.edit-toolbar .el-button {
  min-width: 32px;
}

.edit-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.edit-hint {
  color: #999;
  margin-top: 8px;
}

.answer-edit-toolbar {
  background: #f5f5f5;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
}

.edit-mode-inline {
  flex: 1;
}

.edit-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  font-family: inherit;
}

.edit-textarea:focus {
  outline: none;
  border-color: #409eff;
}

.edit-mode-inline .el-textarea__inner {
  font-size: 14px;
}

.answer-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.edit-btn {
  flex-shrink: 0;
}

.jump-source-info {
  background: #fff7e6;
  border: 1px solid #ffd591;
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 16px;
}

.back-btn {
  margin-bottom: 8px;
}

.source-detail {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  color: #666;
}

.source-chapter {
  color: #1890ff;
  font-weight: 500;
}

.source-question {
  color: #333;
}

.source-item {
  color: #52c41a;
  font-style: italic;
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
  gap: 12px;
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

.chapter-tag {
  background: #e6f7ff;
  color: #1890ff;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.progress-tag {
  background: #f0f0f0;
  color: #666;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
  margin-left: auto;
}

.status-tag {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
}

.status-learning {
  background: #fffbe6;
  color: #faad14;
}

.status-learning-progress {
  background: #fff1f0;
  color: #ff4d4f;
}

.status-reviewing {
  background: #f6ffed;
  color: #52c41a;
}

.question-text {
  line-height: 1.8;
  color: #1a3a8a;  /* 深蓝色 */
  font-weight: bold;
  font-size: var(--dynamic-font-size) !important;
}

.mnemonic-card {
  background: #fffbe6;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}

.mnemonic-btn {
  padding: 0;
  color: #faad14;
}

.mnemonic-content {
  margin-top: 10px;
  font-size: 16px;
}

.mnemonic-label {
  color: #999;
}

.mnemonic-text {
  font-weight: bold;
  color: #fa8c16;
}

.answers-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.answers-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.answers-header h3 {
  margin: 0;
  color: #333;
}

.blank-control {
  display: flex;
  gap: 8px;
}

.answers-section h3 {
  margin-bottom: 16px;
  color: #333;
}

.answer-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.answer-item:last-child {
  border-bottom: none;
}

.item-number {
  font-weight: bold;
  color: #1890ff;
  min-width: 28px;
  font-size: var(--dynamic-font-size) !important;
}

.item-content {
  flex: 1;
  line-height: 1.6;
  font-size: var(--dynamic-font-size) !important;
}

/* 全部答案隐藏状态 */
.item-content.answers-hidden {
  color: transparent !important;
  background: #f5f5f5;
  border-radius: 4px;
  padding: 8px;
  position: relative;
}

.item-content.answers-hidden::before {
  content: '点击"显示全部答案"查看';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #999;
  font-size: 14px;
  white-space: nowrap;
}

/* 隐藏状态下所有子元素也隐藏 */
.item-content.answers-hidden * {
  color: transparent !important;
  visibility: hidden;
}

/* 确保item-content内的所有子元素也使用动态字体大小 */
.item-content * {
  font-size: inherit !important;
}

.normal-segment {
  color: #333;
  font-size: inherit !important;
}

.blank-hidden {
  background: transparent !important;
  color: transparent !important;
  padding: 0;
  border-bottom: 2px solid #1890ff;
  border-radius: 0;
  cursor: pointer;
  margin: 0 2px;
  user-select: none;
  min-width: 50px;
  display: inline-block;
  vertical-align: baseline;
  transition: all 0.2s;
}

.blank-hidden:hover {
  border-bottom-color: #409eff;
}

/* 确保blank-hidden内部元素的样式也被覆盖 */
.blank-hidden * {
  background: transparent !important;
  color: transparent !important;
}

.blank-revealed {
  background: #67c23a;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  cursor: pointer;
  margin: 0 2px;
  user-select: none;
  transition: all 0.2s;
}

.blank-revealed:hover {
  background: #5daf34;
}

.relation-btn {
  padding: 4px 12px;
}

.feedback-section {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
  position: relative;
  z-index: 100;
}

.feedback-section .el-button {
  padding: 12px 32px;
  font-size: 16px;
}

.nav-section {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.empty-state p {
  margin: 16px 0;
}
</style>

<!-- 全局样式用于v-html渲染的内容 -->
<style>
.blank-hidden {
  background: transparent !important;
  color: transparent !important;
  padding: 0;
  border-bottom: 2px solid #1890ff;
  border-radius: 0;
  cursor: pointer;
  margin: 0 2px;
  user-select: none;
  min-width: 50px;
  display: inline-block;
  vertical-align: baseline;
  transition: all 0.2s;
}

.blank-hidden:hover {
  border-bottom-color: #409eff;
}

.blank-hidden * {
  background: transparent !important;
  color: transparent !important;
}

.blank-revealed {
  background: #e6f7ff !important;
  color: #ff0000 !important;
  font-weight: bold !important;
  padding: 0 4px;
  border-bottom: none;
  margin: 0 4px;
}
</style>