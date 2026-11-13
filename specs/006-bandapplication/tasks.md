# Tasks: สมัครเข้าร่วมแสดง (Band Application)

- Feature: สมัครเข้าร่วมแสดง (Band Application)
- Spec ID: SPEC-APP-001
- อ้างอิง: [plan.md](./plan.md)
- วันที่: 2026-11-13

สรุป:
- เฟส: 5 (เฟส 0 + 4 เฟสทำงานจริง + เฟสรอคำตอบ)
- Tasks: 13; รอ Open Questions: 0 tasks
- เฟสแรกที่ลองใช้งานได้จริง: เฟส 1 เลือกอีเว้นต์และกรอกข้อมูลใบสมัคร

## เฟส 0: ฐานราก

### T-01 ตั้งโครงสร้างระบบและฐานข้อมูลใบสมัคร
- รองรับ: PRE-APP-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03 และ T-07
- ไฟล์ที่แตะ: `backend/app/main.py`, `backend/app/models/auth.py`, `backend/app/auth/routes.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: ระบบเปิดได้พร้อมเส้นทางเริ่มต้นสำหรับอีเว้นต์และใบสมัคร และมีโครงสร้างข้อมูล `BandApplication`, `PerformanceSong`, `BandSnapshot` ที่พร้อมใช้งาน
- สถานะ: เสร็จ 

### T-02 เตรียมข้อมูลอีเว้นต์เปิดรับสมัครและ snapshot ข้อมูลวง
- รองรับ: FR-APP-01, FR-APP-02
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-03, T-05, T-07
- ไฟล์ที่แตะ: `backend/app/models/auth.py`, `backend/app/auth/repository.py`, `backend/app/config.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: มีข้อมูลตัวอย่างอีเว้นต์ที่เปิดรับสมัคร และโครง snapshot ของชื่อวง แนวเพลง สมาชิก ผู้ติดต่อ และข้อมูลที่ต่อจาก UC-07 พร้อมใช้งานสำหรับฟอร์มสมัคร
- สถานะ: เสร็จ

#### จุดตรวจเฟส 0
- test ที่ต้องผ่านทั้งหมด: test ของเฟสก่อนหน้าไม่มี; จุดตรวจคือ route เริ่มต้นและ model snapshot เริ่มทำงาน
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม PRE-APP-01:
  Given วงเข้าสู่ระบบแล้ว และมีข้อมูลอีเว้นต์ที่เปิดรับสมัครและข้อมูลวงจาก UC-07
  When เปิดหน้าเริ่มสมัครและเรียก API เปิดรายการอีเว้นต์
  Then ระบบแสดงรายการอีเว้นต์ที่เปิดรับสมัครได้และพร้อมให้งานต่อ
- ยังขาด: ไม่มี

## เฟส 1: เลือกอีเว้นต์และตรวจข้อมูลวงก่อนส่ง (AC-APP-01, AC-APP-02)

