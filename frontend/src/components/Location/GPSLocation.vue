<!-- frontend/src/components/Location/GPSLocation.vue -->
<template>
  <div class="gps-location">
    
    <div class="location-header">
      <h3 class="location-title">
        <va-icon name="place" color="purple" />
        Ubicación GPS
      </h3>
      <p class="location-subtitle">
        Pega las coordenadas desde Google Maps para mostrar tu ubicación exacta
      </p>
    </div>

    <!-- Instrucciones -->
    <VaCollapse v-model="showInstructions" header="¿Cómo obtener las coordenadas?">
      <div class="instructions">
        <ol>
          <li>Abre <a href="https://maps.google.com" target="_blank">Google Maps</a></li>
          <li>Busca tu negocio o la ubicación exacta</li>
          <li>Haz <strong>click derecho</strong> en el punto del mapa</li>
          <li>Selecciona la primera opción (las coordenadas)</li>
          <li>Las coordenadas se copiarán automáticamente</li>
          <li>Pégalas en el campo de abajo</li>
        </ol>
        <div class="instruction-example">
          <va-icon name="info" />
          <span>Ejemplo de formato: <code>-17.3935, -66.1570</code></span>
        </div>
      </div>
    </VaCollapse>

    <!-- Input de Coordenadas -->
    <div class="coordinates-input">
      <VaTextarea
        v-model="localCoordinates"
        label="Coordenadas GPS *"
        placeholder="-17.3935, -66.1570"
        :min-rows="2"
        :max-rows="3"
        :rules="[
          v => !!v || 'Campo requerido',
          v => validateCoordinates(v) || 'Formato inválido. Usa: latitud, longitud (Ej: -17.3935, -66.1570)'
        ]"
        @update:model-value="handleCoordinatesChange"
      >
        <template #appendInner>
          <VaButton
            preset="plain"
            icon="location_searching"
            size="small"
            @click="detectLocation"
            :loading="detecting"
            title="Detectar mi ubicación actual"
          />
        </template>
      </VaTextarea>

      <div v-if="coordinatesError" class="coordinates-error">
        <va-icon name="error" size="small" />
        <span>{{ coordinatesError }}</span>
      </div>

      <div v-else-if="parsedCoordinates" class="coordinates-success">
        <va-icon name="check_circle" size="small" />
        <span>Coordenadas válidas: {{ parsedCoordinates.lat }}, {{ parsedCoordinates.lng }}</span>
      </div>
    </div>

    <!-- Dirección Adicional -->
    <div class="address-input">
      <VaInput
        v-model="localAddress"
        label="Dirección (Opcional)"
        placeholder="Ej: Av. América #123, Zona Sur"
      >
        <template #appendInner>
          <VaIcon name="home" />
        </template>
      </VaInput>
      <div class="field-hint">
        Agrega una dirección de referencia para ayudar a tus clientes
      </div>
    </div>

    <!-- Vista Previa del Mapa -->
    <transition name="fade">
      <div v-if="parsedCoordinates && !coordinatesError" class="map-preview">
        <div class="map-preview-header">
          <div class="map-label">
            <va-icon name="map" size="small" />
            Vista previa del mapa
          </div>
          <VaButton
            preset="plain"
            size="small"
            icon="open_in_new"
            @click="openInGoogleMaps"
          >
            Ver en Google Maps
          </VaButton>
        </div>

        <div class="map-container">
          <iframe
            v-if="mapUrl"
            :src="mapUrl"
            width="100%"
            height="400"
            style="border:0;"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
          ></iframe>
          
          <div v-else class="map-loading">
            <VaProgressCircle indeterminate />
            <p>Cargando mapa...</p>
          </div>
        </div>

        <div class="map-info">
          <va-icon name="info" size="small" />
          <span>Este mapa se mostrará en tu perfil público</span>
        </div>
      </div>
    </transition>

    <!-- Empty State -->
    <div v-if="!localCoordinates" class="empty-state">
      <va-icon name="map" size="3rem" color="#CCC" />
      <p>Ingresa las coordenadas para ver el mapa</p>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useToast } from 'vuestic-ui'

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
const localCoordinates = ref(props.coordinates)
const localAddress = ref(props.address)
const showInstructions = ref(false)
const detecting = ref(false)
const coordinatesError = ref('')

// ========== COMPUTED ==========
const parsedCoordinates = computed(() => {
  if (!localCoordinates.value) return null
  
  const parsed = parseCoordinates(localCoordinates.value)
  if (parsed) {
    coordinatesError.value = ''
    return parsed
  }
  
  return null
})

const mapUrl = computed(() => {
  if (!parsedCoordinates.value) return null
  
  const { lat, lng } = parsedCoordinates.value
  return `https://maps.google.com/maps?q=${lat},${lng}&hl=es&z=15&output=embed`
})

