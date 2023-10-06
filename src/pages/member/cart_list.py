import streamlit as st

from src import const
from src import session_manager
from src.models import cart
from src.models import page
from src.models.custom_pydantic import FrozenBaseModel
from src.services import cart_api
from src.services import order_api


class CartPage(FrozenBaseModel):
    """Cart page."""
    page_id: const.PageId
    title: str
    ssm: session_manager.StreamlitSessionManager

    def render(self) -> None:
        """Render the page."""
        session_id: str | None = self.ssm.get_session_id()
        if not page.validate_user(self.ssm) or (session_id is None):
            return

        cart_api_client: cart_api.ICartAPIClientService = self.ssm.get_cart_api_client()
        cart_info: cart.Cart = cart_api_client.get_cart(session_id=session_id)

        if len(cart_info.cart_items) == 0:
            st.warning("カートに商品がありません。")
            return

        st.title(self.title)

        col_size = (1, 2, 2, 2)
        columns = st.columns(col_size)
        headers = ("No", "商品名", "単価", "数量")
        for col, field_name in zip(columns, headers):
            col.write(field_name)

        for idx, cart_item in enumerate(cart_info.cart_items):
            (
                no_col,
                name_col,
                price_col,
                q_col
            ) = st.columns(col_size)
            no_col.text(idx + 1)
            name_col.text(cart_item.item.name)
            price_col.text(cart_item.item.price)
            q_col.text(cart_item.quantity)

        st.text(f"合計金額: {cart_info.total_price}")
        st.button("注文", on_click=self.__order_commit)

    def __order_commit(self) -> None:
        """Commit the order."""
        session_id: str | None = self.ssm.get_session_id()
        order_api_client: order_api.IOrderAPIClientService = self.ssm.get_order_api_client()
        cart_api_client: cart_api.ICartAPIClientService = self.ssm.get_cart_api_client()

        if session_id is None:
            st.sidebar.error("注文する商品がありません。")
            return

        order_api_client.order_commit(session_id=session_id)
        cart_api_client.clear_cart(session_id=session_id)
        st.sidebar.success("注文が完了しました。")
