# DemoQA Book Store — Selenium UI Automation

[![UI Tests](https://github.com/Jubear-Jabber-Jetu/demoqa-bookstore-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/Jubear-Jabber-Jetu/demoqa-bookstore-automation/actions/workflows/ci.yml)
[![Test Report](https://img.shields.io/badge/Test%20Report-view-2ea44f.svg)](https://jubear-jabber-jetu.github.io/demoqa-bookstore-automation/)
[![Screenshots](https://img.shields.io/badge/Screenshots-view-blue.svg)](https://jubear-jabber-jetu.github.io/demoqa-bookstore-automation/#screenshots)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Selenium 4](https://img.shields.io/badge/selenium-4.x-43B02A.svg)](https://www.selenium.dev/)
[![pytest](https://img.shields.io/badge/pytest-8.x-0A9EDC.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Production-ready UI automation framework for the [DemoQA Book Store](https://demoqa.com/books). Built with **Python**, **Selenium 4**, **pytest**, and the **Page Object Model (POM)** — designed for maintainability, explicit waits, and CI/CD integration.

**Latest CI results (updated after every push to `main`):**
- [Test Report & Screenshots](https://jubear-jabber-jetu.github.io/demoqa-bookstore-automation/)
- [HTML Report only](https://jubear-jabber-jetu.github.io/demoqa-bookstore-automation/report.html)

---

## Features

- **Page Object Model** — one class per page; locators and actions isolated from test logic
- **Explicit waits only** — `WebDriverWait` + `expected_conditions`; no `time.sleep()`
- **Headless support** — `--headless` CLI flag for local runs and CI pipelines
- **Automatic screenshots** — captured on every successful test; `_failed` suffix on failures
- **HTML & JUnit reports** — generated in CI and published as downloadable artifacts
- **GitHub Actions CI** — headless tests on Python 3.10 with Chrome

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Browser automation | Selenium 4.x (Selenium Manager) |
| Test runner | pytest |
| Reporting | pytest-html, JUnit XML |
| CI/CD | GitHub Actions |

## Quick Start

### Prerequisites

- Python 3.10 or newer
- Google Chrome (Selenium Manager handles ChromeDriver)
- Internet access to `https://demoqa.com`

### Install

```bash
git clone https://github.com/Jubear-Jabber-Jetu/demoqa-bookstore-automation.git
cd demoqa-bookstore-automation
pip install -r requirements.txt
```

### Run Tests

```bash
# Headed browser
pytest -v

# Headless (recommended for CI / faster runs)
pytest -v --headless

# With HTML report
pytest -v --headless --html=reports/report.html --self-contained-html
```

Screenshots are saved to `screenshots/` after each test completes.

## Test Credentials

Credentials live in `utils/config.py` (not hardcoded in test files):

| Field | Value |
|-------|-------|
| Username | `qa_bookstore_assessment` |
| Password | `P@ssw0rd123!` |

The session fixture `ensure_test_user` registers this account via the [DemoQA Account API](https://demoqa.com/swagger/#/Account) if it does not already exist. UI registration at [/register](https://demoqa.com/register) requires reCAPTCHA.

## Test Scenarios

| Test | File | Description |
|------|------|-------------|
| `test_search_returns_correct_result` | `tests/test_search.py` | Search for *Git Pocket Guide*; verify single row with correct author and publisher |
| `test_book_details_navigation` | `tests/test_book_details.py` | Navigate to book details; validate Title, Author, Publisher, ISBN, and Total Pages |
| `test_login_and_add_to_collection` | `tests/test_login_and_collection.py` | Log in, add book to collection, confirm alert, verify on Profile page |

## Project Structure

```
demoqa-bookstore-automation/
├── .github/workflows/ci.yml   # GitHub Actions — headless tests, reports, artifacts
├── pages/                     # Page Object classes (no assertions)
│   ├── base_page.py           # Shared waits, click(), type_text(), get_text()
│   ├── book_store_page.py     # Search box, book table, navigation
│   ├── book_details_page.py   # Book metadata, Add To Collection
│   ├── login_page.py          # Login form
│   └── profile_page.py        # Collection table, logout
├── tests/
│   ├── conftest.py            # Driver fixture, headless flag, screenshot capture
│   ├── test_search.py
│   ├── test_book_details.py
│   └── test_login_and_collection.py
├── utils/
│   └── config.py              # URLs, timeouts, credentials, test data
├── reports/                   # HTML / JUnit output (generated)
├── screenshots/               # Per-test screenshots (generated)
├── requirements.txt
├── pytest.ini
└── README.md
```

## CI/CD Pipeline

Every push and pull request to `main` triggers the **UI Tests** workflow:

1. Installs Python 3.10 and Google Chrome
2. Runs `pytest --headless` with HTML and JUnit reporters
3. Publishes test results to the GitHub Checks tab
4. Uploads artifacts (retained 30 days): `html-report`, `junit-report`, `screenshots`
5. **Publishes a public report site to GitHub Pages** (main branch only)

### Public report links (About sidebar + README)

| Resource | URL |
|----------|-----|
| Test results home | https://jubear-jabber-jetu.github.io/demoqa-bookstore-automation/ |
| HTML report | https://jubear-jabber-jetu.github.io/demoqa-bookstore-automation/report.html |

These links appear in the repository **About → Website** field and are refreshed after each successful CI run on `main`.

Download artifacts from the **Actions** tab → select a workflow run → **Artifacts**.

## Screenshots & Reports

| Outcome | Screenshot path |
|---------|-----------------|
| Passed | `screenshots/<test_name>.png` |
| Failed | `screenshots/<test_name>_failed.png` |

## Design Principles

- **Stable locators** — prefer `id`, then CSS; XPath only when necessary
- **No WebElement leakage** — page methods return values, page objects, or `None`
- **Descriptive assertions** — `assert x == y, f"Expected {y}, got {x}"`
- **Fixture-driven setup** — browser lifecycle, user provisioning, and collection cleanup in `conftest.py`

## License

This project is licensed under the [MIT License](LICENSE).
