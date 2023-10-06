from collections import namedtuple

import streamlit as st

import const
import session_manager
from models import order
from models import page
from models.custom_pydantic import FrozenBaseModel


class OrderDetailPage(FrozenBaseModel):
    page_id: const.PageId
    title: str
    ssm: session_manager.StreamlitSessionManager

    def render(self) -> None:
        """Render the page."""
        if not page.validate_user(self.ssm):
            return

        order_info: order.Order | None = self.ssm.get_order()

        st.title(self.title)

        if order_info is None:
            st.warning("商品が選択されていません")
            return

        self.__render_order(order_info)
        self.__render_order_detail(order_info)

    def __render_order(self, order_info: order.Order) -> None:
        """Render the order.

        Args:
            order_info (model.Order): Order
        """
        OrderTuple = namedtuple("OrderTuple", ["注文ID", "合計金額", "注文日付"])
        show_order = OrderTuple(
            order_info.order_id, order_info.total_price, order_info.ordered_at.strftime("%Y-%m-%d %H:%M:%S")
        )

        st.subheader("注文情報")

        col_size = (1, 2)
        for key, value in show_order._asdict().items():
            key_col, value_col = st.columns(col_size)
            key_col.text(key)
            value_col.text(value)

    def __render_order_detail(self, order_info: order.Order) -> None:
        st.subheader("注文詳細一覧")

        col_size = (1, 2, 2, 2)
        columns = st.columns(col_size)
        headers = ("No", "商品名", "単価", "数量")
        for col, field_name in zip(columns, headers):
            col.text(field_name)

        for order_detail in order_info.details:
            (no_col, name_col, price_col, q_col) = st.columns(col_size)
            no_col.text(order_detail.order_no)
            name_col.text(order_detail.item.name)
            price_col.text(order_detail.item.price)
            q_col.text(order_detail.quantity)
