from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from app.auth.login import login_user
from app.auth.register import register_user
from app.auth.repository import AuthRepository
from app.auth.session import create_session, get_session, reset_sessions, validate_session


@pytest.fixture(autouse=True)
def clear_repository():
    repo = AuthRepository()
    repo.reset()
    reset_sessions()
    yield
    repo.reset()
    reset_sessions()


def test_AUTH_session_expiry_and_lockout():
    register_user(
        {
            "email": "student01@ku.th",
            "password": "P@ssword123",
            "confirmPassword": "P@ssword123",
            "role": "นักศึกษา",
            "fullNameOrBandName": "นางสาวสมใจ รักเรียน",
            "studentId": "65123456",
            "universityCode": "KU",
        }
    )

    session = create_session(AuthRepository().get_by_email("student01@ku.th")["id"])
    assert get_session(session["session_id"]) is not None

    session["expires_at"] = datetime.now(timezone.utc) - timedelta(minutes=1)
    assert get_session(session["session_id"]) is None
    assert validate_session(session["session_id"]) is None

    for _ in range(5):
        with pytest.raises(ValueError, match="อีเมลหรือรหัสผ่านไม่ถูกต้อง"):
            login_user({"email": "student01@ku.th", "password": "wrong-pass"})

    user = AuthRepository().get_by_email("student01@ku.th")
    assert user is not None
    assert user["lock_until"] is not None

    user["lock_until"] = datetime.now(timezone.utc) - timedelta(minutes=1)
    user["failed_login_count"] = 0
    result = login_user({"email": "student01@ku.th", "password": "P@ssword123"})
    assert result["success"] is True
    assert result["redirectTo"] == "/dashboard"
