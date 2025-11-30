<!-- 文章卡片组件 - 展示单篇文章的摘要信息 -->
<template>
  <el-card class="article-card" :body-style="{ padding: '24px' }" shadow="hover">
    <!-- 文章头部：标题和分类 -->
    <div class="card-header">
      <h3 class="article-title">{{ article.title }}</h3>
      <el-tag v-if="article.category" type="primary" size="small">
        {{ article.category }}
      </el-tag>
    </div>

    <!-- 文章摘要 -->
    <p class="article-excerpt">{{ article.excerpt }}</p>

    <!-- 文章标签 -->
    <div class="article-tags" v-if="article.tags && article.tags.length > 0">
      <el-tag
        v-for="tag in article.tags"
        size="small"
        effect="plain"
        class="tag-item"
      >
        {{ tag }}
      </el-tag>
    </div>

    <!-- 文章底部：统计信息和发布时间 -->
    <div class="card-footer">
      <div class="article-stats">
        <!-- 浏览量 -->
        <span class="stat-item">
          <el-icon><View /></el-icon>
          <span class="stat-value">{{ article.views }}</span>
        </span>
        <!-- 点赞数 -->
        <span class="stat-item">
          <el-icon><Star /></el-icon>
          <span class="stat-value">{{ article.stars }}</span>
        </span>
      </div>
      <!-- 发布时间 -->
      <div class="article-time">
        <el-icon><Clock /></el-icon>
        <span>{{ formatTime(article.published_time) }}</span>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { View, Star, Clock } from '@element-plus/icons-vue'

// ==================== Props ====================
defineProps({
  article: {
    type: Object,
    required: true
  }
})

// ==================== 工具方法 ====================
/**
 * 格式化时间显示
 * @param {string} time - ISO格式的时间字符串
 * @returns {string} 格式化后的时间字符串
 */
const formatTime = (time) => {
  if (!time) return ''

  const date = new Date(time)
  const now = new Date()
  const diff = now - date

  // 1分钟内
  if (diff < 60000) {
    return '刚刚'
  }
  // 1小时内
  if (diff < 3600000) {
    return `${Math.floor(diff / 60000)}分钟前`
  }
  // 24小时内
  if (diff < 86400000) {
    return `${Math.floor(diff / 3600000)}小时前`
  }
  // 7天内
  if (diff < 604800000) {
    return `${Math.floor(diff / 86400000)}天前`
  }

  // 超过7天显示具体日期
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}
</script>

<style scoped>
/* ==================== 卡片容器 ==================== */
.article-card {
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: var(--el-bg-color);
}

.article-card:hover {
  transform: translateY(-4px);
}

/* ==================== 卡片头部 ==================== */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.article-title {
  flex: 1;
  font-size: 20px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 最多显示2行 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ==================== 文章摘要 ==================== */
.article-excerpt {
  font-size: 14px;
  color: var(--el-text-color-regular);
  line-height: 1.6;
  margin: 0 0 16px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3; /* 最多显示3行 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ==================== 文章标签 ==================== */
.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.tag-item {
  cursor: pointer;
}

/* ==================== 卡片底部 ==================== */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid var(--el-border-color-lighter);
}

.article-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.stat-value {
  font-weight: 500;
}

.article-time {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

/* ==================== 响应式适配 ==================== */
/* 手机适配 (< 768px) */
@media (max-width: 768px) {
  .article-card :deep(.el-card__body) {
    padding: 16px !important;
  }

  .article-title {
    font-size: 18px;
  }

  .article-excerpt {
    font-size: 13px;
    -webkit-line-clamp: 2; /* 手机端只显示2行 */
  }

  .card-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .article-stats {
    gap: 16px;
  }
}
</style>
