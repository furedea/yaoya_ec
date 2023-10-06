"""Define Session model."""
from uuid import uuid4

from src.models import cart
from src.models.custom_pydantic import FrozenBaseModel


class Session(FrozenBaseModel):
    user_id: str
    cart: cart.Cart
    session_id: str = str(uuid4())
