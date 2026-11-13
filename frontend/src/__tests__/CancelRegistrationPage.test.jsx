import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'

import { api } from '../api/client.js'
import CancelRegistrationPage from '../pages/CancelRegistrationPage.jsx'

vi.mock('../api/client.js', () => ({
  api: {
    getMyRegistrations: vi.fn(),
    cancelRegistration: vi.fn(),
  },
}))

test('test_AC_CXL_01_cancel_registration_after_confirmation', async () => {
  api.getMyRegistrations.mockResolvedValue({
    success: true,
    user_id: 42,
    registrations: [
      {
        registration_id: 11,
        event_id: 'evt-1',
        event_name: 'ดนตรีในสวน ครั้งที่ 5',
        status: 'ลงทะเบียน',
        registered_at: '10 พ.ย. 2569',
      },
    ],
  })
  api.cancelRegistration.mockResolvedValue({
    success: true,
    registration_id: 11,
    message: 'ยกเลิกการลงทะเบียนสำเร็จ',
  })

  render(<CancelRegistrationPage user={{ id: 42, role: 'student', full_name_or_band_name: 'สมชาย ใจดี' }} />)

  expect((await screen.findAllByText('การลงทะเบียนของฉัน')).length).toBeGreaterThan(0)
  fireEvent.click(screen.getByRole('button', { name: 'ยกเลิกการลงทะเบียน' }))

  expect(screen.getByText('ยืนยันการยกเลิกการลงทะเบียน?')).toBeTruthy()
  fireEvent.click(screen.getByRole('button', { name: 'ยืนยันการยกเลิก' }))

  await waitFor(() => {
    expect(api.cancelRegistration).toHaveBeenCalledWith({ user_id: 42, registration_id: 11 })
  })
  await waitFor(() => {
    expect(screen.getByText('ยกเลิกการลงทะเบียนแล้ว')).toBeTruthy()
  })
  expect(screen.getByText('สถานะเปลี่ยนเป็น "ยกเลิก" และคืนที่นั่งให้อีเว้นต์แล้ว')).toBeTruthy()
})

test('test_AC_CXL_04_keep_registration_when_not_confirmed', async () => {
  api.getMyRegistrations.mockResolvedValue({
    success: true,
    user_id: 42,
    registrations: [
      {
        registration_id: 12,
        event_id: 'evt-2',
        event_name: 'ดนตรีในสวน ครั้งที่ 5',
        status: 'ลงทะเบียน',
        registered_at: '10 พ.ย. 2569',
      },
    ],
  })

  render(<CancelRegistrationPage user={{ id: 42, role: 'student', full_name_or_band_name: 'สมชาย ใจดี' }} />)

  expect((await screen.findAllByText('การลงทะเบียนของฉัน')).length).toBeGreaterThan(0)
  fireEvent.click(screen.getByRole('button', { name: 'ยกเลิกการลงทะเบียน' }))

  expect(screen.getByText('ยืนยันการยกเลิกการลงทะเบียน?')).toBeTruthy()
  fireEvent.click(screen.getByRole('button', { name: 'ไม่ยืนยัน' }))

  expect(screen.queryByText('ยืนยันการยกเลิกการลงทะเบียน?')).toBeNull()
  expect(screen.getByText('ดนตรีในสวน ครั้งที่ 5')).toBeTruthy()
  expect(screen.getByText('ลงทะเบียน')).toBeTruthy()
})

test('test_T_10_shows_current_registered_count_for_event', async () => {
  api.getMyRegistrations.mockResolvedValue({
    success: true,
    user_id: 42,
    registrations: [
      {
        registration_id: 14,
        event_id: 'evt-4',
        event_name: 'ดนตรีในสวน ครั้งที่ 5',
        status: 'ลงทะเบียน',
        registered_at: '10 พ.ย. 2569',
        registered_count: 12,
      },
    ],
  })

  render(<CancelRegistrationPage user={{ id: 42, role: 'student', full_name_or_band_name: 'สมชาย ใจดี' }} />)

  expect((await screen.findAllByText('การลงทะเบียนของฉัน')).length).toBeGreaterThan(0)
  expect(screen.getByText('ผู้ลงทะเบียนปัจจุบัน: 12 คน')).toBeTruthy()
})

test('test_AC_CXL_05_reject_cancellation_when_registration_not_found', async () => {
  api.getMyRegistrations.mockResolvedValue({
    success: true,
    user_id: 42,
    registrations: [
      {
        registration_id: 13,
        event_id: 'evt-3',
        event_name: 'ดนตรีในสวน ครั้งที่ 5',
        status: 'ลงทะเบียน',
        registered_at: '10 พ.ย. 2569',
      },
    ],
  })
  api.cancelRegistration.mockResolvedValue({
    success: false,
    message: 'ไม่พบข้อมูลการลงทะเบียน',
  })

  render(<CancelRegistrationPage user={{ id: 42, role: 'student', full_name_or_band_name: 'สมชาย ใจดี' }} />)

  expect((await screen.findAllByText('การลงทะเบียนของฉัน')).length).toBeGreaterThan(0)
  fireEvent.click(screen.getByRole('button', { name: 'ยกเลิกการลงทะเบียน' }))
  fireEvent.click(screen.getByRole('button', { name: 'ยืนยันการยกเลิก' }))

  await waitFor(() => {
    expect(api.cancelRegistration).toHaveBeenCalledWith({ user_id: 42, registration_id: 13 })
  })
  await waitFor(() => {
    expect(screen.getByText('ไม่พบข้อมูลการลงทะเบียน')).toBeTruthy()
  })
  expect(screen.getByText('ดนตรีในสวน ครั้งที่ 5')).toBeTruthy()
})
