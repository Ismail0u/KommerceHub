# KommerceHub

**Open Source SaaS Platform for Multi-channel Commercial Management tailored for the African context.**

## Vision & Context

In many Sub-Saharan regions, particularly in Niger, local merchants still rely on manual ledgers or fragmented spreadsheets. **KommerceHub** aims to bridge this digital gap by providing a robust, **offline-first** solution that synchronizes sales, inventory, and mobile payments (Wave, Airtel Money, Mynita) into a single, easy-to-use ecosystem.

By choosing the **AGPL-3.0 license**, we ensure that the platform remains open and that any commercial improvements made by third parties benefit the entire community.

## Key Features (MVP 1.0)

  - **Unified Inventory Management**: Real-time tracking across multiple warehouses with low-stock automated alerts.
  - **Offline-First Mobile POS**: A React Native application allowing field agents to process sales without an internet connection, with background synchronization.
  - **Multitenancy Architecture**: Designed as a SaaS where each merchant manages their own isolated environment.
  - **Local Payment Integration**: Native support for popular West African mobile money APIs.
  - **Professional Reporting**: Dynamic generation of PDF invoices and thermal receipts using WeasyPrint.

## Tech Stack

We utilize a modern, scalable architecture designed for performance and reliability:

  - **Backend**: [Django REST Framework](https://www.django-rest-framework.org/) (Python) — Chosen for its security, robust ORM, and rapid development capabilities.
  - **Frontend Web**: [React](https://react.dev/) + Vite + Tailwind CSS — Providing a high-performance, responsive administrative dashboard.
  - **Mobile**: [React Native](https://reactnative.dev/) (Expo) — Ensuring a smooth cross-platform experience (Android/iOS) with specialized offline storage.
  - **Database**: PostgreSQL (Structured data) & Redis (Caching/Tasks).
  - **Deployment**: Fully containerized using **Docker** for "one-command" environment setup.

##  Project Structure

```bash
kommercehub/
├── backend/      # Django REST API (Business logic, Auth, DB)
├── frontend/     # React Web App (Merchant Dashboard)
├── mobile/       # React Native App (Sales & Field Operations)
├── docker/       # Dockerfiles & Orchestration
└── docs/         # Full functional & technical specifications
```

##  Quick Start (Development Mode)

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/Ismail0u/kommercehub.git
    cd kommercehub
    ```

2.  **Launch with Docker**:

    ```bash
    docker-compose up --build
    ```

    *The API will be available at `localhost:8000` and the Web Dashboard at `localhost:5173`.*

## Contribution & License

This project is licensed under the **GNU Affero General Public License v3.0**.

  - **Commercial use**: Allowed, but you must share your source code if you host it as a service.
  - **Contributions**: We welcome PRs\! Please check our `docs/` folder for the full functional requirements before submitting changes.

-----
**Developed by [Moussa Ismael](https://github.com/Ismail0u) & Yahyah Gamazo Kabirou.**




