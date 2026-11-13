import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'

import * as apiModule from '../api/client.js'
import LoginPage from '../pages/LoginPage.jsx'

test('test_AC_AUTH_05_db_unavailable_message', async () => {
  const navigateSpy = vi.fn()
  vi.spyOn(apiModule.api, 'login').mockResolvedValue({
    success: false,
    message: 'ดำเนินการไม่สำเร็จ กรุณาลองใหม่',
  })

  render(<LoginPage onNavigate={navigateSpy} />)

  fireEvent.change(screen.getByLabelText(/อีเมล/i), {
    target: { value: 'student01@ku.th' },
  })
  fireEvent.change(screen.getByLabelText(/^รหัสผ่าน/i), {
    target: { value: 'P@ssword123' },
  })

  fireEvent.click(screen.getByRole('button', { name: /เข้าสู่ระบบ/i }))

  await waitFor(() => {
    expect(screen.getByText('ดำเนินการไม่สำเร็จ กรุณาลองใหม่')).toBeTruthy()
  })

  expect(navigateSpy).not.toHaveBeenCalled()
  expect(screen.queryByText('นางสาวสมใจ รักเรียน')).toBeNull()
})
