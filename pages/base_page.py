from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import DEFAULT_TIMEOUT


class BasePage:
    """Shared WebDriver helpers and explicit-wait utilities."""

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def dismiss_overlays(self) -> None:
        """Close ad overlays that can block clicks on DemoQA."""
        for locator in ("#close-fixedban", "#fixedban"):
            elements = self.driver.find_elements("css selector", locator)
            for element in elements:
                try:
                    element.click()
                except Exception:
                    pass

    def wait_for_visible(self, locator: tuple[str, str]):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator: tuple[str, str]):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: tuple[str, str]) -> None:
        element = self.wait_for_clickable(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )
        element = self.wait_for_clickable(locator)
        try:
            element.click()
        except ElementClickInterceptedException:
            element = self.wait_for_clickable(locator)
            self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator: tuple[str, str], text: str) -> None:
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple[str, str]) -> str:
        element = self.wait_for_visible(locator)
        return element.text.strip()

    def wait_for_url_contains(self, fragment: str) -> None:
        self.wait.until(EC.url_contains(fragment))

    def wait_for_alert_text(self) -> str:
        alert = self.wait.until(EC.alert_is_present())
        text = alert.text.strip()
        alert.accept()
        return text
