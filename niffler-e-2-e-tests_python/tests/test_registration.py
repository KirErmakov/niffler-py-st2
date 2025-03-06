import os
from pages.login_page import login_page
from pages.registration_page import registration_page
from selene import browser


def test_successful_registration(app_url, app_user):
    browser.open(app_url)
    user, password = app_user

    login_page.create_new_user_button.click()
    registration_page.sign_up(user, password, password)

    registration_page.check_registration_message()


def test_register_with_mismatched_password(app_url, generate_test_user):
    browser.open(app_url)
    user = generate_test_user
    password = "password123"
    mismatched_password = "password321"

    login_page.create_new_user_button.click()
    registration_page.sign_up(user, password, mismatched_password)

    registration_page.check_error_message()


def test_register_existed_user(app_url):
    browser.open(app_url)
    existed_user = os.getenv('TEST_USERNAME')
    password = "pass123"

    login_page.create_new_user_button.click()
    registration_page.sign_up(existed_user, password, password)

    registration_page.check_error_message(existed_user)
