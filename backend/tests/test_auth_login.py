from __future__ import annotations

import pytest

from app.auth.login import login_user
from app.auth.register import register_user
from app.auth.repository import AuthRepository
from app.auth.session import reset_sessions


@pytest.fixture(autouse=True)
def clear_repository():
    repo = AuthRepository()
    repo.reset()
    reset_sessions()
    yield
    repo.reset()
    reset_sessions()


def test_AC_AUTH_02_login_success():
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

    result = login_user({"email": "student01@ku.th", "password": "P@ssword123"})

    assert result["success"] is True
    assert result["redirectTo"] == "/dashboard"
    assert result["user"]["email"] == "student01@ku.th"
    assert result["user"]["role"] == "student"
    assert result["session"]["user_id"] == AuthRepository().get_by_email("student01@ku.th")["id"]
    assert result["session"]["session_id"]


def test_AUTH_login_rejects_invalid_credentials_without_leaking_details():
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

    with pytest.raises(ValueError, match="อีเมลหรือรหัสผ่านไม่ถูกต้อง"):
        login_user({"email": "student01@ku.th", "password": "wrong-pass"})
