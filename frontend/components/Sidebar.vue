<template>
  <aside
    :class="[
      'w-64 bg-secondary border-r border-border flex flex-col',
      isMobile ? 'fixed inset-y-0 left-0 z-50 transform transition-transform duration-300' : '',
      isMobile && !isSidebarOpen ? '-translate-x-full' : '',
    ]"
  >
    <!-- Logo -->
    <div class="h-12 p-2 border-b border-border">
      <img
        src="https://cdn.sa.net/2025/04/12/57tpedf6qZ98PRz.png"
        alt="Logo"
        class="w-full h-full object-contain"
      />
    </div>
    
    <!-- New Conversation Button -->
    <button
      @click="createNewConversation"
      class="m-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors flex items-center gap-2"
    >
      <Plus class="w-5 h-5" />
      新建对话
    </button>
    
    <!-- Search -->
    <div class="px-4 mb-4">
      <div class="relative">
        <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-text-secondary" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索对话..."
          class="w-full pl-10 pr-4 py-2 bg-primary border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </div>
    
    <!-- Conversation List -->
    <div class="flex-1 overflow-y-auto px-2">
      <div
        v-for="conversation in filteredConversations"
        :key="conversation.id"
        :class="[
          'p-3 rounded-lg mb-2 cursor-pointer transition-colors flex items-center justify-between group',
          selectedConversationId === conversation.id ? 'bg-blue-500 text-white' : 'hover:bg-primary'
        ]"
        @click="selectConversation(conversation.id)"
      >
        <div class="flex items-center gap-2 flex-1 min-w-0">
          <component
            :is="getModeIcon(conversation.mode)"
            class="w-4 h-4 flex-shrink-0"
          />
          <span class="truncate">{{ conversation.title || '新对话' }}</span>
        </div>
        <button
          @click.stop="deleteConversation(conversation.id)"
          class="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-500 rounded"
        >
          <Trash2 class="w-4 h-4" />
        </button>
      </div>
    </div>
    
    <!-- Credits -->
    <div class="p-4 border-t border-border">
      <div class="text-sm text-text-secondary">
        积分: <span class="font-semibold text-text-primary">{{ credits }}</span>
      </div>
    </div>
    
    <!-- User Info -->
    <div class="px-4 pb-2">
      <div class="text-sm text-text-secondary">
        用户: <span class="font-semibold text-text-primary">{{ username }}</span>
      </div>
    </div>
    
    <!-- Settings Button -->
    <button
      @click="showSettings = true"
      class="mx-4 mb-2 px-4 py-2 border border-border rounded-lg hover:bg-primary transition-colors flex items-center gap-2"
    >
      <Settings class="w-5 h-5" />
      设置
    </button>
    
    <!-- Logout Button -->
    <button
      @click="handleLogout"
      class="mx-4 mb-4 px-4 py-2 border border-border rounded-lg hover:bg-red-500/10 hover:border-red-500 hover:text-red-500 transition-colors flex items-center gap-2"
    >
      <LogOut class="w-5 h-5" />
      退出登录
    </button>
  </aside>
  
  <!-- Settings Panel -->
  <SettingsPanel v-if="showSettings" @close="showSettings = false" />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useConversationStore } from '~/stores/conversation'
import { useCreditStore } from '~/stores/credit'
import { useAuthStore } from '~/stores/auth'
import {
  Plus, Search, Trash2, Settings, LogOut,
  MessageSquare, FileText, Database, Globe, Image, Code, Brain
} from 'lucide-vue-next'

const props = defineProps({
  isMobile: Boolean,
  isSidebarOpen: Boolean,
})

const emit = defineEmits(['close-sidebar'])

const conversationStore = useConversationStore()
const creditStore = useCreditStore()
const authStore = useAuthStore()

const searchQuery = ref('')
const showSettings = ref(false)
const selectedConversationId = computed(() => conversationStore.currentConversationId)
const credits = computed(() => creditStore.credits)
const username = computed(() => authStore.user?.username || 'Guest')

const filteredConversations = computed(() => {
  if (!searchQuery.value) {
    return conversationStore.conversations
  }
  return conversationStore.conversations.filter(c =>
    c.title?.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const getModeIcon = (mode) => {
  const icons = {
    AI: Brain,
    DOC: FileText,
    KB: Database,
    DB: Database,
    WEB: Globe,
    IMG: Image,
    MCP: Code,
  }
  return icons[mode] || MessageSquare
}

const createNewConversation = () => {
  conversationStore.createConversation()
  if (props.isMobile) {
    emit('close-sidebar')
  }
}

const selectConversation = (id) => {
  conversationStore.selectConversation(id)
  if (props.isMobile) {
    emit('close-sidebar')
  }
}

const deleteConversation = async (id) => {
  if (confirm('确定要删除这个对话吗？')) {
    await conversationStore.deleteConversation(id)
  }
}

const handleLogout = async () => {
  if (confirm('确定要退出登录吗？')) {
    await authStore.logout()
    await navigateTo('/login')
  }
}

// 加载对话列表
onMounted(async () => {
  if (authStore.isAuthenticated) {
    await conversationStore.loadConversations()
    await creditStore.loadCredits()
  }
})
</script>

