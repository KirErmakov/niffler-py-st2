from typing import Sequence

import allure
from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select

from models.config import Envs
from models.spend import Category
from utils.allure_helpers import attach_sql


class SpendDb:
    engine: Engine

    def __init__(self, envs: Envs):
        self.engine = create_engine(envs.spend_db_url)
        event.listen(self.engine, "do_execute", fn=attach_sql)

    @allure.step('DB: Get user categories')
    def get_user_categories(self, username: str) -> Sequence[Category]:
        with Session(self.engine) as session:
            statement = select(Category).where(Category.username == username)
            return session.exec(statement).all()

    @allure.step('DB: Delete a category')
    def delete_category(self, category_id: str):
        with Session(self.engine) as session:
            category = session.get(Category, category_id)
            session.delete(category)
            session.commit()
