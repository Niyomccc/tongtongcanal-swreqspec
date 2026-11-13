from app.config import SCHEDULE_VIEW_SAMPLE_DATA
from app.models.schedule import EventSchedule, ScheduleEntry


_SCHEDULE_CACHE: dict[str, EventSchedule] = {}


def _seed_schedule_cache() -> None:
    """รองรับ PRE-SCV-01 และ FR-SCV-02: โหลดข้อมูลตารางตัวอย่างของทุกอีเว้นต์เพื่อให้ service พร้อมใช้งาน"""
    if _SCHEDULE_CACHE:
        return

    for item in SCHEDULE_VIEW_SAMPLE_DATA:
        _SCHEDULE_CACHE[item["event_id"]] = EventSchedule(
            event_id=item["event_id"],
            schedule_id=item["schedule_id"],
            status=item["status"],
            entries=tuple(
                ScheduleEntry(
                    band_name=entry["band_name"],
                    show_order=entry["show_order"],
                    show_date=entry["show_date"],
                    start_time=entry["start_time"],
                    end_time=entry["end_time"],
                    venue=entry["venue"],
                )
                for entry in item.get("entries", [])
            ),
        )


_seed_schedule_cache()


def list_schedules() -> list[EventSchedule]:
    """รองรับ FR-SCV-02: คืนรายการตารางการแสดงทั้งหมดที่ระบบมีสำหรับอีเว้นต์ต่าง ๆ"""
    return list(_SCHEDULE_CACHE.values())


def get_schedule_by_event_id(event_id: str) -> EventSchedule | None:
    """รองรับ FR-SCV-02 และ NFR-DAT-01: คืนข้อมูลตารางที่ตรงกับอีเว้นต์ที่ผู้ใช้เลือก"""
    normalized_id = str(event_id).strip()
    return _SCHEDULE_CACHE.get(normalized_id)


def get_schedule_status(event_id: str) -> str:
    """รองรับ PRE-SCV-01: คืนสถานะของตารางการแสดงว่าถูกเผยแพร่แล้วหรือยัง"""
    schedule = get_schedule_by_event_id(event_id)
    if schedule is None:
        return "not_found"
    return schedule.status


def get_schedule_payload(event_id: str) -> dict[str, object]:
    """รองรับ FR-SCV-02: คืนสเตตัสและรายการวงพร้อมลำดับ วัน เวลา และสถานที่เป็น payload ที่พร้อมใช้ต่อโดย API"""
    schedule = get_schedule_by_event_id(event_id)
    if schedule is None:
        return {"event_id": str(event_id).strip(), "status": "not_found", "entries": []}

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
