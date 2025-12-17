<template>
  <!-- Teleport para montar el modal directamente en body -->
  <Teleport to="body">
    <Transition name="modal-fade">
      <div v-if="isOpen" class="custom-modal-overlay" @click.self="handleOverlayClick">
        <div class="custom-modal-container">
          <div class="custom-modal-dialog">
            <!-- Header -->
            <div class="modal-header">
              <h2>¡Postulación Enviada Exitosamente!</h2>
            </div>

            <!-- Content -->
            <div class="modal-content">
      <div class="success-icon"></div>

      <div class="success-message">
        <h3>Tu postulación ha sido enviada correctamente</h3>
        <p class="status-info">
          <strong>Estado:</strong> Tu postulación está siendo revisada por el empleador
        </p>
        <p class="info-text">
          El empleador revisará tu perfil y se pondrá en contacto contigo si cumples con los requisitos. Mientras tanto, puedes:
        </p>
      </div>

      <div class="job-info" v-if="applicationData">
        <div class="info-item">
          <strong>Puesto:</strong> {{ applicationData.job_title }}
        </div>
        <div class="info-item" v-if="applicationData.company">
          <strong>Empresa:</strong> {{ applicationData.company }}
        </div>
        <div class="info-item">
          <strong>ID de Postulación:</strong> {{ formatApplicationId(applicationData.id) }}
        </div>
        <div class="info-item">
          <strong>Fecha de Postulación:</strong>
          {{ formatDate(applicationData.applied_at) }}
        </div>
      </div>

      <div class="actions-container">
        <va-button
          class="btn-primary"
          @click="goToDashboard"
          size="large"
        >
          Ver Mis Postulaciones
        </va-button>
        <va-button
          preset="plain"
          class="btn-secondary"
          @click="searchMore"
          size="large"
        >
          Buscar Más Trabajos
        </va-button>
      </div>

      <div class="tips-container">
        <div class="tip">
          <span class="tip-icon">📊</span>
          <span>Puedes revisar el estado de tu postulación en el panel "Mis Postulaciones"</span>
        </div>
        <div class="tip">
          <span class="tip-icon">✉️</span>
          <span>Recibirás notificaciones cuando el empleador revise tu perfil o cambie el estado</span>
        </div>
        <div class="tip">
          <span class="tip-icon">💼</span>
          <span>Sigue postulando a más ofertas para aumentar tus oportunidades</span>
        </div>
      </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  applicationData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'search-more'])

const router = useRouter()

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const handleOverlayClick = () => {
  // No hacer nada - el modal no se puede cerrar haciendo click fuera
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (e) {
    return dateString
  }
}

const formatApplicationId = (id) => {
  if (!id) return 'N/A'
  // Mostrar solo los primeros 8 caracteres del UUID
  return id.substring(0, 8).toUpperCase()
}

const goToDashboard = async () => {
  isOpen.value = false
  // Esperar a que se cierre el modal
  await new Promise(resolve => setTimeout(resolve, 300))
  // Redirigir al dashboard de postulante - sección "Mis Postulaciones"
  router.push('/dashboard/applications')
}

const searchMore = async () => {
  isOpen.value = false
  // Esperar a que se cierre el modal
  await new Promise(resolve => setTimeout(resolve, 300))
  emit('search-more')
  // Volver a la vista de todos los trabajos (GuideView)
  router.push('/guias/trabajos')
}
</script>

<style scoped>
/* Modal Custom - Sin Vuestic */
.custom-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.05);
  z-index: 9998; /* Debajo del container pero visible */
  display: flex;
  align-items: center;
  justify-content: center;
  overflow-y: auto;
}

.custom-modal-container {
  position: fixed;
  z-index: 10001; /* MUY por encima del TopSearchBar (1000-1315) */
  width: 92%;
  max-width: 750px; /* Más ancho: de 600px a 750px */
  max-height: 90vh;
  overflow-y: auto;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.custom-modal-dialog {
  background: white;
  border-radius: 16px;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(0, 0, 0, 0.05);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Transición del modal */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-active .custom-modal-dialog,
.modal-fade-leave-active .custom-modal-dialog {
  transition: transform 0.3s ease;
}

.modal-fade-enter-from .custom-modal-dialog {
  transform: translateY(-50px);
}

.modal-fade-leave-to .custom-modal-dialog {
  transform: translateY(50px);
}

.modal-header {
  text-align: center;
  padding: 15px 0 10px 0;
}

.modal-header h2 {
  color: #7c3aed;
  font-size: 24px;
  font-weight: 700;
  margin: 0;
}

.modal-content {
  padding: 20px 25px;
  text-align: center;
}

.success-icon {
  width: 70px;
  height: 70px;
  background-color: #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  animation: scaleIn 0.6s ease-out;
  position: relative;
}

.success-icon::after {
  content: '';
  width: 25px;
  height: 13px;
  border: 2px solid white;
  border-top: none;
  border-right: none;
  transform: rotate(-45deg);
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.success-message h3 {
  color: #1a1a1a;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 10px 0;
}

.status-info {
  color: #7c3aed;
  font-weight: 500;
  margin: 8px 0;
  padding: 8px;
  background-color: #f9f5ff;
  border-radius: 6px;
  border-left: 3px solid #7c3aed;
  font-size: 13px;
}

.info-text {
  color: #666;
  margin: 10px 0;
  font-size: 13px;
}

.job-info {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 12px;
  margin: 15px 0;
  text-align: left;
}

.info-item {
  padding: 6px 0;
  font-size: 13px;
  color: #333;
  border-bottom: 1px solid #e0e0e0;
}

.info-item:last-child {
  border-bottom: none;
}

.actions-container {
  display: flex;
  gap: 12px;
  margin: 20px 0 15px 0;
  justify-content: center;
}

.btn-primary {
  background-color: #7c3aed;
  color: white;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  padding: 10px 20px !important;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #6d28d9;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(124, 58, 237, 0.2);
}

.btn-secondary {
  color: #7c3aed;
  border: 2px solid #7c3aed;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  padding: 8px 18px !important;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background-color: #f9f5ff;
  border-color: #6d28d9;
  color: #6d28d9;
}

.tips-container {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #e0e0e0;
}

.tip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  margin: 6px 0;
  background-color: #f0f9ff;
  border-radius: 6px;
  text-align: left;
  color: #0c4a6e;
  font-size: 12px;
}

.tip-icon {
  font-size: 18px;
  flex-shrink: 0;
}

@media (max-width: 600px) {
  .modal-content {
    padding: 15px 20px;
  }

  .modal-header {
    padding: 12px 0 8px 0;
  }

  .actions-container {
    flex-direction: column;
    margin: 15px 0 10px 0;
    gap: 8px;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    padding: 10px 20px !important;
  }

  .modal-header h2 {
    font-size: 20px;
  }

  .success-icon {
    width: 60px;
    height: 60px;
    margin: 0 auto 12px;
  }

  .success-icon::after {
    width: 20px;
    height: 10px;
    border-width: 2px;
  }

  .tip {
    padding: 6px 8px;
    margin: 5px 0;
    font-size: 11px;
  }
}
</style>
