<template>
  <div class="mobile-home">
    <!-- 顶部标题栏 -->
    <header class="mobile-header">
      <div class="header-content">
        <h1>在线题库</h1>
        <p class="header-subtitle">高效学习，智能练习</p>
      </div>
      <div class="header-bg"></div>
    </header>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <div class="stat-card primary">
        <div class="stat-icon-wrapper">
          <div class="stat-icon">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M832 384H576V128H192v768h640zm-26.496-64L640 154.496V320zM160 64h480l256 256v608a32 32 0 0 1-32 32H160a32 32 0 0 1-32-32V96a32 32 0 0 1 32-32m160 448h384v64H320zm0-192h160v64H320zm0 384h384v64H320z"></path></svg>
          </div>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ statistics.total_questions }}</div>
          <div class="stat-label">题库总数</div>
        </div>
        <div class="stat-decoration"></div>
      </div>
      <div class="stat-card danger">
        <div class="stat-icon-wrapper">
          <div class="stat-icon">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="m466.752 512-90.496-90.496a32 32 0 0 1 45.248-45.248L512 466.752l90.496-90.496a32 32 0 1 1 45.248 45.248L557.248 512l90.496 90.496a32 32 0 1 1-45.248 45.248L512 557.248l-90.496 90.496a32 32 0 0 1-45.248-45.248z"></path><path fill="currentColor" d="M512 896a384 384 0 1 0 0-768 384 384 0 0 0 0 768m0 64a448 448 0 1 1 0-896 448 448 0 0 1 0 896"></path></svg>
          </div>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ statistics.wrong_count }}</div>
          <div class="stat-label">错题数</div>
        </div>
        <div class="stat-decoration"></div>
      </div>
    </div>

    <!-- 记忆规划数据 -->
    <div class="memory-section">
      <div class="section-header">
        <h3 class="section-heading">
          <svg class="heading-icon" viewBox="0 0 1024 1024"><path fill="currentColor" d="M784.512 230.272v-50.56a32 32 0 1 1 64 0v149.056a32 32 0 0 1-32 32H667.52a32 32 0 1 1 0-64h92.992A320 320 0 1 0 524.8 833.152a320 320 0 0 0 320-320h64a384 384 0 0 1-384 384 384 384 0 0 1-384-384 384 384 0 0 1 643.712-282.88"></path></svg>
          记忆规划
        </h3>
        <span class="view-detail" @click="goToMemoryPlan">
          查看详情
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M716.8 537.6a12.8 12.8 0 0 1 0 17.92L332.8 940.8a12.8 12.8 0 0 1-17.92-17.92l371.2-371.2-371.2-371.2a12.8 12.8 0 1 1 17.92-17.92z"></path></svg>
        </span>
      </div>
      <div class="memory-stats">
        <div class="memory-item">
          <div class="memory-value">{{ memoryPlan.total_records }}</div>
          <div class="memory-label">已加入规划</div>
        </div>
        <div class="memory-divider"></div>
        <div class="memory-item">
          <div class="memory-value today">{{ memoryPlan.today_review_count }}</div>
          <div class="memory-label">今日复习</div>
        </div>
        <div class="memory-divider"></div>
        <div class="memory-item">
          <div class="memory-value">{{ memoryPlan.tomorrow_review_count }}</div>
          <div class="memory-label">明日复习</div>
        </div>
        <div class="memory-divider"></div>
        <div class="memory-item">
          <div class="memory-value">{{ next15DaysTotal }}</div>
          <div class="memory-label">近15天</div>
        </div>
      </div>
    </div>

    <!-- 功能入口 -->
    <div class="features-section">
      <h3 class="section-heading">
        <svg class="heading-icon" viewBox="0 0 1024 1024"><path fill="currentColor" d="M384 96a32 32 0 0 1 64 0v786.752a32 32 0 0 1-54.592 22.656L95.936 608a32 32 0 0 1 0-45.312h.128a32 32 0 0 1 45.184 0L384 805.632zm192 45.248a32 32 0 0 1 54.592-22.592L928.064 416a32 32 0 0 1 0 45.312h-.128a32 32 0 0 1-45.184 0L640 218.496V928a32 32 0 1 1-64 0z"></path></svg>
        刷题练习
      </h3>
      <div class="feature-grid">
        <div class="feature-card sequential" @click="goToSequential">
          <div class="feature-bg"></div>
          <div class="feature-icon">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M384 96a32 32 0 0 1 64 0v786.752a32 32 0 0 1-54.592 22.656L95.936 608a32 32 0 0 1 0-45.312h.128a32 32 0 0 1 45.184 0L384 805.632zm192 45.248a32 32 0 0 1 54.592-22.592L928.064 416a32 32 0 0 1 0 45.312h-.128a32 32 0 0 1-45.184 0L640 218.496V928a32 32 0 1 1-64 0z"></path></svg>
          </div>
          <span class="feature-name">顺序刷题</span>
          <span class="feature-desc">按章节系统学习</span>
        </div>
        <div class="feature-card random" @click="goToRandom">
          <div class="feature-bg"></div>
          <div class="feature-icon">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M784.512 230.272v-50.56a32 32 0 1 1 64 0v149.056a32 32 0 0 1-32 32H667.52a32 32 0 1 1 0-64h92.992A320 320 0 1 0 524.8 833.152a320 320 0 0 0 320-320h64a384 384 0 0 1-384 384 384 384 0 0 1-384-384 384 384 0 0 1 643.712-282.88"></path></svg>
          </div>
          <span class="feature-name">随机出题</span>
          <span class="feature-desc">随机挑战提升</span>
        </div>
        <div class="feature-card wrong" @click="goToWrong">
          <div class="feature-bg"></div>
          <div class="feature-icon">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M928.99 755.83 574.6 203.25c-12.89-20.16-36.76-32.58-62.6-32.58s-49.71 12.43-62.6 32.58L95.01 755.83c-12.91 20.12-12.9 44.91.01 65.03 12.92 20.12 36.78 32.51 62.59 32.49h708.78c25.82.01 49.68-12.37 62.59-32.49s12.92-44.91.01-65.03M554.67 768h-85.33v-85.33h85.33zm0-426.67v298.66h-85.33V341.32z"></path></svg>
          </div>
          <span class="feature-name">错题练习</span>
          <span class="feature-desc">攻克薄弱环节</span>
        </div>
      </div>
    </div>

    <div class="features-section memory-module">
      <h3 class="section-heading">
        <svg class="heading-icon" viewBox="0 0 1024 1024"><path fill="currentColor" d="m512 747.84 228.16 119.936a6.4 6.4 0 0 0 9.28-6.72l-43.52-254.08 184.512-179.904a6.4 6.4 0 0 0-3.52-10.88l-255.104-37.12L517.76 147.904a6.4 6.4 0 0 0-11.52 0L392.192 379.072l-255.104 37.12a6.4 6.4 0 0 0-3.52 10.88L318.08 606.976l-43.584 254.08a6.4 6.4 0 0 0 9.28 6.72z"></path></svg>
        记忆模块
      </h3>
      <div class="feature-grid single">
        <div class="feature-card memory" @click="goToMemoryPractice">
          <div class="feature-bg"></div>
          <div class="feature-icon">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M784.512 230.272v-50.56a32 32 0 1 1 64 0v149.056a32 32 0 0 1-32 32H667.52a32 32 0 1 1 0-64h92.992A320 320 0 1 0 524.8 833.152a320 320 0 0 0 320-320h64a384 384 0 0 1-384 384 384 384 0 0 1-384-384 384 384 0 0 1 643.712-282.88"></path></svg>
          </div>
          <div class="feature-content">
            <span class="feature-name">记忆练习</span>
            <span class="feature-desc">科学记忆曲线复习</span>
          </div>
          <div class="feature-arrow">
            <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M716.8 537.6a12.8 12.8 0 0 1 0 17.92L332.8 940.8a12.8 12.8 0 0 1-17.92-17.92l371.2-371.2-371.2-371.2a12.8 12.8 0 1 1 17.92-17.92z"></path></svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部导航 -->
    <nav class="mobile-nav">
      <div class="nav-item active" @click="goToHome">
        <div class="nav-icon">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M512 512V128h320v384H512zm-192 0H128V128h192v384zm192 384V576h320v320H512zm-192 0V576H128v320h192z"></path></svg>
        </div>
        <span>首页</span>
      </div>
      <div class="nav-item" @click="goToSequential">
        <div class="nav-icon">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M384 96a32 32 0 0 1 64 0v786.752a32 32 0 0 1-54.592 22.656L95.936 608a32 32 0 0 1 0-45.312h.128a32 32 0 0 1 45.184 0L384 805.632z"></path></svg>
        </div>
        <span>刷题</span>
      </div>
      <div class="nav-item" @click="goToWrong">
        <div class="nav-icon">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="M928.99 755.83 574.6 203.25c-12.89-20.16-36.76-32.58-62.6-32.58s-49.71 12.43-62.6 32.58L95.01 755.83c-12.91 20.12-12.9 44.91.01 65.03 12.92 20.12 36.78 32.51 62.59 32.49h708.78c25.82.01 49.68-12.37 62.59-32.49s12.92-44.91.01-65.03"></path></svg>
        </div>
        <span>错题</span>
      </div>
      <div class="nav-item" @click="goToMemoryPractice">
        <div class="nav-icon">
          <svg viewBox="0 0 1024 1024"><path fill="currentColor" d="m512 747.84 228.16 119.936a6.4 6.4 0 0 0 9.28-6.72l-43.52-254.08 184.512-179.904a6.4 6.4 0 0 0-3.52-10.88l-255.104-37.12L517.76 147.904a6.4 6.4 0 0 0-11.52 0L392.192 379.072l-255.104 37.12a6.4 6.4 0 0 0-3.52 10.88L318.08 606.976l-43.584 254.08a6.4 6.4 0 0 0 9.28 6.72z"></path></svg>
        </div>
        <span>记忆</span>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuizStore } from '@/store/quiz'
