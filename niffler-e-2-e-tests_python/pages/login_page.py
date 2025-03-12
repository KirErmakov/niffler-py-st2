from selene import browser, be
import allure


class LoginPage:
    def __init__(self):
        self.username = browser.element('input[name=username]')
        self.password = browser.element('input[name=password]')
        self.login_button = browser.element('button[type=submit]')
        self.create_new_user_button = browser.element('.form__register')
        self.error_message = browser.element("//p[@class='form__error']")
        self.log_in_header = browser.element('h1.header')

    @allure.step('UI: Sign in')
    def sign_in(self, user: str, password: str):
        self.username.should(be.blank).type(user)
        self.password.should(be.blank).type(password)
        self.login_button.click()

    @allure.step('UI: Check login error message')
    def check_error_message(self):
        self.error_message.should(be.visible)

    @allure.step('UI: Check elements on login page')
    def check_page_elements(self):
        self.log_in_header.should(be.visible)
        self.username.should(be.blank)
        self.password.should(be.blank)
        self.login_button.should(be.visible.and_(be.clickable))
        self.create_new_user_button.should(be.visible.and_(be.clickable))


login_page = LoginPage()
