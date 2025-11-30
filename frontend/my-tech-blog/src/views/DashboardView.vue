<template>
  <!-- 控制台主容器 -->
  <el-container class="dashboard-container">
    <!-- 移动端遮罩层 -->
    <div
        v-if="windowWidth < 768 && !isCollapse"
        class="sidebar-overlay"
        @click="toggleCollapse"
    ></div>

    <!-- 左侧侧边栏 -->
    <el-aside :width="asideWidth" class="dashboard-aside" :class="{ 'mobile-hidden': windowWidth < 768 && isCollapse }">
      <!-- 侧边栏菜单 -->
      <el-menu
          :default-active="activeMenu"
          class="dashboard-menu"
          :collapse="isCollapse"
          @select="handleMenuSelect"
      >
        <!-- Logo区域 - 收起时显示图标，展开时显示文字 -->
        <div class="logo-wrapper">
          <div v-if="windowWidth < 768" class="logo-text">
            <el-icon :size="28" color="var(--el-color-primary)"><Monitor /></el-icon>
            <h2>管理控制台</h2>
          </div>
          <div v-else class="logo-icon">
            <el-icon :size="32" color="var(--el-color-primary)"><Monitor /></el-icon>
          </div>
        </div>

        <!-- 仪表盘菜单项 -->
        <el-menu-item index="dashboard">
          <el-icon><DataLine /></el-icon>
          <template #title>仪表盘</template>
        </el-menu-item>

        <!-- 个人信息菜单项 -->
        <el-menu-item index="profile">
          <el-icon><User /></el-icon>
          <template #title>个人信息</template>
        </el-menu-item>

        <!-- 流量统计菜单项 -->
        <el-menu-item index="statistics">
          <el-icon><TrendCharts /></el-icon>
          <template #title>流量统计</template>
        </el-menu-item>

        <!-- 文章编辑菜单项 -->
        <el-menu-item index="article">
          <el-icon><Edit /></el-icon>
          <template #title>文章编辑</template>
        </el-menu-item>
      </el-menu>

      <el-button type="primary" @click="handleLogout">退出登录</el-button>

      <!-- 底部工具栏 - 包含主题切换和折叠按钮 -->
      <div class="sidebar-footer" :class="{ 'collapsed': isCollapse && windowWidth >= 768 }">
        <!-- 主题切换开关 -->
        <div class="theme-switch" :title="isDark ? '切换到浅色模式' : '切换到深色模式'">
          <el-switch
              v-model="isDark"
              :active-icon="Moon"
              :inactive-icon="Sunny"
              @change="handleThemeChange"
          />
        </div>

        <!-- 折叠按钮 (仅桌面端显示) -->
        <div v-if="windowWidth >= 768" class="collapse-button" @click="toggleCollapse">
          <el-icon>
            <DArrowLeft v-if="!isCollapse" />
            <DArrowRight v-else />
          </el-icon>
        </div>
      </div>
    </el-aside>

    <!-- 右侧主内容区域 -->
    <el-main class="dashboard-main">
      <!-- 移动端顶部栏 - 包含汉堡菜单按钮 -->
      <div v-if="windowWidth < 768" class="mobile-header">
        <el-button
            :icon="Menu"
            circle
            @click="toggleCollapse"
            size="large"
        />
        <h3>管理控制台</h3>
      </div>

      <!-- 根据选中的菜单动态渲染组件 -->
      <component :is="currentComponent" />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import {
  DataLine,
  User,
  TrendCharts,
  Edit,
  DArrowLeft,
  DArrowRight,
  Monitor,
  Sunny,
  Moon,
  Menu
} from '@element-plus/icons-vue'
import store from "@/store/index.js"
import { useRoute, useRouter } from "vue-router"
import { ElMessage } from "element-plus"

// 导入子面板组件
import DashboardPanel from '@/components/dashboard/DashboardPanel.vue'
import ProfilePanel from '@/components/dashboard/ProfilePanel.vue'
import StatisticsPanel from '@/components/dashboard/StatisticsPanel.vue'
import ArticleEditPanel from '@/components/dashboard/ArticleEditPanel.vue'
import {applyTheme, initTheme, isDark} from "@/utils/theme.js";

const route = useRoute()
const router = useRouter()

/* ========== 响应式数据 ========== */

// 当前激活的菜单项
const activeMenu = ref('')

// 侧边栏是否折叠
const isCollapse = ref(false)

// 窗口宽度
const windowWidth = ref(window.innerWidth)

/* ========== 计算属性 ========== */

// 侧边栏宽度
const asideWidth = computed(() => {
  // 移动端
  if (windowWidth.value < 768) {
    return isCollapse.value ? '0px' : '250px'
  }
  // 桌面端
  return isCollapse.value ? '64px' : '250px'
})

