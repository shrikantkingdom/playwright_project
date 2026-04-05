# Technical Architecture — Playwright Automation Framework

## 1. Architecture Overview

```
playwright_project/
├── .github/
│   └── workflows/
│       └── ci.yml              ← GitHub Actions CI pipeline
├── api_clients/                ← HTTP client layer (httpx-based)
│   ├── base_client.py          ← BaseAPIClient: timing, auth, logging
│   └── json_placeholder_client.py  ← Domain-specific API methods
├── config/                     ← Configuration management
│   ├── base_config.py          ← BaseConfig dataclass + factory
│   └── environments/           ← Per-environment overrides
│       ├── dev.py
│       ├── qa.py
│       └── staging.py
├── data/                       ← Test data factories
│   └── test_data.py            ← Faker-powered data builders
├── features/                   ← Gherkin BDD scenarios (source of truth)
│   ├── api/
│   │   ├── posts.feature
│   │   ├── todos.feature
│   │   └── users.feature
│   └── ui/
│       ├── cart.feature
│       ├── login.feature
│       └── navigation.feature
├── fixtures/                   ← Shared pytest fixture modules
├── pages/                      ← Page Object Model classes
│   ├── base_page.py            ← BasePage: navigation, waits, screenshots
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py
├── tests/
│   └── step_defs/              ← pytest-bdd step definitions
│       ├── conftest.py         ← BDD shared fixtures (context dict)
│       ├── api/
│       │   ├── conftest.py     ← Shared API assertion steps
│       │   ├── test_posts_steps.py
│       │   ├── test_todos_steps.py
│       │   └── test_users_steps.py
│       └── ui/
│           ├── conftest.py     ← Shared UI given steps (login)
│           ├── test_login_steps.py
│           ├── test_cart_steps.py
│           └── test_navigation_steps.py
├── utils/                      ← Cross-cutting utilities
│   ├── helpers.py              ← Timestamps, dir creation, decorators
│   ├── logger.py               ← Colorized logging setup
│   └── schema_validator.py     ← JSON Schema validation + schemas
├── conftest.py                 ← Root fixtures: config, browser, page, api_client
├── pytest.ini                  ← Test discovery, markers, addopts
├── pyproject.toml              ← Black + flake8 config
├── requirements.txt            ← Python dependencies (pinned versions)
├── Dockerfile                  ← Containerised test runner
└── docs/                       ← Framework documentation
```

---

