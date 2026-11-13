# RTM: ดูรายละเอียดอีเว้นต์ (Event Detail)
อ้างอิง: spec.md SPEC-EVD-001 Draft v1 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2026-11-13 20:47:09Z | test: backend 35 ผ่าน, frontend 17 ผ่าน / 1 ไม่ผ่าน (ไม่ใช่ feature ที่ตรวจ; setup.test.jsx เกี่ยวกับหน้าเปิดระบบทั่วไป)

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| PRE-EVD-01 | - | T-01, T-03 | `backend/app/config.py` / `backend/app/services/event_service.py:_seed_event_cache` | `backend/tests/test_event_detail.py` ครอบคลุมการโหลดข้อมูลเริ่มต้นและการร้องขอ `EVT-001` ผ่าน | ครบ |
| FR-EVD-01 | ไม่มี AC | T-04 | `frontend/src/pages/EventListPage.jsx:EventListPage` | `frontend/src/__tests__/EventListPage.test.jsx` ตรวจการโหลดรายการและ click เลือกอีเว้นต์ผ่าน | ช่องโหว่ |
| FR-EVD-02 | AC-EVD-01, AC-EVD-02 | T-03, T-05 | `backend/app/routes/event_detail.py:get_event_detail`; `frontend/src/pages/EventDetailPage.jsx:EventDetailPage` | `backend/tests/test_event_detail.py::test_AC_EVD_01_event_name_detail`, `::test_AC_EVD_02_event_date_time_location`; `frontend/src/__tests__/EventDetailPage.test.jsx` ผ่าน | ครบ |
| FR-EVD-03 | AC-EVD-03 | T-06 | `backend/app/services/event_service.py:update_event`; `backend/app/services/event_service.py:get_event_by_id` | `backend/tests/test_event_detail.py::test_AC_EVD_03_latest_event_data` ผ่าน | ครบ |
| FR-EVD-04 | AC-EVD-04 | T-07 | `backend/app/routes/event_detail.py:get_event_detail`; `frontend/src/pages/EventDetailPage.jsx:EventDetailPage` | `backend/tests/test_event_detail.py::test_AC_EVD_04_event_not_found`; `frontend/src/__tests__/EventDetailPage.test.jsx` ผ่าน | ครบ |
| NFR-DAT-01 | AC-EVD-03 | T-05, T-06 | `backend/app/services/event_service.py:update_event`; `frontend/src/pages/EventDetailPage.jsx:EventDetailPage` | `backend/tests/test_event_detail.py::test_AC_EVD_03_latest_event_data`; `frontend/src/__tests__/EventDetailPage.test.jsx` ผ่าน | ครบ |
| NFR-PERF-01 | ไม่มี AC ใน spec แต่ได้กำหนดค่า Q-02 แล้ว | T-08 | `backend/app/config.py` / `backend/tests/test_event_performance.py:_request_event_detail` | `backend/tests/test_event_performance.py::test_NFR_PERF_01_event_detail_response_time_p95_under_limit` ผ่าน | ครบ |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/routes/event_detail.py:/api/events` | FR-EVD-01, FR-EVD-02 | ใช่ | คืนรายการอีเว้นต์เพื่อผู้ใช้เลือกจากหน้าอีเว้นต์ตาม FR-EVD-01 และ FR-EVD-02 |
| `backend/app/routes/event_detail.py:/api/events/{event_id}` | FR-EVD-02, FR-EVD-04 | ใช่ | คืนข้อมูลอีเว้นต์ตาม ID และ 404 เมื่อไม่พบข้อมูลตาม FR-EVD-04 |
| `backend/app/services/event_service.py:update_event` | FR-EVD-03, NFR-DAT-01 | ใช่ | แทนข้อมูล cache ด้วยค่าใหม่และคืนค่าใหม่ล่าสุด |
| `frontend/src/pages/EventListPage.jsx:EventListPage` | FR-EVD-01 | ใช่ | แสดงรายการอีเว้นต์และเรียก `onSelectEvent` เมื่อเลือก |
| `frontend/src/pages/EventDetailPage.jsx:EventDetailPage` | FR-EVD-02, FR-EVD-04, NFR-DAT-01 | ใช่ | แสดงชื่อ วัน เวลา สถานที่ และรายละเอียดกิจกรรม พร้อมข้อความไม่พบข้อมูล |
| `backend/app/config.py` | NFR-PERF-01 | ใช่ | เก็บค่า threshold และจำนวน concurrent users ไว้ที่เดียวตามกติกาโครงการ |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-EVD-001 | FR ไม่มี AC | `spec.md`, `tasks.md` | FR-EVD-01 | FR-EVD-01 ระบุว่า “ระบบต้องให้ผู้ใช้เลือกอีเว้นต์จากหน้าอีเว้นต์ได้” แต่ไม่มี AC ที่ตรวจเรื่องการเลือกอีเว้นต์อย่างชัดเจน และ tasks.md ระบุชัดว่าต้องเสนอทีมเพิ่ม AC | แก้ spec |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| - | ไม่มีข้อค้นพบที่แก้แล้วในรอบนี้ | การตรวจพบเพียงช่องว่างของ spec (FR ไม่มี AC) และยังไม่ถูกแก้โดยทีม |
