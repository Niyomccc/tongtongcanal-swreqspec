from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.services.schedule_service import get_schedule_by_event_id

# รองรับ FR-SCV-02: ให้ระบบเรียกข้อมูลตารางการแสดงที่สอดคล้องกับอีเว้นต์ที่ผู้ใช้เลือก
router = APIRouter()


@router.get("/api/events/{event_id}/schedule")
def get_event_schedule(event_id: str) -> dict[str, object]:
    try:
        schedule = get_schedule_by_event_id(event_id)
    except Exception as exc:  # รองรับ FR-SCV-06 และ ASM-01: เมื่อยกเลิกการเรียกข้อมูลไม่ได้ ให้แจ้งผู้ใช้ชัดเจน
        raise HTTPException(status_code=503, detail="แสดงตารางไม่ได้") from exc

    if schedule is None:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลตารางการแสดง")

    if schedule.status != "published":
        return {
            "event_id": schedule.event_id,
            "schedule_id": schedule.schedule_id,
            "status": schedule.status,
            "entries": [],
        }

    return {
        "event_id": schedule.event_id,
        "schedule_id": schedule.schedule_id,
        "status": schedule.status,
        "entries": [
            {
                "band_name": entry.band_name,
                "show_order": entry.show_order,
                "show_date": entry.show_date,
                "start_time": entry.start_time,
                "end_time": entry.end_time,
                "venue": entry.venue,
            }
            for entry in schedule.entries
        ],
    }
