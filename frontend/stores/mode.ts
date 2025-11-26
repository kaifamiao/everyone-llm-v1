import { defineStore } from 'pinia'

export const useModeStore = defineStore('mode', {
  state: () => ({
    currentMode: 'AI',
  }),

  actions: {
    setMode(mode: string) {
      this.currentMode = mode
    },
  },
})

