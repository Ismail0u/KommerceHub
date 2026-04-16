# KommerceHub

**Open Source Multi-channel Commercial Management SaaS Platform tailored for the African context.**

[](https://www.google.com/search?q=%5Bhttps://opensource.org/licenses/AGPL-3.0%5D\(https://opensource.org/licenses/AGPL-3.0\))
[](https://www.djangoproject.com/)
[](https://reactjs.org/)
[](https://expo.dev/)

-----

## Vision & Context

In Sub-Saharan Africa-specifically in **Niger**-local merchants predominantly operate using manual paper ledgers or un-synchronized spreadsheets, leading to zero real-time visibility **KommerceHub** bridges this gap by providing an **offline-first** SaaS solution designed for local constraints: intermittent connectivity and a strong mobile money culture.

By choosing the **AGPL-3.0 license**, we ensure the platform remains open-source while remaining economically viable—similar to the models used by Cal.com or Documenso

-----

##  Key Features (MVP 1.0)

  * **Strict Multi-tenant Architecture**: Every API request is filtered by `merchant_id` to ensure absolute data isolation.
  * **Offline-First Mobile POS**: Full sales processing capability without internet, using WatermelonDB for local storage and automatic background sync.
  * **Inventory & Stock Management**: Full CRUD for products with automated low-stock alerts and movement history.
  * **Sales & Digital Receipts**: Rapid sales registration with automatic PDF ticket generation.
  * **Local Payment Tracking**: Native support for recording payments via **Wave, Airtel Money, Mynita**, and Cash.
  * **RBAC Security**: Three distinct access levels (Platform Admin, Merchant, Seller) enforced at the backend level.

-----

## Tech Stack

  * **Backend**: Django 5 & Django REST Framework with JWT authentication.
  * **Web Dashboard**: React 18, Vite, Tailwind CSS, and Shadcn/ui.
  * **Mobile App**: React Native (Expo SDK 51) using the Hermes engine.
  * **Database & Cache**: PostgreSQL 16 for ACID transactions and Redis 7 for dashboard caching.
  * **DevOps**: Monorepo architecture managed by **Turborepo** with full Docker containerization.

-----

## Project Structure (Monorepo)

```bash
kommercehub/
├── apps/
│   ├── api/          # Django 5 REST API (Business logic & Multi-tenancy) 
│   ├── web/          # React Frontend (Advanced Merchant Dashboard) 
│   └── mobile/       # React Native App (Field Sales & Offline sync) 
├── packages/
│   ├── shared/       # Shared TypeScript types, constants, and Zustand stores 
│   └── ui/           # Shared UI components (Phase 2) 
├── docker-compose.yml # Local orchestration (API + DB + Redis) 
└── docs/             # Technical & Functional specifications 
```

-----

##  Quick Start (Development)

### Prerequisites

  * Docker and Docker Compose installed.
  * Node.js (for monorepo management).

### Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/Ismail0u/KommerceHub.git
    cd kommercehub
    ```

2.  **Launch the full environment**:

    ```bash
    docker-compose up --build
    ```

<!-- end list -->

  * **API (Swagger)**: `http://localhost:8000/api/schema/swagger-ui/`
  * **Web Dashboard**: `http://localhost:5173`

-----

##  Contribution & License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

  * **Commercial Use**: Permitted, but you **must** share your source code and modifications if you host KommerceHub as a service.
  * **Contributions**: We welcome PRs\! Please follow the **Conventional Commits** standard and check our `CONTRIBUTING.md` before submitting.

Developed by **Moussa Ismael** & **Yahyah Gamazo Kabirou** (April 2026).





