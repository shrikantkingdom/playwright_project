# End-to-End Test Strategy

## 1. Purpose & Scope

This document defines the end-to-end (E2E) test strategy for the Playwright Automation Framework. It covers:

- Testing philosophy and pyramid
- Coverage strategy per layer
- Risk-based prioritisation
- Execution strategy
- Environment strategy
- Defect management
- Metrics and KPIs

---

## 2. Testing Philosophy: Shift-Left Quality

Quality is the responsibility of the **entire team**, not just QA. The framework supports shift-left testing by:

- Automated tests run on every pull request (not just at release time)
- Developers can run the full suite locally in minutes
- BDD scenarios are written during sprint planning, before development starts
- API tests guard service contracts independently of the UI

---

## 3. Test Pyramid

```
         ╔══════════════╗
         ║   E2E / UI   ║  ← Playwright BDD (slow, high value, few)
         ╠══════════════╣
         ║   API / Int  ║  ← httpx + pytest-bdd (medium speed, high value)
         ╠══════════════╣
         ║  Unit Tests  ║  ← pytest (fast, low cost, many)
         ╚══════════════╝
```

### Recommended Distribution

| Layer | % of Test Suite | Speed | Confidence |
|---|---|---|---|
| Unit | 70% | < 1 ms/test | Component logic |
| API/Integration | 20% | 100–500 ms/test | Service contracts, data flows |
| UI/E2E | 10% | 5–30 s/test | Critical user journeys |

---

## 4. Test Suite Structure

### 4.1 Smoke Tests (`@smoke`)

**Purpose:** Verify core system is operational. Run on every deployment.  
**Count target:** 20–40 tests  
**Execution time target:** < 5 minutes  
**Trigger:** Every push, every PR, post-deployment

**Scope:**
- Happy path login / logout
- Core API endpoints return 200
- Navigation to key pages succeeds

### 4.2 Regression Tests (`@regression`)

**Purpose:** Catch regressions across all business flows.  
**Count target:** 200–500 tests  
**Execution time target:** < 30 minutes (with parallelism)  
**Trigger:** On merge to `main`, nightly scheduled run

**Scope:**
- All CRUD operations
- Full authentication flows
- Error handling and edge cases
- Cross-browser validation

### 4.3 Performance Tests (`@performance`)

**Purpose:** Validate API response time SLAs.  
**Threshold:** All API responses < 2,000 ms  
**Trigger:** Nightly or on performance-sensitive PRs

### 4.4 Cross-Browser Tests

**Browsers tested:** Chromium, Firefox, WebKit (Safari)  
**Strategy:** Smoke tests run on all 3 browsers; full regression on Chromium only by default  
**Override:** `BROWSER=firefox pytest -m regression`

---

## 5. Coverage Strategy

### 5.1 UI Coverage (SauceDemo)

| Feature | Smoke | Regression | Priority |
|---|---|---|---|
| Login — valid credentials | ✅ | ✅ | P0 |
| Login — invalid credentials | ✅ | ✅ | P0 |
| Login — locked user | ✅ | ✅ | P1 |
| Product listing | ✅ | ✅ | P0 |
| Product sorting | ❌ | ✅ | P1 |
| Add to cart | ✅ | ✅ | P0 |
| Remove from cart | ❌ | ✅ | P1 |
| Checkout flow | ✅ | ✅ | P0 |
| Logout | ❌ | ✅ | P1 |

### 5.2 API Coverage (JSONPlaceholder)

| Endpoint | Smoke | Regression | Performance |
|---|---|---|---|
| GET /posts | ✅ | ✅ | ✅ |
| GET /posts/:id | ✅ | ✅ | ✅ |
| POST /posts | ❌ | ✅ | ❌ |
| PUT /posts/:id | ❌ | ✅ | ❌ |
| PATCH /posts/:id | ❌ | ✅ | ❌ |
| DELETE /posts/:id | ❌ | ✅ | ❌ |
| GET /users | ✅ | ✅ | ✅ |
| GET /todos | ✅ | ✅ | ✅ |

---

## 6. Risk-Based Test Prioritisation

Apply the following framework when deciding what to automate first:

