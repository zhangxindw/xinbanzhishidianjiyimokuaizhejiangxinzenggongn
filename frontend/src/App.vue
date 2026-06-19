<template>
  <!-- 手机端布局 -->
  <MobileLayout v-if="$route.meta.mobile" />
  
  <!-- 电脑端布局 -->
  <div v-else class="app-container" :class="eyeProtectionClass">
    <div class="main-layout">
      <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
        <div class="sidebar-logo">
          <h1 v-if="!sidebarCollapsed">📚 在线题库</h1>
          <span v-else class="sidebar-logo-icon">📚</span>
        </div>
        <ul class="sidebar-menu">
          <li class="sidebar-menu-item" :class="{ active: $route.path === '/home' }" @click="$router.push('/home')">
            <el-icon><HomeFilled /></el-icon>
            <span v-if="!sidebarCollapsed">首页</span>
          </li>
          <li class="sidebar-menu-item" :class="{ active: $route.path === '/questions' }" @click="$router.push('/questions')">
            <el-icon><Document /></el-icon>
            <span v-if="!sidebarCollapsed">题库管理</span>
          </li>
          <li class="sidebar-menu-item" :class="{ active: $route.path === '/knowledge-points' }" @click="$router.push('/knowledge-points')">
            <el-icon><Document /></el-icon>
            <span v-if="!sidebarCollapsed">知识点</span>
          </li>
          <li class="sidebar-menu-item" :class="{ active: $route.path === '/import' }" @click="$router.push('/import')">
            <el-icon><Upload /></el-icon>
            <span v-if="!sidebarCollapsed">Excel导入</span>
          </li>
          <li class="sidebar-menu-item" :class="{ active: $route.path === '/chapters' }" @click="$router.push('/chapters')">
            <el-icon><Folder /></el-icon>
            <span v-if="!sidebarCollapsed">章节管理</span>
          </li>
          <li class="sidebar-menu-item" :class="{ active: $route.path === '/question-types' }" @click="$router.push('/question-types')">
            <el-icon><Collection /></el-icon>
            <span v-if="!sidebarCollapsed">题型管理</span>
          </li>
          <li class="sidebar-menu-item" :class="{ active: $route.path.includes('/practice') && !$route.path.includes('/mobile') }" @click="showPracticeMenu = !showPracticeMenu">
            <el-icon><Reading /></el-icon>
            <span v-if="!sidebarCollapsed">刷题练习</span>
            <el-icon v-if="!sidebarCollapsed"><ArrowDown v-if="!showPracticeMenu" /><ArrowUp v-else /></el-icon>
          </li>
          <li v-if="showPracticeMenu && !sidebarCollapsed" class="sidebar-submenu">
            <div class="sidebar-menu-item" @click="$router.push('/practice/memorize')">
              <el-icon><Memo /></el-icon>
              背题模式
            </div>
            <div class="sidebar-menu-item" @click="$router.push('/practice/sequential')">
              <el-icon><Sort /></el-icon>
              顺序刷题
            </div>
            <div class="sidebar-menu-item" @click="$router.push('/practice/random')">
              <el-icon><RefreshRight /></el-icon>
              随机出题
            </div>
            <div class="sidebar-menu-item" @click="$router.push('/practice/wrong')">
              <el-icon><WarnTriangleFilled /></el-icon>
              错题练习
            </div>
            <div class="sidebar-menu-item" @click="$router.push('/practice/crazy')">
              <el-icon><Lightning /></el-icon>
              疯狂刷题
            </div>
            <div class="sidebar-menu-item" @click="$router.push('/practice/memory')">
              <el-icon><Memo /></el-icon>
              记忆刷题
            </div>
          </li>
          <li class="sidebar-menu-item" :class="{ active: $route.path.includes('/memory') && !$route.path.includes('/mobile') }" @click="showMemoryMenu = !showMemoryMenu">
            <el-icon><Star /></el-icon>
            <span v-if="!sidebarCollapsed">记忆模块</span>
            <el-icon v-if="!sidebarCollapsed"><ArrowDown v-if="!showMemoryMenu" /><ArrowUp v-else /></el-icon>
          </li>
          <li v-if="showMemoryMenu && !sidebarCollapsed" class="sidebar-submenu">
            <div class="sidebar-menu-item" @click="$router.push('/knowledge-points')">
              <el-icon><Document /></el-icon>
              知识点管理
            </div>
            <div class="sidebar-menu-item" @click="$router.push('/memory/practice')">
              <el-icon><RefreshRight /></el-icon>
              记忆练习
            </div>
            <div class="sidebar-menu-item" @click="$router.push('/memory/plan')">
              <el-icon><Calendar /></el-icon>
              记忆规划
            </div>
            <div class="sidebar-menu-item" @click="$router.push('/memory/practice/plan')">
              <el-icon><Collection /></el-icon>
              刷题规划
            </div>
            <div class="sidebar-menu-item" @click="$router.push('/memory/dictation')">
              <el-icon><EditPen /></el-icon>
              默写练习
            </div>
          </li>
          <li class="sidebar-menu-item" :class="{ active: $route.path.includes('distinguish') }" @click="showDistinguishMenu = !showDistinguishMenu">
            <el-icon><Warning /></el-icon>
            <span v-if="!sidebarCollapsed">辨析判断</span>
            <el-icon v-if="!sidebarCollapsed"><ArrowDown v-if="!showDistinguishMenu" /><ArrowUp v-else /></el-icon>
          </li>
          <li v-if="showDistinguishMenu && !sidebarCollapsed" class="sidebar-submenu">
            <div class="sidebar-menu-item" @click="$router.push('/distinguish/management')">
              <el-icon><List /></el-icon>
              辨析题管理
            </div>
            <div class="sidebar-menu-item" @click="$router.push('/distinguish/plan')">
              <el-icon><Calendar /></el-icon>
              辨析规划
            </div>
            <div class="sidebar-menu-item" @click="$router.push('/distinguish/memory')">
              <el-icon><RefreshRight /></el-icon>
              辨析记忆
            </div>
          </li>
          <li class="sidebar-menu-item" :class="{ active: $route.path === '/wrong-questions' }" @click="$router.push('/wrong-questions')">
            <el-icon><CircleClose /></el-icon>
            <span v-if="!sidebarCollapsed">错题本</span>
          </li>
          <li class="sidebar-menu-item" :class="{ active: $route.path === '/favorites' }" @click="$router.push('/favorites')">
            <el-icon><Star /></el-icon>
            <span v-if="!sidebarCollapsed">收藏夹</span>
          </li>
          <li class="sidebar-menu-item" :class="{ active: $route.path === '/statistics' }" @click="$router.push('/statistics')">
            <el-icon><DataAnalysis /></el-icon>
            <span v-if="!sidebarCollapsed">数据统计</span>
          </li>
          <li class="sidebar-menu-item" :class="{ active: $route.path === '/settings' }" @click="$router.push('/settings')">
            <el-icon><Setting /></el-icon>
            <span v-if="!sidebarCollapsed">设置</span>
          </li>
          <li class="sidebar-menu-item mobile-entry" :class="{ active: $route.path.startsWith('/mobile') }" @click="$router.push('/mobile')">
            <el-icon><Iphone /></el-icon>
            <span v-if="!sidebarCollapsed">手机端</span>
          </li>
        </ul>
        <div class="sidebar-toggle" @click="sidebarCollapsed = !sidebarCollapsed">
          <el-icon><DArrowLeft v-if="!sidebarCollapsed" /><DArrowRight v-else /></el-icon>
        </div>
      </aside>
      <main class="main-content" :class="{ expanded: sidebarCollapsed }">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuizStore } from '@/store/quiz'
