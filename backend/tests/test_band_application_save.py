import pytest
from fastapi.testclient import TestClient

from app.auth.application import submit_band_application
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
        email="application@ku.th",
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
    return repo, band, session["session_id"], event["event_id"]


def valid_payload(event_id: str) -> dict:
    return {
        "event_id": event_id,
        "songs": [
            {"song_name": "เพลงต้นฉบับ", "song_type": "ต้นฉบับ"},
            {
                "song_name": "เพลงคัฟเวอร์",
                "song_type": "คัฟเวอร์",
                "original_artist": "ศิลปินเดิม",
            },
        ],
        "total_duration_minutes": 20,
        "equipment_requirements": "ไมโครโฟน",
        "work_sample_link": "https://example.test/sample",
        "notes": "หมายเหตุ",
    }


def test_AC_APP_01_create_application_for_selected_event():
    repo, _, session_id, event_id = create_band_context()

    response = TestClient(app).post(
        f"/api/applications?session_id={session_id}",
        json=valid_payload(event_id),
    )
    result = response.json()

    assert response.status_code == 200
    assert result["success"] is True
    assert result["application"]["event_id"] == event_id
    assert repo.get_band_application(result["application"]["application_id"]) == result["application"]


def test_AC_APP_02_store_band_snapshot_and_performance_data():
    repo, band, session_id, event_id = create_band_context()

    result = submit_band_application(
        session_id=session_id,
        payload=valid_payload(event_id),
        repository=repo,
    )
    application = result["application"]

    band["profile"]["genre"] = "แนวเพลงใหม่"
    saved = repo.get_band_application(application["application_id"])
    snapshot = repo.get_band_snapshot(application["snapshot_id"])
    assert saved["band_snapshot"]["genre"] == "Indie Pop"
    assert snapshot["genre"] == "Indie Pop"
    assert saved["songs"] == [
        {"song_name": "เพลงต้นฉบับ", "song_type": "ต้นฉบับ", "original_artist": None},
        {"song_name": "เพลงคัฟเวอร์", "song_type": "คัฟเวอร์", "original_artist": "ศิลปินเดิม"},
    ]
    assert saved["total_duration_minutes"] == 20
    assert saved["equipment_requirements"] == "ไมโครโฟน"
    assert saved["work_sample_link"] == "https://example.test/sample"
    assert saved["notes"] == "หมายเหตุ"


def test_AC_APP_03_show_pending_review_status():
    repo, _, session_id, event_id = create_band_context()

    result = submit_band_application(
        session_id=session_id,
        payload=valid_payload(event_id),
        repository=repo,
    )

    assert result["status"] == "รอตรวจสอบ"
    assert result["application"]["status"] == "รอตรวจสอบ"


def test_invalid_application_is_not_saved():
    repo, _, session_id, event_id = create_band_context()
    payload = valid_payload(event_id)
    payload["songs"] = []

    result = submit_band_application(
        session_id=session_id,
        payload=payload,
        repository=repo,
    )

    assert result["success"] is False
    assert repo.get_band_application(1) is None
    assert repo.get_band_snapshot(1) is None
