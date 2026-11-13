import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'

import * as apiModule from '../api/client.js'
import LoginPage from '../pages/LoginPage.jsx'
import RegisterPage from '../pages/RegisterPage.jsx'

function calculateP95(values) {
  if (!values.length) return 0

  const sorted = [...values].sort((a, b) => a - b)
  const index = Math.max(0, Math.min(sorted.length - 1, Math.ceil(0.95 * sorted.length) - 1))
  return sorted[index]
}

test('test_AC_AUTH_06_response_time_under_3s[register]', async () => {
  const durations = []
  const registerSpy = vi.spyOn(apiModule.api, 'register').mockImplementation(async (payload) => {
    await new Promise((resolve) => setTimeout(resolve, 5))
    return {
      success: true,
      redirectTo: '/dashboard',
      user: {
        id: payload.email,
        role: 'student',
        full_name_or_band_name: payload.fullNameOrBandName,
      },
    }
  })

  for (let index = 0; index < 50; index += 1) {
    const startedAt = performance.now()
    const { unmount } = render(<RegisterPage onNavigate={vi.fn()} />)

    fireEvent.change(screen.getByLabelText(/ชื่อ-สกุล \/ ชื่อวง/i), {
      target: { value: `นักศึกษา ${index}` },
    })
    fireEvent.change(screen.getByLabelText(/อีเมล/i), {
      target: { value: `student${index.toString().padStart(2, '0')}@ku.th` },
    })
    fireEvent.change(screen.getByLabelText(/^รหัสผ่าน/i), {
      target: { value: 'P@ssword123' },
    })
    fireEvent.change(screen.getByLabelText(/^ยืนยันรหัสผ่าน/i), {
      target: { value: 'P@ssword123' },
    })
    fireEvent.change(screen.getByLabelText(/รหัสนักศึกษา/i), {
      target: { value: `650${index.toString().padStart(2, '0')}` },
    })
    fireEvent.change(screen.getByLabelText(/รหัสมหาวิทยาลัย/i), {
      target: { value: 'KU' },
    })

    fireEvent.click(screen.getAllByRole('button', { name: /สมัครสมาชิก/i }).at(-1))

    await waitFor(() => {
      expect(registerSpy).toHaveBeenCalledTimes(index + 1)
    })

    durations.push(performance.now() - startedAt)
    unmount()
  }

  const p95 = calculateP95(durations)
  expect(p95).toBeLessThanOrEqual(3000)
})

test('test_AC_AUTH_06_response_time_under_3s[login]', async () => {
  const durations = []
  const loginSpy = vi.spyOn(apiModule.api, 'login').mockImplementation(async (payload) => {
    await new Promise((resolve) => setTimeout(resolve, 5))
    return {
      success: true,
      redirectTo: '/dashboard',
      user: {
        id: payload.email,
        role: 'student',
        full_name_or_band_name: 'นักศึกษา ทดสอบ',
      },
    }
  })

  for (let index = 0; index < 50; index += 1) {
    const startedAt = performance.now()
    const navigateSpy = vi.fn()
    const { unmount } = render(<LoginPage onNavigate={navigateSpy} />)

    fireEvent.change(screen.getByLabelText(/อีเมล/i), {
      target: { value: `student${index.toString().padStart(2, '0')}@ku.th` },
    })
    fireEvent.change(screen.getByLabelText(/^รหัสผ่าน/i), {
      target: { value: 'P@ssword123' },
    })

    fireEvent.click(screen.getByRole('button', { name: /เข้าสู่ระบบ/i }))

    await waitFor(() => {
      expect(loginSpy).toHaveBeenCalledTimes(index + 1)
    })

    await waitFor(() => {
      expect(navigateSpy).toHaveBeenCalledWith('/dashboard')
    })

    durations.push(performance.now() - startedAt)
    unmount()
  }

  const p95 = calculateP95(durations)
  expect(p95).toBeLessThanOrEqual(3000)
})
