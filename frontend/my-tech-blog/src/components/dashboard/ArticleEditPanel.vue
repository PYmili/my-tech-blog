<template>
  <!-- 文章编辑面板 -->
  <div class="article-edit-panel">
    <!-- 面板标题 + 操作区域 -->
    <div class="panel-header">
      <!-- 左侧：标题和描述 -->
      <div class="header-left">
        <h2>文章编辑</h2>
        <p>创建和管理您的博客文章</p>
      </div>

      <!-- 右侧：操作按钮和搜索框 -->
      <div class="header-right">
        <!-- 操作按钮组 -->
        <div class="header-actions">
          <el-button type="primary" :icon="Plus" @click="handleCreate">
            新建文章
          </el-button>
          <el-button type="success" :icon="Edit" @click="handleCategoryManage">
            编辑分类
          </el-button>
        </div>

        <!-- 搜索框 -->
        <el-input
            v-model="filterForm.keyword"
            placeholder="输入标题或关键词"
            clearable
            class="header-search"
            @keyup.enter="handleSearch"
        >
          <template #append>
            <el-button :icon="Search" @click="handleSearch" />
          </template>
        </el-input>
      </div>
    </div>

    <!-- 数据统计卡片 -->
    <el-card class="stats-card">
      <template #header>
        <div class="stats-header">
          <el-icon><DataAnalysis /></el-icon>
          <span>数据统计</span>
        </div>
      </template>

      <el-row :gutter="20" class="stats-row">
        <!-- 文章总数 -->
        <el-col :xs="12" :sm="6">
          <div class="stat-item">
            <el-icon class="stat-icon stat-icon--primary"><Document /></el-icon>
            <div class="stat-content">
              <span class="stat-value">{{ pagination.total }}</span>
              <span class="stat-label">文章总数</span>
            </div>
          </div>
        </el-col>

        <!-- 已发布文章 -->
        <el-col :xs="12" :sm="6">
          <div class="stat-item">
            <el-icon class="stat-icon stat-icon--success"><CircleCheck /></el-icon>
            <div class="stat-content">
              <span class="stat-value">{{ publishedCount }}</span>
              <span class="stat-label">已发布</span>
            </div>
          </div>
        </el-col>

        <!-- 草稿文章 -->
        <el-col :xs="12" :sm="6">
          <div class="stat-item">
            <el-icon class="stat-icon stat-icon--warning"><EditPen /></el-icon>
            <div class="stat-content">
              <span class="stat-value">{{ draftCount }}</span>
              <span class="stat-label">草稿</span>
            </div>
          </div>
        </el-col>

        <!-- 分类数量 -->
        <el-col :xs="12" :sm="6">
          <div class="stat-item">
            <el-icon class="stat-icon stat-icon--info"><Folder /></el-icon>
            <div class="stat-content">
              <span class="stat-value">{{ categoryDialog.list.length }}</span>
              <span class="stat-label">分类数量</span>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 文章列表 -->
    <ArticleTable
        :article-list="articleList"
        :loading="loading"
        :pagination="pagination"
        :categories="categoryDialog.list"
        @edit="handleEdit"
        @preview="handlePreview"
        @delete="handleDelete"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
    />

    <!-- 文章创建/编辑对话框 -->
    <ArticleEditor
        v-model:visible="editorDialog.visible"
        v-model:form="editorDialog.form"
        :is-edit="editorDialog.isEdit"
        :category="categoryDialog.list"
        @save="handleSaveArticle"
    />

    <!-- 分类管理对话框 -->
    <CategoryManager
        v-model:visible="categoryDialog.visible"
        v-model:list="categoryDialog.list"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import {
  Plus,
  Search,
  Edit,
  Document,
  CircleCheck,
  EditPen,
  Folder,
  DataAnalysis
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  addPostApi,
  deletePostApi,
  getCategoryListApi,
  getListApi,
  updatePostApi
} from '@/api/posts/index.js'
import ArticleTable from '@/components/dashboard/article/ArticleTable.vue'
import ArticleEditor from '@/components/dashboard/article/ArticleEditor.vue'
import CategoryManager from '@/components/dashboard/article/CategoryManager.vue'

