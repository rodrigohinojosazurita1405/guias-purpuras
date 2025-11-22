<!-- 
  BranchManager.vue
  Componente reutilizable para gestión de múltiples sucursales
  Similar al componente de preguntas del reclutador en JobCreate
  
  @author: Sistema de Guías Púrpuras
  @version: 1.1 - Con soporte para deshabilitar restricciones de plan
-->

<template>
  <div class="branch-manager">
    
    <!-- ========== HEADER ========== -->
    <div class="section-header">
      <h3 class="section-title">
        <va-icon name="store" color="purple" size="1.5rem" />
        Sucursales Adicionales
        <span class="optional-badge">Opcional</span>
      </h3>
      <p class="section-description">
        Agrega más ubicaciones donde tus clientes pueden encontrarte
      </p>
    </div>

    <!-- ========== PLAN BLOQUEADO (FREE) ========== -->
    <div v-if="isPlanBlocked" class="plan-blocked">
      <div class="blocked-content">
        <va-icon name="lock" size="3rem" color="#9CA3AF" />
        <h4>Sucursales bloqueadas</h4>
        <p>Mejora tu plan para agregar múltiples ubicaciones y llegar a más clientes</p>
        
        <div class="plan-benefits">
          <div class="benefit">
            <va-icon name="check_circle" color="#10B981" size="small" />
            <span>Plan Plata: Hasta 3 sucursales</span>
          </div>
          <div class="benefit">
            <va-icon name="check_circle" color="#10B981" size="small" />
            <span>Plan Oro: Hasta 10 sucursales</span>
          </div>
          <div class="benefit">
            <va-icon name="check_circle" color="#10B981" size="small" />
            <span>Plan Diamante: Sucursales ilimitadas</span>
          </div>
        </div>

        <button class="upgrade-btn" @click="$emit('upgrade-plan')">
          <va-icon name="diamond" />
          Mejorar mi plan
        </button>
      </div>
    </div>

    <!-- ========== LISTA DE SUCURSALES ========== -->
    <div v-else class="branches-container">
      
      <!-- Cards de sucursales existentes -->
      <transition-group name="branch-list" tag="div" class="branches-list">
        <div
          v-for="(branch, index) in localBranches"
          :key="branch.id"
          class="branch-card"
        >
          <!-- Header de la card -->
          <div class="branch-card-header">
            <div class="branch-number">
              <va-icon name="location_on" size="small" />
              <span>Sucursal #{{ index + 1 }}</span>
            </div>
            <button
              class="remove-btn"
              @click="removeBranch(index)"
              type="button"
              :title="`Eliminar sucursal ${index + 1}`"
            >
              <va-icon name="close" size="small" />
            </button>
          </div>

          <!-- Formulario de la sucursal -->
          <div class="branch-form">
            
            <!-- Ciudad -->
            <div class="form-group">
              <label class="form-label required">
                <va-icon name="location_city" size="small" />
                Ciudad
              </label>
              <select
                v-model="branch.city"
                class="form-select"
                required
                @change="validateBranch(index)"
              >
                <option value="">Selecciona una ciudad</option>
                <option
                  v-for="city in cities"
                  :key="city.id"
                  :value="city.id"
                >
                  {{ city.name }}
                </option>
              </select>
              <span v-if="branchErrors[index]?.city" class="error-text">
                {{ branchErrors[index].city }}
              </span>
            </div>

            <!-- Dirección -->
            <div class="form-group">
              <label class="form-label required">
                <va-icon name="place" size="small" />
                Dirección
              </label>
              <input
                v-model="branch.address"
                type="text"
                class="form-input"
                placeholder="Ej: Av. Cristo Redentor 123, entre calles..."
                required
                @blur="validateBranch(index)"
              />
              <span v-if="branchErrors[index]?.address" class="error-text">
                {{ branchErrors[index].address }}
              </span>
            </div>

            <!-- Celular -->
            <div class="form-group">
              <label class="form-label">
                <va-icon name="phone" size="small" />
                Celular de contacto
              </label>
              <input
                v-model="branch.phone"
                type="tel"
                class="form-input"
                placeholder="+591 3 1234567"
              />
              <span class="hint-text">
                Opcional - Teléfono específico de esta sucursal
              </span>
            </div>

            <!-- Horarios -->
            <div class="form-group">
              <label class="form-label">
                <va-icon name="schedule" size="small" />
                Horarios de atención
              </label>
              <input
                v-model="branch.hours"
                type="text"
                class="form-input"
                placeholder="Ej: Lun-Vie 9:00-18:00, Sáb 9:00-14:00"
              />
              <span class="hint-text">
                Opcional - Formato libre (Ej: "Lun-Dom 8:00-22:00" o "24 horas")
              </span>
            </div>

            <!-- GPS Location -->
            <div class="form-group gps-group">
              <label class="form-label">
                <va-icon name="my_location" size="small" />
                Ubicación GPS
                <span class="optional-text">(Opcional)</span>
              </label>
              <GPSLocation
                v-model="branch.gps"
                :initial-location="branch.address"
                :compact="true"
              />
            </div>

          </div>
        </div>
      </transition-group>

      <!-- Mensaje cuando no hay sucursales -->
      <div v-if="localBranches.length === 0" class="empty-state">
        <va-icon name="store_mall_directory" size="3rem" color="#D1D5DB" />
        <p>Aún no has agregado sucursales adicionales</p>
        <span class="empty-hint">
          Si tienes múltiples ubicaciones, agrégalas aquí para que tus clientes puedan encontrarte
        </span>
      </div>

      <!-- Botón agregar sucursal -->
      <div class="add-branch-section">
        <button
          class="add-branch-btn"
          :class="{ disabled: !canAddMore }"
          :disabled="!canAddMore"
          @click="addBranch"
          type="button"
        >
          <va-icon name="add" />
          Agregar otra sucursal
        </button>

        <!-- Contador y límite -->
        <div class="branch-counter">
          <span class="counter-text">
            {{ localBranches.length }} {{ disablePlanRestrictions ? (localBranches.length === 1 ? 'sucursal agregada' : 'sucursales agregadas') : `/ ${planLimitDisplay} sucursales` }}
          </span>
          <span v-if="!disablePlanRestrictions && planLimit !== Infinity" class="limit-badge">
            Plan {{ userPlan }}
          </span>
        </div>

        <!-- Mensaje de límite alcanzado -->
        <div v-if="!disablePlanRestrictions && isLimitReached" class="limit-reached">
          <va-icon name="info" size="small" color="#F59E0B" />
          <span>
            Has alcanzado el límite de tu plan actual. 
            <button class="upgrade-link" @click="$emit('upgrade-plan')">
              Mejorar plan
            </button>
          </span>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import GPSLocation from '@/components/Location/GPSLocation.vue'

