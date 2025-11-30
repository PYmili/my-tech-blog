<template>
  <!-- 个人信息面板 -->
  <div class="profile-panel">
    <!-- 面板标题 -->
    <div class="panel-header">
      <h2>个人信息</h2>
      <p>管理您的个人资料和账户设置</p>
    </div>

    <el-row :gutter="20">
      <!-- 左侧头像卡片 -->
      <el-col :xs="24" :md="8">
        <el-card class="avatar-card">
          <div class="avatar-wrapper">
            <el-upload
                class="avatar-uploader"
                action="#"
                :show-file-list="false"
                :before-upload="handleUploadAvatar"
                accept="image/jpeg,image/png,image/webp"
            >
              <el-avatar :size="120" :src="userInfo.avatar">
                <el-icon><User /></el-icon>
              </el-avatar>
            </el-upload>
          </div>
          <div class="user-basic-info">
            <h3>{{ userInfo.username }}</h3>
            <p>{{ userInfo.email }}</p>
            <el-tag type="success">管理员</el-tag>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧信息表单 -->
      <el-col :xs="24" :md="16">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
              <el-button
                type="primary"
                :icon="Edit"
                size="small"
                @click="handleEdit"
              >
                编辑
              </el-button>
            </div>
          </template>

          <el-form
            ref="formRef"
            :model="userInfo"
            :rules="rules"
            label-width="100px"
            :disabled="!isEditing"
          >
            <div class="user-info-flex">
              <div class="user-info-flex" style="flex-direction: column !important;">
                <!-- 用户名 -->
                <el-form-item label="用户名" prop="username">
                  <el-input v-model="userInfo.username" placeholder="请输入用户名" />
                </el-form-item>

                <!-- 邮箱 -->
                <el-form-item label="邮箱" prop="email">
                  <el-input v-model="userInfo.email" placeholder="请输入邮箱" />
                </el-form-item>

                <!-- github主页链接 -->
                <el-form-item label="github" prop="github_home_link">
                  <el-input v-model="userInfo.github_home_link" placeholder="请输入链接" />
                </el-form-item>
              </div>

              <div class="user-info-flex" style="flex-direction: column !important;">
                <!-- 性别 -->
                <el-form-item label="性别" prop="gender" style="width: 100%;">
                  <el-select-v2
                      v-model="userInfo.gender"
                      :options="genderOptions"
                  />
                </el-form-item>

                <!-- 生日 -->
                <el-form-item label="生日" prop="birth_date">
                  <el-date-picker
                      v-model="userInfo.birth_date"
                      type="date"
                      placeholder="Pick a day"
                  />
                </el-form-item>

                <!-- 居住地 -->
                <el-form-item label="居住地" prop="location">
                  <el-input v-model="userInfo.location" placeholder="请输入居住地" />
                </el-form-item>
              </div>
            </div>

            <!-- 个人简介 -->
            <el-form-item label="个人简介" prop="bio">
              <el-input
                v-model="userInfo.bio"
                type="textarea"
                :rows="4"
                placeholder="请输入个人简介"
              />
            </el-form-item>

            <!-- 操作按钮 -->
            <el-form-item v-if="isEditing">
              <el-button type="primary" @click="handleSave">保存</el-button>
              <el-button @click="handleCancel">取消</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 修改密码卡片 -->
        <el-card class="password-card">
          <template #header>
            <div class="card-header">
              <span>修改密码</span>
            </div>
          </template>

          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="100px"
          >
            <!-- 原密码 -->
            <el-form-item label="原密码" prop="oldPassword">
              <el-input
                v-model="passwordForm.oldPassword"
                type="password"
                placeholder="请输入原密码"
                show-password
              />
            </el-form-item>

            <!-- 新密码 -->
            <el-form-item label="新密码" prop="newPassword">
              <el-input
                v-model="passwordForm.newPassword"
                type="password"
                placeholder="请输入新密码"
                show-password
              />
            </el-form-item>

            <!-- 确认密码 -->
            <el-form-item label="确认密码" prop="confirmPassword">
              <el-input
                v-model="passwordForm.confirmPassword"
                type="password"
                placeholder="请再次输入新密码"
                show-password
              />
            </el-form-item>

            <!-- 操作按钮 -->
            <el-form-item>
              <el-button type="primary" @click="handleChangePassword">
                修改密码
              </el-button>
              <el-button @click="handleResetPasswordForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import {ref, reactive, onMounted} from 'vue'
import { User, Edit } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import {JwtPayload} from "@/utils/validator.js";
import {getInformationApi, updateInformationApi, updatePasswordApi, uploadAvatarApi} from "@/api/user/index.js";

const payload = JwtPayload()

