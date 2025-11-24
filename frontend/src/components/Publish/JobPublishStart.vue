<!-- frontend/src/components/Publish/JobPublishStart.vue -->
<!-- PANTALLA INICIAL INTUITIVA PARA PUBLICAR EMPLEO -->

<template>
  <div class="job-publish-start">
    <!-- Header -->
    <div class="start-header">
      <div class="header-icon">
        <va-icon name="work" size="3rem" color="purple" />
      </div>
      <h1 class="start-title">Publica tu Oferta de Trabajo</h1>
      <p class="start-subtitle">
        En solo 2 pasos rápidos, llegará a miles de candidatos en Bolivia
      </p>
    </div>

    <!-- PASO 1: Seleccionar Tipo de Empleo -->
    <div class="selection-step">
      <div class="step-indicator">
        <div class="step-badge">1</div>
        <h2 class="step-name">¿Qué tipo de empleo publicas?</h2>
      </div>

      <!-- Grid de tipos de empleo -->
      <div class="job-types-grid">
        <div
          v-for="jobType in jobTypes"
          :key="jobType.id"
          class="job-type-card"
          :class="{ selected: formData.subcategory === jobType.id }"
          @click="selectJobType(jobType.id)"
        >
          <div class="type-icon">
            <va-icon :name="jobType.icon" size="2rem" />
          </div>
          <h3 class="type-title">{{ jobType.name }}</h3>
          <p class="type-description">{{ jobType.description }}</p>
          <div v-if="formData.subcategory === jobType.id" class="check-mark">
            <va-icon name="check_circle" size="1.5rem" color="success" />
          </div>
        </div>
      </div>

      <span v-if="errors.subcategory" class="error-message">
        <va-icon name="error" size="small" />
        {{ errors.subcategory }}
      </span>
    </div>

    <!-- PASO 2: Seleccionar Ubicación -->
    <div class="selection-step">
      <div class="step-indicator">
        <div class="step-badge">2</div>
        <h2 class="step-name">¿Dónde será el empleo?</h2>
      </div>

      <!-- Selector de Ciudad -->
      <div class="city-selector-section">
        <div class="city-selector">
          <va-icon name="location_city" class="selector-icon" />
          <select
            v-model="formData.city"
            class="city-select"
            required
          >
            <option value="">Selecciona la ciudad</option>
            <option
              v-for="city in cities"
              :key="city.id"
              :value="city.id"
            >
              {{ city.name }}
            </option>
          </select>
          <va-icon name="expand_more" class="dropdown-icon" />
        </div>

        <!-- Preview de la selección -->
        <div v-if="formData.city" class="selection-preview">
          <div class="preview-item">
            <va-icon name="check_circle" color="success" />
            <span>{{ selectedCityName }}</span>
          </div>
        </div>

        <span v-if="errors.city" class="error-message">
          <va-icon name="error" size="small" />
          {{ errors.city }}
        </span>
      </div>
    </div>

    <!-- Botones de Acción -->
    <div class="action-buttons">
      <button
        class="btn btn-secondary"
        @click="$emit('cancel')"
      >
        <va-icon name="arrow_back" size="small" />
        Cancelar
      </button>
      <button
        class="btn btn-primary"
        :disabled="!isFormValid"
        @click="proceedToWizard"
      >
        Continuar al Formulario
        <va-icon name="arrow_forward" size="small" />
      </button>
    </div>

    <!-- Info de ayuda -->
    <div class="help-info">
      <va-icon name="info" size="small" />
      <p>Después completarás más detalles del empleo en el siguiente paso</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['update:formData', 'proceed-to-wizard', 'cancel'])

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      subcategory: '',
      city: ''
    })
  }
})

// Reactive form data
const formData = ref({
  subcategory: props.modelValue.subcategory || '',
  city: props.modelValue.city || ''
})

const errors = ref({
  subcategory: '',
  city: ''
})

// ========== DATA ==========
const jobTypes = [
  {
    id: 'Tiempo Completo',
    name: 'Tiempo Completo',
    icon: 'work_history',
    description: 'Posición laboral de jornada completa'
  },
  {
    id: 'Remoto',
    name: 'Empleo Remoto',
    icon: 'laptop',
    description: 'Trabaja desde cualquier lugar'
  },
  {
    id: 'Freelance',
    name: 'Freelance/Proyecto',
    icon: 'person_check',
    description: 'Proyecto por encargo o duración fija'
  },
  {
    id: 'Pasantías',
    name: 'Pasantías/Prácticas',
    icon: 'school',
    description: 'Programas de formación y experiencia'
  }
]

const cities = [
  { id: 'La Paz', name: 'La Paz' },
  { id: 'Cochabamba', name: 'Cochabamba' },
  { id: 'Santa Cruz', name: 'Santa Cruz' },
  { id: 'Oruro', name: 'Oruro' },
  { id: 'Potosí', name: 'Potosí' },
  { id: 'Tarija', name: 'Tarija' },
  { id: 'Chuquisaca', name: 'Chuquisaca' },
  { id: 'Beni', name: 'Beni' },
  { id: 'Pando', name: 'Pando' },
  { id: 'Remoto', name: 'Remoto (En línea)' }
]

// ========== COMPUTED ==========
const selectedCityName = computed(() => {
  const city = cities.find(c => c.id === formData.value.city)
  return city ? city.name : ''
})

const isFormValid = computed(() => {
  return formData.value.subcategory && formData.value.city
})

