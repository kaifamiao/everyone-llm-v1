import { defineStore } from 'pinia'

export const useModelStore = defineStore('model', {
  state: () => ({
    currentModel: 'gpt-4o',
  }),

  actions: {
    setModel(model: string) {
      this.currentModel = model
    },
  },
})

