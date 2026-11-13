from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.auth.repository import AuthRepository, BandApplicationSaveError
from app.auth.session import validate_session
from app.config import (
    BAND_APPLICATION_MAX_PERFORMANCE_MINUTES,
    BAND_APPLICATION_MAX_SONG_COUNT,
    BAND_APPLICATION_REQUIRED_SNAPSHOT_FIELDS,
)

# รองรับ FR-APP-01, FR-APP-02, PRE-APP-01: รายการอีเว้นต์เปิดรับสมัครและข้อมูลวงสำหรับฟอร์มสมัครต้องตรวจ session ก่อนใช้งาน
router = APIRouter()


def _derive_band_profile(user_record: dict[str, Any]) -> dict[str, Any]:
    profile = dict(user_record.get("profile") or {})
    band_name = str(profile.get("band_name") or user_record.get("full_name_or_band_name") or "").strip()
    genre = str(profile.get("genre") or "").strip()
    members = str(profile.get("members") or profile.get("member_list") or profile.get("member_count") or "").strip()
    contact_name = str(profile.get("contact_name") or "").strip()
    contact_phone = str(profile.get("contact_phone") or profile.get("phone_number") or "").strip()
    return {
        "band_id": int(user_record["id"]),
        "band_name": band_name,
        "genre": genre,
        "members": members,
        "contact_name": contact_name,
        "contact_phone": contact_phone,
    }


def _resolve_band_context(
    *,
    session_id: str | None,
    user_id: int | None,
    repository: AuthRepository,
) -> tuple[int | None, str | None]:
    if session_id:
        session = validate_session(session_id)
        if session is None:
            return None, "เซสชันหมดอายุหรือไม่ถูกต้อง"
        resolved_user_id = int(session.get("user_id"))
        if user_id is not None and resolved_user_id != int(user_id):
            return None, "คุณไม่มีสิทธิ์เข้าถึงข้อมูลนี้"
        return resolved_user_id, None

    if user_id is None:
        return None, "กรุณาเข้าสู่ระบบก่อนใช้งาน"

    user = repository.get_by_id(int(user_id))
    if user is None:
        return None, "ไม่พบผู้ใช้นี้"
    return int(user_id), None


def get_open_application_events(
    *,
    session_id: str | None = None,
    user_id: int | None = None,
    repository: AuthRepository | None = None,
) -> dict[str, Any]:
    repo = repository or AuthRepository()
    resolved_user_id, error = _resolve_band_context(session_id=session_id, user_id=user_id, repository=repo)
    if resolved_user_id is None:
        return {
            "success": False,
            "message": error,
            "events": [],
        }

    user = repo.get_by_id(resolved_user_id)
    if user is None or str(user.get("role") or "").lower() != "band":
        return {
            "success": False,
            "message": "เฉพาะวงที่เข้าสู่ระบบแล้วจึงสามารถดูรายการอีเว้นต์ได้",
            "events": [],
        }

    events = repo.seed_open_band_application_events()
    return {
        "success": True,
        "user_id": resolved_user_id,
        "events": events,
        "message": "รายการอีเว้นต์เปิดรับสมัครพร้อมใช้งาน",
    }


def get_band_application_profile(
    *,
    session_id: str | None = None,
    repository: AuthRepository | None = None,
) -> dict[str, Any]:
    """รองรับ FR-APP-02, NFR-SEC-01 และ Q-03: ต้องยืนยันตัวตนก่อนคืนข้อมูลวงสำหรับ snapshot"""
    repo = repository or AuthRepository()
    resolved_user_id, error = _resolve_band_context(session_id=session_id, user_id=None, repository=repo)
    if resolved_user_id is None:
        return {
            "success": False,
            "user_id": None,
            "message": error,
            "band_profile": {},
            "required_fields": list(BAND_APPLICATION_REQUIRED_SNAPSHOT_FIELDS),
            "missing_fields": [],
            "is_complete": False,
        }

    user = repo.get_by_id(resolved_user_id)
    if user is None or str(user.get("role") or "").lower() != "band":
        return {
            "success": False,
            "user_id": resolved_user_id,
            "message": "ข้อมูลวงสำหรับสมัครไม่พบหรือผู้ใช้ไม่ใช่วงดนตรี",
            "band_profile": {},
            "required_fields": list(BAND_APPLICATION_REQUIRED_SNAPSHOT_FIELDS),
            "missing_fields": list(BAND_APPLICATION_REQUIRED_SNAPSHOT_FIELDS),
            "is_complete": False,
        }

    band_profile = _derive_band_profile(user)
    missing_fields = [
        field for field in BAND_APPLICATION_REQUIRED_SNAPSHOT_FIELDS if not str(band_profile.get(field, "")).strip()
    ]
    return {
        "success": True,
        "user_id": resolved_user_id,
        "band_profile": band_profile,
        "required_fields": list(BAND_APPLICATION_REQUIRED_SNAPSHOT_FIELDS),
        "missing_fields": missing_fields,
        "is_complete": not missing_fields,
        "message": "ข้อมูลวงพร้อมสำหรับสมัคร" if not missing_fields else "ข้อมูลวงยังไม่ครบสำหรับสมัคร",
    }