import axios from 'axios'

const router = useRouter()
const store = useQuizStore()

const statistics = ref({
  total_questions: 0,
  total_answered: 0,
  correct_rate: 0,
  wrong_count: 0
})

const memoryPlan = ref({
  total_records: 0,
  today_review_count: 0,
  tomorrow_review_count: 0,
  next_15_days: []
})

const next15DaysTotal = computed(() => {
  return memoryPlan.value.next_15_days.reduce((sum, item) => sum + item.count, 0)
})

const goToHome = () => router.push('/mobile')
const goToSequential = () => router.push('/mobile/practice/sequential')
const goToRandom = () => router.push('/mobile/practice/random')
const goToWrong = () => router.push('/mobile/practice/wrong')
const goToMemoryPractice = () => router.push('/mobile/memory/practice')
const goToMemoryPlan = () => router.push('/memory/plan')

onMounted(async () => {
  statistics.value = await store.loadStatistics()
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
.mobile-home {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc 0%, #e8f4f8 100%);
  padding-bottom: 80px;
}

/* 顶部标题栏 */
.mobile-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 24px 20px 40px;
  position: relative;
  overflow: hidden;
}

.header-bg {
  position: absolute;
  top: -50%;
  right: -20%;
  width: 200px;
  height: 200px;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
}

.header-content {
  position: relative;
  z-index: 1;
}

.mobile-header h1 {
  font-size: 24px;
  margin: 0 0 4px 0;
  font-weight: 600;
}

.header-subtitle {
  font-size: 13px;
  margin: 0;
  opacity: 0.9;
}

/* 统计卡片 */
.stats-section {
  display: flex;
  gap: 12px;
  padding: 0 16px;
  margin-top: -24px;
  position: relative;
  z-index: 10;
}

.stat-card {
  flex: 1;
  background: white;
  border-radius: 16px;
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.stat-card:active {
  transform: scale(0.98);
}

.stat-card.primary .stat-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card.danger .stat-icon {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
}

.stat-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
}

.stat-icon {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-info {
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1.2;
}

.stat-label {
  font-size: 12px;
  color: #8c8c8c;
  margin-top: 4px;
}

.stat-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, rgba(0,0,0,0.05), transparent);
}

