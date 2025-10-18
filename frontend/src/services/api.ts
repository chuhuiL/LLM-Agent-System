import axios from 'axios'
import type {
  LoginCredentials,
  RegisterData,
  AuthTokens,
  User,
  Patient,
  Template
} from '@/types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const { data } = await axios.post<AuthTokens>(
            `${API_URL}/api/v1/auth/refresh`,
            { refresh_token: refreshToken }
          )

          localStorage.setItem('access_token', data.access_token)
          localStorage.setItem('refresh_token', data.refresh_token)

          originalRequest.headers.Authorization = `Bearer ${data.access_token}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

// Auth API
export const authApi = {
  async login(credentials: LoginCredentials): Promise<AuthTokens> {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const { data } = await api.post<AuthTokens>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    return data
  },

  async register(userData: RegisterData): Promise<User> {
    const { data } = await api.post<User>('/auth/register', userData)
    return data
  },

  async getCurrentUser(): Promise<User> {
    const { data } = await api.get<User>('/users/me')
    return data
  },
}

// Patient API
export const patientApi = {
  async list(search?: string): Promise<Patient[]> {
    const { data } = await api.get<Patient[]>('/patients', {
      params: { search },
    })
    return data
  },

  async get(id: number): Promise<Patient> {
    const { data } = await api.get<Patient>(`/patients/${id}`)
    return data
  },

  async create(patientData: Partial<Patient>): Promise<Patient> {
    const { data } = await api.post<Patient>('/patients', patientData)
    return data
  },

  async update(id: number, patientData: Partial<Patient>): Promise<Patient> {
    const { data } = await api.put<Patient>(`/patients/${id}`, patientData)
    return data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/patients/${id}`)
  },
}

// Template API
export const templateApi = {
  async list(type?: string): Promise<Template[]> {
    const { data } = await api.get<Template[]>('/templates', {
      params: { template_type: type },
    })
    return data
  },

  async get(id: number): Promise<Template> {
    const { data } = await api.get<Template>(`/templates/${id}`)
    return data
  },
}