// ========== PROPS ==========
const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  userPlan: {
    type: String,
    default: 'free',
    validator: (value) => ['free', 'plata', 'oro', 'diamante'].includes(value)
  },
  cities: {
    type: Array,
    required: true
  },
  // 🆕 Nuevo prop para deshabilitar restricciones de plan
  disablePlanRestrictions: {
    type: Boolean,
    default: false
  }
})

// ========== EMITS ==========
const emit = defineEmits(['update:modelValue', 'upgrade-plan'])

// ========== STATE ==========
const localBranches = ref([...props.modelValue])
const branchErrors = ref({})

// ========== PLAN LIMITS ==========
const PLAN_LIMITS = {
  free: 0,
  plata: 3,
  oro: 10,
  diamante: Infinity
}

// ========== COMPUTED ==========
const planLimit = computed(() => {
  // Si las restricciones están deshabilitadas, límite infinito
  if (props.disablePlanRestrictions) return Infinity
  return PLAN_LIMITS[props.userPlan] || 0
})

const planLimitDisplay = computed(() => {
  return planLimit.value === Infinity ? '∞' : planLimit.value
})

const isPlanBlocked = computed(() => {
  // Si las restricciones están deshabilitadas, nunca bloquear
  if (props.disablePlanRestrictions) return false
  return props.userPlan === 'free'
})

