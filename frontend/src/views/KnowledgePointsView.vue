<template>
  <div class="knowledge-points-view">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h2 class="page-title">
          <el-icon><Document /></el-icon>
          知识点管理
        </h2>
        <span class="total-badge">共 {{ total }} 个知识点</span>
      </div>
      <div class="header-actions">
        <el-button type="success" plain @click="goToMemoryPlan">
          <el-icon><Calendar /></el-icon>
          记忆规划
        </el-button>
        <el-button type="warning" plain @click="goToDictation">
          <el-icon><EditPen /></el-icon>
          默写练习
        </el-button>
        <el-button type="info" @click="showImportDialog">
          <el-icon><Upload /></el-icon>
          Excel导入
        </el-button>
        <el-button type="primary" @click="createKnowledgePoint">
          <el-icon><Plus /></el-icon>
          添加知识点
        </el-button>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-section">
      <div class="filter-group">
        <el-checkbox 
          v-model="selectAll" 
          @change="handleSelectAll"
          :indeterminate="isIndeterminate"
          class="select-all-checkbox"
        >
          全选
        </el-checkbox>
        
        <el-button 
          type="danger" 
          plain 
          :disabled="selectedIds.length === 0"
          @click="batchDelete"
          class="batch-delete-btn"
        >
          <el-icon><Delete /></el-icon>
          批量删除 ({{ selectedIds.length }})
        </el-button>
      </div>
      
      <div class="filter-group">
        <el-select 
          v-model="filters.chapter_id" 
          placeholder="选择章节" 
          clearable
          class="filter-select"
        >
          <template #prefix><el-icon><Folder /></el-icon></template>
          <el-option label="全部章节" :value="''" />
          <el-option 
            v-for="chapter in chapters" 
            :key="chapter.id" 
            :label="chapter.name" 
            :value="chapter.id" 
          />
        </el-select>
        
        <el-select 
          v-model="filters.priority" 
          placeholder="优先级" 
          clearable
          class="filter-select"
        >
          <template #prefix><el-icon><Star /></el-icon></template>
          <el-option label="全部" :value="''" />
          <el-option label="必须背" value="must" />
          <el-option label="重点背" value="important" />
          <el-option label="尽量背" value="normal" />
        </el-select>
      </div>
      
      <div class="search-box">
        <el-input 
          v-model="filters.keyword" 
          placeholder="搜索知识点..."
          @keyup.enter="loadKnowledgePoints"
          clearable
        >
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <el-button type="primary" @click="loadKnowledgePoints" class="search-btn">
          <el-icon><Search /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- 知识点卡片列表 -->
    <div class="knowledge-cards" v-loading="loading">
      <div 
        v-for="kp in knowledgePoints" 
        :key="kp.id" 
        class="knowledge-card"
        :class="{ 'selected': selectedIds.includes(kp.id) }"
      >
        <div class="card-header">
          <div class="card-meta">
            <el-checkbox 
              :model-value="selectedIds.includes(kp.id)"
              @change="(val) => handleSelect(kp.id, val)"
              class="card-checkbox"
            />
            <span class="card-id">#{{ kp.id }}</span>
            <span :class="['priority-badge', 'priority-' + kp.priority]">
              {{ kp.priority_label }}
            </span>
            <span v-if="kp.chapter_name" class="chapter-badge">
              <el-icon><Folder /></el-icon>
              {{ kp.chapter_name }}
            </span>
          </div>
          <div class="card-actions">
            <el-button size="small" text type="primary" @click="editKnowledgePoint(kp)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button v-if="kp.in_plan" size="small" text type="warning" @click="removeFromPlan(kp)">
              <el-icon><Remove /></el-icon>
              移出规划
            </el-button>
            <el-button v-else size="small" text type="success" @click="addToPlan(kp)">
              <el-icon><Plus /></el-icon>
              加入规划
            </el-button>
            <el-button size="small" text type="danger" @click="deleteKnowledgePoint(kp)">
              <el-icon><Delete /></el-icon>
              删除
            </el-button>
          </div>
        </div>
        
        <div class="card-body">
          <h3 class="question-text">{{ kp.question }}</h3>
          <p v-if="kp.mnemonic" class="mnemonic-text">
            <el-icon><Memo /></el-icon>
            {{ kp.mnemonic }}
          </p>
        </div>
        
        <div class="card-footer">
          <div class="card-stats">
            <span class="stat-item">
              <el-icon><Document /></el-icon>
              {{ kp.items?.length || 0 }} 条答案
            </span>
          </div>
          
          <div class="card-status">
            <span v-if="kp.in_plan" class="status-in-plan">
              <el-icon><Check /></el-icon>
              已加入规划
            </span>
            <span v-else class="status-not-in-plan">
              <el-icon><Clock /></el-icon>
              未加入
            </span>
            
            <span v-if="kp.next_review" :class="['next-review', getReviewClass(kp.next_review)]">
              <el-icon><Clock /></el-icon>
              {{ formatReviewDate(kp.next_review) }}
            </span>
          </div>
        </div>
      </div>
      
      <el-empty v-if="!loading && knowledgePoints.length === 0" description="暂无知识点" />
    </div>

    <!-- 分页 -->
    <div class="pagination-wrapper" v-if="total > 0">
      <el-pagination 
        @size-change="handleSizeChange" 
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        background
      />
    </div>

    <!-- Excel导入对话框 -->
    <el-dialog 
      title="Excel导入知识点" 
      v-model="importDialogVisible" 
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="import-dialog-content">
        <el-alert type="info" :closable="false" class="import-tips">
          <template #title>
            <b>Excel文件格式要求：</b><br>
            - 文件格式：.xlsx 或 .xls<br>
            - 列顺序：优先级 | 章节 | 题目 | 答案 | 速记<br>
            - 答案支持多行：单元格内换行会自动拆分为多条答案
          </template>
        </el-alert>
        
        <el-upload
          ref="uploadRef"
          class="import-upload"
          drag
          :auto-upload="false"
          :limit="1"
          accept=".xlsx,.xls"
          :on-change="handleFileChange"
          :file-list="importFileList"
        >
          <el-icon class="el-icon--upload"><Upload /></el-icon>
          <div class="el-upload__text">
            拖拽文件到此处，或 <em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">支持 .xlsx 和 .xls 格式</div>
          </template>
        </el-upload>
        
        <div v-if="importPreviewData.length > 0" class="import-preview">
          <div class="preview-header">
            <span>预览（共 {{ importPreviewData.length }} 条）</span>
            <el-button type="text" @click="importPreviewData = []">清除预览</el-button>
          </div>
          <div class="preview-list">
            <div v-for="(item, index) in importPreviewData" :key="index" class="preview-item">
              <div class="preview-title">{{ index + 1 }}. {{ item.question.substring(0, 50) }}{{ item.question.length > 50 ? '...' : '' }}</div>
              <div class="preview-info">
                <el-tag size="small" type="item.priority === 'must' ? 'danger' : item.priority === 'important' ? 'warning' : 'info'">
                  {{ item.priority === 'must' ? '必须背' : item.priority === 'important' ? '重点背' : '尽量背' }}
                </el-tag>
                <el-tag size="small" v-if="item.chapter_name">{{ item.chapter_name }}</el-tag>
                <span class="preview-answers">{{ item.items.length }} 条答案</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="importing" :disabled="importPreviewData.length === 0" @click="handleImport">
          导入 {{ importPreviewData.length }} 条
        </el-button>
      </template>
    </el-dialog>

    <!-- 添加/编辑对话框 -->
    <el-dialog 
      :title="isEdit ? '编辑知识点' : '添加知识点'" 
      v-model="dialogVisible" 
      width="900px"
      class="knowledge-dialog"
      :close-on-click-modal="false"
    >
      <div class="dialog-content">
        <!-- 左侧：基本信息 -->
        <div class="form-section basic-info">
          <div class="section-title">
            <el-icon><InfoFilled /></el-icon>
            基本信息
          </div>
          
          <el-form :model="form" label-position="top">
            <el-form-item label="问题">
              <el-input 
                type="textarea" 
                v-model="form.question" 
                :rows="3" 
                placeholder="输入问题内容，支持格式：**加粗**、__下划线__、==高亮=="
              />
            </el-form-item>
            
            <el-form-item label="速记口诀">
              <el-input 
                v-model="form.mnemonic" 
                placeholder="如：战甲主机认智障"
              >
                <template #prefix><el-icon><Memo /></el-icon></template>
              </el-input>
            </el-form-item>
            
            <div class="form-row">
              <el-form-item label="优先级" class="half-width">
                <el-select v-model="form.priority" class="full-width">
                  <el-option label="必须背" value="must">
                    <span class="priority-option must">● 必须背</span>
                  </el-option>
                  <el-option label="重点背" value="important">
                    <span class="priority-option important">● 重点背</span>
                  </el-option>
                  <el-option label="尽量背" value="normal">
                    <span class="priority-option normal">● 尽量背</span>
                  </el-option>
                </el-select>
              </el-form-item>
              
              <el-form-item label="章节" class="half-width">
                <el-select v-model="form.chapter_id" placeholder="选择章节" class="full-width">
                  <template #prefix><el-icon><Folder /></el-icon></template>
                  <el-option label="未分配章节" :value="''" />
                  <el-option 
                    v-for="chapter in chapters" 
                    :key="chapter.id" 
                    :label="chapter.name" 
                    :value="chapter.id" 
                  />
                </el-select>
              </el-form-item>
            </div>
          </el-form>
        </div>
        
        <!-- 右侧：答案内容 -->
        <div class="form-section answers-section">
          <div class="section-title">
            <el-icon><List /></el-icon>
            答案内容
            <span class="answer-count">{{ form.items.length }} 条</span>
          </div>
          
          <el-radio-group v-model="answerInputMode" size="small" class="input-mode-tabs">
            <el-radio-button value="single">
              <el-icon><Edit /></el-icon>
              单条输入
            </el-radio-button>
            <el-radio-button value="batch">
              <el-icon><DocumentCopy /></el-icon>
              批量输入
            </el-radio-button>
          </el-radio-group>
          
          <el-button size="small" type="primary" @click="insertBlankTag" class="blank-btn">
            <el-icon><EditPen /></el-icon>
            选中文字挖空
          </el-button>
          
          <!-- 批量输入模式 -->
          <div v-if="answerInputMode === 'batch'" class="batch-input">
            <el-input 
              type="textarea" 
              v-model="batchAnswerInput" 
              :rows="8"
              placeholder="输入答案内容，每行作为一条答案

