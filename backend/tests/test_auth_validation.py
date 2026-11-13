from __future__ import annotations

import pytest

from app.auth.register import register_user
from app.auth.repository import AuthRepository
from app.auth.validation import validate_registration_payload


@pytest.fixture(autouse=True)
def clear_repository():
    repo = AuthRepository()
    repo.reset()
    yield
    repo.reset()


def test_AC_AUTH_03_invalid_input_api():
    repo = AuthRepository()
    register_user(
        {
            "email": "student01@ku.th",
            "password": "P@ssword123",
            "confirmPassword": "P@ssword123",
            "role": "นักศึกษา",
            "fullNameOrBandName": "นางสาวสมใจ รักเรียน",
            "studentId": "65123456",
            "universityCode": "KU",
        },
        repository=repo,
    )

    invalid = {
        "email": "bad-email",
        "password": "short",
        "confirmPassword": "different",
        "role": "นักศึกษา",
        "fullNameOrBandName": "",
        "studentId": "bad id",
        "universityCode": "",
    }

    result = validate_registration_payload(invalid, repository=repo)
    assert result["valid"] is False
    assert result["errors"]["email"] == "อีเมลไม่ถูกต้อง"
    assert "password" in result["errors"]
    assert "studentId" in result["errors"]
    assert "confirmPassword" in result["errors"]
    assert "fullNameOrBandName" in result["errors"]

    duplicate = {
        "email": "student01@ku.th",
        "password": "P@ssword123",
        "confirmPassword": "P@ssword123",
        "role": "นักศึกษา",
        "fullNameOrBandName": "นางสาวสมใจ รักเรียน",
        "studentId": "65123457",
        "universityCode": "KU",
    }

    duplicate_result = validate_registration_payload(duplicate, repository=repo)
    assert duplicate_result["errors"]["email"] == "อีเมลนี้มีผู้ใช้อยู่แล้ว"

    valid = {
        "email": "newstudent@ku.th",
        "password": "P@ssword123",
        "confirmPassword": "P@ssword123",
        "role": "นักศึกษา",
        "fullNameOrBandName": "นางสาวใหม่ รักการศึกษา",
        "studentId": "65123457",
        "universityCode": "KU",
    }

    assert validate_registration_payload(valid, repository=repo)["valid"] is True
