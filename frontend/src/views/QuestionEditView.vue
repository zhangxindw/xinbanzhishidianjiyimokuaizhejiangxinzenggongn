<template>
  <div class="question-edit-view">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑题目' : '新建题目' }}</h2>
    </div>

    <div class="card">
      <div class="form-row">
        <div class="form-group">
          <label>题型</label>
          <el-select v-model="form.question_type_id" placeholder="选择题型" style="width: 100%;">
            <el-option v-for="qt in questionTypes" :key="qt.id" :label="qt.name" :value="qt.id" />
          </el-select>
        </div>
        <div class="form-group">
          <label>章节</label>
          <el-select v-model="form.chapter_id" placeholder="选择章节" style="width: 100%;">
            <el-option v-for="ch in chapters" :key="ch.id" :label="ch.name" :value="ch.id" />
          </el-select>
        </div>
        <div class="form-group">
          <label>难度</label>
          <el-rate v-model="form.difficulty" :max="3" show-text :texts="['简单', '中等', '困难']" />
        </div>
        <div class="form-group">
          <label>状态</label>
          <el-select v-model="form.status" style="width: 100%;">
            <el-option label="已发布" value="published" />
            <el-option label="草稿" value="draft" />
            <el-option label="隐藏" value="hidden" />
          </el-select>
        </div>
      </div>

      <div class="form-group">
        <label>题干</label>
        <div class="editor-toolbar">
          <el-button size="small" @click="formatStem('bold')"><b>B</b></el-button>
          <el-button size="small" @click="formatStem('italic')"><i>I</i></el-button>
          <el-button size="small" @click="formatStem('underline')"><u>U</u></el-button>
          <el-button size="small" @click="formatStem('highlight-yellow')">高亮黄</el-button>
          <el-button size="small" @click="formatStem('highlight-green')">高亮绿</el-button>
          <el-button size="small" @click="formatStem('highlight-blue')">高亮蓝</el-button>
          <el-color-picker v-model="textColor" size="small" @change="(c) => formatStem('color', c)" />
          <el-button size="small" @click="insertImageToStem">插入图片</el-button>
          <el-button size="small" @click="insertTableToStem">插入表格</el-button>
        </div>
        <div ref="stemEditorRef" class="rich-editor" contenteditable="true" @input="updateStemHtml"></div>
      </div>

      <div class="options-section">
        <h4>选项</h4>
        <div v-for="(label, index) in optionLabels" :key="label" class="option-row">
          <span class="option-label">{{ label }}</span>
          <div class="option-inputs">
            <div class="editor-toolbar">
              <el-button size="small" @click="formatOption(index, 'bold')"><b>B</b></el-button>
              <el-button size="small" @click="formatOption(index, 'italic')"><i>I</i></el-button>
              <el-button size="small" @click="formatOption(index, 'underline')"><u>U</u></el-button>
              <el-button size="small" @click="formatOption(index, 'highlight-yellow')">高亮</el-button>
              <el-button size="small" @click="insertImageToOption(index)">图片</el-button>
            </div>
            <div :ref="el => optionEditorRefs[index] = el" class="rich-editor" contenteditable="true" @input="updateOptionHtml(index)"></div>
          </div>
        </div>
      </div>

      <div class="form-group">
        <label>答案</label>
        <el-select v-model="form.answer" multiple placeholder="选择答案" style="width: 100%;">
          <el-option label="A" value="A" />
          <el-option label="B" value="B" />
          <el-option label="C" value="C" />
          <el-option label="D" value="D" />
          <el-option label="E" value="E" />
          <el-option label="F" value="F" />
        </el-select>
      </div>

      <div class="form-group">
        <label>解析</label>
        <div class="editor-toolbar">
          <el-button size="small" @click="formatExplanation('bold')"><b>B</b></el-button>
          <el-button size="small" @click="formatExplanation('italic')"><i>I</i></el-button>
          <el-button size="small" @click="formatExplanation('underline')"><u>U</u></el-button>
          <el-button size="small" @click="formatExplanation('highlight-yellow')">高亮黄</el-button>
          <el-button size="small" @click="formatExplanation('highlight-green')">高亮绿</el-button>
          <el-button size="small" @click="formatExplanation('highlight-blue')">高亮蓝</el-button>
          <el-button size="small" @click="insertImageToExplanation">插入图片</el-button>
        </div>
        <div ref="explanationEditorRef" class="rich-editor" contenteditable="true" @input="updateExplanationHtml"></div>
      </div>

      <div style="margin-top: 20px; text-align: center;">
        <el-button @click="$router.back()">取消</el-button>
        <el-button type="primary" @click="saveQuestion">保存</el-button>
      </div>
    </div>

    <el-dialog v-model="showImageDialog" title="插入图片" width="400px">
      <el-input v-model="imageUrl" placeholder="请输入图片URL" />
      <template #footer>
        <el-button @click="showImageDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmInsertImage">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuizStore } from '@/store/quiz'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useQuizStore()

