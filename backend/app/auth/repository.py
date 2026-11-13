from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock
from typing import Any

from app.config import REGISTRATION_STATUS_REGISTERED


# รองรับ FR-AUTH-02, FR-AUTH-03, FR-AUTH-05, FR-REG-02, FR-REG-04, FR-REG-05 และ NFR-SEC-01
class AuthRepository:
    """คลังข้อมูลบัญชีผู้ใช้แบบในหน่วยความจำสำหรับ API สมัครสมาชิก"""

    _instance: "AuthRepository | None" = None
    _lock = RLock()

    def __new__(cls) -> "AuthRepository":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized"):
            return

        self._initialized = True
        self._users_by_email: dict[str, dict[str, Any]] = {}
        self._users_by_id: dict[int, dict[str, Any]] = {}
        self._student_ids: dict[str, int] = {}
        self._band_names: dict[str, int] = {}
        self._events: dict[str, dict[str, Any]] = {}
        self._registrations_by_key: dict[tuple[int, str], dict[str, Any]] = {}
        self._next_user_id = 1
        self._next_registration_id = 1

    def reset(self) -> None:
        self._users_by_email.clear()
        self._users_by_id.clear()
        self._student_ids.clear()
        self._band_names.clear()
        self._events.clear()
        self._registrations_by_key.clear()
        self._next_user_id = 1
        self._next_registration_id = 1

    def create_user(
        self,
        *,
        email: str,
        password_hash: str,
        salt: str,
        full_name_or_band_name: str,
        role: str,
        profile: dict[str, Any],
    ) -> dict[str, Any]:
        normalized_email = email.strip().lower()
        if self._users_by_email.get(normalized_email):
            raise ValueError("อีเมลนี้มีผู้ใช้อยู่แล้ว")

        role = role.strip().lower()
        if role == "student":
            student_id = str(profile.get("student_id") or "").strip()
            if not student_id:
                raise ValueError("ต้องระบุรหัสนักศึกษา")
            if student_id in self._student_ids:
                raise ValueError("รหัสนักศึกษานี้มีผู้ใช้อยู่แล้ว")
            self._student_ids[student_id] = self._next_user_id
        elif role == "band":
            band_name = str(profile.get("band_name") or "").strip()
            if not band_name:
                raise ValueError("ต้องระบุชื่อวง")
            if band_name.lower() in {name.lower() for name in self._band_names}:
                raise ValueError("ชื่อวงนี้มีผู้ใช้อยู่แล้ว")
            self._band_names[band_name.lower()] = self._next_user_id

        user_id = self._next_user_id
        self._next_user_id += 1

        user_record: dict[str, Any] = {
            "id": user_id,
            "email": normalized_email,
            "password_hash": password_hash,
            "salt": salt,
            "full_name_or_band_name": full_name_or_band_name.strip(),
            "role": role,
            "status": "active",
            "created_at": None,
            "profile": profile,
        }

        self._users_by_email[normalized_email] = user_record
        self._users_by_id[user_id] = user_record
        return user_record

    def create_event(
        self,
        *,
        event_id: str,
        capacity: int,
        registration_open: bool = True,
        remaining_seats: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        normalized_event_id = str(event_id).strip()
        if not normalized_event_id:
            raise ValueError("ต้องระบุรหัสอีเว้นต์")
        if capacity <= 0:
            raise ValueError("ความจุของอีเว้นต์ต้องมากกว่า 0")

        event_record = {
            "event_id": normalized_event_id,
            "capacity": int(capacity),
            "registration_open": bool(registration_open),
            "remaining_seats": int(remaining_seats if remaining_seats is not None else capacity),
            "registered_count": 0,
            "metadata": dict(metadata or {}),
        }
        self._events[normalized_event_id] = event_record
        return event_record

    def get_event(self, event_id: str) -> dict[str, Any] | None:
        return self._events.get(str(event_id).strip())

    def register_for_event(
        self,
        *,
        user_id: int,
        event_id: str,
        confirmation_snapshot: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        with self._lock:
            event = self.get_event(event_id)
            if event is None:
                raise ValueError("ไม่พบอีเว้นต์ที่เลือก")
            if not event.get("registration_open", False):
                raise ValueError("อีเว้นต์นี้ปิดรับลงทะเบียน")

            key = (int(user_id), str(event_id).strip())
            if key in self._registrations_by_key:
                raise ValueError("ผู้ใช้นี้ได้ลงทะเบียนอีเว้นต์นี้แล้ว")
            if event.get("remaining_seats", 0) <= 0:
                raise ValueError("ที่นั่งเต็ม")

            user = self.get_by_id(int(user_id))
            if user is None:
                raise ValueError("ไม่พบผู้ใช้")

            snapshot = {
                "user_id": int(user_id),
                "email": user.get("email"),
                "role": user.get("role"),
                "full_name_or_band_name": user.get("full_name_or_band_name"),
                "profile": user.get("profile") or {},
            }
            if confirmation_snapshot:
                snapshot.update(confirmation_snapshot)

            registration_record = {
                "registration_id": self._next_registration_id,
                "event_id": str(event_id).strip(),
                "user_id": int(user_id),
                "status": REGISTRATION_STATUS_REGISTERED,
                "confirmation_snapshot": snapshot,
            }
            self._next_registration_id += 1
            self._registrations_by_key[key] = registration_record
            event["remaining_seats"] = max(0, int(event.get("remaining_seats", 0)) - 1)
            event["registered_count"] = int(event.get("registered_count", 0)) + 1
            return registration_record

    def get_registration(self, *, user_id: int, event_id: str) -> dict[str, Any] | None:
        return self._registrations_by_key.get((int(user_id), str(event_id).strip()))

    def get_registration_by_id(self, registration_id: int) -> dict[str, Any] | None:
        for registration in self._registrations_by_key.values():
            if int(registration.get("registration_id")) == int(registration_id):
                return registration
        return None

    def list_registrations_for_user(self, user_id: int) -> list[dict[str, Any]]:
        items = []
        for registration in self._registrations_by_key.values():
            if int(registration.get("user_id")) != int(user_id):
                continue

            enriched = dict(registration)
            event = self.get_event(enriched.get("event_id"))
            if event is not None:
                enriched["registered_count"] = int(event.get("registered_count", 0))
                enriched["remaining_seats"] = int(event.get("remaining_seats", 0))
            items.append(enriched)
        return sorted(items, key=lambda item: int(item.get("registration_id", 0)))

    def cancel_registration_for_user(self, *, user_id: int, registration_id: int) -> dict[str, Any]:
        """รองรับ FR-CXL-03, NFR-DAT-01, Q-04, Q-05 และ Q-07: ตรวจเจ้าของรายการและอัปเดตสถานะ/จำนวนผู้ลงทะเบียนพร้อมบันทึก timestamp ยกเลิกใน transaction เดียวภายใต้ lock เดียวกัน"""
        with self._lock:
            registration = self.get_registration_by_id(int(registration_id))
            if registration is None:
                raise ValueError("ไม่พบข้อมูลการลงทะเบียน")
            if int(registration.get("user_id")) != int(user_id):
                raise PermissionError("คุณไม่มีสิทธิ์ยกเลิกการลงทะเบียนนี้")
            if registration.get("status") != REGISTRATION_STATUS_REGISTERED:
                raise ValueError("ไม่พบข้อมูลการลงทะเบียน")

            event = self.get_event(registration.get("event_id"))
            if event is None:
                raise ValueError("ไม่พบข้อมูลการลงทะเบียน")

            updated_count = max(0, int(event.get("registered_count", 0)) - 1)
            registration["status"] = "ยกเลิก"
            registration["cancelled_at"] = datetime.now(timezone.utc).isoformat()
            registration["registered_count"] = updated_count
            registration["remaining_seats"] = max(0, int(event.get("capacity", 0)) - updated_count)

            event["registered_count"] = updated_count
            event["remaining_seats"] = max(0, int(event.get("capacity", 0)) - updated_count)
            return registration

    def get_by_email(self, email: str) -> dict[str, Any] | None:
        return self._users_by_email.get(email.strip().lower())

    def get_by_id(self, user_id: int) -> dict[str, Any] | None:
        return self._users_by_id.get(user_id)

    def get_by_student_id(self, student_id: str) -> dict[str, Any] | None:
        user_id = self._student_ids.get(student_id.strip())
        if user_id is None:
            return None
        return self._users_by_id.get(user_id)

    def get_by_band_name(self, band_name: str) -> dict[str, Any] | None:
        user_id = self._band_names.get(band_name.strip().lower())
        if user_id is None:
            return None
        return self._users_by_id.get(user_id)
