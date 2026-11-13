import { render, screen, waitFor } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

import { api } from '../api/client.js'
import ScheduleListPage from '../pages/ScheduleListPage.jsx'

afterEach(() => {
  vi.restoreAllMocks()
})

describe('ScheduleListPage', () => {
  it('test_AC_SCV_06_select_event_to_view_schedule', async () => {
    vi.spyOn(api, 'getEventList').mockResolvedValue([
      { event_id: 'EVT-001', title: 'ดนตรีในสวน ครั้งที่ 5', event_date: '2026-11-20' },
      { event_id: 'EVT-002', title: 'Battle of Bands', event_date: '2026-11-22' },
    ])

    const onSelectEvent = vi.fn()
    render(<ScheduleListPage onSelectEvent={onSelectEvent} />)

    await waitFor(() => {
      expect(screen.getByText('ดนตรีในสวน ครั้งที่ 5')).toBeTruthy()
    })

    screen.getByRole('button', { name: /ดนตรีในสวน ครั้งที่ 5/i }).click()
    expect(onSelectEvent).toHaveBeenCalledWith('EVT-001')
  })
})
