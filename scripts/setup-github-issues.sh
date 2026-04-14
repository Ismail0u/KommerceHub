#!/usr/bin/env bash
# =============================================================================
# setup-github-issues.sh
# Creates all GitHub issues for the KommerceHub MVP
#
# Prerequisites: GitHub CLI installed and authenticated (gh auth login)
# Usage: ./scripts/setup-github-issues.sh kommercehub/kommercehub
# =============================================================================

set -euo pipefail

REPO="${1:-kommercehub/kommercehub}"
M1="Month 1 — Foundations"
M2="Month 2 — Core Features"
M3="Month 3 — Dashboard & Pilot"

echo "📋 Creating GitHub issues for: $REPO"
echo ""

create_issue() {
  local title="$1"
  local body="$2"
  local labels="$3"
  local milestone="$4"

  gh issue create \
    --repo "$REPO" \
    --title "$title" \
    --body "$body" \
    --label "$labels" \
    --milestone "$milestone"

  echo "  ✅ $title"
}

# ==============================================================================
# EPIC — Month 1: Foundations
# ==============================================================================
echo ""
echo "🗺️  EPIC — Month 1: Foundations"

create_issue \
  "[EPIC] Foundations — Setup & Infrastructure" \
  "## Objective
Set up the project foundations: monorepo, Docker, CI/CD, and development environment.

## Child Issues
### Infrastructure & DevOps
- [ ] #
- [ ] #

### Documentation
- [ ] #

