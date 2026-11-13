# Tasks: สมัครสมาชิก / เข้าสู่ระบบ (Authentication)

- Feature: สมัครสมาชิก / เข้าสู่ระบบ (Authentication)
- Spec ID: SPEC-AUTH-001
- อ้างอิง: [plan.md](./plan.md)
- วันที่: 2026-11-13

สรุป:
- เฟส: 8 (เฟส 0–6 และเฟสรอคำตอบ)
- Tasks: 17; รอ Open Questions: 0
- เฟสแรกที่ลองใช้งานจริง: เฟส 1 สมัครสมาชิกสำเร็จ

## เฟส 0 ฐานราก

### T-01 ตั้งโครงแอปและเส้นทาง Auth
- รองรับ: FR-AUTH-01, FR-AUTH-03, PRE-AUTH-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03 และ T-05
- ไฟล์ที่แตะ: `backend/app/main.py`, `frontend/src/App.jsx`
- แบบหน้าจอ: UI-AUTH-01 `mockups/UI-AUTH-01-login.html`
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: เปิดแอปได้และ route `/auth` แสดงจุดเริ่มต้นสมัครสมาชิก/เข้าสู่ระบบสำหรับผู้ใช้ที่ยังไม่เข้าสู่ระบบ
- สถานะ: เสร็จ

### T-02 กำหนดโมเดล Auth และค่ากฎจาก spec
- รองรับ: FR-AUTH-02, FR-AUTH-05, NFR-SEC-01, NFR-PERF-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03, T-05 และ T-14
- ไฟล์ที่แตะ: `backend/app/models/auth.py`, `backend/app/config.py`, `frontend/src/config.js`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: โมเดล User, role profiles, RolePermission และ Session ตาม plan พร้อมค่าตัวเลข/กฎจาก NFR-SEC-01 และ NFR-PERF-01 อยู่ใน config ตามกติกาโครงการ โดยไม่เพิ่มนโยบายที่ spec ไม่ได้ระบุ
- สถานะ: เสร็จ

#### จุดตรวจเฟส 0
- test ที่ต้องผ่านทั้งหมด: `test_AUTH_app_startup`, `test_AUTH_models_and_config`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` (plan.md ไม่ระบุคำสั่งเปิด; ยืนยันกับทีม) | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม PRE-AUTH-01 (ไม่มี AC สำหรับฐานราก):
  Given ยังไม่ได้เข้าสู่ระบบ
  When เปิด route `/auth`
  Then เห็นจุดเริ่มต้นของหน้าสมัครสมาชิก/เข้าสู่ระบบ
- ยังขาด: plan.md ไม่ระบุฐานข้อมูลที่จะใช้และไม่ระบุคำสั่งเปิด backend; ให้ทีมเลือก/ยืนยันเทคโนโลยีที่ plan ไม่ได้กำหนด

## เฟส 1 สมัครสมาชิกสำเร็จ (AC-AUTH-01)

### T-03 สร้าง API สมัครสมาชิก
- รองรับ: FR-AUTH-02, FR-AUTH-03, FR-AUTH-05, NFR-SEC-01
- ตรวจด้วย: AC-AUTH-01
- ไฟล์ที่แตะ: `backend/app/auth/register.py`, `backend/app/auth/repository.py`, `backend/tests/test_auth_registration.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: `test_AC_AUTH_01_register_success` ผ่าน โดย API บันทึกบัญชีและข้อมูลโปรไฟล์ที่ถูกต้อง พร้อม hash รหัสผ่านและปฏิเสธบทบาทที่สมัครเองไม่ได้
- สถานะ: เสร็จ

