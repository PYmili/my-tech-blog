<template>
  <!-- 文章编辑器对话框组件 -->
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑文章' : '创建新文章'"
    width="90%"
    :close-on-click-modal="false"
    class="editor-dialog"
  >
    <el-form :model="formData" label-width="80px">
      <!-- 文章标题 -->
      <el-form-item label="文章标题" required>
        <el-input
          v-model="formData.title"
          placeholder="请输入文章标题"
          clearable
        />
      </el-form-item>

      <!-- 文章分类和状态 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="文章分类" required>
            <el-select
              v-model="formData.category"
              placeholder="请选择分类"
              style="width: 100%"
              default-first-option
            >
              <el-option
                  v-for="(item, idx) in category"
                  :key="idx"
                  :label="item.name"
                  :value="item.name"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="文章状态" required>
            <el-select
              v-model="formData.status"
              placeholder="请选择状态"
              style="width: 100%"
            >
              <el-option label="草稿" value="draft" />
              <el-option label="已发布" value="published" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 文章标签 -->
      <el-form-item label="文章标签">
        <el-input
          v-model="formData.tagsInput"
          placeholder="输入标签后按回车添加，多个标签用回车分隔"
          @keyup.enter="handleAddTag"
        />
        <div class="tags-display" v-if="formData.tags.length > 0">
          <el-tag
            v-for="(tag, index) in formData.tags"
            :key="index"
            closable
            @close="handleRemoveTag(index)"
            style="margin-right: 8px; margin-top: 8px;"
          >
            {{ tag }}
          </el-tag>
        </div>
      </el-form-item>

      <!-- Markdown 编辑器 -->
      <el-form-item label="文章内容" required>
        <MdEditor
          v-model="formData.content_markdown"
          :language="'zh-CN'"
          :toolbars="toolbars"
          :preview-theme="'github'"
          :code-theme="'github'"
          style="height: 600px;"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" @click="handleSave">
          {{ isEdit ? '保存修改' : '创建文章' }}
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

/* ========== Props ========== */
const props = defineProps({
  // 对话框显示状态
  visible: {
    type: Boolean,
    required: true
  },
  // 表单数据
  form: {
    type: Object,
    required: true
  },
  // 是否为编辑模式
  isEdit: {
    type: Boolean,
    default: false
  },
  // 文章分类
  category: {
    type: Array,
    required: true,
    default: []
  }
})

/* ========== Emits ========== */
const emit = defineEmits(['update:visible', 'update:form', 'save'])

/* ========== 计算属性 ========== */

// 对话框显示状态
const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

// 表单数据
const formData = computed({
  get: () => props.form,
  set: (val) => emit('update:form', val)
})

/* ========== 数据 ========== */

// Markdown 编辑器工具栏配置
const toolbars = [
  'bold',
  'underline',
  'italic',
  'strikeThrough',
  '-',
  'title',
  'sub',
  'sup',
  'quote',
  'unorderedList',
  'orderedList',
  'task',
  '-',
  'codeRow',
  'code',
  'link',
  'image',
  'table',
  '-',
  'revoke',
  'next',
  '=',
  'pageFullscreen',
  'fullscreen',
  'preview',
  'htmlPreview',
  'catalog'
]

/* ========== 方法 ========== */

/**
 * 添加标签
 */
const handleAddTag = () => {
  const tag = formData.value.tagsInput.trim()
  if (tag && !formData.value.tags.includes(tag)) {
    formData.value.tags.push(tag)
    formData.value.tagsInput = ''
  }
}

/**
 * 移除标签
 * @param {number} index - 标签索引
 */
const handleRemoveTag = (index) => {
  formData.value.tags.splice(index, 1)
}

/**
 * 取消编辑
 */
const handleCancel = () => {
  dialogVisible.value = false
}

/**
 * 保存文章
 */
const handleSave = () => {
  emit('save')
}
</script>

<style scoped>
/* ========== 编辑器对话框样式 ========== */
.editor-dialog :deep(.el-dialog__body) {
  padding: 20px;
  max-height: 80vh !important;
  overflow-y: auto;
}

/* ========== 标签显示样式 ========== */
.tags-display {
  margin-top: 8px;
}

/* ========== 移动端适配 ========== */
@media screen and (max-width: 768px) {
  .editor-dialog :deep(.el-dialog) {
    width: 95% !important;
  }
}
</style>
