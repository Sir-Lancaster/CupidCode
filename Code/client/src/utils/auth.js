// Authentication utility functions

export function setUserSession(userId, userType) {
  localStorage.setItem('user_id', userId)
  localStorage.setItem('user_type', userType)
}

export function clearUserSession() {
  localStorage.removeItem('user_id')
  localStorage.removeItem('user_type')
}

export function getCurrentUser() {
  return {
    id: localStorage.getItem('user_id'),
    type: localStorage.getItem('user_type')
  }
}

export function isAuthenticated() {
  const user = getCurrentUser()
  return user.id && user.type
}

export function hasRole(requiredRole) {
  const user = getCurrentUser()
  return user.type === requiredRole
}