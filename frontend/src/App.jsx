function AuthStartPage() {
  // แสดงทางเข้าเข้าสู่ระบบ/สมัครสมาชิกก่อนพัฒนาแบบฟอร์มตาม FR-AUTH-01
  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
      <section className="mx-auto w-full max-w-sm rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h1 className="text-xl font-bold text-teal-800">
          ระบบอีเว้นต์ดนตรีนักศึกษา
        </h1>

        <nav aria-label="การยืนยันตัวตน" className="mt-6 flex gap-2 border-b border-slate-200">
          <a
            aria-current="page"
            className="border-b-2 border-teal-700 px-3 py-2 text-sm font-semibold text-teal-800"
            href="/auth"
          >
            เข้าสู่ระบบ
          </a>
          <a
            className="px-3 py-2 text-sm text-slate-600"
            href="/auth?mode=register"
          >
            สมัครสมาชิก
          </a>
        </nav>

        <form className="mt-5 space-y-4">
          <div>
            <label className="mb-1 block text-sm text-slate-600" htmlFor="email">
              อีเมล <span aria-hidden="true">*</span>
            </label>
            <input
              autoComplete="email"
              className="w-full rounded-lg border border-slate-300 px-3 py-2"
              id="email"
              name="email"
              type="email"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm text-slate-600" htmlFor="password">
              รหัสผ่าน <span aria-hidden="true">*</span>
            </label>
            <input
              autoComplete="current-password"
              className="w-full rounded-lg border border-slate-300 px-3 py-2"
              id="password"
              name="password"
              type="password"
            />
          </div>
          <button
            className="w-full rounded-lg bg-teal-700 px-4 py-3 font-semibold text-white"
            type="button"
          >
            เข้าสู่ระบบ
          </button>
        </form>

        <p className="mt-4 text-center text-xs text-slate-500">
          ผู้จัดงานและผู้ดูแลระบบใช้หน้านี้เข้าสู่ระบบเช่นกัน
        </p>
      </section>
    </main>
  )
}

export default function App() {
  // หน้าเข้าสู่ระบบสำหรับผู้ใช้ที่ยังไม่ได้เข้าสู่ระบบตาม PRE-AUTH-01
  if (window.location.pathname === '/auth') {
    return <AuthStartPage />
  }

  // คงหน้าเริ่มต้นเดิมไว้ที่ route หลักระหว่างทยอยพัฒนาฟีเจอร์
  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="text-2xl font-bold text-teal-800">ระบบจองคิวตรวจสุขภาพ</h1>
      <p className="mt-2 text-slate-600">
        โครงหน้าจอพร้อมแล้ว หน้าจอของแต่ละ task จะอยู่ในโฟลเดอร์ src/pages/
      </p>
    </main>
  )
}
