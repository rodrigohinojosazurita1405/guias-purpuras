// frontend/src/stores/useSearchStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useSearchStore = defineStore('search', () => {
  // ========== STATE ==========
  const searchQuery = ref('')
  const selectedCity = ref('')
  const selectedContractType = ref('') // Tipo de contrato seleccionado
  const userDetectedCity = ref('')
  const isLoadingLocation = ref(false)
  const locationMethod = ref('') // 'gps', 'ip', 'manual'

  // ========== GETTERS ==========
  const hasActiveFilters = computed(() => {
    return searchQuery.value || selectedCity.value
  })

  const searchParams = computed(() => {
    const params = {}
    if (searchQuery.value) params.q = searchQuery.value
    if (selectedCity.value) params.ciudad = selectedCity.value
    if (selectedContractType.value) params.contractType = selectedContractType.value
    return params
  })

  const displayCity = computed(() => {
    if (selectedCity.value) {
      const cityNames = {
        'oruro': 'Oruro',
        'la-paz': 'La Paz', 
        'cochabamba': 'Cochabamba',
        'santa-cruz': 'Santa Cruz',
        'potosi': 'Potosí',
        'tarija': 'Tarija',
        'chuquisaca': 'Chuquisaca',
        'beni': 'Beni',
        'pando': 'Pando'
      }
      return cityNames[selectedCity.value] || selectedCity.value
    }
    return 'Toda Bolivia'
  })

  // ========== ACCIONES ==========
  
  /**
   * Inicializar desde localStorage
   */
  const initFromStorage = () => {
    const savedCity = localStorage.getItem('selectedCity')
    const savedContractType = localStorage.getItem('selectedContractType')
    const savedMethod = localStorage.getItem('locationMethod')

    if (savedCity) selectedCity.value = savedCity
    if (savedContractType) selectedContractType.value = savedContractType
    if (savedMethod) locationMethod.value = savedMethod
  }

  /**
   * Detectar ubicación automáticamente (GPS primero, luego IP)
   */
  const detectUserLocation = async () => {
    // Si ya hay una ciudad guardada, no re-detectar
    const savedCity = localStorage.getItem('selectedCity')
    if (savedCity && locationMethod.value) {
      console.log('📍 Ciudad ya detectada:', savedCity)
      return savedCity
    }

    isLoadingLocation.value = true
    
    try {
      // 🎯 INTENTO 1: Geolocalización GPS (más precisa)
      const gpsCity = await tryGPSLocation()
      if (gpsCity) {
        console.log('✅ Ciudad detectada por GPS:', gpsCity)
        return gpsCity
      }

      // 🎯 INTENTO 2: IP Geolocation (fallback)
      const ipCity = await tryIPLocation()
      if (ipCity) {
        console.log('✅ Ciudad detectada por IP:', ipCity)
        return ipCity
      }

      console.log('⚠️ No se pudo detectar ubicación')
      return null
      
    } catch (error) {
      console.error('❌ Error detectando ubicación:', error)
      return null
    } finally {
      isLoadingLocation.value = false
    }
  }

  /**
   * MÉTODO 1: Intentar geolocalización GPS del navegador
   */
  const tryGPSLocation = () => {
    return new Promise((resolve) => {
      if (!navigator.geolocation) {
        console.log('⚠️ Geolocalización no soportada')
        resolve(null)
        return
      }

      navigator.geolocation.getCurrentPosition(
        async (position) => {
          try {
            // API gratuita de reverse geocoding
            const response = await fetch(
              `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${position.coords.latitude}&longitude=${position.coords.longitude}&localityLanguage=es`,
              { timeout: 5000 }
            )
            
            if (!response.ok) throw new Error('API error')
            
            const data = await response.json()
            const detectedCity = mapCityNameToSlug(data.city || data.locality)
            
            if (detectedCity) {
              userDetectedCity.value = detectedCity
              selectedCity.value = detectedCity
              locationMethod.value = 'gps'
              
              localStorage.setItem('selectedCity', detectedCity)
              localStorage.setItem('locationMethod', 'gps')
              
              resolve(detectedCity)
            } else {
              resolve(null)
            }
          } catch (error) {
            console.log('❌ Error en geocoding GPS:', error)
            resolve(null)
          }
        },
        (error) => {
          console.log('⚠️ Usuario negó permisos GPS o timeout:', error.message)
          resolve(null)
        },
        {
          timeout: 8000,
          enableHighAccuracy: false,
          maximumAge: 300000 // Cache 5 minutos
        }
      )
    })
  }

  /**
   * MÉTODO 2: Fallback con IP Geolocation (silencioso, no requiere permisos)
   */
  const tryIPLocation = async () => {
    try {
      // API gratuita de IP geolocation (sin API key, 1000 req/día)
      const response = await fetch('https://ipapi.co/json/', {
        timeout: 5000
      })
      
      if (!response.ok) throw new Error('IP API error')
      
      const data = await response.json()
      
      // Verificar que sea Bolivia
      if (data.country_code !== 'BO') {
        console.log('⚠️ Usuario fuera de Bolivia:', data.country)
        return null
      }
      
      const detectedCity = mapCityNameToSlug(data.city)
      
      if (detectedCity) {
        userDetectedCity.value = detectedCity
        selectedCity.value = detectedCity
        locationMethod.value = 'ip'
        
        localStorage.setItem('selectedCity', detectedCity)
        localStorage.setItem('locationMethod', 'ip')
        
        return detectedCity
      }
      
      return null
      
    } catch (error) {
      console.log('❌ Error en IP geolocation:', error)
      return null
    }
  }

  /**
   * Mapear nombre de ciudad a slug (normalización)
   */
  const mapCityNameToSlug = (cityName) => {
    if (!cityName) return ''
    
    const normalized = cityName
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '') // Quitar acentos
      .trim()
    
    const cityMap = {
      'la paz': 'la-paz',
      'lapaz': 'la-paz',
      'cochabamba': 'cochabamba',
      'santa cruz': 'santa-cruz',
      'santa cruz de la sierra': 'santa-cruz',
      'santacruz': 'santa-cruz',
      'oruro': 'oruro',
      'potosi': 'potosi',
      'tarija': 'tarija',
      'sucre': 'chuquisaca',
      'chuquisaca': 'chuquisaca',
      'beni': 'beni',
      'trinidad': 'beni',
      'pando': 'pando',
      'cobija': 'pando'
    }
    
    return cityMap[normalized] || ''
  }

  /**
   * Establecer ciudad manualmente (usuario selecciona en dropdown)
   */
  const setSelectedCity = (city) => {
    selectedCity.value = city
    locationMethod.value = 'manual'
    
    if (city) {
      localStorage.setItem('selectedCity', city)
      localStorage.setItem('locationMethod', 'manual')
    } else {
      localStorage.removeItem('selectedCity')
      localStorage.removeItem('locationMethod')
    }
  }

  /**
   * Establecer tipo de contrato seleccionado
   */
  const setSelectedContractType = (contractType) => {
    selectedContractType.value = contractType
    if (contractType) {
      localStorage.setItem('selectedContractType', contractType)
    } else {
      localStorage.removeItem('selectedContractType')
    }
  }

  /**
   * Establecer query de búsqueda
   */
  const setSearchQuery = (query) => {
    searchQuery.value = query
  }

  /**
   * Limpiar ciudad y forzar re-detección
   */
  const resetLocation = async () => {
    selectedCity.value = ''
    userDetectedCity.value = ''
    locationMethod.value = ''
    localStorage.removeItem('selectedCity')
    localStorage.removeItem('locationMethod')
    
    // Re-detectar
    return await detectUserLocation()
  }

  /**
   * Limpiar todos los filtros
   */
  const clearAllFilters = () => {
    searchQuery.value = ''
    selectedCity.value = ''
    selectedContractType.value = ''
    localStorage.removeItem('selectedCity')
    localStorage.removeItem('selectedContractType')
  }

  // Inicializar al cargar
  initFromStorage()

  // Detectar ubicación automáticamente si no hay ciudad guardada
  if (!selectedCity.value) {
    detectUserLocation()
  }

  return {
    // State
    searchQuery,
    selectedCity,
    selectedContractType,
    userDetectedCity,
    isLoadingLocation,
    locationMethod,

    // Getters
    hasActiveFilters,
    searchParams,
    displayCity,

    // Actions
    detectUserLocation,
    tryGPSLocation,
    tryIPLocation,
    setSelectedCity,
    setSelectedContractType,
    setSearchQuery,
    resetLocation,
    clearAllFilters
  }
})