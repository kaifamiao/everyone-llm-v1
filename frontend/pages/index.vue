<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar -->
    <Sidebar
      :is-mobile="isMobile"
      :is-sidebar-open="isSidebarOpen"
      @close-sidebar="isSidebarOpen = false"
    />
    
    <!-- Mobile Overlay -->
    <div
      v-if="isMobile && isSidebarOpen"
      class="fixed inset-0 bg-black bg-opacity-50 z-40"
      @click="isSidebarOpen = false"
    />
    
    <!-- Chat Main -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Mobile Header -->
      <div v-if="isMobile" class="flex items-center p-4 border-b border-border">
        <button
          @click="isSidebarOpen = !isSidebarOpen"
          class="p-2 hover:bg-secondary rounded-lg"
        >
          <Menu class="w-6 h-6" />
        </button>
        <h1 class="ml-4 text-lg font-semibold">Everyone-LLM</h1>
      </div>
      
      <!-- Chat Content -->
      <ChatMain />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Menu } from 'lucide-vue-next'

const isMobile = ref(false)
const isSidebarOpen = ref(false)

const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
  if (!isMobile.value) {
    isSidebarOpen.value = false
  }
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

