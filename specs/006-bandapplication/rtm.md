# RTM: สมัครเข้าร่วมแสดง (Band Application)
อ้างอิง: spec.md SPEC-APP-001 Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2026-11-13 21:54 UTC | test: backend 58 ผ่าน 0 ไม่ผ่าน; frontend 26 ผ่าน 1 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)

| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-APP-01 | AC-APP-01 | T-03, T-04 | `backend/app/auth/application.py`: `get_open_application_events`, `events_open_endpoint`; `frontend/src/pages/SelectEventPage.jsx`: `SelectEventPage` | `test_T03_get_open_events_and_band_profile_for_band_user`, `test_T04_select_event_and_show_readonly_band_profile` (ผ่าน) | ช่องโหว่ |
| FR-APP-02 | AC-APP-02 | T-03, T-04, T-07, T-08 | `backend/app/auth/application.py`: `_derive_band_profile`, `get_band_application_profile`; `backend/app/auth/repository.py`: `create_band_application`; `frontend/src/pages/BandApplicationPage.jsx`: `BandApplicationPage` | `test_AC_APP_02_store_band_snapshot_and_performance_data`, `test_T04_shows_band_data_read_only_and_cover_artist_field` (ผ่าน แต่ตรวจ snapshot/ข้อมูลวงไม่ครบทุกฟิลด์) | ช่องโหว่ |
| FR-APP-03 | AC-APP-04 | T-05, T-06, T-09 | `backend/app/auth/application.py`: `validate_band_application`, `application_validate_endpoint`; `frontend/src/pages/BandApplicationPage.jsx`: `validateApplication` | `test_AC_APP_04_*`, `test_TC_APP_01_5_reject_application_without_song`, `test_TC_APP_01_6_reject_application_over_duration_limit`, `test_TC_APP_01_7_reject_application_over_song_limit` (ผ่าน) | ช่องโหว่ |
| FR-APP-04 | AC-APP-01, AC-APP-02, AC-APP-03 | T-07, T-08 | `backend/app/auth/application.py`: `submit_band_application`; `backend/app/auth/repository.py`: `create_band_application`, `get_band_application`; `frontend/src/pages/ApplicationResultPage.jsx`: `ApplicationResultPage` | `test_AC_APP_01_create_application_for_selected_event`, `test_AC_APP_02_store_band_snapshot_and_performance_data`, `test_AC_APP_03_show_pending_review_status`, `test_AC_APP_03_shows_pending_review_after_successful_submission` (ผ่าน; แต่หน้าผลลัพธ์ไม่ได้เชื่อมในเส้นทางใช้งานจริง) | ช่องโหว่ |
| FR-APP-05 | AC-APP-04 | T-05, T-06, T-09 | `backend/app/auth/application.py`: `validate_band_application`; `frontend/src/pages/BandApplicationPage.jsx`: `validateApplication`, ปุ่มส่งใบสมัคร | `test_AC_APP_04_*`, `test_TC_APP_01_5_*`, `test_TC_APP_01_6_*`, `test_TC_APP_01_7_*` (ผ่าน; กรณีข้อมูลวงจาก UC-07 ไม่ครบไม่มีทางไปแก้ข้อมูลใน UI นี้) | ช่องโหว่ |
| FR-APP-06 | AC-APP-05 | T-08, T-10 | `backend/app/auth/application.py`: `submit_band_application`; `backend/app/auth/repository.py`: `create_band_application`; `frontend/src/pages/ApplicationResultPage.jsx`: failure branch | `test_AC_APP_05_do_not_create_partial_application_on_save_failure`, `test_AC_APP_05_shows_failure_and_calls_retry_callback` (ผ่าน; แต่หน้าผลลัพธ์ไม่ได้เชื่อมในเส้นทางใช้งานจริง) | ช่องโหว่ |
| NFR-SEC-01 | ไม่มี AC | T-13 | `backend/app/auth/application.py`: `get_band_application_profile`; `backend/app/auth/repository.py`: `create_band_application`, `get_band_snapshot` | `test_T_13_requires_authentication_before_snapshot_access`, `test_AC_APP_02_store_band_snapshot_and_performance_data` (ผ่าน; การตรวจ snapshot หลังแก้ข้อมูลวงครอบคลุมเพียง `genre`) | ช่องโหว่ |
| NFR-PERF-01 | ไม่มี AC | T-13 | `backend/app/config.py`: เป้าหมาย concurrency/P95; `backend/app/auth/repository.py`: lock ใน `create_band_application` | `test_T_13_application_submission_p95_under_target_for_concurrent_bands` (ผ่าน; ส่งจาก 20 วงและตรวจ P95 ≤ 2 วินาที) | ครบ |
| PRE-APP-01 | ไม่มี AC เฉพาะ | T-01, T-03, T-05, T-07, T-09 | `backend/app/auth/application.py`: `_resolve_band_context`, `get_band_application_profile`, `validate_band_application`, `submit_band_application` | `test_T05_requires_a_valid_band_session`, `test_T_13_requires_authentication_before_snapshot_access` (ผ่าน; แต่ `GET /events/open` ยังยอมรับ `user_id` โดยไม่มี session) | ช่องโหว่ |

