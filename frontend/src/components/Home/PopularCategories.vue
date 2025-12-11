<!-- frontend/src/components/Home/PopularCategories.vue -->
<template>
  <section class="categories-section">
    <div class="categories-container">
      <h2 class="section-title">Explora por categoría</h2>
      
      <!-- Loading state -->
      <div v-if="loading" class="loading-state">
        <va-progress-circle indeterminate color="purple" />
        <p>Cargando categorías...</p>
      </div>

      <!-- Slider infinito de categorías -->
      <div v-else class="slider-container">
        <div class="categories-slider-wrapper">
          <!-- Botón izquierdo superpuesto -->
          <button @click="prevSlide" class="control-btn control-left" :disabled="loading">
            <va-icon name="chevron_left" size="24px" />
          </button>

          <!-- Slider -->
          <div
            class="categories-slider"
            ref="sliderRef"
            @mouseenter="pauseAutoplay"
            @mouseleave="resumeAutoplay"
          >
            <div
              v-for="category in categories"
              :key="category.id"
              @click="handleCategoryClick(category)"
              class="category-card"
            >
              <div class="category-icon">
                <va-icon :name="category.icon" size="2rem" />
              </div>
              <h3 class="category-name">{{ category.name }}</h3>
              <p class="category-count">Ver oportunidades →</p>
            </div>
          </div>

          <!-- Botón derecho superpuesto -->
          <button @click="nextSlide" class="control-btn control-right" :disabled="loading">
            <va-icon name="chevron_right" size="24px" />
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// Mapeo de categorías a íconos
const categoryIcons = {
  'tecnologia': 'computer',
  'ventas': 'shopping_cart',
  'administracion': 'business_center',
  'marketing': 'campaign',
  'ingenieria': 'engineering',
  'educacion': 'school',
  'salud': 'local_hospital',
  'remoto': 'home',
  'finanzas': 'payments',
  'construccion': 'construction',
  'transporte': 'local_shipping',
  'turismo': 'flight',
  'gastronomia': 'restaurant',
  'default': 'work'
}

const categories = ref([])
const loading = ref(true)
const sliderRef = ref(null)
let autoplayInterval = null
let currentPosition = 0

// Obtener categorías dinámicas desde el backend
const fetchCategories = async () => {
  try {
    loading.value = true

    // Obtener categorías y trabajos en paralelo
    const [categoriesRes, jobsRes] = await Promise.all([
      axios.get('http://localhost:8000/api/jobs/categories-dynamic/'),
      axios.get('http://localhost:8000/api/jobs/')
    ])

    // Obtener todos los trabajos para contar por categoría
    const allJobs = jobsRes.data.jobs || jobsRes.data || []

    // El endpoint devuelve { success: true, categories: [...], count: N }
    if (categoriesRes.data && categoriesRes.data.categories && Array.isArray(categoriesRes.data.categories)) {
      // Mapear las categorías y tomar solo las primeras 8 más relevantes
      const allCategories = categoriesRes.data.categories
        .filter(cat => cat.value !== 'Otra categoría') // Excluir "Otra categoría"
        .map(cat => {
          // Contar cuántos empleos hay de esta categoría
          const jobCount = allJobs.filter(job =>
            job.jobCategory === cat.value || job.jobCategory === cat.text
          ).length

          // Obtener el ícono según el slug
          let icon = categoryIcons.default

          // Buscar coincidencias parciales en el slug para asignar íconos
          if (cat.slug.includes('tecnologia') || cat.slug.includes('informatica') || cat.slug.includes('software') || cat.slug.includes('programacion')) {
            icon = 'computer'
          } else if (cat.slug.includes('ventas') || cat.slug.includes('comercial')) {
            icon = 'shopping_cart'
          } else if (cat.slug.includes('administracion') || cat.slug.includes('gestion-administrativa')) {
            icon = 'business_center'
          } else if (cat.slug.includes('marketing') || cat.slug.includes('publicidad')) {
            icon = 'campaign'
          } else if (cat.slug.includes('ingenieria')) {
            icon = 'engineering'
          } else if (cat.slug.includes('educacion')) {
            icon = 'school'
          } else if (cat.slug.includes('salud') || cat.slug.includes('medicina')) {
            icon = 'local_hospital'
          } else if (cat.slug.includes('finanzas') || cat.slug.includes('banca')) {
            icon = 'payments'
          } else if (cat.slug.includes('construccion')) {
            icon = 'construction'
          } else if (cat.slug.includes('transporte') || cat.slug.includes('logistica')) {
            icon = 'local_shipping'
          } else if (cat.slug.includes('turismo') || cat.slug.includes('hosteleria')) {
            icon = 'flight'
          } else if (cat.slug.includes('gastronomia') || cat.slug.includes('alimentos')) {
            icon = 'restaurant'
          }

          return {
            id: cat.slug,
            name: cat.text,
            icon: icon,
            count: jobCount,
            slug: cat.slug
          }
        })
        // Ordenar por cantidad de empleos (mayor a menor)
        .sort((a, b) => b.count - a.count)

      // Mostrar TODAS las categorías en el slider
      categories.value = allCategories
    }
  } catch (error) {
    console.error('Error fetching categories:', error)
    // Fallback a categorías por defecto si falla
    categories.value = [
      { id: 'tecnologia', name: 'Tecnología e Informática', icon: 'computer', count: 0, slug: 'tecnologia-e-informatica' },
      { id: 'ventas', name: 'Comercial y Ventas', icon: 'shopping_cart', count: 0, slug: 'comercial-y-ventas' },
      { id: 'administracion', name: 'Administración y Gestión', icon: 'business_center', count: 0, slug: 'administracion-y-gestion' },
      { id: 'marketing', name: 'Marketing y Publicidad', icon: 'campaign', count: 0, slug: 'marketing-y-publicidad' },
      { id: 'ingenieria', name: 'Ingeniería de Sistemas', icon: 'engineering', count: 0, slug: 'ingenieria-de-sistemas' },
      { id: 'educacion', name: 'Educación e Institutos', icon: 'school', count: 0, slug: 'educacion-e-institutos' },
      { id: 'salud', name: 'Salud y Medicina', icon: 'local_hospital', count: 0, slug: 'salud-y-medicina' },
      { id: 'finanzas', name: 'Finanzas y Contabilidad', icon: 'payments', count: 0, slug: 'finanzas-y-contabilidad' }
    ]
  } finally {
    loading.value = false
  }
}

