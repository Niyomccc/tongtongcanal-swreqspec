from fastapi.testclient import TestClient

from app.auth.repository import AuthRepository
from app.auth.session import create_session, reset_sessions
from app.config import REGISTRATION_STATUS_CANCELLED, REGISTRATION_STATUS_REGISTERED
from app.main import app


def test_AC_CXL_02_change_registration_status_to_cancelled():
    repo = AuthRepository()
    repo.reset()
    user = repo.create_user(
        email="cancel-user@example.com",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Cancel User",
        role="audience",
        profile={"phone_number": "0810000001"},
    )
    event = repo.create_event(event_id="evt-cxl-cancel", capacity=5, registration_open=True, remaining_seats=4)
    registration = repo.register_for_event(user_id=user["id"], event_id=event["event_id"])

    client = TestClient(app)
    response = client.post(
        "/api/cancel-registration/cancel",
        json={"user_id": user["id"], "registration_id": registration["registration_id"]},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["message"] == "ยกเลิกการลงทะเบียนสำเร็จ"

    refreshed_registration = repo.get_registration_by_id(registration["registration_id"])
    assert refreshed_registration is not None
    assert refreshed_registration["status"] == REGISTRATION_STATUS_CANCELLED
    assert repo.get_event(event["event_id"])["registered_count"] == 0


def test_AC_CXL_03_update_event_registration_count():
    repo = AuthRepository()
    repo.reset()
    users = []
    for index in range(3):
        user = repo.create_user(
            email=f"count-{index}@example.com",
            password_hash="hash",
            salt="salt",
            full_name_or_band_name=f"Attendee {index}",
            role="audience",
            profile={"phone_number": f"081000000{index + 2}"},
        )
        users.append(user)

    event = repo.create_event(event_id="evt-cxl-count", capacity=5, registration_open=True, remaining_seats=5)
    registrations = [repo.register_for_event(user_id=user["id"], event_id=event["event_id"]) for user in users]

    client = TestClient(app)
    response = client.post(
        "/api/cancel-registration/cancel",
        json={"user_id": users[0]["id"], "registration_id": registrations[0]["registration_id"]},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True

    refreshed_event = repo.get_event(event["event_id"])
    assert refreshed_event["registered_count"] == 2
    assert refreshed_event["remaining_seats"] == 3


def test_AC_CXL_05_reject_cancellation_when_registration_not_found():
    repo = AuthRepository()
    repo.reset()
    user = repo.create_user(
        email="missing-reg@example.com",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Missing Reg",
        role="audience",
        profile={"phone_number": "0810000010"},
    )
    event = repo.create_event(event_id="evt-cxl-missing", capacity=5, registration_open=True, remaining_seats=5)
    repo.register_for_event(user_id=user["id"], event_id=event["event_id"])

    client = TestClient(app)
    response = client.post(
        "/api/cancel-registration/cancel",
        json={"user_id": user["id"], "registration_id": 999},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is False
    assert payload["message"] == "ไม่พบข้อมูลการลงทะเบียน"

    refreshed_event = repo.get_event(event["event_id"])
    assert refreshed_event["registered_count"] == 1
    assert refreshed_event["remaining_seats"] == 4


def test_T_09_atomic_status_and_count_update():
    repo = AuthRepository()
    repo.reset()
    user = repo.create_user(
        email="atomic-cancel@example.com",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Atomic User",
        role="audience",
        profile={"phone_number": "0810000011"},
    )
    event = repo.create_event(event_id="evt-cxl-atomic", capacity=4, registration_open=True, remaining_seats=3)
    registration = repo.register_for_event(user_id=user["id"], event_id=event["event_id"])
    repo.register_for_event(user_id=repo.create_user(
        email="atomic-2@example.com",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Atomic User 2",
        role="audience",
        profile={"phone_number": "0810000012"},
    )["id"], event_id=event["event_id"])

    client = TestClient(app)
    response = client.post(
        "/api/cancel-registration/cancel",
        json={"user_id": user["id"], "registration_id": registration["registration_id"]},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["message"] == "ยกเลิกการลงทะเบียนสำเร็จ"

    refreshed_registration = repo.get_registration_by_id(registration["registration_id"])
    refreshed_event = repo.get_event(event["event_id"])
    assert refreshed_registration["status"] == REGISTRATION_STATUS_CANCELLED
    assert refreshed_event["registered_count"] == 1
    assert refreshed_event["remaining_seats"] == 3


def test_T_10_tracks_cancelled_audit_metadata_and_current_count():
    repo = AuthRepository()
    repo.reset()
    user = repo.create_user(
        email="audit-user@example.com",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Audit User",
        role="audience",
        profile={"phone_number": "0810000025"},
    )
    event = repo.create_event(event_id="evt-cxl-audit", capacity=4, registration_open=True, remaining_seats=3)
    registration = repo.register_for_event(user_id=user["id"], event_id=event["event_id"])

    cancelled = repo.cancel_registration_for_user(user_id=user["id"], registration_id=registration["registration_id"])

    assert cancelled["user_id"] == user["id"]
    assert cancelled["event_id"] == event["event_id"]
    assert cancelled["cancelled_at"] is not None
    assert cancelled["registered_count"] == 0
    assert repo.get_event(event["event_id"])["registered_count"] == 0


def test_T_08_rejects_ownership_mismatch_after_session_validation():
    repo = AuthRepository()
    repo.reset()
    reset_sessions()

    owner = repo.create_user(
        email="owner@example.com",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Owner User",
        role="audience",
        profile={"phone_number": "0810000020"},
    )
    other_user = repo.create_user(
        email="other@example.com",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Other User",
        role="audience",
        profile={"phone_number": "0810000021"},
    )
    event = repo.create_event(event_id="evt-cxl-owner", capacity=5, registration_open=True, remaining_seats=4)
    registration = repo.register_for_event(user_id=owner["id"], event_id=event["event_id"])
    session = create_session(owner["id"], session_id="session-owner")

    client = TestClient(app)
    response = client.post(
        "/api/cancel-registration/cancel",
        json={"user_id": other_user["id"], "registration_id": registration["registration_id"], "session_id": session["session_id"]},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is False
    assert payload["message"] == "คุณไม่มีสิทธิ์ยกเลิกการลงทะเบียนนี้"

    refreshed = repo.get_registration_by_id(registration["registration_id"])
    assert refreshed["status"] == REGISTRATION_STATUS_REGISTERED
