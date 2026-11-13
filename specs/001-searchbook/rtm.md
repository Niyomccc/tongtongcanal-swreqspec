# RTM: สมัครสมาชิก / เข้าสู่ระบบ (Authentication)
อ้างอิง: spec.md SPEC-AUTH-001 Draft v2 | tasks.md | test-cases.md (ทุกแถวสถานะร่าง)
สร้างด้วย /verify เมื่อ 2026-11-13 10:15 UTC | test: 19 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-AUTH-01 | AC-AUTH-01, AC-AUTH-02 | T-01, T-04, T-07 (เสร็จ) | `frontend/src/App.jsx`: `AuthStartPage`, `App`; `frontend/src/pages/RegisterPage.jsx`: `RegisterPage`; `frontend/src/pages/LoginPage.jsx`: `LoginPage` | `test_AC_AUTH_01_register_form`, `test_AC_AUTH_02_login_form` (ผ่าน; ทดสอบ component แยก ไม่ได้ทดสอบการเลือก/ส่งฟอร์มผ่าน route `/auth`) | ช่องโหว่ (F-01) |
| FR-AUTH-02 | AC-AUTH-01, AC-AUTH-03 | T-02, T-03, T-04, T-08, T-09 (เสร็จ) | `backend/app/auth/register.py`: `RegisterUserInput`, `register_user`; `backend/app/auth/validation.py`: `validate_registration_payload`; `frontend/src/pages/RegisterPage.jsx`: `validate`, `handleSubmit` | `test_AC_AUTH_01_register_success`, `test_AC_AUTH_03_invalid_input_api`, `test_AC_AUTH_03_invalid_input_shows_error` (ผ่าน; ยังไม่ครอบคลุมการข้าม confirmPassword และรูปแบบ email ที่ backend รับ) | ช่องโหว่ (F-04, F-05) |
| FR-AUTH-03 | AC-AUTH-01, AC-AUTH-02 | T-03, T-04, T-05, T-07, T-11 (เสร็จ) | `backend/app/auth/register.py`: `register_user`; `backend/app/auth/login.py`: `login_user`; `backend/app/auth/session.py`: `create_session`; `backend/app/auth/repository.py`: `AuthRepository`; `frontend/src/pages/LoginPage.jsx`, `RegisterPage.jsx` | `test_AC_AUTH_01_register_success`, `test_AC_AUTH_02_login_success`, `test_AC_AUTH_01_register_form`, `test_AC_AUTH_02_login_form` (ผ่าน; repository เก็บข้อมูลเฉพาะในหน่วยความจำ และหน้าใช้งานจริงยังไม่เชื่อม route) | ช่องโหว่ (F-01, F-03) |
| FR-AUTH-04 | AC-AUTH-03 | T-08, T-09 (เสร็จ) | `backend/app/auth/validation.py`: `validate_registration_payload`, `validate_login_payload`; `frontend/src/pages/RegisterPage.jsx`, `LoginPage.jsx`: `validate`, `handleSubmit` | `test_AC_AUTH_03_invalid_input_api`, `test_AC_AUTH_03_invalid_input_shows_error`, `test_AC_AUTH_03_invalid_input_login_error_is_generic` (ผ่าน; แสดงข้อผิดพลาดและแก้ไข/ส่งซ้ำได้) | ครบ |
| FR-AUTH-05 | AC-AUTH-04 | T-10, T-11 (เสร็จ) | `backend/app/auth/permissions.py`: `has_permission`, `require_permission`; `backend/app/auth/routes.py`: `check_permission_endpoint`, `me_endpoint`; `frontend/src/pages/RoleDashboard.jsx`: `RoleDashboard` | `test_AC_AUTH_04_role_permissions`, `test_AC_AUTH_04_role_dashboard` (ผ่าน; ทดสอบชุดสิทธิ์ที่โค้ดกำหนดเอง ไม่ยืนยันตัวผู้ใช้จาก session) | ช่องโหว่ (F-02, F-05) |
| FR-AUTH-06 | AC-AUTH-05 | T-12, T-13 (เสร็จ) | `backend/app/auth/login.py`: `login_user`; `frontend/src/pages/LoginPage.jsx`: `handleSubmit` | `test_AC_AUTH_05_db_unavailable_block_login`, `test_AC_AUTH_05_db_unavailable_message` (ผ่าน; จำลอง repository ล้มเหลวและตรวจว่าไม่สร้าง session/ไม่ redirect) | ครบ |
| NFR-PERF-01 | AC-AUTH-06 | T-14, T-15 (เสร็จ) | `backend/tests/test_auth_performance.py`; `frontend/src/__tests__/auth-performance.test.jsx` | `test_AC_AUTH_06_response_time_under_3s[register]`, `test_AC_AUTH_06_response_time_under_3s[login]` และ backend parameterized tests (ผ่าน; ไม่ได้วัดคำขอจริงตั้งแต่ submit จนหน้าแรกแสดงผลที่ผู้ใช้พร้อมกัน 50 คน) | ช่องโหว่ (F-07) |
| NFR-SEC-01 | ไม่มี AC ตรง ๆ (อ้าง ASM-05) | T-02, T-05, T-06 (เสร็จ) | `backend/app/config.py`; `backend/app/auth/register.py`: `_hash_password`; `backend/app/auth/login.py`: `login_user`; `backend/app/auth/session.py`: `create_session`, `validate_session` | `test_AUTH_session_expiry_and_lockout`, `test_AUTH_login_rejects_invalid_credentials_without_leaking_details`, `test_AC_AUTH_01_register_success` (ผ่าน; ไม่มีการทดสอบ/บังคับ TLS และไม่มีการใช้ session guard กับ route จริง) | ช่องโหว่ (F-02, F-06) |
| PRE-AUTH-01 | ไม่มี AC | T-01 (เสร็จ) | `frontend/src/App.jsx`: `App` ตรวจ pathname `/auth` | `โครงหน้าจอเปิดได้` (ผ่าน แต่ทดสอบ route หลัก `/` ไม่ได้ยืนยัน `/auth`) | ช่องโหว่ (F-01) |

