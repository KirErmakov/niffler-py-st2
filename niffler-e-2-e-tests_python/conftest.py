import os
import allure
from allure_commons.reporter import AllureReporter
from allure_commons.types import AttachmentType
from allure_pytest.listener import AllureListener
from pytest import Item, FixtureDef, FixtureRequest
from dotenv import load_dotenv
import pytest


from models.config import Envs
from faker import Faker


pytest_plugins = ['fixtures.auth_fixtures', 'fixtures.client_fixtures', 'fixtures.pages_fixtures']


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
        auth_url=os.getenv("AUTH_URL"),
        spend_db_url=os.getenv("SPEND_DB_URL"),
        test_username=os.getenv("TEST_USERNAME"),
        test_password=os.getenv("TEST_PASSWORD")
    )
    allure.attach(envs_instance.model_dump_json(indent=2), name='envs.json', attachment_type=AttachmentType.JSON)

    return envs_instance


@pytest.fixture
def generate_test_user():
    fake = Faker()
    return fake.user_name()
