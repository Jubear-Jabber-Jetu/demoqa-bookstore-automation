from pages.book_store_page import BookStorePage
from utils.config import GIT_POCKET_GUIDE_ISBN, GIT_POCKET_GUIDE_TITLE


def test_book_details_navigation(driver):
    bookstore = BookStorePage(driver).open()
    bookstore.search_for(GIT_POCKET_GUIDE_TITLE)
    bookstore.wait_for_row_count(1)

    details_page = bookstore.click_book_title(GIT_POCKET_GUIDE_TITLE)

    title = details_page.get_title()
    author = details_page.get_author()
    publisher = details_page.get_publisher()
    isbn = details_page.get_isbn()
    total_pages = details_page.get_total_pages()

    assert title, f"Expected a non-empty title, got {title!r}"
    assert author, f"Expected a non-empty author, got {author!r}"
    assert publisher, f"Expected a non-empty publisher, got {publisher!r}"
    assert isbn, f"Expected a non-empty ISBN, got {isbn!r}"
    assert total_pages, f"Expected non-empty total pages, got {total_pages!r}"

    assert isbn == GIT_POCKET_GUIDE_ISBN, (
        f"Expected ISBN {GIT_POCKET_GUIDE_ISBN}, got {isbn}"
    )
