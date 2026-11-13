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

# NFR-PERF-01
RESPONSE_TIME_P95_TARGET_SECONDS = 3
PERFORMANCE_CONCURRENT_USERS = 50
