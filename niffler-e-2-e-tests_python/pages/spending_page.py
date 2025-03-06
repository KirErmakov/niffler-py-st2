from selene import browser, be, have


class SpendingPage:
    def __init__(self):
        self.history = browser.element('#spendings')
        self.statistics = browser.element('//*[@id="stat"]/h2')
        self.new_spending = browser.element("//a[@href='/spending']")
        self.spending_container = browser.element('#legend-container')
        self.amount = browser.element('input[name=amount]')
        self.currency = browser.element('#currency')
        self.category = browser.element('input[name=category]')
        self.description = browser.element('input[name=description]')
        self.add_button = browser.element('button[type=submit]')
        self.edit_button = browser.element('button[aria-label="Edit spending"]')
        self.save_changes = browser.element('#save')
        self.spending_checkbox = browser.element('input[type=checkbox]')
        self.delete_button = browser.element('button[id=delete]')
        self.delete_confirm = browser.element("//button[normalize-space()='Delete']")
        self.no_spendings_title = browser.element('//p[.="There are no spendings"]')
        self.successful_edit_message = browser.element('//div[.="Spending is edited successfully"]')

    def check_spending_page_titles(self):
        self.history.should(have.text('History of Spendings'))
        self.statistics.should(be.visible)

    def create_spending(self, amount: int, currency: str, category: str, description: str = None):
        self.amount.clear().should(be.blank).type(amount)

        if currency and currency != "RUB":
            self.currency.click()
            browser.element(f'.MuiButtonBase-root[data-value="{currency}"]').click()

        self.category.clear().should(be.blank).type(category)

        if description:
            self.description.should(be.blank).type(description)

        self.add_button.click()

    def check_spending_exists(self, category, amount):
        self.spending_container.should(have.text(f'{category} {amount}'))

    def edit_spending_description(self, text: str):
        self.edit_button.click()
        self.description.clear().send_keys(text)
        self.save_changes.click()

    def edit_spending_currency(self, currency: str):
        self.edit_button.click()
        self.currency.click()
        browser.element(f'.MuiButtonBase-root[data-value="{currency}"]').click()
        self.save_changes.click()

    def check_edit_should_be_successful(self):
        self.successful_edit_message.should(be.visible)

    def delete_spending(self):
        self.spending_checkbox.click()
        self.delete_button.click()
        self.delete_confirm.click()
        self.no_spendings_title.should(be.visible)


spending_page = SpendingPage()
