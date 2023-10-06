"""Authentication service."""
from typing import Protocol

import dataset

from src.models.custom_pydantic import FrozenBaseModel
from src.models import cart
from src.models import exceptions
from src.models import session
from src.services import mockdb


class IAuthAPIClientService(Protocol):
    def login(self, user_id: str, password: str) -> str:
        ...


class MockAuthAPIClientService(FrozenBaseModel):
    """Mock API client service for authentication."""
    mock_db: mockdb.MockDB
    session_db: mockdb.MockSessionDB

    def login(self, user_id: str, password: str) -> str:
        """Login to Auth API client service.

        Args:
            user_id (str): User ID.
            password (str): Password.

        Returns:
            str: Session ID.

        Raises:
            AuthenticationError: Incorrect user ID or password.
        """
        if not self.__verify_user(user_id, password):
            raise exceptions.AuthenticationError("Incorrect user ID or password.")

        session_info = session.Session(user_id=user_id, cart=cart.Cart(user_id=user_id))
        with self.session_db.connect() as db:
            db.insert(session_info.model_dump())

        return session_info.session_id

    def __verify_user(self, user_id: str, password: str) -> bool:
        """Verify user ID and password.

        Args:
            user_id (str): User ID.
            password (str): Password.

        Returns:
            bool: True if user ID and password are correct.
        """
        with self.mock_db.connect() as db:
            table: dataset.Table = db["users"] # type: ignore
            user_data = table.find_one(user_id=user_id)

        return user_data is not None
