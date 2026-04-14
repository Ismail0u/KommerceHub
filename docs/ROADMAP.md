### KommerceHub Roadmap
**Last Updated:** March 2026

This roadmap reflects our current priorities. It is public and evolves based on user feedback.

#### Status Legend
| Icon | Status |
| :--- | :--- |
| ✅ | **Completed** |
| 🔄 | **In Progress** |
| 📋 | **Planned** |
| 💡 | **In Review / Brainstorming** |
| ❌ | **Out of Scope for MVP** |

---

### Month 1 — Foundations (April 2026)

#### Infrastructure & DevOps
* 📋 Setup Turborepo monorepo
* 📋 Docker Compose (API + PostgreSQL + Redis)
* 📋 CI/CD GitHub Actions (lint + tests + build + deploy staging)
* 📋 Semantic versioning (Conventional Commits)

#### Backend — Core
* 📋 Abstract models (BaseModel: UUID, timestamps, soft delete)
* 📋 `core/` module — mixins, utils, constants
* 📋 `authentication/` module — JWT, RBAC, first-login flow
* 📋 `merchants/` module — Merchant profile, tenant root
* 📋 `sellers/` module — Sellers CRUD, temporary passwords
* 📋 Auto-generated OpenAPI / Swagger documentation

#### Web Frontend
* 📋 Setup React 18 + Vite + Tailwind + Shadcn/ui
* 📋 Role-based routing (Admin / Merchant / Seller)
* 📋 Screens: Login, First-login, Reset password

#### Mobile
* 📋 Setup React Native + Expo SDK 51 + WatermelonDB
* 📋 React Navigation — role-based navigation structure
* 📋 Mandatory first-login password change screen (blocking)
* 📋 Expo SecureStore — secure JWT storage

#### Design
* 📋 Figma Design System — UI components and brand guidelines

---

### Month 2 — Core Features (May 2026)

#### Backend
* 📋 `products/` module — CRUD products, categories, stock movements
* 📋 `sales/` module — Sales recording, SaleItems, tracked cancellations
* 📋 PDF Sales Receipt generation (ReportLab)
* 📋 `notifications/` module — Low stock alerts (decoupled, Celery-ready)
* 📋 Celery Worker + Redis (async notifications)

#### Web Frontend
* 📋 Products CRUD — List, create, edit, delete, images
* 📋 Sales Recording — Product selection, total calculation, payment methods
* 📋 Sales History — Filters, full-text search, cancellation
* 📋 Low stock alerts — Toasts and notifications

#### Mobile
* 📋 Offline-first sales (WatermelonDB + pending_sync)
* 📋 Auto-sync on network return (NetInfo + delta events)
* 📋 Barcode scanning (Expo Camera + ML Kit)
* 📋 PDF Sales Receipt (View + Share)
* 📋 Low stock push notifications (Expo Notifications)

#### Testing
* 📋 Backend coverage > 80% (blocking in CI)
* 📋 Frontend unit tests (Vitest)

---

### Month 3 — Dashboard, Reporting & Pilot (June 2026)

#### Backend
* 📋 `analytics/` module — KPI aggregation, top products, seller rankings
* 📋 On-demand CSV and PDF exports
* 📋 `subscriptions/` module — Table structure (logic enabled post-MVP)

#### Web Frontend
* 📋 Full Dashboard — Daily KPIs, 7d/30d revenue trends, Recharts graphs
* 📋 Seller rankings by revenue
* 📋 Sales distribution by payment method
* 📋 CSV / PDF exports from the dashboard
* 📋 30s auto-refresh

#### Mobile
* 📋 Seller Dashboard — Daily KPIs + personal history

#### Admin Back-office
* 📋 React Admin — Merchant validation, transaction supervision
* 📋 Global Admin Dashboard

#### Deployment & Pilot
* 📋 Playwright E2E tests (critical paths)
* 📋 Production deployment (Render / AWS)
* 📋 Final technical documentation (Docusaurus)
* 📋 Realistic demo fixtures (10 merchants, 500 sales)
* 📋 Onboarding of 10 pilot merchants in Niger
* 📋 Pilot report — Field feedback, metrics, post-MVP prioritization

---

### Post-MVP (Q3–Q4 2026)

#### Payments & Monetization
* 💡 Wave Integration (Payment API)
* 💡 Airtel Money Integration
* 💡 Mynita Integration
* 💡 Pro and Business Plans — Subscription logic activation
* 💡 Stripe (International market)

#### Features
* 💡 iOS Support
* 💡 OAuth (Google, Facebook)
* 💡 Daily email reports (Celery)
* 💡 Multi-shop support per merchant (1-N)
* 💡 Product import via CSV/Excel
* 💡 Public API for third-party integrations

#### Infrastructure
* 💡 APM Monitoring (Prometheus + Grafana)
* 💡 Log aggregation (Loki)
* 💡 Multi-region deployment

---

### Definitive Out of Scope
* ❌ Full accounting software
* ❌ Advanced CRM
* ❌ E-commerce / Online storefront

To propose a feature: [Feature Request](https://github.com/Ismail0u/kommercehub/issues/new?template=feature_request.yml)*