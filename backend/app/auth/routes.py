from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.auth.cancel import cancel_registration_for_user, get_active_registrations_for_user
from app.auth.permissions import get_user_permission_summary, require_permission
from app.auth.session import validate_session

# รองรับ PRE-REG-01 และ FR-AUTH-05: จัดเตรียมเส้นทางพื้นฐานสำหรับผู้ใช้ที่เข้าสู่ระบบแล้วและตรวจสิทธิ์
router = APIRouter()


class PermissionCheckInput(BaseModel):
    role: str
    permission: str


class CancelRegistrationInput(BaseModel):
    user_id: int
    registration_id: int
    session_id: str | None = None


class UserOnlyCancelRegistrationInput(BaseModel):
    user_id: int
    session_id: str | None = None


# รองรับ PRE-CXL-01, FR-CXL-01: มีเส้นทางพื้นฐานสำหรับผู้ใช้ที่เข้าสู่ระบบแล้วเปิดดูข้อมูลการลงทะเบียนของตนเอง
@router.get("/api/registration/ready")
def registration_ready_endpoint() -> dict[str, object]:
    return {
        "success": True,
        "ready": True,
        "message": "ระบบลงทะเบียนเข้าชมงานพร้อมใช้งาน",
    }


@router.get("/api/cancel-registration/ready")
def cancel_registration_ready_endpoint() -> dict[str, object]:
    return {
        "success": True,
        "ready": True,
        "message": "ระบบยกเลิกการลงทะเบียนพร้อมใช้งาน",
    }


@router.get("/api/cancel-registration/me")
def my_registrations_endpoint(user_id: int | None = None) -> dict[str, object]:
    if user_id is None:
        return {
            "success": False,
            "user_id": None,
            "registrations": [],
            "message": "ไม่พบข้อมูลการลงทะเบียน",
        }

    registrations = get_active_registrations_for_user(user_id)
    if not registrations:
        return {
            "success": False,
            "user_id": user_id,
            "registrations": [],
            "message": "ไม่พบข้อมูลการลงทะเบียน",
        }

    return {
        "success": True,
        "user_id": user_id,
        "registrations": registrations,
        "message": "พร้อมใช้งานสำหรับการยกเลิกข้อมูลลงทะเบียนของผู้ใช้",
    }


# รองรับ FR-CXL-03 และ NFR-DAT-01: ยืนยันการยกเลิกจากผู้ใช้และปรับสถานะ/จำนวนอีเว้นต์ทันที
@router.post("/api/cancel-registration/cancel")
def cancel_registration_endpoint(payload: CancelRegistrationInput) -> dict[str, object]:
    if payload.session_id:
        session = validate_session(payload.session_id)
        if session is None or int(session.get("user_id", -1)) != int(payload.user_id):
            return {
                "success": False,
                "user_id": payload.user_id,
                "registration_id": payload.registration_id,
                "message": "คุณไม่มีสิทธิ์ยกเลิกการลงทะเบียนนี้",
            }

    try:
        registration = cancel_registration_for_user(
            user_id=payload.user_id,
            registration_id=payload.registration_id,
        )
        return {
            "success": True,
            "user_id": payload.user_id,
            "registration_id": payload.registration_id,
            "registration": registration,
            "message": "ยกเลิกการลงทะเบียนสำเร็จ",
        }
    except PermissionError:
        return {
            "success": False,
            "user_id": payload.user_id,
            "registration_id": payload.registration_id,
            "message": "คุณไม่มีสิทธิ์ยกเลิกการลงทะเบียนนี้",
        }
    except ValueError:
        return {
            "success": False,
            "user_id": payload.user_id,
            "registration_id": payload.registration_id,
            "message": "ไม่พบข้อมูลการลงทะเบียน",
        }


@router.post("/api/cancel-registration/{registration_id}/cancel")
def cancel_registration_by_path_endpoint(
    registration_id: int,
    payload: UserOnlyCancelRegistrationInput,
) -> dict[str, object]:
    if payload.session_id:
        session = validate_session(payload.session_id)
        if session is None or int(session.get("user_id", -1)) != int(payload.user_id):
            return {
                "success": False,
                "user_id": payload.user_id,
                "registration_id": registration_id,
                "message": "คุณไม่มีสิทธิ์ยกเลิกการลงทะเบียนนี้",
            }

    try:
        registration = cancel_registration_for_user(
            user_id=payload.user_id,
            registration_id=registration_id,
        )
        return {
            "success": True,
            "user_id": payload.user_id,
            "registration_id": registration_id,
            "registration": registration,
            "message": "ยกเลิกการลงทะเบียนสำเร็จ",
        }
    except PermissionError:
        return {
            "success": False,
            "user_id": payload.user_id,
            "registration_id": registration_id,
            "message": "คุณไม่มีสิทธิ์ยกเลิกการลงทะเบียนนี้",
        }
    except ValueError:
        return {
            "success": False,
            "user_id": payload.user_id,
            "registration_id": registration_id,
            "message": "ไม่พบข้อมูลการลงทะเบียน",
        }


@router.post("/api/auth/permissions/check")
def check_permission_endpoint(payload: PermissionCheckInput) -> dict[str, object]:
    try:
        require_permission(payload.role, payload.permission)
        return {
            "success": True,
            "allowed": True,
            "role": payload.role,
            "permission": payload.permission,
        }
    except PermissionError:
        return {
            "success": False,
            "allowed": False,
            "role": payload.role,
            "permission": payload.permission,
            "message": "คุณไม่มีสิทธิ์ดำเนินการนี้",
        }


@router.get("/api/auth/me")
def me_endpoint(role: str | None = None) -> dict[str, object]:
    return {
        "success": True,
        "user": {
            "role": role,
            "permissions": get_user_permission_summary({"role": role})["permissions"],
        },
    }


__all__ = [
    "router",
    "check_permission_endpoint",
    "me_endpoint",
    "registration_ready_endpoint",
    "cancel_registration_ready_endpoint",
    "my_registrations_endpoint",
    "cancel_registration_endpoint",
    "cancel_registration_by_path_endpoint",
    "PermissionCheckInput",
    "CancelRegistrationInput",
    "UserOnlyCancelRegistrationInput",
]