### T-04 ทำหน้าสมัครสมาชิกตามบทบาท
- รองรับ: FR-AUTH-01, FR-AUTH-02, FR-AUTH-03, FR-AUTH-05
- ตรวจด้วย: AC-AUTH-01
- ไฟล์ที่แตะ: `frontend/src/pages/RegisterPage.jsx`, `frontend/src/api/client.js`, `frontend/src/__tests__/RegisterPage.test.jsx`
- แบบหน้าจอ: UI-AUTH-02 `mockups/UI-AUTH-02-register.html`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: `test_AC_AUTH_01_register_form` ผ่านและหน้าจอเรียก API สมัครสมาชิกผ่าน `frontend/src/api/client.js` ก่อนนำผู้ใช้ไปหน้าหลัก
- สถานะ: เสร็จ

### T-17 เชื่อม route สมัครสมาชิกจากหน้า Auth
- รองรับ: FR-AUTH-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานเชื่อม route ของ T-04
- ไฟล์ที่แตะ: `frontend/src/App.jsx`, `frontend/src/__tests__/setup.test.jsx`
- แบบหน้าจอ: UI-AUTH-02 `mockups/UI-AUTH-02-register.html`
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: เมื่อเปิด `/auth?mode=register` แอปแสดง `RegisterPage` และมี test ยืนยันว่าหน้าสมัครสมาชิกแสดงที่ route นี้
- สถานะ: เสร็จ รอทีมตรวจ

#### จุดตรวจเฟส 1
- test ที่ต้องผ่านทั้งหมด: `test_AUTH_app_startup`, `test_AUTH_models_and_config`, `test_AC_AUTH_01_register_success`, `test_AC_AUTH_01_register_form`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` (ยืนยันคำสั่งกับทีม) | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-AUTH-01:
  Given ผู้ใช้ยังไม่มีบัญชีและเลือกบทบาทนักศึกษา ผู้ชม หรือวงดนตรี
  When กรอกข้อมูลที่จำเป็นให้ถูกต้องแล้วส่งแบบฟอร์มสมัครสมาชิก
  Then ระบบบันทึกบัญชีและนำผู้ใช้ไปหน้าหลักของตนเอง
- ยังขาด: ฐานข้อมูล/วิธีเก็บข้อมูลยังไม่ระบุใน plan.md; ต้องยืนยันกับทีมก่อนเลือก implementation

## เฟส 2 เข้าสู่ระบบสำเร็จ (AC-AUTH-02)

### T-05 ตรวจบัญชีและสร้างการเข้าสู่ระบบ
- รองรับ: FR-AUTH-03, NFR-SEC-01
- ตรวจด้วย: AC-AUTH-02
- ไฟล์ที่แตะ: `backend/app/auth/login.py`, `backend/app/auth/session.py`, `backend/tests/test_auth_login.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-02, T-03
- เสร็จเมื่อ: `test_AC_AUTH_02_login_success` ผ่านสำหรับบัญชีที่มีอยู่ โดยตรวจรหัสผ่านจาก hash และคืนผลยืนยันตัวตนเพื่อไปหน้าหลัก
- สถานะ: เสร็จ

