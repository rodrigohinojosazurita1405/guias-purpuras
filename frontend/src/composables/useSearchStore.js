// frontend/src/stores/useSearchStore.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useSearchStore = defineStore('search', () => {
  // ========== STATE ==========
  const searchQuery = ref('')
  const selectedCity = ref('')
  const selectedCategory = ref('profesionales')
  const userDetectedCity = ref('')
  const isLoadingLocation = ref(false)

  // ========== GETTERS ==========
  const hasActiveFilters = computed(() => {
    return searchQuery.value || selectedCity.value
  })

  const searchParams = computed(() => {
    const params = {}
    if (searchQuery.value) params.q = searchQuery.value
    if (selectedCity.value) params.ciudad = selectedCity.value
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

  // ========== ACTIONS ==========
  
  /**
   * Inicializar desde localStorage
   */
  const initFromStorage = () => {
    const savedCity = localStorage.getItem('selectedCity')
    const savedCategory = localStorage.getItem('selectedCategory')
    
    if (savedCity) selectedCity.value = savedCity
    if (savedCategory) selectedCategory.value = savedCategory
  }

  /**
   * Detectar ubicación del usuario
   */
  const detectUserLocation = () => {
    isLoadingLocation.value = true
    
    return new Promise((resolve) => {
      if (!navigator.geolocation) {
        console.log('Geolocalización no soportada')
        isLoadingLocation.value = false
        resolve(null)
        return
      }

      navigator.geolocation.getCurrentPosition(
        async (position) => {
          try {
            // Usamos una API de geocoding gratuita
            const response = await fetch(
              `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${position.coords.latitude}&longitude=${position.coords.longitude}&localityLanguage=es`
            )
            const data = await response.json()
            
            const detectedCity = mapCityNameToSlug(data.city)
            userDetectedCity.value = detectedCity
            
            // Si no hay ciudad seleccionada, usar la detectada
            if (!selectedCity.value && detectedCity) {
              selectedCity.value = detectedCity
              localStorage.setItem('selectedCity', detectedCity)
            }
            
            resolve(detectedCity)
          } catch (error) {
            console.log('Error obteniendo ciudad:', error)
            resolve(null)
          } finally {
            isLoadingLocation.value = false
          }
        },
        (error) => {
          console.log('Error geolocalización:', error)
          isLoadingLocation.value = false
          resolve(null)
        },
        {
          timeout: 10000,
          enableHighAccuracy: false
        }
      )
    })
  }

  /**
   * Mapear nombre de ciudad a slug
   */
  const mapCityNameToSlug = (cityName) => {
    if (!cityName) return ''
    
    const cityMap = {
      'la paz': 'la-paz',
      'lapaz': 'la-paz',
      'cochabamba': 'cochabamba',
      'santa cruz': 'santa-cruz',
      'santacruz': 'santa-cruz',
      'oruro': 'oruro',
      'potosi': 'potosi',
      'potosí': 'potosi',
      'tarija': 'tarija',
      'sucre': 'chuquisaca',
      'chuquisaca': 'chuquisaca',
      'beni': 'beni',
      'pando': 'pando'
    }
    
    return cityMap[cityName.toLowerCase()] || ''
  }

  /**
   * Establecer ciudad seleccionada
   */
  const setSelectedCity = (city) => {
    selectedCity.value = city
    if (city) {
      localStorage.setItem('selectedCity', city)
    } else {
      localStorage.removeItem('selectedCity')
    }
  }

  /**
   * Establecer categoría seleccionada
   */
  const setSelectedCategory = (category) => {
    selectedCategory.value = category
    localStorage.setItem('selectedCategory', category)
  }

  /**
   * Establecer query de búsqueda
   */
  const setSearchQuery = (query) => {
    searchQuery.value = query
  }

  /**
   * Limpiar todos los filtros
   */
  const clearAllFilters = () => {
    searchQuery.value = ''
    selectedCity.value = ''
    selectedCategory.value = 'profesionales'
    localStorage.removeItem('selectedCity')
    localStorage.removeItem('selectedCategory')
  }

  // Inicializar al cargar
  initFromStorage()

  return {
    // State
    searchQuery,
    selectedCity,
    selectedCategory,
    userDetectedCity,
    isLoadingLocation,
    
    // Getters
    hasActiveFilters,
    searchParams,
    displayCity,
    
    // Actions
    detectUserLocation,
    setSelectedCity,
    setSelectedCategory,
    setSearchQuery,
    clearAllFilters
  }
})