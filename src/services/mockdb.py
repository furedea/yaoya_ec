"""Mock DB for streamlit_YaEC."""
from contextlib import contextmanager
from datetime import date
from pathlib import Path
from pydantic import PrivateAttr
from random import randint
from typing import Iterator

import dataset
import mimesis
import tinydb

from models.custom_pydantic import FrozenBaseModel
import const
from models import item
from models import user


class MockDB(FrozenBaseModel):
    """Wrapper for dataset."""

    dbpath: Path
    _dbname: str = PrivateAttr()

    def model_post_init(self, __context) -> None:
        """Post init hook for pydantic."""
        self._dbname = f"sqlite:///{self.dbpath}"
        self.__create_mock_db()

    def __create_mock_db(self) -> None:
        """Create mock DB. (Add if you want to pre-fill the table with data.)"""
        self.__create_mock_user_table()
        self.__create_mock_item_table()

    def __create_mock_user_table(self) -> None:
        """Create mock user table."""
        mock_users = frozenset(
            (
                user.User(
                    user_id="member",
                    name="会員",
                    birthday=date(2000, 1, 1),
                    email="guest@example.com",
                    role=const.UserRole.MEMBER.name,
                ),
                user.User(
                    user_id="admin",
                    name="管理者",
                    birthday=date(2000, 1, 1),
                    email="admin@example.com",
                    role=const.UserRole.ADMIN.name,
                ),
            )
        )
        with self.connect() as db:
            table: dataset.Table = db["users"]  # type: ignore
            for mock_user in mock_users:
                table.insert(mock_user.model_dump())

    def __create_mock_item_table(self, n: int = 10) -> None:
        """Create mock item table.

        Args:
            n (int, optional): Number of items.
        """
        _ = mimesis.Field(locale=mimesis.Locale.JA)
        schema = mimesis.Schema(
            schema=lambda: {
                "item_id": _("uuid"),
                "name": _("vegetable"),
                "price": randint(1, 5) * 100 - 2,
                "producing_area": _("prefecture"),
            },
            iterations=n,
        )
        mock_items = [item.Item.model_validate(data) for data in schema.create()]
        with self.connect() as db:
            table: dataset.Table = db["items"]  # type: ignore
            for mock_item in mock_items:
                table.insert(mock_item.model_dump())

    @contextmanager
    def connect(self) -> Iterator[dataset.Database]:
        """Decorator for connecting to DB. If wrong, rollback.

        Yields:
            Iterator[dataset.Database]: DB connection.
        """
        db: dataset.Database = dataset.connect(self._dbname)
        db.begin()
        try:
            yield db
            db.commit()
        except:
            db.rollback()
            raise


class MockSessionDB(FrozenBaseModel):
    """Wrapper for TinyDB."""

    dbpath: Path
    _db: tinydb.TinyDB = PrivateAttr()

    def model_post_init(self, __context) -> None:
        """Post init hook for pydantic."""
        self._db = tinydb.TinyDB(self.dbpath)

    @contextmanager
    def connect(self) -> Iterator[tinydb.TinyDB]:
        """Decorator for connecting to DB."""
        try:
            yield self._db
        except:
            raise