// ========== METHODS ==========
const selectJobType = (typeId) => {
  formData.value.subcategory = typeId
  errors.value.subcategory = ''
}

const proceedToWizard = () => {
  // Validar
  if (!formData.value.subcategory) {
    errors.value.subcategory = 'Debes seleccionar un tipo de empleo'
    return
  }
  if (!formData.value.city) {
    errors.value.city = 'Debes seleccionar una ciudad'
    return
  }

  // Emitir datos y proceder
  emit('update:formData', formData.value)
  emit('proceed-to-wizard')
}
</script>

<style scoped>
/* ========== CONTENEDOR PRINCIPAL ========== */
.job-publish-start {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

/* ========== HEADER ========== */
.start-header {
  text-align: center;
  margin-bottom: 4rem;
  animation: fadeInDown 0.6s ease;
}

.header-icon {
  margin-bottom: 1.5rem;
}

.start-title {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #5C0099, #9333EA);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.75rem;
}

.start-subtitle {
  font-size: 1.2rem;
  color: #6B7280;
  line-height: 1.6;
}

/* ========== STEP SECTION ========== */
.selection-step {
  margin-bottom: 4rem;
  animation: fadeInUp 0.6s ease backwards;
}

.selection-step:nth-child(2) {
  animation-delay: 0.1s;
}

.selection-step:nth-child(3) {
  animation-delay: 0.2s;
}

/* ========== STEP INDICATOR ========== */
.step-indicator {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.step-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #5C0099, #9333EA);
  color: white;
  font-weight: 800;
  font-size: 1.5rem;
  flex-shrink: 0;
  box-shadow: 0 4px 15px rgba(92, 0, 153, 0.3);
}

.step-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1F2937;
}

/* ========== JOB TYPES GRID ========== */
.job-types-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.job-type-card {
  position: relative;
  padding: 2rem;
  border: 2px solid #E5E7EB;
  border-radius: 16px;
  background: white;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: center;
  overflow: hidden;
}

.job-type-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(92, 0, 153, 0.05), rgba(156, 17, 249, 0.05));
  opacity: 0;
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.job-type-card:hover {
  border-color: #9333EA;
  box-shadow: 0 12px 24px rgba(92, 0, 153, 0.15);
  transform: translateY(-4px);
}

.job-type-card:hover::before {
  opacity: 1;
}

.job-type-card.selected {
  border-color: #9333EA;
  background: linear-gradient(135deg, rgba(92, 0, 153, 0.05), rgba(156, 17, 249, 0.05));
  box-shadow: 0 12px 24px rgba(92, 0, 153, 0.2);
}

.type-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
  color: #9333EA;
}

.type-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1F2937;
  margin-bottom: 0.5rem;
}

.type-description {
  font-size: 0.9rem;
  color: #6B7280;
  line-height: 1.5;
}

.check-mark {
  position: absolute;
  top: 1rem;
  right: 1rem;
  animation: popIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes popIn {
  0% {
    transform: scale(0);
  }
  100% {
    transform: scale(1);
  }
}

/* ========== CITY SELECTOR SECTION ========== */
.city-selector-section {
  background: #F9FAFB;
  padding: 2rem;
  border-radius: 16px;
  margin-bottom: 1.5rem;
}

.city-selector {
  position: relative;
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
}

.city-selector:hover {
  border-color: #9333EA;
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.1);
}

.city-selector:focus-within {
  border-color: #9333EA;
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.15);
}

.selector-icon {
  color: #9333EA;
  flex-shrink: 0;
}

.city-select {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1rem;
  font-family: inherit;
  color: #1F2937;
  background: transparent;
  cursor: pointer;
}

.city-select option {
  color: #1F2937;
}

.dropdown-icon {
  color: #6B7280;
  pointer-events: none;
  flex-shrink: 0;
}

/* ========== SELECTION PREVIEW ========== */
.selection-preview {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(34, 197, 94, 0.1);
  border-radius: 10px;
  border-left: 4px solid #22C55E;
}

.preview-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #166534;
  font-weight: 600;
}

/* ========== ERROR MESSAGE ========== */
.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #DC2626;
  font-size: 0.9rem;
  margin-top: 1rem;
  animation: slideInUp 0.3s ease;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== ACTION BUTTONS ========== */
.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 3rem 0 2rem;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.2rem 2.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, #5C0099, #9333EA);
  color: white;
  box-shadow: 0 4px 15px rgba(92, 0, 153, 0.3);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(92, 0, 153, 0.4);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-secondary {
  background: white;
  color: #9333EA;
  border: 2px solid #9333EA;
}

.btn-secondary:hover:not(:disabled) {
  background: #F3E8FF;
  transform: translateY(-2px);
}

/* ========== HELP INFO ========== */
.help-info {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1.5rem;
  background: #EEE5FF;
  border-radius: 12px;
  border-left: 4px solid #9333EA;
  color: #5C0099;
  font-size: 0.95rem;
  text-align: center;
  justify-content: center;
}

.help-info p {
  margin: 0;
}

/* ========== ANIMATIONS ========== */
@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .job-publish-start {
    padding: 2rem 1rem;
  }

  .start-title {
    font-size: 2rem;
  }

  .start-subtitle {
    font-size: 1rem;
  }

  .step-indicator {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .step-name {
    font-size: 1.3rem;
  }

  .job-types-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .help-info {
    flex-direction: column;
  }
}
</style>