const isEdit = computed(() => !!route.params.id)
const questionTypes = ref([])
const chapters = ref([])
const optionLabels = ['A', 'B', 'C', 'D', 'E', 'F']
const optionEditorRefs = ref([])
const stemEditorRef = ref(null)
const explanationEditorRef = ref(null)
const textColor = ref('#000000')

const form = reactive({
  question_type_id: null,
  chapter_id: null,
  difficulty: 1,
  status: 'published',
  answer: [],
  stem: '',
  stem_html: '',
  option_a: '', option_b: '', option_c: '', option_d: '', option_e: '', option_f: '',
  option_a_html: '', option_b_html: '', option_c_html: '', option_d_html: '', option_e_html: '', option_f_html: '',
  explanation: '',
  explanation_html: ''
})

const showImageDialog = ref(false)
const imageUrl = ref('')
const currentInsertTarget = ref('')
const currentInsertIndex = ref(-1)

const loadQuestion = async (id) => {
  try {
    const res = await axios.get(`/api/questions/${id}`)
    const q = res.data.data
    Object.assign(form, {
      question_type_id: q.question_type_id,
      chapter_id: q.chapter_id,
      difficulty: q.difficulty,
      status: q.status,
      answer: q.answer.split(''),
      stem: q.stem,
      stem_html: q.stem_html || '',
      option_a: q.option_a,
      option_b: q.option_b,
      option_c: q.option_c,
      option_d: q.option_d,
      option_e: q.option_e,
      option_f: q.option_f,
      option_a_html: q.option_a_html || '',
      option_b_html: q.option_b_html || '',
      option_c_html: q.option_c_html || '',
      option_d_html: q.option_d_html || '',
      option_e_html: q.option_e_html || '',
      option_f_html: q.option_f_html || '',
      explanation: q.explanation || '',
      explanation_html: q.explanation_html || ''
    })

    await nextTick()
    if (stemEditorRef.value) {
      stemEditorRef.value.innerHTML = form.stem_html || form.stem
    }
    if (explanationEditorRef.value) {
      explanationEditorRef.value.innerHTML = form.explanation_html || form.explanation
    }
    const optionKeys = ['option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'option_f']
    const optionHtmlKeys = ['option_a_html', 'option_b_html', 'option_c_html', 'option_d_html', 'option_e_html', 'option_f_html']
    optionKeys.forEach((key, i) => {
      const el = optionEditorRefs.value[i]
      if (el) {
        el.innerHTML = form[optionHtmlKeys[i]] || form[key]
      }
    })
  } catch (error) {
    ElMessage.error('加载题目失败')
  }
}

const updateStemHtml = () => {
  if (stemEditorRef.value) {
    form.stem_html = stemEditorRef.value.innerHTML
    form.stem = stemEditorRef.value.innerText
  }
}

const updateOptionHtml = (index) => {
  const el = optionEditorRefs.value[index]
  if (el) {
    const htmlKey = `option_${String.fromCharCode(97 + index)}_html`
    const textKey = `option_${String.fromCharCode(97 + index)}`
    form[htmlKey] = el.innerHTML
    form[textKey] = el.innerText
  }
}

const updateExplanationHtml = () => {
  if (explanationEditorRef.value) {
    form.explanation_html = explanationEditorRef.value.innerHTML
    form.explanation = explanationEditorRef.value.innerText
  }
}

const formatText = (editor, command, value = null) => {
  if (!editor) return
  editor.focus()
  document.execCommand(command, false, value)
}

const formatStem = (command, value = null) => {
  if (command === 'color') {
    formatText(stemEditorRef.value, 'foreColor', value)
  } else if (command.startsWith('highlight-')) {
    const className = command
    const selection = window.getSelection()
    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0)
      const span = document.createElement('span')
      span.className = className
      range.surroundContents(span)
    }
  } else {
    formatText(stemEditorRef.value, command)
  }
  updateStemHtml()
}