import MobileLayout from '@/layouts/MobileLayout.vue'
import { 
  HomeFilled, Document, Upload, Folder, Collection, Reading, Memo, 
  Sort, RefreshRight, WarnTriangleFilled, CircleClose, Star, 
  DataAnalysis, Setting, DArrowLeft, DArrowRight, ArrowDown, ArrowUp,
  Calendar, EditPen, Iphone, Warning, List, Lightning
} from '@element-plus/icons-vue'

const store = useQuizStore()
const showPracticeMenu = ref(false)
const showMemoryMenu = ref(false)
const showDistinguishMenu = ref(false)
const sidebarCollapsed = ref(false)

const eyeProtectionClass = computed(() => {
  const mode = store.preferences.eye_protection_mode
  if (mode === 'none') return ''
  return `eye-protection-${mode}`
})

onMounted(async () => {
  await store.initDatabase()
})
</script>

<style scoped>
.sidebar-submenu {
  list-style: none;
  padding-left: 20px;
}

.sidebar-submenu .sidebar-menu-item {
  font-size: 14px;
  padding: 10px 20px;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar.collapsed .sidebar-logo h1 {
  display: none;
}

.sidebar.collapsed .sidebar-logo-icon {
  font-size: 24px;
}

.sidebar.collapsed .sidebar-menu-item {
  justify-content: center;
  padding: 15px 5px;
}

.sidebar.collapsed .sidebar-menu-item span {
  display: none;
}

.sidebar.collapsed .sidebar-menu-item .el-icon {
  font-size: 20px;
}

.sidebar-toggle {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 10;
}

.sidebar-toggle:hover {
  opacity: 0.9;
}

.sidebar-toggle .el-icon {
  color: white;
  font-size: 18px;
}

.mobile-entry {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin-top: 10px;
  border-radius: 8px;
}

.mobile-entry:hover {
  opacity: 0.9;
}

.mobile-entry .el-icon {
  color: white;
}
</style>