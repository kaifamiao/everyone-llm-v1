<template>
  <div class="min-h-screen bg-primary">
    <NuxtPage />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useRouter, useRoute } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

onMounted(async () => {
  // Check authentication status
  await authStore.checkAuth()
  
  // Redirect to login if not authenticated and not already on auth pages
  const publicPages = ['/login', '/register']
  const isPublicPage = publicPages.includes(route.path)
  
  if (!authStore.isAuthenticated && !isPublicPage) {
    router.push('/login')
  } else if (authStore.isAuthenticated && isPublicPage) {
    router.push('/')
  }
})
</script>