const formatOption = (index, command, value = null) => {
  const el = optionEditorRefs.value[index]
  if (command === 'color') {
    formatText(el, 'foreColor', value)
  } else if (command.startsWith('highlight-')) {
    const selection = window.getSelection()
    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0)
      const span = document.createElement('span')
      span.className = command
      range.surroundContents(span)
    }
  } else {
    formatText(el, command)
  }
  updateOptionHtml(index)
}

const formatExplanation = (command, value = null) => {
  if (command === 'color') {
    formatText(explanationEditorRef.value, 'foreColor', value)
  } else if (command.startsWith('highlight-')) {
    const selection = window.getSelection()
    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0)
      const span = document.createElement('span')
      span.className = command
      range.surroundContents(span)
    }
  } else {
    formatText(explanationEditorRef.value, command)
  }
  updateExplanationHtml()
}

const insertImageToStem = () => {
  currentInsertTarget.value = 'stem'
  showImageDialog.value = true
}

const insertImageToOption = (index) => {
  currentInsertTarget.value = 'option'
  currentInsertIndex.value = index
  showImageDialog.value = true
}

const insertImageToExplanation = () => {
  currentInsertTarget.value = 'explanation'
  showImageDialog.value = true
}

const confirmInsertImage = () => {
  if (!imageUrl.value) return
  let editor
  if (currentInsertTarget.value === 'stem') {
    editor = stemEditorRef.value
    updateStemHtml()
  } else if (currentInsertTarget.value === 'option') {
    editor = optionEditorRefs.value[currentInsertIndex.value]
    updateOptionHtml(currentInsertIndex.value)
  } else if (currentInsertTarget.value === 'explanation') {
    editor = explanationEditorRef.value
    updateExplanationHtml()
  }

  if (editor) {
    const img = document.createElement('img')
    img.src = imageUrl.value
    img.style.maxWidth = '100%'
    editor.appendChild(img)
  }

  showImageDialog.value = false
  imageUrl.value = ''
}

const insertTableToStem = () => {
  const table = document.createElement('table')
  table.border = 1
  table.style.borderCollapse = 'collapse'
  table.style.width = '100%'
  for (let i = 0; i < 3; i++) {
    const row = table.insertRow()
    for (let j = 0; j < 3; j++) {
      const cell = row.insertCell()
      cell.contentEditable = true
      cell.style.border = '1px solid #ddd'
      cell.style.padding = '8px'
      cell.innerHTML = `单元格${i + 1}-${j + 1}`
    }
  }
  stemEditorRef.value.appendChild(table)
  updateStemHtml()
}

const saveQuestion = async () => {
  if (!form.stem && !form.stem_html) {
    ElMessage.warning('请填写题干')
    return
  }
  if (form.answer.length === 0) {
    ElMessage.warning('请选择答案')
    return
  }

  const data = {
    ...form,
    answer: form.answer.join('')
  }

  try {
    if (isEdit.value) {
      await store.updateQuestion(route.params.id, data)
      ElMessage.success('更新成功')
    } else {
      await store.createQuestion(data)
      ElMessage.success('创建成功')
    }
    router.push('/questions')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}



onMounted(async () => {
  questionTypes.value = store.questionTypes
  chapters.value = store.chapters

  if (isEdit.value) {
    await loadQuestion(route.params.id)
  }
})
</script>

<style scoped>
.question-edit-view {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.rich-editor {
  min-height: 100px;
  padding: 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  outline: none;
  line-height: 1.8;
}

.rich-editor:focus {
  border-color: #667eea;
}

.editor-toolbar {
  display: flex;
  gap: 5px;
  margin-bottom: 5px;
  flex-wrap: wrap;
}

.options-section {
  margin: 30px 0;
  padding: 20px;
  background: #f8f8ff;
  border-radius: 8px;
}

.options-section h4 {
  margin-bottom: 15px;
  color: #333;
}

.option-row {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
  align-items: flex-start;
}

.option-label {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #667eea;
  color: white;
  border-radius: 50%;
  font-weight: bold;
  flex-shrink: 0;
}

.option-inputs {
  flex: 1;
}

.option-inputs .rich-editor {
  min-height: 60px;
}
</style>