// Slider controls
const nextSlide = () => {
  if (!sliderRef.value) return
  const cardWidth = 180 // width + gap
  currentPosition -= cardWidth
  sliderRef.value.style.transform = `translateX(${currentPosition}px)`
  sliderRef.value.style.transition = 'transform 0.5s ease'

  // Si llegamos al final, reiniciar (efecto infinito)
  checkInfiniteLoop()
}

const prevSlide = () => {
  if (!sliderRef.value) return
  const cardWidth = 180
  currentPosition += cardWidth
  sliderRef.value.style.transform = `translateX(${currentPosition}px)`
  sliderRef.value.style.transition = 'transform 0.5s ease'

  checkInfiniteLoop()
}

const checkInfiniteLoop = () => {
  if (!sliderRef.value) return

  const sliderWidth = sliderRef.value.scrollWidth / 2

  // Si nos pasamos a la derecha, volver al inicio
  if (currentPosition > 0) {
    setTimeout(() => {
      sliderRef.value.style.transition = 'none'
      currentPosition = -sliderWidth
      sliderRef.value.style.transform = `translateX(${currentPosition}px)`
    }, 500)
  }

  // Si nos pasamos a la izquierda, volver al final
  if (Math.abs(currentPosition) > sliderWidth) {
    setTimeout(() => {
      sliderRef.value.style.transition = 'none'
      currentPosition = 0
      sliderRef.value.style.transform = `translateX(${currentPosition}px)`
    }, 500)
  }
}

// Autoplay
const startAutoplay = () => {
  autoplayInterval = setInterval(() => {
    nextSlide()
  }, 3000) // Cambiar cada 3 segundos
}

const pauseAutoplay = () => {
  if (autoplayInterval) {
    clearInterval(autoplayInterval)
  }
}

const resumeAutoplay = () => {
  startAutoplay()
}

const handleCategoryClick = (category) => {
  router.push({
    path: '/guias/trabajos',
    query: { category: category.slug }
  })
}

onMounted(async () => {
  await fetchCategories()
  // Iniciar autoplay después de cargar las categorías
  if (categories.value.length > 0) {
    startAutoplay()
  }
})

onUnmounted(() => {
  pauseAutoplay()
})
</script>

<style scoped>
.categories-section {
  width: 100%;
  padding: 3rem 2rem;
  background: white;
}

.categories-container {
  max-width: 1400px;
  margin: 0 auto;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1F2937;
  margin: 0 0 2rem 0;
  text-align: center;
}

/* Container del slider */
.slider-container {
  position: relative;
}

/* Slider wrapper con botones superpuestos */
.categories-slider-wrapper {
  overflow: hidden;
  position: relative;
}

.control-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  border: 2px solid #E5E7EB;
  border-radius: 50%;
  color: #6B7280;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.control-btn:hover:not(:disabled) {
  border-color: var(--color-purple);
  background: var(--color-purple);
  color: white;
  transform: translateY(-50%) scale(1.15);
  box-shadow: 0 6px 20px rgba(92, 0, 153, 0.3);
}

.control-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.control-left {
  left: 0.5rem;
}

.control-right {
  right: 0.5rem;
}

.categories-slider {
  display: flex;
  gap: 1.5rem;
  transition: transform 0.5s ease;
}

.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem 1rem;
  min-width: 160px;
  flex-shrink: 0;
  background: #F9FAFB;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.category-card:hover {
  background: white;
  border-color: var(--color-purple);
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(92, 0, 153, 0.12);
}

.category-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 12px;
  margin-bottom: 0.75rem;
  color: var(--color-purple);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
}

.category-card:hover .category-icon {
  background: var(--color-purple);
  color: white;
}

.category-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1F2937;
  margin: 0 0 0.25rem 0;
}

.category-count {
  font-size: 0.875rem;
  color: #6B7280;
  margin: 0;
}

/* Loading state */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  gap: 1rem;
}

.loading-state p {
  color: #6B7280;
  font-size: 0.9375rem;
  margin: 0;
}

/* ==========================================
   RESPONSIVE
   ========================================== */
@media (max-width: 768px) {
  .categories-section {
    padding: 2.5rem 1rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .control-btn {
    width: 40px;
    height: 40px;
  }

  .control-left {
    left: 0.5rem;
  }

  .control-right {
    right: 0.5rem;
  }

  .category-card {
    min-width: 140px;
    padding: 1.25rem 0.75rem;
  }

  .category-icon {
    width: 48px;
    height: 48px;
  }

  .category-name {
    font-size: 0.875rem;
  }

  .category-count {
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  .categories-section {
    padding: 2rem 0.75rem;
  }

  .section-title {
    font-size: 1.375rem;
  }

  .control-btn {
    width: 36px;
    height: 36px;
  }

  .control-left {
    left: 0.25rem;
  }

  .control-right {
    right: 0.25rem;
  }

  .category-card {
    min-width: 120px;
    padding: 1rem 0.5rem;
  }

  .categories-slider {
    gap: 1rem;
  }
}
</style>