### T-03 สร้าง API รายการอีเว้นต์เปิดรับสมัครและข้อมูลวงของวง
- รองรับ: FR-APP-01, FR-APP-02, PRE-APP-01
- ตรวจด้วย: AC-APP-01, AC-APP-02
- ไฟล์ที่แตะ: `backend/app/auth/application.py`, `backend/app/auth/repository.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: API คืน `GET /events/open` และ `GET /bands/me/application-profile` พร้อมข้อมูลวงแบบอ่านอย่างเดียวและระดับความครบถ้วนของข้อมูลวงสำหรับการสมัคร
- สถานะ: เสร็จ

### T-04 ทำหน้าจอเลือกอีเว้นต์และแสดงข้อมูลวงแบบแก้ไขไม่ได้
- รองรับ: FR-APP-01, FR-APP-02
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงาน UI รองรับ AC-APP-01 และ AC-APP-02; ตรวจด้วย `test_T04_select_event_and_show_readonly_band_profile`
- ไฟล์ที่แตะ: `frontend/src/pages/SelectEventPage.jsx`, `frontend/src/pages/BandApplicationPage.jsx`, `frontend/src/api/client.js`, `frontend/src/__tests__/BandApplicationPages.test.jsx`
- แบบหน้าจอ: `UI-APP-01-select-event.html`, `UI-APP-02-application-form.html`
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ผู้ใช้เลือกอีเว้นต์เปิดรับสมัครแล้วเปิดฟอร์มได้ เห็นข้อมูลวงจาก UC-07 แบบอ่านอย่างเดียวและฟอร์มข้อมูลเพลง/การแสดง โดยส่ง `sessionId` ผ่าน API และ `test_T04_select_event_and_show_readonly_band_profile` ผ่าน
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 1
- test ที่ต้องผ่านทั้งหมด: `test_AC_APP_01_create_application_for_selected_event`, `test_AC_APP_02_store_band_snapshot_and_performance_data`, และ test ของเฟส 0
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-APP-01 และ AC-APP-02:
  Given วงที่เข้าสู่ระบบแล้ว เลือกอีเว้นต์ที่เปิดรับสมัคร และมีข้อมูลวงพร้อมใช้งานจาก UC-07
  When ผู้ใช้เลือกอีเว้นต์และเปิดฟอร์มสมัคร
  Then ระบบแสดงอีเว้นต์ที่เลือกและข้อมูลวงที่เป็น snapshot สำหรับการสมัครตามฟอร์ม
- ยังขาด: ไม่มี

## เฟส 2: ส่งใบสมัครสำเร็จและแสดงสถานะ "รอตรวจสอบ" (AC-APP-01, AC-APP-02, AC-APP-03)

### T-05 สร้าง validation ใบสมัครและตรวจเงื่อนไขข้อจำกัดของอีเว้นต์
- รองรับ: FR-APP-03, FR-APP-05, PRE-APP-01
- ตรวจด้วย: AC-APP-04
- ไฟล์ที่แตะ: `backend/app/auth/application.py`, `backend/app/auth/repository.py`, `backend/app/config.py`, `backend/tests/test_band_application_validation.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ระบบตรวจว่าข้อมูลบังคับครบถ้วน รายชื่อเพลงอย่างน้อย 1 เพลง ความยาวการแสดงรวมและจำนวนเพลงไม่เกินค่าที่ผู้จัดงานกำหนด และแจ้งผลลัพธ์ให้ฟอร์มรองรับได้
- สถานะ: เสร็จ

### T-06 ทำหน้าแบบฟอร์มข้อมูลเพลง/การแสดงพร้อมข้อความ validation
- รองรับ: FR-APP-02, FR-APP-03, FR-APP-05
- ตรวจด้วย: AC-APP-04
- ไฟล์ที่แตะ: `frontend/src/pages/BandApplicationPage.jsx`, `frontend/src/api/client.js`, `frontend/src/__tests__/BandApplicationPages.test.jsx`
- แบบหน้าจอ: `UI-APP-02-application-form.html`
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: ผู้ใช้เห็นข้อความแจ้งเมื่อข้อมูลบังคับไม่ครบ หรือข้อจำกัดอีเว้นต์ถูกเกิน และยังไม่สามารถกดส่งใบสมัครได้จนกว่าจะแก้ไขให้ถูกต้อง
- สถานะ: เสร็จ

