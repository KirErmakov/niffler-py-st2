import pytest
from pytest import FixtureRequest

from models.category import CategoryAdd
from pages.spending_page import spending_page


@pytest.fixture(params=[])
def category(request: FixtureRequest, category_client, spend_db):
    category_name = request.param
    category = category_client.add_category(CategoryAdd(name=category_name))
    yield category.name
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(request: FixtureRequest, spends_client):
    test_spend = spends_client.add_spends(request.param)
    yield test_spend

    all_spends = spends_client.get_spends()
    if test_spend.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([test_spend.id])


@pytest.fixture()
def delete_spend():
    yield
    spending_page.delete_spending()
