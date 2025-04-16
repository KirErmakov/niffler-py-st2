from dataclasses import dataclass
from faker import Faker

fake = Faker()


@dataclass
class Category:
    TEST_CATEGORY = fake.word()
