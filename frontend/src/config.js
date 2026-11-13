// API paths follow the Auth API contract in plan.md and support FR-AUTH-02, FR-AUTH-03, and FR-AUTH-05.
export const authApiPaths = {
  register: '/auth/register',
  login: '/auth/login',
  logout: '/auth/logout',
  me: '/auth/me',
  lockoutCheck: '/auth/lockout-check',
}
