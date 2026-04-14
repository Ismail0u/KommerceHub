# Technical Architecture — KommerceHub

## Overview

KommerceHub is a multi-tenant SaaS platform built around three distinct applications sharing common business logic via a Turborepo monorepo.

```
┌─────────────────────────────────────────────────────────────────┐
│                             CLIENTS                             │
├──────────────────┬──────────────────┬───────────────────────────┤
│    Web (React)   │   Mobile (RN)    │      Admin Back-office    │
│    Port 5173     │   Android APK    │      /admin/* routes      │
└────────┬─────────┴────────┬─────────┴──────────┬────────────────┘
         │                  │                    │
         └──────────────────┼────────────────────┘
                            │ HTTPS / REST API
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Django REST Framework API                    │
│                            Port 8000                            │
│                                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────────┐  │
│  │   auth   │ │merchants │ │ products │ │       sales       │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────────┐  │
│  │analytics │ │  notify  │ │  sellers │ │   subscriptions   │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────────────┘  │
└──────┬────────────────────────────────────────────┬─────────────┘
       │                                            │
       ▼                                            ▼
┌─────────────┐                            ┌─────────────────────┐
│ PostgreSQL  │                            │       Redis 7       │
│     16      │                            │   Cache + Sessions  │
│   ACID TX   │                            │  (+ Celery broker)  │
└─────────────┘                            └─────────────────────┘
```

---

## Multi-tenancy

### Data Isolation Model

KommerceHub uses **logical isolation via `merchant_id`** within a shared database (Shared Schema approach).

```
Merchant A ──┐
             ├── All data filtered by merchant_id
Merchant B ──┘

Isolation guaranteed by:
1. get_queryset() override in every Django ViewSet
2. Automated isolation integration tests
3. Database-level Foreign Key constraints
```

### Required Pattern

```python
# Every ViewSet MUST implement this pattern
class AnyViewSet(viewsets.ModelViewSet):
    def get_queryset(self) -> QuerySet:
        user = self.request.user
        if user.role == UserRole.ADMIN:
            return Model.objects.all()  # Admin has global visibility
        return Model.objects.filter(
            merchant=user.merchant,
            is_deleted=False,
        )
```

---

## Authentication & Authorization

### JWT Flow

```
Client                        API                        Redis/DB
  │                            │                             │
  │─── POST /auth/login ──────▶│                             │
  │    {email, password}       │── Verify credentials ─────▶│
  │                            │◀─ Valid User ──────────────│
  │◀── 200 OK ─────────────────│                             │
  │    access_token (15min)    │── Store refresh token ────▶│
  │    refresh_token (7d)      │                             │
  │    [httpOnly cookie]       │                             │
  │                            │                             │
  │─── GET /api/products/ ────▶│                             │
  │    Authorization: Bearer ..│── Verify + Decode JWT ────▶│
  │                            │◀─ Valid Token ─────────────│
  │◀── 200 OK ─────────────────│                             │
  │                            │                             │
  │─── POST /auth/refresh/ ───▶│                             │
  │    [cookie refresh_token]  │── Validate + Rotation ────▶│
  │◀── 200 OK (new token) ─────│◀─ New refresh token ───────│
```

### RBAC — Permissions Matrix

| Permission | Admin | Merchant | Seller |
|---|---|---|---|
| Validate Merchant | ✅ | ❌ | ❌ |
| Product CRUD | ✅ | ✅ | ❌ |
| Record a Sale | ✅ | ✅ | ✅ |
| Cancel a Sale | ✅ | ✅ | ❌ |
| View All Sales | ✅ | ✅ (Own Shop) | ❌ (Own only) |
| Full Dashboard | ✅ | ✅ | ❌ |
| Global Analytics | ✅ | ❌ | ❌ |

---

## Offline-First Architecture (Mobile)

### Core Principle

> **Mobile sends EVENTS, not STATES.**

