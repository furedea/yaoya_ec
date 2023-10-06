"""Defines the data model for an order."""""
from datetime import datetime
from src.models import item
from src.models.custom_pydantic import FrozenBaseModel


class OrderDetail(FrozenBaseModel):
    order_no: int
    item: item.Item
    quantity: int
    subtotal_price: int


class Order(FrozenBaseModel):
    order_id: str
    user_id: str
    total_price: int
    ordered_at: datetime
    details: list[OrderDetail]
