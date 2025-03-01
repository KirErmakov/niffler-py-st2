import os
from dotenv import load_dotenv
import pytest
from selene import browser
from clients.spends_client import SpendsHttpClient
from pages.login_page import login_page
from faker import Faker


@pytest.fixture(scope="session")
def envs():
    load_dotenv()


@pytest.fixture(scope='session')
def app_url(envs):
    return os.getenv("APP_URL")

@pytest.fixture(scope="session")
def gateway_url(envs):
    return os.getenv("GATEWAY_URL")


@pytest.fixture(scope="session")
def app_user(envs):
    return os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")

@pytest.fixture(scope="session")
def auth(app_url, app_user):
    username, password = app_user
    browser.open(app_url)
    login_page.sign_in(username, password)

    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')

@pytest.fixture(scope="session")
def spends_client(gateway_url, auth) -> SpendsHttpClient:
    return SpendsHttpClient(gateway_url, auth)


@pytest.fixture(params=[])
def category(request, spends_client):
    category_name = request.param
    current_categories = spends_client.get_categories()
    category_names = [category["name"] for category in current_categories]
    if category_name not in category_names:
        spends_client.add_category(category_name)
    return category_name


@pytest.fixture(params=[])
def spends(request, spends_client):
    spend = spends_client.add_spends(request.param)

    yield spend

    spends_client.remove_spends([spend["id"]])

@pytest.fixture()
def delete_spend(auth, spends_client):
    yield
    response = spends_client.get_spends()
    spends_client.remove_spends(response[0]["id"])


@pytest.fixture()
def main_page(auth, app_url):
    browser.open(app_url)


@pytest.fixture
def generate_test_user():
    fake = Faker()
    return fake.user_name()