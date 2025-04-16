import pytest
from selene import browser

from urllib.parse import urljoin


@pytest.fixture()
def main_page(auth_token, envs):
    browser.open(envs.app_url)


@pytest.fixture()
def profile_page(envs, auth):
    profile_url = urljoin(envs.app_url, '/profile')
    browser.open(profile_url)