支持挖空格式：用 [[关键词]] 包裹需要挖空的内容
例如：这是一个[[重要]]的内容"
            />
            <el-button type="primary" @click="parseBatchAnswer" class="parse-btn">
              <el-icon><ArrowRight /></el-icon>
              解析并添加
            </el-button>
          </div>
          
          <!-- 单条输入模式 -->
          <div v-else class="single-input">
            <div 
              v-for="(item, index) in form.items" 
              :key="index" 
              class="answer-item"
            >
              <div class="answer-item-header">
                <span class="answer-number">{{ index + 1 }}</span>
                <el-button 
                  size="small" 
                  text 
                  type="primary" 
                  @click="openRelationDialog(index)"
                  v-if="item.id"
                >
                  <el-icon><Link /></el-icon>
                  关联知识点
                </el-button>
                <el-button 
                  size="small" 
                  text 
                  type="danger" 
                  @click="removeItem(index)" 
                  v-if="form.items.length > 1"
                >
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
              
              <el-input 
                type="textarea" 
                v-model="item.content" 
                :rows="2"
                placeholder="输入答案内容，选中文字后点击「选中文字挖空」按钮添加挖空标记"
                @focus="handleTextareaFocus(index)"
              />
              
              <!-- 预览 -->
              <div class="answer-preview" v-if="item.content">
                <span class="preview-label">预览：</span>
                <span class="preview-content" v-html="previewWithBlanks(item.content)"></span>
              </div>
              
              <!-- 已关联的知识点 -->
              <div class="answer-relations" v-if="item.relations && item.relations.length > 0">
                <span class="relations-label">已关联：</span>
                <div class="relation-tags">
                  <el-tag 
                    v-for="rel in item.relations" 
                    :key="rel.id" 
                    size="small" 
                    closable 
                    type="success"
                    @close="removeRelation(index, rel.id)"
                  >
                    {{ rel.question }}
                  </el-tag>
                </div>
              </div>
            </div>
            
            <el-button type="dashed" @click="addItem" class="add-item-btn">
              <el-icon><Plus /></el-icon>
              添加答案条目
            </el-button>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveKnowledgePoint">
            <el-icon><Check /></el-icon>
            保存
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 关联知识点选择对话框 -->
    <el-dialog v-model="relationDialogVisible" title="选择关联知识点" width="600px">
      <div class="relation-search">
        <el-input 
          v-model="relationSearch" 
          placeholder="搜索知识点..."
          @keyup.enter="searchKnowledgePoints"
          clearable
        >
          <template #prefix><el-icon><Search /></el-icon></template>
          <template #append>
            <el-button @click="searchKnowledgePoints">搜索</el-button>
          </template>
        </el-input>
      </div>
      <el-table :data="relationList" border style="width: 100%; margin-top: 15px;" max-height="300">
        <el-table-column prop="question" label="问题" min-width="200">
          <template #default="{ row }">
            <div class="relation-question">{{ row.question }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="chapter_name" label="章节" width="120" />
        <el-table-column label="操作" width="80">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="addRelationToItem(row)">
              <el-icon><Plus /></el-icon>
              关联
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { 
  Plus, Search, Calendar, EditPen, Minus, Link, Remove,
  Document, Folder, Star, Edit, Delete, VideoPlay,
  Memo, Check, Clock, InfoFilled, List, DocumentCopy, ArrowRight,
  Upload
} from '@element-plus/icons-vue'
import * as XLSX from 'xlsx'

const knowledgePoints = ref([])
const chapters = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const answerInputMode = ref('single')
const batchAnswerInput = ref('')
const relationDialogVisible = ref(false)
const relationSearch = ref('')
const relationList = ref([])
const currentRelationItemIndex = ref(null)
const editingId = ref(null)

// 批量选择相关
const selectedIds = ref([])
const selectAll = ref(false)
const isIndeterminate = ref(false)

// Excel导入相关
const importDialogVisible = ref(false)
const importFileList = ref([])
const importPreviewData = ref([])
const importing = ref(false)
const uploadRef = ref(null)

const filters = reactive({
  chapter_id: '',
  priority: '',
  keyword: ''
})

const form = reactive({
  question: '',
  priority: 'normal',
  mnemonic: '',
  chapter_id: '',
  items: [{ content: '' }]
})

const loadChapters = async () => {
  const res = await axios.get('/api/chapters')
  chapters.value = res.data.data || []
}

// 显示导入对话框
const showImportDialog = () => {
  importDialogVisible.value = true
  importFileList.value = []
  importPreviewData.value = []
}

// 处理文件变化
const handleFileChange = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const data = new Uint8Array(e.target.result)
      const workbook = XLSX.read(data, { type: 'array', cellDates: true })
      const sheetName = workbook.SheetNames[0]
      const worksheet = workbook.Sheets[sheetName]
      const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' })
      
      // 解析数据（跳过表头）
      const parsedData = []
      for (let i = 1; i < jsonData.length; i++) {
        const row = jsonData[i]
        if (!row[2] || !row[3]) continue  // 跳过没有题目或答案的行
        
        const priorityMap = { '必须背': 'must', '重点背': 'important', '尽量背': 'normal', '': 'normal' }
        const priority = priorityMap[row[0]] || 'normal'
        
        // 章节名称转ID
        const chapterName = row[1] || ''
        const chapter = chapters.value.find(c => c.name === chapterName)
        const chapterId = chapter ? chapter.id : null
        
        // 答案按换行拆分
        const answerText = String(row[3] || '')
        const answerLines = answerText.split('\n').filter(line => line.trim())
        const items = answerLines.map(line => ({ content: line.trim() }))
        
        parsedData.push({
          question: String(row[2] || '').trim(),
          priority: priority,
          mnemonic: String(row[4] || '').trim(),
          chapter_id: chapterId,
          chapter_name: chapterName,
          items: items
        })
      }
      
      importPreviewData.value = parsedData
    } catch (error) {
      console.error('解析Excel文件失败:', error)
      alert('解析Excel文件失败，请检查文件格式是否正确')
    }
  }
  reader.readAsArrayBuffer(file.raw)
}