// ========== WATCH ==========
watch(localCoordinates, (newVal) => {
  emit('update:coordinates', newVal)
})

watch(localAddress, (newVal) => {
  emit('update:address', newVal)
})

// ========== METHODS ==========
const parseCoordinates = (coordStr) => {
  if (!coordStr) return null
  
  // Limpiar espacios extras
  coordStr = coordStr.trim()
  
  // Intentar varios formatos
  const patterns = [
    /^(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)$/, // -17.3935, -66.1570
    /^(-?\d+\.?\d*)\s+(-?\d+\.?\d*)$/, // -17.3935 -66.1570
    /^lat:\s*(-?\d+\.?\d*)\s*,?\s*lng:\s*(-?\d+\.?\d*)$/i, // lat: -17.3935, lng: -66.1570
  ]
  
  for (const pattern of patterns) {
    const match = coordStr.match(pattern)
    if (match) {
      const lat = parseFloat(match[1])
      const lng = parseFloat(match[2])
      
      // Validar rangos
      if (lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) {
        return { lat, lng }
      }
    }
  }
  
  return null
}

const validateCoordinates = (value) => {
  if (!value) return true // Validación de requerido se hace aparte
  return parseCoordinates(value) !== null
}

const handleCoordinatesChange = (value) => {
  const parsed = parseCoordinates(value)
  
  if (!parsed && value) {
    coordinatesError.value = 'Formato inválido. Usa: latitud, longitud'
  } else {
    coordinatesError.value = ''
  }
}

const detectLocation = () => {
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
      const lat = position.coords.latitude.toFixed(6)
      const lng = position.coords.longitude.toFixed(6)
      localCoordinates.value = `${lat}, ${lng}`
      
      notify({
        message: '✅ Ubicación detectada exitosamente',
        color: 'success'
      })
      
      detecting.value = false
    },
    (error) => {
      let message = '❌ No se pudo detectar la ubicación'
      
      if (error.code === error.PERMISSION_DENIED) {
        message = '❌ Permiso de ubicación denegado'
      } else if (error.code === error.POSITION_UNAVAILABLE) {
        message = '❌ Ubicación no disponible'
      } else if (error.code === error.TIMEOUT) {
        message = '❌ Tiempo de espera agotado'
      }
      
      notify({
        message,
        color: 'danger'
      })
      
      detecting.value = false
    }
  )
}

const openInGoogleMaps = () => {
  if (!parsedCoordinates.value) return
  
  const { lat, lng } = parsedCoordinates.value
  const url = `https://www.google.com/maps/search/?api=1&query=${lat},${lng}`
  window.open(url, '_blank')
}
</script>

<style scoped>
/* ========== Container ========== */
.gps-location {
  padding: 2rem;
  background: white;
  border-radius: 16px;
  border: 2px solid rgba(92, 0, 153, 0.1);
}

/* ========== Header ========== */
.location-header {
  margin-bottom: 2rem;
}

.location-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0 0 0.5rem 0;
}

.location-subtitle {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

/* ========== Instructions ========== */
.instructions {
  padding: 1rem;
}

.instructions ol {
  margin: 0 0 1rem 0;
  padding-left: 1.5rem;
}

.instructions li {
  margin-bottom: 0.5rem;
  color: #333;
  line-height: 1.6;
}

.instruction-example {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background: #E3F2FD;
  border-radius: 8px;
  color: #1976D2;
  font-size: 0.9rem;
}

.instruction-example code {
  background: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
}

/* ========== Coordinates Input ========== */
.coordinates-input {
  margin-bottom: 1.5rem;
}

.coordinates-error {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: #FFEBEE;
  border-radius: 8px;
  color: #C62828;
  font-size: 0.85rem;
}

.coordinates-success {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: #E8F5E9;
  border-radius: 8px;
  color: #2E7D32;
  font-size: 0.85rem;
}

/* ========== Address Input ========== */
.address-input {
  margin-bottom: 2rem;
}

.field-hint {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #666;
  font-style: italic;
}

/* ========== Map Preview ========== */
.map-preview {
  margin-top: 2rem;
}

.map-preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.map-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #666;
  font-size: 0.95rem;
}

.map-container {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: #F5F5F5;
}

.map-container iframe {
  display: block;
}

.map-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  gap: 1rem;
}

.map-loading p {
  margin: 0;
  color: #666;
}

.map-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding: 0.75rem;
  background: #F8F4FF;
  border-radius: 8px;
  color: var(--color-purple);
  font-size: 0.85rem;
}

/* ========== Empty State ========== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  text-align: center;
}

.empty-state p {
  margin: 1rem 0 0 0;
  color: #999;
  font-size: 0.95rem;
}

/* ========== Transitions ========== */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .gps-location {
    padding: 1.5rem;
  }

  .map-preview-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .map-container {
    height: 300px;
  }
}
</style>