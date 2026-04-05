# Selenium to Playwright Migration Guide

## Overview

This guide provides a complete, practical reference for migrating a Python-based Selenium WebDriver test framework to Playwright. It covers conceptual differences, direct API translations, architecture changes, and a phased migration plan.

---

## Part 1: Conceptual Differences

### Browser Management

| Concept | Selenium | Playwright |
|---|---|---|
| Browser launch | `webdriver.Chrome()` | `playwright.chromium.launch()` |
| Driver management | ChromeDriver/GeckoDriver binary | Built-in (no external driver) |
| Session isolation | WebDriver session | `BrowserContext` |
| Parallel browsers | External Grid | Native `BrowserContext` per test |
| Resource cleanup | `driver.quit()` | `browser.close()` / context manager |

**Key insight:** Playwright separates `Browser` (the process) from `BrowserContext` (an isolated session) from `Page` (a tab). This maps to: `Browser → Context → Page`.

### Waiting Strategy

| Scenario | Selenium | Playwright |
|---|---|---|
| Wait for element visible | `WebDriverWait(driver, 10).until(EC.visibility_of_element_located(...))` | `page.locator(...).wait_for(state="visible")` — or just act; auto-wait handles it |
| Wait for clickable | `EC.element_to_be_clickable(...)` | Automatic; `click()` auto-waits |
| Fixed sleep | `time.sleep(2)` | **Never use.** `page.wait_for_load_state("networkidle")` |
| URL change | `WebDriverWait(...).until(EC.url_contains("dashboard"))` | `page.wait_for_url("**/dashboard**")` |
| Element count | Custom polling loop | `expect(page.locator("li")).to_have_count(5)` |

**Critical rule:** Delete all `time.sleep()` calls during migration. Replace with Playwright's auto-wait or explicit wait conditions.

### Selectors

| Selector Type | Selenium | Playwright |
|---|---|---|
| ID | `By.ID, "username"` | `page.locator("#username")` |
| CSS | `By.CSS_SELECTOR, ".btn"` | `page.locator(".btn")` |
| XPath | `By.XPATH, "//button"` | `page.locator("xpath=//button")` |
| Text content | `By.XPATH, "//*[text()='Login']"` | `page.get_by_text("Login")` |
| ARIA role | Manual XPath | `page.get_by_role("button", name="Login")` |
| Test ID | `By.CSS_SELECTOR, "[data-testid='btn']"` | `page.get_by_test_id("btn")` |
| Placeholder | `By.CSS_SELECTOR, "[placeholder='Email']"` | `page.get_by_placeholder("Email")` |
| Label | `By.XPATH, complex` | `page.get_by_label("Email address")` |

**Recommendation:** Prefer `get_by_role`, `get_by_text`, `get_by_label` over CSS/XPath in Playwright. These are more resilient to UI changes and align with accessibility.

---

## Part 2: Direct API Translation

### Setup

**Selenium (Python)**

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)
driver.maximize_window()
```

**Playwright (Python)**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    page = context.new_page()
```

---

### Navigation

| Action | Selenium | Playwright |
|---|---|---|
| Open URL | `driver.get("https://example.com")` | `page.goto("https://example.com")` |
| Go back | `driver.back()` | `page.go_back()` |
| Go forward | `driver.forward()` | `page.go_forward()` |
| Refresh | `driver.refresh()` | `page.reload()` |
| Get URL | `driver.current_url` | `page.url` |
| Get title | `driver.title` | `page.title()` |

---

### Finding Elements

**Selenium**

```python
from selenium.webdriver.common.by import By

element = driver.find_element(By.ID, "username")
elements = driver.find_elements(By.CSS_SELECTOR, ".item")
```

**Playwright**

```python
# Returns a Locator (lazy, not yet found)
locator = page.locator("#username")
locators = page.locator(".item")

# Playwright prefers user-visible queries
locator = page.get_by_role("textbox", name="Username")
```

**Important:** Playwright's `locator()` is lazy — it describes _how_ to find the element, not the element itself. Actions (`click`, `fill`, etc.) trigger the actual lookup with auto-wait.

---

### Interactions

| Action | Selenium | Playwright |
|---|---|---|
| Click | `element.click()` | `page.locator("#btn").click()` |
| Type/fill | `element.send_keys("text")` | `page.locator("#input").fill("text")` |
| Clear + type | `element.clear(); element.send_keys(...)` | `page.locator("#input").fill("new value")` (fill clears first) |
| Press key | `element.send_keys(Keys.ENTER)` | `page.keyboard.press("Enter")` |
| Select dropdown | `Select(element).select_by_visible_text("Option")` | `page.locator("select").select_option(label="Option")` |
| Checkbox | `element.click()` | `page.locator("#chk").check()` / `.uncheck()` |
| Hover | `ActionChains(driver).move_to_element(el).perform()` | `page.locator("#menu").hover()` |
| Double-click | `ActionChains(driver).double_click(el).perform()` | `page.locator("#el").dbl_click()` |
| Right-click | `ActionChains(driver).context_click(el).perform()` | `page.locator("#el").click(button="right")` |
| Drag and drop | `ActionChains(driver).drag_and_drop(src, tgt)` | `page.drag_and_drop("#src", "#tgt")` |
| Upload file | `element.send_keys("/path/to/file")` | `page.locator("#file").set_input_files("/path/to/file")` |

---

### Assertions

**Selenium**

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Text present
assert "Welcome" in driver.find_element(By.TAG_NAME, "h1").text

# Element visible
assert driver.find_element(By.ID, "error").is_displayed()

# URL
assert "dashboard" in driver.current_url
```

**Playwright (using `expect` — Web-First Assertions)**

```python
from playwright.sync_api import expect

# Text content
expect(page.locator("h1")).to_contain_text("Welcome")

# Visibility
expect(page.locator("#error")).to_be_visible()

# URL
expect(page).to_have_url(re.compile(".*dashboard.*"))

# Element count
expect(page.locator(".item")).to_have_count(5)

# Input value
expect(page.locator("#username")).to_have_value("admin")

# Attribute
expect(page.locator("button")).to_have_attribute("disabled", "")
```

**Important:** `expect()` assertions in Playwright **retry automatically** until the condition is met or timeout expires. Do not wrap in `WebDriverWait`.

---

### Screenshots

| Action | Selenium | Playwright |
|---|---|---|
| Full page | `driver.save_screenshot("screen.png")` | `page.screenshot(path="screen.png", full_page=True)` |
| Element only | Manual crop | `page.locator("#el").screenshot(path="el.png")` |

---

### iFrames

**Selenium**

```python
driver.switch_to.frame(driver.find_element(By.ID, "iframe"))
# ... interact ...
driver.switch_to.default_content()
```

**Playwright**

```python
frame = page.frame_locator("#iframe")
frame.locator("#inside-iframe").click()
# No need to switch back — Playwright handles context automatically
```

---

### JavaScript Execution

| Action | Selenium | Playwright |
|---|---|---|
| Execute JS | `driver.execute_script("return document.title")` | `page.evaluate("document.title")` |
| Async JS | `driver.execute_async_script(...)` | `page.evaluate("() => Promise.resolve(42)")` |
| Scroll | `driver.execute_script("window.scrollTo(0, 500)")` | `page.evaluate("window.scrollTo(0, 500)")` |

---

### Alerts and Dialogs

**Selenium**

```python
alert = driver.switch_to.alert
alert.accept()
alert.dismiss()
text = alert.text
```

**Playwright**

```python
# Register handler before action that triggers dialog
page.on("dialog", lambda dialog: dialog.accept())
page.locator("#trigger-alert").click()

# Or handle once
with page.expect_popup() as popup_info:
    page.locator("#open-popup").click()
popup = popup_info.value
```

---

### Cookies and Storage

| Action | Selenium | Playwright |
|---|---|---|
| Get cookies | `driver.get_cookies()` | `context.cookies()` |
| Add cookie | `driver.add_cookie({"name": ..., "value": ...})` | `context.add_cookies([{"name": ..., "value": ..., "url": ...}])` |
| Delete cookie | `driver.delete_cookie("name")` | `context.clear_cookies()` |
| LocalStorage | `driver.execute_script("...")` | `page.evaluate("localStorage.getItem('key')")` |
| Save auth state | Manual serialise | `context.storage_state(path="auth.json")` |

---

### Network Interception

**Selenium** — Not natively supported. Requires BrowserMob Proxy or similar.

**Playwright**

```python
# Block images to speed up tests
page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())

# Mock an API response
page.route("**/api/v1/users", lambda route: route.fulfill(
    status=200,
    json={"users": [{"id": 1, "name": "Test User"}]}
))

# Intercept and modify
def modify_response(route):
    response = route.fetch()
    body = response.json()
    body["feature_flag"] = True
    route.fulfill(response=response, json=body)

page.route("**/api/config", modify_response)
```

---

## Part 3: Page Object Model Migration

### Selenium POM (Before)

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://www.saucedemo.com"
    USERNAME_LOCATOR = (By.ID, "user-name")
    PASSWORD_LOCATOR = (By.ID, "password")
    LOGIN_BTN_LOCATOR = (By.ID, "login-button")
    ERROR_LOCATOR = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def enter_username(self, username):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_LOCATOR)).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_LOCATOR).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BTN_LOCATOR).click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.ERROR_LOCATOR)
            ).text
        except:
            return ""
```

