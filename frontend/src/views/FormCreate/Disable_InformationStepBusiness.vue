<!-- frontend/src/components/Publish/InformationStepBusiness.vue -->
<!-- ✅ VERSIÓN CORREGIDA - CON BRANCH MANAGER SIN RESTRICCIONES -->
<template>
  <div class="information-step-business">
    
    <!-- HEADER -->
    <div class="step-header">
      <div class="header-icon">
        <va-icon name="business" size="2rem" color="purple" />
      </div>
      <div>
        <h2 class="step-title">Información del Negocio</h2>
        <p class="step-subtitle">
          Completa los datos principales de tu empresa
        </p>
      </div>
    </div>

    <!-- FORMULARIO -->
    <div class="form-content">
      
      <!-- INFORMACIÓN BÁSICA -->
      <div class="form-section">
        <h3 class="section-title">
          <va-icon name="info" size="1.25rem" />
          Información Básica
        </h3>

        <div class="form-grid">
          <!-- NOMBRE DEL NEGOCIO -->
          <div class="form-row">
            <va-input
              v-model="localFormData.title"
              label="Nombre del Negocio"
              placeholder="Ej: Fábrica de Plásticos Belén"
              required-mark
              :rules="[
                (v) => !!v || 'El nombre del negocio es requerido',
                (v) => (v && v.length >= 5) || 'Mínimo 5 caracteres',
                (v) => (v && v.length <= 100) || 'Máximo 100 caracteres'
              ]"
              counter
              maxlength="100"
            >
              <template #prepend>
                <va-icon name="business" color="purple" />
              </template>
            </va-input>
            
            <div class="input-hint">
              <va-icon name="info" size="small" />
              <span>Usa el nombre oficial de tu empresa</span>
            </div>
          </div>

          <!-- CATEGORÍA -->
          <div class="form-row">
            <va-select
              v-model="localFormData.businessCategory"
              label="Categoría del Negocio"
              :options="categoryOptions"
              placeholder="Selecciona una categoría"
              required-mark
              :rules="[(v) => !!v || 'La categoría es requerida']"
            >
              <template #prepend>
                <va-icon name="category" color="purple" />
              </template>
            </va-select>
            
            <div class="input-hint">
              <va-icon name="info" size="small" />
              <span>Selecciona la categoría que mejor describe tu negocio</span>
            </div>
          </div>
        </div>

        <!-- DESCRIPCIÓN -->
        <div class="form-row">
          <va-textarea
            v-model="localFormData.description"
            label="Descripción del Negocio"
            placeholder="Describe tu negocio, productos y servicios..."
            :min-rows="4"
            :max-rows="10"
            counter
            maxlength="500"
            required-mark
            :rules="[
              (v) => !!v || 'La descripción es requerida',
              (v) => (v && v.length >= 50) || 'Mínimo 50 caracteres para una buena descripción'
            ]"
          >
            <template #prepend>
              <va-icon name="description" color="purple" />
            </template>
          </va-textarea>
          
          <div class="input-hint">
            <va-icon name="lightbulb" size="small" />
            <span>Una buena descripción ayuda a atraer más clientes. Menciona productos, servicios y ventajas.</span>
          </div>
        </div>

        <!-- DIRECCIÓN -->
        <div class="form-row">
          <va-input
            v-model="localFormData.address"
            label="Dirección"
            placeholder="Ej: Av. América #123, Zona Sur"
            required-mark
            :rules="[(v) => !!v || 'La dirección es requerida']"
          >
            <template #prepend>
              <va-icon name="location_on" color="purple" />
            </template>
          </va-input>
          
          <div class="input-hint">
            <va-icon name="info" size="small" />
            <span>Dirección completa de tu negocio</span>
          </div>
        </div>
      </div>

      <!-- INFORMACIÓN DE CONTACTO -->
      <div class="form-section">
        <h3 class="section-title">
          <va-icon name="contact_phone" size="1.25rem" />
          Información de Contacto
        </h3>

        <div class="form-grid">
          <!-- WHATSAPP (OBLIGATORIO) -->
          <div class="form-row">
            <va-input
              v-model="localFormData.whatsapp"
              label="WhatsApp"
              placeholder="70123456"
              required-mark
              :rules="[
                (v) => !!v || 'WhatsApp es obligatorio',
                (v) => /^[67]\d{7}$/.test(v) || 'Número inválido (debe empezar con 6 o 7 y tener 8 dígitos)'
              ]"
            >
              <template #prepend>
                <span class="whatsapp-prefix">+591</span>
              </template>
              <template #append>
                <va-icon name="whatsapp" color="success" />
              </template>
            </va-input>
            
            <div class="input-hint success-hint">
              <va-icon name="check_circle" size="small" />
              <span>Los clientes podrán contactarte directamente por WhatsApp</span>
            </div>
          </div>

          <!-- EMAIL (OPCIONAL) -->
          <div class="form-row">
            <va-input
              v-model="localFormData.email"
              label="Email (Opcional)"
              placeholder="contacto@negocio.com"
              type="email"
              :rules="[
                (v) => !v || /.+@.+\..+/.test(v) || 'El email no es válido'
              ]"
            >
              <template #prepend>
                <va-icon name="email" color="purple" />
              </template>
            </va-input>
          </div>
        </div>

        <div class="form-grid">
          <!-- SITIO WEB (OPCIONAL) -->
          <div class="form-row">
            <va-input
              v-model="localFormData.website"
              label="Sitio Web (Opcional)"
              placeholder="https://www.minegocio.com"
              :rules="[
                (v) => !v || v.startsWith('http://') || v.startsWith('https://') || 'Debe empezar con http:// o https://'
              ]"
            >
              <template #prepend>
                <va-icon name="language" color="purple" />
              </template>
            </va-input>
          </div>

          <!-- NIT/RUC -->
          <div class="form-row">
            <va-input
              v-model="localFormData.nit"
              label="NIT / RUC"
              placeholder="Ej: 123456789"
              required-mark
              :rules="[(v) => !!v || 'El NIT/RUC es requerido']"
            >
              <template #prepend>
                <va-icon name="badge" color="purple" />
              </template>
            </va-input>
            
            <div class="input-hint">
              <va-icon name="info" size="small" />
              <span>Número de identificación tributaria</span>
            </div>
          </div>
        </div>
      </div>

      <!-- SUCURSALES ADICIONALES -->
      <BranchManager
        ref="branchManagerRef"
        v-model="localFormData.branches"
        :cities="cities"
        :disable-plan-restrictions="true"
      />

      <!-- REDES SOCIALES -->
      <div class="form-section">
        <h3 class="section-title">
          <va-icon name="share" size="1.25rem" />
          Redes Sociales (Opcional)
        </h3>
        <p class="section-description">
          Conecta tus redes sociales para mayor alcance
        </p>

        <SocialMediaFields v-model="localFormData.socialMedia" />
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import SocialMediaFields from '@/components/Common/SocialMediaFields.vue'
import BranchManager from '@/components/Common/BranchManager.vue'

// ========== PROPS Y EMITS ==========
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  cities: {
    type: Array,
    default: () => [
      { id: 'cochabamba', name: 'Cochabamba' },
      { id: 'la-paz', name: 'La Paz' },
      { id: 'santa-cruz', name: 'Santa Cruz' },
      { id: 'oruro', name: 'Oruro' },
      { id: 'potosi', name: 'Potosí' },
      { id: 'sucre', name: 'Sucre' },
      { id: 'tarija', name: 'Tarija' },
      { id: 'beni', name: 'Beni' },
      { id: 'pando', name: 'Pando' }
    ]
  }
})

const emit = defineEmits(['update:modelValue'])

// ========== REFS ==========
const branchManagerRef = ref(null)

// ========== DATA LOCAL (REF + WATCH) ==========
const localFormData = ref({
  title: props.modelValue.title || '',
  businessCategory: props.modelValue.businessCategory || '',
  description: props.modelValue.description || '',
  address: props.modelValue.address || '',
  whatsapp: props.modelValue.whatsapp || '',
  email: props.modelValue.email || '',
  website: props.modelValue.website || '',
  nit: props.modelValue.nit || '',
  branches: props.modelValue.branches || [],
  socialMedia: props.modelValue.socialMedia || {
    facebook: '',
    instagram: '',
    twitter: '',
    linkedin: ''
  }
})