## 2. Layered Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        TEST LAYER                               │
│  features/*.feature  +  tests/step_defs/**/*.py                 │
│  (Gherkin scenarios + pytest-bdd step definitions)              │
├─────────────────────────────────────────────────────────────────┤
│                      FIXTURE LAYER                              │
│  conftest.py (root)  +  tests/step_defs/**/conftest.py          │
│  (browser, page, api_client, config, context)                   │
├──────────────────────────┬──────────────────────────────────────┤
│      UI ABSTRACTION      │        API ABSTRACTION               │
│  pages/*.py (POM)        │  api_clients/*.py                    │
│  BasePage → Page Objects │  BaseAPIClient → Domain Clients      │
├──────────────────────────┴──────────────────────────────────────┤
│                      UTILITY LAYER                               │
│  utils/helpers.py  |  utils/logger.py  |  utils/schema_validator│
├─────────────────────────────────────────────────────────────────┤
│                    CONFIGURATION LAYER                           │
│  config/base_config.py  +  config/environments/               │
│  .env / environment variables  /  GitHub Secrets                │
├─────────────────────────────────────────────────────────────────┤
│                      DATA LAYER                                  │
│  data/test_data.py (Faker factories)                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Deep-Dives

### 3.1 Configuration Layer

```
get_config()  ←  reads .env  ←  overridden by OS environment variables
     │
     ▼
BaseConfig (dataclass)
  ui_base_url, api_base_url
  browser, headless, slow_mo
  default_timeout, api_max_response_ms
  sauce_username, sauce_password
  reruns, workers
```

**Design principles:**
- Immutable dataclass — never mutated during a test session
- `dotenv` loads `.env` at import time; real env vars always win (`override=False`)
- All config consumed via the `config` pytest fixture (session scope) — loaded once
- Per-environment files (`dev.py`, `qa.py`, `staging.py`) inherit from BaseConfig and override specific values

### 3.2 Page Object Model (POM)

```
BasePage
  ├── navigate(url)
  ├── get_current_url()
  ├── get_title()
  ├── wait_for_selector(selector, timeout)
  └── take_screenshot(name)
       │
       ├── LoginPage
       │     ├── open(base_url)
       │     ├── login(username, password)
       │     ├── enter_username(username)  → LoginPage (fluent)
       │     ├── enter_password(password)  → LoginPage (fluent)
       │     ├── click_login()
       │     ├── get_error_message()
       │     └── is_error_displayed()
       │
       ├── InventoryPage
       │     ├── is_loaded()
       │     ├── get_product_names()
       │     ├── sort_by(option)
       │     ├── add_item_to_cart(name)
       │     └── logout()
       │
       └── CartPage
             ├── get_cart_items()
             ├── get_item_count()
             └── checkout()
```

**Design principles:**
- Each page class owns the selectors for that page — no selectors in test files
- Fluent interface (return `self`) for method chaining where it aids readability
- No assertions in page objects — they return values; assertions live in step definitions
- POM classes receive `Page` via constructor injection — facilitates testing

### 3.3 API Client Layer

```
BaseAPIClient (httpx.Client wrapper)
  ├── _request(method, path, **kwargs)  ← timing, logging, elapsed_ms injection
  ├── get(path)
  ├── post(path, json)
  ├── put(path, json)
  ├── patch(path, json)
  ├── delete(path)
  └── close()
       │
       └── JSONPlaceholderClient(BaseAPIClient)
             ├── get_posts()
             ├── get_post(post_id)
             ├── get_post_comments(post_id)
             ├── create_post(payload)
             ├── update_post(post_id, payload)
             ├── partial_update_post(post_id, payload)
             ├── delete_post(post_id)
             ├── get_users()
             ├── get_user(user_id)
             ├── get_todos()
             └── get_todo(todo_id)
```

**Design principles:**
- `BaseAPIClient` is a reusable adapter — new API clients extend it
- `elapsed_ms` is injected onto `httpx.Response` for performance assertions without changing the interface
- Session-scoped in pytest: one connection pool for the entire test suite (performance, resource efficiency)
- Bearer token authentication built into constructor

### 3.4 BDD Layer (pytest-bdd)

```
features/api/posts.feature          ← Gherkin (business-readable)
           ↓ scenarios() binding
tests/step_defs/api/test_posts_steps.py
  @when("I request all posts")
  def when_request_all_posts(api_client, context):
      context["response"] = api_client.get_posts()

  @then("the response status should be 200")
  ← Defined in tests/step_defs/api/conftest.py (reusable across all API features)
```

**Shared step definitions:**
- `tests/step_defs/api/conftest.py` — common `then` steps: status codes, list checks, performance
- `tests/step_defs/ui/conftest.py` — common `given` steps: login preconditions
- `tests/step_defs/conftest.py` — `context` fixture (mutable dict for step state sharing)

**State sharing between steps:**

```python
@pytest.fixture
def context():
    return {}

@when("I request all posts")
def step(api_client, context):
    context["response"] = api_client.get_posts()  # Store in context dict

@then("the response status should be 200")
def step(context):
    assert context["response"].status_code == 200  # Read from context dict
```

### 3.5 Fixture Hierarchy

```
Session scope (created once per test run):
  config              ← BaseConfig instance
  api_client          ← JSONPlaceholderClient (connection pool)
  playwright_instance ← sync_playwright() context
  browser             ← Playwright Browser process

Function scope (created fresh per test):
  browser_context     ← BrowserContext (isolated: cookies, storage, auth)
  page               ← Page (browser tab)
  authenticated_page  ← Page pre-logged into SauceDemo
  context            ← BDD step state dict
```

**Why session-scoped browser, function-scoped context?**

- Browser launch is slow (~200–500 ms). One browser process per session is efficient.
- `BrowserContext` provides **complete isolation** (no shared cookies, localStorage, or auth state between tests).
- Each test gets a fresh context = no test interference.

### 3.6 Artefact Collection

```
reports/
  report.html          ← pytest-html self-contained report
  screenshots/         ← FAILED_<test_name>.png (on failure only)
  videos/              ← <test_name>.webm (always recorded)
  traces/              ← <test_name>.zip (Playwright trace, always)

allure-results/        ← Optional: allure-pytest JSON output
```

**Viewing traces:**

```bash
playwright show-trace reports/traces/test_login.zip
```

This opens an interactive viewer showing every step, DOM snapshot, network request, and console log.

---

## 4. Data Flow: UI Test Execution

```
pytest collect
  → scenarios() loads features/ui/login.feature
  → Step defs in test_login_steps.py are matched

Test: "Successful login with standard user"
  →  conftest.py: config fixture (session) → BaseConfig
  →  conftest.py: browser fixture (session) → Chromium browser
  →  conftest.py: browser_context fixture (function) → new isolated context
  →  conftest.py: page fixture (function) → new page
  →  Step: given_on_login_page
       → LoginPage(page).open(config.ui_base_url)
       → page.goto("https://www.saucedemo.com")
  →  Step: when_login("standard_user", "secret_sauce")
       → login_page.login(username, password)
       → page.fill("#user-name", "standard_user")
       → page.fill("#password", "secret_sauce")
       → page.click("#login-button")
  →  Step: then_on_inventory_page
       → page.wait_for_url("**/inventory.html")
       → assert "inventory.html" in page.url

  →  Teardown:
       → context.tracing.stop(path="reports/traces/test_login.zip")
       → context.close()
       → (On failure: page.screenshot(path="reports/screenshots/FAILED_test_login.png"))
