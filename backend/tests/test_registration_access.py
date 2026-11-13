from __future__ import annotations

import pytest

from app.auth.login import login_user
from app.auth.permissions import (
    can_access_registration_record,
    get_user_permission_summary,
    has_permission,
)
from app.auth.register import register_user
from app.auth.repository import AuthRepository
from app.auth.session import get_session_user_context, reset_sessions
from app.models.auth import Registration, Session


@pytest.fixture(autouse=True)
def clear_auth_state():
    repository = AuthRepository()
    repository.reset()
    reset_sessions()
    yield
    repository.reset()
    reset_sessions()


def test_REG_T10_attendees_share_registration_rights_and_label():
    student = get_user_permission_summary({"role": "student"})
    audience = get_user_permission_summary({"role": "audience"})

    assert has_permission("student", "register_for_event") is True
    assert has_permission("audience", "register_for_event") is True
    assert student["registration_group"] == "ผู้เข้าชม"
    assert audience["registration_group"] == "ผู้เข้าชม"
    assert student["registration_eligible"] is True
    assert audience["registration_eligible"] is True
    assert get_user_permission_summary({"role": "band"})["registration_eligible"] is False


def test_REG_T10_registration_access_is_limited_to_owner_and_organizer():
    assert can_access_registration_record({"user_id": 21, "role": "student"}, 21) is True
    assert can_access_registration_record({"id": 22, "role": "audience"}, 21) is False
    assert can_access_registration_record({"role": "organizer"}, 21) is True
    assert can_access_registration_record({"role": "admin"}, 21) is False
    assert can_access_registration_record(None, 21) is False


def test_REG_T10_login_session_retains_role_context():
    register_user(
        {
            "email": "visitor@example.test",
            "password": "P@ssword123",
            "confirmPassword": "P@ssword123",
            "role": "ผู้ชม",
            "fullNameOrBandName": "ผู้เข้าชมทดสอบ",
            "phoneNumber": "0812345678",
        }
    )

    result = login_user({"email": "visitor@example.test", "password": "P@ssword123"})
    context = get_session_user_context(result["session"]["session_id"])

    assert context == {"user_id": result["user"]["id"], "role": "audience", "display_role": "ผู้ชม"}


def test_REG_T10_registration_model_requires_confirmation_snapshot():
    registration_columns = Registration.__table__.columns
    assert registration_columns["user_id"].nullable is False
    assert registration_columns["event_id"].nullable is False
    assert registration_columns["confirmation_snapshot"].nullable is False
    assert Session.__table__.columns["role"].nullable is True