### T-06 บังคับอายุ session และการล็อกบัญชี
- รองรับ: NFR-SEC-01
- ตรวจด้วย: AC-AUTH-02
- ไฟล์ที่แตะ: `backend/app/auth/session.py`, `backend/app/auth/login.py`, `backend/tests/test_auth_security.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: `test_AUTH_session_expiry_and_lockout` ผ่านตามช่วงหมดอายุเมื่อไม่ใช้งานและจำนวนครั้ง/ระยะเวลาล็อกที่กำหนดใน config
- สถานะ: เสร็จ

### T-07 ทำหน้าเข้าสู่ระบบและเส้นทางไปหน้าหลัก
- รองรับ: FR-AUTH-01, FR-AUTH-03
- ตรวจด้วย: AC-AUTH-02
- ไฟล์ที่แตะ: `frontend/src/pages/LoginPage.jsx`, `frontend/src/pages/RoleDashboard.jsx`, `frontend/src/api/client.js`, `frontend/src/__tests__/LoginPage.test.jsx`
- แบบหน้าจอ: UI-AUTH-01 `mockups/UI-AUTH-01-login.html`; UI-AUTH-03 `mockups/UI-AUTH-03-home-by-role.html`
- ต้องทำหลัง: T-06
- เสร็จเมื่อ: `test_AC_AUTH_02_login_form` ผ่านและการส่งแบบฟอร์มผ่าน API client พาผู้ใช้ที่ยืนยันตัวตนแล้วไปยังหน้าหลักพร้อมแสดงบทบาท
- สถานะ: เสร็จ

#### จุดตรวจเฟส 2
- test ที่ต้องผ่านทั้งหมด: test ของเฟส 0–1 และ `test_AC_AUTH_02_login_success`, `test_AUTH_session_expiry_and_lockout`, `test_AC_AUTH_02_login_form`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` (ยืนยันคำสั่งกับทีม) | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-AUTH-02:
  Given ผู้ใช้มีบัญชีอยู่แล้ว
  When กรอกอีเมลและรหัสผ่านที่ถูกต้องแล้วส่งแบบฟอร์มเข้าสู่ระบบ
  Then ผู้ใช้เข้าสู่ระบบและเห็นหน้าหลักของตนเอง
- ยังขาด: ฐานข้อมูล/วิธีเก็บข้อมูลยังไม่ระบุใน plan.md; รายละเอียด session-based หรือ JWT เป็นการเลือกของทีม

## เฟส 3 แจ้งข้อมูลไม่ถูกต้องและให้แก้ไข (AC-AUTH-03)

### T-08 ตรวจข้อมูลและส่งผล validation จาก API
- รองรับ: FR-AUTH-02, FR-AUTH-04, NFR-SEC-01
- ตรวจด้วย: AC-AUTH-03
- ไฟล์ที่แตะ: `backend/app/auth/validation.py`, `backend/app/auth/register.py`, `backend/app/auth/login.py`, `backend/tests/test_auth_validation.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-03, T-05
- เสร็จเมื่อ: `test_AC_AUTH_03_invalid_input_api` ผ่านสำหรับข้อมูลไม่ครบ รูปแบบอีเมล/รหัสนักศึกษาไม่ถูกต้อง ข้อมูลซ้ำ และรหัสผ่านไม่ผ่านขั้นต่ำที่ spec ระบุ
- สถานะ: เสร็จ

### T-09 แสดงข้อผิดพลาดและคงข้อมูลให้แก้ไขได้
- รองรับ: FR-AUTH-02, FR-AUTH-04, NFR-SEC-01
- ตรวจด้วย: AC-AUTH-03
- ไฟล์ที่แตะ: `frontend/src/pages/RegisterPage.jsx`, `frontend/src/pages/LoginPage.jsx`, `frontend/src/__tests__/AuthValidation.test.jsx`
- แบบหน้าจอ: UI-AUTH-01 `mockups/UI-AUTH-01-login.html`; UI-AUTH-02 `mockups/UI-AUTH-02-register.html`
- ต้องทำหลัง: T-08
- เสร็จเมื่อ: `test_AC_AUTH_03_invalid_input_shows_error` ผ่าน โดยแสดงข้อผิดพลาดและให้แก้ข้อมูลแล้วส่งใหม่ได้ โดยไม่เปิดเผยว่าข้อมูลเข้าสู่ระบบผิดที่อีเมลหรือรหัสผ่าน
- สถานะ: เสร็จ

#### จุดตรวจเฟส 3
- test ที่ต้องผ่านทั้งหมด: test ของเฟส 0–2 และ `test_AC_AUTH_03_invalid_input_api`, `test_AC_AUTH_03_invalid_input_shows_error`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` (ยืนยันคำสั่งกับทีม) | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-AUTH-03:
  Given ผู้ใช้กรอกข้อมูลสมัครสมาชิกไม่ถูกต้อง
  When ส่งแบบฟอร์ม
  Then ระบบแจ้งช่องที่ต้องแก้ไขและผู้ใช้แก้ข้อมูลแล้วส่งใหม่ได้
