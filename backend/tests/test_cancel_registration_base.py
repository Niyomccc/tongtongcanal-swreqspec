from fastapi.testclient import TestClient

from app.auth.repository import AuthRepository
from app.config import REGISTRATION_STATUS_CANCELLED, REGISTRATION_STATUS_REGISTERED
from app.main import app


def test_T_01_cancel_registration_base_routes():
    repo = AuthRepository()
    repo.reset()
    user = repo.create_user(
        email="base@example.com",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Base User",
        role="audience",
        profile={"phone_number": "0812345670"},
    )
    event = repo.create_event(event_id="evt-base", capacity=5, registration_open=True, remaining_seats=4)
    repo.register_for_event(user_id=user["id"], event_id=event["event_id"])

    client = TestClient(app)

    root = client.get("/")
    assert root.status_code == 200
    assert root.json()["status"] == "ok"

    ready = client.get("/api/cancel-registration/ready")
    assert ready.status_code == 200
    assert ready.json()["success"] is True
    assert ready.json()["ready"] is True

    my_registrations = client.get("/api/cancel-registration/me", params={"user_id": user["id"]})
    assert my_registrations.status_code == 200
    payload = my_registrations.json()
    assert payload["success"] is True
    assert payload["user_id"] == user["id"]
    assert isinstance(payload["registrations"], list)
    assert len(payload["registrations"]) == 1


def test_AC_CXL_01_list_active_registrations_for_user():
    repo = AuthRepository()
    repo.reset()
    user = repo.create_user(
        email="user@example.com",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Alice",
        role="audience",
        profile={"phone_number": "0812345678"},
    )
    event = repo.create_event(event_id="evt-cxl-1", capacity=10, registration_open=True, remaining_seats=9)
    repo.register_for_event(user_id=user["id"], event_id=event["event_id"])

    client = TestClient(app)
    response = client.get("/api/cancel-registration/me", params={"user_id": user["id"]})

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["user_id"] == user["id"]
    assert len(payload["registrations"]) == 1
    assert payload["registrations"][0]["status"] == REGISTRATION_STATUS_REGISTERED
    assert payload["registrations"][0]["event_id"] == event["event_id"]


def test_AC_CXL_05_reject_when_no_active_registration_exists():
    repo = AuthRepository()
    repo.reset()
    user = repo.create_user(
        email="noactive@example.com",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Bob",
        role="audience",
        profile={"phone_number": "0812345679"},
    )
    event = repo.create_event(event_id="evt-cxl-2", capacity=10, registration_open=True, remaining_seats=9)
    repo.register_for_event(user_id=user["id"], event_id=event["event_id"])
    repo._registrations_by_key[(user["id"], event["event_id"])]["status"] = REGISTRATION_STATUS_CANCELLED

    client = TestClient(app)
    response = client.get("/api/cancel-registration/me", params={"user_id": user["id"]})

    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is False
    assert payload["registrations"] == []
    assert payload["message"] == "ไม่พบข้อมูลการลงทะเบียน"
