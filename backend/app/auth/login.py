from __future__ import annotations

from datetime import datetime, timedelta, timezone
from hashlib import pbkdf2_hmac
from typing import Any, Mapping

from fastapi import APIRouter
from pydantic import BaseModel

from app.auth.register import _hash_password
from app.auth.repository import AuthRepository
from app.auth.session import create_session, reset_sessions
from app.config import (
    ACCOUNT_LOCKOUT_DURATION_MINUTES,
    FAILED_LOGIN_ATTEMPT_LIMIT,
    GENERIC_LOGIN_ERROR_MESSAGE,
)

# รองรับ FR-AUTH-03 และ NFR-SEC-01


class LoginUserInput(BaseModel):
    email: str
    password: str


def _verify_password(password: str, password_hash: str, salt: str) -> bool:
    derived, _ = _hash_password(password, salt)
    return derived == password_hash


def _as_email(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _as_password(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def login_user(payload: Mapping[str, Any] | LoginUserInput, repository: AuthRepository | None = None) -> dict[str, Any]:
    """ตรวจข้อมูลเข้าสู่ระบบและสร้าง session เมื่อยืนยันตัวตนสำเร็จตาม AC-AUTH-02"""
    if isinstance(payload, LoginUserInput):
        raw = payload.model_dump()
    else:
        raw = dict(payload)

    email = _as_email(raw.get("email") or raw.get("userEmail") or raw.get("emailAddress"))
    password = _as_password(raw.get("password") or raw.get("userPassword") or raw.get("user_password"))

    repo = repository or AuthRepository()
    user = repo.get_by_email(email)
    now = datetime.now(timezone.utc)

    if user is None:
        raise ValueError(GENERIC_LOGIN_ERROR_MESSAGE)

    lock_until = user.get("lock_until")
    if isinstance(lock_until, datetime) and lock_until > now:
        raise ValueError(GENERIC_LOGIN_ERROR_MESSAGE)
    if isinstance(lock_until, datetime) and lock_until <= now:
        user["lock_until"] = None
        user["failed_login_count"] = 0

    user_password_hash = str(user.get("password_hash") or "")
    user_salt = str(user.get("salt") or "")

    if not _verify_password(password, user_password_hash, user_salt):
        failed_attempts = int(user.get("failed_login_count") or 0) + 1
        user["failed_login_count"] = failed_attempts
        if failed_attempts >= FAILED_LOGIN_ATTEMPT_LIMIT:
            user["lock_until"] = now + timedelta(minutes=ACCOUNT_LOCKOUT_DURATION_MINUTES)
        raise ValueError(GENERIC_LOGIN_ERROR_MESSAGE)

    user["failed_login_count"] = 0
    user["lock_until"] = None
    user["last_login_at"] = now

    session = create_session(int(user["id"]))

    return {
        "success": True,
        "message": "เข้าสู่ระบบสำเร็จ",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "full_name_or_band_name": user["full_name_or_band_name"],
            "status": user["status"],
        },
        "session": session,
        "redirectTo": "/dashboard",
    }


router = APIRouter()


@router.post("/auth/login")
@router.post("/api/auth/login")
async def login_endpoint(payload: LoginUserInput) -> dict[str, Any]:
    return login_user(payload)


__all__ = ["LoginUserInput", "login_user", "login_endpoint", "router", "reset_sessions"]
