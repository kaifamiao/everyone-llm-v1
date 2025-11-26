<template>
  <div class="p-4 border-t border-border bg-primary">
    <!-- First Row: Model, Mode, Attachments -->
    <div class="flex gap-2 mb-2">
      <!-- Model Select -->
      <select
        v-model="selectedModel"
        class="px-3 py-2 border border-border rounded-lg bg-primary text-text-primary focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option v-for="model in models" :key="model" :value="model">
          {{ model }}
        </option>
      </select>
      
      <!-- Mode Select -->
      <select
        v-model="selectedMode"
        class="px-3 py-2 border border-border rounded-lg bg-primary text-text-primary focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option v-for="mode in modes" :key="mode.value" :value="mode.value">
          {{ mode.label }}
        </option>
      </select>
      
      <!-- Attachment Button (conditional) -->
      <button
        v-if="showAttachment"
        @click="handleAttachment"
        class="px-3 py-2 border border-border rounded-lg hover:bg-secondary transition-colors"
      >
        <component :is="attachmentIcon" class="w-5 h-5" />
      </button>
    </div>
    
    <!-- Second Row: Input and Send -->
    <div class="flex gap-2">
      <textarea
        v-model="inputText"
        @keydown.enter.exact.prevent="handleSend"
        @keydown.enter.shift.exact="inputText += '\n'"
        :placeholder="inputPlaceholder"
        class="flex-1 px-4 py-2 border border-border rounded-lg bg-primary text-text-primary focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        rows="3"
      />
      <button
        @click="handleSend"
        :disabled="!inputText.trim() || isLoading"
        class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <Send class="w-5 h-5" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useModelStore } from '~/stores/model'
import { useModeStore } from '~/stores/mode'
import { Send, FileText, Image, Database, Globe, Code } from 'lucide-vue-next'

const emit = defineEmits(['send'])

const modelStore = useModelStore()
const modeStore = useModeStore()

const inputText = ref('')
const isLoading = ref(false)

const selectedModel = computed({
  get: () => modelStore.currentModel,
  set: (value) => modelStore.setModel(value),
})

const selectedMode = computed({
  get: () => modeStore.currentMode,
  set: (value) => modeStore.setMode(value),
})

const models = ['gpt-4o', 'gpt-4', 'gpt-3.5-turbo', 'claude-3-opus', 'claude-3-sonnet']

const modes = [
  { value: 'AI', label: 'AI对话' },
  { value: 'DOC', label: '文档对话' },
  { value: 'KB', label: '知识库对话' },
  { value: 'DB', label: '数据库对话' },
  { value: 'WEB', label: 'Web对话' },
  { value: 'IMG', label: '图片对话' },
  { value: 'MCP', label: 'MCP对话' },
]

const showAttachment = computed(() => {
  return ['DOC', 'KB', 'DB', 'WEB', 'IMG', 'MCP'].includes(selectedMode.value)
})

const attachmentIcon = computed(() => {
  const icons = {
    DOC: FileText,
    KB: Database,
    DB: Database,
    WEB: Globe,
    IMG: Image,
    MCP: Code,
  }
  return icons[selectedMode.value] || FileText
})

const inputPlaceholder = computed(() => {
  const placeholders = {
    AI: '输入消息...',
    DOC: '上传文档后输入消息...',
    KB: '选择知识库后输入消息...',
    DB: '选择数据库后输入消息...',
    WEB: '输入URL后输入消息...',
    IMG: '上传图片后输入消息...',
    MCP: '配置MCP后输入消息...',
  }
  return placeholders[selectedMode.value] || '输入消息...'
})

const handleAttachment = () => {
  // TODO: 实现附件上传逻辑
  console.log('Attachment clicked for mode:', selectedMode.value)
}

const handleSend = async () => {
  if (!inputText.value.trim() || isLoading.value) return
  
  const content = inputText.value.trim()
  inputText.value = ''
  isLoading.value = true
  
  try {
    emit('send', content)
  } finally {
    isLoading.value = false
  }
}
</script>