/* 记忆规划数据 */
.memory-section {
  background: white;
  margin: 16px;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-heading {
  display: inline;
  margin: 0;
  font-size: 17px;
  font-weight: 600;
  color: #1a1a1a;
  vertical-align: middle;
}

.heading-icon {
  width: 20px;
  height: 20px;
  color: #667eea;
  vertical-align: middle;
  margin-right: 8px;
}

.view-detail {
  font-size: 13px;
  color: #667eea;
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: color 0.3s;
}

.view-detail:active {
  color: #5a6fd6;
}

.view-detail svg {
  width: 14px;
  height: 14px;
}

.memory-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.memory-item {
  flex: 1;
  text-align: center;
  padding: 8px 4px;
}

.memory-value {
  font-size: 22px;
  font-weight: 700;
  color: #1a1a1a;
  display: block;
}

.memory-value.today {
  color: #667eea;
}

.memory-label {
  font-size: 11px;
  color: #8c8c8c;
  margin-top: 4px;
  display: block;
}

.memory-divider {
  width: 1px;
  height: 32px;
  background: #f0f0f0;
}

/* 功能入口 */
.features-section {
  background: white;
  margin: 0 16px 16px;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

.features-section .section-heading {
  display: block;
  font-size: 17px;
  margin: 0 0 16px;
  color: #1a1a1a;
  font-weight: 600;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.feature-grid.single {
  grid-template-columns: 1fr;
}

.feature-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.feature-card:active {
  transform: scale(0.96);
  background: #f0f2f5;
}

.feature-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}

.feature-card.sequential .feature-bg {
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.feature-card.random .feature-bg {
  background: linear-gradient(90deg, #f093fb, #f5576c);
}

.feature-card.wrong .feature-bg {
  background: linear-gradient(90deg, #fa709a, #fee140);
}

.feature-card.memory .feature-bg {
  background: linear-gradient(90deg, #38ef7d, #11998e);
}

.feature-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.feature-icon svg {
  width: 22px;
  height: 22px;
}

.feature-card.random .feature-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  box-shadow: 0 4px 12px rgba(245, 87, 108, 0.3);
}

.feature-card.wrong .feature-icon {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  box-shadow: 0 4px 12px rgba(250, 112, 154, 0.3);
}

.feature-card.memory .feature-icon {
  background: linear-gradient(135deg, #38ef7d 0%, #11998e 100%);
  box-shadow: 0 4px 12px rgba(56, 239, 125, 0.3);
}

.feature-name {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a1a;
  text-align: center;
}

.feature-desc {
  font-size: 11px;
  color: #8c8c8c;
  text-align: center;
}

.feature-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.feature-arrow {
  color: #c0c0c0;
}

.feature-arrow svg {
  width: 20px;
  height: 20px;
}

.memory-module {
  margin-bottom: 16px;
}

/* 底部导航 */
.mobile-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  display: flex;
  justify-content: space-around;
  padding: 8px 0 calc(8px + env(safe-area-inset-bottom));
  box-shadow: 0 -4px 20px rgba(0,0,0,0.08);
  z-index: 100;
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #8c8c8c;
  font-size: 11px;
  cursor: pointer;
  transition: color 0.3s;
  padding: 4px 0;
}

.nav-item:active {
  color: #667eea;
}

.nav-icon {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2px;
}

.nav-icon svg {
  width: 24px;
  height: 24px;
}

.nav-item.active {
  color: #667eea;
}

.nav-item span {
  font-weight: 500;
}
</style>