```

---

## 5. Data Flow: API Test Execution

```
Test: "Get all posts returns 200"
  →  conftest.py: api_client fixture (session)
       → JSONPlaceholderClient("https://jsonplaceholder.typicode.com")
  →  context fixture (function) → empty dict {}

  →  Step: when_request_all_posts
       → api_client.get_posts()
       → BaseAPIClient._request("GET", "/posts")
       → httpx GET https://jsonplaceholder.typicode.com/posts
       → response.elapsed_ms = 45.2
       → context["response"] = response

  →  Step: check_response_status(200)
       → assert context["response"].status_code == 200

  →  No teardown needed (stateless API call)
```

---

## 6. CI/CD Pipeline Architecture

```
GitHub Push / PR
       │
       ▼
┌──────────────────────────────────────────────┐
│           GitHub Actions Workflow             │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │           api-tests job                  │ │
│  │  ubuntu-latest / Python 3.11            │ │
│  │  pip install → pytest tests/step_defs/  │ │
│  │  api -m api -n auto                     │ │
│  │  Artefact: reports/api-report.html      │ │
│  └─────────────────────────────────────────┘ │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │     ui-tests (matrix: 3 browsers)        │ │
│  │  chromium / firefox / webkit             │ │
│  │  playwright install --with-deps {browser}│ │
│  │  pytest tests/step_defs/ui -m ui        │ │
│  │  Artefacts: HTML report + screenshots   │ │
│  │             + traces                    │ │
│  └─────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

---

## 7. Security Architecture

### 7.1 Secrets Management

| Secret | Local Dev | CI (GitHub Actions) |
|---|---|---|
| `SAUCE_USERNAME` | `.env` (gitignored) | Repository Secret |
| `SAUCE_PASSWORD` | `.env` (gitignored) | Repository Secret |
| `API_TOKEN` | `.env` (gitignored) | Repository Secret |

**Rules:**
- `.env` file is always in `.gitignore` — never committed
- `.env.example` provides the template with placeholder values only
- No credentials hardcoded anywhere in test code or configuration files
- GitHub Actions uses encrypted repository secrets; values never appear in logs

### 7.2 OWASP Compliance in Test Code

- No SQL injection vectors — tests use external public APIs only
- No sensitive data written to logs (passwords are logged as `****`)
- Test artefacts (screenshots, traces) may contain session data — stored as CI artefacts, not published
- Docker containers run as non-root (best practice recommendation)

---

## 8. Extension Points

### Adding a New API Client

```python
# api_clients/my_service_client.py
from api_clients.base_client import BaseAPIClient

class MyServiceClient(BaseAPIClient):
    def get_items(self):
        return self.get("/items")
    
    def create_item(self, payload):
        return self.post("/items", json=payload)
```

```python
# conftest.py — add fixture
@pytest.fixture(scope="session")
def my_service_client(config):
    client = MyServiceClient(base_url=config.my_service_url)
    yield client
    client.close()
```

### Adding a New Page Object

```python
# pages/checkout_page.py
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    FIRST_NAME = "[data-test='firstName']"
    # ...
    
    def fill_shipping_info(self, first, last, zip_code):
        self.page.fill(self.FIRST_NAME, first)
        # ...
```

### Adding a New Feature

1. Create `features/ui/my_feature.feature` (Gherkin)
2. Create `tests/step_defs/ui/test_my_feature_steps.py` (step defs)
3. Run `pytest tests/step_defs/ui/test_my_feature_steps.py -v`

---

## 9. Technology Stack Summary

| Component | Technology | Version | Purpose |
|---|---|---|---|
| Test runner | pytest | 8.4.2 | Test collection, execution, fixtures |
| Browser automation | playwright | 1.58.0 | Browser control, network interception |
| Playwright pytest | pytest-playwright | 0.7.1 | Playwright fixtures integration |
| BDD framework | pytest-bdd | 8.1.0 | Gherkin scenario support |
| HTTP client | httpx | 0.28.1 | API testing |
| Parallelism | pytest-xdist | 3.8.0 | Concurrent test execution |
| Retry | pytest-rerunfailures | 16.0.1 | Flaky test mitigation |
| Reporting | pytest-html | 4.2.0 | HTML test reports |
| Allure reporting | allure-pytest | 2.15.3 | Rich visual reports |
| Schema validation | jsonschema | 4.25.1 | API response validation |
| Test data | Faker | 37.12.0 | Dynamic test data generation |
| Config | python-dotenv | 1.2.1 | .env file loading |
| Logging | colorlog | 6.10.1 | Colour-coded console logging |
| Code format | black | 25.11.0 | Automatic code formatting |
| Linting | flake8 | 7.3.0 | Code quality checks |
| Git hooks | pre-commit | 4.3.0 | Pre-push quality gates |
| Container | Docker | Latest | CI/CD containerisation |
| CI/CD | GitHub Actions | Latest | Pipeline automation |
| Language | Python | 3.11 | Test framework language |
