<template>
  <div class="article-detail-view">
    <div class="content-container">
      <!-- 返回按钮 -->
      <div class="back-button">
        <el-button @click="goBack">
          <template #icon>
            <el-icon>
              <ArrowLeft/>
            </el-icon>
          </template>
          返回列表
        </el-button>
      </div>

      <!-- 文章内容卡片 -->
      <el-card v-if="article" class="article-card" v-loading="loading">
        <!-- 文章头部信息 -->
        <div class="article-header">
          <h1 class="article-title">{{ article.title }}</h1>

          <!-- 文章元信息 -->
          <div class="article-meta">
            <el-tag v-if="article.category" type="primary">
              {{ article.category }}
            </el-tag>
            <span class="meta-item">
              <el-icon><Clock/></el-icon>
              {{ formatDate(article.published_time) }}
            </span>
            <span class="meta-item">
              <el-icon><View/></el-icon>
              {{ article.views }} 次浏览
            </span>
            <span class="meta-item">
              <el-icon><Star/></el-icon>
              {{ article.stars }} 点赞
            </span>
          </div>

          <!-- 文章标签 -->
          <div class="article-tags" v-if="article.tags && article.tags.length > 0">
            <el-tag
                v-for="(tag, idx) in article.tags"
                :key="idx"
                size="small"
                effect="plain"
            >
              {{ tag }}
            </el-tag>
          </div>
        </div>

        <!-- 分割线 -->
        <el-divider/>

        <!-- Markdown 内容渲染区域 -->
        <div class="article-content">
          <md-preview
              :model-value="article.content_markdown"
              :theme="isDark ? 'dark' : 'light'"
              language="zh-CN"
              style="padding: 20px"
          />
        </div>

        <!-- 文章底部操作 -->
        <div class="article-actions">
          <el-button
              type="primary"
              @click="handleLike"
              :disabled="store.getters['auth/isLogin']"
          >
            <template #icon>
              <el-icon>
                <Star/>
              </el-icon>
            </template>
            点赞 ({{ article.stars }})
          </el-button>
        </div>
      </el-card>

      <!-- 评论区组件 -->
      <comment-section
          :article-id="articleId"
          :comments="comments"
          :page="commentPagination.page"
          :size="commentPagination.size"
          :pagination-total="commentPagination.total"
          @refresh-comments="fetchComments"
      />

      <RegisterAnonymousUserDialog
          :visible="registerAnonymousUserVisible"
          @update:visible="val => registerAnonymousUserVisible = val"
          @refresh-data="fetchArticleDetail"
      />
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, computed, reactive} from 'vue'
import {useRouter, useRoute} from 'vue-router'
import {ArrowLeft, Clock, View, Star} from '@element-plus/icons-vue'
import {MdPreview} from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import CommentSection from '@/components/article/CommentSection.vue'
import {ElMessage} from "element-plus";
import {getDetailApi, likePostApi} from "@/api/posts/index.js";
import {getAnonymousUser} from "@/api/anonymous/index.js";
import store from "@/store/index.js";
import RegisterAnonymousUserDialog from "@/components/article/RegisterAnonymousUserDialog.vue";
import {getCommentList} from "@/api/comment/index.js";
import {initTheme, isDark} from "@/utils/theme.js";

const router = useRouter()
const route = useRoute()

// ==================== 响应式数据 ====================
const articleId = computed(() => route.query.id) // 文章ID
const article = ref({
  id: null,
  title: '',
  content_markdown: '',
  category: null,
  tags: [],
  views: 0,
  stars: 0,
  published_time: null
}) // 文章数据
const comments = ref([]) // 评论列表
const loading = ref(false) // 加载状态
const isAnonymousUserLogin = ref(false) // 是否匿名用户登录
const registerAnonymousUserVisible = ref(false)

const commentPagination = reactive({
  page: 1,
  size: 10,
  total: 0,
})

// ==================== API 请求方法 ====================
/**
 * 获取文章详情
 */
const fetchArticleDetail = async () => {
  loading.value = true
  try {
    // 调用后端API获取文章详情
    const response = await getDetailApi(articleId.value)
    if (response.code === 200) {
      article.value = response.data.data
    } else {
      ElMessage.error(response.msg)
    }
  } catch (error) {
    console.error('获取文章详情失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 获取评论列表
 */
const fetchComments = async () => {
  try {
    // 调用后端API获取评论列表
    const response = await getCommentList({
      page: commentPagination.page,
      size: commentPagination.size
    })
    if (response.code === 200) {
      comments.value = response.data.list
      commentPagination.total = response.data.total
    } else {
      ElMessage.error(response.msg)
    }
  } catch (error) {
    console.error('获取评论列表失败:', error)
  }
}

// ==================== 事件处理方法 ====================
/**
 * 返回列表页
 */
const goBack = () => {
  router.push('/')
}

/**
 * 点赞文章
 */
const handleLike = async () => {
  try {
    // 调用后端API点赞文章
    const response = await likePostApi(article.value.id)
    if (response.code === 200) {
      article.value.stars++
    } else {
      ElMessage.error(response.msg)
    }
  } catch (error) {
    console.error('点赞失败:', error)
  }
}

// ==================== 工具方法 ====================
/**
 * 格式化日期
 */
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// ==================== 生命周期 ====================
onMounted(async () => {
  initTheme()
  await fetchArticleDetail()
  await fetchComments()

  // 判断是否是管理员，是则跳过下面步奏
  await store.dispatch('auth/refreshAuthState')
  if (store.getters['auth/isLogin']) return

  // 判断访客是否存在，不存在则创建
  const response = await getAnonymousUser()
  if (response.code === 200) {
    isAnonymousUserLogin.value = true
    registerAnonymousUserVisible.value = false
  } else {
    registerAnonymousUserVisible.value = true
  }
})
</script>

<style scoped>
/* ==================== 页面容器 ==================== */
.article-detail-view {
  min-height: 100vh;
  background-color: var(--el-bg-color-page);
  padding: 20px;
}

.content-container {
  max-width: 70%;
  margin: 0 auto;
}

/* ==================== 返回按钮 ==================== */
.back-button {
  margin-bottom: 20px;
}

/* ==================== 文章卡片 ==================== */
.article-card {
  margin-bottom: 24px;
  background-color: var(--el-bg-color);
}

/* ==================== 文章头部 ==================== */
.article-header {
  margin-bottom: 20px;
}

.article-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--el-text-color-primary);
  line-height: 1.4;
  margin: 0 0 16px 0;
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* ==================== 文章内容 ==================== */
.article-content {
  margin: 24px 0;
  color: var(--el-text-color-primary);
  padding: 20px;
}

/* Markdown 预览组件样式覆盖 */
.article-content :deep(.md-preview) {
  background-color: transparent;
  padding: 0;
}

/* ==================== 文章操作 ==================== */
.article-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 24px;
  border-top: 1px solid var(--el-border-color-lighter);
}

/* ==================== 响应式适配 ==================== */
/* 平板适配 */
@media (max-width: 1024px) {
  .article-title {
    font-size: 28px;
  }
}

/* 手机适配 */
@media (max-width: 768px) {
  .article-detail-view {
    padding: 12px;
  }

  .article-title {
    font-size: 24px;
  }

  .article-meta {
    gap: 12px;
    font-size: 13px;
  }

  .meta-item {
    font-size: 13px;
  }

  .back-button {
    margin-bottom: 16px;
  }
}
</style>
