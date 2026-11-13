import { useMemo } from 'react'

// รองรับ FR-AUTH-03 และ FR-AUTH-05 โดยแสดงเมนูและบทบาทบนหน้าหลักตามสิทธิ์
const ROLE_LABELS = {
  student: 'นักศึกษา',
  audience: 'ผู้ชม',
  band: 'วงดนตรี',
  organizer: 'ผู้จัดงาน',
  admin: 'ผู้ดูแลระบบ',
}

const ROLE_PERMISSIONS = {
  student: ['view_dashboard', 'view_schedule', 'manage_own_profile'],
  audience: ['view_dashboard', 'view_schedule', 'register_for_event'],
  band: ['view_dashboard', 'manage_own_band', 'view_own_bookings'],
  organizer: ['view_dashboard', 'manage_events', 'review_registrations'],
  admin: ['view_dashboard', 'manage_events', 'manage_users', 'manage_permissions', 'review_registrations'],
}

const MENU_BY_ROLE = {
  student: [
    { label: 'ข้อมูลส่วนตัว', permission: 'manage_own_profile' },
    { label: 'ตารางงาน', permission: 'view_schedule' },
    { label: 'ประวัติการใช้บริการ', permission: 'view_dashboard' },
  ],
  audience: [
    { label: 'ค้นหากิจกรรม', permission: 'view_dashboard' },
    { label: 'ตารางกิจกรรม', permission: 'view_schedule' },
    { label: 'การแจ้งเตือน', permission: 'register_for_event' },
  ],
  band: [
    { label: 'ข้อมูลวง', permission: 'manage_own_band' },
    { label: 'รายการอีเว้นต์', permission: 'view_own_bookings' },
    { label: 'ประวัติการแสดง', permission: 'view_dashboard' },
  ],
  organizer: [
    { label: 'จัดการอีเว้นต์', permission: 'manage_events' },
    { label: 'รายงานผู้เข้าร่วม', permission: 'review_registrations' },
    { label: 'ตั้งค่า', permission: 'manage_events' },
  ],
  admin: [
    { label: 'จัดการผู้ใช้', permission: 'manage_users' },
    { label: 'ระบบตรวจสอบ', permission: 'manage_permissions' },
    { label: 'รายงาน', permission: 'review_registrations' },
  ],
}

export function navigateTo(path) {
  window.location.href = path
}

export default function RoleDashboard({ user = {}, onNavigate = navigateTo } = {}) {
  const role = user.role || 'student'
  const roleLabel = ROLE_LABELS[role] || 'ผู้ใช้'

  const permissions = useMemo(() => {
    const fromUser = Array.isArray(user.permissions) ? user.permissions : []
    if (fromUser.length > 0) {
      return new Set(fromUser)
    }

    return new Set(ROLE_PERMISSIONS[role] || ROLE_PERMISSIONS.student)
  }, [role, user.permissions])

  const accessibleMenus = useMemo(() => {
    const menuOptions = MENU_BY_ROLE[role] || MENU_BY_ROLE.student
    return menuOptions.filter((menu) => {
      if (role === 'admin') return true
      return permissions.has(menu.permission)
    })
  }, [permissions, role])

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
            <div key={menu.label} className="rounded-xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm font-medium text-slate-600">{menu.label}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
