from __future__ import annotations

# รองรับ FR-AUTH-05
DEFAULT_ROLE_PERMISSIONS: dict[str, set[str]] = {
    "student": {"view_dashboard", "view_schedule", "manage_own_profile"},
    "audience": {"view_dashboard", "view_schedule", "register_for_event"},
    "band": {"view_dashboard", "manage_own_band", "view_own_bookings"},
    "organizer": {"view_dashboard", "manage_events", "review_registrations"},
    "admin": {"view_dashboard", "manage_events", "manage_users", "manage_permissions", "review_registrations"},
}


def normalize_role(role: str | None) -> str:
    if role is None:
        return ""
    value = str(role).strip().lower()
    if value in {"นักศึกษา", "student"}:
        return "student"
    if value in {"ผู้ชม", "audience"}:
        return "audience"
    if value in {"วงดนตรี", "band"}:
        return "band"
    if value in {"ผู้จัดงาน", "organizer"}:
        return "organizer"
    if value in {"admin", "administrator"}:
        return "admin"
    return value


def get_allowed_permissions(role: str | None) -> set[str]:
    normalized = normalize_role(role)
    return set(DEFAULT_ROLE_PERMISSIONS.get(normalized, set()))


def has_permission(role: str | None, permission: str) -> bool:
    if permission is None:
        return False
    normalized_permission = str(permission).strip().lower()
    if normalize_role(role) == "admin":
        return True
    return normalized_permission in get_allowed_permissions(role)


def require_permission(role: str | None, permission: str) -> bool:
    if not has_permission(role, permission):
        raise PermissionError("คุณไม่มีสิทธิ์ดำเนินการนี้")
    return True


def get_user_permission_summary(user: dict | None) -> dict[str, object]:
    role = user.get("role") if isinstance(user, dict) else None
    return {
        "role": normalize_role(role),
        "permissions": sorted(get_allowed_permissions(role)),
    }