// 当前显示的组件
const currentComponent = computed(() => {
  const componentMap = {
    dashboard: DashboardPanel,
    profile: ProfilePanel,
    statistics: StatisticsPanel,
    article: ArticleEditPanel
  }

  // route query path
  const path = route.query?.path || ''

  // 判断是否可以直接使用path
  if (!activeMenu.value && path && componentMap[path]) {
    activeMenu.value = path
    return componentMap[path]
  }

  // 同步路由查询参数
  if (route.query.path !== activeMenu.value) {
    router.replace({
      query: { ...route.query, path: activeMenu.value || 'dashboard' }
    })
  }

  return componentMap[activeMenu.value] || DashboardPanel
})

/* ========== 方法 ========== */

/**
 * 处理菜单选择
 * @param {string} index - 选中的菜单索引
 */
const handleMenuSelect = (index) => {
  activeMenu.value = index
  // 移动端选择菜单后自动收起侧边栏
  if (windowWidth.value < 768) {
    isCollapse.value = true
  }
}

/**
 * 切换侧边栏折叠状态
 */
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

/**
 * 处理窗口大小变化
 */
const handleResize = () => {
  windowWidth.value = window.innerWidth
  // 移动端自动折叠
  if (windowWidth.value < 768) {
    isCollapse.value = true
  }
}

/**
 * 处理主题切换
 * @param {boolean} value - 是否为暗黑模式
 */
const handleThemeChange = (value) => {
  // 保存到 localStorage
  localStorage.setItem('my_tech_blog_theme', value ? 'dark' : 'light')
  // 应用主题到 html 元素
  applyTheme(value)
}

const handleLogout = () => {
  store.dispatch('auth/clearAuth')
  router.push('/login')
}

/* ========== 生命周期 ========== */

// 组件挂载时添加窗口大小监听
onMounted(async () => {
  initTheme()

  window.addEventListener('resize', handleResize)
  // 初始化检查是否需要折叠
  if (windowWidth.value < 768) {
    isCollapse.value = true
  }

  // 是否登录
  await store.dispatch('auth/refreshAuthState')
  if (!store.getters['auth/isLogin']) {
    ElMessage.error('未登录！')
    return await router.push('login')
  }
})

// 组件卸载时移除监听
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* ========== 主容器样式 ========== */
.dashboard-container {
  height: 100vh;
  width: 100%;
  overflow: hidden;
  position: relative;
}

/* ========== 侧边栏样式 ========== */
.dashboard-aside {
  height: 100vh;
  background-color: var(--el-bg-color);
  border-right: 1px solid var(--el-border-color);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

/* 菜单样式 */
.dashboard-menu {
  flex: 1;
  border-right: none;
  background-color: var(--el-bg-color);
  overflow-y: auto;
}

/* Logo区域样式 - 支持文字和图标切换 */
.logo-wrapper {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--el-border-color);
  margin-bottom: 10px;
  flex-shrink: 0;
}

.logo-text {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 20px;
}

.logo-text h2 {
  font-size: 18px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0;
  white-space: nowrap;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 侧边栏底部工具栏 */
.sidebar-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 20px;
  border-top: 1px solid var(--el-border-color);
  flex-shrink: 0;
  transition: all 0.3s ease;
}

/* 侧边栏收起时，按钮垂直排列 */
.sidebar-footer.collapsed {
  flex-direction: column;
  gap: 16px;
  padding: 16px 0;
}

/* 折叠按钮样式 */
.collapse-button {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--el-fill-color);
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.collapse-button:hover {
  background-color: var(--el-color-primary-light-5);
  color: var(--el-color-primary);
}

/* ========== 主内容区域样式 ========== */
.dashboard-main {
  height: 100vh;
  overflow-y: auto;
  background-color: var(--el-bg-color-page);
  padding: 20px;
}

/* 移动端顶部栏 */
.mobile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--el-border-color);
}

.mobile-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0;
}

/* 移动端遮罩层 */
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
  transition: opacity 0.3s ease;
}

/* ========== 移动端适配 ========== */
@media screen and (max-width: 768px) {
  /* 移动端侧边栏固定定位 */
  .dashboard-aside {
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
  }

  /* 移动端隐藏侧边栏 */
  .dashboard-aside.mobile-hidden {
    transform: translateX(-100%);
  }

  .dashboard-main {
    padding: 15px;
  }

  .logo-text h2 {
    font-size: 16px;
  }

  /* 移动端侧边栏始终展开显示 */
  .dashboard-menu {
    width: 250px;
  }

  /* 移动端底部工具栏调整 */
  .sidebar-footer {
    flex-direction: row;
    gap: 16px;
  }
}

@media screen and (max-width: 480px) {
  .dashboard-main {
    padding: 10px;
  }

  .mobile-header {
    margin-bottom: 15px;
  }

  .mobile-header h3 {
    font-size: 16px;
  }
}
</style>
