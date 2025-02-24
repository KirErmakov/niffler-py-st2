from selene import browser, be, have


class SpendingPage:
    def __init__(self):
        self.history = browser.element('#spendings')
        self.statistics = browser.element('//*[@id="stat"]/h2')
        self.new_spending = browser.element("//a[@href='/spending']")
        self.spending_container = browser.element('#legend-container')
        self.amount = browser.element('input[name=amount]')
        self.currency = browser.element('input[name=currency]')
        self.category = browser.element('input[name=category]')
        self.description = browser.element('input[name=description]')
        self.add_button = browser.element('button[type=submit]')

    def check_spending_page_titles(self):
        self.history.should(have.text('History of Spendings'))
        self.statistics.should(be.visible)

    def create_spending(self, amount: int, currency: str, category: str, description: str = None):
        self.amount.clear().should(be.blank).type(amount)

        if currency and currency != "RUB":
            browser.element('div[id="currency"]').click()
            browser.element(f'.MuiButtonBase-root[data-value="{currency}"]').click()

        self.category.clear().should(be.blank).type(category)

        if description:
            self.description.should(be.blank).type(description)

        self.add_button.click()

    def check_spending_exists(self, category, amount):
        self.spending_container.should(have.text(f'{category} {amount}'))


spending_page = SpendingPage()
