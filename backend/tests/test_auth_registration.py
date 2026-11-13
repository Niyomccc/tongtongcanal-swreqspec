from __future__ import annotations

import threading

import pytest

from app.auth.register import get_event_availability, register_for_event, register_user
from app.auth.repository import AuthRepository
from app.config import EVENT_REGISTRATION_LOW_SEAT_THRESHOLD


@pytest.fixture(autouse=True)
def clear_repository():
    repo = AuthRepository()
    repo.reset()
    yield
    repo.reset()


def test_AC_AUTH_01_register_success():
    payload = {
        "email": "student01@ku.th",
        "password": "P@ssword123",
        "confirmPassword": "P@ssword123",
        "role": "นักศึกษา",
        "fullNameOrBandName": "นางสาวสมใจ รักเรียน",
        "studentId": "65123456",
        "universityCode": "KU",
    }

    result = register_user(payload)

    assert result["success"] is True
    assert result["redirectTo"] == "/dashboard"
    assert result["user"]["role"] == "student"
    assert result["user"]["email"] == "student01@ku.th"
    assert result["profile"]["student_id"] == "65123456"
    assert result["user"]["full_name_or_band_name"] == "นางสาวสมใจ รักเรียน"

    saved = AuthRepository().get_by_email("student01@ku.th")
    assert saved is not None
    assert saved["password_hash"] != payload["password"]
    assert saved["salt"]
    assert saved["profile"]["student_id"] == "65123456"
    assert saved["role"] == "student"


def test_AUTH_registration_rejects_public_admin_roles():
    with pytest.raises(ValueError, match="ไม่อนุญาต"):
        register_user(
            {
                "email": "admin@ku.th",
                "password": "P@ssword123",
                "confirmPassword": "P@ssword123",
                "role": "admin",
                "fullNameOrBandName": "ผู้ดูแล",
            }
        )

    with pytest.raises(ValueError, match="ไม่อนุญาต"):
        register_user(
            {
                "email": "organizer@ku.th",
                "password": "P@ssword123",
                "confirmPassword": "P@ssword123",
                "role": "organizer",
                "fullNameOrBandName": "ผู้จัดงาน",
            }
        )


def test_AC_REG_01_register_available_event():
    repo = AuthRepository()
    user = repo.create_user(
        email="audience01@ku.th",
        password_hash="hashed",
        salt="salt",
        full_name_or_band_name="ผู้ชมคนแรก",
        role="audience",
        profile={"phone_number": "0812345678"},
    )
    event = repo.create_event(event_id="evt-01", capacity=3, registration_open=True)

    result = register_for_event(
        {
            "user_id": user["id"],
            "event_id": event["event_id"],
            "confirmation_snapshot": {"ticket_type": "general"},
        },
        repository=repo,
    )

    assert result["success"] is True
    assert result["registration"]["event_id"] == "evt-01"
    assert result["registration"]["user_id"] == user["id"]
    assert repo.get_event("evt-01")["remaining_seats"] == 2


def test_AC_REG_02_store_confirmed_registration_data():
    repo = AuthRepository()
    user = repo.create_user(
        email="audience02@ku.th",
        password_hash="hashed",
        salt="salt",
        full_name_or_band_name="ผู้ชมคนสอง",
        role="audience",
        profile={"phone_number": "0898765432"},
    )
    event = repo.create_event(event_id="evt-02", capacity=2, registration_open=True)

    payload = {
        "user_id": user["id"],
        "event_id": event["event_id"],
        "confirmation_snapshot": {
            "email": user["email"],
            "role": user["role"],
            "full_name_or_band_name": user["full_name_or_band_name"],
            "ticket_type": "student",
        },
    }

    register_for_event(payload, repository=repo)
    saved = repo.get_registration(user_id=user["id"], event_id=event["event_id"])

    assert saved is not None
    assert saved["confirmation_snapshot"]["email"] == user["email"]
    assert saved["confirmation_snapshot"]["role"] == user["role"]
    assert saved["confirmation_snapshot"]["full_name_or_band_name"] == user["full_name_or_band_name"]
    assert saved["confirmation_snapshot"]["ticket_type"] == "student"


