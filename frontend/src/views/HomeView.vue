<template>
  <div class="home-view">
    <div class="page-header">
      <h2>欢迎使用在线题库系统</h2>
      <p>支持Excel批量导入、多种刷题模式、实时编辑功能</p>
    </div>

    <el-row :gutter="20">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #667eea;">
            <el-icon><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.total_questions }}</div>
            <div class="stat-label">题库总数</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #52c41a;">
            <el-icon><CircleCheck /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.total_answered }}</div>
            <div class="stat-label">已答题数</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #faad14;">
            <el-icon><Star /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.correct_rate }}%</div>
            <div class="stat-label">正确率</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #ff4d4f;">
            <el-icon><CircleClose /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.wrong_count }}</div>
            <div class="stat-label">错题数</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <div class="card">
          <h3>快捷入口</h3>
          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/practice/memorize')">
              <el-icon><Memo /></el-icon>
              背题模式
            </el-button>
            <el-button type="success" @click="$router.push('/practice/random')">
              <el-icon><RefreshRight /></el-icon>
              随机出题
            </el-button>
            <el-button type="warning" @click="$router.push('/practice/sequential')">
              <el-icon><Sort /></el-icon>
              顺序刷题
            </el-button>
            <el-button type="danger" @click="$router.push('/practice/wrong')">
              <el-icon><WarnTriangleFilled /></el-icon>
              错题练习
            </el-button>
            <el-button type="info" @click="$router.push('/practice/crazy')">
              <el-icon><Lightning /></el-icon>
              疯狂刷题
            </el-button>
            <el-button type="success" @click="$router.push('/practice/memory')">
              <el-icon><Memo /></el-icon>
              记忆刷题
            </el-button>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="card">
          <h3>功能说明</h3>
          <div class="feature-list">
            <div class="feature-item">
              <el-icon color="#667eea"><Upload /></el-icon>
              <span>支持Excel批量导入题目</span>
            </div>
            <div class="feature-item">
              <el-icon color="#667eea"><Edit /></el-icon>
              <span>富媒体编辑支持图片、表格、公式</span>
            </div>
            <div class="feature-item">
              <el-icon color="#667eea"><Reading /></el-icon>
              <span>多种刷题模式：背题、随机、跨章节</span>
            </div>
            <div class="feature-item">
              <el-icon color="#667eea"><Setting /></el-icon>
              <span>护眼模式、字体大小调节</span>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 记忆规划数据预览卡片 -->
    <div class="card memory-plan-card" style="margin-top: 20px;">
      <div class="memory-plan-header">
        <h3>记忆规划数据</h3>
        <el-button type="primary" text @click="$router.push('/memory/plan')">
          查看详情 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
      <el-row :gutter="20" style="margin-top: 15px;">
        <el-col :span="6">
          <div class="memory-stat-item">
            <div class="memory-stat-icon" style="background: #e6f7ff;">
              <el-icon color="#1890ff"><Collection /></el-icon>
            </div>
            <div class="memory-stat-info">
              <div class="memory-stat-value">{{ memoryPlan.total_records }}</div>
              <div class="memory-stat-label">已加入规划</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="memory-stat-item">
            <div class="memory-stat-icon" style="background: #fff7e6;">
              <el-icon color="#fa8c16"><Calendar /></el-icon>
            </div>
            <div class="memory-stat-info">
              <div class="memory-stat-value">{{ memoryPlan.today_review_count }}</div>
              <div class="memory-stat-label">今日预计复习</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="memory-stat-item">
            <div class="memory-stat-icon" style="background: #f6ffed;">
              <el-icon color="#52c41a"><Sunrise /></el-icon>
            </div>
            <div class="memory-stat-info">
              <div class="memory-stat-value">{{ memoryPlan.tomorrow_review_count }}</div>
              <div class="memory-stat-label">明日预计复习</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="memory-stat-item">
            <div class="memory-stat-icon" style="background: #fff0f6;">
              <el-icon color="#eb2f96"><TrendCharts /></el-icon>
            </div>
            <div class="memory-stat-info">
              <div class="memory-stat-value">{{ next15DaysTotal }}</div>
              <div class="memory-stat-label">近15天需复习</div>
            </div>
          </div>
        </el-col>
      </el-row>
      <!-- 近15天复习趋势图 -->
      <div class="review-chart" style="margin-top: 20px;">
        <div class="chart-title">近15天复习计划趋势</div>
        <div class="chart-bars">
          <div v-for="(item, index) in memoryPlan.next_15_days" :key="index" class="chart-bar-item">
            <div class="bar-wrapper">
              <div class="bar" :style="{ height: getBarHeight(item.count) + 'px', background: getBarColor(item.count) }"></div>
            </div>
            <div class="bar-label">{{ item.date }}</div>
            <div class="bar-value">{{ item.count }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="card" style="margin-top: 20px;">
      <h3>最近导入记录</h3>
      <el-table :data="recentImports" style="width: 100%">
        <el-table-column prop="action" label="操作" />
        <el-table-column prop="target_type" label="对象类型" />
        <el-table-column prop="details" label="详情" />
        <el-table-column prop="created_at" label="时间">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuizStore } from '@/store/quiz'
