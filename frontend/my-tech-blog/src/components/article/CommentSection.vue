<!-- 评论区组件 - 展示和发表评论 -->
<template>
  <el-card class="comment-section">
    <!-- 评论区标题 -->
    <template #header>
      <div class="section-header">
        <el-icon class="header-icon"><ChatDotRound /></el-icon>
        <span class="header-title">评论区 ({{ comments.length }})</span>
      </div>
    </template>

    <!-- 发表评论表单 -->
    <div class="comment-form">
      <el-form ref="formRef" :model="commentForm" :rules="formRules">
        <el-form-item prop="content">
          <el-input
              :disabled="store.getters['auth/isLogin']"
              v-model="commentForm.content"
              type="textarea"
              placeholder="写下你的评论..."
              :rows="4"
              maxlength="500"
              show-word-limit
              resize="none"
          />
        </el-form-item>

        <!-- 按钮容器靠右对齐 -->
        <el-form-item>
          <div style="display: flex; justify-content: flex-end; width: 100%;">
            <el-button
                type="primary"
                :loading="submitting"
                @click="handleSubmitComment"
                :disabled="store.getters['auth/isLogin']"
            >
              发表评论
            </el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>

    <!-- 评论列表 -->
    <div class="comment-list">
      <el-divider content-position="left">
        <span class="divider-text">全部评论</span>
      </el-divider>

      <!-- 评论项 -->
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="comment-item"
      >
        <!-- 用户头像 -->
        <div class="comment-avatar">
          <el-avatar :size="40">
            <el-icon><User /></el-icon>
          </el-avatar>
        </div>

        <!-- 评论内容 -->
        <div class="comment-content">
          <div class="comment-header">
            <span class="author-name">{{ comment.author.nickname }}</span>
            <span class="comment-time">{{ formatTime(comment.created_time) }}</span>
          </div>
          <p class="comment-text">{{ comment.content }}</p>
        </div>
      </div>

      <!-- 暂无评论提示 -->
      <el-empty
        v-if="comments.length === 0"
        description="暂无评论，快来抢沙发吧！"
        :image-size="100"
      />
      <div class="pagination-wrapper">
        <el-pagination
            v-if="comments.length > 0"
            v-model:current-page="paginationPage"
            v-model:page-size="paginationSize"
            :total="paginationTotal"
            :page-sizes="[10, 20, 30, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            @current-change="val => emit('update:page', val)"
            @size-change="val => emit('update:size', val)"
        />
      </div>
    </div>
  </el-card>
</template>

<script setup>
import {ref, reactive, computed} from 'vue'
import { ElMessage } from 'element-plus'
import { ChatDotRound, User } from '@element-plus/icons-vue'
import {addPostComment} from "@/api/comment/index.js";
import store from "@/store/index.js";

// ==================== Props ====================
const props = defineProps({
  articleId: {
    type: [String, Number],
    required: true
  },
  comments: {
    type: Array,
    default: () => []
  },
  page: {
    type: Number,
    required: true
  },
  size: {
    type: Number,
    required: true
  },
  paginationTotal: {
    type: Number,
    required: true
  }
})

// ==================== Emits ====================
const emit = defineEmits(['refresh-comments', 'update:page', 'update:size'])

// ==================== 响应式数据 ====================
const formRef = ref(null) // 表单引用
const submitting = ref(false) // 提交状态

// 评论表单数据
const commentForm = reactive({
  id: props.articleId,
  content: ''
})

// 表单验证规则
const formRules = {
  content: [
    { required: true, message: '请输入评论内容', trigger: 'blur' },
    { min: 1, max: 500, message: '评论内容不能超过 500 个字符', trigger: 'blur' }
  ]
}

const paginationPage = computed({
  get: () => props.page,
  set: val => emit('update:page', val),
})

const paginationSize = computed({
  get: () => props.size,
  set: val => emit('update:size', val),
})

// ==================== 事件处理方法 ====================
/**
 * 提交评论
 */
const handleSubmitComment = async () => {
  // 表单验证
  if (!formRef.value) return

  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    // 调用后端API提交评论
    const response = await addPostComment(commentForm)
    if (response.code === 200) {
      ElMessage.success('评论发表成功')
      // 重置表单
      formRef.value.resetFields()
      // 刷新评论列表
      emit('refresh-comments')
    } else {
      ElMessage.error(response.msg)
    }
  } catch (error) {
    console.error('发表评论失败:', error)
    ElMessage.error('发表评论失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

// ==================== 工具方法 ====================
/**
 * 格式化时间显示
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

  // 超过7天显示具体日期时间
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
/* ==================== 评论区容器 ==================== */
.comment-section {
  background-color: var(--el-bg-color);
}

/* ==================== 区块头部 ==================== */
.section-header {
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

/* ==================== 评论表单 ==================== */
.comment-form {
  margin-bottom: 24px;
}

/* ==================== 评论列表 ==================== */
.comment-list {
  margin-top: 24px;
}

.pagination-wrapper {
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
}

.divider-text {
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-secondary);
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 16px 0;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.comment-item:last-child {
  border-bottom: none;
}

/* ==================== 评论头像 ==================== */
.comment-avatar {
  flex-shrink: 0;
}

.comment-avatar :deep(.el-avatar) {
  background-color: var(--el-color-primary-light-5);
  color: var(--el-color-primary);
}

/* ==================== 评论内容 ==================== */
.comment-content {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.author-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.comment-time {
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

.comment-text {
  font-size: 14px;
  color: var(--el-text-color-regular);
  line-height: 1.6;
  margin: 0;
  word-wrap: break-word;
  white-space: pre-wrap;
}

/* ==================== 响应式适配 ==================== */
/* 手机适配 */
@media (max-width: 768px) {
  .comment-avatar :deep(.el-avatar) {
    width: 36px;
    height: 36px;
  }

  .comment-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .author-name {
    font-size: 13px;
  }

  .comment-time {
    font-size: 12px;
  }

  .comment-text {
    font-size: 13px;
  }

  .comment-form :deep(.el-form-item__label) {
    font-size: 14px;
  }
}
</style>