/* ========== 响应式数据 ========== */

/** 加载状态 */
const loading = ref(false)

/** 筛选表单 */
const filterForm = reactive({
  keyword: ''
})

/** 分页配置 */
const pagination = reactive({
  currentPage: 1,
  pageSize: 10,
  total: 0
})

/** 文章列表 */
const articleList = ref([])

/** 文章编辑器对话框配置 */
const editorDialog = reactive({
  visible: false,
  isEdit: false,
  currentId: null,
  form: {
    id: 0,
    title: '',
    category: '',
    status: 'draft',
    content_markdown: '',
    tags: [],
    tagsInput: ''
  }
})

/** 分类管理对话框配置 */
const categoryDialog = reactive({
  visible: false,
  list: []
})

/* ========== 计算属性 ========== */

/**
 * 已发布文章数量
 * @returns {number} 已发布的文章数
 */
const publishedCount = computed(() => {
  return articleList.value.filter(article => article.status === 'published').length
})

/**
 * 草稿文章数量
 * @returns {number} 草稿状态的文章数
 */
const draftCount = computed(() => {
  return articleList.value.filter(article => article.status === 'draft').length
})

/* ========== 方法 ========== */

/**
 * 创建新文章
 * 重置表单数据并打开编辑器对话框
 */
const handleCreate = () => {
  editorDialog.visible = true
  editorDialog.isEdit = false
  editorDialog.currentId = null
  editorDialog.form = {
    title: '',
    category: '',
    status: 'draft',
    content_markdown: '',
    tags: [],
    tagsInput: ''
  }
}

/**
 * 搜索文章
 * 根据关键词筛选文章列表
 */
const handleSearch = async () => {
  loading.value = true
  await getArticleList()
}

/**
 * 编辑文章
 * @param {Object} row - 文章数据对象
 */
const handleEdit = (row) => {
  editorDialog.visible = true
  editorDialog.isEdit = true
  editorDialog.currentId = row.id
  editorDialog.form = {
    id: row.id,
    title: row.title,
    category: row.category,
    status: row.status,
    content_markdown: row.content_markdown || '# 文章内容\n\n请输入文章内容...',
    tags: row.tags || [],
    tagsInput: ''
  }
}

/**
 * 预览文章
 * @param {Object} row - 文章数据对象
 */
const handlePreview = (row) => {
  ElMessage.info(`预览文章: ${row.title}`)
  // TODO: 实现文章预览功能
}

/**
 * 删除文章
 * @param {Object} row - 文章数据对象
 */
const handleDelete = (row) => {
  ElMessageBox.confirm(
      `确定要删除文章《${row.title}》吗？此操作不可恢复！`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
  )
      .then(async () => {
        const response = await deletePostApi(row.id)
        if (response.code === 200) {
          ElMessage.success('删除成功')
          await getArticleList()
        } else {
          ElMessage.error(response.msg)
        }
      })
      .catch(() => {
        ElMessage.info('已取消删除')
      })
}

/**
 * 每页数量变化处理
 * @param {number} val - 新的每页数量
 */
const handleSizeChange = (val) => {
  pagination.pageSize = val
  getArticleList()
}

/**
 * 当前页变化处理
 * @param {number} val - 新的当前页码
 */
const handleCurrentChange = (val) => {
  pagination.currentPage = val
  getArticleList()
}

/**
 * 保存文章
 * 处理文章的创建或更新操作
 */
