import pytest
from fastapi.testclient import TestClient

from app.auth.repository import AuthRepository
from app.auth.session import create_session, reset_sessions
from app.main import app


@pytest.fixture(autouse=True)
def clear_application_state():
    repo = AuthRepository()
    repo.reset()
    reset_sessions()
    yield
    repo.reset()
    reset_sessions()


def create_band_context():
    repo = AuthRepository()
    band = repo.create_user(
        email="application-duplicate@ku.th",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Moonlight Band",
        role="band",
        profile={
            "band_name": "Moonlight Band",
            "genre": "Indie Pop",
            "members": "นักร้องและกีตาร์, กลอง, เบส",
            "contact_name": "ผู้ติดต่อ",
            "contact_phone": "089-876-5432",
        },
    )
    session = create_session(band["id"], role="band")
    event = repo.seed_open_band_application_events()[0]
    return repo, session["session_id"], event["event_id"]


# รองรับ Q-01: วงสมัครอีเว้นต์เดียวกันซ้ำได้
def test_T_11_allows_repeated_application_for_same_event():
    repo, session_id, event_id = create_band_context()
    client = TestClient(app)
    payload = {
        "event_id": event_id,
        "songs": [{"song_name": "เพลงต้นฉบับ", "song_type": "ต้นฉบับ"}],
        "total_duration_minutes": 20,
    }

    first_response = client.post(
        f"/api/applications?session_id={session_id}",
        json=payload,
    )
    second_response = client.post(
        f"/api/applications?session_id={session_id}",
        json=payload,
    )

    first_application = first_response.json()["application"]
    second_application = second_response.json()["application"]
    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.json()["success"] is True
    assert second_response.json()["success"] is True
    assert first_application["event_id"] == event_id
    assert second_application["event_id"] == event_id
    assert first_application["application_id"] != second_application["application_id"]
    assert repo.get_band_application(first_application["application_id"]) is not None
    assert repo.get_band_application(second_application["application_id"]) is not None
