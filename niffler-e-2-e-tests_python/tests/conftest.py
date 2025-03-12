import os
from urllib.parse import urljoin
import allure
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from allure_pytest.listener import AllureListener
from pytest import Item, FixtureDef, FixtureRequest
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


def allure_logger(config) -> AllureReporter:
    listener: AllureListener = config.pluginmanager.get_plugin('allure_listener')
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_call(item: Item):
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).title())


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f'[{scope_letter}] ' + " ".join(fixturedef.argname.split('_')).title()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_teardown(item):
    yield
    logger = allure_logger(item.config)
    test_result = logger.get_test(None)

    if test_result:
        test_result.labels = [
            label for label in test_result.labels
            if label.name != 'tag'
        ]


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    envs_instance = Envs(
        app_url=os.getenv("APP_URL"),
        gateway_url=os.getenv("GATEWAY_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD")
    )
    allure.attach(envs_instance.model_dump_json(indent=2), name='envs.json', attachment_type=AttachmentType.JSON)

    return envs_instance


@pytest.fixture(scope="session")
def auth(envs) -> str:
    username, password = envs.test_username, envs.test_password
    browser.open(envs.app_url)
    login_page.sign_in(username, password)
    token = browser.driver.execute_script('return window.localStorage.getItem("id_token")')
    allure.attach(token, name='token.txt', attachment_type=AttachmentType.TEXT)
    return token


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
