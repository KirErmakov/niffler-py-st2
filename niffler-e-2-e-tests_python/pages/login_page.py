from selene import browser, be


class LoginPage:
    def __init__(self):
        self.username = browser.element('input[name=username]')
        self.password = browser.element('input[name=password]')
        self.login_button = browser.element('button[type=submit]')
        self.create_new_user_button = browser.element('.form__register')
        self.error_message = browser.element("//p[@class='form__error']")

    def sign_in(self, user: str, password: str):
        self.username.should(be.blank).type(user)
        self.password.should(be.blank).type(password)
        self.login_button.click()

    def check_error_message(self):
        self.error_message.should(be.visible)


login_page = LoginPage()