```
Risk Score = (Business Impact × Likelihood of Failure) / Cost to Automate

Priority 1 (P0): Score > 15  — Always automate, always in smoke
Priority 2 (P1): Score 8–15 — Automate for regression
Priority 3 (P2): Score < 8  — Manual or exploratory only
```

### Example Risk Assessment

| Test Area | Business Impact (1–5) | Failure Likelihood (1–5) | Automation Cost (1–5) | Score | Priority |
|---|---|---|---|---|---|
| Login flow | 5 | 3 | 1 | 15 | P0 |
| Checkout flow | 5 | 4 | 2 | 10 | P1 |
| Sorting/filtering | 3 | 2 | 2 | 3 | P2 |
| Admin bulk actions | 4 | 3 | 5 | 2.4 | P2 |

---

## 7. Flaky Test Management

Flakiness is the primary enemy of automated test suite trust.

### Definition

A test is **flaky** if it fails intermittently without any code change.

### Prevention

1. Use Playwright's built-in auto-wait — never use `time.sleep()`
2. Use `page.wait_for_url()` / `page.wait_for_selector()` over hardcoded waits
3. Use `pytest-rerunfailures` (`--reruns 2`) as a safety net, not a fix
4. Network mocks for non-deterministic external APIs when possible

### Process

| Step | Action |
|---|---|
| Detect | CI reports flaky test (passed after rerun) |
| Log | Create a `[FLAKY]` ticket with failure screenshot + trace |
| Quarantine | Move test to `@flaky` marker; exclude from main pipeline |
| Fix | Investigate root cause within 1 sprint |
| Unquarantine | Remove `@flaky` marker; add to CI pipeline |

---

## 8. Execution Strategy

### Local Development

```bash
# API smoke tests (< 2 minutes)
pytest -m "api and smoke"

# UI smoke on default browser
pytest -m "ui and smoke"

# Full regression parallel
pytest -m regression -n auto
```

### CI Pipeline

| Pipeline | Trigger | Tests | Target Time |
|---|---|---|---|
| PR checks | Every PR | smoke | < 5 min |
| Main merge | Push to main | smoke + regression | < 30 min |
| Nightly | Scheduled 02:00 | all (regression + performance) | < 60 min |
| Release gate | Manual/tag | full regression all browsers | < 60 min |

---

## 9. Test Data Strategy

### Principles

1. **Tests are data-independent** — No test hardcodes data that changes
2. **Faker for generated data** — Dynamic, unique data per test run
3. **Idempotent setup** — Tests leave no side effects; each test starts fresh
4. **No shared mutable state** — Function-scoped fixtures for browser state

### Data Sources

| Data Type | Source | Notes |
|---|---|---|
| Static credentials | `.env` / GitHub Secrets | SauceDemo standard_user |
| Generated payloads | `data/test_data.py` + Faker | API POST/PUT bodies |
| Schema definitions | `utils/schema_validator.py` | Response validation |
| Environment URLs | `config/environments/` | Per-env config |

---

## 10. Defect Management

### Severity Classification

| Severity | Definition | Example |
|---|---|---|
| S1 Critical | System unusable, data loss, security breach | Login broken, checkout fails |
| S2 High | Major feature broken, no workaround | Product search broken |
| S3 Medium | Feature partially broken, workaround exists | Sorting incorrect |
| S4 Low | Minor UI issue, cosmetic defect | Alignment issue |

### Defect SLA

| Severity | Resolution SLA |
|---|---|
| S1 | < 4 hours |
| S2 | < 1 business day |
| S3 | < 1 sprint |
| S4 | Backlog, best-effort |

---

## 11. Metrics and KPIs

### Test Health Metrics

| Metric | Target | Measurement |
|---|---|---|
| Automation coverage | > 80% of regression suite | Test count vs requirement count |
| Pass rate | > 98% on clean builds | CI reports |
| Flaky test rate | < 1% | Tests that pass on rerun / total |
| Test execution time (smoke) | < 5 min | CI job duration |
| Test execution time (regression) | < 30 min | CI job duration |
| MTTR (Mean Time to Green) | < 2 hours | Time from red to green |

### Release Quality Metrics

| Metric | Target |
|---|---|
| Escaped defects (production bugs) | < 2 per release |
| Defect detection rate | > 90% caught pre-production |
| Test debt (unapproved skipped tests) | 0 |
