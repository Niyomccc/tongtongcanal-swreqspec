# RTM: ดูตารางการแสดง (Schedule View)
อ้างอิง: [spec.md](./spec.md) Draft v2 | [tasks.md](./tasks.md) | [test-cases.md](./test-cases.md)
สร้างด้วย /verify เมื่อ 2026-11-13 21:29 | test: backend 35 ผ่าน 0 ไม่ผ่าน; frontend 21 ผ่าน 3 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)

| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| PRE-SCV-01 | AC-SCV-04 | T-01 เสร็จ; T-04 พร้อมทำ (สถานะ task ไม่ตรงกับโค้ดที่มีแล้ว) | `backend/app/config.py`: `SCHEDULE_VIEW_SAMPLE_DATA`; `backend/app/services/schedule_service.py`: `_seed_schedule_cache`, `get_schedule_by_event_id`; `backend/app/routes/schedule_view.py`: `get_event_schedule`; `frontend/src/pages/ScheduleViewPage.jsx`: unpublished state | `test_AC_SCV_04_unpublished_schedule_message` (ผ่าน; ตรวจข้อความและเช็กเพียงว่าไม่พบวงตัวอย่างหนึ่งวง) | ช่องโหว่: ไม่มี backend test ยืนยัน seed/API และ test ไม่ยืนยันว่าไม่มีแถวตารางใด ๆ |
| FR-SCV-01 | AC-SCV-01 ถูกอ้างใน traceability แต่ AC ตรวจการแสดงรายชื่อ ไม่ได้ตรวจการเลือกเมนู/อีเว้นต์ | T-06 เสร็จ ทั้งที่ยังระบุ Q-03 และเงื่อนไขเสร็จของ task ยังไม่ปรากฏคำตอบทีม | `frontend/src/pages/ScheduleListPage.jsx`: `ScheduleListPage`; `backend/app/routes/event_detail.py`: `list_event_details`; `frontend/src/main.jsx` และ `frontend/src/App.jsx`: entry point ปัจจุบันไม่ได้เชื่อมหน้า Schedule | `test_AC_SCV_06_select_event_to_view_schedule` (ผ่าน แต่ใช้ AC-SCV-06 ซึ่งไม่มีใน spec) | ช่องโหว่: FR ไม่มี AC ตรวจการเลือก และหน้าตารางยังเข้าใช้งานจาก entry point จริงไม่ได้ |
| FR-SCV-02 | AC-SCV-03 | T-01, T-02, T-03 เสร็จ | `backend/app/services/schedule_service.py`: `get_schedule_by_event_id`, `get_schedule_payload`; `backend/app/routes/schedule_view.py`: `get_event_schedule`; `frontend/src/api/client.js`: `getScheduleByEventId` | ไม่มี backend test ของ schedule endpoint/service; `test_AC_SCV_03_schedule_matches_published_data` (ผ่าน แต่จำลอง API ใน UI test) | ช่องโหว่: ไม่มี test ตรวจการเรียกข้อมูลของอีเว้นต์ที่เลือกผ่าน service/route จริง |
| FR-SCV-03 | AC-SCV-01 | T-03, T-07 เสร็จ | `frontend/src/pages/ScheduleViewPage.jsx`: เรียง entries ด้วย `show_order` และ render แถววง | `test_AC_SCV_01_show_bands_in_schedule_order` (ผ่าน แต่ตรวจชื่อและจำนวนแถว ไม่ตรวจลำดับจริง); ไม่มี test ของแถว TC ที่อนุมัติ | ช่องโหว่: การเรียงลำดับที่นำไปใช้ยังรอคำตอบ Q-04 และ test ไม่ตรวจ Then เรื่องลำดับ |
| FR-SCV-04 | AC-SCV-02 | T-03, T-07 เสร็จ | `frontend/src/pages/ScheduleViewPage.jsx`: render วัน เวลา และสถานที่; ใช้ placeholder เมื่อค่าไม่มี | `test_AC_SCV_02_show_date_time_and_venue` (ผ่าน แต่ตรวจเพียงว่ามีบางค่าปรากฏ); ไม่มี test ของแถว TC ที่อนุมัติ | ช่องโหว่: การแสดงค่าที่หายไปเลือกคำตอบแทนทีมตาม Q-05 และ test ไม่ตรวจครบทุกวง/ทุกฟิลด์ |
| FR-SCV-05 | AC-SCV-04 | T-04 พร้อมทำ แม้มี implementation และ test แล้ว | `backend/app/routes/schedule_view.py`: คืน entries ว่างเมื่อ status ไม่ใช่ `published`; `frontend/src/pages/ScheduleViewPage.jsx`: แสดงข้อความ unpublished | `test_AC_SCV_04_unpublished_schedule_message` (ผ่าน แต่ตรวจเพียงไม่พบวงหนึ่งชื่อ) | ช่องโหว่: test ไม่ยืนยันว่าไม่มีรายการวงใด ๆ และไม่มี test backend ของสถานะ unpublished |
| FR-SCV-06 | AC-SCV-05 | T-05 เสร็จ | `backend/app/routes/schedule_view.py`: `get_event_schedule` จับ exception และคืน HTTP 503; `frontend/src/pages/ScheduleViewPage.jsx`: แสดง error | `test_AC_SCV_05_schedule_load_failure_message` (ผ่านโดย mock rejected client; ไม่ทดสอบ backend/ฐานข้อมูลล้มเหลวจริง) | ช่องโหว่: ขอบเขต failure ยังรอ Q-06 และ test ตรวจเฉพาะ error ที่จำลองจาก client |
| NFR-DAT-01 | AC-SCV-03 | T-01, T-03, T-07 เสร็จ | `backend/app/config.py`: ข้อมูล seed; `backend/app/services/schedule_service.py`: คืนข้อมูล cache; `frontend/src/pages/ScheduleViewPage.jsx`: render payload | `test_AC_SCV_03_schedule_matches_published_data` (ผ่าน แต่ใช้ fixture ใน test และตรวจเพียงบางค่า ไม่เปรียบเทียบกับ source of truth จริง) | ช่องโหว่: ไม่มี test ยืนยันความตรงและความเป็นปัจจุบันเทียบข้อมูลผู้จัดงานจริง; Q-04/Q-05 ยังเปิด |
| NFR-PERF-01 | ไม่มี AC | T-08 เสร็จ ทั้งที่ Q-02 ยังเปิด | `backend/app/config.py`: `SCHEDULE_VIEW_P95_TARGET_SECONDS`, `SCHEDULE_VIEW_PERFORMANCE_PERCENTILE`, `SCHEDULE_VIEW_CONCURRENT_USERS`, `SCHEDULE_VIEW_REQUEST_PERCENTAGE` | ไม่มี `backend/tests/test_schedule_performance.py`; `test_NFR_PERF_01_event_detail_response_time_p95_under_limit` ทดสอบ Event Detail ไม่ใช่ Schedule View | ช่องโหว่: ค่า 3 วินาที, 95%, 50 คนถูกกำหนดทั้งที่ Q-02 ยังเปิด และไม่มี performance test ของ Schedule View |

