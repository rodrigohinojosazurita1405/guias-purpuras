<!-- 
  ==========================================
  INFORMATIONSTEPGASTRONOMIA.VUE
  ==========================================
  
  Formulario específico para la categoría GASTRONOMÍA
  (Restaurantes, Cafeterías, Heladerías, etc.)
  
  Campos específicos:
    - Nombre del establecimiento
    - Tipo de cocina
    - Rango de precios
    - Horarios de atención
    - Menú (PDF o texto)
    - Delivery disponible
    - Capacidad
    - Estacionamiento
    - Logo del restaurante
-->

<template>
  <div class="information-step-gastronomia">
    <!-- 
      ==========================================
      HEADER
      ==========================================
    -->
    <div class="step-header">
      <div class="header-icon">
        <va-icon name="restaurant" size="2rem" color="purple" />
      </div>
      <div>
        <h2 class="step-title">Información del Anuncio</h2>
        <p class="step-subtitle">
          Describe tu establecimiento de forma clara y atractiva
        </p>
      </div>
    </div>

    <!-- 
      ==========================================
      FORMULARIO
      ==========================================
    -->
    <div class="form-content">
      
      <!-- 
        ==========================================
        INFORMACIÓN BÁSICA
        ==========================================
      -->
      <div class="form-section">
        <h3 class="section-title">
          <va-icon name="info" size="1.25rem" />
          Información Básica
        </h3>

        <!-- Nombre del Establecimiento -->
        <div class="form-row">
          <va-input
            v-model="localFormData.title"
            label="Nombre del Establecimiento"
            placeholder="Ej: Restaurante El Sabor Boliviano"
            :rules="[
              (v) => !!v || 'El nombre es obligatorio',
              (v) => (v && v.length >= 5) || 'Mínimo 5 caracteres',
              (v) => (v && v.length <= 100) || 'Máximo 100 caracteres'
            ]"
            counter
            maxlength="100"
            required-mark
          >
            <template #prepend>
              <va-icon name="storefront" color="purple" />
            </template>
          </va-input>
          
          <div class="input-hint">
            <va-icon name="info" size="small" />
            <span>Un buen nombre es claro, específico y atractivo</span>
          </div>
        </div>

        <!-- Tipo de Cocina - ELIMINADO -->
        <!-- Ahora se filtra por subcategorías creadas en el backend -->

        <!-- Descripción Detallada -->
        <div class="form-row">
          <va-textarea
            v-model="localFormData.description"
            label="Descripción Detallada"
            placeholder="Describe tu restaurante: ambiente, especialidades, historia, qué lo hace único..."
            :min-rows="5"
            :max-rows="10"
            counter
            maxlength="500"
            required-mark
            :rules="[
              (v) => !!v || 'La descripción es obligatoria',
              (v) => (v && v.length >= 50) || 'Mínimo 50 caracteres para una buena descripción'
            ]"
          >
            <template #prepend>
              <va-icon name="description" color="purple" />
            </template>
          </va-textarea>
          
          <div class="input-hint">
            <va-icon name="lightbulb" size="small" />
            <span>Incluye información sobre el ambiente, platillos estrella, experiencia del chef, etc.</span>
          </div>
        </div>
      </div>

      <!-- 
        ==========================================
        PRECIOS Y SERVICIOS
        ==========================================
      -->
      <div class="form-section">
        <h3 class="section-title">
          <va-icon name="payments" size="1.25rem" />
          Precios y Servicios
        </h3>

        <div class="form-grid">
          <!-- Rango de Precios -->
          <div class="form-row">
            <va-select
              v-model="localFormData.priceRange"
              label="Rango de Precios Promedio"
              placeholder="Selecciona un rango"
              :options="priceRanges"
              required-mark
              :rules="[(v) => !!v || 'Selecciona un rango de precios']"
            >
              <template #prepend>
                <va-icon name="attach_money" color="purple" />
              </template>
            </va-select>
            
            <div class="input-hint">
              <va-icon name="info" size="small" />
              <span>Precio promedio por persona</span>
            </div>
          </div>

          <!-- Delivery Disponible -->
          <div class="form-row">
            <va-switch
              v-model="localFormData.deliveryAvailable"
              label="¿Ofreces servicio de delivery?"
              color="success"
              size="large"
            >
              <template #innerLabel>
                <div class="switch-label">
                  <va-icon name="delivery_dining" />
                  <span>{{ localFormData.deliveryAvailable ? 'Sí, disponible' : 'No disponible' }}</span>
                </div>
              </template>
            </va-switch>
          </div>
        </div>

        <!-- Menú - ELIMINADO -->
        <!-- Ahora el menú se crea en un paso separado (MenuStep) con fotos individuales de cada plato -->
      </div>

      <!-- 
        ==========================================
        HORARIOS Y CAPACIDAD
        ==========================================
      -->
      <div class="form-section">
        <h3 class="section-title">
          <va-icon name="schedule" size="1.25rem" />
          Horarios y Capacidad
        </h3>

        <div class="form-grid">
          <!-- Horarios de Atención -->
          <div class="form-row">
            <va-input
              v-model="localFormData.schedule"
              label="Horarios de Atención"
              placeholder="Ej: Lun-Dom: 12:00 - 22:00"
              required-mark
              :rules="[(v) => !!v || 'Los horarios son obligatorios']"
            >
              <template #prepend>
                <va-icon name="access_time" color="purple" />
              </template>
            </va-input>
            
            <div class="input-hint">
              <va-icon name="info" size="small" />
              <span>Especifica días y horarios de apertura</span>
            </div>
          </div>

          <!-- Capacidad -->
          <div class="form-row">
            <va-input
              v-model.number="localFormData.capacity"
              label="Capacidad (Personas)"
              placeholder="50"
              type="number"
              :min="1"
              :max="1000"
            >
              <template #prepend>
                <va-icon name="people" color="purple" />
              </template>
            </va-input>
            
            <div class="input-hint">
              <va-icon name="info" size="small" />
              <span>Cantidad aproximada de comensales</span>
            </div>
          </div>
        </div>

        <!-- Estacionamiento -->
        <div class="form-row">
          <va-switch
            v-model="localFormData.parking"
            label="¿Cuentas con estacionamiento?"
            color="success"
            size="large"
          >
            <template #innerLabel>
              <div class="switch-label">
                <va-icon name="local_parking" />
                <span>{{ localFormData.parking ? 'Sí, disponible' : 'No disponible' }}</span>
              </div>
            </template>
          </va-switch>
        </div>
      </div>

      <!-- 
        ==========================================
        INFORMACIÓN DE CONTACTO
        ==========================================
      -->
      <div class="form-section">
        <h3 class="section-title">
          <va-icon name="contact_phone" size="1.25rem" />
          Información de Contacto
        </h3>

        <div class="form-grid">
          <!-- WhatsApp -->
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

          <!-- Email (Opcional) -->
          <div class="form-row">
            <va-input
              v-model="localFormData.email"
              label="Email (Opcional)"
              placeholder="contacto@restaurant.com"
              type="email"
              :rules="[
                (v) => !v || /.+@.+\..+/.test(v) || 'Email inválido'
              ]"
            >
              <template #prepend>
                <va-icon name="email" color="purple" />
              </template>
            </va-input>
          </div>
        </div>

        <!-- Sitio Web o Redes Sociales -->
        <div class="form-row">
          <va-input
            v-model="localFormData.website"
            label="Sitio Web, Facebook o Instagram (Opcional)"
            placeholder="https://tu-sitio.com o https://facebook.com/tupagina"
            :rules="[
              (v) => !v || v.startsWith('http://') || v.startsWith('https://') || 'Debe empezar con http:// o https://'
            ]"
          >
            <template #prepend>
              <va-icon name="language" color="purple" />
            </template>
          </va-input>
          
          <div class="input-hint">
            <va-icon name="info" size="small" />
            <span>Puedes agregar tu sitio web, página de Facebook o perfil de Instagram</span>
          </div>
        </div>
      </div>

      <!-- 
        ==========================================
        INFORMACIÓN ADICIONAL
        ==========================================
      -->
      <div class="form-section">
        <h3 class="section-title">
          <va-icon name="more_horiz" size="1.25rem" />
          Información Adicional (Opcional)
        </h3>

        <!-- Características Especiales -->
        <div class="form-row">
          <div class="checkbox-group">
            <p class="checkbox-label">Servicios y Características:</p>
            
            <div class="checkbox-grid">
              <va-checkbox
                v-model="localFormData.features"
                label="WiFi Gratis"
                array-value="WiFi Gratis"
              />
              <va-checkbox
                v-model="localFormData.features"
                label="Música en Vivo"
                array-value="Música en Vivo"
              />
              <va-checkbox
                v-model="localFormData.features"
                label="Terraza"
                array-value="Terraza"
              />
              <va-checkbox
                v-model="localFormData.features"
                label="Aire Acondicionado"
                array-value="Aire Acondicionado"
              />
              <va-checkbox
                v-model="localFormData.features"
                label="Apto para Niños"
                array-value="Apto para Niños"
              />
              <va-checkbox
                v-model="localFormData.features"
                label="Reservas Online"
                array-value="Reservas Online"
              />
              <va-checkbox
                v-model="localFormData.features"
                label="Opciones Vegetarianas"
                array-value="Opciones Vegetarianas"
              />
              <va-checkbox
                v-model="localFormData.features"
                label="Opciones Veganas"
                array-value="Opciones Veganas"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// ==========================================
