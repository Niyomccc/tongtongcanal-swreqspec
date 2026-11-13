import { render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'

import { api } from '../api/client.js'
import EventDetailPage from '../pages/EventDetailPage.jsx'

describe('EventDetailPage', () => {
  it('loads and renders event details for the selected event', async () => {
    vi.spyOn(api, 'getEventById').mockResolvedValue({
      event_id: 'EVT-001',
      title: 'ดนตรีในสวน ครั้งที่ 5',
      event_date: '2026-11-20',
      start_time: '16:00',
      end_time: '21:00',
      location: 'ลานกิจกรรม อาคาร 5',
      description: 'การแสดงดนตรีจากวงนักศึกษา 8 วง พร้อมบูธกิจกรรมและมุมอาหาร เข้าชมฟรี',
    })

    render(<EventDetailPage eventId="EVT-001" onBack={vi.fn()} />)

    await waitFor(() => {
      expect(screen.getByText('ดนตรีในสวน ครั้งที่ 5')).toBeTruthy()
    })

    expect(screen.getByText('2026-11-20')).toBeTruthy()
    expect(screen.getByText('16:00 – 21:00 น.')).toBeTruthy()
    expect(screen.getByText('ลานกิจกรรม อาคาร 5')).toBeTruthy()
    expect(screen.getByText('การแสดงดนตรีจากวงนักศึกษา 8 วง พร้อมบูธกิจกรรมและมุมอาหาร เข้าชมฟรี')).toBeTruthy()
  })

  it('test_AC_EVD_04_event_not_found', async () => {
    vi.spyOn(api, 'getEventById').mockRejectedValue(new Error('ไม่พบข้อมูลอีเว้นต์'))

    render(<EventDetailPage eventId="EVT-404" onBack={vi.fn()} />)

    await waitFor(() => {
      expect(screen.getByText('ไม่พบข้อมูลอีเว้นต์')).toBeTruthy()
    })
  })
})
