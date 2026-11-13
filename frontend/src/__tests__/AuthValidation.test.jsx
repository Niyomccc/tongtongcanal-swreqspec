import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'

import * as apiModule from '../api/client.js'
import LoginPage from '../pages/LoginPage.jsx'
import RegisterPage from '../pages/RegisterPage.jsx'

test('test_AC_AUTH_03_invalid_input_shows_error', async () => {
  const registerSpy = vi.spyOn(apiModule.api, 'register').mockResolvedValue({
    success: false,
    message: 'ข้อมูลไม่ถูกต้อง',
    errors: {
      email: 'อีเมลไม่ถูกต้อง',
      password: 'รหัสผ่านต้องยาวอย่างน้อย 8 ตัวอักษร',
      fullNameOrBandName: 'กรุณาระบุชื่อ-สกุล หรือชื่อวง',
    },
  })
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
    expect(registerSpy).toHaveBeenCalled()
  })

  await waitFor(() => {
    expect(screen.getByText('อีเมลไม่ถูกต้อง')).toBeTruthy()
  })
  expect(screen.getByDisplayValue('student01@ku.th')).toBeTruthy()

  fireEvent.change(screen.getByLabelText(/อีเมล/i), {
    target: { value: 'student02@ku.th' },
  })
  registerSpy.mockResolvedValueOnce({ success: true, redirectTo: '/dashboard' })
  fireEvent.click(screen.getAllByRole('button', { name: /สมัครสมาชิก/i }).at(-1))

  await waitFor(() => {
    expect(navigateSpy).toHaveBeenCalledWith('/dashboard')
  })
})

test('test_AC_AUTH_03_invalid_input_login_error_is_generic', async () => {
  const loginSpy = vi.spyOn(apiModule.api, 'login').mockResolvedValue({
    success: false,
    message: 'อีเมลหรือรหัสผ่านไม่ถูกต้อง',
  })
  const navigateSpy = vi.fn()

  render(<LoginPage onNavigate={navigateSpy} />)

  fireEvent.change(screen.getByLabelText(/อีเมล/i), {
    target: { value: 'student01@ku.th' },
  })
  fireEvent.change(screen.getByLabelText(/^รหัสผ่าน/i), {
    target: { value: 'P@ssword123' },
  })

  fireEvent.click(screen.getByRole('button', { name: /เข้าสู่ระบบ/i }))

  await waitFor(() => {
    expect(loginSpy).toHaveBeenCalledWith({
      email: 'student01@ku.th',
      password: 'P@ssword123',
    })
  })

  await waitFor(() => {
    expect(screen.getByText('อีเมลหรือรหัสผ่านไม่ถูกต้อง')).toBeTruthy()
  })
  expect(screen.getByDisplayValue('student01@ku.th')).toBeTruthy()
  expect(screen.getByDisplayValue('P@ssword123')).toBeTruthy()
})
