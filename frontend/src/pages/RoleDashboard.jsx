import { useMemo } from 'react'

// รองรับ FR-AUTH-03 และ FR-AUTH-05 โดยแสดงเมนูและบทบาทบนหน้าหลักตามสิทธิ์
const ROLE_LABELS = {
  student: 'นักศึกษา',
  audience: 'ผู้ชม',
  band: 'วงดนตรี',
  organizer: 'ผู้จัดงาน',
  admin: 'ผู้ดูแลระบบ',
}

const MENU_BY_ROLE = {
  student: ['ข้อมูลส่วนตัว', 'ตารางงาน', 'ประวัติการใช้บริการ'],
  audience: ['ค้นหากิจกรรม', 'ตารางกิจกรรม', 'การแจ้งเตือน'],
  band: ['ข้อมูลวง', 'รายการอีเว้นต์', 'ประวัติการแสดง'],
  organizer: ['จัดการอีเว้นต์', 'รายงานผู้เข้าร่วม', 'ตั้งค่า'],
  admin: ['จัดการผู้ใช้', 'ระบบตรวจสอบ', 'รายงาน'],
}

export function navigateTo(path) {
  window.location.href = path
}

export default function RoleDashboard({ user = {}, onNavigate = navigateTo } = {}) {
  const role = user.role || 'student'
  const roleLabel = ROLE_LABELS[role] || 'ผู้ใช้'
  const accessibleMenus = useMemo(() => MENU_BY_ROLE[role] || MENU_BY_ROLE.student, [role])

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-8 text-slate-800">
      <section className="mx-auto w-full max-w-4xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">Welcome</p>
            <h1 className="mt-2 text-3xl font-bold text-slate-800">
              {user.full_name_or_band_name || 'ผู้ใช้'}
            </h1>
          </div>

          <div className="flex items-center gap-3">
            <span className="rounded-full bg-teal-50 px-3 py-1 text-sm font-semibold text-teal-800">
              {roleLabel}
            </span>
            <button
              type="button"
              onClick={() => onNavigate('/auth')}
              className="rounded-lg border border-slate-200 px-3 py-2 text-sm font-medium text-slate-700"
            >
              ออกจากระบบ
            </button>
          </div>
        </div>

        <div className="mt-6 grid gap-4 md:grid-cols-3">
          {accessibleMenus.map((menu) => (
            <div key={menu} className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-medium text-slate-600">{menu}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
