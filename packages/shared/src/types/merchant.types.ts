export interface Merchant {
  id: string
  name: string
  logo: string | null
  currency: string
  sector: string | null
  isValidated: boolean
  createdAt: string
}

export interface CreateMerchantPayload {
  name: string
  email: string
  phone: string
  password: string
  sector?: string
}