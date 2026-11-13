import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'

import * as apiModule from '../api/client.js'
import RegisterPage from '../pages/RegisterPage.jsx'

beforeEach(() => {
  vi.restoreAllMocks()
  vi.spyOn(apiModule.api, 'register').mockResolvedValue({
    success: true,
    redirectTo: '/dashboard',
  })
  vi.spyOn(apiModule.api, 'registerEvent').mockResolvedValue({
    success: true,
    redirectTo: '/dashboard',
  })
})

test('test_AC_AUTH_01_register_form', async () => {
  const navigateSpy = vi.fn()

  render(<RegisterPage onNavigate={navigateSpy} />)

  fireEvent.change(screen.getByLabelText(/ชื่อ-สกุล \/ ชื่อวง/i), {
    target: { value: 'นางสาวสมใจ รักเรียน' },
  })
  fireEvent.change(screen.getByLabelText(/อีเมล/i), {
    target: { value: 'student01@ku.th' },
  })
  fireEvent.change(screen.getByLabelText(/^รหัสผ่าน/i), {
    target: { value: 'P@ssword123' },
  })
  fireEvent.change(screen.getByLabelText(/^ยืนยันรหัสผ่าน/i), {
    target: { value: 'P@ssword123' },
  })
  fireEvent.change(screen.getByLabelText(/รหัสนักศึกษา/i), {
    target: { value: '65123456' },
  })
  fireEvent.change(screen.getByLabelText(/รหัสมหาวิทยาลัย/i), {
    target: { value: 'KU' },
  })

  fireEvent.click(screen.getAllByRole('button', { name: /สมัครสมาชิก/i }).at(-1))

  await waitFor(() => {
    expect(apiModule.api.register).toHaveBeenCalledWith(
      expect.objectContaining({
        email: 'student01@ku.th',
        password: 'P@ssword123',
        confirmPassword: 'P@ssword123',
        role: 'student',
        fullNameOrBandName: 'นางสาวสมใจ รักเรียน',
        studentId: '65123456',
        universityCode: 'KU',
      }),
    )
  })

  await waitFor(() => {
    expect(navigateSpy).toHaveBeenCalledWith('/dashboard')
  })
})

test('test_AC_REG_04_reject_duplicate_registration', async () => {
  const registerEventSpy = vi.spyOn(apiModule.api, 'registerEvent')
  const user = { id: 101, fullName: 'สมชาย ใจดี', role: 'student' }
  const events = [
    {
      id: 'evt-01',
      name: 'ดนตรีในสวน ครั้งที่ 5',
      date: 'ศ 20 พ.ย. 2569 · 16.00 น.',
      location: 'ลานกิจกรรม อาคาร 5',
      remainingSeats: 8,
      capacity: 150,
    },
  ]

  render(
    <RegisterPage
      mode="event"
      user={user}
      events={events}
      existingRegistrationEventIds={['evt-01']}
    />,
  )

  expect(screen.getAllByText(/ลงทะเบียนซ้ำไม่ได้/i).length).toBeGreaterThan(0)
  expect(screen.getByText(/คุณลงทะเบียนอีเว้นต์นี้ไว้แล้ว/i)).toBeTruthy()

  const submitButton = screen.getAllByRole('button', { name: /ลงทะเบียนซ้ำไม่ได้/i })[0]
  fireEvent.click(submitButton)

  expect(registerEventSpy).not.toHaveBeenCalled()
})

test('test_AC_REG_05_full_event_ui_message', async () => {
  vi.spyOn(apiModule.api, 'registerEvent').mockResolvedValue({
    success: false,
    message: 'ที่นั่งเต็ม มีผู้ใช้อื่นยืนยันที่นั่งสุดท้ายก่อนคุณ จึงลงทะเบียนไม่สำเร็จ',
  })

  const user = { id: 101, fullName: 'สมชาย ใจดี', role: 'student' }
  const events = [
    {
      id: 'evt-02',
      name: 'ดนตรีในสวน ครั้งที่ 5',
      date: 'ศ 20 พ.ย. 2569 · 16.00 น.',
      location: 'ลานกิจกรรม อาคาร 5',
      remainingSeats: 1,
      capacity: 150,
    },
  ]

  render(<RegisterPage mode="event" user={user} events={events} />)

  fireEvent.click(screen.getByRole('button', { name: /ยืนยันการลงทะเบียน/i }))

  await waitFor(() => {
    expect(screen.getByRole('heading', { name: /ที่นั่งเต็ม/i })).toBeTruthy()
    expect(screen.getByText(/มีผู้ใช้อื่นยืนยันที่นั่งสุดท้ายก่อนคุณ/i)).toBeTruthy()
  })

  expect(screen.getByText(/ดนตรีในสวน ครั้งที่ 5/i)).toBeTruthy()
})
