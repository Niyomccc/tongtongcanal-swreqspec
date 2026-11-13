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
