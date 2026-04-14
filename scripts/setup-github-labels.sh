#!/bin/bash
# scripts/setup-github-labels.sh
# Usage: GITHUB_TOKEN=xxx REPO=your-username/kommercehub bash scripts/setup-github-labels.sh

set -e

API="https://api.github.com/repos/${REPO}/labels"
AUTH="Authorization: Bearer ${GITHUB_TOKEN}"

create_label() {
  local name="$1"
  local color="$2"
  local description="$3"

  curl -s -X POST "$API" \
    -H "$AUTH" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$name\",\"color\":\"$color\",\"description\":\"$description\"}" \
    > /dev/null

  echo "✅ Label created: $name"
}

echo "🏷️  Creating GitHub labels for $REPO..."

# Type
create_label "type: bug"         "d73a4a" "Unexpected behavior or errors"
create_label "type: feature"     "a2eeef" "New functionality"
create_label "type: docs"        "0075ca" "Documentation updates"
create_label "type: security"    "e4e669" "Vulnerabilities or security improvements"
create_label "type: performance" "cfd3d7" "Performance optimizations"
create_label "type: chore"       "ffffff" "Tooling, CI, dependencies"
create_label "type: test"        "bfd4f2" "Testing and coverage"

# Priority
create_label "priority: critical" "b60205" "Blocker, must be addressed immediately"
create_label "priority: high"     "e99695" "High impact on users or business"
create_label "priority: medium"   "f9d0c4" "Moderate impact"
create_label "priority: low"      "fef2c0" "Nice-to-have improvement"

# Module
create_label "module: auth"          "7057ff" "Authentication and authorization"
create_label "module: products"      "008672" "Product and stock management"
create_label "module: sales"         "e4e669" "Sales and transactions management"
create_label "module: analytics"     "0052cc" "Dashboard and statistics"
create_label "module: notifications" "d93f0b" "Alerts and notifications system"
create_label "module: admin"         "1d76db" "Back-office administration"
create_label "module: subscriptions" "5319e7" "Plans and subscription management"
create_label "module: offline-sync"  "0e8a16" "Offline synchronization logic"

# Scope / Platform
create_label "scope: backend"  "c2e0c6" "Django REST API"
create_label "scope: frontend" "bfd4f2" "React Web application"
create_label "scope: mobile"   "d4c5f9" "React Native mobile application"
create_label "scope: infra"    "f9d0c4" "DevOps, CI/CD, and deployment"
create_label "scope: shared"   "eeeeee" "Code in packages/shared"

# Status
create_label "status: needs-triage" "eeeeee" "Issue waiting for evaluation"
create_label "status: in-progress"  "0e8a16" "Currently being developed"
create_label "status: blocked"      "d73a4a" "Blocked by a dependency or technical issue"
create_label "status: review"       "cfd3d7" "Awaiting peer review"

echo ""
echo "🎉 All labels have been successfully created on $REPO"