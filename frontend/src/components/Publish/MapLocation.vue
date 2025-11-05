<!-- frontend/src/components/Publish/MapLocation.vue -->
<!-- Componente para MOSTRAR ubicación en mapa (solo lectura) -->
<template>
  <div class="map-location">
    <div class="map-header" v-if="!hideHeader">
      <div class="map-title">
        <va-icon name="place" size="1.2rem" />
        <span>{{ title || 'Ubicación' }}</span>
      </div>
      <div class="map-address" v-if="address">
        {{ address }}
      </div>
    </div>

    <div class="map-container" :style="{ height: height }">
      <div id="map" ref="mapContainer" class="leaflet-map"></div>
    </div>

    <div class="map-footer">
      <VaButton
        color="warning"
        @click="openInGoogleMaps"
      >
        <va-icon name="near_me" class="button-icon" />
        Cómo llegar
      </VaButton>
      <p class="footer-hint">Abre en Google Maps para obtener direcciones</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const props = defineProps({
  coordinates: {
    type: Object,
    required: true,
    validator: (val) => val && typeof val.lat === 'number' && typeof val.lng === 'number'
  },
  title: {
    type: String,
    default: ''
  },
  address: {
    type: String,
    default: ''
  },
  zoom: {
    type: Number,
    default: 15
  },
  height: {
    type: String,
    default: '400px'
  },
  hideHeader: {
    type: Boolean,
    default: false
  },
  showDirections: {
    type: Boolean,
    default: true
  },
  readonly: {
    type: Boolean,
    default: true
  }
})

const mapContainer = ref(null)
let map = null
let marker = null

onMounted(() => {
  // Esperar un poco más para que el tab sea visible
  setTimeout(() => {
    initMap()
  }, 300)
})

watch(() => props.coordinates, (newCoords) => {
  if (map && newCoords) {
    updateMarker(newCoords)
  }
}, { deep: true })

// Exponer método para recalcular tamaño (útil cuando está en tabs)
defineExpose({
  refreshMapSize: () => {
    if (map) {
      setTimeout(() => {
        map.invalidateSize()
      }, 100)
    }
  }
})

const initMap = () => {
  if (!mapContainer.value || !props.coordinates) return

  // Inicializar mapa
  map = L.map(mapContainer.value, {
    center: [props.coordinates.lat, props.coordinates.lng],
    zoom: props.zoom,
    scrollWheelZoom: !props.readonly,
    dragging: !props.readonly,
    touchZoom: !props.readonly,
    doubleClickZoom: !props.readonly,
    boxZoom: !props.readonly,
    keyboard: !props.readonly,
    zoomControl: true
  })

  // Agregar capa de tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)

  // Crear icono personalizado
  const customIcon = L.divIcon({
    className: 'custom-marker',
    html: `
      <div class="marker-pin">
        <div class="marker-icon">📍</div>
      </div>
    `,
    iconSize: [40, 40],
    iconAnchor: [20, 40]
  })

  // Agregar marcador
  marker = L.marker([props.coordinates.lat, props.coordinates.lng], {
    icon: customIcon,
    draggable: false
  }).addTo(map)

  // Popup con información
  if (props.title || props.address) {
    const popupContent = `
      <div style="text-align: center; min-width: 150px;">
        ${props.title ? `<strong>${props.title}</strong><br>` : ''}
        ${props.address ? `<span style="font-size: 0.9em;">${props.address}</span>` : ''}
      </div>
    `
    marker.bindPopup(popupContent).openPopup()
  }

  // Ajustar tamaño después de cargar
  setTimeout(() => {
    if (map) map.invalidateSize()
  }, 100)
}

const updateMarker = (newCoords) => {
  if (!map || !marker) return

  marker.setLatLng([newCoords.lat, newCoords.lng])
  map.setView([newCoords.lat, newCoords.lng], props.zoom)
}

const openInGoogleMaps = () => {
  const { lat, lng } = props.coordinates
  window.open(`https://www.google.com/maps/search/?api=1&query=${lat},${lng}`, '_blank')
}
</script>

<style scoped>
.map-location {
  width: 100%;
}

.map-header {
  padding: 1rem;
  background: #F8F4FF;
  border-radius: 12px 12px 0 0;
  border: 2px solid rgba(92, 0, 153, 0.1);
  border-bottom: none;
}

.map-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: #5C0099;
  margin-bottom: 0.5rem;
}

.map-address {
  font-size: 0.95rem;
  color: #666;
  padding-left: 2rem;
}

.map-container {
  width: 100%;
  border-radius: 0;
  overflow: hidden;
  position: relative;
}

.leaflet-map {
  width: 100%;
  height: 100%;
  z-index: 1;
}

.map-footer {
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #5C0099, #8B00CC);
  border-radius: 0 0 16px 16px;
  text-align: center;
  box-shadow: 0 -2px 20px rgba(92, 0, 153, 0.3);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.map-footer .va-button {
  font-weight: 600;
  color: #5C0099 !important;
}

.map-footer .button-icon {
  color: #5C0099 !important;
}

.footer-hint {
  margin: 0.75rem 0 0 0;
  font-size: 0.85rem;
  font-weight: 400;
  color: white;
  letter-spacing: 0.2px;
}

.button-icon {
  margin-right: 0.5rem;
}

.map-footer .va-button {
  font-weight: 600;
  font-size: 1rem;
  padding: 0.875rem 2rem;
  background: linear-gradient(135deg, #FFC107 0%, #FFB300 100%) !important;
  color: white !important;
  border: none;
  box-shadow: 0 4px 14px rgba(255, 193, 7, 0.35);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 10px;
  text-transform: none;
  letter-spacing: 0.5px;
}

.map-footer .va-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 193, 7, 0.45);
  background: linear-gradient(135deg, #FFB300 0%, #FFA000 100%) !important;
}

.map-footer .va-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(255, 193, 7, 0.3);
}

/* Custom marker styles */
:deep(.custom-marker) {
  background: none;
  border: none;
}

:deep(.marker-pin) {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: bounce 1s ease-in-out infinite;
}

:deep(.marker-icon) {
  font-size: 2.5rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* Leaflet popup customization */
:deep(.leaflet-popup-content-wrapper) {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.2);
}

:deep(.leaflet-popup-tip) {
  background: white;
}

/* Disable interactions on readonly */
:deep(.leaflet-container.leaflet-touch-drag) {
  cursor: default !important;
}

/* Responsive */
@media (max-width: 768px) {
  .map-container {
    height: 300px !important;
  }
  
  .map-header {
    padding: 0.75rem;
  }
  
  .map-title {
    font-size: 1rem;
  }
  
  .map-address {
    font-size: 0.85rem;
  }
}
</style>