<template>
  <div class="practice-plan-view">
    <div class="page-header">
      <h2>刷题规划</h2>
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
            <div class="stat-label">已添加题目</div>
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
          开始刷题记忆
        </el-button>
      </div>
      <div v-if="todayTasks.length > 0">
        <el-table :data="todayTasks" border style="width: 100%">
          <el-table-column prop="stem" label="题目" />
          <el-table-column prop="chapter_name" label="章节" width="150" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <span :class="row.status === 'learning' ? 'status-learning' : 'status-reviewing'">
                {{ row.status === 'learning' ? '初学中' : '复习中' }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="next_review_date" label="下次复习" width="120" />
          <el-table-column prop="review_count" label="复习次数" width="80" />
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button type="danger" size="small" @click="removeFromPlan(row.id)">
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div v-else class="empty-state">
        <el-icon size="48" color="#ccc"><VideoPlay /></el-icon>
        <p>今日待复习任务已完成！</p>
      </div>
    </div>

    <!-- 添加题目到刷题规划 -->
    <div class="card" style="margin-top: 20px;">
      <div class="card-header">
        <h3>从题库选择题目加入规划</h3>
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
        <el-input 
          v-model="filterKeyword" 
          placeholder="搜索题目关键词"
          @keyup.enter="loadAvailableQuestions"
        />
        <el-button @click="loadAvailableQuestions">筛选</el-button>
      </div>

      <el-table :data="availableQuestions" border style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" :selectable="checkSelectable" />
        <el-table-column prop="stem" label="题目" show-overflow-tooltip>
          <template #default="{ row }">
            <span v-html="row.stem_html || row.stem"></span>
          </template>
        </el-table-column>
        <el-table-column prop="chapter_name" label="章节" width="150" />
        <el-table-column prop="question_type_name" label="类型" width="100" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <span v-if="row.already_in_plan" class="status-in-plan">已加入</span>
            <span v-else class="status-available">可选</span>
          </template>
        </el-table-column>
      </el-table>

      <div class="batch-actions">
        <el-button type="primary" @click="addToPracticePlan">
          <el-icon><Plus /></el-icon>
          添加选中到刷题规划
        </el-button>
        <span class="selected-info">已选 {{ selectedQuestionIds.length }} 题</span>
      </div>

      <!-- 分页组件 -->
      <div class="pagination-wrapper">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
          :current-page="currentPage"
          :page-sizes="[15, 20, 30, 50, 80, 100, 200, 300, 500]"
          :page-size="pageSize"
          :total="totalItems"
          layout="total, sizes, prev, pager, next, jumper"
        />
      </div>
    </div>

    <!-- 刷题记忆算法说明 -->
    <div class="card" style="margin-top: 20px;">
      <h3>刷题记忆算法说明</h3>
      <div class="curve-info">
        <div class="curve-item">
          <span class="curve-step">初学阶段</span>
          <ul>
            <li>首次做错：安排在8题后再次出现</li>
            <li>首次做对：安排在12题后验证是否真正掌握</li>
            <li>验证做对：完成初学，进入复习阶段</li>
            <li>验证做错：重新回到8题后循环</li>
            <li><strong>必须连续两次做对才能完成初学</strong></li>
          </ul>
        </div>
        <div class="curve-item">
          <span class="curve-step">复习间隔</span>
          <p>复习间隔档位：1天 → 2天 → 4天 → 7天 → 15天 → 30天 → 60天 → 120天...</p>
        </div>
        <div class="curve-item">
          <span class="curve-step">复习反馈</span>
          <ul>
            <li><strong>做对</strong>：间隔前进到下一个档位</li>
            <li><strong>做错</strong>：打回初学状态，重新开始</li>
          </ul>
        </div>
        <div class="curve-item">
          <span class="curve-step">学习原则</span>
          <p>先完成今日待复习任务，才能学习新题目。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { Document, Clock, Calendar, Bell, Plus, Delete, VideoPlay } from '@element-plus/icons-vue'

const stats = reactive({
  total_records: 0,
  learning_count: 0,
  reviewing_count: 0,
  today_review_count: 0
})

const todayTasks = ref([])
const chapters = ref([])
const availableQuestions = ref([])
const selectedQuestionIds = ref([])

const filterChapter = ref('')
const filterKeyword = ref('')

const currentPage = ref(1)
const pageSize = ref(15)
const totalItems = ref(0)

const loadStats = async () => {
  try {
    const res = await axios.get('/api/practice-plan/statistics?user_id=default_user')
    Object.assign(stats, res.data.data || {})
  } catch (error) {
    console.error('加载统计失败:', error)
  }
}

const loadTodayTasks = async () => {
  try {
    const res = await axios.get('/api/practice-plan/list?user_id=default_user')
    todayTasks.value = res.data.data || []
  } catch (error) {
    console.error('加载今日任务失败:', error)
  }
}

const loadChapters = async () => {
  try {
    const res = await axios.get('/api/chapters')
    chapters.value = res.data.data || []
  } catch (error) {
    console.error('加载章节失败:', error)
  }
}

const loadAvailableQuestions = async (page = 1) => {
  try {
    const params = new URLSearchParams()
    params.set('page', page)
    params.set('page_size', pageSize.value)
    if (filterChapter.value) {
      params.append('chapter_id', filterChapter.value)
    }
    if (filterKeyword.value) {
      params.set('keyword', filterKeyword.value)
    }
    
    const res = await axios.get(`/api/practice-plan/questions?${params}`)
    availableQuestions.value = res.data.data || []
    totalItems.value = res.data.total || 0
    currentPage.value = res.data.page || 1
  } catch (error) {
    console.error('加载题目失败:', error)
  }
}

const checkSelectable = (row) => {
  return !row.already_in_plan
}

const handlePageChange = (page) => {
  loadAvailableQuestions(page)
}

const handleSizeChange = (size) => {
  pageSize.value = size
  loadAvailableQuestions(1)
}

const handleSelectionChange = (val) => {
  selectedQuestionIds.value = val.map(item => item.id)
}

const addToPracticePlan = async () => {
  if (selectedQuestionIds.value.length === 0) {
    alert('请先选择题目')
    return
  }
  
  try {
    await axios.post('/api/practice-plan/add?user_id=default_user', {
      question_ids: selectedQuestionIds.value
    })
    
    alert(`已将 ${selectedQuestionIds.value.length} 个题目添加到刷题规划！`)
    selectedQuestionIds.value = []
    await loadAvailableQuestions()
    await loadStats()
    await loadTodayTasks()
  } catch (error) {
    console.error('添加失败:', error)
    alert('添加失败: ' + (error.response?.data?.message || error.message))
  }
}

const removeFromPlan = async (recordId) => {
  if (!confirm('确定要移除这道题吗？')) return
  
  try {
    await axios.delete(`/api/practice-plan/record/${recordId}`)
    await loadTodayTasks()
    await loadStats()
  } catch (error) {
    console.error('移除失败:', error)
    alert('移除失败')
  }
}

const confirmClearAll = () => {
  if (stats.total_records === 0) {
    alert('当前没有已添加的规划')
    return
  }
  
  if (confirm('规划清空后不可恢复，是否清空全部规划？')) {
    clearAllPlan()
  }
}

const clearAllPlan = async () => {
  try {
    await axios.delete('/api/practice-plan/clear-all?user_id=default_user')
    alert('清空成功')
    await loadStats()
    await loadTodayTasks()
  } catch (error) {
    console.error('清空失败:', error)
    alert('清空失败')
  }
}

const startPractice = () => {
  window.location.replace('/practice/memory')
}

onMounted(async () => {
  await loadStats()
  await loadTodayTasks()
  await loadChapters()
  await loadAvailableQuestions()
})
</script>

<style scoped>
.practice-plan-view {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
}

.stat-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.stat-icon .el-icon {
  font-size: 28px;
  color: #fff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.card {
  background: #fff;
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
  font-size: 18px;
}

.filter-section {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.filter-section .el-select,
.filter-section .el-input {
  width: 200px;
}

.batch-actions {
  margin-top: 15px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.selected-info {
  color: #666;
  font-size: 14px;
}

.pagination-wrapper {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
  color: #999;
}

.empty-state p {
  margin-top: 10px;
  font-size: 16px;
}

.status-learning {
  color: #faad14;
  font-weight: bold;
}

.status-reviewing {
  color: #52c41a;
  font-weight: bold;
}

.status-in-plan {
  color: #52c41a;
  font-weight: bold;
}

.status-available {
  color: #1890ff;
}

.curve-info {
  padding: 10px 0;
}

.curve-item {
  margin-bottom: 20px;
}

.curve-step {
  font-weight: bold;
  font-size: 16px;
  color: #333;
  display: block;
  margin-bottom: 8px;
}

.curve-item ul {
  margin: 0;
  padding-left: 20px;
}

.curve-item p {
  margin: 0;
  color: #666;
  line-height: 1.6;
}
</style>
