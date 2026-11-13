from __future__ import annotations

# รองรับ NFR-SEC-01, ASM-04 และ Q-05: กำหนดสิทธิ์ข้อมูลลงทะเบียนและกลุ่มผู้เข้าชม
REGISTRATION_ROLE_LABELS: dict[str, str] = {
    "student": "นักศึกษา",
    "audience": "ผู้ชม",
    "band": "วงดนตรี",
    "organizer": "ผู้จัดงาน",
    "admin": "ผู้ดูแล",
}

REGISTRATION_ATTENDEE_LABEL = "ผู้เข้าชม"
REGISTRATION_PUBLIC_ROLE_GROUP = {"student", "audience"}

DEFAULT_ROLE_PERMISSIONS: dict[str, set[str]] = {
    "student": {"view_dashboard", "view_schedule", "manage_own_profile", "register_for_event"},
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


def get_user_display_role(role: str | None) -> str:
    """คืนคำเรียกบทบาทของผู้ใช้ตาม Q-05"""
    normalized = normalize_role(role)
    return REGISTRATION_ROLE_LABELS.get(normalized, normalized or "ผู้ใช้")


def can_access_registration_record(user: dict | None, owner_user_id: int | None) -> bool:
    """จำกัดข้อมูลลงทะเบียนให้เจ้าของรายการหรือผู้จัดงานตาม NFR-SEC-01 และ ASM-04"""
    if not isinstance(user, dict):
        return False

    actor_user_id = user.get("user_id", user.get("id"))
    actor_role = normalize_role(user.get("role"))
    if actor_role == "organizer":
        return True
    if owner_user_id is None:
        return False
    return actor_user_id == owner_user_id


def get_user_permission_summary(user: dict | None) -> dict[str, object]:
    """สรุปสิทธิ์และคำเรียกกลุ่มผู้เข้าชมตาม Q-05"""
    role = user.get("role") if isinstance(user, dict) else None
    normalized = normalize_role(role)
    registration_eligible = normalized in REGISTRATION_PUBLIC_ROLE_GROUP
    return {
        "role": normalized,
        "display_role": get_user_display_role(role),
        "permissions": sorted(get_allowed_permissions(role)),
        "registration_group": REGISTRATION_ATTENDEE_LABEL if registration_eligible else None,
        "registration_eligible": registration_eligible,
    }
