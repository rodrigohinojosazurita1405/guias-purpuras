<!-- frontend/src/components/Location/GPSLocation.vue -->
<template>
  <div class="gps-location">
    
    <!-- Header -->
    <div class="location-header">
      <h3 class="location-title">
        <va-icon name="place" color="#FF6B6B" />
        Ubicación de tu Negocio
      </h3>
      <p class="location-subtitle">
        Haz click en el mapa donde está ubicado tu negocio o busca tu dirección
      </p>
    </div>

    <!-- Checklist de Validación -->
    <div class="location-checklist">
      <div class="checklist-header">
        <va-icon name="checklist" size="small" />
        <span>Estado de Ubicación</span>
      </div>
      <div class="checklist-items">
        <div class="checklist-item" :class="{ completed: hasCoordinates }">
          <va-icon 
            :name="hasCoordinates ? 'check_circle' : 'radio_button_unchecked'" 
            :color="hasCoordinates ? 'success' : 'secondary'"
            size="small"
          />
          <span>Ubicación seleccionada en el mapa</span>
        </div>
        <div class="checklist-item" :class="{ completed: isInBolivia }">
          <va-icon 
            :name="isInBolivia ? 'check_circle' : 'radio_button_unchecked'" 
            :color="isInBolivia ? 'success' : 'secondary'"
            size="small"
          />
          <span>Ubicación dentro de Bolivia</span>
        </div>
        <div class="checklist-item" :class="{ completed: localAddress }">
          <va-icon 
            :name="localAddress ? 'check_circle' : 'radio_button_unchecked'" 
            :color="localAddress ? 'success' : 'secondary'"
            size="small"
          />
          <span>Dirección de referencia agregada</span>
        </div>
      </div>
    </div>

    <!-- Búsqueda Rápida -->
    <div class="search-section">
      <VaInput
        v-model="searchQuery"
        placeholder="Busca tu dirección: Ej. Av. América, La Paz"
        @keyup.enter="searchAddress"
      >
        <template #prepend>
          <va-icon name="search" />
        </template>
        <template #append>
          <VaButton
            preset="plain"
            size="small"
            @click="searchAddress"
            :loading="searching"
          >
             Buscar
          </VaButton>
        </template>
      </VaInput>
      
      <VaButton
        preset="plain"
        size="small"
        icon="my_location"
        @click="detectCurrentLocation"
        :loading="detecting"
      >
        Usar mi ubicación actual
      </VaButton>
    </div>

    <!-- Mapa Interactivo -->
    <div class="map-section">
      <div class="map-instructions">
        <va-icon name="touch_app" size="small" color="warning" />
        <span>Haz click en el mapa o arrastra el marcador rojo a la ubicación exacta de tu negocio</span>
      </div>

      <div class="map-container">
        <div id="map" ref="mapContainer"></div>
        
        <!-- Zoom Controls -->
        <div class="map-controls">
          <VaButton
            preset="plain"
            icon="add"
            size="small"
            @click="zoomIn"
            class="control-btn"
          />
          <VaButton
            preset="plain"
            icon="remove"
            size="small"
            @click="zoomOut"
            class="control-btn"
          />
        </div>
      </div>

      <!-- Coordenadas Actuales -->
      <div v-if="parsedCoordinates" class="coordinates-display">
        <div class="coord-label">
          <va-icon name="gps_fixed" size="small" />
          <span>Coordenadas seleccionadas:</span>
        </div>
        <div class="coord-values">
          <code>{{ parsedCoordinates.lat.toFixed(6) }}, {{ parsedCoordinates.lng.toFixed(6) }}</code>
          <VaButton
            preset="plain"
            size="small"
            icon="content_copy"
            @click="copyCoordinates"
            title="Copiar coordenadas"
          />
        </div>
      </div>

      <!-- Alerta Bolivia -->
      <div v-if="hasCoordinates && !isInBolivia" class="bolivia-alert">
        <va-icon name="warning" size="small" />
        <span>La ubicación seleccionada parece estar fuera de Bolivia. Por favor verifica.</span>
      </div>
    </div>

    <!-- Dirección de Referencia -->
    <div class="address-section">
      <VaInput
        v-model="localAddress"
        label="Dirección de Referencia"
        placeholder="Ej: Av. América #123, entre Calle 1 y 2, Zona Sur"
      >
        <template #prepend>
          <VaIcon name="home" />
        </template>
      </VaInput>
      <div class="field-hint">
        <va-icon name="info" size="small" />
        Esta dirección ayudará a tus clientes a encontrarte más fácilmente
      </div>
    </div>

    <!-- Botón Ver en Google Maps -->
    <div v-if="parsedCoordinates" class="google-maps-link">
      <VaButton
        preset="plain"
        icon="open_in_new"
        @click="openInGoogleMaps"
      >
        Ver en Google Maps
      </VaButton>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { useToast } from 'vuestic-ui'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix para iconos de Leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