// ========== OPCIONES DE FORMULARIO ==========
const categoryOptions = [
  { text: 'Manufactura', value: 'Manufactura' },
  { text: 'Servicios', value: 'Servicios' },
  { text: 'Comercio', value: 'Comercio' },
  { text: 'Tecnología', value: 'Tecnología' },
  { text: 'Alimentación', value: 'Alimentación' },
  { text: 'Construcción', value: 'Construcción' },
  { text: 'Textil', value: 'Textil' },
  { text: 'Automotriz', value: 'Automotriz' },
  { text: 'Salud', value: 'Salud' },
  { text: 'Educación', value: 'Educación' },
  { text: 'Turismo', value: 'Turismo' },
  { text: 'Otro', value: 'Otro' }
]

// ========== WATCH PARA SINCRONIZACIÓN ==========
watch(localFormData, (newValue) => {
  emit('update:modelValue', { ...props.modelValue, ...newValue })
}, { deep: true })

// ========== VALIDACIÓN ==========
const validate = () => {
  const errors = []
  
  if (!localFormData.value.title || localFormData.value.title.length < 5) {
    errors.push('El nombre del negocio debe tener al menos 5 caracteres')
  }
  
  if (!localFormData.value.businessCategory) {
    errors.push('La categoría es requerida')
  }
  
  if (!localFormData.value.description || localFormData.value.description.length < 50) {
    errors.push('La descripción debe tener al menos 50 caracteres')
  }
  
  if (!localFormData.value.address) {
    errors.push('La dirección es requerida')
  }
  
  if (!localFormData.value.whatsapp) {
    errors.push('El WhatsApp es obligatorio')
  } else if (!/^[67]\d{7}$/.test(localFormData.value.whatsapp)) {
    errors.push('El número de WhatsApp debe ser válido (8 dígitos, empezar con 6 o 7)')
  }
  
  if (localFormData.value.email && !/.+@.+\..+/.test(localFormData.value.email)) {
    errors.push('El email no es válido')
  }
  
  if (localFormData.value.website && 
      !localFormData.value.website.startsWith('http://') && 
      !localFormData.value.website.startsWith('https://')) {
    errors.push('La URL debe empezar con http:// o https://')
  }
  
  if (!localFormData.value.nit) {
    errors.push('El NIT/RUC es requerido')
  }
  
  // Validar sucursales usando el ref del BranchManager
  if (branchManagerRef.value && !branchManagerRef.value.validate()) {
    errors.push('Hay errores en la información de las sucursales')
  }
  
  if (errors.length > 0) {
    console.error('Errores de validación:', errors)
    return false
  }
  
  return true
}

// ========== EXPONER MÉTODOS AL PADRE ==========
defineExpose({
  validate
})
</script>

<style scoped>
.information-step-business {
  width: 100%;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #E0E0E0;
}

.header-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, #5C0099 0%, #4A0077 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(92, 0, 153, 0.2);
}

.step-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2C1654;
  margin: 0;
}

.step-subtitle {
  font-size: 1rem;
  color: #666;
  margin: 0.25rem 0 0 0;
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #5C0099;
  margin: 0 0 0.5rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #F5F5F5;
}

.section-description {
  color: #666;
  font-size: 0.95rem;
  margin: -0.5rem 0 0.5rem 0;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.input-hint {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #666;
  padding: 0.5rem;
  background: #F5F5F5;
  border-radius: 8px;
}

.success-hint {
  background: #E8F5E9;
  color: #2E7D32;
}

.whatsapp-prefix {
  font-weight: 700;
  color: #5C0099;
  padding: 0.5rem;
  background: #F5F5F5;
  border-radius: 6px;
}

@media (max-width: 768px) {
  .step-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .header-icon {
    width: 56px;
    height: 56px;
  }

  .step-title {
    font-size: 1.25rem;
  }

  .step-subtitle {
    font-size: 0.9rem;
  }

  .section-title {
    font-size: 1.1rem;
  }
}
</style>