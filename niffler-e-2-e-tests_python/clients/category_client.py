import allure

import requests

from models.category import CategoryAdd
from models.config import Envs
from models.spend import Category
from utils.sessions import BaseSession


class CategoryHttpClient:
    session: requests.Session
    base_url: str

    def __init__(self, envs: Envs, token: str):
        self.session = BaseSession(base_url=envs.gateway_url)
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    @allure.step('API: Get list of categories')
    def get_categories(self) -> list[Category]:
        response = self.session.get("/api/categories/all")

        return [Category.model_validate(item) for item in response.json()]

    @allure.step('API: Add category')
    def add_category(self, category: CategoryAdd):
        response = self.session.post("/api/categories/add", json=category.model_dump())

        return Category.model_validate(response.json())
