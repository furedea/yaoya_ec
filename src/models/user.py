"""Define User model."""
from datetime import date

import const
from models.custom_pydantic import FrozenBaseModel


class User(FrozenBaseModel):
    user_id: str
    name: str
    birthday: date
    email: str
    role: str
