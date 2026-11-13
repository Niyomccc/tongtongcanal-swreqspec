from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from app.auth.permissions import get_user_display_role, normalize_role
from app.config import SESSION_IDLE_TIMEOUT_MINUTES

# รองรับ FR-AUTH-03 และ NFR-SEC-01
_SESSION_STORE: dict[str, dict[str, Any]] = {}


def reset_sessions() -> None:
    """ล้างข้อมูล session สำหรับการทดสอบหรือเริ่มรอบใหม่"""
    _SESSION_STORE.clear()


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def create_session(user_id: int, *, session_id: str | None = None, role: str | None = None) -> dict[str, Any]:
    """สร้าง session พร้อมบทบาทที่ใช้ตรวจสิทธิ์ตาม NFR-SEC-01 และ Q-05"""
    generated_session_id = session_id or secrets.token_urlsafe(32)
    issued_at = _utc_now()
    expires_at = issued_at + timedelta(minutes=SESSION_IDLE_TIMEOUT_MINUTES)
    normalized_role = normalize_role(role) or None
    record = {
        "session_id": generated_session_id,
        "user_id": user_id,
        "role": normalized_role,
        "display_role": get_user_display_role(normalized_role) if normalized_role else None,
        "issued_at": issued_at,
        "expires_at": expires_at,
        "last_seen_at": issued_at,
    }
    _SESSION_STORE[generated_session_id] = record
    return record


def get_session(session_id: str) -> dict[str, Any] | None:
    """คืน session ที่ยังไม่หมดอายุตาม FR-AUTH-03"""
    session = _SESSION_STORE.get(session_id)
    if session is None:
        return None

    if session["expires_at"] <= _utc_now():
        _SESSION_STORE.pop(session_id, None)
        return None
    return session


def validate_session(session_id: str) -> dict[str, Any] | None:
    """ตรวจ session และต่ออายุเมื่อใช้งานอีกครั้งภายใต้ idle timeout พร้อมให้ role และสิทธิ์พร้อมใช้งาน"""
    session = _SESSION_STORE.get(session_id)
    if session is None:
        return None

    now = _utc_now()
    if session["expires_at"] <= now:
        _SESSION_STORE.pop(session_id, None)
        return None

    session["last_seen_at"] = now
    session["expires_at"] = now + timedelta(minutes=SESSION_IDLE_TIMEOUT_MINUTES)
    return session


def get_session_user_context(session_id: str) -> dict[str, Any] | None:
    """คืน context ที่ใช้ตรวจสิทธิ์ข้อมูลลงทะเบียนตาม NFR-SEC-01 และ Q-05"""
    session = get_session(session_id)
    if session is None:
        return None
    return {
        "user_id": session.get("user_id"),
        "role": session.get("role"),
        "display_role": session.get("display_role"),
    }


def invalidate_session(session_id: str) -> bool:
    """ยกเลิก session โดยตรงเมื่อ logout หรือ force terminate"""
    existed = session_id in _SESSION_STORE
    _SESSION_STORE.pop(session_id, None)
    return existed


def list_sessions_for_user(user_id: int) -> list[dict[str, Any]]:
    """คืน session ทั้งหมดของผู้ใช้เพื่อใช้ในการตรวจสอบการเข้าถึง"""
    return [session for session in _SESSION_STORE.values() if session["user_id"] == user_id]


__all__ = [
    "create_session",
    "get_session",
    "validate_session",
    "get_session_user_context",
    "invalidate_session",
    "list_sessions_for_user",
    "reset_sessions",
]
