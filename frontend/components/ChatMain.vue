<template>
  <div class="flex-1 flex flex-col overflow-hidden">
    <!-- Header -->
    <div class="p-4 border-b border-border flex items-center justify-between">
      <input
        v-model="conversationTitle"
        @blur="updateTitle"
        class="text-lg font-semibold bg-transparent border-none outline-none flex-1"
        placeholder="新对话"
      />
      <button
        @click="exportConversation"
        class="p-2 hover:bg-secondary rounded-lg"
        title="导出对话"
      >
        <Download class="w-5 h-5" />
      </button>
    </div>
    
    <!-- Messages -->
    <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-4">
      <div
        v-for="message in messages"
        :key="message.id"
        :class="[
          'flex gap-4',
          message.role === 'user' ? 'justify-end' : 'justify-start'
        ]"
      >
        <div
          :class="[
            'flex gap-3 max-w-3xl',
            message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
          ]"
        >
          <!-- Avatar -->
          <div class="flex-shrink-0">
            <component
              :is="message.role === 'user' ? User : Bot"
              class="w-8 h-8"
            />
          </div>
          
          <!-- Message Content -->
          <div
            :class="[
              'rounded-lg p-4',
              message.role === 'user'
                ? 'bg-blue-500 text-white'
                : 'bg-secondary text-text-primary'
            ]"
          >
            <div
              v-html="renderMarkdown(message.content)"
              class="prose prose-sm max-w-none dark:prose-invert"
            />
            
            <!-- Message Actions -->
            <div
              v-if="message.role === 'assistant'"
              class="flex gap-2 mt-2 pt-2 border-t border-border"
            >
              <button @click="likeMessage(message.id)" class="p-1 hover:bg-primary rounded">
                <ThumbsUp class="w-4 h-4" />
              </button>
              <button @click="dislikeMessage(message.id)" class="p-1 hover:bg-primary rounded">
                <ThumbsDown class="w-4 h-4" />
              </button>
              <button @click="regenerateMessage(message.id)" class="p-1 hover:bg-primary rounded">
                <RefreshCw class="w-4 h-4" />
              </button>
              <button @click="copyMessage(message.content)" class="p-1 hover:bg-primary rounded">
                <Copy class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Loading Indicator -->
      <div v-if="isLoading" class="flex justify-start">
        <div class="flex gap-3 max-w-3xl">
          <Bot class="w-8 h-8" />
          <div class="bg-secondary rounded-lg p-4">
            <div class="flex gap-1">
              <span class="w-2 h-2 bg-text-secondary rounded-full animate-bounce" style="animation-delay: 0s" />
              <span class="w-2 h-2 bg-text-secondary rounded-full animate-bounce" style="animation-delay: 0.2s" />
              <span class="w-2 h-2 bg-text-secondary rounded-full animate-bounce" style="animation-delay: 0.4s" />
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Input Area -->
    <ChatInput @send="handleSend" />
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useConversationStore } from '~/stores/conversation'
import { User, Bot, Download, ThumbsUp, ThumbsDown, RefreshCw, Copy } from 'lucide-vue-next'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'

const conversationStore = useConversationStore()
const messagesContainer = ref(null)
const conversationTitle = ref('')
const isLoading = ref(false)

const messages = computed(() => {
  const conversationId = conversationStore.currentConversationId
  if (!conversationId) return []
  return conversationStore.getMessages(conversationId)
})

const renderMarkdown = (content) => {
  marked.setOptions({
    highlight: (code, lang) => {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value
      }
      return hljs.highlightAuto(code).value
    },
  })
  return marked.parse(content)
}

const updateTitle = async () => {
  const conversationId = conversationStore.currentConversationId
  if (conversationId) {
    await conversationStore.updateConversationTitle(conversationId, conversationTitle.value)
  }
}

const handleSend = async (content) => {
  isLoading.value = true
  try {
    await conversationStore.sendMessage(content)
    await nextTick()
    scrollToBottom()
  } finally {
    isLoading.value = false
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const likeMessage = (messageId) => {
  console.log('Like message:', messageId)
}

const dislikeMessage = (messageId) => {
  console.log('Dislike message:', messageId)
}

const regenerateMessage = (messageId) => {
  console.log('Regenerate message:', messageId)
}

const copyMessage = async (content) => {
  await navigator.clipboard.writeText(content)
  alert('已复制到剪贴板')
}

const exportConversation = () => {
  const conversationId = conversationStore.currentConversationId
  if (!conversationId) return
  
  const conversation = conversationStore.conversations.find(c => c.id === conversationId)
  const msgs = conversationStore.getMessages(conversationId)
  
  // 导出为 JSON
  const data = {
    conversation,
    messages: msgs,
  }
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${conversation?.title || 'conversation'}.json`
  a.click()
  URL.revokeObjectURL(url)
}

watch(() => conversationStore.currentConversationId, async (newId) => {
  if (newId) {
    await conversationStore.loadMessages(newId)
    const conversation = conversationStore.conversations.find(c => c.id === newId)
    conversationTitle.value = conversation?.title || '新对话'
    await nextTick()
    scrollToBottom()
  }
}, { immediate: true })

watch(messages, () => {
  nextTick(() => scrollToBottom())
}, { deep: true })
</script>

