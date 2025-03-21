from selene import browser, have
import allure


class ProfilePage:
    def __init__(self):
        self.username = browser.element('#username')
        self.name = browser.element('#name')
        self.save_changes = browser.element("//button[.='Save changes']")
        self.category = browser.element('#category')
        self.created_category = lambda name: browser.element(f'//span[normalize-space(text())="{name}"]')
        self.edit_category_button = browser.element('button[aria-label="Edit category"]')
        self.edit_category_input = browser.element('//input[@placeholder="Edit category"]')
        self.archive_button = browser.element('button[aria-label="Archive category"]')
        self.confirm_archive = browser.element('//button[normalize-space(text())="Archive"]')

    @allure.step('UI: Check username in profile')
    def check_username_is_correct(self, username: str):
        self.username.should(have.value(username))

    @allure.step('UI: Change name in profile')
    def set_name(self, new_name: str):
        self.name.clear().type(new_name)
        self.save_changes.click()

    @allure.step('UI: Verify name in profile')
    def check_name_is_correct(self, name):
        self.name.should(have.value(name))

    @allure.step('UI: Create a category')
    def create_category(self, category_name):
        self.category.type(category_name).press_enter()

    @allure.step('UI: Edit category name')
    def edit_category_name(self, name):
        self.edit_category_button.click()
        self.edit_category_input.clear().type(name).press_enter()

    @allure.step('UI: Verify category name')
    def check_category_name(self, name):
        self.created_category(name).should(have.text(name))

    @allure.step('UI: Place a category in archive')
    def archive_category(self):
        self.archive_button.click()
        self.confirm_archive.click()


profile = ProfilePage()
