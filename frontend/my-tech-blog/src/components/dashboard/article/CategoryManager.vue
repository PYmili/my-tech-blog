<template>
  <!-- 分类管理对话框组件 -->
  <el-dialog
      v-model="dialogVisible"
      title="分类管理"
      width="600px"
  >
    <div class="category-manage">
      <!-- 添加新分类 -->
      <el-input
          v-model="newCategory.name"
          placeholder="输入新分类名称"
          style="margin-bottom: 16px;"
      />
      <el-input
          v-model="newCategory.description"
          placeholder="输入新分类描述"
          style="margin-bottom: 16px;"
      />
      <div class="new-category-btn-group">
        <el-button :icon="Plus" @click="handleAddCategory">添加</el-button>
      </div>

      <!-- 分类列表 -->
      <el-table :data="categoryList" border>
        <el-table-column prop="name" label="分类名称"/>
        <el-table-column prop="count" label="文章数量"/>
        <el-table-column prop="description" label="描述" show-overflow-tooltip/>
        <el-table-column label="操作" width="120">
          <template #default="{ $index }">
            <el-button
                type="danger"
                size="small"
                :icon="Delete"
                @click="handleDeleteCategory($index)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <template #footer>
      <el-button type="primary" @click="dialogVisible = false">
        完成
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import {ref, computed} from 'vue'
import {Plus, Delete} from '@element-plus/icons-vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {addCategoryApi, deleteCategoryApi} from "@/api/posts/index.js";

/* ========== Props ========== */
const props = defineProps({
  // 对话框显示状态
  visible: {
    type: Boolean,
    required: true
  },
  // 分类列表
  list: {
    type: Array,
    required: true
  }
})

/* ========== Emits ========== */
const emit = defineEmits(['update:visible', 'update:list'])

/* ========== 计算属性 ========== */

// 对话框显示状态
const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

// 分类列表
const categoryList = computed({
  get: () => props.list,
  set: (val) => emit('update:list', val)
})

/* ========== 数据 ========== */

// 新分类名称
const newCategory = ref({
  name: '',
  description: '',
})

/* ========== 方法 ========== */

/**
 * 添加分类
 */
const handleAddCategory = async () => {
  const category = newCategory.value
  if (!category.name) {
    ElMessage.warning('请输入分类名称')
    return
  }

  // 检查是否已存在
  if (categoryList.value.some(item => item.name === category.name)) {
    ElMessage.warning('该分类已存在')
    return
  }

  const response = await addCategoryApi(category)
  console.log(response)
  if (response.code === 200) {
    categoryList.value.push(category)
    newCategory.value = {...newCategory.value}
    ElMessage.success('分类添加成功')
  } else {
    ElMessage.error(response.msg)
    ElMessage.error('分类添加失败！')
  }
}

/**
 * 删除分类
 * @param {number} index - 分类索引
 */
const handleDeleteCategory = (index) => {
  ElMessageBox.confirm(
      '确定要删除该分类吗？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
  )
      .then(async () => {
        const response = await deleteCategoryApi(categoryList.value[index].name)
        if (response.code === 200) {
          categoryList.value.splice(index, 1)
          ElMessage.success('删除成功')
        } else {
          ElMessage.error(response.msg)
          ElMessage.error('删除失败！')
        }
      })
      .catch(() => {
        ElMessage.info('已取消删除')
      })
}
</script>

<style scoped>
/* ========== 分类管理样式 ========== */
.category-manage {
  padding: 10px 0;
}

.new-category-btn-group {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  width: 100%;
  margin-bottom: 20px;
}

/* ========== 移动端适配 ========== */
@media screen and (max-width: 768px) {
  :deep(.el-dialog) {
    width: 95% !important;
  }
}
</style>
