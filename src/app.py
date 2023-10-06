"""Module to manage multiple page apps."""
from pydantic import PrivateAttr
import streamlit as st

import session_manager
import const
from models import page
from models.custom_pydantic import FrozenBaseModel


class MultiPageApp(FrozenBaseModel):
    """Class to manage multiple page apps."""

    ssm: session_manager.StreamlitSessionManager
    page_list: list[page.Page]
    nav_label: str = "ページ一覧"
    _pages: dict[const.PageId, page.Page] = PrivateAttr()

    def model_post_init(self, __context) -> None:
        """Post init."""
        self._pages = {page_info.page_id: page_info for page_info in self.page_list}

    def render(self) -> None:
        """Render the page in the app."""
        page_id: const.PageId | None = st.sidebar.selectbox(
            self.nav_label,
            list(self._pages.keys()),
            format_func=lambda page_id: self._pages[page_id].title,
        )
        if page_id is None:
            st.error("ページが選択されていません")
            return

        self.ssm.set_page_id(page_id)
        self.ssm.show_userbox()
        self._pages[page_id].render()