```
❌ Bad (State):  PATCH /products/123/ { stock_qty: 7 }
✅ Good (Event): POST /sales/ { items: [{product: 123, qty: 3}] }
```

### Synchronization Strategy



```
Mobile (WatermelonDB)                 Backend (PostgreSQL)
       │                                          │
       │  [Offline] Record Sale                   │
       │  Sale { status: PENDING_SYNC }           │
       │  Local Stock = local_stock - qty         │
       │                                          │
       │  [Reconnection detected - NetInfo]       │
       │                                          │
       │─── POST /api/sync/push/ ───────────────▶│
       │    { sales: [...pending_sync_sales] }    │ ← Batch
       │                                          │
       │                               ┌──────────┤
       │                               │ For each sale:
       │                               │ BEGIN TRANSACTION
       │                               │ SELECT stock FOR UPDATE
       │                               │ IF stock >= qty THEN
       │                               │   stock = stock - qty (DELTA)
       │                               │   INSERT Sale
       │                               │ ELSE
       │                               │   CONFLICT → Return error
       │                               │ COMMIT
       │                               └──────────┤
       │                                          │
       │◀── 200 { synced: [...], conflicts: [...] }
       │                                          │
       │  [Handle Conflicts]                      │
       │  Conflicting Sale → status CONFLICT      │
       │  Notify Merchant                         │
```

### Offline Sale States

```
PENDING_SYNC → (Successful sync) → SYNCED
             → (Stock conflict)  → CONFLICT
             → (Network error)   → PENDING_SYNC (retry)
```

---

## Data Model

### BaseModel (Universal Inheritance)

```python
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """Soft delete — never physically remove data."""
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])
```

### Simplified Relationship Schema

```
User (1) ──── (1) Merchant ──── (N) Seller
                    │
                    ├──── (N) Product ──── (N) StockMovement
                    │           │
                    │           └──── (N) SaleItem
                    │
                    ├──── (N) Sale ──────── (N) SaleItem
                    │           │
                    │           └──── (1) Seller
                    │
                    ├──── (1) Subscription
                    └──── (N) Notification
```

---

## Caching Strategy (Redis)

```python
# Dashboard KPIs — 30s cache (auto-refresh on frontend)
CACHE_TTL = {
    "dashboard_kpis": 30,          # seconds
    "top_products": 60,            # 1 minute
    "sales_by_payment": 300,       # 5 minutes
    "monthly_revenue": 1800,       # 30 minutes
}

# Cache key pattern (Multi-tenant isolation)
def get_cache_key(merchant_id: str, metric: str) -> str:
    return f"analytics:{merchant_id}:{metric}"
```

---

## CI/CD Pipeline

```
Push / PR
    │
    ▼
┌─────────────────────────────────────────────┐
│               GitHub Actions                │
│                                             │
│  ① Lint ──────── ESLint + Ruff (< 2min)     │
│  ② Tests ─────── Pytest + Vitest (< 5min)   │
│  ③ Build ─────── Docker build (< 3min)      │
│  ④ Coverage ──── PR Comment                 │
└────────────────────┬────────────────────────┘
                     │ If merge to main
                     ▼
              Deploy → Staging (Render)
                     │ If tag vX.Y.Z
                     ▼
              Deploy → Production
```

---

## Security — Checkpoints

| Checkpoint | Implementation |
|---|---|
| Multi-tenant Isolation | `get_queryset()` filter by merchant |
| Authentication | JWT HS256, refresh token rotation |
| Web Token Storage | httpOnly cookie (anti-XSS) |
| Mobile Token Storage | Expo SecureStore (keychain/keystore) |
| Password Hashing | Argon2 (OWASP recommended) |
| Transport | HTTPS + HSTS |
| CORS | Whitelist allowed domains only |
| Rate Limiting | 100 req/min (public) / 1000 req/min (auth) |
| CSRF | Django CSRF middleware active |
| SQL Injection | Django ORM (parameterized queries) |
| Audit Logs | All sensitive actions tracked |
| Secrets | Environment variables (never hardcoded) |