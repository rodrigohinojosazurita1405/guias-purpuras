<!-- frontend/src/components/Profile/CompanyProfileEdit.vue -->
<template>
  <div class="company-edit-container">
    <div class="edit-header">
      <h2>Perfil De La Empresa</h2>
      <va-button
        preset="plain"
        color="textPrimary"
        @click="$emit('close')"
      >
        <va-icon name="close" size="large" />
      </va-button>
    </div>

    <!-- No Company Message -->
    <div v-if="!showForm" class="no-company-message">
      <va-icon name="business" size="3rem" color="purple" />
      <h3>No tienes perfil de empresa aún</h3>
      <p>Crea uno para publicar anuncios y gestionar tu negocio</p>
      <button class="purple-btn-gradient" @click="showForm = true">
        <va-icon name="add" />
        Crear Perfil De Empresa
      </button>
    </div>

    <!-- Loading State -->
    <div v-else-if="loading" class="loading-state">
      <va-progress-bar indeterminate color="purple" size="large" />
    </div>

    <!-- Form -->
    <form v-else @submit.prevent="handleSaveCompany" class="company-form">
      <!-- Nombre de Empresa -->
      <div class="form-group">
        <label class="form-label">Nombre de la Empresa *</label>
        <va-input
          v-model="formData.companyName"
          placeholder="Tech Solutions Bolivia"
          class="form-input"
          required
        />
      </div>

      <!-- Email Empresa -->
      <div class="form-group">
        <label class="form-label">Email de la Empresa *</label>
        <va-input
          v-model="formData.email"
          type="email"
          placeholder="contact@company.com"
          class="form-input"
          required
        />
      </div>

      <!-- Teléfono -->
      <div class="form-group">
        <label class="form-label">Teléfono</label>
        <va-input
          v-model="formData.phone"
          placeholder="+591..."
          type="tel"
          class="form-input"
        />
      </div>

      <!-- Sitio Web -->
      <div class="form-group">
        <label class="form-label">Sitio Web</label>
        <va-input
          v-model="formData.website"
          placeholder="https://company.com"
          type="url"
          class="form-input"
        />
      </div>

      <!-- Ubicación -->
      <div class="form-group">
        <label class="form-label">Ubicación</label>
        <va-input
          v-model="formData.location"
          placeholder="La Paz, Bolivia"
          class="form-input"
        />
      </div>

      <!-- Ciudad -->
      <div class="form-group">
        <label class="form-label">Ciudad</label>
        <va-select
          v-model="formData.city"
          :options="cities"
          class="form-input"
        />
      </div>

      <!-- Descripción -->
      <div class="form-group">
        <label class="form-label">Descripción</label>
        <va-textarea
          v-model="formData.description"
          placeholder="Cuéntanos sobre tu empresa..."
          rows="4"
          class="form-textarea"
        />
      </div>

      <!-- Categoría -->
      <div class="form-group">
        <label class="form-label">Categoría</label>
        <va-select
          v-model="formData.category"
          :options="categories"
          class="form-input"
        />
      </div>

      <!-- Submit Button -->
      <div class="form-actions">
        <button type="submit" class="purple-btn-gradient" :disabled="saving">
          <va-icon name="save" />
          {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToast } from 'vuestic-ui'

// ========== COMPOSABLES ==========
const { init: notify } = useToast()

// ========== PROPS ==========
const props = defineProps({
  userProfileId: {
    type: String,
    required: true
  },
  companyProfileId: {
    type: String,
    default: null
  }
})

// ========== EMITS ==========
const emit = defineEmits(['close', 'created', 'updated'])

// ========== DATA ==========
const loading = ref(false)
const saving = ref(false)
const showForm = ref(false)

const formData = ref({
  companyName: '',
  email: '',
  phone: '',
  website: '',
  location: '',
  city: '',
  description: '',
  category: 'other'
})

