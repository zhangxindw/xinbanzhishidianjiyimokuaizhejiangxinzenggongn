<template>
  <div class="distinguish-plan">
    <div class="page-header">
      <div class="header-left">
        <h2>辨析规划</h2>
        <p class="header-desc">管理辨析记忆学习计划</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="startPractice" :disabled="todayTasks.length === 0" class="modern-btn primary-btn">
          <el-icon><VideoPlay /></el-icon>
          开始练习 ({{ todayTasks.length }})
        </el-button>
        <el-button type="danger" @click="clearAllConfirm" :disabled="stats.total_records === 0" class="modern-btn danger-btn">
          <el-icon><Delete /></el-icon>
          清除所有
        </el-button>
      </div>
    </div>

    <el-row :gutter="24" class="stats-row">
      <el-col :xs="12" :sm="12" :md="6">
        <div class="stat-card">
          <div class="stat-icon purple">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.total_records }}</div>
            <div class="stat-label">已添加选项</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6">
        <div class="stat-card">
          <div class="stat-icon orange">
            <el-icon><Clock /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.learning_count }}</div>
            <div class="stat-label">初学中</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6">
        <div class="stat-card">
          <div class="stat-icon green">
            <el-icon><VideoPlay /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.reviewing_count }}</div>
            <div class="stat-label">复习中</div>
          </div>
        </div>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6">
        <div class="stat-card">
          <div class="stat-icon red">
            <el-icon><Calendar /></el-icon>
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.today_review_count }}</div>
            <div class="stat-label">今日待复习</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <div class="content-card">
      <div class="card-header">
        <h3>规划列表</h3>
        <span class="record-count" v-if="planRecords.length > 0">{{ planRecords.length }} 条记录</span>
      </div>
      
      <div v-if="planRecords.length > 0" class="records-grid">
        <div v-for="record in planRecords" :key="record.id" class="record-item">
          <div class="record-header">
            <span class="chapter-tag">{{ record.chapter_name || '未分类' }}</span>
            <el-tag :type="record.status === 'learning' ? 'warning' : 'success'" size="small" effect="dark" round>
              {{ record.status === 'learning' ? '初学中' : '复习中' }}
            </el-tag>
          </div>
          
          <div class="record-stem" v-html="record.question_stem"></div>
          
          <div class="record-option">
            <span class="option-label">{{ record.option_key }}.</span>
            <span class="option-text">{{ record.option_text }}</span>
          </div>
          
          <div class="record-footer">
            <div class="review-info">
              <el-icon><Calendar /></el-icon>
              <span :class="{ 'today-highlight': isToday(record.next_review_date) }">
                下次复习: {{ formatDate(record.next_review_date) }}
              </span>
            </div>
            <el-button size="small" type="danger" @click="removeFromPlan(record.id)" class="remove-btn">
              <el-icon><Delete /></el-icon>
              移出
            </el-button>
          </div>
        </div>
      </div>
      
      <el-empty v-else description="暂无规划记录" class="empty-state">
        <el-button type="primary" @click="goToManagement">
          <el-icon><Plus /></el-icon>
          添加辨析题
        </el-button>
      </el-empty>
    </div>

    <el-dialog 
      v-model="showClearConfirm" 
      title="确认清除所有规划" 
      width="450px" 
      :close-on-click-modal="false"
      class="modern-dialog"
    >
      <div class="confirm-content">
        <div class="warning-icon">
          <el-icon><Warning /></el-icon>
        </div>
        <p>确定要清除所有规划吗？</p>
        <p class="warning-text">此操作不可恢复，所有学习进度将被重置。</p>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showClearConfirm = false" class="cancel-btn">取消</el-button>
          <el-button type="danger" @click="clearAllPlan" class="confirm-btn">确认清除</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import { Document, Clock, VideoPlay, Calendar, Delete, Plus, Warning } from "@element-plus/icons-vue"
import { ElMessage, ElMessageBox } from "element-plus"

const stats = ref({ total_records: 0, learning_count: 0, reviewing_count: 0, today_review_count: 0 })
const todayTasks = ref([])
const planRecords = ref([])
const showClearConfirm = ref(false)

const loadStats = async () => {
  try {
    const res = await axios.get("/api/distinguish/plan/statistics")
    stats.value = res.data.data || {}
  } catch (e) { console.error(e) }
}

