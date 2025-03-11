import pytest
from faker import Faker
from models.category import CategoryAdd
from models.spend import SpendAdd
from pages.spending_page import spending_page
from marks import Pages, TestData

fake = Faker()
TEST_CATEGORY = fake.word()


@Pages.main_page
def test_spending_title_exists():
    spending_page.check_spending_page_titles()


@Pages.main_page
@TestData.delete_spend
def test_create_spending(auth, delete_spend):
    spending_page.new_spending.click()
    spending_page.create_spending(100, 'RUB', 'test')

    spending_page.check_spending_exists('test', 100)


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(
    SpendAdd(
        amount=110.55,
        description="QA.GURU Python Advanced 2",
        category=CategoryAdd(name=TEST_CATEGORY),
        spendDate="2025-02-28T18:39:27.955Z",
        currency="RUB"
    )
)
def test_delete_spending_via_table_actions(category, spends):
    spending_page.check_spending_exists(TEST_CATEGORY, '110.55')
    spending_page.delete_spending()


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(
    SpendAdd(
        amount=110.55,
        description="QA.GURU Python Advanced 2",
        category=CategoryAdd(name=TEST_CATEGORY),
        spendDate="2025-02-28T18:39:27.955Z",
        currency="RUB"
    )
)
@pytest.mark.parametrize('currency', ['USD', 'EUR', 'KZT'])
def test_edit_spending_currency(category, spends, currency):
    spending_page.edit_spending_currency(currency)
    spending_page.check_edit_should_be_successful()


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(
    SpendAdd(
        amount=110.55,
        description="QA.GURU Python Advanced 2",
        category=CategoryAdd(name=TEST_CATEGORY),
        spendDate="2025-02-28T18:39:27.955Z",
        currency="RUB"
    )
)
def test_edit_spending_description(category, spends):
    spending_page.edit_spending_description('New test')
    spending_page.check_edit_should_be_successful()


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(
    SpendAdd(
        amount=110.55,
        description="QA.GURU Python Advanced 2",
        category=CategoryAdd(name=TEST_CATEGORY),
        spendDate="2025-02-28T18:39:27.955Z",
        currency="RUB"
    )
)
def test_edit_spending_category(category, spends):
    spending_page.edit_category('Test category')
    spending_page.check_edit_should_be_successful()
