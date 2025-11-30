<template>
  <el-dialog
      v-model="dialogVisible"
      title="访客登记"
      destroy-on-close
      center
  >
    <template #header>
      为了社区环境和安全考虑，我们需要您登记一下您的信息。（仅一次）
    </template>

    <el-input v-model="nickname" placeholder="请输入昵称" />

    <template #footer>
      <div style="display: flex; justify-content: flex-end">
        <el-button type="primary" @click="handlerRegister">提交</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {computed, ref} from "vue";
import {ElMessage} from "element-plus";
import {getAnonymousUser, registerAnonymousUser} from "@/api/anonymous/index.js";

const props = defineProps({
  visible: {
    type: Boolean,
    required: true,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'refresh-data'])

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

const nickname = ref('')

const handlerRegister = async () => {
  if (!nickname.value) {
    return ElMessage.error('请输入昵称！')
  }
  if (nickname.value.length > 50) {
    return ElMessage.error('昵称过长！请在50字符以内')
  }

  const response = await getAnonymousUser(nickname.value)
  if (response.code === 200) {
    return ElMessage.error('昵称已登记，请换一个！')
  }

  const registerRes = await registerAnonymousUser(nickname.value)
  if (registerRes.code === 200) {
    ElMessage.success('登记成功！祝您阅读愉快！')
  } else {
    ElMessage.error(response.msg)
  }

  emit('update:visible', false)
  emit('refresh-data')
}
</script>

<style scoped>

</style>
