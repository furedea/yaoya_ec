"""Item service."""
from typing import Protocol

import dataset

from models.custom_pydantic import FrozenBaseModel
from models import item
from services import mockdb


class IItemAPIClientService(Protocol):
    def get_all(self) -> list[item.Item]:
        ...


class MockItemAPIClientService(FrozenBaseModel):
    """Mock API client service for item."""

    mock_db: mockdb.MockDB

    def get_all(self) -> list[item.Item]:
        """Get all items.

        Returns:
            list[model.Item]: List of items.
        """
        with self.mock_db.connect() as db:
            table: dataset.Table = db["items"]  # type: ignore
            items_data = table.all()

        return [item.Item.model_validate(item_data) for item_data in items_data]
