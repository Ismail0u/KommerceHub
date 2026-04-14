# GitHub Organization — KommerceHub

This document outlines the complete project organization on GitHub. 
**Please read this before creating issues or Pull Requests (PRs).**

---

## GitHub Project Board Structure
We use **GitHub Projects (v2)** with a Kanban-style view.

### Board Columns
| Column | Description | Who Moves It |
| :--- | :--- | :--- |
| **Backlog** | Issues created but not yet ready for development | Maintainers |
| **Ready** | Issues with all necessary info to start | Maintainers |
| **In Progress** | Issues with an assigned developer | The Developer |
| **Review** | Open PR, waiting for review | The Developer |
| **Done** | Merged and deployed to staging | Automated CI System |

---

## Labeling System

### By Type (Nature of the issue)
* `type: bug` 🔴 **Red** – Unexpected behavior or error
* `type: feature` 🔵 **Blue** – New functionality
* `type: epic` 🟣 **Purple** – A collection of related tickets
* `type: docs` 🔵 **Dark Blue** – Documentation only
* `type: refactor` 🟡 **Yellow** – Refactoring without functional changes
* `type: perf` 🟡 **Yellow** – Performance improvement
* `type: security` 🔴 **Dark Red** – Security issue
* `type: chore` ⚪ **Light Gray** – Maintenance, dependencies, CI
* `type: test` 🔵 **Light Blue** – Tests only

### By Module (Backend)
`module: auth` · `module: merchants` · `module: sellers` · `module: products` · `module: sales` · `module: analytics` · `module: notifications` · `module: subscriptions`

### By Platform
`platform: web` · `platform: mobile` · `platform: api` · `platform: devops`

### By Priority
| Label | Description |
| :--- | :--- |
| `priority: critical` | Blocker — handled immediately |
| `priority: high` | Current Sprint |
| `priority: medium` | Normal priority |
| `priority: low` | Nice-to-have |

---

## Milestones
| Milestone | Deadline | Goal |
| :--- | :--- | :--- |
| **Month 1 — Foundations** | April 30, 2026 | Setup, Auth, Core Models |
| **Month 2 — Core Features** | May 31, 2026 | Products, Sales, Offline mode |
| **Month 3 — Dashboard & Pilot**| June 30, 2026 | Analytics, Deploy, Pilot launch |
| **Post-MVP** | TBD | Payments, Pro plans |

---

## Branch Naming Convention
* `feature/<issue-number>-<short-description>`
* `fix/<issue-number>-<short-description>`
* `docs/<short-description>`
* `chore/<short-description>`

**Examples:**
* `feature/5-jwt-merchant-login`
* `fix/23-seller-first-login-blocking`

---

## Issue Workflow
1.  **Issue Creation** (Bug report or feature request).
2.  **Triage** by maintainer (Labels + Milestone + Priority). `status: triage` → `status: ready`.
3.  **Developer assignment**: Comment "I'm taking this issue". `status: ready` → `status: in progress`.
4.  **Create branch**: `feature/<id>-<description>`.
5.  **Development** with atomic conventional commits.
6.  **Open PR** to `develop` (Reference the issue: "Closes #42"). `status: in progress` → `status: review`.
7.  **CI Checks**: Lint + Tests + Build.
8.  **Review** by maintainer (Max 48h).
9.  **Merge** to `develop` → Automatic Staging Deployment. `status: review` → `Done`.
10. **Issue closed** automatically by GitHub.

---

## Basic Rules
* **One PR = One Issue**: No PRs touching 5 different things.
* **Never commit directly** to `main` or `develop`.
* **Always comment** on the issue before starting to avoid duplicates.
* **Critical/Security** issues are handled in **< 24h**.
* **Secrets in code** = Immediate PR rejection.

---