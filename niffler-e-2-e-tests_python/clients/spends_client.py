import allure
import requests

from models.config import Envs
from models.spend import Spend, SpendAdd
from utils.sessions import BaseSession


class SpendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs, token: str):
        self.session = BaseSession(base_url=envs.gateway_url)
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    @allure.step('API: Get list of spends')
    def get_spends(self) -> list[Spend]:
        response = self.session.get('/api/spends/all')
        return [Spend.model_validate(item) for item in response.json()]

    @allure.step('API: Add spend')
    def add_spends(self, spend: SpendAdd) -> Spend:
        response = self.session.post('/api/spends/add', json=spend.model_dump())
        return Spend.model_validate(response.json())

    @allure.step('API: Update spend')
    def update_spends(self, update_info: Spend):
        response = self.session.patch('/api/spends/edit', json=update_info.model_dump())
        return Spend.model_validate(response.json())

    @allure.step('API: Remove spend')
    def remove_spends(self, ids: list[str]):
        self.session.delete('/api/spends/remove', params={"ids": ids})