const loadTasks = async () => {
  try {
    const res = await axios.get("/api/distinguish/plan/tasks")
    todayTasks.value = res.data.data || []
  } catch (e) { console.error(e) }
}

const loadPlanRecords = async () => {
  try {
    const res = await axios.get("/api/distinguish/plan/list")
    planRecords.value = res.data.data || []
  } catch (e) { console.error(e) }
}

const startPractice = () => {
  window.location.href = "/distinguish/memory"
}

const removeFromPlan = async (recordId) => {
  try {
    await ElMessageBox.confirm('确定要将此条目移出规划吗？', '确认移出', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await axios.delete(`/api/distinguish/plan/record/${recordId}`)
    ElMessage.success('已移出规划')
    await loadStats()
    await loadPlanRecords()
    await loadTasks()
  } catch (e) {
    if (e !== 'cancel') {
      console.error(e)
      ElMessage.error('移出失败')
    }
  }
}

const clearAllConfirm = () => {
  showClearConfirm.value = true
}

const clearAllPlan = async () => {
  try {
    await axios.delete("/api/distinguish/plan/clear-all")
    showClearConfirm.value = false
    ElMessage.success('已清除所有规划')
    await loadStats()
    await loadPlanRecords()
    await loadTasks()
  } catch (e) {
    console.error(e)
    ElMessage.error('清除失败')
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return "-"
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}/${date.getDate()}`
}

const isToday = (dateStr) => {
  if (!dateStr) return false
  const date = new Date(dateStr)
  const today = new Date()
  return date.toDateString() === today.toDateString()
}

const goToManagement = () => {
  window.location.href = "/distinguish/management"
}

onMounted(() => { loadStats(); loadTasks(); loadPlanRecords() })
</script>

<style scoped>
.distinguish-plan {
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

.primary-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.primary-btn:disabled {
  background: #d1d5db;
  box-shadow: none;
}

.danger-btn {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(248, 113, 113, 0.3);
}

.danger-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(248, 113, 113, 0.4);
}

.stats-row {
  margin-bottom: 28px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 18px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  height: 100%;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
  flex-shrink: 0;
}

.stat-icon.purple {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-icon.orange {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-icon.green {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-icon.red {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}

.stat-label {
  color: #64748b;
  font-size: 14px;
  margin-top: 4px;
}

.content-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f1f5f9;
}

.card-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.record-count {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.records-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 20px;
}

.record-item {
  background: #f8fafc;
  border-radius: 14px;
  padding: 20px;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.record-item:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.chapter-tag {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1d4ed8;
  padding: 5px 14px;
  border-radius: 18px;
  font-size: 12px;
  font-weight: 600;
}

.record-stem {
  font-size: 15px;
  line-height: 1.7;
  color: #334155;
  margin-bottom: 14px;
  padding: 12px;
  background: white;
  border-radius: 10px;
  max-height: 80px;
  overflow: hidden;
}

.record-option {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 14px;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  border-radius: 10px;
  margin-bottom: 14px;
}

.option-label {
  font-size: 18px;
  font-weight: 700;
  color: #475569;
}

.option-text {
  font-size: 15px;
  line-height: 1.6;
  color: #334155;
}

.record-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.review-info {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #64748b;
  font-size: 13px;
}

.today-highlight {
  color: #ef4444;
  font-weight: 600;
}

.remove-btn {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #dc2626;
  border: none;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 8px;
}

.remove-btn:hover {
  background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
}

.empty-state {
  padding: 60px 20px;
}

.empty-state :deep(.el-empty__description p) {
  color: #64748b;
  font-size: 15px;
}

.modern-dialog :deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
}

.modern-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
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

.confirm-content {
  text-align: center;
  padding: 24px;
}

.warning-icon {
  width: 72px;
  height: 72px;
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  font-size: 36px;
  color: #ef4444;
}

.confirm-content p {
  font-size: 16px;
  color: #334155;
  margin: 0 0 8px 0;
}

.warning-text {
  font-size: 14px !important;
  color: #ef4444 !important;
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

.confirm-btn {
  padding: 10px 24px;
  border-radius: 10px;
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
  
  .records-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: 18px;
  }
  
  .stat-icon {
    width: 52px;
    height: 52px;
    font-size: 24px;
  }
  
  .stat-value {
    font-size: 26px;
  }
}
</style>
