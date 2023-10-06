"""Define Page model."""
from typing import Protocol

import const
import session_manager
from models import user


def validate_user(ssm: session_manager.StreamlitSessionManager) -> bool:
    """Validate the user.

    Args:
        ssm (session_manager.StreamlitSessionManager): The session manager.

    Returns:
        bool: True if the user is valid, otherwise False.
    """
    user_info: user.User | None = ssm.get_user()
    if (user_info is None) or (user_info.role not in (const.UserRole.MEMBER, const.UserRole.ADMIN)):
        return False
    return True


class Page(Protocol):
    page_id: const.PageId
    title: str
    ssm: session_manager.StreamlitSessionManager

    def render(self) -> None:
        pass