const cities = [
  'La Paz',
  'Cochabamba',
  'Santa Cruz',
  'Oruro',
  'Potosí',
  'Tarija',
  'Chuquisaca',
  'Beni',
  'Pando'
]

const categories = [
  { text: 'Empleador - Trabajos', value: 'jobs' },
  { text: 'Restaurante - Gastronomía', value: 'restaurant' },
  { text: 'Negocio', value: 'business' },
  { text: 'Profesional', value: 'professional' },
  { text: 'Otro', value: 'other' }
]

// ========== LIFECYCLE ==========
onMounted(() => {
  if (props.companyProfileId) {
    loadCompanyProfile()
    showForm.value = true
  }
})

// ========== METHODS ==========
const loadCompanyProfile = async () => {
  try {
    loading.value = true
    const response = await fetch(`/api/profiles/company/${props.companyProfileId}/`)

    if (!response.ok) {
      throw new Error('No se pudo cargar el perfil de empresa')
    }

    const data = await response.json()
    if (data.success && data.profile) {
      formData.value = {
        companyName: data.profile.companyName,
        email: data.profile.email,
        phone: data.profile.phone || '',
        website: data.profile.website || '',
        location: data.profile.location || '',
        city: data.profile.city || '',
        description: data.profile.description || '',
        category: data.profile.category || 'other'
      }
    }
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  } finally {
    loading.value = false
  }
}

const handleSaveCompany = async () => {
  try {
    // Validación
    if (!formData.value.companyName.trim()) {
      notify({
        message: '⚠️ El nombre de la empresa es requerido',
        color: 'warning',
        duration: 3000
      })
      return
    }

    if (!formData.value.email.trim()) {
      notify({
        message: '⚠️ El email es requerido',
        color: 'warning',
        duration: 3000
      })
      return
    }

    saving.value = true

    // Crear o actualizar
    if (props.companyProfileId) {
      // Actualizar
      const response = await fetch(`/api/profiles/company/${props.companyProfileId}/edit`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData.value)
      })

      if (!response.ok) {
        throw new Error('Error al guardar')
      }

      const data = await response.json()
      if (data.success) {
        notify({
          message: '✅ Perfil de empresa actualizado',
          color: 'success',
          duration: 5000
        })
        emit('updated', data.profile)
        setTimeout(() => emit('close'), 1000)
      }
    } else {
      // Crear
      const response = await fetch('/api/profiles/company/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          userProfileId: props.userProfileId,
          ...formData.value
        })
      })

      if (!response.ok) {
        throw new Error('Error al crear')
      }

      const data = await response.json()
      if (data.success) {
        notify({
          message: '✅ Perfil de empresa creado',
          color: 'success',
          duration: 5000
        })
        emit('created', data.profile)
        setTimeout(() => emit('close'), 1000)
      }
    }
  } catch (err) {
    notify({
      message: `Error: ${err.message}`,
      color: 'danger',
      duration: 5000
    })
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.company-edit-container {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 2.5rem;
  max-width: 600px;
  margin: 0 auto;
}

.edit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.edit-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.no-company-message {
  text-align: center;
  padding: 2rem;
}

.no-company-message h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
  margin: 1rem 0 0.5rem;
}

.no-company-message p {
  color: #666;
  margin-bottom: 1.5rem;
}

.loading-state {
  text-align: center;
  padding: 2rem;
}

.company-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  display: block;
  font-weight: 600;
  color: #333;
  font-size: 0.95rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #5C0099;
  box-shadow: 0 0 0 3px rgba(92, 0, 153, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f0f0f0;
}

/* Purple Button Gradient */
.purple-btn-gradient {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.purple-btn-gradient:hover {
  background: linear-gradient(135deg, #6d28d9, #5b21b6);
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  transform: translateY(-2px);
}

.purple-btn-gradient:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Responsive */
@media (max-width: 768px) {
  .company-edit-container {
    padding: 1.5rem;
  }

  .edit-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .edit-header h2 {
    font-size: 1.25rem;
  }
}
</style>
