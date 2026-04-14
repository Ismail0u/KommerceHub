# 📝 Description

Fixes \#[issue\_number]

-----

# 🔄 Type of Change

  - [ ] 🐛 **Bug fix** (non-breaking change which fixes an issue)
  - [ ] ✨ **New feature** (non-breaking change which adds functionality)
  - [ ] 💥 **Breaking change** (fix or feature that would cause existing functionality to not work as expected)
  - [ ] 📚 **Documentation** update
  - [ ] 🔧 **Chore / Refactoring** (no functional changes)
  - [ ] ⚡ **Performance** improvement
  - [ ] 🔒 **Security** fix

-----

# 🧪 How to Test

1.  ...
2.  ...
3.  ...

**Happy Path Scenario:**
...

**Edge Case Scenario:**
...

-----

# 📸 Screenshots (if UI related)

| Before | After |
| :--- | :--- |
|  |  |

-----

# ✅ Checklist

### Code Quality

  - [ ] Code follows the conventions defined in `CONTRIBUTING.md`
  - [ ] No `console.log` / `print()` debug statements left in code
  - [ ] No credentials or secrets committed
  - [ ] Any remaining `TODO`s are tracked as GitHub issues

### Testing

  - [ ] Existing tests pass (`pnpm test` / `pytest`)
  - [ ] New tests have been added for the changes
  - [ ] Test coverage has not decreased

### Backend (if applicable)

  - [ ] `get_queryset()` correctly filters by merchant (multi-tenant isolation)
  - [ ] Django migrations are included and reversible
  - [ ] Endpoints are documented in Swagger/OpenAPI (`drf-spectacular`)
  - [ ] Rate limiting is configured for new public endpoints

### Mobile (if applicable)

  - [ ] Verified offline mode functionality
  - [ ] Offline data uses **delta events** (not final states)
  - [ ] Tested on Android (emulator or physical device)

### Security

  - [ ] RBAC permissions are verified on the API side (not just frontend)
  - [ ] No sensitive data exposed in logs
  - [ ] User inputs are validated and sanitized

-----

# 📋 Reviewer Notes

-----