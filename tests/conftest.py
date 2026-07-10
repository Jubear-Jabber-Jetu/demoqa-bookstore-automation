from pathlib import Path

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.config import (
    BASE_URL,
    TEST_PASSWORD,
    TEST_USERNAME,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome in headless mode",
    )


@pytest.fixture(scope="session")
def ensure_test_user() -> None:
    """Ensure the configured test account exists via the DemoQA Account API."""
    response = requests.post(
        f"{BASE_URL}/Account/v1/User",
        json={"userName": TEST_USERNAME, "password": TEST_PASSWORD},
        timeout=30,
    )
    if response.status_code not in (201, 406):
        response.raise_for_status()


@pytest.fixture(scope="function")
def clean_user_collection(ensure_test_user) -> None:
    """Remove all books from the test user's collection before collection tests."""
    login_response = requests.post(
        f"{BASE_URL}/Account/v1/Login",
        json={"userName": TEST_USERNAME, "password": TEST_PASSWORD},
        timeout=30,
    )
    login_response.raise_for_status()
    login_data = login_response.json()
    token = login_data["token"]
    user_id = login_data["userId"]
    headers = {"Authorization": f"Bearer {token}"}

    user_response = requests.get(
        f"{BASE_URL}/Account/v1/User/{user_id}",
        headers=headers,
        timeout=30,
    )
    user_response.raise_for_status()
    books = user_response.json().get("books", [])

    for book in books:
        delete_response = requests.delete(
            f"{BASE_URL}/BookStore/v1/Book",
            json={"isbn": book["isbn"], "userId": user_id},
            headers=headers,
            timeout=30,
        )
        delete_response.raise_for_status()


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest):
    headless = request.config.getoption("--headless")
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)
    if not headless:
        browser.maximize_window()

    def capture_screenshot_and_quit() -> None:
        report = getattr(request.node, "rep_call", None)
        if report is not None:
            SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
            if report.passed:
                screenshot_path = SCREENSHOTS_DIR / f"{request.node.name}.png"
            else:
                screenshot_path = SCREENSHOTS_DIR / f"{request.node.name}_failed.png"
            browser.save_screenshot(str(screenshot_path))
        browser.quit()

    request.addfinalizer(capture_screenshot_and_quit)

    return browser


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
