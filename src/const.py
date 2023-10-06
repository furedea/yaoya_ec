"""Define constant values for the application."""
from enum import auto, Enum


class UserRole(Enum):
    """User roles."""
    ADMIN = auto()
    MEMBER = auto()


class PageId(Enum):
    """Page IDs for streamlit.session_state."""
    PUBLIC_LOGIN = auto()
    PUBLIC_ITEM_LIST = auto()
    PUBLIC_ITEM_DETAIL = auto()
    MEMBER_CART = auto()
    MEMBER_ORDER_LIST = auto()
    MEMBER_ORDER_DETAIL = auto()


class SessionKey(Enum):
    """Session keys for streamlit.session_state."""
    AUTH_API_CLIENT = auto()
    USER_API_CLIENT = auto()
    ITEM_API_CLIENT = auto()
    ORDER_API_CLIENT = auto()
    CART_API_CLIENT = auto()
    USER = auto()
    ITEM = auto()
    ORDER = auto()
    PAGE_ID = auto()
    SESSION_ID = auto()
    USERBOX = auto()