### Playwright POM (After)

```python
from playwright.sync_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self, base_url: str) -> "LoginPage":
        self.navigate(base_url)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        self.page.fill(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self.page.fill(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        self.page.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        locator = self.page.locator(self.ERROR_MESSAGE)
        if locator.is_visible():
            return locator.inner_text()
        return ""
```

**Key differences:**
- No `WebDriverWait` — auto-wait is built-in
- Fluent return `self` for method chaining
- Type hints on all parameters
- No `By.X, "selector"` tuple pattern — plain CSS string

---

## Part 4: Fixture Migration (pytest)

### Selenium conftest.py (Before)

```python
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
```

### Playwright conftest.py (After)

```python
import pytest
from playwright.sync_api import sync_playwright, BrowserContext, Page

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture
def browser_context(browser) -> BrowserContext:
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    context.tracing.start(screenshots=True, snapshots=True)
    yield context
    context.tracing.stop(path="trace.zip")
    context.close()

@pytest.fixture
def page(browser_context) -> Page:
    page = browser_context.new_page()
    yield page
    page.close()
```

---

## Part 5: Phased Migration Plan

### Phase 0: Preparation (Week 1)

- [ ] Audit existing Selenium test suite: count tests, identify highest-value candidates
- [ ] Set up Playwright alongside Selenium (both can coexist during migration)
- [ ] Install `playwright`, `pytest-playwright`
- [ ] Set up base POM classes and fixtures (this framework)
- [ ] Team training: 1-day Playwright workshop

### Phase 1: Infrastructure Migration (Week 1–2)

- [ ] Migrate `conftest.py` fixtures from Selenium to Playwright
- [ ] Migrate `BasePage` class
- [ ] Set up CI pipeline for Playwright tests (run alongside Selenium during transition)
- [ ] Establish naming conventions and coding standards

### Phase 2: Smoke Tests (Week 2–3)

- [ ] Migrate P0 critical path tests (login, checkout, core navigation)
- [ ] Target: 20–30 tests
- [ ] Validate cross-browser execution (Chromium, Firefox, WebKit)
- [ ] Verify CI pipeline is green

### Phase 3: Regression Suite (Week 3–8)

- [ ] Migrate feature area by feature area (not test by test)
- [ ] Prioritise by risk: P0 → P1 → P2
- [ ] Delete Selenium equivalents as each area is migrated
- [ ] Target: 80% coverage parity with legacy suite

### Phase 4: Enhancement (Week 8–12)

- [ ] Add network interception tests (impossible in Selenium)
- [ ] Add trace/video capture to CI
- [ ] Add performance assertions to API tests
- [ ] Implement authentication state caching

### Phase 5: Decommission Selenium

- [ ] All tests green in Playwright
- [ ] Remove `selenium`, `webdriver-manager` from `requirements.txt`
- [ ] Archive Selenium test code in a `legacy/` branch
- [ ] Final team training: advanced Playwright patterns

---

## Part 6: Common Migration Pitfalls

### 1. Keeping `time.sleep()` — Fatal Mistake

```python
# ❌ Selenium habit — never do this in Playwright
time.sleep(2)
page.click("#submit")

# ✅ Playwright way — auto-wait handles it
page.click("#submit")
# OR for explicit conditions:
page.wait_for_load_state("networkidle")
```

### 2. Using `find_element` Mental Model

```python
# ❌ Wrong — treating locator like a found element
element = page.locator("#username")
element.is_displayed()  # AttributeError in Playwright

# ✅ Correct — use Playwright's locator methods
page.locator("#username").is_visible()
```

### 3. Forgetting BrowserContext Isolation

```python
# ❌ Sharing one context between tests — leaks cookies/storage
page1 = browser.new_page()  # Bad: pages in same hidden context

# ✅ Each test gets its own context
context = browser.new_context()
page1 = context.new_page()
```

### 4. Wrong `expect()` Import

```python
# ❌ pytest assertion — does not auto-retry
assert page.locator("h1").inner_text() == "Welcome"

# ✅ Playwright expect — retries until timeout
from playwright.sync_api import expect
expect(page.locator("h1")).to_have_text("Welcome")
```

### 5. Not Using `wait_for_url` After Navigation

```python
# ❌ Race condition — checking URL before navigation completes
page.click("#login-btn")
assert "dashboard" in page.url  # May fail intermittently

# ✅ Explicit URL wait
page.click("#login-btn")
page.wait_for_url("**/dashboard**")
assert "dashboard" in page.url
```