// 执行导入
const handleImport = async () => {
  if (importPreviewData.value.length === 0) return
  
  importing.value = true
  let successCount = 0
  let failCount = 0
  
  try {
    for (const item of importPreviewData.value) {
      try {
        const data = {
          question: item.question,
          priority: item.priority,
          mnemonic: item.mnemonic,
          chapter_id: item.chapter_id,
          items: item.items.map(i => ({ content: i.content }))
        }
        await axios.post('/api/knowledge-points', data)
        successCount++
      } catch (e) {
        console.error('导入失败:', item.question, e)
        failCount++
      }
    }
    
    alert(`导入完成：成功 ${successCount} 条${failCount > 0 ? `，失败 ${failCount} 条` : ''}`)
    
    if (successCount > 0) {
      importDialogVisible.value = false
      loadKnowledgePoints()
    }
  } finally {
    importing.value = false
  }
}

const loadKnowledgePoints = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.set('page', currentPage.value)
    params.set('per_page', pageSize.value)
    if (filters.chapter_id) params.set('chapter_id', filters.chapter_id)
    if (filters.priority) params.set('priority', filters.priority)
    if (filters.keyword) params.set('keyword', filters.keyword)

    const res = await axios.get(`/api/knowledge-points?${params}`)
    knowledgePoints.value = res.data.data || []
    total.value = res.data.total || 0
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (val) => {
  pageSize.value = val
  loadKnowledgePoints()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  loadKnowledgePoints()
}

