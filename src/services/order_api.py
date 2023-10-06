import datetime
from typing import Final, Protocol
from uuid import uuid4

import dataset
import tinydb

from models.custom_pydantic import FrozenBaseModel
from models import cart
from models import order
from models import session
from services import mockdb


JST: Final = datetime.timezone(datetime.timedelta(hours=+9), "JST")


class IOrderAPIClientService(Protocol):
    def get_orders(self, session_id: str) -> list[order.Order]:
        ...

    def order_commit(self, session_id: str) -> None:
        pass


class MockOrderAPIClientService(FrozenBaseModel):
    mock_db: mockdb.MockDB
    session_db: mockdb.MockSessionDB

    def get_orders(self, session_id: str) -> list[order.Order]:
        """Get orders.

        Args:
            session_id (str): Session ID
        Returns:
            list[Order]: List of orders
        """
        session_info = self.__get_session(session_id)

        with self.mock_db.connect() as db:
            orders_table: dataset.Table = db["orders"]  # type: ignore
            orders_data = list(orders_table.find(user_id=session_info.user_id))
            orders = [order.Order.model_validate_json(order_data["order_body"]) for order_data in orders_data]
        return orders

    def __get_session(self, session_id: str) -> session.Session:
        """Get session.

        Args:
            session_id (str): Session ID
        Returns:
            Session: Session
        """
        with self.session_db.connect() as db:
            query = tinydb.Query()
            doc = db.search(query.session_id == session_id)[0]
            session_info = session.Session.model_validate(doc)

        return session_info

    def order_commit(self, session_id: str) -> None:
        """Commit the order.

        Args:
            session_id (str): Session ID
        """
        session_info = self.__get_session(session_id)

        order_info = self.__create_order_from_cart(session_info.cart)
        with self.mock_db.connect() as db:
            orders_table: dataset.Table = db["orders"]  # type: ignore
            order_data = dict(
                order_id=order_info.order_id, user_id=order_info.user_id, order_body=order_info.model_dump_json()
            )
            orders_table.insert(order_data)

    def __create_order_from_cart(self, cart_info: cart.Cart) -> order.Order:
        """Create order from cart.

        Args:
            cart_info (Cart): Cart
        Returns:
            Order: Order
        """
        order_details = []
        for idx, cart_item in enumerate(cart_info.cart_items):
            subtotal_price = cart_item.item.price * cart_item.quantity
            order_detail = order.OrderDetail(
                order_no=idx + 1, item=cart_item.item, quantity=cart_item.quantity, subtotal_price=subtotal_price
            )
            order_details.append(order_detail)
        order_info = order.Order(
            order_id=str(uuid4()),
            user_id=cart_info.user_id,
            total_price=cart_info.total_price,
            ordered_at=datetime.datetime.now(JST),
            details=order_details,
        )
        return order_info
