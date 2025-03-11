from faker.proxy import Faker
from marks import Pages, TestData
from pages.profile_page import profile

fake = Faker()
TEST_CATEGORY = fake.word()


@Pages.profile_page
def test_username_in_profile_is_correct(envs, auth):
    profile.check_username(envs.test_username)


@Pages.profile_page
def test_change_name_in_profile(auth):
    name = fake.name()

    profile.set_name(name)
    profile.check_name_is_correct(name)


@Pages.profile_page
@TestData.category(TEST_CATEGORY)
def test_category_exist(auth, category):
    profile.check_category_name(TEST_CATEGORY)


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


@Pages.profile_page
@TestData.category(TEST_CATEGORY)
def test_edit_category_name(envs, auth, category, spend_db):
    new_name = fake.word()

    profile.edit_category_name(new_name)
    categories = spend_db.get_user_categories(envs.test_username)
    category_names = [category.name for category in categories]

    assert new_name in category_names, f"Category '{new_name}' not found in DB"


@Pages.profile_page
@TestData.category(TEST_CATEGORY)
def test_archive_category(envs, auth, category, spend_db):
    profile.archive_category()

    categories = spend_db.get_user_categories(envs.test_username)
    archived_categories = [category.name for category in categories if category.archived is True]

    assert category in archived_categories, f'Category {category} is not archived'
