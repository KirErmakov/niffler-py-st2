import pytest

from clients.category_client import CategoryHttpClient
from clients.spends_client import SpendsHttpClient
from database.spend_db import SpendDb
from models.config import Envs


@pytest.fixture(scope="session")
def spends_client(envs: Envs, auth_token: str) -> SpendsHttpClient:
    return SpendsHttpClient(envs, auth_token)


@pytest.fixture(scope="session")
def spend_db(envs: Envs) -> SpendDb:
    return SpendDb(envs)


@pytest.fixture(scope='session')
def category_client(envs: Envs, auth_token: str) -> CategoryHttpClient:
    return CategoryHttpClient(envs, auth_token)