const canAddMore = computed(() => {
  return localBranches.value.length < planLimit.value
})

const isLimitReached = computed(() => {
  return localBranches.value.length >= planLimit.value && planLimit.value !== Infinity
})

// ========== METHODS ==========

/**
 * Genera un ID único para cada sucursal
 */
const generateId = () => {
  return `branch-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

/**
 * Agrega una nueva sucursal vacía
 */
const addBranch = () => {
  if (!canAddMore.value) return

  const newBranch = {
    id: generateId(),
    city: '',
    address: '',
    phone: '',
    hours: '',
    gps: { lat: null, lng: null }
  }

  localBranches.value.push(newBranch)
  emit('update:modelValue', localBranches.value)
}

/**
 * Elimina una sucursal por índice
 */
const removeBranch = (index) => {
  localBranches.value.splice(index, 1)
  
  // Limpiar errores de ese índice
  if (branchErrors.value[index]) {
    delete branchErrors.value[index]
  }
  
  emit('update:modelValue', localBranches.value)
}

/**
 * Valida una sucursal específica
 */
const validateBranch = (index) => {
  const branch = localBranches.value[index]
  const errors = {}

  if (!branch.city) {
    errors.city = 'Debes seleccionar una ciudad'
  }

  if (!branch.address || branch.address.trim() === '') {
    errors.address = 'Debes ingresar una dirección'
  }

  if (Object.keys(errors).length > 0) {
    branchErrors.value[index] = errors
  } else {
    delete branchErrors.value[index]
  }

  return Object.keys(errors).length === 0
}

/**
 * Valida todas las sucursales
 * Retorna true si todo es válido
 */
const validate = () => {
  // Si no hay sucursales, es válido (es opcional)
  if (localBranches.value.length === 0) {
    return true
  }

  // Validar cada sucursal
  let allValid = true
  branchErrors.value = {}

  localBranches.value.forEach((branch, index) => {
    const isValid = validateBranch(index)
    if (!isValid) {
      allValid = false
    }
  })

  return allValid
}

/**
 * Obtiene los errores actuales
 */
const getErrors = () => {
  return branchErrors.value
}

/**
 * Limpia todos los errores
 */
const clearErrors = () => {
  branchErrors.value = {}
}

// ========== WATCHERS ==========

// Sincronizar con prop cuando cambia externamente
watch(() => props.modelValue, (newValue) => {
  localBranches.value = [...newValue]
}, { deep: true })

// Emitir cambios cuando localBranches cambia
watch(localBranches, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })

// ========== EXPOSE ==========
defineExpose({
  validate,
  getErrors,
  clearErrors,
  addBranch,
  removeBranch
})
</script>

<style scoped>
/* ========== SECTION HEADER ========== */
.branch-manager {
  margin: 2rem 0;
}

.section-header {
  margin-bottom: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.375rem;
  font-weight: 700;
  color: #1F2937;
  margin-bottom: 0.5rem;
}

.optional-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  background: #F3F4F6;
  color: #6B7280;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.section-description {
  font-size: 0.9375rem;
  color: #6B7280;
  line-height: 1.5;
}

/* ========== PLAN BLOQUEADO ========== */
.plan-blocked {
  background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
  border: 2px dashed #D1D5DB;
  border-radius: 16px;
  padding: 3rem 2rem;
}

.blocked-content {
  text-align: center;
  max-width: 500px;
  margin: 0 auto;
}

.blocked-content h4 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #374151;
  margin: 1rem 0 0.5rem;
}

.blocked-content > p {
  font-size: 0.9375rem;
  color: #6B7280;
  margin-bottom: 2rem;
}

.plan-benefits {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
  text-align: left;
}

.benefit {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.benefit span {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #374151;
}

.upgrade-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.3);
}

.upgrade-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(92, 0, 153, 0.4);
}

/* ========== BRANCHES CONTAINER ========== */
.branches-container {
  position: relative;
}

.branches-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

/* ========== BRANCH CARD ========== */
.branch-card {
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.branch-card:hover {
  border-color: #5C0099;
  box-shadow: 0 4px 12px rgba(92, 0, 153, 0.1);
}

.branch-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #F3F4F6;
}

.branch-number {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 700;
  color: #5C0099;
}

.remove-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #FEE2E2;
  color: #DC2626;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-btn:hover {
  background: #DC2626;
  color: white;
  transform: scale(1.1);
}

/* ========== BRANCH FORM ========== */
.branch-form {
  display: grid;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.gps-group {
  margin-top: 0.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9375rem;
  font-weight: 600;
  color: #374151;
}

.form-label.required::after {
  content: '*';
  color: #EF4444;
  margin-left: 0.125rem;
}

.optional-text {
  font-size: 0.875rem;
  font-weight: 400;
  color: #9CA3AF;
}

.form-select,
.form-input {
  width: 100%;
  padding: 0.875rem 1rem;
  font-size: 0.9375rem;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  background: white;
  color: #1F2937;
  transition: all 0.3s ease;
}

.form-select:focus,
.form-input:focus {
  outline: none;
  border-color: #5C0099;
  box-shadow: 0 0 0 4px rgba(92, 0, 153, 0.1);
}

.form-select {
  cursor: pointer;
}

.hint-text {
  font-size: 0.8125rem;
  color: #9CA3AF;
  font-style: italic;
}

.error-text {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.875rem;
  color: #DC2626;
  font-weight: 500;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  background: #F9FAFB;
  border: 2px dashed #E5E7EB;
  border-radius: 16px;
  margin-bottom: 1.5rem;
}

.empty-state p {
  font-size: 1rem;
  font-weight: 600;
  color: #6B7280;
  margin: 1rem 0 0.5rem;
}

.empty-hint {
  display: block;
  font-size: 0.875rem;
  color: #9CA3AF;
  max-width: 400px;
  margin: 0 auto;
}

/* ========== ADD BRANCH SECTION ========== */
.add-branch-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.add-branch-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background: white;
  border: 2px solid #5C0099;
  border-radius: 12px;
  color: #5C0099;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-branch-btn:hover:not(.disabled) {
  background: #5C0099;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(92, 0, 153, 0.3);
}

.add-branch-btn.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  border-color: #D1D5DB;
  color: #9CA3AF;
}

.branch-counter {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.counter-text {
  font-size: 0.9375rem;
  font-weight: 600;
  color: #6B7280;
}

.limit-badge {
  display: inline-flex;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, #F3E8FF, #E9D5FF);
  color: #5C0099;
  font-size: 0.75rem;
  font-weight: 700;
  border-radius: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.limit-reached {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  background: #FEF3C7;
  border: 1px solid #FCD34D;
  border-radius: 12px;
  font-size: 0.875rem;
  color: #92400E;
}

.upgrade-link {
  background: none;
  border: none;
  color: #5C0099;
  font-weight: 600;
  text-decoration: underline;
  cursor: pointer;
  padding: 0;
  transition: all 0.2s ease;
}

.upgrade-link:hover {
  color: #9333EA;
}

/* ========== ANIMATIONS ========== */
.branch-list-enter-active,
.branch-list-leave-active {
  transition: all 0.4s ease;
}

.branch-list-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.branch-list-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.branch-list-move {
  transition: transform 0.4s ease;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .plan-blocked {
    padding: 2rem 1rem;
  }

  .branch-card {
    padding: 1rem;
  }

  .section-title {
    font-size: 1.125rem;
  }

  .branch-counter {
    flex-direction: column;
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .section-title {
    flex-wrap: wrap;
  }

  .optional-badge {
    font-size: 0.625rem;
    padding: 0.25rem 0.5rem;
  }

  .add-branch-btn {
    font-size: 0.9375rem;
    padding: 0.875rem 1.25rem;
  }
}
</style>