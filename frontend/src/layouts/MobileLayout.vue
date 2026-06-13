<template>
  <div class="mobile-app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useQuizStore } from '@/store/quiz'

const store = useQuizStore()

onMounted(async () => {
  await store.initDatabase()
})
</script>

<style scoped>
.mobile-app {
  width: 100%;
  min-height: 100vh;
  background: #f5f5f5;
}
</style>