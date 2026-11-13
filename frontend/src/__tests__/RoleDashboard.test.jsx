import { render, screen } from '@testing-library/react'

import RoleDashboard from '../pages/RoleDashboard.jsx'

test('test_AC_AUTH_04_role_dashboard', () => {
  const { rerender } = render(
    <RoleDashboard
      user={{
        role: 'student',
        full_name_or_band_name: 'นางสาวสมใจ รักเรียน',
        permissions: ['view_dashboard', 'view_schedule', 'manage_own_profile'],
      }}
    />,
  )

  expect(screen.getByText('นางสาวสมใจ รักเรียน')).toBeTruthy()
  expect(screen.getByText('ข้อมูลส่วนตัว')).toBeTruthy()
  expect(screen.queryByText('จัดการผู้ใช้')).toBeNull()

  rerender(
    <RoleDashboard
      user={{
        role: 'admin',
        full_name_or_band_name: 'ผู้ดูแลระบบ',
        permissions: ['view_dashboard', 'manage_events', 'manage_users', 'manage_permissions', 'review_registrations'],
      }}
    />,
  )

  expect(screen.getAllByText('ผู้ดูแลระบบ').length).toBeGreaterThan(0)
  expect(screen.getByText('จัดการผู้ใช้')).toBeTruthy()
  expect(screen.getByText('ระบบตรวจสอบ')).toBeTruthy()
})
