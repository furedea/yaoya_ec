"""Login Page Module."""
import streamlit as st

from src import const
from src import session_manager
from src.models import exceptions
from src.models import user
from src.models.custom_pydantic import FrozenBaseModel
from src.services import auth_api
from src.services import user_api


class LoginPage(FrozenBaseModel):
    page_id: const.PageId
    title: str
    ssm: session_manager.StreamlitSessionManager

    def render(self) -> None:
        auth_api_clint: auth_api.IAuthAPIClientService = self.ssm.get_auth_api_client()
        user_api_client: user_api.IUserAPIClientService = self.ssm.get_user_api_client()

        st.title(self.title)
        with st.form("form"):
            user_id: str = st.text_input("ユーザーID")
            password: str = st.text_input("パスワード", type="password")
            submit_button: bool = st.form_submit_button("ログイン")

        if submit_button:
            try:
                session_id: str = auth_api_clint.login(user_id, password)
                user_info: user.User = user_api_client.get_by_session_id(session_id)
            except exceptions.AuthenticationError:
                st.sidebar.error("ユーザーID または パスワードが間違っています。")
                return

            st.sidebar.success("ログインに成功しました。")
            self.ssm.set_user(user_info)
            self.ssm.set_session_id(session_id)
