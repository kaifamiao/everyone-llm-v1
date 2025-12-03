<template>
  <div class="min-h-screen flex items-center justify-center bg-primary px-4">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="text-center text-3xl font-bold text-text-primary">
          Everyone-LLM
        </h2>
        <p class="mt-2 text-center text-sm text-text-secondary">
          创建新账户
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div v-if="error" class="bg-red-500/10 border border-red-500 text-red-500 px-4 py-3 rounded">
          {{ error }}
        </div>
        
        <div v-if="success" class="bg-green-500/10 border border-green-500 text-green-500 px-4 py-3 rounded">
          注册成功！正在跳转到登录页面...
        </div>
        
        <div class="space-y-4">
          <div>
            <label for="username" class="block text-sm font-medium text-text-primary mb-2">
              用户名 *
            </label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              required
              class="w-full px-4 py-3 bg-secondary border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent text-text-primary"
              placeholder="请输入用户名"
            />
          </div>
          
          <div>
            <label for="email" class="block text-sm font-medium text-text-primary mb-2">
              邮箱
            </label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              class="w-full px-4 py-3 bg-secondary border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent text-text-primary"
              placeholder="请输入邮箱（可选）"
            />
          </div>
          
          <div>
            <label for="phone" class="block text-sm font-medium text-text-primary mb-2">
              手机号
            </label>
            <input
              id="phone"
              v-model="formData.phone"
              type="tel"
              class="w-full px-4 py-3 bg-secondary border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent text-text-primary"
              placeholder="请输入手机号（可选）"
            />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium text-text-primary mb-2">
              密码 *
            </label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              minlength="6"
              class="w-full px-4 py-3 bg-secondary border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent text-text-primary"
              placeholder="请输入密码（至少6位）"
            />
          </div>
          
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-text-primary mb-2">
              确认密码 *
            </label>
            <input
              id="confirmPassword"
              v-model="confirmPassword"
              type="password"
              required
              class="w-full px-4 py-3 bg-secondary border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent text-text-primary"
              placeholder="请再次输入密码"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-accent hover:bg-accent/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </div>

        <div class="text-center">
          <NuxtLink
            to="/login"
            class="text-sm text-accent hover:text-accent/80"
          >
            已有账户？立即登录
          </NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const formData = ref({
  username: '',
  email: '',
  phone: '',
  password: '',
})
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  
  // Validate passwords match
  if (formData.value.password !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    loading.value = false
    return
  }
  
  try {
    const data = {
      username: formData.value.username,
      password: formData.value.password,
    }
    
    if (formData.value.email) {
      data.email = formData.value.email
    }
    
    if (formData.value.phone) {
      data.phone = formData.value.phone
    }
    
    await authStore.register(data)
    success.value = true
    
    // Redirect to login after 2 seconds
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err) {
    error.value = err.message || '注册失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>
