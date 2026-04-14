#!/usr/bin/env bash
# =============================================================================
# setup-github-milestones.sh
# Creates GitHub milestones for KommerceHub using GitHub CLI
#
# Prerequisites: GitHub CLI installed and authenticated
#   → brew install gh  (macOS)
#   → winget install GitHub.cli  (Windows)
#   → gh auth login
#
# Usage: ./scripts/setup-github-milestones.sh kommercehub/kommercehub
# =============================================================================

set -euo pipefail

REPO="${1:-kommercehub/kommercehub}"

echo "🗓️  Creating milestones for: $REPO"
echo ""

# Milestone 1 — Foundations
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  "/repos/$REPO/milestones" \
  -f title="Month 1 — Foundations" \
  -f description="Setup Turborepo monorepo, GitHub Actions CI/CD, Docker Compose, full JWT authentication (merchant + seller), data models, first-login flow." \
  -f due_on="2026-04-30T23:59:59Z" \
  -f state="open"
echo "✅ Milestone 1 created — Foundations (deadline: April 30, 2026)"

# Milestone 2 — Core Features
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  "/repos/$REPO/milestones" \
  -f title="Month 2 — Core Features" \
  -f description="Product CRUD, inventory management, sales recording, mobile offline mode (WatermelonDB + delta sync), PDF receipts, low stock alerts, Celery." \
  -f due_on="2026-05-31T23:59:59Z" \
  -f state="open"
echo "✅ Milestone 2 created — Core Features (deadline: May 31, 2026)"

# Milestone 3 — Dashboard & Pilot
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  "/repos/$REPO/milestones" \
  -f title="Month 3 — Dashboard & Pilot" \
  -f description="Full dashboard with analytics, CSV/PDF exports, admin back office, Playwright E2E tests, production deployment, onboarding 10 pilot merchants in Niger." \
  -f due_on="2026-06-30T23:59:59Z" \
  -f state="open"
echo "✅ Milestone 3 created — Dashboard & Pilot (deadline: June 30, 2026)"

# Post-MVP Milestone
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  "/repos/$REPO/milestones" \
  -f title="Post-MVP" \
  -f description="Mobile payment integrations (Wave, Airtel Money, Mynita), Pro/Business plans, iOS support, OAuth, post-pilot features based on field feedback." \
  -f state="open"
echo "✅ Post-MVP milestone created"

echo ""
echo "=================================================="
echo "✅ 4 milestones created for $REPO"
echo ""
echo "📋 Next step — Labels:"
echo "   ./scripts/setup-github-labels.sh $REPO"
echo ""
echo "📋 Then issues:"
echo "   ./scripts/setup-github-issues.sh $REPO"
echo "=================================================="