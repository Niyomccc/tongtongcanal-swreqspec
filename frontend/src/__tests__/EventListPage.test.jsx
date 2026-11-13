import { render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'

import * as apiModule from '../api/client.js'
import EventListPage from '../pages/EventListPage.jsx'

describe('EventListPage', () => {
  it('loads event list and allows selecting an event', async () => {
    const onSelectEvent = vi.fn()
    vi.spyOn(apiModule.api, 'getEventList').mockResolvedValue([
      {
        event_id: 'EVT-001',
        title: 'ดนตรีในสวน ครั้งที่ 5',
        event_date: '2026-11-20',
        start_time: '16:00',
        end_time: '21:00',
        location: 'ลานกิจกรรม อาคาร 5',
        description: 'คอนเสิร์ตกลางแจ้งที่รวมวงดนตรี',
      },
      {
        event_id: 'EVT-002',
        title: 'Battle of Bands',
        event_date: '2026-11-22',
        start_time: '18:30',
        end_time: '22:00',
        location: 'อาคารศิลปะกลาง',
        description: 'การแข่งขันวงดนตรี',
      },
    ])

    render(<EventListPage onSelectEvent={onSelectEvent} />)

    await waitFor(() => {
      expect(screen.getByText('ดนตรีในสวน ครั้งที่ 5')).toBeTruthy()
    })

    const button = screen.getByRole('button', { name: /ดนตรีในสวน ครั้งที่ 5/i })
    button.click()

    await waitFor(() => {
      expect(onSelectEvent).toHaveBeenCalledWith('EVT-001')
    })
  })
})