## Acceptance Criteria
- [ ] \`pnpm install && pnpm dev\` starts all local services
- [ ] CI passes on every PR
- [ ] README allows an external developer to start in < 10 minutes" \
  "type: epic,platform: devops,priority: critical" \
  "$M1"

create_issue \
  "[EPIC] Authentication & RBAC" \
  "## Objective
Implement the complete authentication system: JWT, RBAC roles, seller first-login flow, and password reset.

## Child Issues
### Backend
- [ ] #
- [ ] #

### Web Frontend
- [ ] #
- [ ] #

### Mobile
- [ ] #

## Acceptance Criteria
- [ ] A merchant can register and log in via email
- [ ] A seller can log in via phone + temporary password
- [ ] First-login flow blocks all navigation until password change (API side)
- [ ] An admin can validate a merchant from the back-office
- [ ] JWT tokens are in httpOnly cookies (web) and Expo SecureStore (mobile)" \
  "type: epic,module: auth,priority: critical" \
  "$M1"

# ==============================================================================
# MONTH 1 — Infrastructure
# ==============================================================================
echo ""
echo "🔧 Month 1 — Infrastructure"

create_issue \
  "feat(devops): setup Turborepo monorepo with pnpm workspaces" \
  "## Description
Initialize the Turborepo monorepo structure.

## Tasks
- [ ] Initialize repo with \`npx create-turbo@latest\`
- [ ] Configure \`pnpm-workspace.yaml\` (apps/web, apps/mobile, packages/shared)
- [ ] Configure \`turbo.json\` — pipelines: build, test, lint, dev
- [ ] Create \`packages/shared/\` with base TypeScript types (User, Merchant, Seller, Product, Sale)
- [ ] Configure base \`tsconfig.json\` (strict mode)
- [ ] Verify that \`pnpm dev\` launches web + api in parallel

## Acceptance Criteria
- [ ] \`pnpm build\` compiles all packages without error
- [ ] \`pnpm lint\` and \`pnpm test\` work from the root
- [ ] Types from \`packages/shared\` are importable in \`apps/web\`

## Technical Notes
See [ADR-001](../docs/ARCHITECTURE.md#adr-001--monorepo-turborepo) for architectural decisions." \
  "type: feature,platform: devops,status: ready,priority: critical" \
  "$M1"

create_issue \
  "feat(devops): Docker Compose — API + PostgreSQL + Redis" \
  "## Description
Configure Docker Compose for the local development environment.

## Tasks
- [ ] \`docker-compose.yml\` with services: db (PostgreSQL 16), redis (Redis 7), api (Django)
- [ ] Multi-stage \`Dockerfile\` for Django backend (dev + prod)
- [ ] \`.env.example\` with all required variables and default dev values
- [ ] Health checks for db and redis
- [ ] Persistent volume for PostgreSQL (data survives \`docker-compose down\`)
- [ ] Init script: \`docker-compose up -d db redis && python manage.py migrate\`

## Acceptance Criteria
- [ ] \`docker-compose up -d\` starts all services
- [ ] Django API can connect to PostgreSQL and Redis
- [ ] PostgreSQL data persists between restarts
- [ ] \`docker-compose.yml\` is documented (comments on each service)" \
  "type: feature,platform: devops,status: ready,priority: critical" \
  "$M1"

create_issue \
  "feat(ci): GitHub Actions pipeline — lint, tests, build, deploy staging" \
  "## Description
Configure the complete CI/CD pipeline on GitHub Actions.

## Tasks
- [ ] Job \`lint-backend\`: Ruff check + format check
- [ ] Job \`test-backend\`: Pytest with PostgreSQL and Redis service containers, coverage > 80%
- [ ] Job \`lint-frontend\`: ESLint + TypeScript type check
- [ ] Job \`test-frontend\`: Vitest with coverage report
- [ ] Job \`build\`: Build web app + shared packages
- [ ] Job \`deploy-staging\`: Automatic deployment to Render on merge to \`develop\`
- [ ] Upload coverage to Codecov
- [ ] Comment on PR with staging link after deployment
- [ ] Configure GitHub secrets: \`CODECOV_TOKEN\`, \`RENDER_API_KEY\`, \`RENDER_STAGING_SERVICE_ID\`

## Acceptance Criteria
- [ ] CI triggers on every PR and push to main/develop
- [ ] Coverage < 80% fails the CI
- [ ] Staging deploy is automatic on develop merge
- [ ] Total CI time < 5 minutes

## Reference
See the already created \`.github/workflows/ci.yml\` file." \
  "type: feature,platform: devops,status: ready,priority: critical" \
  "$M1"

# ==============================================================================
# MONTH 1 — Backend Auth
# ==============================================================================
echo ""
echo "🔐 Month 1 — Backend Authentication"

create_issue \
  "feat(api): BaseModel — UUID, timestamps, soft delete" \
  "## Description
Create the abstract base model from which all project models will inherit.

## Tasks
- [ ] Create \`apps/api/core/models.py\` with \`BaseModel\`
- [ ] Fields: \`id\` (UUIDField, primary_key=True, default=uuid4), \`created_at\`, \`updated_at\`, \`is_deleted\`
- [ ] Custom manager \`ActiveManager\` that filters \`is_deleted=False\` by default
- [ ] \`soft_delete()\` method that sets \`is_deleted=True\` and \`updated_at=now()\`
- [ ] Unit tests for BaseModel

## Starter Code
\`\`\`python
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        self.is_deleted = True
        self.save(update_fields=['is_deleted', 'updated_at'])
\`\`\`

## Acceptance Criteria
- [ ] All project models inherit from BaseModel
- [ ] \`Model.objects.all()\` never returns deleted objects
- [ ] \`Model.all_objects.all()\` returns everything, including deleted
- [ ] Tests: soft delete, manager, auto-generated UUID" \
  "type: feature,module: auth,platform: api,status: ready,priority: critical,good first issue" \
  "$M1"

create_issue \
  "feat(api): User model with RBAC roles (Admin, Merchant, Seller)" \
  "## Description
Create the custom User model with the RBAC role system.

## Tasks
- [ ] Create a custom \`AbstractUser\` in \`authentication/models.py\`
- [ ] Enum \`UserRole\`: \`ADMIN\`, \`MERCHANT\`, \`SELLER\`
- [ ] Specific fields: \`phone\` (unique, nullable), \`role\`, \`must_change_password\`
- [ ] Configure \`AUTH_USER_MODEL = 'authentication.User'\` in settings
- [ ] RBAC permission classes: \`IsAdmin\`, \`IsMerchant\`, \`IsSeller\`, \`IsMerchantOrSeller\`
- [ ] Permission tests

## Acceptance Criteria
- [ ] User model is configured as AUTH_USER_MODEL
- [ ] A User can have the role MERCHANT (email login) or SELLER (phone login)
- [ ] Permission classes correctly return True/False based on role
- [ ] Clean migration without conflicts with default Django apps" \
  "type: feature,module: auth,platform: api,status: ready,priority: critical" \
  "$M1"

create_issue \
  "feat(api): JWT authentication — merchant (email) and seller (phone) login" \
  "## Description
Implement JWT authentication endpoints for both user types.

## Tasks
- [ ] Configure \`djangorestframework-simplejwt\`: 15min access, 7 days refresh, rotation enabled
- [ ] Endpoint \`POST /api/v1/auth/login/merchant/\`: email + password → access + refresh tokens
- [ ] Endpoint \`POST /api/v1/auth/login/seller/\`: phone + password → access + refresh tokens
- [ ] Endpoint \`POST /api/v1/auth/refresh/\`: refresh token → new access token (rotation)
- [ ] Endpoint \`POST /api/v1/auth/logout/\`: blacklist refresh token
- [ ] Web storage: tokens in httpOnly cookies (not in JSON response body)
- [ ] Endpoint \`GET /api/v1/auth/me/\`: returns the logged-in user with their role

## Acceptance Criteria
- [ ] Login returns tokens in httpOnly cookies (SameSite=Strict, Secure in production)
- [ ] Refresh token is rotatable — old one is blacklisted after each renewal
- [ ] Expired token returns 401 with a clear message
- [ ] Tests: valid login, invalid login, refresh, logout, access without token

## Security
⚠️ Tokens must NEVER appear in Django logs." \
  "type: feature,module: auth,platform: api,status: ready,priority: critical" \
  "$M1"

create_issue \
  "feat(api): first-login flow — mandatory password change for seller" \
  "## Description
Implement the first-login flow for sellers: total block until password change.

## Tasks
- [ ] \`Seller\` model with \`temp_password_expires_at\` (DateTimeField)
- [ ] On seller creation: generate temp password (12 chars random alphanumeric), set \`must_change_password=True\` and \`temp_password_expires_at=now()+72h\`
- [ ] \`BlockedIfMustChangePassword\` middleware or permission: returns 403 with \`{ force_password_change: true }\` if flag is active
- [ ] Endpoint \`POST /api/v1/auth/change-password/\`: validates old password, sets new one, resets flag to False
- [ ] Endpoint \`POST /api/v1/sellers/{id}/regenerate-password/\`: merchant can regenerate a new temp password
- [ ] On login verification: if \`temp_password_expires_at\` < now() → rejection with expiration message

## Acceptance Criteria
- [ ] A seller with \`must_change_password=True\` cannot access ANY other endpoint
- [ ] Blocking is API-side, not just UI-side
- [ ] Temp password expired after 72h → login rejected with expiration message
- [ ] Merchant can regenerate a new temp password
- [ ] Tests: blocking first-login, successful change, 72h expiration" \
  "type: feature,module: auth,module: sellers,platform: api,status: ready,priority: critical" \
  "$M1"

create_issue \
  "feat(api): merchant password reset via email link" \
  "## Description
Allow a merchant to reset their password via a secure email link.

## Tasks
- [ ] Endpoint \`POST /api/v1/auth/password-reset/request/\`: sends email with a signed token (1-hour expiration)
- [ ] Endpoint \`POST /api/v1/auth/password-reset/confirm/\`: validates token and changes password
- [ ] Minimal and responsive HTML email template
- [ ] Token is single-use — invalidated after use
- [ ] Rate limiting on request endpoint: max 3 requests per hour per email

## Acceptance Criteria
- [ ] Invalid email still returns 200 (no user enumeration)
- [ ] Token expires after 1 hour
- [ ] Token can only be used once
- [ ] Tests: request, confirmation, expiration, double-use" \
  "type: feature,module: auth,platform: api,status: ready,priority: high" \
  "$M1"

create_issue \
  "feat(api): Merchant and Seller models with multi-tenancy" \
  "## Description
Create Merchant and Seller models with multi-tenant architecture.

## Tasks
- [ ] \`Merchant\` model: \`user\` (OneToOne), \`name\`, \`logo\`, \`currency\` (default: XOF), \`sector\`, \`is_validated\` (False by default)
- [ ] \`Seller\` model: \`merchant\` (FK), \`user\` (OneToOne), \`is_active\`, \`temp_password_expires_at\`
- [ ] Sellers CRUD: endpoints for the merchant (create, list, deactivate their sellers)
- [ ] \`get_queryset()\` pattern: always filter by \`merchant=request.user.merchant\`
- [ ] Multi-tenant isolation tests: one merchant cannot see another's sellers

## Acceptance Criteria
- [ ] A merchant can create a seller with an auto-generated temp password
- [ ] A merchant cannot access another merchant's sellers (404, not 403)
- [ ] Isolation tests: merchant A does not see merchant B's data" \
  "type: feature,module: merchants,module: sellers,platform: api,status: ready,priority: critical" \
  "$M1"

# ==============================================================================
# MONTH 1 — Frontend Web Auth
# ==============================================================================
echo ""
echo "🌐 Month 1 — Frontend Web Authentication"

create_issue \
  "feat(web): setup React 18 + Vite + Tailwind + Shadcn/ui" \
  "## Description
Initialize the web application with the full stack.

## Tasks
- [ ] Initialize with \`create vite@latest apps/web --template react-ts\`
- [ ] Configure TailwindCSS v3
- [ ] Install and configure Shadcn/ui (init + base components: Button, Input, Form, Card, Toast)
- [ ] Configure Axios with JWT interceptors (transparent refresh token)
- [ ] Configure React Query (TanStack Query v5) with appropriate defaults
- [ ] Configure React Router v6 with role protection layout
- [ ] Folder structure: \`pages/\`, \`components/\`, \`hooks/\`, \`lib/\`, \`stores/\`
- [ ] Base Zustand store: \`useAuthStore\` (user, token, isAuthenticated)
- [ ] Configure TypeScript aliases: \`@/\` → \`src/\`

## Acceptance Criteria
- [ ] \`pnpm --filter web dev\` starts without error
- [ ] \`pnpm --filter web build\` compiles without TypeScript error
- [ ] Axios interceptor automatically refreshes expired token" \
  "type: feature,platform: web,status: ready,priority: critical" \
  "$M1"

create_issue \
  "feat(web): Login pages (merchant and seller) with Zod validation" \
  "## Description
Create login screens for both types of users.

## Tasks
- [ ] \`/login\` page with tabs: Merchant (email) / Seller (phone)
- [ ] React Hook Form + Zod validation
- [ ] API calls to \`/api/v1/auth/login/merchant/\` and \`/api/v1/auth/login/seller/\`
- [ ] Error handling: invalid credentials, unvalidated account, expired password
- [ ] Detect \`force_password_change\` flag → redirect to password change screen
- [ ] Post-login redirect based on role: Admin → /admin, Merchant → /dashboard, Seller → /sales/new

## Acceptance Criteria
- [ ] Page is responsive (mobile and desktop)
- [ ] API errors are displayed clearly to the user
- [ ] A seller with must_change_password is redirected immediately
- [ ] Vitest tests cover: valid login, invalid email, incorrect password" \
  "type: feature,module: auth,platform: web,status: ready,priority: critical" \
  "$M1"

create_issue \
  "feat(web): role-protected routing and base layout" \
  "## Description
Create the routing system with role protection and main layouts.

## Tasks
- [ ] \`ProtectedRoute\` component checking auth and role
- [ ] Admin Layout with sidebar navigation
- [ ] Merchant Layout with sidebar navigation
- [ ] Seller Layout (simplified)
- [ ] 404 page and 403 page (access denied)
- [ ] Auto-redirect to /login if not authenticated

## Acceptance Criteria
- [ ] A seller accessing /dashboard (merchant) is redirected to 403
- [ ] An unauthenticated user accessing any protected route is redirected to /login
- [ ] Return route is preserved after login (\`?redirect=/products\`)" \
  "type: feature,module: auth,platform: web,status: ready,priority: critical" \
  "$M1"

# ==============================================================================
# MONTH 1 — Mobile Auth
# ==============================================================================
echo ""
echo "📱 Month 1 — Mobile Authentication"

create_issue \
  "feat(mobile): setup React Native + Expo SDK 51 + WatermelonDB + navigation" \
  "## Description
Initialize the mobile application with the full stack.

## Tasks
- [ ] Initialize with \`npx create-expo-app@latest apps/mobile --template blank-typescript\`
- [ ] Configure React Navigation v6 — Stack + Tab navigators
- [ ] Install and configure WatermelonDB with base schema (tables: sales, products)
- [ ] Configure Expo SecureStore for JWT token storage
- [ ] Configure Axios with interceptors (same as web — logic in packages/shared)
- [ ] Configure NetInfo for connectivity detection
- [ ] Folder structure: \`screens/\`, \`components/\`, \`db/\`, \`hooks/\`, \`stores/\`

## Acceptance Criteria
- [ ] \`npx expo start\` starts without error
- [ ] WatermelonDB is initialized and operational
- [ ] Base navigation works
- [ ] Tokens are stored in Expo SecureStore (not AsyncStorage)" \
  "type: feature,platform: mobile,status: ready,priority: critical" \
  "$M1"

create_issue \
  "feat(mobile): seller login screen and first-login flow" \
  "## Description
Create the mobile login screen for sellers and the first-login flow.

## Tasks
- [ ] Login screen: phone field + password field
- [ ] Seller login API call → token storage in Expo SecureStore
- [ ] Detect \`force_password_change\` flag in API response
- [ ] \`ChangePasswordScreen\` screen: blocking (impossible to navigate elsewhere)
- [ ] New password validation (min 8 chars, confirmation)
- [ ] After successful change: redirect to main seller screen

## Acceptance Criteria
- [ ] Seller cannot access any screen before changing password
- [ ] Back button is disabled on password change screen
- [ ] API errors displayed in French (or English if preferred)
- [ ] Screen is functional on Android (iOS deferred)" \
  "type: feature,module: auth,platform: mobile,status: ready,priority: critical" \
  "$M1"

echo ""
echo "============================================================"
echo "✅ Month 1 Issues created for $REPO"
echo ""
echo "Total issues created: $(gh issue list --repo "$REPO" --state open --json number | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))')"
echo ""
echo "📋 Next step: create Month 2 issues"
echo "   Edit this script and run the Month 2 section"
echo "============================================================"