<!-- 热度排行榜组件 - 展示前10篇热门文章 -->
<template>
  <el-card class="hot-rank-card" :body-style="{ padding: '20px' }">
    <!-- 排行榜标题 -->
    <template #header>
      <div class="card-header">
        <el-icon class="header-icon"><TrendCharts /></el-icon>
        <span class="header-title">热度排行榜</span>
      </div>
    </template>

    <!-- 排行榜列表 -->
    <div class="rank-list">
      <div
        v-for="(article, index) in hotArticles"
        :key="article.id"
        class="rank-item"
        :class="{ 'top-three': index < 3 }"
        @click="handleArticleClick(article.id)"
      >
        <!-- 排名序号 -->
        <div class="rank-number" :class="`rank-${index + 1}`">
          {{ index + 1 }}
        </div>

        <!-- 文章信息 -->
        <div class="article-info">
          <div class="article-title">{{ article.title }}</div>
          <div class="article-stats">
            <span class="stat-item">
              <el-icon><View /></el-icon>
              {{ article.views }}
            </span>
            <span class="stat-item">
              <el-icon><Star /></el-icon>
              {{ article.stars }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 暂无数据提示 -->
    <el-empty
      v-if="hotArticles.length === 0"
      description="暂无热门文章"
      :image-size="80"
    />
  </el-card>
</template>

<script setup>
import { TrendCharts, View, Star } from '@element-plus/icons-vue'

// ==================== Props ====================
defineProps({
  hotArticles: {
    type: Array,
    default: () => []
  }
})

// ==================== Emits ====================
const emit = defineEmits(['article-click'])

// ==================== 事件处理 ====================
/**
 * 点击文章项
 */
const handleArticleClick = (articleId) => {
  emit('article-click', articleId)
}
</script>

<style scoped>
/* ==================== 卡片容器 ==================== */
.hot-rank-card {
  position: sticky;
  top: 20px;
  background-color: var(--el-bg-color);
}

/* ==================== 卡片头部 ==================== */
.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 16px;
  color: var(--el-text-color-primary);
}

.header-icon {
  color: var(--el-color-primary);
  font-size: 18px;
}

.header-title {
  font-weight: 600;
}

/* ==================== 排行榜列表 ==================== */
.rank-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rank-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: var(--el-fill-color-blank);
}

.rank-item:hover {
  background-color: var(--el-fill-color-light);
  transform: translateX(4px);
}

/* ==================== 排名序号 ==================== */
.rank-number {
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  font-weight: 700;
  font-size: 14px;
  background-color: var(--el-fill-color);
  color: var(--el-text-color-regular);
}

/* 前三名特殊样式 */
.top-three .rank-number {
  color: #fff;
}

.rank-1 {
  background: linear-gradient(135deg, #FFD700, #FFA500) !important;
}

.rank-2 {
  background: linear-gradient(135deg, #C0C0C0, #A9A9A9) !important;
}

.rank-3 {
  background: linear-gradient(135deg, #CD7F32, #8B4513) !important;
}

/* ==================== 文章信息 ==================== */
.article-info {
  flex: 1;
  min-width: 0; /* 防止文本溢出 */
}

.article-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  line-height: 1.4;
  margin-bottom: 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 最多显示2行 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.article-stats {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* ==================== 响应式适配 ==================== */
/* 平板适配 */
@media (max-width: 1024px) {
  .hot-rank-card {
    position: static;
  }
}

/* 手机适配 */
@media (max-width: 768px) {
  .rank-item {
    padding: 10px;
    gap: 10px;
  }

  .rank-number {
    width: 24px;
    height: 24px;
    font-size: 13px;
  }

  .article-title {
    font-size: 13px;
  }

  .article-stats {
    font-size: 11px;
    gap: 10px;
  }
}
</style>
