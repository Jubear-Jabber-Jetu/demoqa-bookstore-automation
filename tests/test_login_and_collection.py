from pages.book_store_page import BookStorePage
from pages.login_page import LoginPage
from utils.config import (
    BOOK_ADDED_ALERT_TEXT,
    GIT_POCKET_GUIDE_TITLE,
    TEST_PASSWORD,
    TEST_USERNAME,
)


def test_login_and_add_to_collection(driver, clean_user_collection):
    login_page = LoginPage(driver).open()
    profile_page = login_page.login(TEST_USERNAME, TEST_PASSWORD)

    bookstore = BookStorePage(driver).open()
    bookstore.search_for(GIT_POCKET_GUIDE_TITLE)
    bookstore.wait_for_row_count(1)
    details_page = bookstore.click_book_title(GIT_POCKET_GUIDE_TITLE)

    confirmation_message = details_page.add_to_collection()
    assert confirmation_message == BOOK_ADDED_ALERT_TEXT, (
        f"Expected confirmation {BOOK_ADDED_ALERT_TEXT!r}, got {confirmation_message!r}"
    )

    profile_page = details_page.go_to_profile()
    profile_page.wait_for_book_in_collection(GIT_POCKET_GUIDE_TITLE)
    collection_titles = profile_page.get_collection_titles()

    assert GIT_POCKET_GUIDE_TITLE in collection_titles, (
        f"Expected {GIT_POCKET_GUIDE_TITLE!r} in collection, got {collection_titles!r}"
    )
