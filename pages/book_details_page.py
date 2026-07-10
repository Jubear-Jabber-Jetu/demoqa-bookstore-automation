from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class BookDetailsPage(BasePage):
    ISBN_WRAPPER = (By.ID, "ISBN-wrapper")
    TITLE_WRAPPER = (By.ID, "title-wrapper")
    AUTHOR_WRAPPER = (By.ID, "author-wrapper")
    PUBLISHER_WRAPPER = (By.ID, "publisher-wrapper")
    PAGES_WRAPPER = (By.ID, "pages-wrapper")
    ADD_TO_COLLECTION_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Add To Your Collection']",
    )

    FIELD_VALUE_SELECTOR = ".col-md-9 label"

    def wait_until_loaded(self) -> "BookDetailsPage":
        self.dismiss_overlays()
        self.wait_for_visible(self.ISBN_WRAPPER)
        return self

    def _get_wrapper_value(self, wrapper_locator: tuple[str, str]) -> str:
        wrapper = self.wait_for_visible(wrapper_locator)
        value_element = wrapper.find_element(By.CSS_SELECTOR, self.FIELD_VALUE_SELECTOR)
        return value_element.text.strip()

    def get_isbn(self) -> str:
        return self._get_wrapper_value(self.ISBN_WRAPPER)

    def get_title(self) -> str:
        return self._get_wrapper_value(self.TITLE_WRAPPER)

    def get_author(self) -> str:
        return self._get_wrapper_value(self.AUTHOR_WRAPPER)

    def get_publisher(self) -> str:
        return self._get_wrapper_value(self.PUBLISHER_WRAPPER)

    def get_total_pages(self) -> str:
        return self._get_wrapper_value(self.PAGES_WRAPPER)

    def add_to_collection(self) -> str:
        self.click(self.ADD_TO_COLLECTION_BUTTON)
        return self.wait_for_alert_text()

    def go_to_profile(self) -> "ProfilePage":
        from pages.profile_page import ProfilePage
        from utils.config import PROFILE_URL

        self.driver.get(PROFILE_URL)
        profile_page = ProfilePage(self.driver)
        profile_page.wait_until_loaded()
        return profile_page
