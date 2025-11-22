/**
 * API utility for making authenticated requests
 * Automatically adds JWT token to request headers
 */

import { useAuthStore } from '@/stores/useAuthStore'

const API_BASE_URL = 'http://localhost:8000/api'

/**
 * Get the current access token from the auth store
 */
const getAccessToken = () => {
  const authStore = useAuthStore()
  return authStore.accessToken
}

/**
 * Fetch wrapper that automatically adds authorization header
 */
export const apiCall = async (endpoint, options = {}) => {
  const token = getAccessToken()

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  }

  // Add authorization header if token exists
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`

  try {
    const response = await fetch(url, {
      ...options,
      headers
    })

    // If token expired (401), try to refresh it
    if (response.status === 401 && token) {
      const authStore = useAuthStore()
      const refreshResult = await authStore.refreshAccessToken()

      if (refreshResult.success) {
        // Retry the original request with new token
        const newToken = authStore.accessToken
        headers.Authorization = `Bearer ${newToken}`

        return fetch(url, {
          ...options,
          headers
        })
      } else {
        // Refresh failed, user needs to login again
        // The logout was already called in refreshAccessToken
        throw new Error('Session expired, please login again')
      }
    }

    return response
  } catch (error) {
    console.error('API call error:', error)
    throw error
  }
}

/**
 * Helper functions for common HTTP methods
 */

export const get = (endpoint, options = {}) => {
  return apiCall(endpoint, { ...options, method: 'GET' })
}

export const post = (endpoint, data, options = {}) => {
  return apiCall(endpoint, {
    ...options,
    method: 'POST',
    body: JSON.stringify(data)
  })
}

export const patch = (endpoint, data, options = {}) => {
  return apiCall(endpoint, {
    ...options,
    method: 'PATCH',
    body: JSON.stringify(data)
  })
}

export const put = (endpoint, data, options = {}) => {
  return apiCall(endpoint, {
    ...options,
    method: 'PUT',
    body: JSON.stringify(data)
  })
}

export const del = (endpoint, options = {}) => {
  return apiCall(endpoint, { ...options, method: 'DELETE' })
}

export default {
  apiCall,
  get,
  post,
  patch,
  put,
  del
}
