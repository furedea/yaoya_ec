"""Define User model."""
from datetime import date

from src import const
from src.models.custom_pydantic import FrozenBaseModel


class User(FrozenBaseModel):
    user_id: str
    name: str
    birthday: date
    email: str
    role: str
