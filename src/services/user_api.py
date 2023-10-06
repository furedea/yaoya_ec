"""User service."""
from typing import Protocol

import dataset
import tinydb

from models.custom_pydantic import FrozenBaseModel
from models import exceptions
from models import user
from services import mockdb


class IUserAPIClientService(Protocol):
    def get_by_user_id(self, user_id: str) -> user.User:
        ...

    def get_by_session_id(self, session_id: str) -> user.User:
        ...


class MockUserAPIClientService(FrozenBaseModel):
    """Mock API client service for user."""

    mock_db: mockdb.MockDB
    session_db: mockdb.MockSessionDB

    def get_by_user_id(self, user_id: str) -> user.User:
        """Get user by user ID.

        Args:
            user_id (str): User ID.

        Returns:
            User: User.
        """
        with self.mock_db.connect() as db:
            table: dataset.Table = db["users"]  # type: ignore
            user_data = table.find_one(user_id=user_id)

        if user_data is None:
            raise exceptions.NotFoundError(user_id)

        return user.User.model_validate(user_data)

    def get_by_session_id(self, session_id: str) -> user.User:
        """Get user by session ID.

        Args:
            session_id (str): Session ID.

        Returns:
            User: User.
        """
        user_id: str = self.__get_user_id(session_id)
        user_info: user.User = self.get_by_user_id(user_id)
        return user_info

    def __get_user_id(self, session_id: str) -> str:
        """Get user ID by session ID.

        Args:
            session_id (str): Session ID.

        Returns:
            str: User ID.
        """
        with self.session_db.connect() as db:
            query = tinydb.Query()
            doc = db.search(query.session_id == session_id)

        return doc[0]["user_id"]
