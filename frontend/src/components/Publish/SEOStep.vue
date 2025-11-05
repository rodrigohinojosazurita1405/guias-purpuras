<!-- frontend/src/components/Publish/SEOStep.vue -->
<!-- PASO OPCIONAL: OPTIMIZACIÓN SEO - REUTILIZABLE PARA TODAS LAS GUÍAS -->
<template>
  <div class="seo-step">
    
    <!-- Header -->
    <div class="step-header">
      <div class="header-content">
        <va-icon name="search" size="3rem" color="#5C0099" />
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
        <va-icon name="trending_up" size="2rem" color="#2196F3" />
        <h3 class="motivation-title">¿Por qué optimizar tu SEO?</h3>
      </div>
      
      <ul class="benefits-list">
        <li class="benefit-item">
          <div class="benefit-icon">
            <va-icon name="public" size="1.5rem" color="#4CAF50" />
          </div>
          <div class="benefit-content">
            <strong>Aparece en Google</strong>
            <p>Tu publicación aparecerá en búsquedas de Google cuando alguien busque tus servicios</p>
          </div>
        </li>
        
        <li class="benefit-item">
          <div class="benefit-icon">
            <va-icon name="groups" size="1.5rem" color="#4CAF50" />
          </div>
          <div class="benefit-content">
            <strong>Más clientes potenciales</strong>
            <p>Llega a personas que ni siquiera conocían Guías Púrpuras</p>
          </div>
        </li>
        
        <li class="benefit-item">
          <div class="benefit-icon">
            <va-icon name="workspace_premium" size="1.5rem" color="#4CAF50" />
          </div>
          <div class="benefit-content">
            <strong>Mejor posicionamiento</strong>
            <p>Destaca frente a tu competencia con palabras clave optimizadas</p>
          </div>
        </li>
        
        <li class="benefit-item">
          <div class="benefit-icon">
            <va-icon name="bar_chart" size="1.5rem" color="#4CAF50" />
          </div>
          <div class="benefit-content">
            <strong>Resultados medibles</strong>
            <p>Los anuncios con SEO optimizado reciben 5x más visitas</p>
          </div>
        </li>
      </ul>
    </div>

    <!-- Componente SEO -->
    <div class="seo-container">
      <SEOFields
        :model-value="localSeoData"
        @update:model-value="handleSEOUpdate"
        :entity-type="entityType"
        :base-url="baseUrl"
        :available-categories="availableCategories"
      />
    </div>

    <!-- Skip Option -->
    <div class="skip-notice">
      <va-icon name="info" size="small" color="#666" />
      <span>Puedes omitir este paso y optimizar tu SEO después si lo prefieres</span>
    </div>

  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import SEOFields from '@/components/SEO/SEOFields.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      slug: '',
      mainKeyword: '',
      tags: [],
      metaDescription: '',
      locationKeywords: '',
      categories: []
    })
  },
  entityType: {
    type: String,
    required: true // 'profesional', 'restaurante', 'negocio', 'trabajo'
  },
  baseUrl: {
    type: String,
    required: true // 'guiaspurpuras.com/profesionales'
  },
  categoriesEndpoint: {
    type: String,
    default: null // '/api/categories/profesionales/'
  }
})

const emit = defineEmits(['update:modelValue'])

const localSeoData = ref({ ...props.modelValue })

// Categorías SEO - Se cargarán desde Django si hay endpoint
const availableCategories = ref([
  { id: 1, name: 'General', selected: false },
  { id: 2, name: 'Servicios', selected: false },
  { id: 3, name: 'Consultoría', selected: false },
  { id: 4, name: 'Técnico', selected: false },
  { id: 5, name: 'Profesional', selected: false },
  { id: 6, name: 'Comercial', selected: false },
  { id: 7, name: 'Especializado', selected: false },
  { id: 8, name: 'Premium', selected: false }
])

const handleSEOUpdate = (seoData) => {
  localSeoData.value = { ...seoData }
}

// Watch para emitir cambios
watch(
  localSeoData,
  (newVal) => {
    emit('update:modelValue', newVal)
  },
  { deep: true }
)

// Cargar categorías desde Django si hay endpoint
onMounted(async () => {
  if (props.categoriesEndpoint) {
    try {
      const response = await fetch(props.categoriesEndpoint)
      const categories = await response.json()
      availableCategories.value = categories.map(cat => ({
        id: cat.id,
        name: cat.name,
        selected: false
      }))
    } catch (error) {
      console.error('Error al cargar categorías SEO:', error)
      // Usar categorías por defecto si falla
    }
  }
})

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
  background: linear-gradient(135deg, #E3F2FD 0%, #FFFFFF 100%);
  border: 2px solid #90CAF9;
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

/* ========== SEO Container ========== */
.seo-container {
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

  .benefit-item {
    gap: 0.75rem;
  }

  .benefit-icon {
    width: 40px;
    height: 40px;
  }
}
</style>