import axios from 'axios'

const store = useQuizStore()
const statistics = ref({
  total_questions: 0,
  total_answered: 0,
  correct_rate: 0,
  wrong_count: 0
})
const recentImports = ref([])

// 记忆规划数据
const memoryPlan = ref({
  total_records: 0,
  today_review_count: 0,
  tomorrow_review_count: 0,
  next_15_days: []
})

// 近15天总复习数
const next15DaysTotal = computed(() => {
  return memoryPlan.value.next_15_days.reduce((sum, item) => sum + item.count, 0)
})

// 获取柱状图高度（最大80px）
const getBarHeight = (count) => {
  const max = Math.max(...memoryPlan.value.next_15_days.map(d => d.count), 1)
  return Math.max((count / max) * 80, 4)
}

// 获取柱状图颜色
const getBarColor = (count) => {
  if (count === 0) return '#d9d9d9'
  if (count <= 3) return '#52c41a'
  if (count <= 6) return '#faad14'
  return '#ff4d4f'
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN')
}

onMounted(async () => {
  statistics.value = await store.loadStatistics()
  try {
    const res = await axios.get('/api/logs?page=1&per_page=10')
    recentImports.value = res.data.data || []
  } catch (e) {
    console.error('Failed to load logs:', e)
  }
  // 加载记忆规划数据
  try {
    const mpRes = await axios.get('/api/memory/preview')
    if (mpRes.data.status === 'ok') {
      memoryPlan.value = mpRes.data.data
    }
  } catch (e) {
    console.error('Failed to load memory plan preview:', e)
  }
})
</script>

<style scoped>
.home-view {
  padding: 20px;
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

.quick-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 15px;
}

.quick-actions .el-button {
  display: flex;
  align-items: center;
  gap: 5px;
}

.feature-list {
  margin-top: 15px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}

.feature-item:last-child {
  border-bottom: none;
}

/* 记忆规划卡片样式 */
.memory-plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.memory-plan-header h3 {
  margin: 0;
}

.memory-stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: #fafafa;
  border-radius: 8px;
}

.memory-stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}

.memory-stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.memory-stat-label {
  color: #666;
  font-size: 13px;
}

/* 复习趋势图 */
.review-chart {
  padding: 15px;
  background: #fafafa;
  border-radius: 8px;
}

.chart-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
}

.chart-bars {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  height: 120px;
  padding: 0 5px;
}

.chart-bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  min-width: 0;
}

.bar-wrapper {
  width: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  height: 90px;
}

.bar {
  width: 70%;
  min-width: 4px;
  border-radius: 3px 3px 0 0;
  transition: all 0.3s;
}

.bar-label {
  font-size: 11px;
  color: #999;
  margin-top: 6px;
  white-space: nowrap;
  transform: rotate(-30deg);
  transform-origin: center top;
}

.bar-value {
  font-size: 11px;
  color: #666;
  margin-top: 2px;
}
</style>
