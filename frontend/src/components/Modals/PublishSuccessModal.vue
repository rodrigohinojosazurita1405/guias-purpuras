<template>
  <va-modal
    v-model="isOpen"
    :closeable="false"
    :ok-text="null"
    :cancel-text="null"
    class="success-modal"
    size="large"
  >
    <template #header>
      <div class="modal-header">
        <h2>Anuncio Publicado Exitosamente</h2>
      </div>
    </template>

    <div class="modal-content">
      <div class="success-icon"></div>

      <div class="success-message">
        <h3>Tu oferta de trabajo ha sido publicada exitosamente</h3>
        <p class="status-info">
          <strong>Estado:</strong> En aprobación por el equipo de Guías Púrpuras
        </p>
        <p class="info-text">
          Tu anuncio será revisado y activado en breve. Mientras tanto, puedes:
        </p>
      </div>

      <div class="job-info" v-if="jobData">
        <div class="info-item">
          <strong>Título:</strong> {{ jobData.title }}
        </div>
        <div class="info-item">
          <strong>ID:</strong> {{ jobData.id }}
        </div>
        <div class="info-item">
          <strong>Fecha de Publicación:</strong>
          {{ formatDate(jobData.createdAt) }}
        </div>
      </div>

      <div class="actions-container">
        <va-button
          class="btn-primary"
          @click="goToDashboard"
          size="large"
        >
          Ir a Mis Anuncios
        </va-button>
        <va-button
          preset="plain"
          class="btn-secondary"
          @click="publishAnother"
          size="large"
        >
          Publicar Otro Anuncio
        </va-button>
      </div>

      <div class="tips-container">
        <div class="tip">
          <span class="tip-icon">ℹ</span>
          <span>Puedes ver el estado de tu anuncio en la sección "Mis Anuncios" del panel de control</span>
        </div>
        <div class="tip">
          <span class="tip-icon">✉</span>
          <span>Recibirás una notificación por email cuando tu anuncio sea aprobado</span>
        </div>
      </div>
    </div>
  </va-modal>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/useAuthStore'

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  jobData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'publish-another'])

const router = useRouter()
const authStore = useAuthStore()

const isOpen = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

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

const goToDashboard = async () => {
  isOpen.value = false
  // Esperar a que se cierre el modal
  await new Promise(resolve => setTimeout(resolve, 300))
  router.push('/dashboard/jobs-manager')
}

const publishAnother = async () => {
  isOpen.value = false
  // Esperar a que se cierre el modal
  await new Promise(resolve => setTimeout(resolve, 300))
  emit('publish-another')
  router.push('/publicar')
}
</script>

<style scoped>
.success-modal :deep(.va-modal__container) {
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.modal-header {
  text-align: center;
  padding: 20px 0;
}

.modal-header h2 {
  color: #7c3aed;
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

.modal-content {
  padding: 30px;
  text-align: center;
}

.success-icon {
  width: 100px;
  height: 100px;
  background-color: #10b981;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  animation: scaleIn 0.6s ease-out;
  position: relative;
}

.success-icon::after {
  content: '';
  width: 35px;
  height: 18px;
  border: 3px solid white;
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
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 15px 0;
}

.status-info {
  color: #7c3aed;
  font-weight: 500;
  margin: 10px 0;
  padding: 10px;
  background-color: #f9f5ff;
  border-radius: 8px;
  border-left: 3px solid #7c3aed;
}

.info-text {
  color: #666;
  margin: 15px 0;
  font-size: 14px;
}

.job-info {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 15px;
  margin: 20px 0;
  text-align: left;
}

.info-item {
  padding: 8px 0;
  font-size: 14px;
  color: #333;
  border-bottom: 1px solid #e0e0e0;
}

.info-item:last-child {
  border-bottom: none;
}

.actions-container {
  display: flex;
  gap: 15px;
  margin: 30px 0;
  justify-content: center;
}

.btn-primary {
  background-color: #7c3aed;
  color: white;
  border-radius: 8px;
  font-weight: 600;
  padding: 12px 30px !important;
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
  padding: 10px 30px !important;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background-color: #f9f5ff;
  border-color: #6d28d9;
  color: #6d28d9;
}

.tips-container {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
}

.tip {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  margin: 10px 0;
  background-color: #f0f9ff;
  border-radius: 8px;
  text-align: left;
  color: #0c4a6e;
  font-size: 13px;
}

.tip-icon {
  font-size: 18px;
  flex-shrink: 0;
}

@media (max-width: 600px) {
  .modal-content {
    padding: 20px;
  }

  .actions-container {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }

  .modal-header h2 {
    font-size: 22px;
  }

  .success-icon {
    width: 70px;
    height: 70px;
  }

  .success-icon::after {
    width: 25px;
    height: 13px;
    border-width: 2px;
  }
}
</style>