const createKnowledgePoint = () => {
  isEdit.value = false
  form.question = ''
  form.priority = 'normal'
  form.mnemonic = ''
  form.chapter_id = ''
  form.items = [{ content: '' }]
  batchAnswerInput.value = ''
  answerInputMode.value = 'single'
  dialogVisible.value = true
}

const parseBatchAnswer = () => {
  if (!batchAnswerInput.value.trim()) return
  
  const lines = batchAnswerInput.value.split('\n').filter(line => line.trim())
  form.items = lines.map(line => ({ content: line.trim() }))
  answerInputMode.value = 'single'
}

const previewWithBlanks = (content) => {
  if (!content) return ''
  return content.replace(/\[\[(.*?)\]\]/g, '<span class="blank-highlight">$1</span>')
}

const editKnowledgePoint = async (row) => {
  isEdit.value = true
  editingId.value = row.id
  form.question = row.question
  form.priority = row.priority
  form.mnemonic = row.mnemonic
  form.chapter_id = row.chapter_id || ''
  form.items = row.items ? row.items.map(item => ({ 
    id: item.id,
    content: item.content,
    relations: []
  })) : [{ content: '', relations: [] }]
  
  for (let i = 0; i < form.items.length; i++) {
    if (form.items[i].id) {
      try {
        const res = await axios.get(`/api/knowledge-point-items/${form.items[i].id}/relations`)
        form.items[i].relations = res.data.data || []
      } catch (e) {
        console.error('加载关联信息失败', e)
      }
    }
  }
  
  dialogVisible.value = true
}

