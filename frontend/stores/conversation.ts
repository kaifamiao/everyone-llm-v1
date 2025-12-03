import { defineStore } from 'pinia'
import { api } from '~/services/api'
import { useModelStore } from './model'
import { useModeStore } from './mode'
import { useSettingsStore } from './settings'
import { useCreditStore } from './credit'

export interface Message {
  id: number
  conversation_id: number
  role: 'user' | 'assistant' | 'system'
  content: string
  token_count: number
  created_at: string
}

export interface Conversation {
  id: number
  user_id: number
  title: string | null
  model: string | null
  mode: string | null
  status: string
  created_at: string
  updated_at: string
}

export const useConversationStore = defineStore('conversation', {
  state: () => ({
    conversations: [] as Conversation[],
    currentConversationId: null as number | null,
    messages: {} as Record<number, Message[]>,
  }),

  actions: {
    async loadConversations() {
      try {
        const data = await api.get('/conversations')
        this.conversations = data
      } catch (error) {
        console.error('Failed to load conversations:', error)
      }
    },

    async createConversation() {
      try {
        const modelStore = useModelStore()
        const modeStore = useModeStore()

        const data = await api.post('/conversations', {
          title: '新对话',
          model: modelStore.currentModel,
          mode: modeStore.currentMode,
        })

        this.conversations.unshift(data)
        this.currentConversationId = data.id
        this.messages[data.id] = []
        return data
      } catch (error) {
        console.error('Failed to create conversation:', error)
        throw error
      }
    },

    async selectConversation(id: number) {
      this.currentConversationId = id
      if (!this.messages[id]) {
        await this.loadMessages(id)
      }
    },

    async loadMessages(conversationId: number) {
      try {
        const data = await api.get(`/conversations/${conversationId}/messages`)
        this.messages[conversationId] = data
      } catch (error) {
        console.error('Failed to load messages:', error)
      }
    },

    getMessages(conversationId: number): Message[] {
      return this.messages[conversationId] || []
    },

    async sendMessage(content: string) {
      if (!this.currentConversationId) {
        // 创建新对话
        await this.createConversation()
      }

      const conversationId = this.currentConversationId!
      const modelStore = useModelStore()
      const modeStore = useModeStore()
      const settingsStore = useSettingsStore()

      // 保存用户消息
      const userMessage = await api.post(`/conversations/${conversationId}/messages`, {
        role: 'user',
        content,
        token_count: 0,
      })

      if (!this.messages[conversationId]) {
        this.messages[conversationId] = []
      }
      this.messages[conversationId].push(userMessage)

      // 发送到 AI API
      const systemPrompt = generateSystemPrompt(modeStore.currentMode)
      const historyMessages = this.getMessages(conversationId)
        .slice(-settingsStore.settings.historyCount)
        .map(m => ({ role: m.role, content: m.content }))

      const messages = [
        { role: 'system', content: systemPrompt },
        ...historyMessages,
        { role: 'user', content },
      ]

      // SSE 流式响应 - 通过后端代理
      let assistantContent = ''
      const assistantMessageId = Date.now() // 临时ID

      try {
        const response = await fetch('http://localhost:8000/api/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${api.token || localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            model: modelStore.currentModel,
            messages,
            stream: true,
            temperature: settingsStore.settings.temperature,
            max_tokens: settingsStore.settings.maxTokens,
          }),
        })

        const reader = response.body?.getReader()
        const decoder = new TextDecoder()

        if (!reader) throw new Error('No reader')

        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          const chunk = decoder.decode(value)
          const lines = chunk.split('\n')

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6)
              if (data === '[DONE]') continue

              try {
                const json = JSON.parse(data)
                const delta = json.choices?.[0]?.delta?.content
                if (delta) {
                  assistantContent += delta
                  // 实时更新消息
                  const tempMessage = this.messages[conversationId].find(m => m.id === assistantMessageId)
                  if (tempMessage) {
                    tempMessage.content = assistantContent
                  } else {
                    this.messages[conversationId].push({
                      id: assistantMessageId,
                      conversation_id: conversationId,
                      role: 'assistant',
                      content: assistantContent,
                      token_count: 0,
                      created_at: new Date().toISOString(),
                    })
                  }
                }

                // 处理 usage
                if (json.usage) {
                  const tokenCount = json.usage.total_tokens || 0
                  // 保存助手消息
                  const assistantMessage = await api.post(`/conversations/${conversationId}/messages`, {
                    role: 'assistant',
                    content: assistantContent,
                    token_count: tokenCount,
                  })

                  // 更新消息
                  const index = this.messages[conversationId].findIndex(m => m.id === assistantMessageId)
                  if (index !== -1) {
                    this.messages[conversationId][index] = assistantMessage
                  }

                  // 扣除积分
                  const creditStore = useCreditStore()
                  await creditStore.deductCredits({
                    conversation_id: conversationId,
                    message_id: assistantMessage.id,
                    token_count: tokenCount,
                    mode: modeStore.currentMode,
                  })

                  // 如果是第一条消息，生成标题
                  if (this.messages[conversationId].filter(m => m.role === 'user').length === 1) {
                    await this.generateTitle(conversationId, content)
                  }
                }
              } catch (e) {
                // 忽略解析错误
              }
            }
          }
        }
      } catch (error) {
        console.error('Failed to send message:', error)
        throw error
      }
    },

    async generateTitle(conversationId: number, firstMessage: string) {
      // 简单实现：截取前30个字符作为标题
      const title = firstMessage.slice(0, 30)
      await this.updateConversationTitle(conversationId, title)
    },

    async updateConversationTitle(conversationId: number, title: string) {
      try {
        const data = await api.put(`/conversations/${conversationId}`, { title })
        const index = this.conversations.findIndex(c => c.id === conversationId)
        if (index !== -1) {
          this.conversations[index] = data
        }
      } catch (error) {
        console.error('Failed to update title:', error)
      }
    },

    async deleteConversation(id: number) {
      try {
        await api.delete(`/conversations/${id}`)
        this.conversations = this.conversations.filter(c => c.id !== id)
        delete this.messages[id]
        if (this.currentConversationId === id) {
          this.currentConversationId = null
        }
      } catch (error) {
        console.error('Failed to delete conversation:', error)
        throw error
      }
    },
  },
})

function generateSystemPrompt(mode: string): string {
  const prompts = {
    AI: '你是一个有用的AI助手。',
    DOC: '你是一个文档分析助手，可以帮助用户分析和理解文档内容。',
    KB: '你是一个知识库检索助手，可以帮助用户从知识库中查找相关信息。',
    DB: '你是一个数据库查询助手，可以帮助用户查询和分析数据库。',
    WEB: '你是一个Web搜索助手，可以帮助用户搜索和分析网页内容。',
    IMG: '你是一个图片分析助手，可以帮助用户分析和理解图片内容。',
    MCP: '你是一个MCP协议助手，可以帮助用户使用MCP协议进行交互。',
  }
  return prompts[mode] || prompts.AI
}

