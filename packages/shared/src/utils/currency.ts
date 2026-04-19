export function formatCurrency(amount: number, currency = 'XOF'): string {
  if (currency === 'XOF') {
    return `${amount.toLocaleString('fr-FR')} FCFA`
  }
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency,
  }).format(amount)
}

export function calculateTotal(
  items: Array<{ quantity: number; unitPrice: number }>
): number {
  return items.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0)
}