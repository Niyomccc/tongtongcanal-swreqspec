from __future__ import annotations

import re
import secrets
from hashlib import pbkdf2_hmac
from typing import Any, Mapping

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.auth.repository import AuthRepository
from app.auth.validation import validate_registration_payload
from app.config import PASSWORD_MIN_LENGTH

# รองรับ FR-AUTH-02, FR-AUTH-03, FR-AUTH-05 และ NFR-SEC-01
PUBLIC_ROLES = {"student", "audience", "band"}
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


class RegisterUserInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    email: str
    password: str
    confirmPassword: str | None = None
    confirm_password: str | None = None
    role: str
    fullNameOrBandName: str | None = None
    full_name_or_band_name: str | None = None
    studentId: str | None = None
    student_id: str | None = None
    universityCode: str | None = None
    university_code: str | None = None
    phoneNumber: str | None = None
    phone_number: str | None = None
    bandName: str | None = None
    band_name: str | None = None
    contactName: str | None = None
    contact_name: str | None = None
    memberCount: int | None = None
    member_count: int | None = None
    genre: str | None = None
    performanceList: str | None = None
    performance_list: str | None = None
    profileData: dict[str, Any] | None = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not value or "@" not in value:
            raise ValueError("อีเมลไม่ถูกต้อง")
        return value.strip()

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        normalized = str(value).strip().lower()
        if normalized not in ROLE_ALIASES:
            raise ValueError("บทบาทไม่ถูกต้อง")
        return ROLE_ALIASES[normalized]


# รองรับ FR-AUTH-02 และ FR-AUTH-03
def _normalize_role(value: Any) -> str:
    if value is None:
        return ""
    normalized = str(value).strip().lower()
    return ROLE_ALIASES.get(normalized, normalized)


def _normalize_payload(payload: Mapping[str, Any] | RegisterUserInput) -> dict[str, Any]:
    if isinstance(payload, RegisterUserInput):
        raw = payload.model_dump(exclude_none=True)
    else:
        raw = dict(payload)

    profile_data = raw.get("profileData") or {}
    if not isinstance(profile_data, dict):
        profile_data = {}

    merged = {**profile_data, **raw}

    merged["role"] = _normalize_role(merged.get("role") or merged.get("userRole") or merged.get("user_role"))
    merged["password"] = merged.get("password") or merged.get("userPassword") or merged.get("user_password")
    merged["confirmPassword"] = (
        merged.get("confirmPassword")
        or merged.get("confirm_password")
        or merged.get("confirmPasswordValue")
    )
    merged["email"] = merged.get("email") or merged.get("emailAddress")
    merged["fullNameOrBandName"] = (
        merged.get("fullNameOrBandName")
        or merged.get("full_name_or_band_name")
        or merged.get("fullName")
    )
    merged["studentId"] = merged.get("studentId") or merged.get("student_id") or profile_data.get("studentId")
    merged["universityCode"] = (
        merged.get("universityCode") or merged.get("university_code") or profile_data.get("universityCode")
    )
    merged["phoneNumber"] = merged.get("phoneNumber") or merged.get("phone_number") or profile_data.get("phoneNumber")
    merged["bandName"] = merged.get("bandName") or merged.get("band_name") or profile_data.get("bandName")
    merged["contactName"] = merged.get("contactName") or merged.get("contact_name") or profile_data.get("contactName")
    merged["memberCount"] = merged.get("memberCount") or merged.get("member_count") or profile_data.get("memberCount")
    merged["genre"] = merged.get("genre") or profile_data.get("genre")
    merged["performanceList"] = (
        merged.get("performanceList") or merged.get("performance_list") or profile_data.get("performanceList")
    )
    return merged


# รองรับ FR-AUTH-02, FR-AUTH-03, FR-AUTH-05 และ NFR-SEC-01
def _hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    derived = pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000)
    return derived.hex(), salt