- ยังขาด: ข้อกำหนดนโยบายรหัสผ่านเฉพาะหน่วยงานที่เกินกว่าขั้นต่ำใน NFR-SEC-01 ยังไม่มีรายละเอียดให้กำหนด

## เฟส 4 จำกัดสิทธิ์ตามบทบาท (AC-AUTH-04)

### T-10 บังคับใช้สิทธิ์จาก RolePermission
- รองรับ: FR-AUTH-05
- ตรวจด้วย: AC-AUTH-04
- ไฟล์ที่แตะ: `backend/app/auth/permissions.py`, `backend/app/auth/routes.py`, `backend/tests/test_auth_permissions.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: `test_AC_AUTH_04_role_permissions` ผ่าน โดย backend ตรวจสิทธิ์ของแต่ละบทบาทและไม่ให้ใช้ฟังก์ชันที่ไม่มีสิทธิ์
- สถานะ: เสร็จ

### T-11 แสดงเมนูหน้าหลักตามสิทธิ์
- รองรับ: FR-AUTH-03, FR-AUTH-05
- ตรวจด้วย: AC-AUTH-04
- ไฟล์ที่แตะ: `frontend/src/pages/RoleDashboard.jsx`, `frontend/src/api/client.js`, `frontend/src/__tests__/RoleDashboard.test.jsx`
- แบบหน้าจอ: UI-AUTH-03 `mockups/UI-AUTH-03-home-by-role.html`
- ต้องทำหลัง: T-10
- เสร็จเมื่อ: `test_AC_AUTH_04_role_dashboard` ผ่าน โดยหน้าจอแสดงเฉพาะเมนูที่ผู้ใช้ได้รับสิทธิ์และ backend ยังคงบังคับสิทธิ์เมื่อเรียกฟังก์ชัน
- สถานะ: เสร็จ

#### จุดตรวจเฟส 4
- test ที่ต้องผ่านทั้งหมด: test ของเฟส 0–3 และ `test_AC_AUTH_04_role_permissions`, `test_AC_AUTH_04_role_dashboard`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` (ยืนยันคำสั่งกับทีม) | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-AUTH-04:
  Given ผู้ใช้แต่ละบทบาทเข้าสู่ระบบแล้ว
  When เปิดหน้าหลักและลองเรียกฟังก์ชันที่มีและไม่มีสิทธิ์
  Then เห็นและใช้ได้เฉพาะฟังก์ชันตามสิทธิ์ของบทบาท
- ยังขาด: รายการสิทธิ์จริงของแต่ละบทบาทยังไม่มีใน spec; ไม่สร้างการทำงานของ UC อื่นหรือ UC-14 จาก mockup

## เฟส 5 ปฏิเสธการเข้าสู่ระบบเมื่อระบบตรวจสอบไม่ได้ (AC-AUTH-05)

