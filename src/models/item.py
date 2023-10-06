"""Define Item model."""
from src.models.custom_pydantic import FrozenBaseModel


class Item(FrozenBaseModel):
    item_id: str
    name: str
    price: int
    producing_area: str
