from __future__ import annotations

import pytest

from app.auth.register import register_user
from app.auth.repository import AuthRepository


@pytest.fixture(autouse=True)
def clear_repository():
    repo = AuthRepository()
    repo.reset()
    yield
    repo.reset()


def test_AC_AUTH_01_register_success():
    payload = {
        "email": "student01@ku.th",
        "password": "P@ssword123",
        "confirmPassword": "P@ssword123",
        "role": "นักศึกษา",
        "fullNameOrBandName": "นางสาวสมใจ รักเรียน",
        "studentId": "65123456",
        "universityCode": "KU",
    }

    result = register_user(payload)

    assert result["success"] is True
    assert result["redirectTo"] == "/dashboard"
    assert result["user"]["role"] == "student"
    assert result["user"]["email"] == "student01@ku.th"
    assert result["profile"]["student_id"] == "65123456"
    assert result["user"]["full_name_or_band_name"] == "นางสาวสมใจ รักเรียน"

    saved = AuthRepository().get_by_email("student01@ku.th")
    assert saved is not None
    assert saved["password_hash"] != payload["password"]
    assert saved["salt"]
    assert saved["profile"]["student_id"] == "65123456"
    assert saved["role"] == "student"


def test_AUTH_registration_rejects_public_admin_roles():
    with pytest.raises(ValueError, match="ไม่อนุญาต"):
        register_user(
            {
                "email": "admin@ku.th",
                "password": "P@ssword123",
                "confirmPassword": "P@ssword123",
                "role": "admin",
                "fullNameOrBandName": "ผู้ดูแล",
            }
        )

    with pytest.raises(ValueError, match="ไม่อนุญาต"):
        register_user(
            {
                "email": "organizer@ku.th",
                "password": "P@ssword123",
                "confirmPassword": "P@ssword123",
                "role": "organizer",
                "fullNameOrBandName": "ผู้จัดงาน",
            }
        )
