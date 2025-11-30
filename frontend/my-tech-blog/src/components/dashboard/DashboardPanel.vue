<template>
  <!-- 仪表盘面板 -->
  <div class="dashboard-panel">
    <!-- 面板标题 -->
    <div class="panel-header">
      <h2>仪表盘</h2>
      <p>欢迎回来，管理员</p>
    </div>

    <!-- 统计卡片区域 -->
    <el-row :gutter="20" class="stats-row">
      <!-- 文章总数卡片 -->
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#409EFF">
              <Document />
            </el-icon>
            <div class="stat-info">
              <span class="stat-label">文章总数</span>
              <span class="stat-value">{{ stats.totalArticles }}</span>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 总访问量卡片 -->
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#67C23A">
              <View />
            </el-icon>
            <div class="stat-info">
              <span class="stat-label">总访问量</span>
              <span class="stat-value">{{ stats.totalViews }}</span>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 评论总数卡片 -->
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#E6A23C">
              <ChatDotRound />
            </el-icon>
            <div class="stat-info">
              <span class="stat-label">评论总数</span>
              <span class="stat-value">{{ stats.totalComments }}</span>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 点赞总数卡片 -->
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#F56C6C">
              <Star />
            </el-icon>
            <div class="stat-info">
              <span class="stat-label">点赞总数</span>
              <span class="stat-value">{{ stats.totalStars }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近文章列表 -->
    <el-card class="recent-articles" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>最近文章</span>
        </div>
      </template>
      <el-table v-if="recentArticles.length > 0" :data="recentArticles" style="width: 100%">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="category" label="分类">
          <template #default="{ row }">
            <el-tag v-if="row.category">{{ row.category }}</el-tag>
            <el-tag v-else type="warning">暂无</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="tags" label="标签">
          <template #default="{ row }">
            <el-tag v-for="(tag, idx) in row.tags" :key="idx">
              {{ tag }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="views" label="浏览量" />
        <el-table-column prop="stars" label="点赞数" />
        <el-table-column prop="published_time" label="发布时间" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="text" size="small" @click="handleView(row)">
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty
          v-else
          description="暂无文章"
          class="empty-state"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  Document,
  View,
  ChatDotRound,
  Star,
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import {recentApi, statisticsApi} from "@/api/posts/index.js";

/* ========== 响应式数据 ========== */

// 统计数据
const stats = ref({
  totalArticles: 0,
  totalViews: 0,
  totalComments: 0,
  totalStars: 0
})

// 最近文章列表
const recentArticles = ref([])

/* ========== 方法 ========== */

/**
 * 加载仪表盘数据
 */
const loadDashboardData = async () => {
  try {
    // 统计数据
    const response = await statisticsApi()
    if (response.code === 200) {
      stats.value = {
        totalArticles: response.data.total,
        totalViews: response.data.views,
        totalComments: response.data.comments,
        totalStars: response.data.stars
      }
    } else {
      ElMessage.error(response.msg)
    }
  } catch (e) {
    console.error('statisticsApi 异常', e)
    ElMessage.error('获取统计失败')
  }

  try {
    // 最近文章
    const response = await recentApi()
    if (response.code === 200) {
      recentArticles.value = response.data.recentArticles
    } else {
      ElMessage.error(response.msg)
    }
  } catch (e) {
    console.error('recentApi 异常', e)
    ElMessage.error('获取最近文章失败')
  }
}

/**
 * 查看文章
 * @param {Object} row - 文章数据
 */
const handleView = (row) => {
  ElMessage.info(`查看文章: ${row.title}`)
  // TODO: 实现编辑逻辑
}

/* ========== 生命周期 ========== */

// 组件挂载时加载数据
onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
/* ========== 面板容器样式 ========== */
.dashboard-panel {
  width: 100%;
}

/* ========== 面板标题样式 ========== */
.panel-header {
  margin-bottom: 24px;
}

.panel-header h2 {
  font-size: 28px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0 0 8px 0;
}

.panel-header p {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
}

/* ========== 统计卡片样式 ========== */
.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 40px;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

/* ========== 快捷操作样式 ========== */

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

/* ========== 最近文章样式 ========== */
.recent-articles {
  margin-bottom: 20px;
}

/* ========== 移动端适配 ========== */
@media screen and (max-width: 768px) {
  .panel-header h2 {
    font-size: 24px;
  }

  .stat-value {
    font-size: 20px;
  }
}

@media screen and (max-width: 480px) {
  .panel-header h2 {
    font-size: 20px;
  }

  .stat-icon {
    font-size: 32px;
  }

  .stat-value {
    font-size: 18px;
  }
}
</style>
