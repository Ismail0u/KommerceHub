export const USER_ROLES = {
  ADMIN: 'admin',
  MERCHANT: 'merchant',
  SELLER: 'seller',
} as const

export type UserRoleValue = (typeof USER_ROLES)[keyof typeof USER_ROLES]

export const ROLE_LABELS: Record<UserRoleValue, string> = {
  admin: 'Administrateur',
  merchant: 'Commerçant',
  seller: 'Vendeur',
}