# รองรับ FR-AUTH-02, FR-AUTH-03, FR-AUTH-05 และ NFR-SEC-01
def _validate_and_build_profile(payload: Mapping[str, Any]) -> dict[str, Any]:
    role = _normalize_role(payload.get("role"))
    profile: dict[str, Any] = {}

    if role == "student":
        student_id = str(payload.get("studentId") or payload.get("student_id") or "").strip()
        if not student_id:
            raise ValueError("ต้องระบุรหัสนักศึกษา")
        if not re.fullmatch(r"[A-Za-z0-9-]+", student_id):
            raise ValueError("รูปแบบรหัสนักศึกษาไม่ถูกต้อง")
        profile["student_id"] = student_id
        profile["university_code"] = str(payload.get("universityCode") or payload.get("university_code") or "").strip()
        profile["full_name_or_band_name"] = str(payload.get("fullNameOrBandName") or payload.get("full_name_or_band_name") or "").strip()
    elif role == "audience":
        phone_number = str(payload.get("phoneNumber") or payload.get("phone_number") or "").strip()
        if not phone_number:
            raise ValueError("ต้องระบุหมายเลขโทรศัพท์")
        profile["phone_number"] = phone_number
        profile["full_name_or_band_name"] = str(payload.get("fullNameOrBandName") or payload.get("full_name_or_band_name") or "").strip()
    elif role == "band":
        band_name = str(payload.get("bandName") or payload.get("band_name") or "").strip()
        if not band_name:
            raise ValueError("ต้องระบุชื่อวง")
        profile["band_name"] = band_name
        profile["contact_name"] = str(payload.get("contactName") or payload.get("contact_name") or "").strip()
        profile["phone_number"] = str(payload.get("phoneNumber") or payload.get("phone_number") or "").strip()
        profile["member_count"] = payload.get("memberCount") or payload.get("member_count")
        profile["genre"] = payload.get("genre")
        profile["performance_list"] = payload.get("performanceList") or payload.get("performance_list")
        profile["full_name_or_band_name"] = band_name
    else:
        raise ValueError("ไม่อนุญาตให้สมัครด้วยบทบาทนี้")

    return profile


# รองรับ FR-AUTH-02, FR-AUTH-03, FR-AUTH-05 และ NFR-SEC-01
def register_user(payload: Mapping[str, Any] | RegisterUserInput, repository: AuthRepository | None = None) -> dict[str, Any]:
    normalized = _normalize_payload(payload)
    role = _normalize_role(normalized.get("role"))

    repo = repository or AuthRepository()
    validation = validate_registration_payload(normalized, repository=repo)
    if not validation["valid"]:
        errors = validation["errors"]
        first_error = next(iter(errors.values()))
        raise ValueError(first_error)

    email = str(normalized.get("email") or "").strip()
    password = str(normalized.get("password") or "")
    confirm_password = str(normalized.get("confirmPassword") or normalized.get("confirm_password") or "")
    if "@" not in email:
        raise ValueError("อีเมลไม่ถูกต้อง")
    if len(password) < PASSWORD_MIN_LENGTH:
        raise ValueError(f"รหัสผ่านต้องยาวอย่างน้อย {PASSWORD_MIN_LENGTH} ตัวอักษร")
    if confirm_password and password != confirm_password:
        raise ValueError("รหัสผ่านและยืนยันรหัสผ่านไม่ตรงกัน")

    full_name_or_band_name = (
        str(normalized.get("fullNameOrBandName") or normalized.get("full_name_or_band_name") or "").strip()
    )
    if not full_name_or_band_name and role == "student":
        full_name_or_band_name = str(normalized.get("fullName") or "").strip()

    if not full_name_or_band_name:
        raise ValueError("ต้องระบุชื่อผู้ใช้หรือชื่อวง")

    profile = _validate_and_build_profile(normalized)
    if role == "student" and not profile.get("student_id"):
        raise ValueError("ต้องระบุรหัสนักศึกษา")
    if role == "band" and not profile.get("band_name"):
        raise ValueError("ต้องระบุชื่อวง")

    if repo.get_by_email(email):
        raise ValueError("อีเมลนี้มีผู้ใช้อยู่แล้ว")

    if role == "student":
        student_id = str(profile["student_id"]).strip()
        if repo.get_by_student_id(student_id):
            raise ValueError("รหัสนักศึกษานี้มีผู้ใช้อยู่แล้ว")
    if role == "band":
        band_name = str(profile["band_name"]).strip()
        if repo.get_by_band_name(band_name):
            raise ValueError("ชื่อวงนี้มีผู้ใช้อยู่แล้ว")

    password_hash, salt = _hash_password(password)
    user = repo.create_user(
        email=email,
        password_hash=password_hash,
        salt=salt,
        full_name_or_band_name=full_name_or_band_name,
        role=role,
        profile=profile,
    )
    return {
        "success": True,
        "message": "สมัครสมาชิกสำเร็จ",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "full_name_or_band_name": user["full_name_or_band_name"],
            "status": user["status"],
        },
        "profile": profile,
        "redirectTo": "/dashboard",
    }


router = APIRouter()


@router.post("/auth/register")
@router.post("/api/auth/register")
async def register_endpoint(payload: RegisterUserInput) -> dict[str, Any]:
    return register_user(payload)


__all__ = ["RegisterUserInput", "register_user", "register_endpoint", "router"]
