"""Defines the Cart and CartItem models."""
from models import item
from models.custom_pydantic import FrozenBaseModel


class CartItem(FrozenBaseModel):
    item: item.Item
    quantity: int = 0


class Cart(FrozenBaseModel):
    user_id: str
    cart_items: list[CartItem] = []
    total_price: int = 0
