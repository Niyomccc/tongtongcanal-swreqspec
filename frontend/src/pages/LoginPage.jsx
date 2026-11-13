import { useState } from 'react'

import { api } from '../api/client.js'
import RoleDashboard from './RoleDashboard.jsx'

// รองรับ FR-AUTH-01 และ FR-AUTH-03
export function navigateTo(path) {
  window.location.href = path
}

export default function LoginPage({ onNavigate = navigateTo } = {}) {
  const [form, setForm] = useState({ email: '', password: '' })
  const [errors, setErrors] = useState({})
  const [submitError, setSubmitError] = useState('')
  const [authenticatedUser, setAuthenticatedUser] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const updateField = (field, value) => {
    setForm((current) => ({ ...current, [field]: value }))
    setErrors((current) => ({ ...current, [field]: '' }))
  }

  const validate = () => {
    const nextErrors = {}

    if (!form.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      nextErrors.email = 'อีเมลไม่ถูกต้อง'
    }

    if (!form.password) {
      nextErrors.password = 'กรุณาระบุรหัสผ่าน'
    }

    return nextErrors
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    const nextErrors = validate()
    setErrors(nextErrors)
    if (Object.keys(nextErrors).length > 0) {
      return
    }

    setIsSubmitting(true)
    setSubmitError('')

    try {
      const result = await api.login({
        email: form.email.trim(),
        password: form.password,
      })

      if (!result?.success) {
        setSubmitError(result?.message || 'เข้าสู่ระบบไม่สำเร็จ')
        return
      }

      const user = result.user || { role: 'student' }
      setAuthenticatedUser(user)
      onNavigate(result.redirectTo || '/dashboard')
    } catch (error) {
      setSubmitError(error?.message || 'เข้าสู่ระบบไม่สำเร็จ')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (authenticatedUser) {
    return <RoleDashboard user={authenticatedUser} onNavigate={onNavigate} />
  }

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10 text-slate-800">
      <section className="mx-auto w-full max-w-sm rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-teal-700">ระบบอีเว้นต์ดนตรีนักศึกษา</p>
        <h1 className="mt-3 text-2xl font-bold text-slate-800">เข้าสู่ระบบ</h1>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4" noValidate>
          <div>
            <label htmlFor="login-email" className="mb-1 block text-sm font-medium text-slate-700">
              อีเมล <span className="text-red-500">*</span>
            </label>
            <input
              id="login-email"
              type="email"
              autoComplete="email"
              value={form.email}
              onChange={(event) => updateField('email', event.target.value)}
              className={`w-full rounded-xl border px-3 py-2.5 outline-none focus:border-teal-600 ${
                errors.email ? 'border-red-400 bg-red-50' : 'border-slate-300'
              }`}
              placeholder="name@example.com"
            />
            {errors.email && <p className="mt-1 text-xs text-red-600">{errors.email}</p>}
          </div>

          <div>
            <label htmlFor="login-password" className="mb-1 block text-sm font-medium text-slate-700">
              รหัสผ่าน <span className="text-red-500">*</span>
            </label>
            <input
              id="login-password"
              type="password"
              autoComplete="current-password"
              value={form.password}
              onChange={(event) => updateField('password', event.target.value)}
              className={`w-full rounded-xl border px-3 py-2.5 outline-none focus:border-teal-600 ${
                errors.password ? 'border-red-400 bg-red-50' : 'border-slate-300'
              }`}
              placeholder="••••••••"
            />
            {errors.password && <p className="mt-1 text-xs text-red-600">{errors.password}</p>}
          </div>

          {submitError && <p className="text-sm text-red-600">{submitError}</p>}

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-xl bg-teal-700 px-4 py-3 font-semibold text-white transition hover:bg-teal-800 disabled:opacity-70"
          >
            {isSubmitting ? 'กำลังเข้าสู่ระบบ...' : 'เข้าสู่ระบบ'}
          </button>
        </form>
      </section>
    </main>
  )
}
