import allure
import pytest
from faker.proxy import Faker
from marks import Pages, TestData
from pages.profile_page import profile


pytestmark = [
    pytest.mark.allure_label("Profile", label_type="epic"),
    pytest.mark.allure_label('Profile actions', label_type="feature")
    ]


fake = Faker()
TEST_CATEGORY = fake.word()


@allure.story('Profile username is correct')
@Pages.profile_page
def test_username_in_profile_is_correct(envs, auth):
    profile.check_username_is_correct(envs.test_username)


@allure.story('Change name')
@Pages.profile_page
def test_change_name_in_profile(auth):
    name = fake.name()

    profile.set_name(name)
    profile.check_name_is_correct(name)


@allure.story('Created category exists')
@Pages.profile_page
@TestData.category(TEST_CATEGORY)
def test_category_exist(auth, category):
    profile.check_category_name(TEST_CATEGORY)


@allure.story('Create a category')
@Pages.profile_page
def test_create_category(envs, auth, spend_db):
    new_category = TEST_CATEGORY

    profile.create_category(new_category)
    # Проверяем наличие созданной категории в БД
    categories = spend_db.get_user_categories(envs.test_username)
    category_names = [category.name for category in categories]

    assert new_category in category_names, f"Category '{new_category}' not found in DB"

    # Удаляем запись из БД (не использую фикстуру, так как в тесте проверяется создание категории через UI)
    for category in categories:
        if category.name == new_category:
            spend_db.delete_category(category.id)
            break


@allure.story('Edit category')
@Pages.profile_page
@TestData.category(TEST_CATEGORY)
def test_edit_category_name(envs, auth, category, spend_db):
    new_name = fake.word()

    profile.edit_category_name(new_name)
    categories = spend_db.get_user_categories(envs.test_username)
    category_names = [category.name for category in categories]

    assert new_name in category_names, f"Category '{new_name}' not found in DB"


@allure.story('Acrhive category')
@Pages.profile_page
@TestData.category(TEST_CATEGORY)
def test_archive_category(envs, auth, category, spend_db):
    profile.archive_category()

    categories = spend_db.get_user_categories(envs.test_username)
    archived_categories = [category.name for category in categories if category.archived is True]

    assert category in archived_categories, f'Category {category} is not archived'
