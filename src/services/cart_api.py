from typing import Callable, Protocol

import tinydb

from src.models.custom_pydantic import FrozenBaseModel
from src.models import cart
from src.models import session

from src.services import mockdb


class ICartAPIClientService(Protocol):
    def get_cart(self, session_id: str) -> cart.Cart:
        ...

    def add_item(self, session_id: str, cart_item: cart.CartItem) -> None:
        pass

    def clear_cart(self, session_id: str) -> None:
        pass


class MockCartAPIClientService(FrozenBaseModel):
    session_db: mockdb.MockSessionDB

    def get_cart(self, session_id: str) -> cart.Cart:
        """Get the cart.

        Args:
            session_id (str): The session ID.
        Returns:
            model.Cart: The cart.
        """
        with self.session_db.connect() as db:
            query = tinydb.Query()
            session_dict = db.search(query.session_id == session_id)[0]
            session_info = session.Session.model_validate(session_dict)
        return session_info.cart

    def add_item(self, session_id: str, cart_item: cart.CartItem) -> None:
        """Add the item to the cart.

        Args:
            session_id (str): The session ID.
            cart_item (model.CartItem): The cart item.
        """
        with self.session_db.connect() as db:
            query = tinydb.Query()
            db.update(self.__get_add_item_cb(cart_item), query.session_id == session_id) # type: ignore

    def __get_add_item_cb(self, cart_item: cart.CartItem) -> Callable[[dict], None]:
        """Get the callback function to add the item to the cart.

        Args:
            cart_item (model.CartItem): The cart item.

        Returns:
            Callable[[dict], None]: The callback function.
        """
        def transform(doc: dict) -> None:
            """Transform the document."""
            session_info = session.Session.model_validate(doc)
            cart_info: cart.Cart = session_info.cart
            new_cart_items: list[cart.CartItem] = [*cart_info.cart_items, cart_item]
            new_total_price = cart_item.item.price * cart_item.quantity + cart_info.total_price
            new_cart = cart.Cart(
                user_id=cart_info.user_id,
                cart_items=new_cart_items,
                total_price=new_total_price
            )
            new_session = session.Session(
                user_id=session_info.user_id,
                cart=new_cart,
                session_id=session_info.session_id
            )
            for key, value in new_session.model_dump().items():
                doc[key] = value
        return transform

    def clear_cart(self, session_id: str) -> None:
        """Clear the cart.

        Args:
            session_id (str): The session ID.
        """
        with self.session_db.connect() as db:
            query = tinydb.Query()
            db.update(self.__get_clear_cart_cb(), query.session_id == session_id) # type: ignore

    def __get_clear_cart_cb(self) -> Callable[[dict], None]:
        """Get the callback function to clear the cart.

        Returns:
            Callable[[dict], None]: The callback function.
        """
        def transform(doc: dict) -> None:
            """Transform the document."""
            session_info = session.Session.model_validate(doc)
            new_session = session.Session(
                user_id=session_info.user_id,
                cart=cart.Cart(user_id=session_info.user_id),
                session_id=session_info.session_id
            )
            for key, value in new_session.model_dump().items():
                doc[key] = value
        return transform
