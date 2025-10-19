<template>
  <!--
  ═══════════════════════════════════════════════════════════
  ImageGallery.vue - Galería de imágenes del anuncio
  ═══════════════════════════════════════════════════════════
  Propósito: Mostrar imagen principal + thumbnails
  Props: images (array de URLs)
  Emits: Ninguno (manejo interno)
  Conecta con: ListingDetailView (componente padre)
  -->
  
  <!-- ========== Imagen Principal ========== -->
  <div class="gallery-section">
    <div class="main-image">
      <img :src="currentImage" alt="Imagen principal" />
      
      <!-- Badges -->
      <div class="image-badges">
        <VaBadge v-if="plan === 'top'" text="TOP" color="danger" />
        <VaBadge v-if="plan === 'featured'" text="Destacado" color="warning" />
        <VaBadge v-if="verified" text="Verificado" color="success" />
      </div>
      
      <!-- Contador -->
      <div class="image-counter">
        {{ currentIndex + 1 }} / {{ images.length }}
      </div>
    </div>
    
    <!-- ========== Thumbnails ========== -->
    <div class="thumbnail-grid">
      <button
        v-for="(image, index) in images"
        :key="index"
        :class="['thumbnail', { active: currentIndex === index }]"
        @click="currentIndex = index"
      >
        <img :src="image" :alt="`Imagen ${index + 1}`" />
      </button>
    </div>
  </div>
</template>

<script>
/**
 * ImageGallery Component
 * 
 * Props:
 * - images: Array de URLs de imágenes
 * - plan: String ('top' | 'featured' | 'free')
 * - verified: Boolean
 * 
 * State:
 * - currentIndex: índice de imagen actual
 */
export default {
  name: 'ImageGallery',
  props: {
    images: {
      type: Array,
      required: true
    },
    plan: {
      type: String,
      default: 'free'
    },
    verified: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      currentIndex: 0
    }
  },
  computed: {
    currentImage() {
      return this.images[this.currentIndex]
    }
  }
}
</script>

<style scoped>
/* ========== Galería ========== */
.gallery-section {
  margin-bottom: 2rem;
}

.main-image {
  position: relative;
  width: 100%;
  height: 500px;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 1rem;
  background: var(--color-gray-200);
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-badges {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  z-index: 10;
}

.image-counter {
  position: absolute;
  bottom: 1.5rem;
  right: 1.5rem;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  color: #ffffff;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

/* ========== Thumbnails ========== */
.thumbnail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 1rem;
}

.thumbnail {
  width: 100%;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  border: 3px solid transparent;
  cursor: pointer;
  transition: all 0.3s;
  background: var(--color-gray-200);
  padding: 0;
}

.thumbnail:hover {
  border-color: var(--color-purple-dark);
}

.thumbnail.active {
  border-color: var(--color-purple-dark);
  box-shadow: 0 4px 12px rgba(93, 0, 153, 0.3);
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .main-image {
    height: 300px;
  }
  
  .thumbnail-grid {
    grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  }
}
</style>