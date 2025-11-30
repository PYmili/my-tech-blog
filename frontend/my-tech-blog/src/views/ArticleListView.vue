<template>
  <div class="article-list-view">
    <!-- 页面头部 -->
    <div class="page-header">
      <h1 class="page-title">技术博客</h1>
      <p class="page-subtitle">分享技术，记录成长</p>
    </div>

    <div class="content-wrapper">
      <!-- 左侧：文章列表区域 -->
      <div class="article-list-section">
        <!-- 分类筛选 -->
        <div class="filter-bar">
          <el-select
            v-model="selectedCategory"
            placeholder="全部分类"
            clearable
            @change="handleCategoryChange"
            class="category-select"
          >
            <el-option label="全部分类" value="" />
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </div>

        <!-- 文章卡片列表 -->
        <div v-if="articles.length > 0" class="article-cards">
          <article-card
            v-for="article in articles"
            :key="article.id"
            :article="article"
            @click="goToArticle(article.id)"
          />
        </div>

        <!-- 暂无数据提示 -->
        <el-empty
          v-else
          description="暂无文章"
        />

        <!-- 分页组件 -->
        <div v-if="total > 0" class="pagination-wrapper">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[10, 20, 30, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            @current-change="handlePageChange"
            @size-change="handleSizeChange"
          />
        </div>
      </div>

      <!-- 右侧：热度排行榜 -->
      <div class="sidebar">
        <hot-rank-list :hot-articles="hotArticles" @article-click="goToArticle" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ArticleCard from '@/components/article/ArticleCard.vue'
import HotRankList from '@/components/article/HotRankList.vue'
import {getCategoryListApi, getHotApi, getListApi} from "@/api/posts/index.js";
import {ElMessage} from "element-plus";
import store from "@/store/index.js";
import {getFingerprint} from "@/utils/fingerprint.js";
import {initTheme} from "@/utils/theme.js";

const router = useRouter()

// ==================== 响应式数据 ====================
const articles = ref([]) // 文章列表
const hotArticles = ref([]) // 热度排行榜
const categories = ref([]) // 分类列表
const selectedCategory = ref(null) // 选中的分类
const currentPage = ref(1) // 当前页码
const pageSize = ref(10) // 每页数量
const total = ref(0) // 总数量

// ==================== API 请求方法 ====================
/**
 * 获取文章列表
 */
const fetchArticles = async () => {
  try {
    // 调用后端API获取文章列表
    const response = await getListApi({
      page: currentPage.value,
      size: pageSize.value,
      status: 'published'
    })
    if (response.code === 200) {
      articles.value = response.data.list
      total.value = response.data.total
    } else {
      ElMessage.error(response.msg)
    }
  } catch (error) {
    console.error('获取文章列表失败:', error)
  }
}

/**
 * 获取热度排行榜（前10）
 */
const fetchHotArticles = async () => {
  try {
    // 调用后端API获取热度排行榜
    const response = await getHotApi()
    if (response.code === 200) {
      hotArticles.value = response.data.list
    } else {
      ElMessage.error(response.msg)
    }
  } catch (error) {
    console.error('获取热度排行榜失败:', error)
  }
}

/**
 * 获取分类列表
 */
const fetchCategories = async () => {
  try {
    // 调用后端API获取分类列表
    const response = await getCategoryListApi()
    if (response.code === 200) {
      categories.value = response.data.list
    } else {
      ElMessage.error(response.msg)
    }
  } catch (error) {
    console.error('获取分类列表失败:', error)
  }
}

// ==================== 事件处理方法 ====================
/**
 * 分类变更处理
 */
const handleCategoryChange = () => {
  currentPage.value = 1
  fetchArticles()
}

/**
 * 页码变更处理
 */
const handlePageChange = (page) => {
  currentPage.value = page
  fetchArticles()
  // 滚动到顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

/**
 * 每页数量变更处理
 */
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchArticles()
}

/**
 * 跳转到文章详情页
 */
const goToArticle = (articleId) => {
  console.log("articleId: ", articleId)
  router.push(`/article?id=${articleId}`)
}

// ==================== 生命周期 ====================
onMounted(async () => {
  initTheme()
  await fetchArticles()
  await fetchHotArticles()
  await fetchCategories()
})
</script>

<style scoped>
/* ==================== 页面容器 ==================== */
.article-list-view {
  min-height: 100vh;
  background-color: var(--el-bg-color-page);
  padding: 20px;
}

/* ==================== 页面头部 ==================== */
.page-header {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, var(--el-color-primary-light-3), var(--el-color-primary));
  border-radius: 12px;
  margin-bottom: 30px;
  color: #fff;
}

.page-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 10px 0;
}

.page-subtitle {
  font-size: 16px;
  margin: 0;
  opacity: 0.9;
}

/* ==================== 内容布局 ==================== */
.content-wrapper {
  display: flex;
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.article-list-section {
  flex: 1;
  min-width: 0; /* 防止flex子元素溢出 */
}

.sidebar {
  width: 320px;
  flex-shrink: 0;
}

/* ==================== 筛选栏 ==================== */
.filter-bar {
  margin-bottom: 24px;
  display: flex;
  align-items: center;
}

.category-select {
  width: 200px;
}

/* ==================== 文章卡片列表 ==================== */
.article-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ==================== 分页 ==================== */
.pagination-wrapper {
  margin-top: 32px;
  display: flex;
  justify-content: center;
}

/* ==================== 响应式适配 ==================== */
/* 平板适配 (768px - 1024px) */
@media (max-width: 1024px) {
  .content-wrapper {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }

  .page-title {
    font-size: 28px;
  }

  .page-subtitle {
    font-size: 14px;
  }
}

/* 手机适配 (< 768px) */
@media (max-width: 768px) {
  .article-list-view {
    padding: 12px;
  }

  .page-header {
    padding: 24px 16px;
    margin-bottom: 20px;
  }

  .page-title {
    font-size: 24px;
  }

  .page-subtitle {
    font-size: 13px;
  }

  .filter-bar {
    margin-bottom: 16px;
  }

  .category-select {
    width: 100%;
  }

  .pagination-wrapper {
    margin-top: 24px;
  }

  /* 移动端分页布局调整 */
  .pagination-wrapper :deep(.el-pagination) {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
