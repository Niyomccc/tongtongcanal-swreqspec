from __future__ import annotations

import pytest

from app.auth.login import login_user
from app.auth.session import _SESSION_STORE, reset_sessions


class UnavailableRepository:
    def get_by_email(self, email: str):
        raise RuntimeError("database unavailable")


def test_AC_AUTH_05_db_unavailable_block_login():
    reset_sessions()

    with pytest.raises(ValueError, match="อีเมลหรือรหัสผ่านไม่ถูกต้อง"):
        login_user({"email": "student01@ku.th", "password": "P@ssword123"}, repository=UnavailableRepository())

    assert len(_SESSION_STORE) == 0
