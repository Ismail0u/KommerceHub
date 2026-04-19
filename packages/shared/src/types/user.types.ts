export type UserRole = 'admin' | 'merchant' | 'seller'

export interface User {
  id: string
  email: string | null
  phone: string | null
  role: UserRole
  isActive: boolean
  mustChangePassword: boolean
  createdAt: string
}

export interface LoginMerchantPayload {
  email: string
  password: string
}

export interface LoginSellerPayload {
  phone: string
  password: string
}

export interface LoginResponse {
  user: User
  forcePasswordChange: boolean
}

export interface ChangePasswordPayload {
  currentPassword: string
  newPassword: string
  confirmPassword: string
}