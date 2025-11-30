import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      name: 'Login',
      path: '/login',
      component: () => import('@/views/LoginView.vue'),
      meta: {
        title: '登录',
        keepAlive: true,
      }
    },
    {
      name: 'Dashboard',
      path: '/dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: {
        title: '控制台',
        keepAlive: true,
      },
    },
    {
      name: 'Home',
      path: '/',
      component: () => import('@/views/ArticleListView.vue'),
      meta: {
        title: '文章列表',
        keepAlive: true,
      }
    },
    {
      name: 'Article Detail',
      path: '/article',
      component: () => import('@/views/ArticleDetailView.vue'),
      meta: {
        title: '文章详细',
        keepAlive: true,
      }
    }
  ],
})

export default router
