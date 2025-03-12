from selene import browser, be, have
import allure


class RegistrationPage:
    def __init__(self):
        self.username = browser.element('input[name=username]')
        self.password = browser.element('input[name=password]')
        self.submit_password = browser.element('input[name=passwordSubmit]')
        self.sing_up_button = browser.element('button[class=form__submit]')
        self.registration_message = browser.element('.form__paragraph')
        self.error_message = browser.element('.form__error')

    @allure.step('UI: Sign up')
    def sign_up(self, user: str, password: str, submit_password: str):
        self.username.should(be.blank).type(user)
        self.password.should(be.blank).type(password)
        self.submit_password.should(be.blank).type(submit_password)
        self.sing_up_button.click()

    @allure.step('UI: Verify registration is successful')
    def check_registration_message(self):
        self.registration_message.should(have.text("Congratulations! You've registered"))

    @allure.step('UI: Verify registration error message is correct')
    def check_error_message(self, existed_username: str = None,
                            not_allowed_username: bool = False, not_allowed_password: bool = False):
        if existed_username:
            self.error_message.should(have.text(f'Username `{existed_username}` already exists'))

        elif not_allowed_username:
            self.error_message.should(have.text('Allowed username length should be from 3 to 50 characters'))

        elif not_allowed_password:
            self.error_message.should(have.text('Allowed password length should be from 3 to 12 characters'))

        else:
            self.error_message.should(have.text('Passwords should be equal'))


registration_page = RegistrationPage()
