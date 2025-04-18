import pytest
import allure
from clients.category_client import CategoryHttpClient
from database.spend_db import SpendDb
from marks import TestData
from models.category import CategoryAdd
from models.enums import Category


pytestmark = [
    pytest.mark.allure_label('API', label_type='epic'),
    pytest.mark.allure_label("Category", label_type="feature")
]


@allure.story('Create a category')
def test_create_category(category_client: CategoryHttpClient, spend_db: SpendDb):
    category_name = Category.TEST_CATEGORY
    new_category = category_client.add_category((CategoryAdd(name=category_name)))
    assert new_category.name == category_name
    assert new_category.id is not None

    spend_db.delete_category(new_category.id)


@allure.story('Get categories list')
@TestData.category(Category.TEST_CATEGORY)
def test_get_categories(category, category_client: CategoryHttpClient, spend_db: SpendDb):

    categories = category_client.get_categories()

    assert len(categories), "The categories list is empty"
    for cat in categories:
        assert cat.id is not None
        assert cat.name == Category.TEST_CATEGORY

