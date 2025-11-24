<!-- frontend/src/components/Layout/TopBar.vue -->
<template>
  <div class="top-bar">
    <div class="top-bar-content">
      <!-- Ubicación detectada -->
      <div class="top-left">
        <div class="location-display">
          <p>Mostrando anuncios para:</p>
          <va-icon 
            :name="searchStore.isLoadingLocation ? 'refresh' : 'location_on'" 
            :class="['location-icon', { spinning: searchStore.isLoadingLocation }]"
            size="small" 
          />
          <span class="location-text">{{ searchStore.displayCity }}</span>
          <button 
            v-if="!searchStore.isLoadingLocation"
            @click="changeLocation" 
            class="change-btn"
            title="Cambiar ubicación"
          >
            cambiar
          </button>
        </div>
      </div>

      <!-- Enlaces de contacto y ayuda -->
      <div class="top-right">
        <a href="/" class="top-link top-link-home" title="Ir a inicio">
          <va-icon name="home" size="small" />
          <span class="link-text">Inicio</span>
        </a>
        <a href="tel:+59165324767" class="top-link">
          <va-icon name="phone" size="small" />
          <span class="link-text">+591 65324767</span>
        </a>
        <a href="mailto:info@guiaspurpuras.com.bo" class="top-link">
          <va-icon name="email" size="small" />
          <span class="link-text">info@guiaspurpuras.com.bo</span>
        </a>
        <a href="#" class="top-link" @click.prevent="showHelp">
          <va-icon name="help_outline" size="small" />
          <span class="link-text">Ayuda</span>
        </a>
        <div class="language-selector">
          <va-icon name="language" size="small" />
          <span>ES</span>
        </div>
      </div>
    </div>

    <!-- Modal para cambiar ubicación -->
    <va-modal
      v-model="showLocationModal"
      title="Cambiar ubicación"
      size="small"
      :hide-default-actions="true"
      class="location-modal"
    >
      <div class="location-modal-content">
        <p class="modal-description">
          Selecciona tu ciudad para ver anuncios relevantes cerca de ti
        </p>
        
        <va-select
          v-model="selectedCity"
          :options="cities"
          label="Ciudad"
          placeholder="Selecciona una ciudad"
          class="city-select"
        >
          <template #prepend>
            <va-icon name="location_city" />
          </template>
        </va-select>

        <div class="modal-actions">
          <va-button
            @click="detectLocation"
            preset="secondary"
            :loading="searchStore.isLoadingLocation"
          >
            <va-icon name="my_location" />
            Detectar automáticamente
          </va-button>
          
          <va-button
            @click="saveLocation"
            color="primary"
            :disabled="!selectedCity"
          >
            Guardar
          </va-button>
        </div>
      </div>
    </va-modal>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useSearchStore } from '@/stores/useSearchStore'
import { useToast } from 'vuestic-ui'

const searchStore = useSearchStore()
const { init: notify } = useToast()

// State
const showLocationModal = ref(false)
const selectedCity = ref(null)

// Ciudades disponibles
const cities = [
  { value: '', text: 'Toda Bolivia' },
  { value: 'la-paz', text: 'La Paz' },
  { value: 'cochabamba', text: 'Cochabamba' },
  { value: 'santa-cruz', text: 'Santa Cruz' },
  { value: 'oruro', text: 'Oruro' },
  { value: 'potosi', text: 'Potosí' },
  { value: 'tarija', text: 'Tarija' },
  { value: 'chuquisaca', text: 'Chuquisaca' },
  { value: 'beni', text: 'Beni' },
  { value: 'pando', text: 'Pando' }
]

// Methods
const changeLocation = () => {
  // Encontrar el objeto completo que coincida con el valor del store
  const cityValue = searchStore.selectedCity
  selectedCity.value = cities.find(c => c.value === cityValue) || cities[0]
  showLocationModal.value = true
}

