from urllib.parse import urljoin
import allure
import requests
from allure_commons.types import AttachmentType
from requests import Response
from requests_toolbelt.utils.dump import dump_response
from models.spend import Spend, SpendAdd


class SpendsHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
        self.session.hooks['response'].append(self.attach_response)

    @staticmethod
    @allure.step('Attach HTTP-response')
    def attach_response(response: Response, *args, **kwargs):
        attachment_name = response.request.method + " " + response.request.url
        allure.attach(dump_response(response), attachment_name, attachment_type=AttachmentType.TEXT)

    @allure.step('API: Get list of spends')
    def get_spends(self) -> list[Spend]:
        response = self.session.get(urljoin(self.base_url, '/api/spends/all'))
        self.raise_for_status(response)
        return [Spend.model_validate(item) for item in response.json()]

    @allure.step('API: Add spend')
    def add_spends(self, spend: SpendAdd) -> Spend:
        url = urljoin(self.base_url, "/api/spends/add")
        response = self.session.post(url, json=spend.model_dump())
        self.raise_for_status(response)
        return Spend.model_validate(response.json())

    @allure.step('API: Remove spend')
    def remove_spends(self, ids: list[str]):
        url = urljoin(self.base_url, "/api/spends/remove")
        response = self.session.delete(url, params={"ids": ids})
        self.raise_for_status(response)

    @staticmethod
    def raise_for_status(response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise
