from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import PROFILE_URL


class ProfilePage(BasePage):
    COLLECTION_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    LOGOUT_BUTTON = (By.XPATH, "//button[normalize-space()='Log out' or normalize-space()='Logout']")

    def open(self) -> "ProfilePage":
        self.driver.get(PROFILE_URL)
        self.dismiss_overlays()
        return self.wait_until_loaded()

    def wait_until_loaded(self) -> "ProfilePage":
        self.wait.until(
            lambda driver: "profile" in driver.current_url
            or driver.find_elements(*self.COLLECTION_ROWS)
            or driver.find_elements(*self.LOGOUT_BUTTON)
        )
        return self

    def get_collection_titles(self) -> list[str]:
        rows = self.driver.find_elements(*self.COLLECTION_ROWS)
        titles: list[str] = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                titles.append(cells[1].text.strip())
        return titles

    def wait_for_book_in_collection(self, title: str) -> "ProfilePage":
        self.wait.until(
            lambda driver: title
            in [
                row.find_elements(By.TAG_NAME, "td")[1].text.strip()
                for row in driver.find_elements(*self.COLLECTION_ROWS)
                if len(row.find_elements(By.TAG_NAME, "td")) >= 2
            ]
        )
        return self

    def logout(self) -> None:
        self.click(self.LOGOUT_BUTTON)
