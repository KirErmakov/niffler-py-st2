import os

import allure
import pytest
from pages.login_page import login_page
from pages.spending_page import spending_page
from selene import browser

pytestmark = [
    pytest.mark.allure_label('User Management', label_type="epic"),
    pytest.mark.allure_label('Log In', label_type='feature')
    ]


@allure.story('Successful login')
def test_successful_login(auth):
    spending_page.check_spending_page_titles()


@allure.story('Non existed user')
def test_non_existed_user_login(envs):
    browser.open(envs.app_url)
    user, password = "invalid_user", "invalid_password"

    login_page.sign_in(user, password)

    login_page.check_error_message()


@allure.story('Wrong password')
def test_login_with_wrong_password(envs):
    browser.open(envs.app_url)
    user = os.getenv("USERNAME")
    wrong_password = 'wrnpass1'

    login_page.sign_in(user, wrong_password)

    login_page.check_error_message()


@allure.story('Sign out')
def test_sign_out(auth):
    spending_page.sign_out()
    login_page.check_page_elements()
