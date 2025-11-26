class ApiClient {
  private baseURL: string
  private token: string | null = null

  constructor() {
    // 默认使用环境变量或硬编码的地址
    const apiBase = process.env.API_BASE_URL || 'http://localhost:8000'
    this.baseURL = apiBase + '/api/v1'
    
    // 从 localStorage 读取 token
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('access_token')
    }
  }

  setToken(token: string) {
    this.token = token
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token)
    }
  }

  clearToken() {
    this.token = null
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token')
    }
  }

  private async request<T>(
    method: string,
    endpoint: string,
    data?: any
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    }

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }

    const options: RequestInit = {
      method,
      headers,
    }

    if (data && method !== 'GET') {
      options.body = JSON.stringify(data)
    }

    const response = await fetch(url, options)

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: response.statusText }))
      throw { status: response.status, ...error }
    }

    return response.json()
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>('GET', endpoint)
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>('POST', endpoint, data)
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>('PUT', endpoint, data)
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>('DELETE', endpoint)
  }
}

export const api = new ApiClient()