// IMPORTS
// ==========================================
import { ref, watch } from 'vue'

// ==========================================
// PROPS & EMITS
// ==========================================
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  },
  subcategory: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

// ==========================================
// STATE
// ==========================================
const localFormData = ref({
  // Información básica
  title: props.modelValue.title || '',
  description: props.modelValue.description || '',
  
  // Precios y servicios
  priceRange: props.modelValue.priceRange || '',
  deliveryAvailable: props.modelValue.deliveryAvailable || false,
  
  // Horarios y capacidad
  schedule: props.modelValue.schedule || '',
  capacity: props.modelValue.capacity || null,
  parking: props.modelValue.parking || false,
  
  // Contacto
  whatsapp: props.modelValue.whatsapp || '',
  email: props.modelValue.email || '',
  website: props.modelValue.website || '',
  
  // Características adicionales
  features: props.modelValue.features || []
})

// ==========================================
// OPTIONS - RANGOS DE PRECIO
// ==========================================
const priceRanges = [
  { text: '💵 Económico (Bs. 10 - 30)', value: 'economico' },
  { text: '💵💵 Moderado (Bs. 30 - 60)', value: 'moderado' },
  { text: '💵💵💵 Alto (Bs. 60 - 100)', value: 'alto' },
  { text: '💵💵💵💵 Premium (Bs. 100+)', value: 'premium' }
]