def validate_band_application(
    *,
    session_id: str | None,
    payload: dict[str, Any],
    repository: AuthRepository | None = None,
) -> dict[str, Any]:
    """รองรับ FR-APP-03, FR-APP-05 และ PRE-APP-01: ตรวจข้อมูลวง เพลง และข้อจำกัดก่อนส่งใบสมัคร"""
    repo = repository or AuthRepository()
    resolved_user_id, error = _resolve_band_context(
        session_id=session_id,
        user_id=None,
        repository=repo,
    )
    errors: list[str] = []
    if resolved_user_id is None:
        errors.append(error or "กรุณาเข้าสู่ระบบก่อนใช้งาน")
        return {
            "success": False,
            "is_valid": False,
            "errors": errors,
            "message": "ข้อมูลใบสมัครไม่ถูกต้อง",
        }

    user = repo.get_by_id(resolved_user_id)
    if user is None or str(user.get("role") or "").lower() != "band":
        errors.append("เฉพาะวงที่เข้าสู่ระบบแล้วจึงสามารถส่งใบสมัครได้")
    else:
        band_profile = _derive_band_profile(user)
        missing_profile_fields = [
            field
            for field in BAND_APPLICATION_REQUIRED_SNAPSHOT_FIELDS
            if not str(band_profile.get(field) or "").strip()
        ]
        member_value = str(band_profile.get("members") or "").strip()
        if member_value.isdecimal() and int(member_value) < 1:
            missing_profile_fields.append("members")
        if missing_profile_fields:
            errors.append("ข้อมูลวงยังไม่ครบสำหรับสมัคร")

    event_id = str(payload.get("event_id") or "").strip()
    event = repo.get_event(event_id) if event_id else None
    if event is None or not event.get("registration_open", False):
        errors.append("ไม่พบอีเว้นต์ที่เปิดรับสมัคร")

    songs = payload.get("songs")
    if not isinstance(songs, list) or not songs:
        errors.append("ต้องระบุเพลงอย่างน้อย 1 เพลง")
    else:
        if len(songs) > BAND_APPLICATION_MAX_SONG_COUNT:
            errors.append(f"จำนวนเพลงต้องไม่เกิน {BAND_APPLICATION_MAX_SONG_COUNT} เพลง")
        for index, song in enumerate(songs, start=1):
            if not isinstance(song, dict):
                errors.append(f"ข้อมูลเพลงลำดับที่ {index} ไม่ถูกต้อง")
                continue
            song_name = str(song.get("song_name") or "").strip()
            song_type = str(song.get("song_type") or "").strip()
            if not song_name:
                errors.append(f"กรุณาระบุชื่อเพลงลำดับที่ {index}")
            if song_type not in {"ต้นฉบับ", "คัฟเวอร์"}:
                errors.append(f"กรุณาระบุประเภทเพลงลำดับที่ {index}")
            if song_type == "คัฟเวอร์" and not str(song.get("original_artist") or "").strip():
                errors.append(f"กรุณาระบุศิลปินเดิมของเพลงลำดับที่ {index}")

    total_duration = payload.get("total_duration_minutes")
    try:
        if isinstance(total_duration, bool):
            raise ValueError
        parsed_duration = int(total_duration)
        if isinstance(total_duration, float) and not total_duration.is_integer():
            raise ValueError
    except (TypeError, ValueError):
        parsed_duration = None
        errors.append("กรุณาระบุความยาวการแสดงรวมเป็นจำนวนนาที")
    else:
        if parsed_duration > BAND_APPLICATION_MAX_PERFORMANCE_MINUTES:
            errors.append(
                f"ความยาวการแสดงรวมต้องไม่เกิน {BAND_APPLICATION_MAX_PERFORMANCE_MINUTES} นาที"
            )

    is_valid = not errors
    return {
        "success": is_valid,
        "is_valid": is_valid,
        "errors": errors,
        "limits": {
            "max_performance_minutes": BAND_APPLICATION_MAX_PERFORMANCE_MINUTES,
            "max_song_count": BAND_APPLICATION_MAX_SONG_COUNT,
        },
        "message": "ข้อมูลใบสมัครถูกต้อง" if is_valid else "ข้อมูลใบสมัครไม่ถูกต้อง",
    }


