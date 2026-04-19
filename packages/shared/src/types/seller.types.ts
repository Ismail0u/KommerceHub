export interface Seller {
  id: string
  merchantId: string
  fullName: string
  phone: string
  isActive: boolean
  tempPasswordExpiresAt: string | null
  createdAt: string
}

export interface CreateSellerPayload {
  fullName: string
  phone: string
}

export interface RegeneratePasswordResponse {
  temporaryPassword: string
  expiresAt: string
}