### T-07 สร้าง API บันทึกใบสมัคร snapshot พร้อมสถานะ "รอตรวจสอบ"
- รองรับ: FR-APP-04, ASM-03, ASM-06
- ตรวจด้วย: AC-APP-01, AC-APP-02, AC-APP-03
- ไฟล์ที่แตะ: `backend/app/auth/application.py`, `backend/app/auth/repository.py`, `backend/tests/test_band_application_save.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: เมื่อข้อมูลถูกต้อง ระบบบันทึกสำเนาข้อมูลวงและข้อมูลเพลง/การแสดงไว้กับใบสมัคร รวมถึง `status = "รอตรวจสอบ"` และผูกกับอีเว้นต์ที่เลือก
- สถานะ: เสร็จ

### T-08 ทำหน้าผลการส่งใบสมัครและแสดงสถานะ "รอตรวจสอบ"
- รองรับ: FR-APP-04, FR-APP-06
- ตรวจด้วย: AC-APP-03, AC-APP-05
- ไฟล์ที่แตะ: `frontend/src/pages/ApplicationResultPage.jsx`, `frontend/src/api/client.js`, `frontend/src/__tests__/ApplicationResultPage.test.jsx`
- แบบหน้าจอ: `UI-APP-03-result.html`
- ต้องทำหลัง: T-07
- เสร็จเมื่อ: ผู้ใช้เห็นข้อความ “ส่งใบสมัครแล้ว” พร้อมสถานะ “รอตรวจสอบ” และเมื่อบันทึกไม่สำเร็จเห็นข้อความ “ส่งใบสมัครไม่สำเร็จ” โดยไม่มีใบสมัครที่ไม่สมบูรณ์
- สถานะ: เสร็จ 

#### จุดตรวจเฟส 2
- test ที่ต้องผ่านทั้งหมด: `test_AC_APP_01_create_application_for_selected_event`, `test_AC_APP_02_store_band_snapshot_and_performance_data`, `test_AC_APP_03_show_pending_review_status`, และ test ของเฟส 1
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-APP-01 ถึง AC-APP-03:
  Given วงกรอกข้อมูลครบถ้วนและยกเลิกปัญหาจาก validation แล้ว
  When ผู้ใช้กดส่งใบสมัคร
  Then ระบบบันทึกใบสมัครสำเร็จ ผูกกับอีเว้นต์ที่เลือก และแสดงสถานะ "รอตรวจสอบ"
- ยังขาด: ไม่มี

## เฟส 3: ป้องกันใบสมัครที่ไม่สมบูรณ์และเกินข้อจำกัด (AC-APP-04)

### T-09 ปฏิเสธการส่งเมื่อข้อมูลไม่ครบหรือเกินข้อจำกัดของอีเว้นต์
- รองรับ: FR-APP-03, FR-APP-05
- ตรวจด้วย: AC-APP-04
- ไฟล์ที่แตะ: `backend/app/auth/application.py`, `frontend/src/pages/BandApplicationPage.jsx`, `backend/tests/test_band_application_rejection.py`
- แบบหน้าจอ: `UI-APP-02-application-form.html`
- ต้องทำหลัง: T-06
- เสร็จเมื่อ: หากข้อมูลบังคับไม่ครบ หรือความยาวการแสดงรวม/จำนวนเพลงเกินค่าที่ผู้จัดงานกำหนด ระบบไม่บันทึกใบสมัครและแจ้งให้แก้ไขก่อนส่งอีกครั้ง
- สถานะ: เสร็จ

#### จุดตรวจเฟส 3
- test ที่ต้องผ่านทั้งหมด: `test_AC_APP_04_reject_incomplete_or_over_limit_application`, และ test ของเฟส 1–2
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-APP-04:
  Given วงกรอกข้อมูลบังคับไม่ครบ หรือกรอกความยาว/จำนวนเพลงเกินข้อจำกัดของอีเว้นต์
  When กดส่งใบสมัคร
  Then ระบบให้แก้ไขข้อมูลก่อนส่ง และไม่บันทึกใบสมัครไว้ในระบบ
- ยังขาด: Q-02 (ค่าความยาว/จำนวนเพลงสูงสุดยังไม่ได้กำหนดใน spec)

## เฟส 4: จัดการบันทึกล้มเหลวและแจ้งข้อผิดพลาด (AC-APP-05)

### T-10 จัดการกรณีระบบบันทึกใบสมัครไม่สำเร็จและแสดงข้อความผิดพลาด
- รองรับ: FR-APP-06
- ตรวจด้วย: AC-APP-05
- ไฟล์ที่แตะ: `backend/app/auth/application.py`, `backend/app/auth/repository.py`, `frontend/src/pages/ApplicationResultPage.jsx`, `backend/tests/test_band_application_save_failure.py`
- แบบหน้าจอ: `UI-APP-03-result.html`
- ต้องทำหลัง: T-07
- เสร็จเมื่อ: เมื่อการบันทึกใบสมัครล้มเหลว ระบบแจ้งว่าการส่งไม่สำเร็จ และยังไม่มีใบสมัครที่ไม่สมบูรณ์ถูกสร้างในฐานข้อมูล
- สถานะ: เสร็จ

#### จุดตรวจเฟส 4
- test ที่ต้องผ่านทั้งหมด: `test_AC_APP_05_do_not_create_partial_application_on_save_failure`, และ test ของเฟส 1–3
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม AC-APP-05:
  Given ระบบไม่สามารถบันทึกใบสมัครได้ระหว่างส่ง
  When วงกดส่งใบสมัคร
  Then ระบบแจ้งว่าส่งไม่สำเร็จ และไม่มีใบสมัครที่ไม่สมบูรณ์ในระบบ
- ยังขาด: ไม่มี

## เฟส 5: งานเพิ่มเติมและคำตอบที่ยังรอ

### T-11 อนุญาตการสมัครอีเว้นต์เดิมซ้ำ
- รองรับ: Q-01 (ปิดแล้ว: อนุญาตให้สมัครอีเว้นต์เดียวกันซ้ำ)
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานรองรับกติกาการสมัครซ้ำ
- ไฟล์ที่แตะ: `backend/app/auth/application.py`, `backend/app/auth/repository.py`, `backend/tests/test_band_application_duplicates.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-07
- เสร็จเมื่อ: วงส่งใบสมัครสำหรับอีเว้นต์เดิมซ้ำได้ และระบบไม่ปฏิเสธใบสมัครเพียงเพราะมีใบสมัครเดิม
- สถานะ: เสร็จ