// ==========================================
// WATCHERS
// ==========================================
watch(localFormData, (newValue) => {
  emit('update:modelValue', { ...props.modelValue, ...newValue })
}, { deep: true })

// ==========================================
// MÉTODOS DE VALIDACIÓN
// ==========================================
const validate = () => {
  const errors = []
  
  // Validaciones obligatorias
  if (!localFormData.value.title || localFormData.value.title.length < 5) {
    errors.push('El nombre del establecimiento debe tener al menos 5 caracteres')
  }
  
  if (!localFormData.value.description || localFormData.value.description.length < 50) {
    errors.push('La descripción debe tener al menos 50 caracteres')
  }
  
  if (!localFormData.value.priceRange) {
    errors.push('Debes seleccionar un rango de precios')
  }
  
  if (!localFormData.value.schedule) {
    errors.push('Los horarios de atención son obligatorios')
  }
  
  if (!localFormData.value.whatsapp) {
    errors.push('El número de WhatsApp es obligatorio')
  } else if (!/^[67]\d{7}$/.test(localFormData.value.whatsapp)) {
    errors.push('El número de WhatsApp debe ser válido (8 dígitos, empezar con 6 o 7)')
  }
  
  // Email (solo si existe)
  if (localFormData.value.email && !/.+@.+\..+/.test(localFormData.value.email)) {
    errors.push('El email no es válido')
  }
  
  // Website (solo si existe)
  if (localFormData.value.website && 
      !localFormData.value.website.startsWith('http://') && 
      !localFormData.value.website.startsWith('https://')) {
    errors.push('La URL debe empezar con http:// o https://')
  }
  
  if (errors.length > 0) {
    console.error('Errores de validación:', errors)
    return false
  }
  
  return true
}

// Exponer método validate() para que PublishView.vue pueda llamarlo
defineExpose({
  validate
})
</script>

<style scoped>
/* ==========================================
   CONTENEDOR PRINCIPAL
   ========================================== */
.information-step-gastronomia {
  width: 100%;
}

/* ==========================================
   HEADER
   ========================================== */
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
  background: linear-gradient(135deg, var(--color-purple) 0%, var(--color-purple-dark) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(92, 0, 153, 0.2);
}

.step-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-purple-darkest);
  margin: 0;
}

.step-subtitle {
  font-size: 1rem;
  color: #666;
  margin: 0.25rem 0 0 0;
}

/* ==========================================
   FORMULARIO
   ========================================== */
.form-content {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

/* ==========================================
   SECCIONES
   ========================================== */
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
  color: var(--color-purple-dark);
  margin: 0 0 0.5rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #F5F5F5;
}

/* ==========================================
   FILAS Y GRILLAS
   ========================================== */
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

/* ==========================================
   HINTS
   ========================================== */
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

/* ==========================================
   WHATSAPP PREFIX
   ========================================== */
.whatsapp-prefix {
  font-weight: 700;
  color: var(--color-purple);
  padding: 0.5rem;
  background: #F5F5F5;
  border-radius: 6px;
}

/* ==========================================
   SWITCH LABEL
   ========================================== */
.switch-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
}

/* ==========================================
   CHECKBOX GROUP
   ========================================== */
.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checkbox-label {
  font-weight: 600;
  color: var(--color-purple-dark);
  margin: 0;
}

.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

/* ==========================================
   RESPONSIVE - TABLET
   ========================================== */
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

  .checkbox-grid {
    grid-template-columns: 1fr;
  }
}

/* ==========================================
   RESPONSIVE - MOBILE
   ========================================== */
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