import pytest

from pages.spending_page import spending_page
from marks import Pages, TestData


@Pages.main_page
def test_spending_title_exists():
    spending_page.check_spending_page_titles()

@pytest.mark.skip
def test_create_spending(auth):
    spending_page.new_spending.click()
    spending_page.create_spending(100, 'RUB', 'test')

    spending_page.check_spending_exists('test', 100)


TEST_CATEGORY = "school"


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends({
    "amount": "110.55",
    "description": "QA.GURU Python Advanced 2",
    "category": {
        "name": TEST_CATEGORY
    },
    "spendDate": "2025-02-28T18:39:27.955Z",
    "currency": "RUB"
})
def test_delete_spending_via_table_actions(category, spends):
    spending_page.check_spending_exists(TEST_CATEGORY, '110.55')
    spending_page.delete_spending()


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends({
    "amount": "110.55",
    "description": "QA.GURU Python Advanced 2",
    "category": {
        "name": TEST_CATEGORY
    },
    "spendDate": "2025-02-28T18:39:27.955Z",
    "currency": "RUB"
})
def test_edit_spending_currency(category, spends):
    spending_page.edit_spending_currency('USD')
    spending_page.check_edit_should_be_successful()



@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends({
    "amount": "108.51",
    "description": "QA.GURU Python Advanced 2",
    "category": {
        "name": TEST_CATEGORY
    },
    "spendDate": "2025-02-28T18:39:27.955Z",
    "currency": "RUB"
})
def test_edit_spending_description(category, spends):
    spending_page.edit_spending_description('New test')
    spending_page.check_edit_should_be_successful()

