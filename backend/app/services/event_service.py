from app.config import EVENT_DETAIL_SAMPLE_EVENTS
from app.models.event import EventDetail


_EVENT_CACHE: dict[str, EventDetail] = {}


def _seed_event_cache() -> None:
    """รองรับ PRE-EVD-01 และ FR-EVD-01: เรียกใช้ข้อมูลชุดเริ่มต้นก่อนใช้งานหน้า Event Detail"""
    if _EVENT_CACHE:
        return

    for item in EVENT_DETAIL_SAMPLE_EVENTS:
        _EVENT_CACHE[item["event_id"]] = EventDetail(
            event_id=item["event_id"],
            title=item["title"],
            event_date=item["event_date"],
            start_time=item["start_time"],
            end_time=item["end_time"],
            location=item["location"],
            description=item["description"],
        )


_seed_event_cache()


def list_events() -> list[EventDetail]:
    """รองรับ PRE-EVD-01 และ FR-EVD-01: คืนรายการอีเว้นต์ที่พร้อมเลือกจากหน้าอีเว้นต์"""
    return list(_EVENT_CACHE.values())


def get_event_by_id(event_id: str) -> EventDetail | None:
    """รองรับ FR-EVD-02 และ FR-EVD-03: คืนข้อมูลอีเว้นต์ล่าสุดตาม ID ที่เลือกเพื่อแสดงรายละเอียด"""
    normalized_id = str(event_id).strip()
    return _EVENT_CACHE.get(normalized_id)


def update_event(event_id: str, **changes: str) -> EventDetail | None:
    """รองรับ FR-EVD-03 และ NFR-DAT-01: อัปเดตข้อมูลอีเว้นต์ที่ cached แล้วคืนข้อมูลล่าสุด"""
    normalized_id = str(event_id).strip()
    current = _EVENT_CACHE.get(normalized_id)
    if current is None:
        return None

    updated = EventDetail(
        event_id=current.event_id,
        title=changes.get("title", current.title),
        event_date=changes.get("event_date", current.event_date),
        start_time=changes.get("start_time", current.start_time),
        end_time=changes.get("end_time", current.end_time),
        location=changes.get("location", current.location),
        description=changes.get("description", current.description),
    )
    _EVENT_CACHE[normalized_id] = updated
    return updated
