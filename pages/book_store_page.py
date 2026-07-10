from dataclasses import dataclass

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.book_details_page import BookDetailsPage
from utils.config import BOOKS_URL


@dataclass(frozen=True)
class BookRowData:
    title: str
    author: str
    publisher: str


class BookStorePage(BasePage):
    SEARCH_INPUT = (By.ID, "searchBox")
    BOOK_ROWS = (By.CSS_SELECTOR, "table tbody tr")
    LOGIN_BUTTON = (By.ID, "login")

    def open(self) -> "BookStorePage":
        self.driver.get(BOOKS_URL)
        self.dismiss_overlays()
        self.wait_for_visible(self.SEARCH_INPUT)
        return self

    def search_for(self, query: str) -> "BookStorePage":
        self.type_text(self.SEARCH_INPUT, query)
        return self

    def wait_for_row_count(self, expected_count: int) -> "BookStorePage":
        self.wait.until(
            lambda driver: len(driver.find_elements(*self.BOOK_ROWS)) == expected_count
        )
        return self

    def get_visible_book_rows(self) -> list[BookRowData]:
        rows = self.driver.find_elements(*self.BOOK_ROWS)
        book_rows: list[BookRowData] = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 4:
                continue
            book_rows.append(
                BookRowData(
                    title=cells[1].text.strip(),
                    author=cells[2].text.strip(),
                    publisher=cells[3].text.strip(),
                )
            )
        return book_rows

    def click_book_title(self, title: str) -> BookDetailsPage:
        title_link = (
            By.XPATH,
            f"//table//tbody//tr//a[normalize-space()='{title}']",
        )
        self.click(title_link)
        self.wait_for_url_contains("search=")
        details_page = BookDetailsPage(self.driver)
        details_page.wait_until_loaded()
        return details_page

    def go_to_login(self) -> "LoginPage":
        from pages.login_page import LoginPage

        self.click(self.LOGIN_BUTTON)
        login_page = LoginPage(self.driver)
        login_page.wait_until_loaded()
        return login_page
