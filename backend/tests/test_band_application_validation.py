import pytest

from app.auth.application import validate_band_application
from app.auth.repository import AuthRepository
from app.auth.session import create_session, reset_sessions
from app.config import BAND_APPLICATION_MAX_PERFORMANCE_MINUTES, BAND_APPLICATION_MAX_SONG_COUNT


@pytest.fixture(autouse=True)
def clear_application_state():
    repo = AuthRepository()
    repo.reset()
    reset_sessions()
    yield
    repo.reset()
    reset_sessions()


def create_band_session(
    repo: AuthRepository,
    *,
    complete: bool = True,
    members: str = "นักร้องและกีตาร์, กลอง, เบส",
) -> tuple[str, str]:
    profile = {
        "band_name": "Moonlight Band",
        "genre": "Indie Pop",
        "members": members,
        "contact_name": "ผู้ติดต่อ",
        "contact_phone": "089-876-5432",
    }
    if not complete:
        profile["genre"] = ""
    band = repo.create_user(
        email="moonlight@ku.th",
        password_hash="hash",
        salt="salt",
        full_name_or_band_name="Moonlight Band",
        role="band",
        profile=profile,
    )
    session = create_session(band["id"], role="band")
    event = repo.seed_open_band_application_events()[0]
    return session["session_id"], event["event_id"]


def valid_payload(event_id: str, *, song_count: int = 1, duration: int = 20) -> dict:
    return {
        "event_id": event_id,
        "songs": [
            {"song_name": f"เพลง {index}", "song_type": "ต้นฉบับ"}
            for index in range(song_count)
        ],
        "total_duration_minutes": duration,
    }


def test_AC_APP_04_accepts_applications_at_configured_limits():
    repo = AuthRepository()
    session_id, event_id = create_band_session(repo)
    payload = valid_payload(
        event_id,
        song_count=BAND_APPLICATION_MAX_SONG_COUNT,
        duration=BAND_APPLICATION_MAX_PERFORMANCE_MINUTES,
    )

    result = validate_band_application(session_id=session_id, payload=payload, repository=repo)

    assert result["success"] is True
    assert result["is_valid"] is True
    assert result["limits"] == {
        "max_performance_minutes": BAND_APPLICATION_MAX_PERFORMANCE_MINUTES,
        "max_song_count": BAND_APPLICATION_MAX_SONG_COUNT,
    }
    assert all(
        event["max_performance_minutes"] == BAND_APPLICATION_MAX_PERFORMANCE_MINUTES
        and event["max_song_count"] == BAND_APPLICATION_MAX_SONG_COUNT
        for event in repo.list_open_application_events()
    )


def test_AC_APP_04_rejects_applications_over_duration_or_song_limits():
    repo = AuthRepository()
    session_id, event_id = create_band_session(repo)
    payload = valid_payload(
        event_id,
        song_count=BAND_APPLICATION_MAX_SONG_COUNT + 1,
        duration=BAND_APPLICATION_MAX_PERFORMANCE_MINUTES + 1,
    )

    result = validate_band_application(session_id=session_id, payload=payload, repository=repo)

    assert result["success"] is False
    assert result["is_valid"] is False
    assert any("จำนวนเพลง" in error for error in result["errors"])
    assert any("ความยาวการแสดงรวม" in error for error in result["errors"])


def test_AC_APP_04_rejects_incomplete_band_or_required_song_data():
    repo = AuthRepository()
    session_id, event_id = create_band_session(repo, complete=False)
    payload = valid_payload(event_id)
    payload["songs"][0] = {
        "song_name": "",
        "song_type": "คัฟเวอร์",
        "original_artist": "",
    }

    result = validate_band_application(session_id=session_id, payload=payload, repository=repo)

    assert result["success"] is False
    assert any("ข้อมูลวงยังไม่ครบ" in error for error in result["errors"])
    assert any("ชื่อเพลง" in error for error in result["errors"])
    assert any("ศิลปินเดิม" in error for error in result["errors"])


def test_AC_APP_04_rejects_empty_song_list_and_missing_duration():
    repo = AuthRepository()
    session_id, event_id = create_band_session(repo)
    payload = {"event_id": event_id, "songs": []}

    result = validate_band_application(session_id=session_id, payload=payload, repository=repo)

    assert result["success"] is False
    assert any("อย่างน้อย 1 เพลง" in error for error in result["errors"])
    assert any("ความยาวการแสดงรวม" in error for error in result["errors"])


def test_AC_APP_04_rejects_band_with_no_members():
    repo = AuthRepository()
    session_id, event_id = create_band_session(repo, members="0")

    result = validate_band_application(
        session_id=session_id,
        payload=valid_payload(event_id),
        repository=repo,
    )

    assert result["success"] is False
    assert any("ข้อมูลวงยังไม่ครบ" in error for error in result["errors"])


def test_T05_requires_a_valid_band_session():
    repo = AuthRepository()
    payload = valid_payload("event-band-01")

    result = validate_band_application(
        session_id="invalid-session",
        payload=payload,
        repository=repo,
    )

    assert result["success"] is False
    assert result["is_valid"] is False
    assert "เซสชันหมดอายุหรือไม่ถูกต้อง" in result["errors"]
