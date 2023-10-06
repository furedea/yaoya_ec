import streamlit as st

import app
import init_app
import session_manager


if __name__ == "__main__":
    # Confirmation of initialization
    if not st.session_state.get("has_already_started", False):
        ssm: session_manager.StreamlitSessionManager = init_app.init_session()
        pages: list = init_app.init_pages(ssm)
        app_info: app.MultiPageApp = init_app.init_app(ssm, pages)
        st.session_state["has_already_started"] = True
        st.session_state["app"] = app_info
        st.set_page_config(page_title="八百屋さんEC", layout="wide")

    app_info = st.session_state.get("app", None)
    if app_info is not None:
        app_info.render()