ไม่พบ shared constraint ID ใน Constraints ของ feature spec; shared constraints ที่มีอยู่ระบุว่าใช้งานกับ 001-booking เท่านั้น จึงไม่มีแถว shared constraint ที่ใช้กับ feature นี้

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)

| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/routes/schedule_view.py`: `GET /api/events/{event_id}/schedule`, `get_event_schedule` | FR-SCV-02, FR-SCV-05, FR-SCV-06, ASM-01, ASM-02 | บางส่วน | ค้นตาม event_id และส่ง entries เฉพาะ published; exception ทุกชนิดถูกตีความเป็นโหลดข้อมูลไม่ได้ (Q-06 ยังไม่กำหนดขอบเขต) |
| `backend/app/services/schedule_service.py`: `_seed_schedule_cache`, `list_schedules`, `get_schedule_by_event_id`, `get_schedule_status`, `get_schedule_payload` | PRE-SCV-01, FR-SCV-02, NFR-DAT-01 | บางส่วน | ใช้ in-memory seed/cache ไม่ใช่ฐานข้อมูลผู้จัดงาน และไม่มี test backend ของ schedule |
| `frontend/src/api/client.js`: `getEventList`, `getScheduleByEventId` | FR-SCV-01, FR-SCV-02 | บางส่วน | client มีการเรียก endpoint แต่ UI tests จำลอง client; ยังไม่มีการต่อ flow จาก application entry point |
| `frontend/src/pages/ScheduleListPage.jsx`: `ScheduleListPage` | FR-SCV-01 | บางส่วน | แสดงรายการให้เลือกและส่ง event_id ผ่าน callback; component ไม่ได้ถูกเชื่อมใน `App.jsx` |
| `frontend/src/pages/ScheduleViewPage.jsx`: `ScheduleViewPage` | FR-SCV-01 ถึง FR-SCV-06, NFR-DAT-01, ASM-02 | บางส่วน | แสดงตารางและสถานะตาม response; ใช้ default `EVT-001`, เรียง `show_order` และแทนค่าที่หายด้วย “—” ทั้งที่ Q-03/Q-04/Q-05 ยังเปิด |
| `frontend/src/App.jsx`: `App`; `frontend/src/main.jsx`: render root | — | ไม่ตรงกับการเปิดใช้งาน feature | root แสดงหน้าเริ่มต้นลงทะเบียนและไม่ได้ mount ScheduleListPage/ScheduleViewPage; ตรวจแล้วว่า feature ไม่ได้เชื่อมกับ entry point |
| `backend/app/config.py`: `SCHEDULE_VIEW_SAMPLE_DATA` และค่าคงที่ Schedule View | PRE-SCV-01, FR-SCV-02, Q-02, Q-03, Q-04, Q-05, Q-06 | บางส่วน | ค่า seed รองรับการทดสอบหน้าจอ แต่มีการกำหนดคำตอบของ Open Questions เป็นค่าคงที่โดยไม่มีการปิด Q ใน spec |
| `frontend/src/__tests__/ScheduleViewPage.test.jsx` | AC-SCV-01 ถึง AC-SCV-05 | บางส่วน | มี AC-level tests ผ่าน แต่ไม่มี test ตาม approved TC rows; assertion ของ AC-01/02/03/04/05 ไม่ครอบคลุมรายละเอียด Then ครบ |
| `frontend/src/__tests__/ScheduleListPage.test.jsx` | FR-SCV-01; ชื่อ test อ้าง AC-SCV-06 | ไม่ตรง ID | AC-SCV-06 ไม่มีใน spec; ห้ามใช้ ID นี้เป็น AC จนกว่าทีมจะแก้ spec อย่างเป็นทางการ |
| `specs/003-schedule-view/mockups/UI-SCV-01-schedule.html` | UI-SCV-01; FR-SCV-01, FR-SCV-03 ถึง FR-SCV-06 | mockup มีเนื้อหาเกิน requirement | มีแถบนำทาง “การลงทะเบียนของฉัน” และปุ่ม “ลองอีกครั้ง” ซึ่งไม่มี FR รองรับ; spec ไม่มีหมวด UI ที่ระบุว่ารายการเหล่านี้ต้องตรง |

## 3. ข้อค้นพบ

ชนิดที่ใช้: AC ไม่มี test / test อ่อน / FR ไม่มี AC / เดา Q-xx / อ้าง ID ผิดเรื่อง / mockup เกิน spec

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | FR ไม่มี AC | `spec.md` FR-SCV-01; `frontend/src/main.jsx`, `frontend/src/App.jsx` | FR-SCV-01 | ไม่มี AC ที่ตรวจการเลือกเมนูและเลือกอีเว้นต์โดยตรง; `AC-SCV-01` ตรวจการแสดงรายชื่อวงเท่านั้น และหน้า ScheduleListPage/ScheduleViewPage ไม่ได้เชื่อมจาก app entry point ทำให้ flow ใช้งานจริงไม่ถึงผู้ใช้ | |
| F-02 | อ้าง ID ผิดเรื่อง | `frontend/src/__tests__/ScheduleListPage.test.jsx`: `test_AC_SCV_06_select_event_to_view_schedule` | ไม่มี AC-SCV-06 ใน `spec.md`; T-06 ระบุว่าการเลือกยังรอ Q-03 | test สร้างการอ้าง AC-SCV-06 ที่ไม่มีใน spec แทนการอ้าง FR-SCV-01 อย่างถูกต้อง | |
| F-03 | AC ไม่มี test | `specs/003-schedule-view/test-cases.md`; `frontend/src/__tests__/ScheduleViewPage.test.jsx`, `ScheduleListPage.test.jsx` | TC-SCV-01-1 ถึง TC-SCV-05-3 (15 แถว สถานะ “ใช้ได้”) | ไม่มี test ที่ใช้ชื่อ test ตาม 15 แถวที่อนุมัติ; มีเพียง AC-level tests เดิม 5 ตัวและ selection test 1 ตัว จึงยังไม่ได้เขียน test หนึ่งตัวต่อหนึ่งแถวตามตาราง | |
| F-04 | test อ่อน | `frontend/src/__tests__/ScheduleViewPage.test.jsx`: AC-SCV-01, AC-SCV-02, AC-SCV-03 | Then ของ AC-SCV-01 ถึง AC-SCV-03 | AC-01 ตรวจว่าชื่อวงปรากฏและจำนวน row มากกว่า 3 แต่ไม่ตรวจลำดับ; AC-02 ตรวจว่ามีตัวอย่างวัน/เวลา/สถานที่บางค่า ไม่ครบทุกวง; AC-03 ตรวจ fixture บางค่า ไม่ตรวจเทียบทุก field กับข้อมูลผู้จัดงาน/source of truth | |
| F-05 | test อ่อน | `backend/app/routes/schedule_view.py`; ไม่มี backend test schedule | FR-SCV-02, FR-SCV-05, FR-SCV-06, NFR-DAT-01 | backend suite ผ่าน 35 tests แต่ไม่มี test ของ schedule route/service/seed; UI tests ทั้งหมด mock API จึงไม่ตรวจ endpoint และ contract จริง | |
| F-06 | เดา Q-xx | `backend/app/config.py`: Q-04/Q-05; `frontend/src/pages/ScheduleViewPage.jsx`; T-07 | Q-04, Q-05 | โค้ดเลือกเรียงตาม `show_order` และแทนค่าที่หายด้วย “—” ขณะที่ spec ยังเปิดคำถามทั้งสองข้อ; tasks.md ระบุ T-07 เสร็จทั้งที่เงื่อนไขเสร็จต้องรอคำตอบทีม | |
| F-07 | เดา Q-xx | `backend/app/config.py`; `backend/app/routes/schedule_view.py`; T-08 | Q-02, Q-06 | กำหนด performance เป็น 3 วินาที, 95%, 50 concurrent และตีความ exception ทุกชนิดเป็น database-load failure ทั้งที่ Q-02/Q-06 ยังเปิด; T-08 ถูกระบุเสร็จโดยไม่มีผลตัดสินจากทีม | |
| F-08 | AC ไม่มี test | `backend/tests/` และ `specs/003-schedule-view/tasks.md` T-08 | NFR-PERF-01 | ไม่มี test performance สำหรับ Schedule View ตาม path ที่ tasks.md ระบุ; test performance ที่มีตรวจ `/api/events/EVT-001` ของ Event Detail ไม่ใช่ endpoint ตาราง; Q-02 ยังไม่ปิด | |
| F-09 | mockup เกิน spec | `specs/003-schedule-view/mockups/UI-SCV-01-schedule.html` | FR-SCV-01 ถึง FR-SCV-06 และ Out of scope | mockup แสดงเมนู “การลงทะเบียนของฉัน” และปุ่ม “ลองอีกครั้ง” แต่ไม่มี requirement รองรับ; หมวด UI ใน spec ไม่ได้ระบุให้สองรายการนี้ต้องตรง จึงต้องให้ทีม/PO ตัดสิน ไม่ควรถือเป็นงานที่ขาด | |

## 4. แก้แล้ว

| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| — | ไม่มี | ไม่พบ RTM เดิมใน feature folder |