const detectLocation = async () => {
  const detected = await searchStore.resetLocation()
  if (detected) {
    // Actualizar el select con el nuevo valor
    const cityValue = searchStore.selectedCity
    selectedCity.value = cities.find(c => c.value === cityValue) || cities[0]
    
    notify({
      message: `📍 Ubicación detectada: ${searchStore.displayCity}`,
      color: 'success'
    })
    showLocationModal.value = false
  } else {
    notify({
      message: 'No se pudo detectar tu ubicación. Por favor selecciona manualmente.',
      color: 'warning'
    })
  }
}

const saveLocation = () => {
  // Extraer el value del objeto seleccionado
  const cityValue = selectedCity.value?.value || ''
  searchStore.setSelectedCity(cityValue)
  
  notify({
    message: cityValue 
      ? `✅ Ubicación cambiada a ${searchStore.displayCity}`
      : '✅ Mostrando resultados de toda Bolivia',
    color: 'success'
  })
  showLocationModal.value = false
}

const showHelp = () => {
  notify({
    message: '📚 Sección de ayuda próximamente',
    color: 'info'
  })
}
</script>

<style scoped>
/* ========== TOP BAR ========== */
.top-bar {
  background: var(--color-purple-dark);
  color: #ffffff;
  padding: 0.5rem 0;
  font-size: 0.85rem;
  width: 100%;
  border: none;
}

.top-bar-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* ========== UBICACIÓN ========== */
.top-left {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.location-display {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  transition: all 0.3s ease;
}

.location-display:hover {
  background: rgba(255, 255, 255, 0.15);
}

.location-icon {
  color: var(--color-yellow-primary);
  transition: transform 0.3s ease;
}

.location-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.location-text {
  font-weight: 600;
  color: white;
}

.change-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.8rem;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
  transition: color 0.3s ease;
}

.change-btn:hover {
  color: var(--color-yellow-primary);
}

/* ========== LINKS ========== */
.top-right {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.top-link {
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.3s ease;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.top-link:hover {
  color: var(--color-yellow-primary);
  background: rgba(255, 255, 255, 0.05);
}

/* ========== HOME BUTTON ========== */
.top-link-home {
  color: white;
  background: rgba(255, 255, 255, 0.15);
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-weight: 500;
}

.top-link-home:hover {
  background: rgba(255, 255, 255, 0.25);
  color: var(--color-yellow-primary);
}

.language-selector {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
  padding: 0.25rem 0.75rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.language-selector:hover {
  background: rgba(255, 255, 255, 0.15);
  color: var(--color-yellow-primary);
}

/* ========== MODAL ========== */
.location-modal-content {
  padding: 1rem 0;
}

.modal-description {
  color: #666;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.city-select {
  margin-bottom: 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

/* ========== FIX Z-INDEX MODAL ========== */
:deep(.va-modal) {
  z-index: 99999 !important;
}

:deep(.va-modal__overlay) {
  z-index: 99998 !important;
  position: fixed !important;
}

:deep(.va-modal__container) {
  z-index: 99999 !important;
  position: fixed !important;
}

:deep(.va-modal__dialog) {
  z-index: 99999 !important;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1024px) {
  .top-bar-content {
    padding: 0 2rem;
  }

  .top-right {
    gap: 1rem;
  }

  .link-text {
    display: none;
  }

  .top-link {
    padding: 0.25rem;
  }
}

@media (max-width: 768px) {
  .top-bar-content {
    padding: 0 1rem;
    gap: 1rem;
  }

  .top-left {
    gap: 1rem;
  }

  .top-right {
    gap: 0.75rem;
  }

  .location-text {
    font-size: 0.8rem;
  }

  .change-btn {
    display: none;
  }

  /* Ocultar algunos links en mobile para no saturar */
  .top-link:nth-child(2) {
    display: none;
  }
}

@media (max-width: 480px) {
  .top-bar {
    font-size: 0.75rem;
  }

  .location-display {
    padding: 0.2rem 0.5rem;
  }

  .top-right {
    gap: 0.5rem;
  }

  .language-selector {
    padding: 0.2rem 0.5rem;
  }
}
</style>