/* ========== 响应式数据 ========== */

// 表单引用
const formRef = ref(null)
const passwordFormRef = ref(null)

// 是否处于编辑状态
const isEditing = ref(false)

// 用户信息
const userInfo = reactive({
  username: payload?.username,
  email: payload?.email || '暂无',
  github_home_link: '',
  gender: '',
  birth_date: '',
  location: '',
  bio: '',
  avatar: ''
})

const genderOptions = [
  { value: 'male', label: '男' },
  { value: 'female', label: '女' },
  { value: 'prefer_not_to_say', label: '不愿透露' },
]

// 用户信息备份（用于取消编辑）
let userInfoBackup = null

// 密码表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

/* ========== 表单验证规则 ========== */

// 用户信息验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在3-20个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

// 密码验证规则
const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在6-20个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

/* ========== 方法 ========== */

/**
 * 通过API获取用户信息
 * @returns {Promise<void>}
 */
const getUserInformation = async () => {
  const response = await getInformationApi()
  if (response.code === 200) {
    const information = response.data?.information
    userInfo.github_home_link = information.github_home_link
    userInfo.gender = information.gender
    userInfo.birth_date = information.birth_date
    userInfo.location = information.location
    userInfo.bio = information.bio
    userInfo.avatar = information.avatar
  } else {
    ElMessage.error(response.msg)
  }
}

/**
 * 上传头像
 */
const handleUploadAvatar = async (file) => {
  console.log(file)
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isLt2M) {
    ElMessage.error('头像大小不可超过 2MiB')
    return false
  }
  // 发送请求
  const response = await uploadAvatarApi(file)
  if (response.code === 200) {
    ElMessage.success('更新头像成功！')
    await getUserInformation()
  } else {
    ElMessage.error(response.msg)
  }
  // 返回 false 手动提交，阻止 el-upload 上传
  return false
}

/**
 * 进入编辑模式
 */
const handleEdit = () => {
  isEditing.value = true
  // 备份原始数据
  userInfoBackup = { ...userInfo }
}

/**
 * 保存用户信息
 */
const handleSave = async () => {
  try {
    await formRef.value.validate()
    // 调用后端API保存用户信息
    const response = await updateInformationApi(userInfo)
    if (response.code === 200) {
      isEditing.value = false
      userInfoBackup = null
      ElMessage.success('保存成功')
    } else {
      ElMessage.error(response.msg)
    }
  } catch (error) {
    ElMessage.error('请检查表单填写是否正确')
  }
}

/**
 * 取消编辑
 */
const handleCancel = () => {
  // 恢复原始数据
  if (userInfoBackup) {
    Object.assign(userInfo, userInfoBackup)
    userInfoBackup = null
  }
  isEditing.value = false
  formRef.value.clearValidate()
}

/**
 * 修改密码
 */
const handleChangePassword = async () => {
  try {
    await passwordFormRef.value.validate()
    // 调用后端API修改密码
    const response = await updatePasswordApi(passwordForm)
    if (response.code === 200) {
      ElMessage.success('密码修改成功')
      handleResetPasswordForm()
    } else {
      ElMessage.error(response.msg)
    }
  } catch (error) {
    ElMessage.error('请检查表单填写是否正确')
  }
}

/**
 * 重置密码表单
 */
const handleResetPasswordForm = () => {
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  passwordFormRef.value.clearValidate()
}

onMounted(async () => {
  // 获取用户信息
  await getUserInformation()
})
</script>

<style scoped>
/* ========== 面板容器样式 ========== */
.profile-panel {
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

/* ========== 头像卡片样式 ========== */
.avatar-card {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  height: 97% !important;
}

.avatar-wrapper {
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.avatar-uploader {
  width: 100%;
  transition: all 0.3s ease;
}

.avatar-uploader:hover {
  transform: scale(1.3);
}

.user-basic-info {
  padding: 20px 0;
  border-top: 1px solid var(--el-border-color);
}

.user-basic-info h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0 0 8px 0;
}

.user-basic-info p {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0 0 12px 0;
}

/* ========== 信息卡片样式 ========== */
.info-card {
  margin-bottom: 20px;;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.user-info-flex {
  display: flex;
  justify-content: space-around;
  align-items: self-start;
}

/* ========== 密码卡片样式 ========== */
.password-card {
  margin-bottom: 20px;
}

/* ========== 移动端适配 ========== */
@media screen and (max-width: 768px) {
  .panel-header h2 {
    font-size: 24px;
  }

  .avatar-card {
    margin-bottom: 20px;
  }

  .user-info-flex {
    flex-direction: column;
  }
}

@media screen and (max-width: 480px) {
  .panel-header h2 {
    font-size: 20px;
  }
}
</style>
