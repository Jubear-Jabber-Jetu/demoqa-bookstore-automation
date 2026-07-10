from pages.book_store_page import BookStorePage
from utils.config import (
    GIT_POCKET_GUIDE_AUTHOR,
    GIT_POCKET_GUIDE_PUBLISHER,
    GIT_POCKET_GUIDE_TITLE,
)


def test_search_returns_correct_result(driver):
    bookstore = BookStorePage(driver).open()
    bookstore.search_for(GIT_POCKET_GUIDE_TITLE)
    bookstore.wait_for_row_count(1)

    rows = bookstore.get_visible_book_rows()
    assert len(rows) == 1, f"Expected exactly 1 book row, got {len(rows)}"

    book = rows[0]
    assert book.title == GIT_POCKET_GUIDE_TITLE, (
        f"Expected title {GIT_POCKET_GUIDE_TITLE!r}, got {book.title!r}"
    )
    assert book.author == GIT_POCKET_GUIDE_AUTHOR, (
        f"Expected author {GIT_POCKET_GUIDE_AUTHOR!r}, got {book.author!r}"
    )
    assert book.publisher == GIT_POCKET_GUIDE_PUBLISHER, (
        f"Expected publisher {GIT_POCKET_GUIDE_PUBLISHER!r}, got {book.publisher!r}"
    )
