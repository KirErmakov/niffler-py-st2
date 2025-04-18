import pytest
import allure
from selene import browser
from allure_commons.types import AttachmentType

from models.config import Envs
from clients.auth_client import OAuthClient
from pages.login_page import login_page


@pytest.fixture(scope="session")
def auth_token(envs: Envs):
    return OAuthClient(envs).get_token(envs.test_username, envs.test_password)


@pytest.fixture(scope="session")
def auth(envs: Envs) -> str:
    username, password = envs.test_username, envs.test_password
    browser.open(envs.app_url)
    login_page.sign_in(username, password)
    token = browser.driver.execute_script('return window.localStorage.getItem("id_token")')
    allure.attach(token, name='token.txt', attachment_type=AttachmentType.TEXT)
    return token
