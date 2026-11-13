import pytest
from fastapi.testclient import TestClient

from app.auth.repository import AuthRepository
from app.auth.session import create_session, reset_sessions
from app.config import BAND_APPLICATION_MAX_PERFORMANCE_MINUTES, BAND_APPLICATION_MAX_SONG_COUNT
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
        email="application-rejection@ku.th",
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


def valid_payload(event_id: str) -> dict:
    return {
        "event_id": event_id,
        "songs": [{"song_name": "เพลงต้นฉบับ", "song_type": "ต้นฉบับ"}],
        "total_duration_minutes": BAND_APPLICATION_MAX_PERFORMANCE_MINUTES,
    }


def assert_application_was_not_saved(repo: AuthRepository, response) -> None:
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["is_valid"] is False
    assert repo.get_band_application(1) is None
    assert repo.get_band_snapshot(1) is None


# รองรับ AC-APP-04: ข้อมูลบังคับไม่ครบต้องถูกปฏิเสธและไม่สร้างใบสมัคร
def test_AC_APP_04_rejects_incomplete_submission_without_saving():
    repo, session_id, event_id = create_band_context()
    payload = valid_payload(event_id)
    payload["songs"] = []

    response = TestClient(app).post(
        f"/api/applications?session_id={session_id}",
        json=payload,
    )

    assert_application_was_not_saved(repo, response)
    assert any("อย่างน้อย 1 เพลง" in error for error in response.json()["errors"])


# รองรับ AC-APP-04: ความยาวการแสดงเกินค่าที่กำหนดต้องถูกปฏิเสธและไม่สร้างใบสมัคร
def test_AC_APP_04_rejects_over_duration_submission_without_saving():
    repo, session_id, event_id = create_band_context()
    payload = valid_payload(event_id)
    payload["total_duration_minutes"] = BAND_APPLICATION_MAX_PERFORMANCE_MINUTES + 1

    response = TestClient(app).post(
        f"/api/applications?session_id={session_id}",
        json=payload,
    )

    assert_application_was_not_saved(repo, response)
    assert any("ความยาวการแสดงรวม" in error for error in response.json()["errors"])


# รองรับ AC-APP-04: จำนวนเพลงเกินค่าที่กำหนดต้องถูกปฏิเสธและไม่สร้างใบสมัคร
def test_AC_APP_04_rejects_over_song_count_submission_without_saving():
    repo, session_id, event_id = create_band_context()
    payload = valid_payload(event_id)
    payload["songs"] = [
        {"song_name": f"เพลง {index}", "song_type": "ต้นฉบับ"}
        for index in range(BAND_APPLICATION_MAX_SONG_COUNT + 1)
    ]

    response = TestClient(app).post(
        f"/api/applications?session_id={session_id}",
        json=payload,
    )

    assert_application_was_not_saved(repo, response)
    assert any("จำนวนเพลง" in error for error in response.json()["errors"])
