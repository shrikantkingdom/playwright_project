# 🎭 Playwright Automation Framework

A production-ready Python test automation framework built with **Playwright**, **Pytest**, and best-practice design patterns. Demonstrates UI testing, REST API testing, and basic performance validation using public demo applications.

---

## 📁 Project Structure

```
playwright_project/
├── api_clients/                  # Reusable HTTP client layer
│   ├── base_client.py            # Base httpx wrapper (timing, auth, logging)
│   └── json_placeholder_client.py# JSONPlaceholder API client
├── config/                       # Configuration management
│   ├── base_config.py            # BaseConfig dataclass + get_config() factory
│   └── environments/             # Per-environment overrides (dev, qa, staging)
│       ├── dev.py
│       ├── qa.py
│       └── staging.py
├── data/                         # Test data factories (Faker-powered)
│   └── test_data.py
├── docs/                         # Framework documentation
│   ├── business-decisions.md     # Technology ADRs and ROI model
│   ├── e2e-test-strategy.md      # Test strategy and coverage plan
│   ├── playwright-pros-cons.md   # Playwright vs Selenium vs Cypress
│   ├── selenium-to-playwright-migration.md
│   ├── technical-architecture.md # Architecture diagrams and data flows
│   └── sdet-manager-interview-qa.md
├── features/                     # Gherkin BDD scenarios (living documentation)
│   ├── api/
│   │   ├── posts.feature
│   │   ├── todos.feature
│   │   └── users.feature
│   └── ui/
│       ├── cart.feature
│       ├── login.feature
│       └── navigation.feature
├── fixtures/                     # Shared pytest fixture modules
├── pages/                        # Page Object Model (POM) classes
│   ├── base_page.py              # Base class with common helpers
│   ├── login_page.py             # SauceDemo login page
│   ├── inventory_page.py         # Product listing page
│   └── cart_page.py              # Cart & checkout pages
├── tests/
│   └── step_defs/                # pytest-bdd step definitions
│       ├── conftest.py           # Shared BDD context fixture
│       ├── ui/                   # UI step definitions (Playwright)
│       │   ├── conftest.py       # Shared UI given steps
│       │   ├── test_login_steps.py
│       │   ├── test_navigation_steps.py
│       │   └── test_cart_steps.py
│       └── api/                  # API step definitions (httpx)
│           ├── conftest.py       # Shared API assertion steps
│           ├── test_posts_steps.py
│           ├── test_users_steps.py
│           └── test_todos_steps.py
├── utils/                        # Shared utilities
│   ├── logger.py                 # Coloured logging setup
│   ├── helpers.py                # Timestamps, dir creation, decorators
│   └── schema_validator.py       # jsonschema wrapper + common schemas
├── reports/                      # Generated test reports (gitignored)
├── .env.example                  # Environment variable template
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI pipeline
├── .pre-commit-config.yaml       # Pre-commit hooks (black + flake8)
├── conftest.py                   # Root-level pytest fixtures
├── Dockerfile                    # Containerised test runner
├── pytest.ini                    # Pytest configuration
├── pyproject.toml                # Black / flake8 config
└── requirements.txt              # Python dependencies
```

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10+
- pip or a virtual environment manager

### 2. Clone & set up a virtual environment

```bash
git clone <repo-url>
cd playwright_project
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install --with-deps chromium firefox webkit
```

### 5. Configure environment

```bash
cp .env.example .env
# Edit .env if needed (defaults work out of the box)
```

---

## 🧪 Running Tests

### Run all tests

```bash
pytest
```

### Run only UI tests

```bash
pytest tests/step_defs/ui -m ui
```

### Run only API tests

```bash
pytest tests/step_defs/api -m api
```

### Run smoke tests

```bash
pytest -m smoke
```

### Run regression tests

```bash
pytest -m regression
```

### Run performance tests

```bash
pytest -m performance
```

---

## 🌐 Cross-Browser UI Testing

Run UI tests on a specific browser:

```bash
BROWSER=chromium pytest tests/step_defs/ui -m ui
BROWSER=firefox  pytest tests/step_defs/ui -m ui
BROWSER=webkit   pytest tests/step_defs/ui -m ui
```

---

## ⚡ Parallel Execution

Use **pytest-xdist** to run tests in parallel:

```bash
# Auto-detect workers (one per CPU core)
pytest tests/step_defs/api -n auto

# Fixed number of workers
pytest tests/step_defs/api -n 4
```

---

## 🔁 Retry Mechanism

Automatic retries for flaky tests are powered by **pytest-rerunfailures**:

```bash
# Retry failed tests up to 3 times with a 2-second delay
pytest --reruns 3 --reruns-delay 2
```

---

## 📊 Reporting

### HTML Report (default)

An HTML report is automatically generated at `reports/report.html` after each run.

```bash
pytest                             # generates reports/report.html
open reports/report.html           # macOS
xdg-open reports/report.html      # Linux
```

### Allure Report — API tests

```bash
# Run API tests and collect Allure results
pytest tests/step_defs/api -m api --alluredir=allure-results/api

# Open interactive Allure report in browser
allure serve allure-results/api
```

### Allure Report — UI tests

```bash
# Run UI tests and collect Allure results
pytest tests/step_defs/ui -m ui --alluredir=allure-results/ui

# Open interactive Allure report in browser
allure serve allure-results/ui
```

### Why step_defs paths, not feature paths?

When using **pytest-bdd**, you always run the **step definition files** — not the `.feature` files directly.
The feature files are plain Gherkin documentation; they do not contain executable code.
Each step definition module links to its feature file via the `scenarios()` decorator:

```python
# in test_navigation_steps.py
from pytest_bdd import scenarios
scenarios("features/ui/navigation.feature")   # links at collection time
```

So `pytest tests/step_defs/ui -m ui` is the correct and idiomatic command.

---

## 🏗️ Architecture Overview

### Page Object Model (POM)

All UI interactions are encapsulated in page classes under `pages/`:

```python
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

def test_login(page, config):
    login = LoginPage(page)
    login.open(config.ui_base_url)
    login.login(config.sauce_username, config.sauce_password)
    page.wait_for_url("**/inventory.html")
    assert InventoryPage(page).is_loaded()
```

### API Client Layer

```python
def test_create_post(api_client):
    response = api_client.create_post({"userId": 1, "title": "Hi", "body": "World"})
    assert response.status_code == 201
    assert response.json()["title"] == "Hi"
```

### Schema Validation

```python
from utils.schema_validator import POST_SCHEMA, validate_schema

def test_post_schema(api_client):
    response = api_client.get_post(1)
    validate_schema(response.json(), POST_SCHEMA)
```

---

## ⚙️ Configuration

| Variable              | Default                                  | Description                    |
|-----------------------|------------------------------------------|--------------------------------|
| `ENV`                 | `qa`                                     | Active environment             |
| `UI_BASE_URL`         | `https://www.saucedemo.com`              | SauceDemo base URL             |
| `API_BASE_URL`        | `https://jsonplaceholder.typicode.com`   | JSONPlaceholder base URL       |
| `SAUCE_USERNAME`      | `standard_user`                          | SauceDemo login username       |
| `SAUCE_PASSWORD`      | `secret_sauce`                           | SauceDemo login password       |
| `BROWSER`             | `chromium`                               | chromium / firefox / webkit    |
| `HEADLESS`            | `true`                                   | Run browser headlessly         |
| `DEFAULT_TIMEOUT`     | `30000`                                  | Playwright timeout (ms)        |
| `API_MAX_RESPONSE_MS` | `2000`                                   | Max API response time (ms)     |
| `RERUNS`              | `2`                                      | Retry count for flaky tests    |
| `WORKERS`             | `2`                                      | Parallel worker count          |

---

## 🐳 Docker

```bash
# Build
docker build -t playwright-tests .

# Run all tests
docker run --rm playwright-tests

# Run only API tests
docker run --rm playwright-tests pytest tests/step_defs/api -m api -v
```

---

## 🔧 Code Quality

```bash
black .                            # auto-format
flake8 . --max-line-length=88      # lint
pre-commit install                 # install git hooks
pre-commit run --all-files         # run hooks manually
```

---

## 🏷️ Custom Markers

| Marker        | Description                              |
|---------------|------------------------------------------|
| `ui`          | Playwright browser-based UI tests        |
| `api`         | HTTP REST API tests                      |
| `smoke`       | Critical path tests (fast subset)        |
| `regression`  | Full regression test suite               |
| `performance` | Response-time and threshold assertions   |

```bash
pytest -m "smoke and api"
pytest -m "ui and not regression"
pytest -m "performance"
```

---

## 🔬 Sample Applications

| Layer | Application          | URL                                      |
|-------|----------------------|------------------------------------------|
| UI    | SauceDemo            | https://www.saucedemo.com                |
| API   | JSONPlaceholder      | https://jsonplaceholder.typicode.com     |

---

## 📈 Performance Testing (Placeholder)

Basic response-time assertions are built into the API test suite via the `performance` marker.
For load testing, add Locust or k6 scripts to a `performance/` directory.

---

## 📜 License

MIT
