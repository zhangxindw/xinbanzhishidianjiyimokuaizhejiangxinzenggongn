import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/HomeView.vue')
  },
  // ========== 手机端模块路由 ==========
  {
    path: '/mobile',
    name: 'MobileHome',
    component: () => import('@/views/mobile/MobileHomeView.vue'),
    meta: { mobile: true }
  },
  {
    path: '/mobile/practice/:mode',
    name: 'MobilePractice',
    component: () => import('@/views/mobile/MobilePracticeView.vue'),
    meta: { mobile: true }
  },
  {
    path: '/mobile/memory/practice',
    name: 'MobileMemoryPractice',
    component: () => import('@/views/mobile/MobileMemoryPracticeView.vue'),
    meta: { mobile: true }
  },
  // ========== 电脑端原有路由 ==========
  {
    path: '/questions',
    name: 'Questions',
    component: () => import('@/views/QuestionsView.vue')
  },
  {
    path: '/questions/new',
    name: 'QuestionCreate',
    component: () => import('@/views/QuestionEditView.vue')
  },
  {
    path: '/questions/:id/edit',
    name: 'QuestionEdit',
    component: () => import('@/views/QuestionEditView.vue')
  },
  {
    path: '/import',
    name: 'Import',
    component: () => import('@/views/ImportView.vue')
  },
  {
    path: '/chapters',
    name: 'Chapters',
    component: () => import('@/views/ChaptersView.vue')
  },
  {
    path: '/question-types',
    name: 'QuestionTypes',
    component: () => import('@/views/QuestionTypesView.vue')
  },
  {
    path: '/practice/memorize',
    name: 'PracticeMemorize',
    component: () => import('@/views/PracticeView.vue'),
    meta: { practiceMode: 'memorize' }
  },
  {
    path: '/practice/sequential',
    name: 'PracticeSequential',
    component: () => import('@/views/PracticeView.vue'),
    meta: { practiceMode: 'sequential' }
  },
  {
    path: '/practice/random',
    name: 'PracticeRandom',
    component: () => import('@/views/PracticeView.vue'),
    meta: { practiceMode: 'random' }
  },
  {
    path: '/practice/wrong',
    name: 'PracticeWrong',
    component: () => import('@/views/PracticeView.vue'),
    meta: { practiceMode: 'wrong' }
  },
  {
    path: '/wrong-questions',
    name: 'WrongQuestions',
    component: () => import('@/views/WrongQuestionsView.vue')
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('@/views/FavoritesView.vue')
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: () => import('@/views/StatisticsView.vue')
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/SettingsView.vue')
  },
  // ========== 知识点记忆模块路由 ==========
  {
    path: '/knowledge-points',
    name: 'KnowledgePoints',
    component: () => import('@/views/KnowledgePointsView.vue')
  },
  {
    path: '/memory/practice',
    name: 'MemoryPractice',
    component: () => import('@/views/MemoryPracticeView.vue')
  },
  {
    path: '/memory/plan',
    name: 'MemoryPlan',
    component: () => import('@/views/MemoryPlanView.vue')
  },
  {
    path: '/memory/dictation',
    name: 'MemoryDictation',
    component: () => import('@/views/DictationPracticeView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
