import os
import pytest
from pages.spending_page import spending_page
from pages.login_page import login_page


@pytest.fixture(scope="function", autouse=True)
def login():
    user = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    login_page.sign_in(user, password)


def test_spending_title_exists():
    spending_page.check_spending_page_titles()


def test_create_spending():
    spending_page.new_spending.click()
    spending_page.create_spending(100, 'RUB', 'test')

    spending_page.check_spending_exists('test', 100)


