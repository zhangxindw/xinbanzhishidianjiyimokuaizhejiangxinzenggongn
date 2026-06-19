<template>
  <div class="distinguish-mgt">
    <div class="page-header">
      <div class="header-left">
        <h2>辨析题管理</h2>
        <p class="header-desc">管理和编辑辨析判断题库</p>
      </div>
      <div class="header-actions">
        <div class="action-stat" v-if="selectedIds.length > 0">
          <span class="stat-badge">{{ selectedIds.length }} 项已选</span>
        </div>
        <el-button type="primary" :disabled="selectedIds.length === 0" @click="addToPlan" class="modern-btn primary-btn">
          <el-icon><Plus /></el-icon>
          添加到规划
        </el-button>
        <el-button type="danger" :disabled="selectedIds.length === 0" @click="batchDelete" class="modern-btn danger-btn">
          <el-icon><Delete /></el-icon>
          批量删除
        </el-button>
      </div>
    </div>

    <div class="filter-bar">
      <div class="filter-item">
        <el-select v-model="filterChapter" placeholder="章节筛选" clearable class="filter-select">
          <el-option label="全部章节" value="" />
          <el-option v-for="chapter in chapters" :key="chapter.id" :label="chapter.name" :value="chapter.id" />
        </el-select>
      </div>
      <div class="filter-item">
        <el-select v-model="filterInPlan" placeholder="规划状态" clearable class="filter-select">
          <el-option label="全部状态" value="" />
          <el-option label="已加入规划" value="true" />
          <el-option label="未加入规划" value="false" />
        </el-select>
      </div>
      <div class="filter-actions">
        <el-button type="primary" @click="loadData" class="filter-btn">
          <el-icon><Search /></el-icon>
          筛选
        </el-button>
        <el-button @click="resetFilters" class="reset-btn">
          <el-icon><RefreshLeft /></el-icon>
          重置
        </el-button>
      </div>
    </div>

    <el-table 
      :data="questions" 
      border 
      stripe 
      @selection-change="onSelectionChange" 
      v-loading="loading"
      class="modern-table"
      :header-cell-style="{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: '#fff', fontWeight: '600' }"
    >
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column prop="chapter_name" label="章节" width="140">
        <template #default="{ row }">
          <span class="chapter-badge">{{ row.chapter_name || '未分类' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="题干" min-width="220">
        <template #default="{ row }">
          <div class="stem-cell" v-html="row.question_stem_html || row.question_stem" />
        </template>
      </el-table-column>
      <el-table-column label="选项" width="320">
        <template #default="{ row }">
          <div class="options-list">
            <div v-for="opt in row.options" :key="opt.id" class="option-item" :class="{ 'is-wrong': !opt.is_correct }">
              <span class="option-key">{{ opt.option_key }}.</span>
              <span class="option-text">{{ opt.option_text }}</span>
              <el-tag :type="opt.is_correct ? 'success' : 'danger'" size="small" effect="light">
                {{ opt.is_correct ? '正确' : '错误' }}
              </el-tag>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="规划状态" width="130" align="center">
        <template #default="{ row }">
          <el-tag :type="isInPlan(row.id) ? 'success' : 'info'" effect="dark" round>
            {{ isInPlan(row.id) ? '✓ 已加入' : '○ 未加入' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160" align="center">
        <template #default="{ row }">
          <div class="action-btns">
            <el-button size="small" @click="editItem(row)" class="edit-btn">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="deleteItem(row.id)" class="delete-btn">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-wrapper" v-if="total > perPage">
      <el-pagination
        v-model:current-page="page"
        :total="total"
        :page-size="perPage"
        layout="prev, pager, next, jumper"
        @current-change="loadData"
        background
      />
    </div>

    <el-dialog 
      v-model="showEditDialog" 
      title="编辑辨析题" 
      width="75%" 
      :close-on-click-modal="false"
      class="modern-dialog"
      destroy-on-close
    >
      <div class="edit-form">
        <el-form :model="editForm" label-width="100px" class="edit-form-inner">
          <el-form-item label="章节" class="form-item">
            <el-input v-model="editForm.chapter_name" placeholder="请输入章节名称" />
          </el-form-item>
          <el-form-item label="题干" class="form-item">
            <el-input v-model="editForm.stem" type="textarea" :rows="3" placeholder="请输入题目题干" />
          </el-form-item>
          <el-form-item label="解析" class="form-item">
            <el-input v-model="editForm.explanation" type="textarea" :rows="3" placeholder="请输入题目解析" />
          </el-form-item>
          <el-form-item label="选项" class="form-item">
            <div class="options-edit-list">
              <div v-for="(opt, idx) in editForm.options" :key="opt.id" class="option-edit-row">
                <el-select v-model="opt.option_key" class="key-select">
                  <el-option label="A" value="A" />
                  <el-option label="B" value="B" />
                  <el-option label="C" value="C" />
                  <el-option label="D" value="D" />
                </el-select>
                <el-input v-model="opt.option_text" placeholder="选项内容" class="text-input" />
                <el-switch v-model="opt.is_correct" active-text="正确" inactive-text="错误" />
                <el-input v-model="opt.corrected_text" placeholder="正确表述（错误选项填写）" class="corrected-input" />
                <el-button type="danger" size="small" @click="editForm.options.splice(idx, 1)" v-if="editForm.options.length > 2" circle>
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
              <el-button type="primary" size="small" @click="addOption" class="add-option-btn">
                <el-icon><Plus /></el-icon>
                添加选项
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showEditDialog = false" class="cancel-btn">取消</el-button>
          <el-button type="primary" @click="saveEdit" class="save-btn">保存修改</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import { ElMessage, ElMessageBox } from "element-plus"
import { Search, RefreshLeft } from "@element-plus/icons-vue"

const questions = ref([])
const loading = ref(false)
const selectedIds = ref([])
const page = ref(1)
const perPage = 20
const total = ref(0)
const planQuestionIds = ref(new Set())
const chapters = ref([])
const filterChapter = ref("")
const filterInPlan = ref("")

const showEditDialog = ref(false)
const editForm = ref({
  id: null,
  chapter_name: "",
  stem: "",
  explanation: "",
  options: []
})

const loadData = async () => {
  loading.value = true
  try {
    let url = `/api/distinguish/questions?page=${page.value}&per_page=${perPage}`
    if (filterChapter.value) {
      url += `&chapter_id=${filterChapter.value}`
    }
    if (filterInPlan.value !== "") {
      url += `&in_plan=${filterInPlan.value}`
    }
    const res = await axios.get(url)
    questions.value = res.data.data || []
    total.value = res.data.total || 0
    await loadPlanStatus()
  } catch (e) { console.error(e) }
  loading.value = false
}

const loadChapters = async () => {
  try {
    const res = await axios.get("/api/chapters")
    chapters.value = res.data.data || []
  } catch (e) { console.error(e) }
}

const resetFilters = () => {
  filterChapter.value = ""
  filterInPlan.value = ""
  page.value = 1
  loadData()
}

const loadPlanStatus = async () => {
  try {
    const res = await axios.get("/api/distinguish/plan/list")
    const planRecords = res.data.data || []
    planQuestionIds.value = new Set()
    for (const record of planRecords) {
      if (record.question_id) {
        planQuestionIds.value.add(record.question_id)
      }
    }
  } catch (e) { console.error(e) }
}

const isInPlan = (questionId) => {
  return planQuestionIds.value.has(questionId)
}

const onSelectionChange = (rows) => {
  selectedIds.value = rows.map(r => r.id).filter(id => !isInPlan(id))
}

const deleteItem = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这道辨析题吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await axios.delete(`/api/distinguish/questions/${id}`)
    ElMessage.success('删除成功')
    await loadData()
  } catch (e) {
    if (e !== 'cancel') {
      console.error(e)
      ElMessage.error('删除失败')
    }
  }
}

const batchDelete = async () => {
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedIds.value.length} 道辨析题吗？`, '确认批量删除', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await axios.delete("/api/distinguish/questions/batch", { data: { ids: selectedIds.value } })
    selectedIds.value = []
    ElMessage.success('批量删除成功')
    await loadData()
  } catch (e) {
    if (e !== 'cancel') {
      console.error(e)
      ElMessage.error('批量删除失败')
    }
  }
}

const addToPlan = async () => {
  const optionIds = []
  for (const q of questions.value) {
    if (selectedIds.value.includes(q.id)) {
      for (const opt of q.options) {
        optionIds.push(opt.id)
      }
    }
  }
  if (optionIds.length === 0) {
    ElMessage.warning('没有可添加的选项')
    return
  }
  try {
    await axios.post("/api/distinguish/plan/add", { option_ids: optionIds })
    ElMessage.success(`已将 ${optionIds.length} 个选项添加到规划`)
    await loadData()
  } catch (e) {
    console.error(e)
    ElMessage.error('添加失败')
  }
}

const editItem = (row) => {
  editForm.value = {
    id: row.id,
    chapter_name: row.chapter_name,
    stem: row.stem || row.question_stem,
    explanation: row.explanation || "",
    options: JSON.parse(JSON.stringify(row.options))
  }
  showEditDialog.value = true
}

const addOption = () => {
  const keys = ["A", "B", "C", "D"]
  const usedKeys = editForm.value.options.map(o => o.option_key)
  const newKey = keys.find(k => !usedKeys.includes(k)) || String.fromCharCode(65 + editForm.value.options.length)
  editForm.value.options.push({
    id: null,
    option_key: newKey,
    option_text: "",
    is_correct: false,
    corrected_text: ""
  })
}

const saveEdit = async () => {
  try {
    await axios.put(`/api/distinguish/questions/${editForm.value.id}`, editForm.value)
    showEditDialog.value = false
    await loadData()
    ElMessage.success('保存成功')
  } catch (e) {
    console.error(e)
    ElMessage.error('保存失败')
  }
}

onMounted(() => {
  loadChapters()
  loadData()
})
</script>

<style scoped>
.distinguish-mgt {
  padding: 28px 32px;
  min-height: calc(100vh - 60px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 28px;
  padding: 24px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  margin-bottom: 20px;
}

.filter-item {
  display: flex;
  align-items: center;
}

.filter-select {
  width: 200px;
}

.filter-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: auto;
}

.filter-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  font-weight: 600;
  border-radius: 8px;
}

.reset-btn {
  border-radius: 8px;
}

.header-left h2 {
  font-size: 26px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 6px 0;
}

.header-desc {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

.action-stat {
  margin-right: 8px;
}

.stat-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.modern-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.3s ease;
  border: none;
}

.primary-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.danger-btn {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(248, 113, 113, 0.3);
}

.danger-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(248, 113, 113, 0.4);
}

.modern-table {
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.modern-table :deep(.el-table__header-wrapper th) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  color: white;
  font-weight: 600;
  font-size: 14px;
  padding: 16px 0;
}

.modern-table :deep(.el-table__row) {
  transition: all 0.2s ease;
}

.modern-table :deep(.el-table__row:hover) {
  background: #f8fafc !important;
  transform: scale(1.01);
}

.chapter-badge {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1d4ed8;
  padding: 5px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
}

.stem-cell {
  max-height: 60px;
  overflow: hidden;
  font-size: 14px;
  line-height: 1.6;
  color: #334155;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border-radius: 8px;
  background: #f8fafc;
  font-size: 13px;
  transition: all 0.2s ease;
}

.option-item:hover {
  background: #f1f5f9;
}

.option-item.is-wrong {
  background: #fef2f2;
  border: 1px solid #fecaca;
}

.option-key {
  font-weight: 700;
  color: #475569;
  min-width: 20px;
}

.option-text {
  flex: 1;
  color: #334155;
}

.action-btns {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.edit-btn {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1d4ed8;
  border: none;
  font-weight: 600;
}

.delete-btn {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #dc2626;
  border: none;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 28px;
}

.pagination-wrapper :deep(.el-pagination) {
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.pagination-wrapper :deep(.el-pagination.is-background .el-pager li) {
  border-radius: 8px;
}

.pagination-wrapper :deep(.el-pagination.is-background .el-pager li.is-active) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.modern-dialog :deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
}

.modern-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 24px;
  margin: 0;
}

.modern-dialog :deep(.el-dialog__title) {
  color: white;
  font-size: 18px;
  font-weight: 700;
}

.modern-dialog :deep(.el-dialog__close) {
  color: white;
}

.edit-form {
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
}

.form-item {
  margin-bottom: 20px;
}

.form-item :deep(.el-form-item__label) {
  font-weight: 600;
  color: #475569;
}

.options-edit-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-edit-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.key-select {
  width: 70px;
}

.text-input {
  flex: 2;
}

.corrected-input {
  flex: 3;
}

.add-option-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  font-weight: 600;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn {
  padding: 10px 24px;
  border-radius: 10px;
}

.save-btn {
  padding: 10px 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
}

.save-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
  }
  
  .header-actions {
    flex-wrap: wrap;
    width: 100%;
  }
  
  .option-edit-row {
    flex-wrap: wrap;
  }
}
</style>