### T-12 ปฏิเสธ login เมื่อฐานข้อมูลหรือ auth service ใช้ไม่ได้
- รองรับ: FR-AUTH-06
- ตรวจด้วย: AC-AUTH-05
- ไฟล์ที่แตะ: `backend/app/auth/login.py`, `backend/tests/test_auth_unavailable.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: `test_AC_AUTH_05_db_unavailable_block_login` ผ่านและไม่มี session ถูกสร้างเมื่อ backend ตรวจบัญชีไม่ได้
- สถานะ: เสร็จ

### T-13 แสดงข้อผิดพลาดเมื่อเข้าสู่ระบบไม่ได้
- รองรับ: FR-AUTH-06
- ตรวจด้วย: AC-AUTH-05
- ไฟล์ที่แตะ: `frontend/src/pages/LoginPage.jsx`, `frontend/src/__tests__/LoginUnavailable.test.jsx`
- แบบหน้าจอ: UI-AUTH-01 `mockups/UI-AUTH-01-login.html`
- ต้องทำหลัง: T-12
- เสร็จเมื่อ: `test_AC_AUTH_05_db_unavailable_message` ผ่านและหน้าจอแจ้งว่าดำเนินการไม่สำเร็จโดยไม่แสดง success state
- สถานะ: เสร็จ

#### จุดตรวจเฟส 5
- test ที่ต้องผ่านทั้งหมด: test ของเฟส 0–4 และ `test_AC_AUTH_05_db_unavailable_block_login`, `test_AC_AUTH_05_db_unavailable_message`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` (ยืนยันคำสั่งกับทีม) | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-AUTH-05:
  Given ฐานข้อมูลหรือบริการตรวจสอบบัญชีใช้งานไม่ได้
  When ส่งแบบฟอร์มเข้าสู่ระบบ
  Then ระบบไม่ให้เข้าสู่ระบบและแจ้งว่าดำเนินการไม่สำเร็จ
- ยังขาด: ยังต้องเลือก/ยืนยันวิธีจำลองฐานข้อมูลหรือ auth service ที่ไม่พร้อมสำหรับการทดสอบ

## เฟส 6 ตรวจเวลาตอบสนองเมื่อมีผู้ใช้พร้อมกัน (AC-AUTH-06)

### T-14 วัดเวลาสมัครสมาชิกภายใต้โหลด 50 คน
- รองรับ: NFR-PERF-01
- ตรวจด้วย: AC-AUTH-06
- ไฟล์ที่แตะ: `backend/tests/test_auth_performance.py`, `frontend/src/__tests__/auth-performance.test.jsx`
- แบบหน้าจอ: UI-AUTH-02 `mockups/UI-AUTH-02-register.html`; UI-AUTH-03 `mockups/UI-AUTH-03-home-by-role.html`
- ต้องทำหลัง: T-04, T-11
- เสร็จเมื่อ: `test_AC_AUTH_06_response_time_under_3s[register]` วัดจากส่งฟอร์มสมัครจนหน้าหลักแสดงผลที่ผู้ใช้พร้อมกัน 50 คนและยืนยัน p95 ไม่เกิน 3 วินาที
- สถานะ: เสร็จ

### T-15 วัดเวลาเข้าสู่ระบบภายใต้โหลด 50 คน
- รองรับ: NFR-PERF-01
- ตรวจด้วย: AC-AUTH-06
- ไฟล์ที่แตะ: `backend/tests/test_auth_performance.py`, `frontend/src/__tests__/auth-performance.test.jsx`
- แบบหน้าจอ: UI-AUTH-01 `mockups/UI-AUTH-01-login.html`; UI-AUTH-03 `mockups/UI-AUTH-03-home-by-role.html`
- ต้องทำหลัง: T-07, T-11, T-14
- เสร็จเมื่อ: `test_AC_AUTH_06_response_time_under_3s[login]` วัดจากส่งฟอร์มเข้าสู่ระบบจนหน้าหลักแสดงผลที่ผู้ใช้พร้อมกัน 50 คนและยืนยัน p95 ไม่เกิน 3 วินาที
- สถานะ: เสร็จ

