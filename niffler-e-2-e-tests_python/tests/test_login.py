import os
from pages.login_page import login_page
from pages.spending_page import spending_page
from selene import browser


def test_successful_login(auth):
    spending_page.check_spending_page_titles()


def test_non_existed_user_login(envs):
    browser.open(envs.app_url)
    user, password = "invalid_user", "invalid_password"

    login_page.sign_in(user, password)

    login_page.check_error_message()


def test_login_with_wrong_password(envs):
    browser.open(envs.app_url)
    user = os.getenv("USERNAME")
    wrong_password = 'wrnpass1'

    login_page.sign_in(user, wrong_password)

    login_page.check_error_message()


def test_sign_out(auth):
    spending_page.sign_out()
    login_page.check_page_elements()
