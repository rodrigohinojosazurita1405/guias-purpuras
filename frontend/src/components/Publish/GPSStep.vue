<!-- frontend/src/components/Publish/GPSStep.vue -->
<!-- PASO OPCIONAL: UBICACIÓN GPS - REUTILIZABLE PARA TODAS LAS GUÍAS -->
<template>
  <div class="gps-step">
    
    <!-- Header -->
    <div class="step-header">
      <div class="header-content">
        <va-icon name="place" size="3rem" color="#FF6B6B" />
        <div class="header-text">
          <h2 class="step-title">Ubicación GPS</h2>
          <p class="step-description">
            Agrega tu ubicación para que los clientes te encuentren fácilmente en el mapa
          </p>
        </div>
      </div>
      <VaBadge text="Opcional" color="warning" size="large" />
    </div>

    <!-- Mensaje Motivador -->
    <div class="motivation-box">
      <div class="motivation-header">
        <va-icon name="lightbulb" size="2rem" color="#FFC107" />
        <h3 class="motivation-title">¿Por qué agregar tu ubicación?</h3>
      </div>
      
      <div class="benefits-grid">
        <div class="benefit-card">
          <div class="benefit-icon green">
            <va-icon name="search" size="1.5rem" />
          </div>
          <div class="benefit-content">
            <strong>Aparece en búsquedas locales</strong>
            <p>Los clientes cercanos te encontrarán cuando busquen en su zona</p>
          </div>
        </div>
        
        <div class="benefit-card">
          <div class="benefit-icon blue">
            <va-icon name="navigation" size="1.5rem" />
          </div>
          <div class="benefit-content">
            <strong>Fácil de encontrar</strong>
            <p>Tus clientes pueden usar el mapa para llegar directamente a ti</p>
          </div>
        </div>
        
        <div class="benefit-card">
          <div class="benefit-icon purple">
            <va-icon name="verified" size="1.5rem" />
          </div>
          <div class="benefit-content">
            <strong>Mayor confianza</strong>
            <p>Mostrar tu ubicación genera credibilidad y profesionalismo</p>
          </div>
        </div>
        
        <div class="benefit-card">
          <div class="benefit-icon success">
            <va-icon name="trending_up" size="1.5rem" />
          </div>
          <div class="benefit-content">
            <strong>Más visibilidad</strong>
            <p>Los anuncios con ubicación reciben 3x más contactos</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Componente GPS -->
    <div class="gps-container">
      <GPSLocation
        v-model:coordinates="localCoordinates"
        v-model:address="localAddress"
        ref="gpsLocationRef"
      />
    </div>

    <!-- Skip Option -->
    <div class="skip-notice">
      <va-icon name="info" size="small" color="#FF6B6B" />
      <span>Puedes omitir este paso y agregarlo después desde el dashboard</span>
    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import GPSLocation from '@/components/Location/GPSLocation.vue'

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

const emit = defineEmits(['update:coordinates', 'update:address', 'validation-change'])

const localCoordinates = ref(props.coordinates)
const localAddress = ref(props.address)
const gpsLocationRef = ref(null)

// Watch para emitir cambios
watch(localCoordinates, (newVal) => {
  emit('update:coordinates', newVal)
  checkValidation()
})

watch(localAddress, (newVal) => {
  emit('update:address', newVal)
})

// Verificar validación
const checkValidation = () => {
  if (gpsLocationRef.value) {
    const data = gpsLocationRef.value.getLocationData()
    emit('validation-change', data.isValid)
  }
}

// Método de validación (siempre pasa porque es opcional)
const validate = () => {
  return true // GPS es opcional
}

// Obtener datos para Django
const getLocationData = () => {
  if (gpsLocationRef.value) {
    return gpsLocationRef.value.getLocationData()
  }
  return null
}

// Exponer métodos para uso externo
defineExpose({
  validate,
  getLocationData
})
</script>

<style scoped>
/* ========== Container ========== */
.gps-step {
  padding: 2.5rem;
  background: white;
  border-radius: 16px;
  max-width: 1000px;
  margin: 0 auto;
}

/* ========== Header ========== */
.step-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2.5rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid #F0F0F0;
}

.header-content {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
  flex: 1;
}

.header-text {
  flex: 1;
}

.step-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 0.5rem 0;
}

.step-description {
  font-size: 1.1rem;
  color: #6B7280;
  margin: 0;
  line-height: 1.6;
}

/* ========== Motivation Box ========== */
.motivation-box {
  background: linear-gradient(135deg, #FFF9E6 0%, #FFFFFF 100%);
  border: 2px solid #FCD34D;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2.5rem;
  box-shadow: 0 2px 8px rgba(252, 211, 77, 0.1);
}

.motivation-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.75rem;
}

.motivation-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0;
}

/* ========== Benefits Grid ========== */
.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.25rem;
}

.benefit-card {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  border: 2px solid #F3F4F6;
  transition: all 0.3s;
}

.benefit-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  border-color: #E5E7EB;
}

.benefit-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.benefit-icon.green {
  background: #D1FAE5;
  color: #059669;
}

.benefit-icon.blue {
  background: #DBEAFE;
  color: #2563EB;
}

.benefit-icon.purple {
  background: #E9D5FF;
  color: #7C3AED;
}

.benefit-icon.success {
  background: #D1FAE5;
  color: #10B981;
}

.benefit-content {
  flex: 1;
}

.benefit-content strong {
  display: block;
  font-size: 1rem;
  font-weight: 600;
  color: #1F2937;
  margin-bottom: 0.35rem;
}

.benefit-content p {
  margin: 0;
  font-size: 0.875rem;
  color: #6B7280;
  line-height: 1.5;
}

/* ========== GPS Container ========== */
.gps-container {
  margin-bottom: 2rem;
}

/* ========== Skip Notice ========== */
.skip-notice {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #F9FAFB 0%, #FFFFFF 100%);
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  color: #4B5563;
  font-size: 0.95rem;
  text-align: center;
  justify-content: center;
  font-weight: 500;
}

/* ========== Responsive ========== */
@media (max-width: 992px) {
  .benefits-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
}

@media (max-width: 768px) {
  .gps-step {
    padding: 1.5rem;
  }

  .step-header {
    flex-direction: column;
    gap: 1rem;
  }

  .header-content {
    flex-direction: column;
    gap: 1rem;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .step-description {
    font-size: 1rem;
  }

  .motivation-box {
    padding: 1.5rem;
  }

  .motivation-title {
    font-size: 1.1rem;
  }

  .benefits-grid {
    grid-template-columns: 1fr;
  }

  .benefit-card {
    gap: 0.75rem;
    padding: 1.25rem;
  }

  .benefit-icon {
    width: 44px;
    height: 44px;
  }
}
</style>