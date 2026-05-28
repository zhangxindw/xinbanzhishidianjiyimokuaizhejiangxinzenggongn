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
import { ref, onMounted } from 'vue'
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
</style>
