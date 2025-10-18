export interface User {
  id: number
  email: string
  role: 'clinician' | 'admin' | 'patient'
  is_active: boolean
  is_verified: boolean
  created_at: string
  last_login: string | null
  profile?: UserProfile
}

export interface UserProfile {
  id: number
  first_name: string
  last_name: string
  specialty?: string
  license_number?: string
  phone?: string
  preferences?: Record<string, any>
}

export interface LoginCredentials {
  username: string  // email
  password: string
}

export interface RegisterData {
  email: string
  password: string
  role: 'clinician' | 'admin' | 'patient'
  first_name: string
  last_name: string
  specialty?: string
  license_number?: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface Patient {
  id: number
  mrn: string
  first_name: string
  last_name: string
  middle_name?: string
  date_of_birth: string
  gender?: string
  email?: string
  phone?: string
  address?: Record<string, any>
  demographics?: Record<string, any>
  is_active: boolean
  created_at: string
  updated_at?: string
}

export interface Template {
  id: number
  name: string
  template_type: 'soap' | 'hp' | 'progress' | 'discharge' | 'consult' | 'custom'
  description?: string
  structure_json: Record<string, any>
  specialty?: string
  version: number
  is_system: boolean
  created_at: string
}