// ========== PROPS ==========
const props = defineProps({
  coordinates: {
    type: String,
    default: ''
  },
  address: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:coordinates', 'update:address'])

// ========== COMPOSABLES ==========
const { init: notify } = useToast()

// ========== STATE ==========
const mapContainer = ref(null)
const map = ref(null)
const marker = ref(null)
const localAddress = ref(props.address)
const searchQuery = ref('')
const searching = ref(false)
const detecting = ref(false)

// Bolivia center coordinates (La Paz)
const BOLIVIA_CENTER = { lat: -16.5000, lng: -68.1500 }
const DEFAULT_ZOOM = 13

// Límites aproximados de Bolivia
const BOLIVIA_BOUNDS = {
  north: -9.5,
  south: -23.0,
  west: -69.5,
  east: -57.5
}

// ========== COMPUTED ==========
const parsedCoordinates = computed(() => {
  if (!marker.value) return null
  
  const latlng = marker.value.getLatLng()
  return {
    lat: latlng.lat,
    lng: latlng.lng
  }
})

const hasCoordinates = computed(() => {
  return parsedCoordinates.value !== null
})

const isInBolivia = computed(() => {
  if (!parsedCoordinates.value) return false
  
  const { lat, lng } = parsedCoordinates.value
  return (
    lat <= BOLIVIA_BOUNDS.north &&
    lat >= BOLIVIA_BOUNDS.south &&
    lng >= BOLIVIA_BOUNDS.west &&
    lng <= BOLIVIA_BOUNDS.east
  )
})

// ========== LIFECYCLE ==========
onMounted(() => {
  initMap()
  
  // Si hay coordenadas previas, cargarlas
  if (props.coordinates) {
    const coords = parseCoordinatesString(props.coordinates)
    if (coords) {
      addMarker(coords.lat, coords.lng)
      map.value.setView([coords.lat, coords.lng], 15)
    }
  }
})

onBeforeUnmount(() => {
  if (map.value) {
    map.value.remove()
  }
})

// ========== WATCH ==========
watch(parsedCoordinates, (newVal) => {
  if (newVal) {
    const coordString = `${newVal.lat.toFixed(6)}, ${newVal.lng.toFixed(6)}`
    emit('update:coordinates', coordString)
  }
}, { deep: true })

watch(localAddress, (newVal) => {
  emit('update:address', newVal)
})

// ========== METHODS ==========
const initMap = () => {
  // Crear mapa
  map.value = L.map(mapContainer.value, {
    center: [BOLIVIA_CENTER.lat, BOLIVIA_CENTER.lng],
    zoom: 6,
    zoomControl: false
  })

  // Agregar tiles de OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map.value)

  // Click en el mapa
  map.value.on('click', (e) => {
    addMarker(e.latlng.lat, e.latlng.lng)
  })
}

const addMarker = (lat, lng) => {
  // Remover marcador anterior si existe
  if (marker.value) {
    map.value.removeLayer(marker.value)
  }

  // Crear nuevo marcador
  const redIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  })

  marker.value = L.marker([lat, lng], {
    icon: redIcon,
    draggable: true
  }).addTo(map.value)

  // Popup
  marker.value.bindPopup(`
    <div style="text-align: center;">
      <strong>Tu negocio</strong><br/>
      <small>${lat.toFixed(6)}, ${lng.toFixed(6)}</small>
    </div>
  `).openPopup()

  // Evento drag
  marker.value.on('dragend', (e) => {
    const position = e.target.getLatLng()
    marker.value.setLatLng(position)
    
    notify({
      message: '📍 Ubicación actualizada',
      color: 'info',
      duration: 2000
    })
  })

  // Validar Bolivia
  if (!isInBolivia.value) {
    notify({
      message: '⚠️ La ubicación parece estar fuera de Bolivia',
      color: 'warning',
      duration: 4000
    })
  } else {
    notify({
      message: '✅ Ubicación seleccionada',
      color: 'success',
      duration: 2000
    })
  }
}

