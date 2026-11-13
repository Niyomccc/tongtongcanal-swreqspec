from __future__ import annotations

import re
from typing import Any, Mapping

from app.auth.repository import AuthRepository
from app.config import GENERIC_LOGIN_ERROR_MESSAGE, PASSWORD_MIN_LENGTH

# รองรับ FR-AUTH-02, FR-AUTH-04 และ NFR-SEC-01

ROLE_ALIASES = {
    "student": "student",
    "นักศึกษา": "student",
    "audience": "audience",
    "ผู้ชม": "audience",
    "band": "band",
    "วงดนตรี": "band",
    "organizer": "organizer",
    "ผู้จัดงาน": "organizer",
    "admin": "admin",
}

PUBLIC_ROLES = {"student", "audience", "band"}


def _normalize_role(value: Any) -> str:
    if value is None:
        return ""
    normalized = str(value).strip().lower()
    return ROLE_ALIASES.get(normalized, normalized)


def _coerce_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def validate_email(value: Any) -> str:
    """ตรวจรูปแบบอีเมลและคืนค่า normalized email ตาม FR-AUTH-02"""
    email = _coerce_str(value)
    if not email or "@" not in email:
        raise ValueError("อีเมลไม่ถูกต้อง")
    return email.lower()


def validate_password(value: Any) -> str:
    """ตรวจความยาวขั้นต่ำรหัสผ่านตาม NFR-SEC-01"""
    password = _coerce_str(value)
    if len(password) < PASSWORD_MIN_LENGTH:
        raise ValueError(f"รหัสผ่านต้องยาวอย่างน้อย {PASSWORD_MIN_LENGTH} ตัวอักษร")
    return password


def validate_registration_payload(payload: Mapping[str, Any], *, repository: AuthRepository | None = None) -> dict[str, Any]:
    """ตรวจข้อมูลสมัครสมาชิกและคืน errors รวมแบบยืดหยุ่นสำหรับ API validation"""
    raw = dict(payload)
    role = _normalize_role(raw.get("role") or raw.get("userRole") or raw.get("user_role"))

    if role not in ROLE_ALIASES.values():
        raise ValueError("บทบาทไม่ถูกต้อง")
    if role not in PUBLIC_ROLES:
        raise ValueError("ไม่อนุญาตให้สมัครด้วยบทบาทนี้")

    errors: dict[str, str] = {}
    email = raw.get("email") or raw.get("emailAddress")
    if not email or "@" not in str(email):
        errors["email"] = "อีเมลไม่ถูกต้อง"
    else:
        normalized_email = str(email).strip().lower()
        repo = repository or AuthRepository()
        if repo.get_by_email(normalized_email):
            errors["email"] = "อีเมลนี้มีผู้ใช้อยู่แล้ว"

    password = raw.get("password") or raw.get("userPassword") or raw.get("user_password")
    if password is None or len(str(password)) < PASSWORD_MIN_LENGTH:
        errors["password"] = f"รหัสผ่านต้องยาวอย่างน้อย {PASSWORD_MIN_LENGTH} ตัวอักษร"

    confirm_password = raw.get("confirmPassword") or raw.get("confirm_password")
    if confirm_password is not None and password is not None and str(password) != str(confirm_password):
        errors["confirmPassword"] = "รหัสผ่านและยืนยันรหัสผ่านไม่ตรงกัน"

    full_name = (
        raw.get("fullNameOrBandName")
        or raw.get("full_name_or_band_name")
        or raw.get("fullName")
        or raw.get("bandName")
        or raw.get("band_name")
        or raw.get("full_name")
    )
    if not str(full_name or "").strip():
        errors["fullNameOrBandName"] = "ต้องระบุชื่อผู้ใช้หรือชื่อวง"

    if role == "student":
        student_id = raw.get("studentId") or raw.get("student_id")
        student_id_text = str(student_id or "").strip()
        if not student_id_text:
            errors["studentId"] = "ต้องระบุรหัสนักศึกษา"
        elif not re.fullmatch(r"[A-Za-z0-9-]+", student_id_text):
            errors["studentId"] = "รูปแบบรหัสนักศึกษาไม่ถูกต้อง"
        else:
            repo = repository or AuthRepository()
            if repo.get_by_student_id(student_id_text):
                errors["studentId"] = "รหัสนักศึกษานี้มีผู้ใช้อยู่แล้ว"

        university_code = raw.get("universityCode") or raw.get("university_code")
        if not str(university_code or "").strip():
            errors["universityCode"] = "กรุณาระบุรหัสมหาวิทยาลัย"

    elif role == "audience":
        phone_number = raw.get("phoneNumber") or raw.get("phone_number")
        if not str(phone_number or "").strip():
            errors["phoneNumber"] = "ต้องระบุหมายเลขโทรศัพท์"

    elif role == "band":
        band_name = raw.get("bandName") or raw.get("band_name")
        if not str(band_name or "").strip():
            errors["bandName"] = "ต้องระบุชื่อวง"
        else:
            repo = repository or AuthRepository()
            if repo.get_by_band_name(str(band_name).strip()):
                errors["bandName"] = "ชื่อวงนี้มีผู้ใช้อยู่แล้ว"

        contact_name = raw.get("contactName") or raw.get("contact_name")
        if not str(contact_name or "").strip():
            errors["contactName"] = "กรุณาระบุชื่อผู้ติดต่อ"

        phone_number = raw.get("phoneNumber") or raw.get("phone_number")
        if not str(phone_number or "").strip():
            errors["phoneNumber"] = "กรุณาระบุเบอร์โทรศัพท์"

    if errors:
        return {"valid": False, "errors": errors}
    return {"valid": True, "errors": {}}


def validate_login_payload(payload: Mapping[str, Any], *, repository: AuthRepository | None = None) -> dict[str, Any]:
    """ตรวจข้อมูล login แบบ generic error เพื่อไม่เปิดเผยข้อมูลที่ผิดว่าผิดตรงไหนตาม NFR-SEC-01"""
    raw = dict(payload)
    email = str(raw.get("email") or raw.get("userEmail") or raw.get("emailAddress") or "").strip().lower()
    password = str(raw.get("password") or raw.get("userPassword") or raw.get("user_password") or "")

    if not email or "@" not in email or not password:
        raise ValueError(GENERIC_LOGIN_ERROR_MESSAGE)

    repo = repository or AuthRepository()
    user = repo.get_by_email(email)
    if user is None:
        raise ValueError(GENERIC_LOGIN_ERROR_MESSAGE)

    return {"valid": True, "email": email, "password": password, "user": user}


__all__ = [
    "ROLE_ALIASES",
    "PUBLIC_ROLES",
    "validate_email",
    "validate_password",
    "validate_registration_payload",
    "validate_login_payload",
]