const addItem = () => {
  form.items.push({ content: '', relations: [] })
}

const removeItem = (index) => {
  form.items.splice(index, 1)
}

// 保存当前聚焦的textarea索引
const activeTextareaIndex = ref(null)

// 当textarea获得焦点时记录索引
const handleTextareaFocus = (index) => {
  activeTextareaIndex.value = index
}

// 插入挖空标记到选中的文字
const insertBlankTag = () => {
  // 使用 window.getSelection() 获取选中的文字
  const selection = window.getSelection()
  
  if (!selection || selection.rangeCount === 0) {
    alert('请先点击答案输入框并选中要挖空的文字')
    return
  }
  
  const selectedText = selection.toString()
  
  if (!selectedText) {
    alert('请先选中要挖空的文字')
    return
  }
  
  // 检查是否有记录的活动textarea索引
  if (activeTextareaIndex.value === null) {
    alert('请先点击答案输入框并选中要挖空的文字')
    return
  }
  
  const index = activeTextareaIndex.value
  const content = form.items[index].content
  
  // 查找选中文字在内容中的位置
  const startIndex = content.indexOf(selectedText)
  
  if (startIndex === -1) {
    alert('未找到选中的文字，请重新选择')
    return
  }
  
  const endIndex = startIndex + selectedText.length
  
  // 在选中的文字前后添加挖空标记
  const newValue = content.substring(0, startIndex) + 
                   '[[' + selectedText + ']]' + 
                   content.substring(endIndex)
  
  form.items[index].content = newValue
  
  // 清除选中状态
  selection.removeAllRanges()
}

const openRelationDialog = async (itemIndex) => {
  currentRelationItemIndex.value = itemIndex
  relationSearch.value = ''
  await searchKnowledgePoints()
  relationDialogVisible.value = true
}

const searchKnowledgePoints = async () => {
  try {
    const res = await axios.get('/api/knowledge-points', {
      params: {
        keyword: relationSearch.value,
        page: 1,
        per_page: 50
      }
    })
    if (editingId.value) {
      relationList.value = (res.data.data || []).filter(kp => kp.id !== editingId.value)
    } else {
      relationList.value = res.data.data || []
    }
  } catch (e) {
    console.error('搜索知识点失败', e)
    relationList.value = []
  }
}

const addRelationToItem = (kp) => {
  if (currentRelationItemIndex.value === null) return
  
  const item = form.items[currentRelationItemIndex.value]
  if (!item.relations) {
    item.relations = []
  }
  
  if (item.relations.some(r => r.id === kp.id)) {
    alert('该知识点已关联')
    return
  }
  
  item.relations.push({
    id: kp.id,
    question: kp.question
  })
}

const removeRelation = (itemIndex, relationId) => {
  const item = form.items[itemIndex]
  if (item.relations) {
    item.relations = item.relations.filter(r => r.id !== relationId)
  }
}