### T-12 กำหนดค่าข้อจำกัดสูงสุดของความยาวการแสดงรวมและจำนวนเพลงตามอีเว้นต์
- รองรับ: Q-02
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานรองรับข้อจำกัดจริงของอีเว้นต์
- ไฟล์ที่แตะ: `backend/app/config.py`, `backend/app/auth/application.py`, `frontend/src/pages/BandApplicationPage.jsx`
- แบบหน้าจอ: `UI-APP-02-application-form.html`
- ต้องทำหลัง: T-05
- เสร็จเมื่อ: ข้อจำกัด 30 นาทีและ 8 เพลงใช้ร่วมกันทุกอีเว้นต์ และมีข้อมูลตัวอย่างสำหรับทดสอบโดยไม่ต้องเดาค่า
- สถานะ: เสร็จ

### T-13 กำหนดมาตรการความปลอดภัยและเป้าหมายประสิทธิภาพของการส่งใบสมัคร
- รองรับ: NFR-SEC-01, NFR-PERF-01, Q-03 (ปิดแล้ว)
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานรองรับความปลอดภัยและ performance target
- ไฟล์ที่แตะ: `backend/app/config.py`, `backend/app/auth/application.py`, `backend/tests/test_auth_performance.py`
- แบบหน้าจอ: ไม่มี
- ต้องทำหลัง: T-07
- เสร็จเมื่อ: ต้องยืนยันตัวตนก่อนเข้าถึง snapshot และการส่งใบสมัครจาก 20 วงพร้อมกันมี P95 ไม่เกิน 2 วินาที
- สถานะ: เสร็จ

#### จุดตรวจเฟส 5
- test ที่ต้องผ่านทั้งหมด: test ของเฟส 0–4 และ T-11 ถึง T-13
- เปิดระบบ: Backend: `cd backend && uvicorn app.main:app --reload --port 8000` | Frontend: `cd frontend && npm run dev`
- คนลองเองตาม Q-01 ถึง Q-03:
  Given ทีมตอบคำถามข้อกำหนดเพิ่มเติมแล้ว
  When ผู้ใช้ส่งใบสมัครหลายวงพร้อมกันหรือกรอกข้อมูลตามข้อจำกัดที่กำหนด
  Then ระบบต้องปฏิบัติตามกติกาที่ทีมกำหนด และยังคงรักษาความปลอดภัยและประสิทธิภาพตามเป้าหมาย
- ยังขาด: ไม่มี Open Questions

### ตารางตรวจความครบ

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-APP-01 | T-03, T-04, T-07, T-08 |
| AC-APP-02 | T-03, T-04, T-07, T-08 |
| AC-APP-03 | T-07, T-08 |
| AC-APP-04 | T-05, T-06, T-09 |
| AC-APP-05 | T-08, T-10 |

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| PRE-APP-01 | T-01, T-03, T-05, T-07, T-09 |

| FR ID | AC ที่ตรวจ FR นี้ | เฟส |
|---|---|---|
| FR-APP-01 | AC-APP-01 | เฟส 1 |
| FR-APP-02 | AC-APP-02, AC-APP-04 | เฟส 1, เฟส 2 |
| FR-APP-03 | AC-APP-04 | เฟส 2, เฟส 3 |
| FR-APP-04 | AC-APP-01, AC-APP-02, AC-APP-03 | เฟส 2 |
| FR-APP-05 | AC-APP-04 | เฟส 2, เฟส 3 |
| FR-APP-06 | AC-APP-05 | เฟส 4 |

### สิ่งที่ยังไม่ทำ
- ไม่มี Open Questions ที่ยังรอคำตอบ
