from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.profile_page import ProfilePage
from utils.config import LOGIN_URL


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "userName")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login")
    ERROR_MESSAGE = (By.ID, "name")

    def open(self) -> "LoginPage":
        self.driver.get(LOGIN_URL)
        self.dismiss_overlays()
        return self.wait_until_loaded()

    def wait_until_loaded(self) -> "LoginPage":
        self.wait_for_visible(self.USERNAME_INPUT)
        return self

    def login(self, username: str, password: str) -> ProfilePage:
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        profile_page = ProfilePage(self.driver)
        profile_page.wait_until_loaded()
        return profile_page

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)
