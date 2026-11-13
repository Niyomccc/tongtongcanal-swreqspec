from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.services.event_service import get_event_by_id, list_events

# รองรับ FR-EVD-01 และ FR-EVD-02: ให้หน้าอีเว้นต์เลือกและเรียกดูรายละเอียดอีเว้นต์จาก backend
router = APIRouter()


@router.get("/api/events")
def list_event_details() -> list[dict[str, str]]:
    return [
        {
            "event_id": event.event_id,
            "title": event.title,
            "event_date": event.event_date,
            "start_time": event.start_time,
            "end_time": event.end_time,
            "location": event.location,
            "description": event.description,
        }
        for event in list_events()
    ]


@router.get("/api/events/{event_id}")
def get_event_detail(event_id: str) -> dict[str, str]:
    event = get_event_by_id(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลอีเว้นต์")

    return {
        "event_id": event.event_id,
        "title": event.title,
        "event_date": event.event_date,
        "start_time": event.start_time,
        "end_time": event.end_time,
        "location": event.location,
        "description": event.description,
    }
