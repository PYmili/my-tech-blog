<template>
  <!-- 登录页面容器 -->
  <div class="login-container">
    <!-- 登录卡片 -->
    <el-card class="login-card" shadow="hover">
      <!-- 标题区域 -->
      <div class="login-header">
        <el-icon class="header-icon" :size="48">
          <User />
        </el-icon>
        <h1 class="header-title">管理员登录</h1>
        <p class="header-subtitle">我的技术博客管理系统</p>
      </div>

      <!-- 登录表单 -->
      <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          size="large"
      >
        <!-- 用户名输入框 -->
        <el-form-item prop="username">
          <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              :prefix-icon="User"
              clearable
              @keyup.enter="handleLogin"
          />
        </el-form-item>

        <!-- 密码输入框 -->
        <el-form-item prop="password">
          <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              :prefix-icon="Lock"
              show-password
              clearable
              @keyup.enter="handleLogin"
          />
        </el-form-item>

        <!-- 记住我选项 -->
<!--        <el-form-item class="remember-item">-->
<!--          <el-checkbox v-model="loginForm.rememberMe">-->
<!--            记住我-->
<!--          </el-checkbox>-->
<!--        </el-form-item>-->

        <!-- 登录按钮 -->
        <el-form-item>
          <el-button
              type="primary"
              class="login-button"
              :loading="loading"
              @click="handleLogin"
          >
            <span v-if="!loading">登录</span>
            <span v-else>登录中...</span>
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 页脚提示 -->
      <div class="login-footer">
        <el-icon class="footer-icon" :size="14">
          <InfoFilled />
        </el-icon>
        <span class="footer-text">请使用管理员账号登录</span>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import {ref, reactive} from 'vue'
import {User, Lock, InfoFilled} from '@element-plus/icons-vue'
import {ElMessage} from 'element-plus'
import { loginApi } from '@/api/auth/index.js'
import store from "@/store/index.js";
import router from "@/router/index.js";

/**
 * 表单引用
 */
const loginFormRef = ref(null)

/**
 * 加载状态
 */
const loading = ref(false)

/**
 * 登录表单数据
 */
const loginForm = reactive({
  username: '', // 用户名
  password: '', // 密码
  rememberMe: false // 记住我
})

/**
 * 表单验证规则
 */
const loginRules = {
  // 用户名验证规则
  username: [
    {required: true, message: '请输入用户名', trigger: 'blur'},
    {min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur'}
  ],
  // 密码验证规则
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'},
    {min: 6, max: 30, message: '密码长度在 6 到 30 个字符', trigger: 'blur'}
  ]
}

/**
 * 处理登录逻辑
 * 验证表单后触发登录事件
 */
const handleLogin = async () => {
  // 验证表单
  if (!loginFormRef.value) return

  try {
    // 验证表单是否通过
    await loginFormRef.value.validate()

    // 设置加载状态
    loading.value = true

    // 调用后端登录接口
    const response = await loginApi({
      username: loginForm.username,
      password: loginForm.password
    })
    if (response.code === 200) {
      ElMessage.success('登录成功！')
      // 设置登录状态
      store.commit('auth/SET_TOKEN', response.data)
      await store.dispatch('auth/refreshAuthState')
      await router.push('dashboard')
    } else {
      ElMessage.error(response.msg)
    }

  } catch (error) {
    // 表单验证失败或登录失败
    console.error('登录失败:', error)
  } finally {
    // 取消加载状态
    loading.value = false
  }
}
</script>

<style scoped>
/**
 * 登录容器 - 全屏居中布局
 */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, var(--el-color-primary-light-9) 0%, var(--el-color-primary-light-7) 100%);
}

/**
 * 登录卡片
 */
.login-card {
  width: 100%;
  max-width: 420px;
  border-radius: 12px;
  overflow: hidden;
}

/* 移除 Element Plus 卡片默认内边距，使用自定义间距 */
.login-card :deep(.el-card__body) {
  padding: 40px 32px;
}

/**
 * 登录头部
 */
.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.header-icon {
  color: var(--el-color-primary);
  margin-bottom: 16px;
}

.header-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0 0 8px 0;
}

.header-subtitle {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
}

/**
 * 登录表单
 */
.login-form {
  margin-top: 24px;
}

/* 记住我选项 */
.remember-item {
  margin-bottom: 24px;
}

.remember-item :deep(.el-form-item__content) {
  justify-content: flex-start;
}

/* 登录按钮 */
.login-button {
  width: 100%;
  height: 44px;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 1px;
}

/**
 * 登录页脚
 */
.login-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--el-border-color-lighter);
}

.footer-icon {
  color: var(--el-color-info);
  margin-right: 6px;
}

.footer-text {
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

/**
 * 移动端适配
 */
@media screen and (max-width: 768px) {
  .login-container {
    padding: 16px;
  }

  .login-card :deep(.el-card__body) {
    padding: 32px 24px;
  }

  .header-icon {
    font-size: 40px;
  }

  .header-title {
    font-size: 24px;
  }

  .header-subtitle {
    font-size: 13px;
  }

  .login-button {
    height: 42px;
    font-size: 15px;
  }
}

@media screen and (max-width: 480px) {
  .login-container {
    padding: 12px;
  }

  .login-card :deep(.el-card__body) {
    padding: 24px 20px;
  }

  .header-icon {
    font-size: 36px;
  }

  .header-title {
    font-size: 22px;
  }

  .login-form {
    margin-top: 20px;
  }

  .login-footer {
    margin-top: 20px;
    padding-top: 20px;
  }
}
</style>
