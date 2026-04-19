export interface Product {
  id: string
  merchantId: string
  name: string
  category: string | null
  price: number
  stockQty: number
  lowStockThreshold: number
  barcode: string | null
  image: string | null
  createdAt: string
  updatedAt: string
}

export interface CreateProductPayload {
  name: string
  category?: string
  price: number
  stockQty: number
  lowStockThreshold?: number
  barcode?: string
}

export type StockMovementType = 'in' | 'out' | 'adjustment'

export interface StockMovement {
  id: string
  productId: string
  type: StockMovementType
  quantity: number
  reason: string
  createdBy: string
  createdAt: string
}