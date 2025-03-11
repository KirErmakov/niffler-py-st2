from datetime import datetime
from pydantic import BaseModel

from models.category import CategoryAdd, Category
from sqlmodel import Field


class Spend(BaseModel):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: Category
    spendDate: datetime
    currency: str
    username: str


class SpendAdd(BaseModel):
    amount: float
    description: str
    category: CategoryAdd
    spendDate: str
    currency: str
