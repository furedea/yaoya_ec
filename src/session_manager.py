"""Manage streamlit.session_state."""
import streamlit as st

import const
from models import item
from models import order
from models import user
from services import auth_api
from services import cart_api
from services import item_api
from services import user_api
from services import order_api


class StreamlitSessionManager:
    """Wrapper for streamlit.session_state. Manage only data that is explicitly retained."""

    def __init__(
        self,
        auth_api_client: auth_api.IAuthAPIClientService,
        user_api_client: user_api.IUserAPIClientService,
        item_api_client: item_api.IItemAPIClientService,
        order_api_client: order_api.IOrderAPIClientService,
        cart_api_client: cart_api.ICartAPIClientService,
    ) -> None:
        self.__session_state = st.session_state
        self.__session_state[const.SessionKey.AUTH_API_CLIENT.name] = auth_api_client
        self.__session_state[const.SessionKey.USER_API_CLIENT.name] = user_api_client
        self.__session_state[const.SessionKey.ITEM_API_CLIENT.name] = item_api_client
        self.__session_state[const.SessionKey.ORDER_API_CLIENT.name] = order_api_client
        self.__session_state[const.SessionKey.CART_API_CLIENT.name] = cart_api_client
        self.__session_state[const.SessionKey.USER.name] = None
        self.__session_state[const.SessionKey.ITEM.name] = None
        self.__session_state[const.SessionKey.ORDER.name] = None
        self.__session_state[const.SessionKey.PAGE_ID.name] = const.PageId.PUBLIC_LOGIN.name
        self.__session_state[const.SessionKey.SESSION_ID.name] = None
        self.__session_state[const.SessionKey.USERBOX.name] = None

    def get_user(self) -> user.User | None:
        return self.__session_state[const.SessionKey.USER.name]

    def get_item(self) -> item.Item | None:
        return self.__session_state[const.SessionKey.ITEM.name]

    def get_order(self) -> order.Order | None:
        return self.__session_state[const.SessionKey.ORDER.name]

    def get_session_id(self) -> str | None:
        return self.__session_state[const.SessionKey.SESSION_ID.name]

    def get_auth_api_client(self) -> auth_api.IAuthAPIClientService:
        return self.__session_state[const.SessionKey.AUTH_API_CLIENT.name]

    def get_user_api_client(self) -> user_api.IUserAPIClientService:
        return self.__session_state[const.SessionKey.USER_API_CLIENT.name]

    def get_item_api_client(self) -> item_api.IItemAPIClientService:
        return self.__session_state[const.SessionKey.ITEM_API_CLIENT.name]

    def get_order_api_client(self) -> order_api.IOrderAPIClientService:
        return self.__session_state[const.SessionKey.ORDER_API_CLIENT.name]

    def get_cart_api_client(self) -> cart_api.ICartAPIClientService:
        return self.__session_state[const.SessionKey.CART_API_CLIENT.name]

    def set_user(self, user_info: user.User) -> None:
        """Set user. Show username.

        Args:
            user_info (User): User
        """
        self.__session_state[const.SessionKey.USER.name] = user_info
        userbox = self.__session_state[const.SessionKey.USERBOX.name]
        userbox.text(f"ユーザ名: {user_info.name}")

    def set_item(self, item_info: item.Item) -> None:
        self.__session_state[const.SessionKey.ITEM.name] = item_info

    def set_order(self, order_info: order.Order) -> None:
        self.__session_state[const.SessionKey.ORDER.name] = order_info

    def set_page_id(self, page_id: const.PageId) -> None:
        self.__session_state[const.SessionKey.PAGE_ID.name] = page_id.name

    def set_session_id(self, session_id: str) -> None:
        self.__session_state[const.SessionKey.SESSION_ID.name] = session_id

    def show_userbox(self) -> None:
        """Show userbox."""
        userbox = self.__session_state[const.SessionKey.USERBOX.name]
        user_info: user.User | None = self.get_user()
        if userbox is None or user_info is None:
            self.__session_state[const.SessionKey.USERBOX.name] = st.sidebar.text("ログインしていません")
            return

        self.__session_state[const.SessionKey.USERBOX.name] = st.sidebar.text(f"ユーザ名: {user_info.name}")