#### จุดตรวจเฟส 6
- test ที่ต้องผ่านทั้งหมด: test ของเฟส 0–5 และ `test_AC_AUTH_06_response_time_under_3s[register]`, `test_AC_AUTH_06_response_time_under_3s[login]`
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` (ยืนยันคำสั่งกับทีม) | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-AUTH-06:
  Given เตรียมบัญชีทดสอบและสภาพแวดล้อมให้รองรับผู้ใช้พร้อมกัน 50 คน
  When วัดการสมัครและเข้าสู่ระบบตั้งแต่ส่งฟอร์มจนหน้าหลักแสดงผล
  Then ทั้งสองกรณีตอบสนองไม่เกิน 3 วินาทีที่ p95
- ยังขาด: plan.md ไม่ระบุเครื่องมือทดสอบโหลด; ทีมต้องเลือกเครื่องมือและสภาพแวดล้อมก่อนยืนยันผล

## เฟสสุดท้าย: รอคำตอบ

### T-16 ยืนยันรายการคำถาม Q-03 ที่อ้างถึงใน traceability
- รองรับ: NFR-SEC-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานค้างที่ spec อ้าง Q-03
- ไฟล์ที่แตะ: `specs/001-searchbook/spec.md`, `specs/001-searchbook/plan.md`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: ทีมยืนยันว่า Q-03 หมายถึงมาตรการใด หรือยืนยันว่าเป็นข้อความตกค้างและแก้ traceability/Open Questions ให้สอดคล้อง โดยไม่เดานโยบายรหัสผ่านเพิ่มเติม
- สถานะ: เสร็จ

## ตารางตรวจความครบ

### AC กับ task

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-AUTH-01 | T-03, T-04 |
| AC-AUTH-02 | T-05, T-07 |
| AC-AUTH-03 | T-08, T-09 |
| AC-AUTH-04 | T-10, T-11 |
| AC-AUTH-05 | T-12, T-13 |
| AC-AUTH-06 | T-14, T-15 |

### Constraint กับ task

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| PRE-AUTH-01 | T-01 |

ไม่มี shared constraint ใน `specs/001-searchbook/spec.md` ที่อ้างถึง `specs/000-shared/constraints.md`; ข้อจำกัดร่วมที่ระบุไว้ในไฟล์นั้นอ้างถึง 001-booking จึงไม่นำมาใช้กับฟีเจอร์นี้

### FR กับ AC และเฟส

| FR ID | AC ที่ตรวจ FR นี้ | เฟส |
|---|---|---|
| FR-AUTH-01 | AC-AUTH-01, AC-AUTH-02 | เฟส 0–2 |
| FR-AUTH-02 | AC-AUTH-01, AC-AUTH-03 | เฟส 1, 3 |
| FR-AUTH-03 | AC-AUTH-01, AC-AUTH-02 | เฟส 1–2 |
| FR-AUTH-04 | AC-AUTH-03 | เฟส 3 |
| FR-AUTH-05 | AC-AUTH-04 | เฟส 1, 4 |
| FR-AUTH-06 | AC-AUTH-05 | เฟส 5 |

## สิ่งที่ยังไม่ทำ

- Open Questions ในหัวข้อ `Assumptions & Open Questions` ของ spec: ไม่มีข้อที่ระบุเป็นคำถามค้าง หลัง Draft v2
- รายการค้างที่ spec อ้างถึง: traceability ของ NFR-SEC-01 เคยระบุ Q-03 แต่ไม่ปรากฏใน Open Questions; T-16 ได้ยืนยันว่าเป็นข้อความตกค้างและแก้ traceability ให้ชี้ไปที่ ASM-05 อย่างสอดคล้อง
- plan.md ยังไม่กำหนดฐานข้อมูล, วิธี session/JWT ที่จะใช้, รายการสิทธิ์ของแต่ละบทบาท, คำสั่งเปิด backend หรือเครื่องมือทดสอบโหลด; ให้ทีมเลือก/ยืนยันก่อน implementation โดยไม่ถือว่า CON-TECH-01 จากฟีเจอร์ 001-booking ใช้กับ Authentication
- UI-AUTH-03 แสดงเมนูของฟีเจอร์อื่น รวมถึง UC-14 ซึ่งเป็น Out of scope ของ spec นี้; tasks ครอบคลุมการอนุญาตตามสิทธิ์เท่านั้น ไม่รวมสร้างการทำงานของเมนู/UC เหล่านั้น