ไม่มี shared constraint จาก `specs/000-shared/constraints.md` ที่ spec ฟีเจอร์นี้อ้างถึง; constraint ในไฟล์ shared อ้างถึง 001-booking เท่านั้น

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/main.py`: ประกอบ FastAPI และ Auth routers | FR-AUTH-01, FR-AUTH-03, FR-AUTH-05 | บางส่วน | API routes ถูกลงทะเบียน แต่ frontend route ไม่ได้เชื่อม `LoginPage`/`RegisterPage` และไม่มี dashboard route ใน `App` |
| `backend/app/auth/register.py`: `POST /api/auth/register`, `POST /auth/register`, `register_user` | FR-AUTH-02, FR-AUTH-03, FR-AUTH-05, NFR-SEC-01 | บางส่วน | บันทึกเฉพาะในหน่วยความจำ; field/rule บางรายการไม่มีที่มาใน spec; ยืนยันรหัสผ่านไม่จำเป็นเมื่อเรียก API โดยตรง |
| `backend/app/auth/login.py`: `POST /api/auth/login`, `POST /auth/login`, `login_user` | FR-AUTH-03, FR-AUTH-04, FR-AUTH-06, NFR-SEC-01 | บางส่วน | ตรวจ hash/lockout และส่ง generic error; session ที่สร้างไม่ถูกนำไปใช้ป้องกัน route |
| `backend/app/auth/session.py`: create/get/validate/invalidate session | FR-AUTH-03, NFR-SEC-01 | บางส่วน | มี idle expiry ใน helper แต่ไม่มี route หรือ middleware เรียกตรวจ session; store เป็นหน่วยความจำ |
| `backend/app/auth/permissions.py`: `has_permission`, `require_permission` | FR-AUTH-05 | ไม่ครบ | สิทธิ์แต่ละบทบาทถูกเลือกในโค้ดโดยไม่มี matrix ใน spec; admin bypass ขึ้นกับค่า role ที่ส่งเข้า helper |
| `backend/app/auth/routes.py`: `POST /api/auth/permissions/check` | FR-AUTH-05 | ไม่ตรง | รับ `role` จาก request body โดยไม่ตรวจ session/ตัวตนจริง จึงไม่ยืนยันว่า role เป็นของผู้เรียก |
| `backend/app/auth/routes.py`: `GET /api/auth/me` | FR-AUTH-05 | ไม่ตรง | คืน permissions ตาม query `role` ที่ caller ระบุ แทนการอ่านบทบาทของผู้ใช้ที่ยืนยันตัวตน |
| `backend/app/auth/validation.py`: validation สมัคร/เข้าสู่ระบบ | FR-AUTH-02, FR-AUTH-04, NFR-SEC-01 | บางส่วน | ตรวจอีเมลฝั่ง backend เพียงว่ามี `@`; confirmPassword ที่หายไปไม่เป็น error; กฎรูปแบบรหัสนักศึกษาเป็นค่าที่โค้ดกำหนดเอง |
| `backend/app/auth/repository.py`: `AuthRepository.create_user`, lookups | FR-AUTH-02, FR-AUTH-03 | ไม่ครบ | ใช้ dict ใน process; restart ทำให้บัญชีที่สมัครหาย |
| `backend/app/models/auth.py`: Auth SQLAlchemy entities | FR-AUTH-02, FR-AUTH-03, FR-AUTH-05, NFR-SEC-01 | บางส่วน | มี model แต่ repository/API ไม่ใช้ model เหล่านี้ในการ persist ข้อมูล |
| `frontend/src/App.jsx`: `AuthStartPage`, `App` | FR-AUTH-01, PRE-AUTH-01 | ไม่ครบ | `/auth?mode=register` ยังแสดงหน้าเดิม และปุ่ม login เป็น `type="button"` ไม่มี submit handler |
| `frontend/src/pages/RegisterPage.jsx`: `RegisterPage`, `validate`, `handleSubmit` | FR-AUTH-01, FR-AUTH-02, FR-AUTH-03, FR-AUTH-04, FR-AUTH-05 | บางส่วน | component ทำงานเมื่อเรียกโดยตรง แต่ไม่ถูก route จาก `App`; มีฟิลด์/กฎที่ spec ไม่กำหนด และ hardcode ความยาว password |
| `frontend/src/pages/LoginPage.jsx`: `LoginPage`, `handleSubmit` | FR-AUTH-01, FR-AUTH-03, FR-AUTH-04, FR-AUTH-06, NFR-SEC-01 | บางส่วน | component สร้าง dashboard ใน state หลัง login แต่ไม่ถูกใช้โดย `App` และไม่ได้เก็บ/ส่ง session |
| `frontend/src/pages/RoleDashboard.jsx`: `RoleDashboard` | FR-AUTH-03, FR-AUTH-05 | บางส่วน | เมนูและ permission sets ถูกกำหนดในโค้ด; ปุ่มออกจากระบบเพียงนำทางกลับ `/auth` ไม่ invalidate session |
| `frontend/src/api/client.js`: `api.register`, `api.login`, `api.getCurrentUser` | FR-AUTH-02, FR-AUTH-03, FR-AUTH-05, FR-AUTH-06 | บางส่วน | เรียก API ตาม path แต่ไม่มี session/cookie/token ที่เชื่อมกับการตรวจสิทธิ์ |
| `backend/app/config.py`: ค่าความปลอดภัยและประสิทธิภาพ | NFR-SEC-01, NFR-PERF-01 | บางส่วน | มีค่าขั้นต่ำรวมถึง TLS version แต่ไม่มีการตั้งค่า server/deployment ที่บังคับ TLS |
| `backend/tests/test_auth_performance.py`, `frontend/src/__tests__/auth-performance.test.jsx` | NFR-PERF-01 | ไม่ตรง | backend วัดฟังก์ชันโดยตรง ส่วน frontend ใช้ API mock และวนทีละราย ไม่ได้วัด 50 concurrent users แบบ end-to-end |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | test อ่อน | `frontend/src/App.jsx:1-71` | FR-AUTH-01, FR-AUTH-03, PRE-AUTH-01 | `App` แสดงฟอร์ม login แบบ static; ลิงก์สมัครสมาชิกเปลี่ยน query แต่ไม่เปลี่ยนหน้า และปุ่ม login ไม่มี handler; `LoginPage`/`RegisterPage` ไม่ได้เชื่อมกับ route ในแอป จึงไม่มี flow สมัคร/เข้าสู่ระบบจริงผ่านหน้าที่ผู้ใช้เปิดได้ | |
| F-02 | อ้าง ID ผิดเรื่อง | `backend/app/auth/routes.py:13-43`; `backend/app/auth/permissions.py:35-50` | FR-AUTH-05, NFR-SEC-01 | permission endpoint รับ role จาก request และ `/api/auth/me` เชื่อ role จาก query โดยไม่มีการยืนยัน session/ตัวตน; ผู้เรียกสามารถระบุ `admin` เองได้ จึงไม่ได้จำกัดสิทธิ์ตามบทบาทของผู้ใช้ที่เข้าสู่ระบบจริง | |
| F-03 | อ้าง ID ผิดเรื่อง | `backend/app/auth/repository.py:8-89` | FR-AUTH-03 | `AuthRepository` เก็บบัญชีใน dict ภายใน process แทนการ persist; เมื่อ process หยุด/เริ่มใหม่บัญชีหาย ทำให้การบันทึกสมาชิกไม่คงอยู่ตามความหมายของ FR-AUTH-03; plan/tasks ยังระบุให้ทีมยืนยันวิธีเก็บข้อมูลก่อนเลือก implementation | |
| F-04 | อ้าง ID ผิดเรื่อง | `backend/app/auth/register.py:30-60,180-185`; `backend/app/auth/validation.py:67-81` | FR-AUTH-02 | API ยอมรับ confirmPassword ที่ไม่ส่งมา และ backend ตรวจอีเมลเพียงว่ามี `@` (เช่น `x@` ผ่าน); เงื่อนไขช่องบังคับ/รูปแบบอีเมลจึงเลี่ยงได้เมื่อเรียก API โดยตรง แม้ frontend จะตรวจบางส่วน | |
| F-05 | โค้ดไม่มี FR | `backend/app/auth/validation.py:99-108`; `backend/app/auth/register.py:35-54,138-158`; `frontend/src/pages/RegisterPage.jsx:19,91-92,302-308` | FR-AUTH-02, ASM-02 | ใช้ regex รหัสนักศึกษา `[A-Za-z0-9-]+` โดยไม่มีรูปแบบมหาวิทยาลัยจาก spec; บังคับ `universityCode` ซึ่งไม่อยู่ในฟิลด์สมัครที่ ASM-02 ระบุ/ไม่มีใน mockup; API ยังรับรายละเอียดวง `memberCount`, `genre`, `performanceList` ทั้งที่ ASM-02 ระบุให้กรอกภายหลังผ่าน UC-07/UC-06 | |
| F-06 | test อ่อน | `backend/app/config.py:5-6`; `backend/app/auth/session.py:22-62`; `frontend/src/api/client.js:22-35` | NFR-SEC-01 | `MINIMUM_TLS_VERSION` เป็นเพียงค่าคงที่ ไม่มี server/deployment config หรือ test ที่ยืนยัน HTTPS TLS 1.2; session helper มี timeout แต่ไม่มี route/middleware เรียกตรวจ session และ frontend ไม่เก็บ session ที่ login คืนมา จึงไม่มีหลักฐานว่า security controls ใช้จริงใน flow | |
| F-07 | test อ่อน | `backend/tests/test_auth_performance.py:23-99`; `frontend/src/__tests__/auth-performance.test.jsx:16-110` | NFR-PERF-01, AC-AUTH-06 | backend วัด `register_user`/`login_user` โดยตรง ไม่รวม HTTP/UI/dashboard; frontend ใช้ API mock หน่วงคงที่และรัน 50 รอบเรียงกัน ไม่ได้ยิงพร้อมกัน และกรณี register ไม่ assert ว่าหน้าหลักแสดง จึงไม่ตรวจ threshold ตามช่วงวัดที่ NFR กำหนด แม้ test ทั้งหมดผ่าน | |
| F-08 | ตัวเลขฝังในโค้ด | `frontend/src/pages/RegisterPage.jsx:75`; `frontend/src/config.js` | NFR-SEC-01 | หน้าจอ hardcode ความยาว password ขั้นต่ำ `8` ซ้ำ แทนการอ่านค่าจาก `frontend/src/config.js` ตามกติกาโครงการ; config ฝั่ง frontend ปัจจุบันมีเฉพาะ API paths | |
| F-09 | โค้ดไม่มี FR | `frontend/src/pages/RoleDashboard.jsx:90-93` | ไม่มี FR รองรับ | เพิ่มปุ่ม “ออกจากระบบ” ซึ่งไม่มีใน mockup UI-AUTH-03 และไม่มี FR ใน spec; การทำงานปัจจุบันแค่นำทางกลับ `/auth` โดยไม่เรียก logout หรือยกเลิก session | |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
