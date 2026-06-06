<template>
  <div class="memory-plan-view">
    <div class="page-header">
      <h2>记忆规划 - 艾宾浩斯遗忘曲线</h2>
      <el-button type="danger" plain @click="confirmClearAll">
        <el-icon><Delete /></el-icon>
        一键清空全部规划
      </el-button>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #667eea;">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_records }}</div>
            <div class="stat-label">已添加知识点</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #faad14;">
            <el-icon><Clock /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.learning_count }}</div>
            <div class="stat-label">初学中</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #52c41a;">
            <el-icon><VideoPlay /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.reviewing_count }}</div>
            <div class="stat-label">复习中</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #ff4d4f;">
            <el-icon><Calendar /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.today_review_count }}</div>
            <div class="stat-label">今日待复习</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 今日待复习 -->
    <div class="card" style="margin-top: 20px;">
      <div class="card-header">
        <h3>今日待复习任务</h3>
        <el-button type="primary" @click="startPractice">
          <el-icon><Bell /></el-icon>
          开始练习
        </el-button>
      </div>
      <div v-if="todayTasks.length > 0">
        <el-table :data="todayTasks" border style="width: 100%">
          <el-table-column prop="knowledge_point.priority_label" label="优先级" width="100">
            <template #default="{ row }">
              <span :class="getPriorityClass(row.knowledge_point.priority)">
                {{ row.knowledge_point.priority_label }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="knowledge_point.question" label="知识点" />
          <el-table-column prop="knowledge_point.mnemonic" label="速记口诀" width="150" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <span :class="row.status === 'learning' ? 'status-learning' : 'status-reviewing'">
                {{ row.status === 'learning' ? '初学中' : '复习中' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="next_review_date" label="下次复习" width="120" />
          <el-table-column prop="review_count" label="复习次数" width="80" />
        </el-table>
      </div>
      <div v-else class="empty-state">
        <el-icon size="48" color="#ccc"><VideoPlay /></el-icon>
        <p>今日待复习任务已完成！</p>
      </div>
    </div>

    <!-- 添加知识点到记忆规划 -->
    <div class="card" style="margin-top: 20px;">
      <div class="card-header">
        <h3>添加知识点到记忆规划</h3>
      </div>
      
      <div class="filter-section">
        <el-select v-model="filterChapter" placeholder="选择章节" clearable>
          <el-option label="全部章节" :value="''" />
          <el-option 
            v-for="chapter in chapters" 
            :key="chapter.id" 
            :label="chapter.name" 
            :value="chapter.id" 
          />
        </el-select>
        <el-select v-model="filterPriority" placeholder="选择优先级" clearable>
          <el-option label="全部" :value="''" />
          <el-option label="[必须背]" value="must" />
          <el-option label="[重点背]" value="important" />
          <el-option label="[尽量背]" value="normal" />
        </el-select>
        <el-input 
          v-model="filterKeyword" 
          placeholder="搜索知识点"
          @keyup.enter="loadAvailableKnowledgePoints"
        />
        <el-button @click="loadAvailableKnowledgePoints">筛选</el-button>
      </div>

      <el-table :data="availableKnowledgePoints" border style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column prop="priority_label" label="优先级" width="100">
          <template #default="{ row }">
            <span :class="getPriorityClass(row.priority)">
              {{ row.priority_label }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="question" label="知识点" />
        <el-table-column prop="mnemonic" label="速记口诀" width="150" />
        <el-table-column prop="chapter_name" label="章节" width="120" />
      </el-table>

      <div class="batch-actions">
        <el-button type="primary" @click="addToMemoryPlan">
          <el-icon><Plus /></el-icon>
          添加选中到记忆规划
        </el-button>
      </div>
    </div>

    <!-- 艾宾浩斯曲线说明 -->
    <div class="card" style="margin-top: 20px;">
      <h3>艾宾浩斯遗忘曲线说明</h3>
      <div class="curve-info">
        <div class="curve-item">
          <span class="curve-step">初学阶段</span>
          <p>新知识点首次进入系统时，需要当天内连续两次背出才能进入复习阶段。</p>
        </div>
        <div class="curve-item">
          <span class="curve-step">复习间隔</span>
          <p>复习间隔档位：1天 → 2天 → 4天 → 7天 → 15天 → 30天 → 60天 → 120天...</p>
        </div>
        <div class="curve-item">
          <span class="curve-step">反馈调整</span>
          <ul>
            <li><strong>背出了</strong>：间隔前进到下一个档位</li>
            <li><strong>模糊</strong>：间隔回退一档</li>
            <li><strong>背不出</strong>：打回初学状态，重新开始</li>
          </ul>
        </div>
        <div class="curve-item">
          <span class="curve-step">学习原则</span>
          <p>先完成今日待复习任务，才能学习新知识点。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { Document, Clock, Calendar, Bell, Plus, Delete } from '@element-plus/icons-vue'

const stats = reactive({
  total_records: 0,
  learning_count: 0,
  reviewing_count: 0,
  today_review_count: 0
})

const todayTasks = ref([])
const chapters = ref([])
const availableKnowledgePoints = ref([])
const selectedKpIds = ref([])

const filterChapter = ref('')
const filterPriority = ref('')
const filterKeyword = ref('')

const loadStats = async () => {
  const res = await axios.get('/api/memory/statistics?user_id=default_user')
  Object.assign(stats, res.data.data || {})
}

// 确认清空全部规划
const confirmClearAll = () => {
  if (stats.total_records === 0) {
    alert('当前没有已添加的规划')
    return
  }
  
  if (confirm('规划清空后不可恢复，是否清空全部规划？')) {
    clearAllPlan()
  }
}

// 清空全部规划
const clearAllPlan = async () => {
  try {
    await axios.delete('/api/memory/clear-all')
    alert('清空成功')
    loadStats()
    loadTodayTasks()
  } catch (error) {
    console.error('清空失败:', error)
    alert('清空失败: ' + (error.response?.data?.message || error.message))
  }
}

const loadTodayTasks = async () => {
  const res = await axios.get('/api/memory/today-tasks?user_id=default_user')
  todayTasks.value = res.data.data || []
}

const loadChapters = async () => {
  const res = await axios.get('/api/chapters')
  chapters.value = res.data.data || []
}

const loadAvailableKnowledgePoints = async () => {
  try {
    const params = new URLSearchParams()
    if (filterChapter.value) params.set('chapter_id', filterChapter.value)
    if (filterPriority.value) params.set('priority', filterPriority.value)
    if (filterKeyword.value) params.set('keyword', filterKeyword.value)
    
    const res = await axios.get(`/api/knowledge-points?${params}`)
    console.log('所有知识点:', res.data.data)
    
    // 获取已在记忆规划中的知识点ID
    const memoryRes = await axios.get('/api/memory-records?user_id=default_user')
    const existingIds = new Set(memoryRes.data.data.map(r => r.knowledge_point_id))
    console.log('已添加的知识点ID:', existingIds)
    
    // 过滤掉已添加的知识点
    availableKnowledgePoints.value = res.data.data.filter(kp => !existingIds.has(kp.id))
    console.log('可用知识点:', availableKnowledgePoints.value)
  } catch (error) {
    console.error('加载知识点失败:', error)
    alert('加载知识点失败: ' + (error.response?.data?.message || error.message))
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

const handleSelectionChange = (val) => {
  selectedKpIds.value = val.map(item => item.id)
}

const addToMemoryPlan = async () => {
  if (selectedKpIds.value.length === 0) {
    alert('请先选择知识点')
    return
  }
  
  await axios.post('/api/memory-records?user_id=default_user', {
    kp_ids: selectedKpIds.value
  })
  
  alert(`已将 ${selectedKpIds.value.length} 个知识点添加到记忆规划！`)
  selectedKpIds.value = []
  await loadAvailableKnowledgePoints()
  await loadStats()
  await loadTodayTasks()
}

const startPractice = () => {
  window.location.href = '/memory/practice'
}

onMounted(async () => {
  await loadStats()
  await loadTodayTasks()
  await loadChapters()
  await loadAvailableKnowledgePoints()
})
</script>

<style scoped>
.memory-plan-view {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.card-header h3 {
  margin: 0;
}

.priority-must {
  background: #ff4d4f;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.priority-important {
  background: #faad14;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.priority-normal {
  background: #52c41a;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.status-learning {
  background: #fff7e6;
  color: #fa8c16;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.status-reviewing {
  background: #f6ffed;
  color: #52c41a;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-state p {
  margin: 16px 0;
}

.filter-section {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.filter-section .el-select,
.filter-section .el-input {
  width: 180px;
}

.batch-actions {
  margin-top: 15px;
  text-align: right;
}

.curve-info {
  color: #666;
  line-height: 1.8;
}

.curve-item {
  margin-bottom: 15px;
}

.curve-item:last-child {
  margin-bottom: 0;
}

.curve-step {
  display: inline-block;
  background: #667eea;
  color: white;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 8px;
}

.curve-item ul {
  margin: 0;
  padding-left: 20px;
}

.curve-item li {
  margin-bottom: 5px;
}
</style>