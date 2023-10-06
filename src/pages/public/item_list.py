import streamlit as st

from src import const
from src import session_manager
from src.models import item
from src.models.custom_pydantic import FrozenBaseModel
from src.services import item_api


class ItemListPage(FrozenBaseModel):
    page_id: const.PageId
    title: str
    ssm: session_manager.StreamlitSessionManager

    def render(self) -> None:
        item_api_client: item_api.IItemAPIClientService = self.ssm.get_item_api_client()

        st.title(self.title)

        col_size = (1, 2, 2, 2)
        columns = st.columns(col_size)
        headers = ("No", "名前", "価格", "")
        for col, field_name in zip(columns, headers, strict=True):
            col.text(field_name)

        for idx, item_info in enumerate(item_api_client.get_all()):
            (
                no_col,
                name_col,
                price_col,
                button_col
            ) = st.columns(col_size)
            no_col.text(idx + 1)
            name_col.text(item_info.name)
            price_col.text(item_info.price)
            button_col.button("詳細", key=item_info.item_id, on_click=self.__detail_on_click, args=(item_api,))

    def __detail_on_click(self, item_info: item.Item) -> None:
        self.ssm.set_item(item_info)
        self.ssm.set_page_id(const.PageId.PUBLIC_ITEM_DETAIL)
