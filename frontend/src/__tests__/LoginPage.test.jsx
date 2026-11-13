import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'

import * as apiModule from '../api/client.js'
import LoginPage from '../pages/LoginPage.jsx'

beforeEach(() => {
  vi.restoreAllMocks()
  vi.spyOn(apiModule.api, 'login').mockResolvedValue({
    success: true,
    redirectTo: '/dashboard',
    user: {
      id: 1,
      email: 'student01@ku.th',
      role: 'student',
      full_name_or_band_name: 'นางสาวสมใจ รักเรียน',
    },
  })
})

test('test_AC_AUTH_02_login_form', async () => {
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
    expect(apiModule.api.login).toHaveBeenCalledWith({
      email: 'student01@ku.th',
      password: 'P@ssword123',
    })
  })

  await waitFor(() => {
    expect(navigateSpy).toHaveBeenCalledWith('/dashboard')
  })

  await waitFor(() => {
    expect(screen.getByText('นางสาวสมใจ รักเรียน')).toBeTruthy()
  })
})
