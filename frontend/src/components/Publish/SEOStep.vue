<!-- frontend/src/components/Publish/SEOStep.vue -->
<!-- PASO OPCIONAL: OPTIMIZACIÓN SEO - REUTILIZABLE PARA TODAS LAS GUÍAS -->
<template>
  <div class="seo-step">
    
    <!-- Header -->
    <div class="step-header">
      <div class="header-content">
        <va-icon name="search" size="3rem" color="#7C3AED" />
        <div class="header-text">
          <h2 class="step-title">Optimización SEO</h2>
          <p class="step-description">
            Optimiza tu publicación para aparecer en más búsquedas de Google
          </p>
        </div>
      </div>
      <VaBadge text="Opcional" color="info" size="large" />
    </div>

    <!-- Mensaje Motivador -->
    <div class="motivation-box">
      <div class="motivation-header">
        <va-icon name="trending_up" size="2rem" color="#7C3AED" />
        <h3 class="motivation-title">¿Por qué optimizar tu SEO?</h3>
      </div>
      
      <div class="benefits-grid">
        <div class="benefit-card">
          <div class="benefit-icon green">
            <va-icon name="public" size="1.5rem" />
          </div>
          <div class="benefit-content">
            <strong>Aparece en Google</strong>
            <p>Tu publicación aparecerá en búsquedas de Google cuando alguien busque tus servicios</p>
          </div>
        </div>
        
        <div class="benefit-card">
          <div class="benefit-icon purple">
            <va-icon name="groups" size="1.5rem" />
          </div>
          <div class="benefit-content">
            <strong>Más clientes potenciales</strong>
            <p>Llega a personas que ni siquiera conocían Guías Púrpuras</p>
          </div>
        </div>
        
        <div class="benefit-card">
          <div class="benefit-icon blue">
            <va-icon name="workspace_premium" size="1.5rem" />
          </div>
          <div class="benefit-content">
            <strong>Mejor posicionamiento</strong>
            <p>Destaca frente a tu competencia con palabras clave optimizadas</p>
          </div>
        </div>
        
        <div class="benefit-card">
          <div class="benefit-icon success">
            <va-icon name="bar_chart" size="1.5rem" />
          </div>
          <div class="benefit-content">
            <strong>Resultados medibles</strong>
            <p>Los anuncios con SEO optimizado reciben 5x más visitas</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Formulario SEO Simplificado -->
    <div class="seo-container">
      <div class="form-group">
        <label>Slug (URL amigable)</label>
        <input
          v-model="localSeoData.slug"
          type="text"
          placeholder="ej: titulo-del-empleo"
          class="form-input"
        />
      </div>

      <div class="form-group">
        <label>Título SEO (Para Google)</label>
        <input
          v-model="localSeoData.title"
          type="text"
          placeholder="Máximo 60 caracteres"
          maxlength="60"
          class="form-input"
        />
        <small>{{ localSeoData.title.length }}/60</small>
      </div>

      <div class="form-group">
        <label>Descripción Meta</label>
        <textarea
          v-model="localSeoData.metaDescription"
          placeholder="Máximo 160 caracteres"
          maxlength="160"
          rows="3"
          class="form-input"
        ></textarea>
        <small>{{ localSeoData.metaDescription.length }}/160</small>
      </div>

      <div class="form-group">
        <label>Palabras clave (separadas por comas)</label>
        <input
          v-model="localSeoData.tags"
          type="text"
          placeholder="empleo, trabajo, bolivian jobs"
          class="form-input"
        />
      </div>
    </div>

    <!-- Skip Option -->
    <div class="skip-notice">
      <va-icon name="info" size="small" color="#7C3AED" />
      <span>Puedes omitir este paso y optimizar tu SEO después desde el dashboard</span>
    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      slug: '',
      title: '',
      mainKeyword: '',
      tags: [],
      metaDescription: '',
      locationKeywords: ''
    })
  },
  businessTitle: {
    type: String,
    default: ''
  },
  businessDescription: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'validation-change'])

const localSeoData = ref({ ...props.modelValue })
const isValid = ref(false)

const handleSEOUpdate = (seoData) => {
  localSeoData.value = { ...seoData }
}

const handleValidationChange = (valid) => {
  isValid.value = valid
  emit('validation-change', valid)
}

// Watch para emitir cambios
watch(
  localSeoData,
  (newVal) => {
    emit('update:modelValue', newVal)
  },
  { deep: true }
)

// Método de validación (siempre pasa porque es opcional)
const validate = () => {
  return true // SEO es opcional
}

// Exponer validate para uso externo
defineExpose({
  validate
})
</script>

<style scoped>
/* ========== Container ========== */
.seo-step {
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
  background: linear-gradient(135deg, #F3F4F6 0%, #FFFFFF 100%);
  border: 2px solid #E5E7EB;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
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

.benefit-icon.purple {
  background: #E9D5FF;
  color: #7C3AED;
}

.benefit-icon.blue {
  background: #DBEAFE;
  color: #2563EB;
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

/* ========== SEO Container ========== */
.seo-container {
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
  .seo-step {
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