def submit_band_application(
    *,
    session_id: str | None,
    payload: dict[str, Any],
    repository: AuthRepository | None = None,
) -> dict[str, Any]:
    """รองรับ FR-APP-04, ASM-03, ASM-06 และ NFR-PERF-01: ตรวจและบันทึกใบสมัคร"""
    repo = repository or AuthRepository()
    validation = validate_band_application(
        session_id=session_id,
        payload=payload,
        repository=repo,
    )
    if not validation["is_valid"]:
        return validation

    resolved_user_id, error = _resolve_band_context(
        session_id=session_id,
        user_id=None,
        repository=repo,
    )
    if resolved_user_id is None:
        return {
            "success": False,
            "is_valid": False,
            "errors": [error or "กรุณาเข้าสู่ระบบก่อนใช้งาน"],
            "message": "ไม่สามารถส่งใบสมัครได้",
        }

    user = repo.get_by_id(resolved_user_id)
    if user is None or str(user.get("role") or "").lower() != "band":
        return {
            "success": False,
            "is_valid": False,
            "errors": ["เฉพาะวงที่เข้าสู่ระบบแล้วจึงสามารถส่งใบสมัครได้"],
            "message": "ไม่สามารถส่งใบสมัครได้",
        }

    try:
        application = repo.create_band_application(
            band_id=resolved_user_id,
            event_id=str(payload.get("event_id") or ""),
            band_profile=_derive_band_profile(user),
            performance_data=payload,
        )
    except BandApplicationSaveError:
        return {
            "success": False,
            "message": "ส่งใบสมัครไม่สำเร็จ",
        }
    return {
        "success": True,
        "is_valid": True,
        "application": application,
        "status": application["status"],
        "message": "ส่งใบสมัครแล้ว",
    }


@router.get("/events/open")
@router.get("/api/events/open")
def events_open_endpoint(
    session_id: str | None = None,
    user_id: int | None = None,
) -> dict[str, Any]:
    return get_open_application_events(session_id=session_id, user_id=user_id)


@router.get("/bands/me/application-profile")
@router.get("/api/bands/me/application-profile")
def band_application_profile_endpoint(
    session_id: str | None = None,
) -> dict[str, Any]:
    """รองรับ NFR-SEC-01 และ Q-03: ต้องใช้ session ที่ยืนยันแล้วเพื่อเข้าถึงข้อมูลวง"""
    return get_band_application_profile(session_id=session_id)


@router.post("/applications/validate")
@router.post("/api/applications/validate")
def application_validate_endpoint(
    payload: dict[str, Any],
    session_id: str | None = None,
) -> dict[str, Any]:
    return validate_band_application(session_id=session_id, payload=payload)


@router.post("/applications")
@router.post("/api/applications")
def application_create_endpoint(
    payload: dict[str, Any],
    session_id: str | None = None,
) -> dict[str, Any]:
    """รองรับ FR-APP-04, ASM-03 และ ASM-06: บันทึกใบสมัครของวงที่เข้าสู่ระบบแล้ว"""
    return submit_band_application(session_id=session_id, payload=payload)


__all__ = [
    "router",
    "events_open_endpoint",
    "band_application_profile_endpoint",
    "application_validate_endpoint",
    "application_create_endpoint",
    "get_open_application_events",
    "get_band_application_profile",
    "validate_band_application",
    "submit_band_application",
]
