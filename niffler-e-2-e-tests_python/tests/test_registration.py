from pages.login_page import login_page
from pages.registration_page import registration_page
from selene import browser


def test_successful_registration(envs):
    browser.open(envs.app_url)
    user, password = envs.test_username, envs.test_password

    login_page.create_new_user_button.click()
    registration_page.sign_up(user, password, password)

    registration_page.check_registration_message()


def test_register_with_mismatched_password(envs, generate_test_user):
    browser.open(envs.app_url)
    user = generate_test_user
    password = "password123"
    mismatched_password = "password321"

    login_page.create_new_user_button.click()
    registration_page.sign_up(user, password, mismatched_password)

    registration_page.check_error_message()


def test_register_existed_user(envs):
    browser.open(envs.app_url)
    existed_user = envs.test_username
    password = "pass123"

    login_page.create_new_user_button.click()
    registration_page.sign_up(existed_user, password, password)

    registration_page.check_error_message(existed_user)


def test_register_user_with_less_than_3_chars_username(envs):
    browser.open(envs.app_url)
    user = envs.test_username[0:2]
    password = envs.test_password

    login_page.create_new_user_button.click()
    registration_page.sign_up(user, password, password)
    registration_page.check_error_message(not_allowed_username=True)


def test_register_user_with_less_than_3_chars_password(envs, generate_test_user):
    browser.open(envs.app_url)
    user = generate_test_user
    password = envs.test_password[0:2]

    login_page.create_new_user_button.click()
    registration_page.sign_up(user, password, password)
    registration_page.check_error_message(not_allowed_password=True)
