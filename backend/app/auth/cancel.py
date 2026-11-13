from __future__ import annotations

from typing import Any

from app.auth.repository import AuthRepository
from app.config import REGISTRATION_STATUS_REGISTERED


# รองรับ PRE-CXL-01, FR-CXL-01 และ FR-CXL-05: ดึงข้อมูลการลงทะเบียนที่ยังเปิดใช้งานสำหรับผู้ใช้
def get_active_registrations_for_user(
    user_id: int,
    *,
    repository: AuthRepository | None = None,
) -> list[dict[str, Any]]:
    repo = repository or AuthRepository()
    return [
        registration
        for registration in repo.list_registrations_for_user(user_id)
        if registration.get("status") == REGISTRATION_STATUS_REGISTERED
    ]


# รองรับ FR-CXL-03, NFR-DAT-01 และ Q-05: เปลี่ยนสถานะการลงทะเบียนเป็นยกเลิกและปรับจำนวนผู้ลงทะเบียนภายใต้ transaction เดียวใน repository
# เพื่อให้ทั้ง `Registration.status` และ `Event.registered_count` อัปเดตพร้อมกันหรือไม่เกิดอะไรเลย

def cancel_registration_for_user(
    *,
    user_id: int,
    registration_id: int,
    repository: AuthRepository | None = None,
) -> dict[str, Any]:
    repo = repository or AuthRepository()
    return repo.cancel_registration_for_user(user_id=user_id, registration_id=registration_id)


# รองรับ PRE-CXL-01, FR-CXL-01 และ FR-CXL-05: ตรวจว่า registration ที่เลือกเป็นของผู้ใช้คนนี้จริง
def is_registration_owned_by_user(
    *,
    user_id: int,
    registration_id: int,
    repository: AuthRepository | None = None,
) -> bool:
    repo = repository or AuthRepository()
    registration = repo.get_registration_by_id(registration_id)
    return bool(registration and int(registration.get("user_id")) == int(user_id))
