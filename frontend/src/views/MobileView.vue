<template>
  <div class="mobile-view-container">
    <div class="mobile-frame">
      <div class="mobile-header">
        <div class="mobile-notch"></div>
        <div class="mobile-status-bar">
          <span class="time">9:41</span>
          <div class="status-icons">
            <span>📶</span>
            <span>🔋</span>
          </div>
        </div>
      </div>
      
      <div class="mobile-screen">
        <div class="mobile-app-header">
          <h2 class="app-title">📚 学习助手</h2>
        </div>
        
        <div class="mobile-menu">
          <div class="menu-section">
            <h3 class="section-title">刷题练习</h3>
            <div class="menu-grid">
              <div class="menu-item" @click="$router.push('/mobile/practice/sequential')">
                <div class="menu-icon sequential-icon">
                  <el-icon><Sort /></el-icon>
                </div>
                <span class="menu-label">顺序刷题</span>
              </div>
              <div class="menu-item" @click="$router.push('/mobile/practice/random')">
                <div class="menu-icon random-icon">
                  <el-icon><RefreshRight /></el-icon>
                </div>
                <span class="menu-label">随机出题</span>
              </div>
              <div class="menu-item" @click="$router.push('/mobile/practice/wrong')">
                <div class="menu-icon wrong-icon">
                  <el-icon><WarnTriangleFilled /></el-icon>
                </div>
                <span class="menu-label">错题练习</span>
              </div>
            </div>
          </div>
          
          <div class="menu-section">
            <h3 class="section-title">记忆模块</h3>
            <div class="menu-grid">
              <div class="menu-item" @click="$router.push('/mobile/memory/practice')">
                <div class="menu-icon memory-icon">
                  <el-icon><Star /></el-icon>
                </div>
                <span class="menu-label">记忆练习</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mobile-footer">
          <div class="home-btn" @click="$router.push('/mobile')">
            <el-icon><HomeFilled /></el-icon>
          </div>
        </div>
      </div>
      
      <div class="mobile-home-indicator"></div>
    </div>
  </div>
</template>

<script setup>
import { Sort, RefreshRight, WarnTriangleFilled, Star, HomeFilled } from '@element-plus/icons-vue'
</script>

<style scoped>
.mobile-view-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.mobile-frame {
  width: 375px;
  height: 812px;
  background: #1c1c1e;
  border-radius: 40px;
  padding: 20px;
  box-sizing: border-box;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  position: relative;
}

.mobile-header {
  text-align: center;
  margin-bottom: 10px;
}

.mobile-notch {
  width: 150px;
  height: 30px;
  background: #1c1c1e;
  border-radius: 0 0 20px 20px;
  margin: 0 auto -10px;
  position: relative;
  z-index: 10;
}

.mobile-status-bar {
  display: flex;
  justify-content: space-between;
  padding: 0 20px;
  color: #fff;
  font-size: 14px;
}

.status-icons {
  display: flex;
  gap: 8px;
}

.mobile-screen {
  background: linear-gradient(180deg, #f5f5f7 0%, #e8e8ed 100%);
  border-radius: 30px;
  height: calc(100% - 60px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.mobile-app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  text-align: center;
}

.app-title {
  color: #fff;
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.mobile-menu {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.menu-section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 14px;
  color: #8e8e93;
  margin-bottom: 15px;
  padding-left: 10px;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.menu-item {
  background: #fff;
  border-radius: 16px;
  padding: 20px 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.menu-item:active {
  transform: scale(0.95);
  background: #f0f0f0;
}

.menu-icon {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #fff;
}

.sequential-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.random-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.wrong-icon {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.memory-icon {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: #666 !important;
}

.menu-label {
  font-size: 12px;
  color: #333;
  font-weight: 500;
}

.mobile-footer {
  background: #fff;
  padding: 15px;
  border-top: 1px solid #e0e0e0;
}

.home-btn {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  color: #fff;
  font-size: 20px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.mobile-home-indicator {
  width: 134px;
  height: 6px;
  background: #3c3c3c;
  border-radius: 3px;
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
}
</style>