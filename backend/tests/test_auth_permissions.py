from __future__ import annotations

import pytest

from app.auth.permissions import get_allowed_permissions, has_permission, require_permission
from app.auth.routes import PermissionCheckInput, check_permission_endpoint


def test_AC_AUTH_04_role_permissions():
    assert has_permission("student", "view_dashboard") is True
    assert has_permission("student", "manage_events") is False
    assert has_permission("audience", "register_for_event") is True
    assert has_permission("band", "manage_own_band") is True
    assert has_permission("band", "manage_events") is False
    assert has_permission("organizer", "manage_events") is True
    assert has_permission("admin", "manage_users") is True

    with pytest.raises(PermissionError):
        require_permission("student", "manage_events")

    assert get_allowed_permissions("student") == {
        "view_dashboard",
        "view_schedule",
        "manage_own_profile",
        "register_for_event",
    }

    result = check_permission_endpoint(PermissionCheckInput(role="student", permission="manage_events"))
    assert result["success"] is False
    assert result["allowed"] is False
    assert result["message"] == "คุณไม่มีสิทธิ์ดำเนินการนี้"

    admin_result = check_permission_endpoint(PermissionCheckInput(role="admin", permission="manage_users"))
    assert admin_result["success"] is True
    assert admin_result["allowed"] is True
