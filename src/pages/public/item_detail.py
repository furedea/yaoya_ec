from collections import namedtuple

import streamlit as st

import const
import session_manager
from models import cart
from models import item
from models import user
from models.custom_pydantic import FrozenBaseModel
from services import cart_api


class ItemDetailPage(FrozenBaseModel):
    page_id: const.PageId
    title: str
    ssm: session_manager.StreamlitSessionManager

    def render(self) -> None:
        """Render the page."""
        st.title(self.title)

        item_info: item.Item | None = self.ssm.get_item()
        if item_info is None:
            st.error("商品が選択されていません")
            return

        self.__render_item_detail(item_info)

        user_info: user.User | None = self.ssm.get_user()
        session_id: str | None = self.ssm.get_session_id()
        if user_info is None or session_id is None:
            st.info("カートに追加するためにはログインが必要です。")
            return

        self.__render_cart_in(item_info, session_id)

    def __render_item_detail(self, item_info: item.Item) -> None:
        """Render the item detail.

        Args:
            item_info (model.Item): The item to render.
        """
        ItemTuple = namedtuple("ItemTuple", ["商品名", "価格", "生産地"])
        show_item = ItemTuple(item_info.name, item_info.price, item_info.producing_area)

        col_size = (1, 2)
        for key, value in show_item._asdict().items():
            key_col, value_col = st.columns(col_size)
            key_col.text(key)
            value_col.text(value)

    def __render_cart_in(self, item_info: item.Item, session_id: str) -> None:
        """Render the cart in button.

        Args:
            item_info (model.Item): The item to add to the cart.
            session_id (str): The session ID.
        """
        with st.form("item_detail_form"):
            st.number_input("数量", step=1, min_value=1, max_value=9, key="_quantity")
            st.form_submit_button(
                label="カートに追加", on_click=self.__cart_in, kwargs=dict(item=item_info, session_id=session_id)
            )

    def __cart_in(self, item_info: item.Item, session_id: str) -> None:
        """Add the item to the cart.

        Args:
            item_info (model.Item): The item to add to the cart.
            session_id (str): The session ID.
        """
        cart_api_client: cart_api.ICartAPIClientService = self.ssm.get_cart_api_client()
        cart_item = cart.CartItem(item=item_info, quantity=st.session_state["_quantity"])
        cart_api_client.add_item(session_id, cart_item)
        st.sidebar.success("カートに追加しました")
        st.session_state["_quantity"] = 1
