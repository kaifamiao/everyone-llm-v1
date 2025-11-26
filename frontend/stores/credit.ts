import { defineStore } from 'pinia'
import { api } from '~/services/api'

export const useCreditStore = defineStore('credit', {
  state: () => ({
    credits: 100000,
  }),

  actions: {
    async loadCredits() {
      try {
        const data = await api.get('/user/credits')
        this.credits = data.credits
      } catch (error) {
        console.error('Failed to load credits:', error)
      }
    },

    async deductCredits(params: {
      conversation_id: number
      message_id: number
      token_count: number
      mode: string
    }) {
      try {
        const data = await api.post('/user/credits/deduct', params)
        this.credits = data.remaining_credits
      } catch (error: any) {
        if (error.status === 429) {
          alert('积分不足，请充值')
        }
        throw error
      }
    },
  },
})

