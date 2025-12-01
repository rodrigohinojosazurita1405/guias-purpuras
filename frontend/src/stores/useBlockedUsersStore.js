import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useBlockedUsersStore = defineStore('blockedUsers', () => {
  // State
  const blockedUsers = ref([])
  const loading = ref(false)
  const error = ref(null)
  const apiUrl = 'http://localhost:8000/api'

  // Getters
  const blockedUserCount = computed(() => blockedUsers.value.length)

  const blockedUsersByReason = computed(() => {
    const grouped = {
      SPAM: [],
      UNQUALIFIED: [],
      OTHER: []
    }
    blockedUsers.value.forEach(block => {
      if (grouped[block.reason]) {
        grouped[block.reason].push(block)
      }
    })
    return grouped
  })

  const permanentBlocks = computed(() => {
    return blockedUsers.value.filter(b => b.isPermanent)
  })

  const temporaryBlocks = computed(() => {
    return blockedUsers.value.filter(b => !b.isPermanent)
  })

  // Actions
  const loadBlockedUsers = async (accessToken) => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${apiUrl}/blocked-users/me`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          blockedUsers.value = data.blockedUsers || []
          console.log('✅ Usuarios bloqueados cargados:', blockedUsers.value.length)
        } else {
          error.value = data.message || 'Error al cargar usuarios bloqueados'
        }
      } else {
        const errorData = await response.json()
        error.value = errorData.message || `Error ${response.status}`
        console.error('❌ Error al cargar usuarios bloqueados:', response.status, errorData)
      }
    } catch (err) {
      error.value = err.message
      console.error('❌ Error en loadBlockedUsers:', err)
    } finally {
      loading.value = false
    }
  }

  const blockUser = async (blockedUserId, reason = 'OTHER', reasonNotes = '', isPermanent = true, accessToken) => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${apiUrl}/blocked-users/block`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
          blockedUserId,
          reason,
          reasonNotes,
          isPermanent
        })
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          // Agregar el nuevo bloqueo a la lista
          if (data.blockedUser) {
            blockedUsers.value.push(data.blockedUser)
          }
          console.log('✅ Usuario bloqueado:', data.message)
          return true
        } else {
          error.value = data.message || 'Error al bloquear usuario'
        }
      } else {
        const errorData = await response.json()
        error.value = errorData.message || `Error ${response.status}`
        console.error('❌ Error al bloquear:', response.status, errorData)
      }
    } catch (err) {
      error.value = err.message
      console.error('❌ Error en blockUser:', err)
    } finally {
      loading.value = false
    }

    return false
  }

  const unblockUser = async (blockId, accessToken) => {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${apiUrl}/blocked-users/${blockId}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          // Remover del estado local
          blockedUsers.value = blockedUsers.value.filter(b => b.id !== blockId)
          console.log('✅ Usuario desbloqueado:', data.message)
          return true
        } else {
          error.value = data.message || 'Error al desbloquear usuario'
        }
      } else {
        const errorData = await response.json()
        error.value = errorData.message || `Error ${response.status}`
        console.error('❌ Error al desbloquear:', response.status, errorData)
      }
    } catch (err) {
      error.value = err.message
      console.error('❌ Error en unblockUser:', err)
    } finally {
      loading.value = false
    }

    return false
  }

  const checkIfBlocked = async (userId, companyId = null, accessToken = null) => {
    try {
      let url = `${apiUrl}/blocked-users/check/${userId}/`
      if (companyId) {
        url += `?company_id=${companyId}`
      }

      const headers = {
        'Content-Type': 'application/json'
      }

      if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`
      }

      const response = await fetch(url, {
        method: 'GET',
        headers
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success) {
          console.log(`✅ Estado de bloqueo verificado para usuario ${userId}:`, data.isBlocked)
          return data
        } else {
          console.error('❌ Error:', data.message)
          return { success: false, isBlocked: false }
        }
      } else {
        const errorData = await response.json()
        console.error('❌ Error al verificar bloqueo:', response.status, errorData)
        return { success: false, isBlocked: false }
      }
    } catch (err) {
      console.error('❌ Error en checkIfBlocked:', err)
      return { success: false, isBlocked: false }
    }
  }

  const getBlockedUserById = (blockId) => {
    return blockedUsers.value.find(b => b.id === blockId)
  }

  const isUserBlocked = (blockedUserId) => {
    return blockedUsers.value.some(b => b.blockedUserId === blockedUserId)
  }

  const clearBlockedUsers = () => {
    blockedUsers.value = []
    error.value = null
  }

  return {
    // State
    blockedUsers,
    loading,
    error,

    // Getters
    blockedUserCount,
    blockedUsersByReason,
    permanentBlocks,
    temporaryBlocks,

    // Actions
    loadBlockedUsers,
    blockUser,
    unblockUser,
    checkIfBlocked,
    getBlockedUserById,
    isUserBlocked,
    clearBlockedUsers
  }
})
