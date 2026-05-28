<template>
  <div class="statistics-view">
    <div class="page-header">
      <h2>数据统计</h2>
      <p>查看刷题数据统计，了解学习进度</p>
    </div>

    <el-row :gutter="20">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
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
          <div class="stat-icon" style="background: linear-gradient(135deg, #52c41a 0%, #73d13d 100%);">
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
          <div class="stat-icon" style="background: linear-gradient(135deg, #faad14 0%, #ffc53d 100%);">
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
          <div class="stat-icon" style="background: linear-gradient(135deg, #ff4d4f 0%, #ff7875 100%);">
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
          <h3>各题型分布</h3>
          <div class="chart-container">
            <div v-for="stat in statistics.type_stats" :key="stat.type_id" class="stat-bar">
              <div class="stat-bar-label">
                <span>{{ stat.type_name }}</span>
                <span>{{ stat.count }} 题</span>
              </div>
              <el-progress :percentage="(stat.count / statistics.total_questions * 100) || 0" :stroke-width="20" />
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="card">
          <h3>学习概览</h3>
          <div class="overview-list">
            <div class="overview-item">
              <span class="overview-icon" style="background: #667eea;">
                <el-icon><Document /></el-icon>
              </span>
              <span class="overview-text">题库题目总数</span>
              <span class="overview-value">{{ statistics.total_questions }}</span>
            </div>
            <div class="overview-item">
              <span class="overview-icon" style="background: #52c41a;">
                <el-icon><CircleCheck /></el-icon>
              </span>
              <span class="overview-text">回答正确数</span>
              <span class="overview-value">{{ statistics.total_correct }}</span>
            </div>
            <div class="overview-item">
              <span class="overview-icon" style="background: #ff4d4f;">
                <el-icon><CircleClose /></el-icon>
              </span>
              <span class="overview-text">错题本数量</span>
              <span class="overview-value">{{ statistics.wrong_count }}</span>
            </div>
            <div class="overview-item">
              <span class="overview-icon" style="background: #faad14;">
                <el-icon><Star /></el-icon>
              </span>
              <span class="overview-text">收藏数量</span>
              <span class="overview-value">{{ statistics.favorite_count }}</span>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuizStore } from '@/store/quiz'

const store = useQuizStore()

const statistics = ref({
  total_questions: 0,
  total_answered: 0,
  total_correct: 0,
  correct_rate: 0,
  wrong_count: 0,
  favorite_count: 0,
  type_stats: []
})

onMounted(async () => {
  statistics.value = await store.loadStatistics()
})
</script>

<style scoped>
.statistics-view {
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

.chart-container {
  margin-top: 20px;
}

.stat-bar {
  margin-bottom: 20px;
}

.stat-bar-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  color: #666;
}

.overview-list {
  margin-top: 20px;
}

.overview-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px 0;
  border-bottom: 1px solid #f0f0f0;
}

.overview-item:last-child {
  border-bottom: none;
}

.overview-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.overview-text {
  flex: 1;
  color: #666;
}

.overview-value {
  font-weight: bold;
  font-size: 18px;
  color: #333;
}
</style>
