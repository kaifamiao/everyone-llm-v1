import { defineStore } from 'pinia'
import { api } from '~/services/api'

export interface User {
    id: number
    username: string
    email: string | null
    phone: string | null
    status: string
    created_at: string
}

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null as User | null,
        isAuthenticated: false,
    }),

    actions: {
        async login(username: string, password: string) {
            try {
                // FastAPI OAuth2PasswordRequestForm expects form data
                const formData = new URLSearchParams()
                formData.append('username', username)
                formData.append('password', password)

                const response = await fetch('http://localhost:8000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: formData,
                })

                if (!response.ok) {
                    const error = await response.json()
                    throw new Error(error.detail || 'Login failed')
                }

                const data = await response.json()
                api.setToken(data.access_token)

                // Get user info
                await this.loadUser()

                return data
            } catch (error: any) {
                console.error('Login error:', error)
                throw error
            }
        },

        async register(userData: {
            username: string
            password: string
            email?: string
            phone?: string
        }) {
            try {
                const data = await api.post('/auth/register', userData)
                return data
            } catch (error: any) {
                console.error('Register error:', error)
                throw error
            }
        },

        async loadUser() {
            try {
                const data = await api.get<User>('/auth/me')
                this.user = data
                this.isAuthenticated = true
            } catch (error) {
                console.error('Failed to load user:', error)
                this.logout()
            }
        },

        async logout() {
            try {
                await api.post('/auth/logout')
            } catch (error) {
                console.error('Logout error:', error)
            } finally {
                api.clearToken()
                this.user = null
                this.isAuthenticated = false
            }
        },

        async checkAuth() {
            const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null
            if (token) {
                await this.loadUser()
            }
        },
    },
})