const saveKnowledgePoint = async () => {
  if (!form.question.trim()) {
    alert('请输入问题')
    return
  }
  
  const hasContent = form.items.some(item => item.content.trim())
  if (!hasContent) {
    alert('请输入至少一条答案内容')
    return
  }
  
  try {
    const data = {
      question: form.question,
      priority: form.priority,
      mnemonic: form.mnemonic,
      chapter_id: form.chapter_id || null,
      items: form.items.filter(item => item.content.trim()).map(item => ({ 
        id: item.id,
        content: item.content,
        relations: item.relations ? item.relations.map(r => r.id) : []
      }))
    }
    
    if (isEdit.value) {
      await axios.put(`/api/knowledge-points/${editingId.value}`, data)
    } else {
      await axios.post('/api/knowledge-points', data)
    }
    
    dialogVisible.value = false
    loadKnowledgePoints()
  } catch (e) {
    console.error('保存失败', e)
    alert('保存失败')
  }
}

const removeFromPlan = async (row) => {
  if (!confirm(`确定将知识点"${row.question}"移出记忆规划吗？`)) return
  
  try {
    await axios.delete(`/api/memory-record/${row.id}?user_id=default_user`)
    alert('已移出记忆规划')
    loadKnowledgePoints()  // 重新加载列表，更新状态
  } catch (e) {
    console.error('移出规划失败', e)
    alert('移出规划失败')
  }
}

const addToPlan = async (row) => {
  try {
    await axios.post('/api/memory-records?user_id=default_user', {
      kp_ids: [row.id]
    })
    alert('已加入记忆规划')
    loadKnowledgePoints()  // 重新加载列表，更新状态
  } catch (e) {
    console.error('加入规划失败', e)
    alert('加入规划失败')
  }
}

const deleteKnowledgePoint = async (row) => {
  if (!confirm(`确定删除知识点"${row.question}"吗？`)) return
  
  try {
    await axios.delete(`/api/knowledge-points/${row.id}`)
    loadKnowledgePoints()
  } catch (e) {
    console.error('删除失败', e)
    alert('删除失败')
  }
}

// 批量删除
const batchDelete = async () => {
  if (selectedIds.value.length === 0) return
  
  if (!confirm(`确定删除选中的 ${selectedIds.value.length} 个知识点吗？`)) return
  
  try {
    await axios.delete('/api/knowledge-points/batch', {
      data: { ids: selectedIds.value }
    })
    alert('批量删除成功')
    selectedIds.value = []
    selectAll.value = false
    isIndeterminate.value = false
    loadKnowledgePoints()
  } catch (e) {
    console.error('批量删除失败', e)
    alert('批量删除失败')
  }
}

// 处理单个选择
const handleSelect = (id, checked) => {
  if (checked) {
    selectedIds.value.push(id)
  } else {
    const index = selectedIds.value.indexOf(id)
    if (index > -1) {
      selectedIds.value.splice(index, 1)
    }
  }
  updateSelectAllState()
}

// 处理全选
const handleSelectAll = (checked) => {
  if (checked) {
    selectedIds.value = knowledgePoints.value.map(kp => kp.id)
  } else {
    selectedIds.value = []
  }
  updateSelectAllState()
}

// 更新全选状态
const updateSelectAllState = () => {
  const totalCount = knowledgePoints.value.length
  const selectedCount = selectedIds.value.length
  
  if (selectedCount === 0) {
    selectAll.value = false
    isIndeterminate.value = false
  } else if (selectedCount === totalCount) {
    selectAll.value = true
    isIndeterminate.value = false
  } else {
    selectAll.value = false
    isIndeterminate.value = true
  }
}

const practiceKnowledgePoint = (row) => {
  window.location.href = `/memory/practice?kp_ids=${row.id}`
}

const goToMemoryPlan = () => {
  window.location.href = '/memory/plan'
}

const goToDictation = () => {
  window.location.href = '/memory/dictation'
}

// 格式化复习日期
const formatReviewDate = (dateStr) => {
  if (!dateStr) return '-'
  
  // 处理多种日期格式
  let date
  if (typeof dateStr === 'string') {
    // 如果是ISO格式字符串（如 "2024-06-09"），直接使用
    if (dateStr.includes('T')) {
      date = new Date(dateStr)
    } else if (dateStr.includes('-')) {
      // 处理 "2024-06-09" 格式
      const parts = dateStr.split('-')
      date = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]))
    } else {
      date = new Date(dateStr)
    }
  } else {
    date = new Date(dateStr)
  }
  
  // 验证日期是否有效
  if (isNaN(date.getTime())) {
    return '-'
  }
  
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  
  const reviewDate = new Date(date)
  reviewDate.setHours(0, 0, 0, 0)
  
  if (reviewDate.getTime() === today.getTime()) {
    return '今天'
  } else if (reviewDate.getTime() === tomorrow.getTime()) {
    return '明天'
  } else if (reviewDate.getTime() < today.getTime()) {
    return '已逾期'
  } else {
    // 显示 "月/日" 格式
    return `${reviewDate.getMonth() + 1}/${reviewDate.getDate()}`
  }
}

