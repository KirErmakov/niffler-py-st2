import os
from urllib.parse import urljoin

from dotenv import load_dotenv
import pytest
from selene import browser

from clients.category_client import CategoryHttpClient
from clients.spends_client import SpendsHttpClient
from database.spend_db import SpendDb
from models.category import CategoryAdd
from pages.login_page import login_page
from models.config import Envs
from faker import Faker

from pages.spending_page import spending_page


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(
        app_url=os.getenv("APP_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD")
    )


@pytest.fixture(scope="session")
def auth(envs):
    username, password = envs.test_username, envs.test_password
    browser.open(envs.app_url)
    login_page.sign_in(username, password)

    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


@pytest.fixture(scope="session")
def spends_client(envs, auth) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, auth)


@pytest.fixture(scope='session')
def category_client(envs, auth) -> CategoryHttpClient:
    return CategoryHttpClient(envs.gateway_url, auth)


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture(params=[])
def category(request, category_client, spend_db):
    category_name = request.param
    category = category_client.add_category(CategoryAdd(name=category_name))
    yield category.name
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(request, spends_client):
    test_spend = spends_client.add_spends(request.param)

    yield test_spend

    all_spends = spends_client.get_spends()
    if test_spend.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([test_spend.id])


@pytest.fixture()
def delete_spend():
    yield
    spending_page.delete_spending()


@pytest.fixture()
def main_page(auth, envs):
    browser.open(envs.app_url)


@pytest.fixture()
def profile_page(envs, auth):
    profile_url = urljoin(envs.app_url, '/profile')
    browser.open(profile_url)


@pytest.fixture
def generate_test_user():
    fake = Faker()
    return fake.user_name()
