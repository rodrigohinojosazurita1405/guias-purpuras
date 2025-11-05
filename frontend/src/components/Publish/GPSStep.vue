<!-- frontend/src/components/Publish/GPSStep.vue -->
<!-- PASO OPCIONAL: UBICACIÓN GPS - REUTILIZABLE PARA TODAS LAS GUÍAS -->
<template>
  <div class="gps-step">
    
    <!-- Header -->
    <div class="step-header">
      <div class="header-content">
        <va-icon name="place" size="3rem" color="#5C0099" />
        <div class="header-text">
          <h2 class="step-title">Ubicación GPS</h2>
          <p class="step-description">
            Agrega tu ubicación para que los clientes te encuentren fácilmente
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
      
      <ul class="benefits-list">
        <li class="benefit-item">
          <div class="benefit-icon">
            <va-icon name="search" size="1.5rem" color="#4CAF50" />
          </div>
          <div class="benefit-content">
            <strong>Aparece en búsquedas locales</strong>
            <p>Los clientes cercanos te encontrarán cuando busquen en su zona</p>
          </div>
        </li>
        
        <li class="benefit-item">
          <div class="benefit-icon">
            <va-icon name="navigation" size="1.5rem" color="#4CAF50" />
          </div>
          <div class="benefit-content">
            <strong>Fácil de encontrar</strong>
            <p>Tus clientes pueden usar el mapa para llegar directamente a ti</p>
          </div>
        </li>
        
        <li class="benefit-item">
          <div class="benefit-icon">
            <va-icon name="verified" size="1.5rem" color="#4CAF50" />
          </div>
          <div class="benefit-content">
            <strong>Mayor confianza</strong>
            <p>Mostrar tu ubicación genera credibilidad y profesionalismo</p>
          </div>
        </li>
        
        <li class="benefit-item">
          <div class="benefit-icon">
            <va-icon name="trending_up" size="1.5rem" color="#4CAF50" />
          </div>
          <div class="benefit-content">
            <strong>Más visibilidad</strong>
            <p>Los anuncios con ubicación reciben 3x más contactos</p>
          </div>
        </li>
      </ul>
    </div>

    <!-- Componente GPS -->
    <div class="gps-container">
      <GPSLocation
        v-model:coordinates="localCoordinates"
        v-model:address="localAddress"
      />
    </div>

    <!-- Skip Option -->
    <div class="skip-notice">
      <va-icon name="info" size="small" color="#666" />
      <span>Puedes omitir este paso y agregarlo después si lo prefieres</span>
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

const emit = defineEmits(['update:coordinates', 'update:address'])

const localCoordinates = ref(props.coordinates)
const localAddress = ref(props.address)

// Watch para emitir cambios
watch(localCoordinates, (newVal) => {
  emit('update:coordinates', newVal)
})

watch(localAddress, (newVal) => {
  emit('update:address', newVal)
})

// Método de validación (siempre pasa porque es opcional)
const validate = () => {
  return true // GPS es opcional
}

// Exponer validate para uso externo
defineExpose({
  validate
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
  margin-bottom: 2rem;
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
  color: #333;
  margin: 0 0 0.5rem 0;
}

.step-description {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
  line-height: 1.6;
}

/* ========== Motivation Box ========== */
.motivation-box {
  background: linear-gradient(135deg, #FFF8E1 0%, #FFFFFF 100%);
  border: 2px solid #FFD54F;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2.5rem;
}

.motivation-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.motivation-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

/* ========== Benefits List ========== */
.benefits-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.benefit-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.benefit-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #E8F5E9;
  border-radius: 12px;
}

.benefit-content {
  flex: 1;
}

.benefit-content strong {
  display: block;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.25rem;
}

.benefit-content p {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
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
  padding: 1rem 1.5rem;
  background: #F5F5F5;
  border-radius: 8px;
  color: #666;
  font-size: 0.95rem;
  text-align: center;
  justify-content: center;
}

/* ========== Responsive ========== */
@media (max-width: 992px) {
  .benefits-list {
    grid-template-columns: 1fr;
    gap: 1.25rem;
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

  .benefit-item {
    gap: 0.75rem;
  }

  .benefit-icon {
    width: 40px;
    height: 40px;
  }
}
</style>