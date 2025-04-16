from datetime import datetime

import pytest
import allure

from clients.spends_client import SpendsHttpClient
from database.spend_db import SpendDb
from fixtures.client_fixtures import spends_client
from marks import TestData
from models.category import CategoryAdd
from models.spend import SpendAdd, Spend
from models.enums import Category

pytestmark = [
    pytest.mark.allure_label('API', label_type='epic'),
    pytest.mark.allure_label("Spending", label_type="feature")
]


@allure.story('Create a spending')
def test_create_spending(spends_client: SpendsHttpClient, spend_db: SpendDb):
    spend_data = SpendAdd(
        amount=110.55,
        description="QA.GURU Python Advanced 2",
        category=CategoryAdd(name=Category.TEST_CATEGORY),
        spendDate=datetime.now().strftime("%Y-%m-%d"),
        currency="RUB"
    )
    created_spending = spends_client.add_spends(spend_data)

    assert created_spending.category.name == spend_data.category.name
    assert created_spending.description == spend_data.description
    assert created_spending.amount == spend_data.amount
    assert created_spending.currency == spend_data.currency

    spends_client.remove_spends(created_spending.id)
    spend_db.delete_category(created_spending.category.id)


@allure.story('Get spendings list')
@TestData.category(Category.TEST_CATEGORY)
@TestData.spends(
    SpendAdd(
        amount=110.55,
        description="QA.GURU Python Advanced 2",
        category=CategoryAdd(name=Category.TEST_CATEGORY),
        spendDate=datetime.now().strftime("%Y-%m-%d"),
        currency="RUB"
    )
)
def test_get_spendings(category, spends, spends_client: SpendsHttpClient):
    spends_list = spends_client.get_spends()

    for spending in spends_list:
        assert spending.id == spends.id
        assert spending.description == spends.description
        assert spending.amount == spends.amount


@allure.story('Create spending without description')
@TestData.category(Category.TEST_CATEGORY)
def test_create_spending_without_description(category, spends_client: SpendsHttpClient, spend_db: SpendDb):
    spend_data = SpendAdd(
        amount=110.55,
        description='',
        category=CategoryAdd(name=Category.TEST_CATEGORY),
        spendDate=datetime.now().strftime("%Y-%m-%d"),
        currency="RUB"
    )
    created_spending = spends_client.add_spends(spend_data)

    assert created_spending.category.name == spend_data.category.name
    assert created_spending.description == ''

    spends_client.remove_spends(created_spending.id)


@allure.story('Change spending currency')
@TestData.category(Category.TEST_CATEGORY)
@TestData.spends(
    SpendAdd(
        amount=110.55,
        description="QA.GURU Python Advanced 2",
        category=CategoryAdd(name=Category.TEST_CATEGORY),
        spendDate=datetime.now().strftime("%Y-%m-%d"),
        currency="RUB"
    )
)
@pytest.mark.parametrize('currency', ['USD', 'EUR', 'KZT'])
def test_edit_spending_currency(category, spends, currency, spends_client: SpendsHttpClient):
    updated_data = Spend(
        id=spends.id,
        amount=spends.amount,
        description=spends.description,
        category=spends.category,
        spendDate=spends.spendDate,
        currency=currency,
        username=spends.username
    )

    updated_spending = spends_client.update_spends(updated_data)

    assert updated_spending.currency == currency


@allure.story('Delete spending')
def test_delete_spending(spends_client: SpendsHttpClient, spend_db: SpendDb):
    spend_data = SpendAdd(
        amount=110.55,
        description="QA.GURU Python Advanced 2",
        category=CategoryAdd(name=Category.TEST_CATEGORY),
        spendDate=datetime.now().strftime("%Y-%m-%d"),
        currency="RUB"
    )
    created_spending = spends_client.add_spends(spend_data)

    spends_client.remove_spends(created_spending.id)
    spends_list = spends_client.get_spends()

    assert not spends_list
    spend_db.delete_category(created_spending.category.id)


@TestData.category(Category.TEST_CATEGORY)
@TestData.spends(
    SpendAdd(
        amount=110.55,
        description="QA.GURU Python Advanced 2",
        category=CategoryAdd(name=Category.TEST_CATEGORY),
        spendDate=datetime.now().strftime("%Y-%m-%d"),
        currency="RUB"
    )
)
@allure.story('Change description')
def test_edit_spending_description(category, spends, spends_client: SpendsHttpClient):
    updated_data = Spend(
        id=spends.id,
        amount=spends.amount,
        description="New description",
        category=spends.category,
        spendDate=spends.spendDate,
        currency=spends.currency,
        username=spends.username
    )

    updated_spending = spends_client.update_spends(updated_data)

    assert updated_spending.description == updated_data.description
