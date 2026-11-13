"""ค่าที่กำหนดจากข้อกำหนด Auth และ Registration"""

# Registration model rules: capacity and remaining seats come from the Event record,
# while the duplicate guard is enforced by the unique user_id + event_id pair.
# ข้อมูลถูกระบุใน Event และ Registration model ตาม FR-REG-01, FR-REG-02, FR-REG-05, ASM-01, ASM-02 และ ASM-03
EVENT_REGISTRATION_UNIQUE_FIELDS = ("user_id", "event_id")
EVENT_REGISTRATION_OPEN_FLAG = "registration_open"

# NFR-SEC-01
PASSWORD_MIN_LENGTH = 8
MINIMUM_TLS_VERSION = "1.2"
SESSION_IDLE_TIMEOUT_MINUTES = 30
FAILED_LOGIN_ATTEMPT_LIMIT = 5
ACCOUNT_LOCKOUT_DURATION_MINUTES = 15
GENERIC_LOGIN_ERROR_MESSAGE = "อีเมลหรือรหัสผ่านไม่ถูกต้อง"

# Q-01: เกณฑ์แจ้งเตือนว่าที่นั่งเหลือน้อยกำหนดเป็นจำนวนที่นั่งที่เหลือไม่เกิน 5 ที่นั่ง
EVENT_REGISTRATION_LOW_SEAT_THRESHOLD = 5

# FR-APP-01 และ FR-APP-02: Data seed สำหรับอีเว้นต์ที่เปิดรับสมัครและข้อมูล snapshot ของวง
BAND_APPLICATION_EVENT_IDS = ("event-band-01", "event-band-02")
BAND_APPLICATION_REQUIRED_SNAPSHOT_FIELDS = (
    "band_name",
    "genre",
    "members",
    "contact_name",
    "contact_phone",
)
# Q-02: ใช้ข้อจำกัดเดียวกันทุกอีเว้นต์
BAND_APPLICATION_MAX_PERFORMANCE_MINUTES = 30
BAND_APPLICATION_MAX_SONG_COUNT = 8
# NFR-SEC-01, NFR-PERF-01, Q-03
BAND_APPLICATION_CONCURRENT_BANDS_TARGET = 20
BAND_APPLICATION_RESPONSE_P95_TARGET_SECONDS = 2.0

# PRE-CXL-01, FR-CXL-01, FR-CXL-03, ASM-01, ASM-03, ASM-04
REGISTRATION_STATUS_REGISTERED = "ลงทะเบียน"
REGISTRATION_STATUS_CANCELLED = "ยกเลิก"

# PRE-EVD-01 และ FR-EVD-02: ตัวอย่างข้อมูลอีเว้นต์สำหรับหน้า Event Detail ใช้เป็น seed เริ่มต้นในระบบ
EVENT_DETAIL_SAMPLE_EVENTS = [
    {
        "event_id": "EVT-001",
        "title": "ดนตรีในสวน ครั้งที่ 5",
        "event_date": "2026-11-20",
        "start_time": "16:00",
        "end_time": "21:00",
        "location": "ลานกิจกรรม อาคาร 5",
        "description": "คอนเสิร์ตกลางแจ้งที่รวมวงดนตรีและกิจกรรมถ่ายทอดสดในพื้นที่สันทนาการ",
    },
    {
        "event_id": "EVT-002",
        "title": "Battle of Bands",
        "event_date": "2026-11-22",
        "start_time": "18:30",
        "end_time": "22:00",
        "location": "อาคารศิลปะกลาง",
        "description": "การแข่งขันวงดนตรีจากมหาวิทยาลัยต่าง ๆ พร้อมการแสดงและโซนกิจกรรมสาธารณะ",
    },
]

# PRE-SCV-01, FR-SCV-02, NFR-DAT-01: ตัวอย่างตารางการแสดงสำหรับอีเว้นต์ที่เผยแพร่แล้วและอีเว้นต์ที่ยังไม่เผยแพร่
SCHEDULE_STATUS_PUBLISHED = "published"
SCHEDULE_STATUS_UNPUBLISHED = "unpublished"
SCHEDULE_VIEW_SAMPLE_DATA = [
    {
        "event_id": "EVT-001",
        "schedule_id": "SCH-001",
        "status": SCHEDULE_STATUS_PUBLISHED,
        "entries": [
            {
                "band_name": "The Echoes",
                "show_order": 1,
                "show_date": "2026-11-20",
                "start_time": "17:00",
                "end_time": "17:45",
                "venue": "เวทีหลัก",
            },
            {
                "band_name": "Neon Valley",
                "show_order": 2,
                "show_date": "2026-11-20",
                "start_time": "18:15",
                "end_time": "19:00",
                "venue": "เวทีหลัก",
            },
            {
                "band_name": "Midnight Harbor",
                "show_order": 3,
                "show_date": "2026-11-20",
                "start_time": "19:30",
                "end_time": "20:30",
                "venue": "อาคารศิลปะกลาง",
            },
        ],
    },
    {
        "event_id": "EVT-002",
        "schedule_id": "SCH-002",
        "status": SCHEDULE_STATUS_UNPUBLISHED,
        "entries": [],
    },
]

# Q-03: ให้ผู้ใช้เลือกอีเว้นต์ที่ต้องการดูตารางการแสดงจากรายการที่มีจริง
SCHEDULE_VIEW_DEFAULT_EVENT_ID = "EVT-001"

# Q-04, Q-05: ใช้ลำดับการแสดงที่บันทึกไว้ก่อน หากข้อมูลวัน/เวลา/สถานที่หาย ใช้ '—' แทนผลลัพธ์บนหน้า
SCHEDULE_VIEW_MISSING_VALUE_PLACEHOLDER = "—"

# Q-02, Q-06: ค่าพื้นฐานที่ใช้เป็นเงื่อนไข performance และการจัดการกรณีเรียกข้อมูลล้มเหลว
SCHEDULE_VIEW_P95_TARGET_SECONDS = 3
SCHEDULE_VIEW_PERFORMANCE_PERCENTILE = 95
SCHEDULE_VIEW_CONCURRENT_USERS = 50
SCHEDULE_VIEW_REQUEST_PERCENTAGE = 95

# NFR-PERF-01
RESPONSE_TIME_P95_TARGET_SECONDS = 3
PERFORMANCE_CONCURRENT_USERS = 50
