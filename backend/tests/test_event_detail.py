from fastapi.testclient import TestClient

from app.main import app
from app.services.event_service import get_event_by_id, update_event


def test_AC_EVD_01_event_name_detail():
    client = TestClient(app)

    response = client.get("/api/events/EVT-001")

    assert response.status_code == 200
    payload = response.json()
    assert payload["event_id"] == "EVT-001"
    assert payload["title"] == "ดนตรีในสวน ครั้งที่ 5"
    assert payload["description"]


def test_AC_EVD_02_event_date_time_location():
    client = TestClient(app)

    response = client.get("/api/events/EVT-001")

    assert response.status_code == 200
    payload = response.json()
    assert payload["event_date"] == "2026-11-20"
    assert payload["start_time"] == "16:00"
    assert payload["end_time"] == "21:00"
    assert payload["location"] == "ลานกิจกรรม อาคาร 5"


def test_AC_EVD_03_latest_event_data():
    original = get_event_by_id("EVT-001")
    assert original is not None

    updated = update_event(
        "EVT-001",
        title="ดนตรีในสวน ครั้งที่ 7",
        event_date="2026-12-05",
        start_time="17:00",
        end_time="22:30",
        location="หอประชุมใหญ่",
        description="ข้อมูลอัปเดตล่าสุดสำหรับการแสดงในคืนสุดท้าย",
    )

    assert updated is not None
    refreshed = get_event_by_id("EVT-001")
    assert refreshed is not None
    assert refreshed.title == "ดนตรีในสวน ครั้งที่ 7"
    assert refreshed.event_date == "2026-12-05"
    assert refreshed.start_time == "17:00"
    assert refreshed.end_time == "22:30"
    assert refreshed.location == "หอประชุมใหญ่"
    assert refreshed.description == "ข้อมูลอัปเดตล่าสุดสำหรับการแสดงในคืนสุดท้าย"

    update_event(
        "EVT-001",
        title=original.title,
        event_date=original.event_date,
        start_time=original.start_time,
        end_time=original.end_time,
        location=original.location,
        description=original.description,
    )


def test_AC_EVD_04_event_not_found():
    client = TestClient(app)

    response = client.get("/api/events/EVT-404")

    assert response.status_code == 404
    assert response.json()["detail"] == "ไม่พบข้อมูลอีเว้นต์"