const handleSaveArticle = async () => {
  // 表单验证
  if (!editorDialog.form.title) {
    ElMessage.warning('请输入文章标题')
    return
  }
  if (!editorDialog.form.category) {
    ElMessage.warning('请选择文章分类')
    return
  }
  if (!editorDialog.form.content_markdown) {
    ElMessage.warning('请输入文章内容')
    return
  }

  // 调用后端API保存文章
  let response
  if (!editorDialog.isEdit) {
    response = await addPostApi(editorDialog.form)
  } else {
    response = await updatePostApi(editorDialog.form)
  }

  if (response.code === 200) {
    ElMessage.success(editorDialog.isEdit ? '文章更新成功' : '文章创建成功')
    editorDialog.visible = false
    await getArticleList()
  } else {
    ElMessage.error(response.msg)
  }
}

/**
 * 打开分类管理对话框
 */
const handleCategoryManage = () => {
  categoryDialog.visible = true
}

/**
 * 获取文章列表
 * @returns {Promise<void>}
 */
const getArticleList = async () => {
  loading.value = true
  try {
    const response = await getListApi({
      page: pagination.currentPage,
      size: pagination.pageSize,
      keyword: filterForm.keyword
    })
    if (response.code === 200) {
      articleList.value = response.data.list
      pagination.total = response.data.total
    } else {
      ElMessage.error(response.msg)
    }
  } catch (error) {
    ElMessage.error('获取文章列表失败')
  } finally {
    loading.value = false
  }
}

/**
 * 获取分类列表
 * @returns {Promise<void>}
 */
const getCategoryList = async () => {
  const response = await getCategoryListApi()
  if (response.code === 200) {
    categoryDialog.list = response.data.list
  } else {
    ElMessage.error(response.msg)
  }
}

/* ========== 生命周期 ========== */
onMounted(async () => {
  await getArticleList()
  await getCategoryList()
})
</script>

<style scoped>
/* ========== 面板容器样式 ========== */
.article-edit-panel {
  width: 100%;
}

/* ========== 面板标题样式 ========== */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}

.header-left h2 {
  font-size: 28px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0 0 8px 0;
}

.header-left p {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
}

/* ========== 头部右侧操作区域 ========== */
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.header-search {
  width: 280px;
}

/* ========== 数据统计卡片样式 ========== */
.stats-card {
  margin-bottom: 20px;
}

.stats-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.stats-row {
  display: flex;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background-color: var(--el-fill-color-lighter);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  background-color: var(--el-fill-color-light);
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 32px;
  padding: 12px;
  border-radius: 8px;
}

/* 统计图标颜色变体 */
.stat-icon--primary {
  color: var(--el-color-primary);
  background-color: var(--el-color-primary-light-9);
}

.stat-icon--success {
  color: var(--el-color-success);
  background-color: var(--el-color-success-light-9);
}

.stat-icon--warning {
  color: var(--el-color-warning);
  background-color: var(--el-color-warning-light-9);
}

.stat-icon--info {
  color: var(--el-color-info);
  background-color: var(--el-color-info-light-9);
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--el-text-color-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: var(--el-text-color-secondary);
  margin-top: 4px;
}

/* ========== 移动端适配 ========== */
@media screen and (max-width: 768px) {
  .panel-header {
    flex-direction: column;
    align-items: stretch;
  }

  .header-left h2 {
    font-size: 24px;
  }

  .header-right {
    flex-direction: column;
    align-items: stretch;
  }

  .header-actions {
    width: 100%;
    justify-content: stretch;
  }

  .header-actions .el-button {
    flex: 1;
  }

  .header-search {
    width: 100%;
  }

  /* 统计卡片移动端适配 */
  .stat-item {
    padding: 12px;
    margin-bottom: 12px;
  }

  .stat-icon {
    font-size: 24px;
    padding: 8px;
  }

  .stat-value {
    font-size: 20px;
  }

  .stat-label {
    font-size: 12px;
  }
}

@media screen and (max-width: 480px) {
  .header-left h2 {
    font-size: 20px;
  }

  .header-actions {
    flex-direction: column;
  }

  .stat-item {
    padding: 10px;
  }

  .stat-icon {
    font-size: 20px;
    padding: 6px;
  }

  .stat-value {
    font-size: 18px;
  }
}
</style>
