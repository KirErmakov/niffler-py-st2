import os
from dotenv import load_dotenv
import pytest
from selene import browser
from faker import Faker


load_dotenv()


@pytest.fixture
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture(scope='function', autouse=True)
def setup_browser(app_url):
    browser.config.base_url = app_url
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    browser.open('/')
    yield
    browser.quit()


@pytest.fixture
def generate_test_user():
    fake = Faker()
    return fake.user_name()