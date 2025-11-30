<template>
  <!-- 文章列表表格组件 -->
  <el-card class="list-card">
    <template #header>
      <div class="card-header">
        <span>文章列表（共 {{ pagination.total }} 篇）</span>
      </div>
    </template>

    <el-table
        :data="articleList"
        style="width: 100%"
        v-loading="loading"
    >
      <!-- 文章标题 -->
      <el-table-column prop="title" label="标题" show-overflow-tooltip />

      <!-- 分类列添加筛选功能 -->
      <el-table-column
          prop="category"
          label="分类"
          :filters="categoryFilters"
          :filter-method="filterCategory"
          filter-placement="bottom-end"
      >
        <template #default="{ row }">
          <el-tag v-if="row?.category">{{ row.category }}</el-tag>
          <el-tag v-else type="warning">暂无</el-tag>
        </template>
      </el-table-column>

      <!-- 状态列添加筛选功能 -->
      <el-table-column
          prop="status"
          label="状态"
          :filters="statusFilters"
          :filter-method="filterStatus"
          filter-placement="bottom-end"
      >
        <template #default="{ row }">
          <el-tag :type="row.status === 'published' ? 'success' : 'info'">
            {{ row.status === 'published' ? '已发布' : '草稿' }}
          </el-tag>
        </template>
      </el-table-column>

      <!-- 标签 -->
      <el-table-column prop="tags" label="标签">
        <template #default="{ row }">
          <el-tag
              v-for="(tag, idx) in row.tags"
              :key="idx"
              style="margin-right: 4px;"
          >
            {{ tag }}
          </el-tag>
        </template>
      </el-table-column>

      <!-- 浏览量 -->
      <el-table-column prop="views" label="浏览量" sortable />

      <!-- 点赞数 -->
      <el-table-column prop="stars" label="点赞数" sortable />

      <!-- 创建时间 -->
      <el-table-column
          prop="created_time"
          label="创建时间"
          sortable
          show-overflow-tooltip
      />

      <!-- 操作列 -->
      <el-table-column label="操作" fixed="right" min-width="150">
        <template #default="{ row }">
          <!-- 桌面端：显示按钮组 -->
          <div class="op-buttons op-buttons--desktop">
            <el-button
                type="primary"
                size="small"
                :icon="Edit"
                @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
                type="warning"
                size="small"
                :icon="View"
                @click="handlePreview(row)"
            >
              预览
            </el-button>
            <el-button
                type="danger"
                size="small"
                :icon="Delete"
                @click="handleDelete(row)"
            >
              删除
            </el-button>
          </div>

          <!-- 移动端：显示下拉菜单 -->
          <div class="op-buttons op-buttons--mobile">
            <el-dropdown trigger="click" @command="(cmd) => handleCommand(cmd, row)">
              <el-button type="primary" size="small">
                操作
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="edit" :icon="Edit">
                    编辑
                  </el-dropdown-item>
                  <el-dropdown-item command="preview" :icon="View">
                    预览
                  </el-dropdown-item>
                  <el-dropdown-item command="delete" :icon="Delete" divided>
                    删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination-wrapper">
      <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
      />
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { Edit, View, Delete, ArrowDown } from '@element-plus/icons-vue'

/* ========== Props ========== */
const props = defineProps({
  /** 文章列表数据 */
  articleList: {
    type: Array,
    required: true
  },
  /** 加载状态 */
  loading: {
    type: Boolean,
    default: false
  },
  /** 分页配置 */
  pagination: {
    type: Object,
    required: true
  },
  /** 分类列表 */
  categories: {
    type: Array,
    default: () => []
  }
})

/* ========== Emits ========== */
const emit = defineEmits(['edit', 'preview', 'delete', 'size-change', 'current-change'])

/* ========== 计算属性 ========== */

/**
 * 分类筛选器选项
 * 将分类列表转换为筛选器格式
 */
const categoryFilters = computed(() => {
  return props.categories.map(category => ({
    text: category.name,
    value: category.name
  }))
})

/* ========== 数据 ========== */

/** 状态筛选器选项 */
const statusFilters = [
  { text: '已发布', value: 'published' },
  { text: '草稿', value: 'draft' }
]

/* ========== 方法 ========== */

/**
 * 编辑文章
 * @param {Object} row - 文章数据
 */
const handleEdit = (row) => {
  emit('edit', row)
}

/**
 * 预览文章
 * @param {Object} row - 文章数据
 */
const handlePreview = (row) => {
  emit('preview', row)
}

/**
 * 删除文章
 * @param {Object} row - 文章数据
 */
const handleDelete = (row) => {
  emit('delete', row)
}

/**
 * 处理下拉菜单命令（移动端）
 * @param {string} command - 命令类型：edit/preview/delete
 * @param {Object} row - 文章数据
 */
const handleCommand = (command, row) => {
  switch (command) {
    case 'edit':
      handleEdit(row)
      break
    case 'preview':
      handlePreview(row)
      break
    case 'delete':
      handleDelete(row)
      break
  }
}

/**
 * 每页数量变化
 * @param {number} val - 每页数量
 */
const handleSizeChange = (val) => {
  emit('size-change', val)
}

/**
 * 当前页变化
 * @param {number} val - 当前页码
 */
const handleCurrentChange = (val) => {
  emit('current-change', val)
}

/**
 * 筛选分类
 * @param {string} value - 分类名称
 * @param {Object} row - 行数据
 * @returns {boolean} 是否匹配
 */
const filterCategory = (value, row) => {
  return row.category === value
}

/**
 * 筛选状态
 * @param {string} value - 状态值
 * @param {Object} row - 行数据
 * @returns {boolean} 是否匹配
 */
const filterStatus = (value, row) => {
  return row.status === value
}
</script>

<style scoped>
/* ========== 列表卡片样式 ========== */
.list-card {
  margin-bottom: 20px;
}

.card-header {
  font-weight: 600;
  color: var(--el-text-color-primary);
}

/* ========== 分页样式 ========== */
.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* ========== 操作按钮样式 ========== */
.op-buttons {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 桌面端按钮组：默认显示 */
.op-buttons--desktop {
  display: flex;
}

/* 移动端下拉菜单：默认隐藏 */
.op-buttons--mobile {
  display: none;
}

/* ========== 移动端适配 ========== */
@media screen and (max-width: 768px) {
  /* 移动端分页样式 */
  .pagination-wrapper :deep(.el-pagination) {
    flex-wrap: wrap;
    justify-content: center;
  }

  /* 移动端：隐藏按钮组，显示下拉菜单 */
  .op-buttons--desktop {
    display: none;
  }

  .op-buttons--mobile {
    display: flex;
  }
}
</style>