const searchAddress = async () => {
  if (!searchQuery.value.trim()) {
    notify({
      message: 'Escribe una dirección para buscar',
      color: 'warning'
    })
    return
  }

  searching.value = true

  try {
    // Usar Nominatim API de OpenStreetMap
    const query = `${searchQuery.value}, Bolivia`
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`
    )
    
    const data = await response.json()

    if (data && data.length > 0) {
      const result = data[0]
      const lat = parseFloat(result.lat)
      const lng = parseFloat(result.lon)

      // Centrar mapa y agregar marcador
      map.value.setView([lat, lng], 16)
      addMarker(lat, lng)

      // Sugerir dirección
      if (result.display_name) {
        localAddress.value = result.display_name
      }

      notify({
        message: '✅ Dirección encontrada',
        color: 'success'
      })
    } else {
      notify({
        message: '❌ No se encontró la dirección. Intenta con otra búsqueda.',
        color: 'danger'
      })
    }
  } catch (error) {
    console.error('Error buscando dirección:', error)
    notify({
      message: '❌ Error al buscar dirección',
      color: 'danger'
    })
  } finally {
    searching.value = false
  }
}

const detectCurrentLocation = () => {
  if (!navigator.geolocation) {
    notify({
      message: '❌ Tu navegador no soporta geolocalización',
      color: 'danger'
    })
    return
  }

  detecting.value = true

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude
      const lng = position.coords.longitude

      // Centrar mapa y agregar marcador
      map.value.setView([lat, lng], 16)
      addMarker(lat, lng)

      notify({
        message: '✅ Ubicación detectada exitosamente',
        color: 'success'
      })

      detecting.value = false
    },
    (error) => {
      let message = '❌ No se pudo detectar la ubicación'

      if (error.code === error.PERMISSION_DENIED) {
        message = '❌ Permiso de ubicación denegado. Actívalo en tu navegador.'
      } else if (error.code === error.POSITION_UNAVAILABLE) {
        message = '❌ Ubicación no disponible'
      } else if (error.code === error.TIMEOUT) {
        message = '❌ Tiempo de espera agotado'
      }

      notify({
        message,
        color: 'danger',
        duration: 4000
      })

      detecting.value = false
    }
  )
}

const zoomIn = () => {
  map.value.zoomIn()
}

const zoomOut = () => {
  map.value.zoomOut()
}

const copyCoordinates = () => {
  if (!parsedCoordinates.value) return

  const coordString = `${parsedCoordinates.value.lat.toFixed(6)}, ${parsedCoordinates.value.lng.toFixed(6)}`
  
  navigator.clipboard.writeText(coordString).then(() => {
    notify({
      message: '📋 Coordenadas copiadas al portapapeles',
      color: 'success',
      duration: 2000
    })
  })
}

const openInGoogleMaps = () => {
  if (!parsedCoordinates.value) return

  const { lat, lng } = parsedCoordinates.value
  const url = `https://www.google.com/maps/search/?api=1&query=${lat},${lng}`
  window.open(url, '_blank')
}

const parseCoordinatesString = (coordStr) => {
  if (!coordStr) return null

  const parts = coordStr.split(',').map(s => s.trim())
  if (parts.length !== 2) return null

  const lat = parseFloat(parts[0])
  const lng = parseFloat(parts[1])

  if (isNaN(lat) || isNaN(lng)) return null
  if (lat < -90 || lat > 90 || lng < -180 || lng > 180) return null

  return { lat, lng }
}

// ========== EXPOSE ==========
defineExpose({
  getLocationData: () => ({
    latitude: parsedCoordinates.value?.lat || null,
    longitude: parsedCoordinates.value?.lng || null,
    address: localAddress.value || '',
    country: 'Bolivia',
    isValid: hasCoordinates.value && isInBolivia.value
  })
})
</script>

<style scoped>
/* ========== Container ========== */
.gps-location {
  background: white;
  border-radius: 16px;
}

/* ========== Header ========== */
.location-header {
  margin-bottom: 2rem;
}

.location-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.5rem 0;
}

.location-subtitle {
  margin: 0;
  color: #6B7280;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* ========== Checklist ========== */
.location-checklist {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #FAFAFA 0%, #FFFFFF 100%);
  border-radius: 12px;
  border: 2px solid #E5E7EB;
}

.checklist-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #374151;
  font-size: 0.95rem;
}

.checklist-items {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.checklist-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: white;
  border-radius: 8px;
  font-size: 0.9rem;
  color: #6B7280;
  transition: all 0.2s;
  border: 1px solid #F3F4F6;
}

.checklist-item.completed {
  color: #059669;
  font-weight: 500;
  background: #F0FDF4;
  border-color: #BBF7D0;
}

/* ========== Search Section ========== */
.search-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 2px solid #E5E7EB;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.search-section > :first-child {
  flex: 1;
}

/* ========== Map Section ========== */
.map-section {
  margin-bottom: 2rem;
}

.map-instructions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: #FFF9E6;
  border: 2px solid #FFC107;
  border-radius: 12px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #D97706;
  font-weight: 500;
}

.map-container {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #E5E7EB;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

#map {
  height: 500px;
  width: 100%;
  z-index: 1;
}

.map-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 1000;
}

.control-btn {
  background: white !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

/* ========== Coordinates Display ========== */
.coordinates-display {
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #F0FDF4 0%, #FFFFFF 100%);
  border: 2px solid #BBF7D0;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.coord-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #059669;
  font-size: 0.9rem;
}

.coord-values {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.coord-values code {
  background: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  color: #059669;
  border: 1px solid #BBF7D0;
}

/* ========== Bolivia Alert ========== */
.bolivia-alert {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: #FEF3C7;
  border: 2px solid #FCD34D;
  border-radius: 12px;
  color: #B45309;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

/* ========== Address Section ========== */
.address-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 2px solid #E5E7EB;
}

.field-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
  font-size: 0.85rem;
  color: #6B7280;
  line-height: 1.4;
}

/* ========== Google Maps Link ========== */
.google-maps-link {
  text-align: center;
  padding: 1rem;
  background: #F3F4F6;
  border-radius: 12px;
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .search-section {
    flex-direction: column;
  }

  #map {
    height: 400px;
  }

  .coordinates-display {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .coord-values {
    flex-direction: column;
  }
}

/* ========== Leaflet Overrides ========== */
:deep(.leaflet-popup-content-wrapper) {
  border-radius: 8px;
}

:deep(.leaflet-popup-content) {
  margin: 10px;
}
</style>