// 根据复习日期获取样式类
const getReviewClass = (dateStr) => {
  if (!dateStr) return ''
  
  // 处理多种日期格式
  let date
  if (typeof dateStr === 'string') {
    if (dateStr.includes('T')) {
      date = new Date(dateStr)
    } else if (dateStr.includes('-')) {
      const parts = dateStr.split('-')
      date = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]))
    } else {
      date = new Date(dateStr)
    }
  } else {
    date = new Date(dateStr)
  }
  
  // 验证日期是否有效
  if (isNaN(date.getTime())) {
    return 'review-future'
  }
  
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  
  const reviewDate = new Date(date)
  reviewDate.setHours(0, 0, 0, 0)
  
  if (reviewDate.getTime() < today.getTime()) {
    return 'review-overdue'
  } else if (reviewDate.getTime() === today.getTime()) {
    return 'review-today'
  } else {
    return 'review-future'
  }
}

onMounted(() => {
  loadChapters()
  loadKnowledgePoints()
})
</script>

<style scoped>
/* 页面容器 */
.knowledge-points-view {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--el-border-color-lighter, #ebeef5);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--el-text-color-primary, #303133);
}

.page-title .el-icon {
  color: var(--el-color-primary, #409eff);
}

.total-badge {
  padding: 6px 14px;
  background: var(--el-fill-color-light, #f5f7fa);
  border-radius: 20px;
  font-size: 13px;
  color: var(--el-text-color-secondary, #909399);
}

.header-actions {
  display: flex;
  gap: 10px;
}

/* 筛选区 */
.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px 20px;
  background: var(--el-fill-color-lighter, #fafafa);
  border-radius: 12px;
}

.filter-group {
  display: flex;
  gap: 12px;
  align-items: center;
}

.select-all-checkbox {
  font-weight: 500;
  color: var(--el-text-color-primary, #303133);
}

.batch-delete-btn {
  margin-left: 8px;
}

.filter-select {
  width: 160px;
}

.search-box {
  display: flex;
  gap: 8px;
}

.search-box .el-input {
  width: 280px;
}

.search-btn {
  flex-shrink: 0;
}

/* 知识点卡片 */
.knowledge-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.knowledge-card {
  background: var(--el-bg-color, #ffffff);
  border: 1px solid var(--el-border-color-lighter, #ebeef5);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.knowledge-card.selected {
  border-color: var(--el-color-primary, #409eff);
  box-shadow: 0 0 0 2px var(--el-color-primary-light-8, #ecf5ff);
}

.knowledge-card:hover {
  border-color: var(--el-color-primary-light-5, #a0cfff);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 14px 16px;
  background: var(--el-fill-color-light, #f5f7fa);
  border-bottom: 1px solid var(--el-border-color-lighter, #ebeef5);
  gap: 12px;
}

.card-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.card-checkbox {
  margin-right: 4px;
}

.card-id {
  font-size: 13px;
  color: var(--el-text-color-secondary, #909399);
  font-weight: 500;
  flex-shrink: 0;
}

.priority-badge {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.priority-badge.priority-must {
  background: #fef0f0;
  color: #ff4d4f;
}

.priority-badge.priority-important {
  background: #fffbe6;
  color: #faad14;
}

.priority-badge.priority-normal {
  background: #f6ffed;
  color: #52c41a;
}

.chapter-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  background: var(--el-fill-color, #f4f4f5);
  border-radius: 12px;
  font-size: 12px;
  color: var(--el-text-color-secondary, #909399);
  flex-shrink: 0;
  max-width: 100%;
  overflow: hidden;
}

.chapter-badge .el-icon {
  flex-shrink: 0;
}

.chapter-badge span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-actions {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
}

.card-body {
  padding: 16px;
}

.question-text {
  margin: 0 0 10px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary, #303133);
  line-height: 1.5;
}

.mnemonic-text {
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0;
  padding: 8px 12px;
  background: var(--el-fill-color-light, #f5f7fa);
  border-radius: 8px;
  font-size: 13px;
  color: var(--el-text-color-secondary, #909399);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-top: 1px solid var(--el-border-color-lighter, #ebeef5);
}

.card-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 13px;
  color: var(--el-text-color-secondary, #909399);
}

.card-status {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-in-plan,
.status-not-in-plan {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.status-in-plan {
  color: var(--el-color-success, #67c23a);
}

.status-not-in-plan {
  color: var(--el-text-color-secondary, #909399);
}

.next-review {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 10px;
}

.review-overdue {
  background: #fef0f0;
  color: #ff4d4f;
}

.review-today {
  background: #fffbe6;
  color: #faad14;
}

.review-future {
  background: #ecf5ff;
  color: #409eff;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

/* 对话框样式 */
.dialog-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.form-section {
  padding: 20px;
  background: var(--el-fill-color-lighter, #fafafa);
  border-radius: 12px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  padding-bottom: 12px;
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary, #303133);
  border-bottom: 2px solid var(--el-color-primary, #409eff);
}

.section-title .el-icon {
  color: var(--el-color-primary, #409eff);
}

.answer-count {
  margin-left: auto;
  padding: 2px 10px;
  background: var(--el-color-primary, #409eff);
  color: white;
  border-radius: 10px;
  font-size: 12px;
  font-weight: normal;
}

.form-row {
  display: flex;
  gap: 16px;
}

.half-width {
  flex: 1;
}

.full-width {
  width: 100%;
}

.priority-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.priority-option.must {
  color: #ff4d4f;
}

.priority-option.important {
  color: #faad14;
}

.priority-option.normal {
  color: #52c41a;
}

/* 答案输入区 */
.input-mode-tabs {
  margin-bottom: 16px;
}

.blank-btn {
  margin-left: 12px;
  margin-bottom: 16px;
}

.batch-input {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.parse-btn {
  align-self: flex-end;
}

.single-input {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.answer-item {
  padding: 14px;
  background: white;
  border: 1px solid var(--el-border-color-lighter, #ebeef5);
  border-radius: 8px;
}

.answer-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.answer-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background: var(--el-color-primary, #409eff);
  color: white;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
}

.answer-preview {
  margin-top: 10px;
  padding: 8px 12px;
  background: var(--el-fill-color-light, #f5f7fa);
  border-radius: 6px;
  font-size: 13px;
}

.preview-label {
  color: var(--el-text-color-secondary, #909399);
  margin-right: 8px;
}

:deep(.blank-highlight) {
  background: var(--el-color-warning, #e6a23c);
  color: white;
  padding: 1px 6px;
  border-radius: 4px;
  font-weight: 500;
}

.answer-relations {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed var(--el-border-color-lighter, #ebeef5);
}

.relations-label {
  display: block;
  font-size: 12px;
  color: var(--el-text-color-secondary, #909399);
  margin-bottom: 8px;
}

.relation-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.add-item-btn {
  margin-top: 8px;
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 关联对话框 */
.relation-search {
  margin-bottom: 0;
}

.relation-question {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 空状态 */
:deep(.el-empty) {
  padding: 40px 0;
}

/* 响应式 */
@media (max-width: 1024px) {
  .knowledge-cards {
    grid-template-columns: 1fr;
  }
  
  .dialog-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    flex-wrap: wrap;
  }
  
  .filter-section {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .filter-group {
    flex-wrap: wrap;
  }
  
  .search-box {
    width: 100%;
  }
  
  .search-box .el-input {
    width: 100%;
  }
}

/* Excel导入对话框样式 */
.import-dialog-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.import-tips {
  line-height: 1.8;
}

.import-upload {
  width: 100%;
}

.import-upload .el-upload-dragger {
  padding: 40px 20px;
}

.import-preview {
  border: 1px solid var(--el-border-color-lighter, #ebeef5);
  border-radius: 8px;
  overflow: hidden;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--el-fill-color-light, #f5f7fa);
  border-bottom: 1px solid var(--el-border-color-lighter, #ebeef5);
  font-weight: 500;
}

.preview-list {
  max-height: 300px;
  overflow-y: auto;
}

.preview-item {
  padding: 12px 16px;
  border-bottom: 1px solid var(--el-border-color-lighter, #ebeef5);
}

.preview-item:last-child {
  border-bottom: none;
}

.preview-title {
  font-size: 14px;
  color: var(--el-text-color-primary, #303133);
  margin-bottom: 8px;
}

.preview-info {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.preview-answers {
  font-size: 12px;
  color: var(--el-text-color-secondary, #909399);
}
</style>
