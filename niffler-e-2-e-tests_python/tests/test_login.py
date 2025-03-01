import os
from pages.login_page import login_page
from pages.spending_page import spending_page


def test_successful_login():
    user = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    login_page.sign_in(user, password)

    spending_page.check_spending_page_titles()


def test_non_existed_user_login():
    user, password = "invalid_user", "invalid_password"

    login_page.sign_in(user, password)

    login_page.check_error_message()


def test_login_with_wrong_password():
    user = os.getenv("USERNAME")
    wrong_password = 'wrnpass1'

    login_page.sign_in(user, wrong_password)

    login_page.check_error_message()
