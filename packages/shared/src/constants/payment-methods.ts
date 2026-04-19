export const PAYMENT_METHODS = {
  CASH: 'cash',
  WAVE: 'wave',
  AIRTEL_MONEY: 'airtel_money',
  MYNITA: 'mynita',
  CARD: 'card',
} as const

export type PaymentMethod = (typeof PAYMENT_METHODS)[keyof typeof PAYMENT_METHODS]

export const PAYMENT_METHOD_LABELS: Record<PaymentMethod, string> = {
  cash: 'Espèces',
  wave: 'Wave',
  airtel_money: 'Airtel Money',
  mynita: 'Mynita',
  card: 'Carte bancaire',
}