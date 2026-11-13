// test ตรวจว่าโครงหน้าจอพร้อมใช้ (ไม่ใช่ test ของ AC ใด)
import { render, screen } from '@testing-library/react'
import App from '../App.jsx'

test('โครงหน้าจอเปิดได้', () => {
  render(<App />)
  expect(screen.getByRole('heading', { name: 'ระบบอีเว้นต์ดนตรีนักศึกษา' })).toBeTruthy()
  expect(screen.getByRole('link', { name: 'เข้าสู่ระบบ' }).getAttribute('href')).toBe(
    'http://127.0.0.1:5173/auth',
  )
})

test('route สมัครสมาชิกแสดงหน้าสมัครสมาชิก', () => {
  window.history.replaceState({}, '', '/auth?mode=register')

  render(<App />)

  expect(screen.getByRole('heading', { name: 'สมัครสมาชิก' })).toBeTruthy()
  expect(screen.getByText('สมัครในบทบาท')).toBeTruthy()

  window.history.replaceState({}, '', '/')
})
