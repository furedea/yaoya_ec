"""Initialize app."""
from pathlib import Path
from tempfile import TemporaryDirectory

import app
import session_manager
import const
from models import page
from pages.member import cart_list
from pages.member import order_list
from pages.member import order_detail
from pages.public import login
from pages.public import item_detail
from pages.public import item_list
from services import auth_api
from services import cart_api
from services import item_api
from services import mockdb
from services import order_api
from services import user_api


def init_session() -> session_manager.StreamlitSessionManager:
    """Initialize session."""
    mockdir = Path(TemporaryDirectory().name)
    mockdir.mkdir(exist_ok=True)
    mock_db = mockdb.MockDB(dbpath=mockdir.joinpath("mock.db"))
    session_db = mockdb.MockSessionDB(dbpath=mockdir.joinpath("session.json"))
    ssm = session_manager.StreamlitSessionManager(
        auth_api_client=auth_api.MockAuthAPIClientService(mock_db=mock_db, session_db=session_db),
        user_api_client=user_api.MockUserAPIClientService(mock_db=mock_db, session_db=session_db),
        item_api_client=item_api.MockItemAPIClientService(mock_db=mock_db),
        order_api_client=order_api.MockOrderAPIClientService(mock_db=mock_db, session_db=session_db),
        cart_api_client=cart_api.MockCartAPIClientService(session_db=session_db),
    )
    return ssm


def init_pages(ssm: session_manager.StreamlitSessionManager) -> list[page.Page]:
    """Initialize pages.

    Args:
        ssm (StreamlitSessionManager): Streamlit session manager

    Returns:
        list[Page]: List of pages
    """
    pages: list[page.Page] = [
        login.LoginPage(page_id=const.PageId.PUBLIC_LOGIN, title="ログイン", ssm=ssm),
        item_list.ItemListPage(page_id=const.PageId.PUBLIC_ITEM_LIST, title="商品一覧", ssm=ssm),
        item_detail.ItemDetailPage(page_id=const.PageId.PUBLIC_ITEM_DETAIL, title="商品詳細", ssm=ssm),
        cart_list.CartPage(page_id=const.PageId.MEMBER_CART, title="カート", ssm=ssm),
        order_list.OrderListPage(page_id=const.PageId.MEMBER_ORDER_LIST, title="注文一覧", ssm=ssm),
        order_detail.OrderDetailPage(page_id=const.PageId.MEMBER_ORDER_DETAIL, title="注文詳細", ssm=ssm),
    ]
    return pages


def init_app(ssm: session_manager.StreamlitSessionManager, pages: list[page.Page]) -> app.MultiPageApp:
    app_info = app.MultiPageApp(ssm=ssm, page_list=pages)
    return app_info
