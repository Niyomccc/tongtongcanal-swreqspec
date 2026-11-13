// รองรับ PRE-REG-01: หลังผู้ใช้เข้าสู่ระบบแล้วให้เห็นจุดเริ่มต้นของการลงทะเบียนอีเว้นต์
export default function App() {
  return (
    <main className="mx-auto max-w-2xl p-6">
      <section className="rounded-2xl border border-teal-200 bg-white p-6 shadow-sm">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">
          ระบบลงทะเบียนเข้าชมงาน
        </p>
        <h1 className="mt-3 text-3xl font-bold text-slate-800">ลงทะเบียนเข้าชมงาน</h1>
        <p className="mt-3 text-slate-600">
          ผู้ใช้ที่เข้าสู่ระบบแล้วสามารถเริ่มตรวจสอบอีเว้นต์ที่เปิดให้ลงทะเบียน และยืนยันการเข้าร่วมได้จากจุดเริ่มต้นนี้
        </p>
        <div className="mt-5 rounded-xl border border-slate-200 bg-slate-50 p-4">
          <p className="text-sm font-medium text-slate-700">สถานะ:</p>
          <p className="mt-1 text-sm text-slate-600">พร้อมตรวจสอบความจุของอีเว้นต์และเริ่มกระบวนการลงทะเบียน</p>
        </div>
      </section>
    </main>
  )
}
