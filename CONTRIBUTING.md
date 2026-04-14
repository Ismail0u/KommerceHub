-----

# Contribution Guide — KommerceHub

Thank you for contributing to KommerceHub\! This guide covers everything you need to know to contribute effectively.

## Table of Contents

1.  [Code of Conduct](https://www.google.com/search?q=%23code-of-conduct)
2.  [How to Contribute](https://www.google.com/search?q=%23how-to-contribute)
3.  [Development Setup](https://www.google.com/search?q=%23development-setup)
4.  [Coding Conventions](https://www.google.com/search?q=%23coding-conventions)
5.  [Conventional Commits](https://www.google.com/search?q=%23conventional-commits)
6.  [Pull Request Process](https://www.google.com/search?q=%23pull-request-process)
7.  [Reporting a Bug](https://www.google.com/search?q=%23reporting-a-bug)
8.  [Proposing a Feature](https://www.google.com/search?q=%23proposing-a-feature)

-----

## Code of Conduct

This project adheres to the **Contributor Covenant**. By participating, you agree to abide by its terms.

## How to Contribute

### Finding Something to Work On

1.  Check [open issues](https://www.google.com/search?q=https://github.com/KommerceHub/kommercehub/issues).
2.  Filter by the `good first issue` label if you are a beginner.
3.  Filter by the `help wanted` label for priority issues.
4.  Comment on the issue to let others know you are taking it on.

### Contribution Workflow

**Fork → Clone → Branch → Code → Test → Commit → Push → Pull Request**

```bash
# Fork via the GitHub UI, then:
git clone https://github.com/YOUR_USERNAME/kommercehub.git
cd kommercehub
git remote add upstream https://github.com/Ismail0u/kommercehub.git

# Create a descriptive branch
git checkout -b feat/inventory-movement-management
# or
git checkout -b fix/offline-sync-stock-conflict
# or
git checkout -b docs/multi-tenant-architecture
```

-----

## Development Setup

### 1\. Django Backend

```bash
cd apps/api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements/dev.txt

# Environment variables
cp .env.example .env

# Start PostgreSQL + Redis via Docker
docker-compose up -d db redis

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Load demo data
python manage.py loaddata fixtures/demo.json

# Start the server
python manage.py runserver
```

### 2\. Web Frontend

```bash
cd apps/web
pnpm install
pnpm dev
```

### 3\. Mobile App

```bash
cd apps/mobile
pnpm install
npx expo start
```

### 4\. All-in-one (Docker)

```bash
# From the project root
docker-compose up
```

-----

## Coding Conventions

### Python / Django

  * **Formatter:** `ruff format` (replaces Black)
  * **Linter:** `ruff check`
  * **Type hints:** Mandatory on all public functions.
  * **Docstrings:** Google style.

<!-- end list -->

```python
# ✅ Good
def get_merchant_sales(merchant_id: UUID, days: int = 30) -> QuerySet:
    """
    Returns a merchant's sales over the last N days.

    Args:
        merchant_id: Merchant's UUID.
        days: Number of days to include.

    Returns:
        QuerySet of sales sorted by descending date.
    """
    since = timezone.now() - timedelta(days=days)
    return Sale.objects.filter(
        merchant_id=merchant_id,
        created_at__gte=since,
    ).order_by('-created_at')

# ❌ Bad
def getSales(m, d=30):
    return Sale.objects.filter(merchant_id=m)
```

**Critical Rule — Multi-tenancy:** Every ViewSet **MUST** filter by merchant in `get_queryset()`.

```python
# ✅ Mandatory in every ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Product.objects.filter(
            merchant=self.request.user.merchant
        )
```

### TypeScript / React

  * **Formatter:** Prettier
  * **Linter:** ESLint
  * **Styling:** TailwindCSS only (no CSS modules or styled-components).
  * **Components:** Functional components only, hooks.
  * **Props:** Explicit TypeScript interfaces.

<!-- end list -->

```typescript
// ✅ Good
interface SaleCardProps {
  sale: Sale;
  onCancel?: (id: string) => void;
}

export function SaleCard({ sale, onCancel }: SaleCardProps) {
  // ...
}

// ❌ Bad
export function SaleCard(props: any) {
  // ...
}
```

-----

## Conventional Commits

This project uses **Conventional Commits**. This format is mandatory—CI will reject non-compliant commits.

**Format:** `<type>(<scope>): <short description>`

**Types:**
| Type | Usage |
| :--- | :--- |
| **feat** | New feature |
| **fix** | Bug fix |
| **docs** | Documentation only |
| **style** | Formatting, white-space (no logic change) |
| **refactor** | Code change that neither fixes a bug nor adds a feature |
| **test** | Adding missing tests or correcting existing tests |
| **chore** | Maintenance, dependencies, CI |
| **perf** | Performance optimization |

**Scopes:** `api`, `web`, `mobile`, `auth`, `products`, `sales`, `analytics`, `notifications`, `subscriptions`, `docs`, `ci`, `docker`.

-----

## Tests

  * **Backend (Pytest):** `pytest`
  * **Frontend (Vitest):** `pnpm test`
  * **End-to-End (Playwright):** `pnpm test:e2e`

**Rule:** Any PR that drops test coverage below **80%** will be rejected.

-----

## Pull Request Process

### Before opening a PR:

  - [ ] Tests pass locally.
  - [ ] Coverage is at least 80%.
  - [ ] Code is formatted (`ruff format` / `Prettier`).
  - [ ] Commits follow Conventional Commits.
  - [ ] Branch is up to date with `main` (`git rebase upstream/main`).

### Review:

  * Minimum **1 approval** required before merging.
  * CI must pass (lint + tests + build).
  * All conversations must be resolved.

-----

## Reporting a Bug

Use the **bug report template**. Include:

  * Steps to reproduce.
  * Expected vs. observed behavior.
  * Environment (OS, Browser, Mobile version).
  * Error logs if available.

## Proposing a Feature

Use the **feature request template**. Discuss via an issue before starting to code to avoid unnecessary work.

**Thank you for contributing to KommerceHub\! 🙏**
