import type { PaymentMethod } from '../constants/payment-methods'

export type SaleStatus = 'completed' | 'cancelled'
export type SaleSyncStatus = 'pending' | 'synced' | 'conflict'

export interface SaleItem {
  id: string
  productId: string
  productName: string
  quantity: number
  unitPrice: number
  subtotal: number
}

export interface Sale {
  id: string
  merchantId: string
  sellerId: string
  sellerName: string
  items: SaleItem[]
  totalAmount: number
  paymentMethod: PaymentMethod
  status: SaleStatus
  notes: string | null
  createdAt: string
  cancellationReason: string | null
}

export interface CreateSalePayload {
  items: Array<{ productId: string; quantity: number }>
  paymentMethod: PaymentMethod
  notes?: string
}

export interface CancelSalePayload {
  reason: string
}