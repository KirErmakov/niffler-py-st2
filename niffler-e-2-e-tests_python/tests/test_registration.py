import os
from pages.login_page import login_page
from pages.registration_page import registration_page


def test_successful_registration(generate_test_user):
    user = generate_test_user
    password = "password123"

    login_page.create_new_user_button.click()
    registration_page.sign_up(user, password, password)

    registration_page.check_registration_message()


def test_register_with_mismatched_password(generate_test_user):
    user = generate_test_user
    password = "password123"
    mismatched_password = "password321"

    login_page.create_new_user_button.click()
    registration_page.sign_up(user, password, mismatched_password)

    registration_page.check_error_message()


def test_register_existed_user():
    user = os.getenv('USERNAME')
    password = "pass123"

    login_page.create_new_user_button.click()
    registration_page.sign_up(user, password, password)

    registration_page.check_error_message(user)
