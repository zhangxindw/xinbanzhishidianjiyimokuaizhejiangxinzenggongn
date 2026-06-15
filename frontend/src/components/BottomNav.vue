<template>
  <nav class="bottom-nav">
    <div 
      v-for="item in navItems" 
      :key="item.key"
      class="nav-item"
      :class="{ active: currentKey === item.key }"
      @click="handleClick(item)"
    >
      <div class="icon-container">
        <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path :d="item.path"></path>
        </svg>
      </div>
      <span class="nav-label">{{ item.label }}</span>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const navItems = [
  { key: 'home', label: '首页', path: 'M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z M9 22 9 12 15 12 15 22', url: '/mobile' },
  { key: 'practice', label: '刷题', path: 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z', url: '/mobile/practice/sequential' },
  { key: 'wrong', label: '错题', path: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z', url: '/mobile/practice/wrong' },
  { key: 'memory', label: '记忆', path: 'M12 4.5a2.5 2.5 0 0 0-4.96-.46 2.5 2.5 0 0 0-1.98 3 2.5 2.5 0 0 0 .42 4.94 2.5 2.5 0 0 0 3.77.66 2.5 2.5 0 0 0 4.96.46 2.5 2.5 0 0 0 1.98-3 2.5 2.5 0 0 0-.42-4.94 2.5 2.5 0 0 0-3.77-.66z M12 4.5v15a2.5 2.5 0 0 0 4.96.46 2.5 2.5 0 0 0 1.98-3 2.5 2.5 0 0 0-.42-4.94 2.5 2.5 0 0 0-3.77-.66 2.5 2.5 0 0 0-4.96-.46V4.5', url: '/mobile/memory/practice' }
]

const currentKey = ref('home')

const updateCurrentKey = () => {
  const path = route.path
  if (path.startsWith('/mobile/practice/sequential') || path.startsWith('/mobile/practice/random')) {
    currentKey.value = 'practice'
  } else if (path.startsWith('/mobile/practice/wrong')) {
    currentKey.value = 'wrong'
  } else if (path.startsWith('/mobile/memory')) {
    currentKey.value = 'memory'
  } else {
    currentKey.value = 'home'
  }
}

const handleClick = (item) => {
  if (currentKey.value !== item.key) {
    router.push(item.url)
  }
}

onMounted(() => {
  updateCurrentKey()
  router.afterEach(updateCurrentKey)
})

onUnmounted(() => {
  router.afterEach(() => {})
})
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding-bottom: env(safe-area-inset-bottom);
  box-shadow: 0 -1px 6px rgba(0, 0, 0, 0.04);
  z-index: 999;
  border-top: 1px solid #f0f0f0;
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #999999;
}

.nav-item.active {
  color: #667eea;
}

.icon-container {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
}

.nav-icon {
  width: 22px;
  height: 22px;
  transition: all 0.2s ease;
}

.nav-item.active .nav-icon {
  transform: scale(1.1);
}

.nav-label {
  font-size: 10px;
  font-weight: 500;
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: calc(6px + env(safe-area-inset-bottom));
  width: 20px;
  height: 3px;
  background: #667eea;
  border-radius: 2px;
}
</style>