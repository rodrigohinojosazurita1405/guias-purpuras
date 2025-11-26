<template>
  <div style="padding: 20px; background: #f5f5f5; border-radius: 8px; margin: 20px 0;">
    <h3>Debug Authentication</h3>
    <div style="font-family: monospace; white-space: pre-wrap; background: white; padding: 10px; border-radius: 4px; max-height: 300px; overflow-y: auto;">
{{ debugInfo }}
    </div>
    <button @click="testEndpoint" style="margin-top: 10px; padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer;">
      Test API Endpoint
    </button>
    <div v-if="testResult" style="margin-top: 10px; padding: 10px; background: white; border-radius: 4px; max-height: 300px; overflow-y: auto;">
      <strong>Test Result:</strong>
      <pre>{{ testResult }}</pre>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAuthStore } from '@/stores/useAuthStore'

const authStore = useAuthStore()
const testResult = ref('')

const debugInfo = computed(() => {
  const authUserFromStorage = localStorage.getItem('auth_user')
  const accessTokenFromStorage = localStorage.getItem('access_token')

  return `Auth Store State:
isAuthenticated: ${authStore.isAuthenticated}
user: ${authStore.user ? JSON.stringify(authStore.user) : 'null'}
accessToken: ${authStore.accessToken ? authStore.accessToken.substring(0, 50) + '...' : 'null'}

LocalStorage:
access_token: ${accessTokenFromStorage ? accessTokenFromStorage.substring(0, 50) + '...' : 'null'}
auth_user: ${authUserFromStorage}
`
})

const testEndpoint = async () => {
  try {
    testResult.value = 'Testing...'
    if (!authStore.user) {
      testResult.value = 'Error: No user logged in'
      return
    }

    const response = await fetch(
      `/api/user/published?email=${encodeURIComponent(authStore.user.email)}`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`,
          'Content-Type': 'application/json'
        }
      }
    )

    testResult.value = `Status: ${response.status}\n`
    const text = await response.text()
    testResult.value += `Response:\n${text.substring(0, 500)}`
  } catch (err) {
    testResult.value = `Error: ${err.message}`
  }
}
</script>
