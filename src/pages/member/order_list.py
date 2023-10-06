import streamlit as st

import const
import session_manager
from models import exceptions
from models import order
from models import page
from models.custom_pydantic import FrozenBaseModel
from services import order_api


class OrderListPage(FrozenBaseModel):
    page_id: const.PageId
    title: str
    ssm: session_manager.StreamlitSessionManager

    def render(self) -> None:
        """Render the page."""
        session_id: str | None = self.ssm.get_session_id()
        if not page.validate_user(self.ssm) or (session_id is None):
            return

        order_api_client: order_api.IOrderAPIClientService = self.ssm.get_order_api_client()

        st.title(self.title)

        col_size = (1, 2, 2, 4, 2)
        columns = st.columns(col_size)
        headers = ("No", "注文ID", "合計金額", "注文日付", "")
        for col, field_name in zip(columns, headers):
            col.text(field_name)

        try:
            orders: list[order.Order] = order_api_client.get_orders(session_id=session_id)
        except exceptions.NotFoundError:
            st.warning("注文履歴はありません。")
            return

        for idx, order_info in enumerate(orders):
            (col_no, col_id, col_total, col_date, col_button) = st.columns(col_size)
            col_no.text(idx + 1)
            col_id.text(order_info.order_id[-8:])
            col_total.text(order_info.total_price)
            col_date.text(order_info.ordered_at.strftime("%Y-%m-%d %H:%M:%S"))
            col_button.button("詳細", key=order_info.order_id, on_click=self.__order_detail, args=(order_api,))

    def __order_detail(self, order_info: order.Order) -> None:
        self.ssm.set_order(order_info)
        self.ssm.set_page_id(const.PageId.MEMBER_ORDER_DETAIL)