def test_AC_REG_03_show_remaining_seats_when_below_threshold():
    repo = AuthRepository()
    event = repo.create_event(
        event_id="evt-03-low",
        capacity=20,
        registration_open=True,
        remaining_seats=EVENT_REGISTRATION_LOW_SEAT_THRESHOLD,
    )

    availability = get_event_availability(event["event_id"], repository=repo)

    assert availability["remaining_seats"] == EVENT_REGISTRATION_LOW_SEAT_THRESHOLD
    assert availability["low_seat_warning"] is True
    assert availability["warning_message"] == f"เหลือที่นั่งไม่เกิน {EVENT_REGISTRATION_LOW_SEAT_THRESHOLD} ที่นั่ง"


def test_AC_REG_04_reject_duplicate_registration():
    repo = AuthRepository()
    user = repo.create_user(
        email="audience03@ku.th",
        password_hash="hashed",
        salt="salt",
        full_name_or_band_name="ผู้ชมคนสาม",
        role="audience",
        profile={"phone_number": "0810000003"},
    )
    event = repo.create_event(event_id="evt-03", capacity=2, registration_open=True)

    payload = {
        "user_id": user["id"],
        "event_id": event["event_id"],
        "confirmation_snapshot": {"ticket_type": "general"},
    }

    first = register_for_event(payload, repository=repo)
    assert first["success"] is True

    with pytest.raises(ValueError, match="ลงทะเบียนซ้ำไม่ได้"):
        register_for_event(payload, repository=repo)

    saved = repo.get_registration(user_id=user["id"], event_id=event["event_id"])
    assert saved is not None
    assert saved["registration_id"] == first["registration"]["registration_id"]
    assert repo.get_event(event["event_id"])["remaining_seats"] == 1


def test_AC_REG_05_reject_full_event_and_race_for_last_seat():
    repo = AuthRepository()
    event = repo.create_event(event_id="evt-05", capacity=1, registration_open=True)

    first_user = repo.create_user(
        email="audience05a@ku.th",
        password_hash="hashed",
        salt="salt",
        full_name_or_band_name="ผู้ชมคนแรก",
        role="audience",
        profile={"phone_number": "0810000005"},
    )
    second_user = repo.create_user(
        email="audience05b@ku.th",
        password_hash="hashed",
        salt="salt",
        full_name_or_band_name="ผู้ชมคนที่สอง",
        role="audience",
        profile={"phone_number": "0810000006"},
    )

    first = register_for_event(
        {
            "user_id": first_user["id"],
            "event_id": event["event_id"],
            "confirmation_snapshot": {"ticket_type": "general"},
        },
        repository=repo,
    )
    assert first["success"] is True
    assert repo.get_event(event["event_id"])["remaining_seats"] == 0

    with pytest.raises(ValueError, match="ที่นั่งเต็ม"):
        register_for_event(
            {
                "user_id": second_user["id"],
                "event_id": event["event_id"],
                "confirmation_snapshot": {"ticket_type": "general"},
            },
            repository=repo,
        )

    race_event = repo.create_event(event_id="evt-05-race", capacity=1, registration_open=True)
    barrier = threading.Barrier(2)
    successes: list[dict[str, object]] = []
    failures: list[str] = []

    def attempt_registration(user_id: int) -> None:
        barrier.wait()
        try:
            result = register_for_event(
                {
                    "user_id": user_id,
                    "event_id": race_event["event_id"],
                    "confirmation_snapshot": {"ticket_type": "general"},
                },
                repository=repo,
            )
            successes.append(result)
        except ValueError as exc:
            failures.append(str(exc))

    third_user = repo.create_user(
        email="audience05c@ku.th",
        password_hash="hashed",
        salt="salt",
        full_name_or_band_name="ผู้ชมคนที่สาม",
        role="audience",
        profile={"phone_number": "0810000007"},
    )
    fourth_user = repo.create_user(
        email="audience05d@ku.th",
        password_hash="hashed",
        salt="salt",
        full_name_or_band_name="ผู้ชมคนที่สี่",
        role="audience",
        profile={"phone_number": "0810000008"},
    )

    threads = [
        threading.Thread(target=attempt_registration, args=(third_user["id"],)),
        threading.Thread(target=attempt_registration, args=(fourth_user["id"],)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(successes) == 1
    assert len(failures) == 1
    assert "ที่นั่งเต็ม" in failures[0]
    assert repo.get_event(race_event["event_id"])["remaining_seats"] == 0
