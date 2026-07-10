"""Application URLs, test data, and timeout constants."""

BASE_URL = "https://demoqa.com"
BOOKS_URL = f"{BASE_URL}/books"
LOGIN_URL = f"{BASE_URL}/login"
REGISTER_URL = f"{BASE_URL}/register"
PROFILE_URL = f"{BASE_URL}/profile"

DEFAULT_TIMEOUT = 15

# Registered once via https://demoqa.com/register or the Account API.
# UI registration requires reCAPTCHA; use the API if the account does not exist yet.
TEST_USERNAME = "qa_bookstore_assessment"
TEST_PASSWORD = "P@ssw0rd123!"

GIT_POCKET_GUIDE_TITLE = "Git Pocket Guide"
GIT_POCKET_GUIDE_AUTHOR = "Richard E. Silverman"
GIT_POCKET_GUIDE_PUBLISHER = "O'Reilly Media"
GIT_POCKET_GUIDE_ISBN = "9781449325862"

BOOK_ADDED_ALERT_TEXT = "Book added to your collection."