หมายเหตุ: `specs/000-shared/constraints.md` ไม่มี Constraint ที่ SPEC-APP-001 อ้างใช้; ตารางดังกล่าวระบุว่าใช้กับฟีเจอร์ `001-booking` เท่านั้น จึงไม่มี CON/DOM/IF เพิ่มในตารางนี้

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)

| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/auth/application.py`: `GET /events/open`, `get_open_application_events` | FR-APP-01, PRE-APP-01 | บางส่วน | กรองรายการเปิดรับสมัคร แต่รับ `user_id` โดยไม่มี session และเรียก seed ที่บังคับเปิดอีเว้นต์เดิมทุกครั้ง (F-02, F-03) |
| `backend/app/auth/application.py`: `GET /bands/me/application-profile`, `get_band_application_profile` | FR-APP-02, FR-APP-05, PRE-APP-01, NFR-SEC-01 | ส่วนใหญ่ตรง | ต้องมี session และคืนข้อมูลแบบอ่านอย่างเดียว พร้อมสถานะ field ที่ขาด; รูปแบบสมาชิกยังไม่ยืนยันชื่อและตำแหน่ง/เครื่องดนตรี (F-04) |
| `backend/app/auth/application.py`: `POST /applications/validate`, `validate_band_application` | FR-APP-03, FR-APP-05, PRE-APP-01 | บางส่วน | ตรวจเพลง ชนิดเพลง ศิลปินเดิม จำนวนเพลง เวลา และความครบถ้วนของโปรไฟล์; การตรวจสมาชิกอาศัยข้อความไม่ว่างหรือจำนวนสมาชิก ไม่ตรวจรายละเอียดที่ FR-APP-02 บังคับ (F-04) |
| `backend/app/auth/application.py`: `POST /applications`, `submit_band_application` | FR-APP-04, FR-APP-06, PRE-APP-01, NFR-PERF-01 | บางส่วน | ตรวจซ้ำก่อนบันทึกและจัดการ `BandApplicationSaveError`; มี service/API แต่ UI ไม่เรียก `createBandApplication` จากฟอร์ม (F-01) |
| `backend/app/auth/repository.py`: `list_open_application_events`, `seed_open_band_application_events` | FR-APP-01, Q-02 | ไม่ตรงทั้งหมด | event ID, ชื่อ, สถานที่ และ capacity เป็นค่าตัวอย่างคงที่ใน runtime; เมื่อพบ event เดิมจะตั้ง `registration_open=True` แม้เดิมปิดอยู่ (F-03, F-05) |
| `backend/app/auth/repository.py`: `create_band_snapshot`, `get_band_snapshot`, `create_band_application`, `get_band_application` | FR-APP-02, FR-APP-04, ASM-03, ASM-06, NFR-SEC-01 | ส่วนใหญ่ตรง | เก็บสำเนาแยกจาก profile และ status เริ่มต้นเป็น “รอตรวจสอบ”; repository เก็บข้อมูลในหน่วยความจำ จึงยังไม่ยืนยันการคงอยู่หลัง process restart |
| `backend/app/auth/application.py`: `_derive_band_profile`, `_resolve_band_context` | FR-APP-02, PRE-APP-01, NFR-SEC-01 | บางส่วน | ข้อมูลจาก session จำกัดเป็นวง แต่ `_resolve_band_context` มีทางสำรองตรวจเพียง user ID สำหรับรายการอีเว้นต์; `members` ใช้ `member_count` เป็น fallback ได้ (F-02, F-04) |
| `frontend/src/api/client.js`: `getOpenApplicationEvents`, `getBandApplicationProfile`, `validateBandApplication`, `createBandApplication` | FR-APP-01–06, PRE-APP-01 | บางส่วน | API client ส่ง session ให้ทุก call; `createBandApplication` ถูกเรียกจาก `ApplicationResultPage` เท่านั้น ซึ่งไม่มี component ใด import ไปใช้งานจริง (F-01) |
| `frontend/src/pages/SelectEventPage.jsx`: `SelectEventPage` | FR-APP-01, FR-APP-02 | ส่วนประกอบตรง แต่ยังไม่ถูกเรียก | โหลดอีเว้นต์และเปิดฟอร์มได้เมื่อ mount; ไม่มีการเชื่อมจาก `App.jsx` (F-01) |
| `frontend/src/pages/BandApplicationPage.jsx`: `BandApplicationPage`, `validateApplication` | FR-APP-02, FR-APP-03, FR-APP-05 | บางส่วน | แสดงข้อมูลวง/ฟอร์มและตรวจ validation; เมื่อ valid แสดงว่า “ยังไม่ได้บันทึกใบสมัคร” และไม่มี action ส่งจริง; โปรไฟล์วงไม่ครบแล้วไม่มีทางไปแก้ (F-01, F-08) |
| `frontend/src/pages/ApplicationResultPage.jsx`: `ApplicationResultPage` | FR-APP-04, FR-APP-06 | ส่วนประกอบตรง แต่ยังไม่ถูกเรียก | แสดงผลสำเร็จ/ล้มเหลวเมื่อ component ถูก mount แต่ไม่พบการ import หรือเรียกจาก flow ของหน้าจอ (F-01) |
| `frontend/src/App.jsx`: `App` | ไม่มี FR ของ SPEC-APP-001 | ไม่ตรงกับฟีเจอร์นี้ | แสดงจุดเริ่มต้นลงทะเบียนเข้าชมงาน ไม่ได้ mount `SelectEventPage`; `setup.test.jsx` ล้มเหลวเพราะหา “ระบบจองคิวตรวจสุขภาพ” ไม่พบ |
| `backend/app/main.py`: `app_root`, การ include routers | โครงแอปตาม T-01 | บางส่วน | include application router แต่ root ไม่ได้ส่งผู้ใช้ไปหน้าสมัครวง |
| `backend/app/auth/register.py`, `login.py`, `routes.py`; `frontend/src/pages/RegisterPage.jsx`, `LoginPage.jsx`, `CancelRegistrationPage.jsx` | นอกขอบเขต UC-06 / ฟีเจอร์อื่น | ไม่ใช้ยืนยัน SPEC-APP-001 | มี API/หน้าจอ auth, attendee registration และ cancel registration; UC-01 ระบุว่า login อยู่นอก scope ของฟีเจอร์นี้ และฟังก์ชันเหล่านี้ไม่ถูกนับเป็นการทำให้ FR ของ SPEC-APP-001 ครบ |
| `specs/006-bandapplication/mockups/UI-APP-01` ถึง `UI-APP-03` | ไม่มีข้อกำหนด UI ที่ระบุ “ต้องตรง” ใน spec | mockup มีส่วนเกิน spec | มีทางไปข้อมูลวง/สถานะสมัคร และการ retry ที่ไม่มี FR รองรับหรืออ้าง UC-07/UC-08 ซึ่งเป็น Out of scope (F-07) |

## 3. ข้อค้นพบ

ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง / ของแถม / mockup เกิน spec / ขัดกับข้อกำหนด

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | ขัดกับข้อกำหนด | `frontend/src/App.jsx`, `SelectEventPage.jsx`, `BandApplicationPage.jsx`, `ApplicationResultPage.jsx` | FR-APP-01, FR-APP-04, FR-APP-06; AC-APP-01, AC-APP-03, AC-APP-05; T-04, T-08 | `App` ไม่ได้ mount `SelectEventPage`; ฟอร์มเรียกได้เพียง validation และเมื่อ valid ระบุว่ายังไม่ได้บันทึก; `ApplicationResultPage` ไม่ถูกใช้งานจริง ดังนั้นผู้ใช้ไม่มีเส้นทาง UI ที่ส่งใบสมัคร บันทึก และเห็นผล แม้ component/backend test แยกกันผ่าน | |
| F-02 | ละเมิด Constraint | `backend/app/auth/application.py`: `_resolve_band_context`, `get_open_application_events`, `events_open_endpoint` | PRE-APP-01 | `GET /events/open` รับ `user_id` โดยไม่มี `session_id`; `_resolve_band_context` ตรวจเพียงว่ามี user และเป็น role band จึงเปิดรายการอีเว้นต์ได้โดยไม่ยืนยันว่าผู้ใช้เข้าสู่ระบบ | |
| F-03 | ขัดกับข้อกำหนด | `backend/app/auth/repository.py`: `seed_open_band_application_events` | FR-APP-01, PRE-APP-01 | ทุกครั้งที่เรียก seed หากพบอีเว้นต์เดิม โค้ดตั้ง `registration_open=True` โดยไม่รักษาสถานะเดิม ทำให้อีเว้นต์ที่ปิดรับสมัครถูกนำกลับมาแสดงว่าเปิดรับสมัคร | |
| F-04 | ขัดกับข้อกำหนด | `backend/app/models/auth.py`: `BandProfile`; `backend/app/auth/application.py`: `_derive_band_profile`, `validate_band_application` | FR-APP-02, FR-APP-03, ASM-04 | ข้อมูลโปรไฟล์รองรับ `member_count` แต่ไม่มีโครงสร้างตรวจชื่อสมาชิกและตำแหน่ง/เครื่องดนตรี; `_derive_band_profile` ใช้จำนวนสมาชิกเป็น `members` ได้ และ validation ยอมรับค่าที่ไม่ว่าง/จำนวนที่ไม่เป็นศูนย์ จึงอาจผ่านทั้งที่ไม่มีข้อมูลสมาชิกตามที่กำหนด | |
| F-05 | ของแถม | `backend/app/auth/repository.py`: `seed_open_band_application_events`; `backend/app/config.py`: `BAND_APPLICATION_EVENT_IDS` | FR-APP-01; กฎ AGENTS.md ข้อ 8 | ข้อมูลตัวอย่างชื่ออีเว้นต์และสถานที่จาก mockup ถูกกำหนดเป็น seed ใน runtime ที่ endpoint เรียกทุกครั้ง จึงไม่ใช่เพียงข้อมูล mock สำหรับ UI และจำกัดรายการที่ระบบคืนเป็นข้อมูลตัวอย่างคงที่; ให้ทีมยืนยันว่าต้องเป็น seed สำหรับใช้งานจริงหรือไม่ | |
| F-06 | test อ่อน | `backend/tests/test_band_application_save.py`: `test_AC_APP_02_store_band_snapshot_and_performance_data`; `frontend/src/__tests__/BandApplicationPages.test.jsx`: `test_T04_shows_band_data_read_only_and_cover_artist_field` | FR-APP-02, AC-APP-02, NFR-SEC-01 | test snapshot เปลี่ยนและตรวจเฉพาะ `genre` ไม่ได้ยืนยันว่า band name, members, contact name/phone ยังคงเป็นค่าขณะสมัคร; UI test ตรวจ read-only เฉพาะชื่อวงและแนวเพลง จึงยังมีการลบ/เปลี่ยน field อื่นได้โดย test ไม่ล้ม | |
| F-07 | mockup เกิน spec | `specs/006-bandapplication/mockups/UI-APP-01-select-event.html`, `UI-APP-02-application-form.html`, `UI-APP-03-result.html` | Out of scope UC-07, UC-08; ไม่มี FR รองรับการ retry | mockup มีทางไป “ข้อมูลวง” (UC-07), “สถานะการสมัคร”/“ดูสถานะการสมัคร” (UC-08) และปุ่ม retry หลังบันทึกล้มเหลว แต่ spec ไม่ได้กำหนด UI เหล่านี้และ UC-07/UC-08 อยู่ใน Out of scope; ต้องให้ทีมยืนยันส่วน mockup ที่จะคงไว้ ไม่ถือเป็นงานที่ขาดจากโค้ด | |
| F-08 | ขัดกับข้อกำหนด | `frontend/src/pages/BandApplicationPage.jsx`: branch `!isBandProfileComplete` | FR-APP-05, ASM-02 | เมื่อข้อมูลวงจาก UC-07 ไม่ครบ UI แสดงให้ไปแก้ในเมนูข้อมูลวงและปิดปุ่มส่ง แต่ไม่มี link/navigation ไปยังหน้าข้อมูลวงหรือทางแก้ข้อมูล จึงยังไม่เห็นวิธีที่ผู้ใช้จะแก้ข้อมูลที่เกี่ยวข้องก่อนกลับมาส่งตาม FR-APP-05 | |

## 4. แก้แล้ว

| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|

## สรุปการทดสอบและข้อจำกัด

- Backend: `58 passed`, `0 failed`, มี Starlette deprecation warning 1 รายการ
- Frontend: `26 passed`, `1 failed` จาก 27 tests; `setup.test.jsx` คาดหวัง “ระบบจองคิวตรวจสุขภาพ” แต่ `App.jsx` แสดง “ระบบลงทะเบียนเข้าชมงาน” จึงไม่ใช่ failure จาก test ของ Band Application โดยตรง
- ใน `test-cases.md` มี AC-APP-01 จำนวน 7 แถวสถานะ “ใช้ได้”; AC-APP-02 ถึง AC-APP-05 ยังเป็น “ร่าง” ทั้งหมด ไม่มี test จากแถวเหล่านี้ที่ถือว่าได้รับอนุมัติแล้ว
- ข้อมูลใน `AuthRepository` เป็น in-memory; spec ไม่ระบุการคงอยู่หลัง process restart จึงยังสรุปความคงทนของข้อมูลจากการทดสอบรอบนี้ไม่ได้
- `tasks.md` ในจุดตรวจเฟส 3 ยังระบุว่า Q-02 ค้าง แม้ spec ระบุว่าปิดแล้ว; ไม่ได้แก้ไฟล์ตามขอบเขต `/verify`
