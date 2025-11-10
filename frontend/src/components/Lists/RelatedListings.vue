<template>
  <!--
  ═══════════════════════════════════════════════════════════
  RelatedListings.vue - Anuncios relacionados
  ═══════════════════════════════════════════════════════════
  Propósito: Mostrar 3 anuncios similares al final
  Props: relatedListings (array de anuncios)
  Emits: listing-click (cuando se hace clic en un anuncio)
  Conecta con: ListingDetailView (componente padre)
  TODO: Obtener desde Django /api/listings/related/:id/
  -->
  
  <div class="related-section">
    <h2>Anuncios Relacionados</h2>
    
    <!-- ========== Grid de Anuncios Relacionados ========== -->
    <div class="related-grid">
      <div
        v-for="listing in relatedListings"
        :key="listing.id"
        class="related-card"
        @click="$emit('listing-click', listing)"
      >
        <!-- Imagen -->
        <div class="related-image">
          <img :src="listing.image" :alt="listing.title" />
        </div>
        
        <!-- Contenido -->
        <div class="related-content">
          <h4>{{ listing.title }}</h4>
          <p>{{ listing.location }}</p>
          <div class="related-footer">
            <span v-if="listing.price">Bs. {{ listing.price.toLocaleString() }}</span>
            <span v-else>Consultar</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * RelatedListings Component
 * 
 * Props:
 * - relatedListings: Array de objetos (mínimo 3)
 * 
 * Emits:
 * - listing-click: (listing) cuando se hace clic
 * 
 * TODO:
 * - Conectar con Django API /api/listings/related/:id/
 */
export default {
  name: 'RelatedListings',
  props: {
    relatedListings: {
      type: Array,
      required: true
    }
  },
  emits: ['listing-click']
}
</script>

<style scoped>
/* ========== Sección ========== */
.related-section {
  margin-bottom: 2rem;
}

.related-section h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: 1.5rem;
}

/* ========== Grid ========== */
.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.related-card {
  background: #ffffff;
  border: 2px solid var(--color-gray-100);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.related-card:hover {
  border-color: var(--color-purple-dark);
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

/* ========== Imagen ========== */
.related-image {
  width: 100%;
  height: 150px;
  overflow: hidden;
  background: var(--color-gray-200);
}

.related-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.related-card:hover .related-image img {
  transform: scale(1.1);
}

/* ========== Contenido ========== */
.related-content {
  padding: 1rem;
}

.related-content h4 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin: 0 0 0.5rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.related-content p {
  color: var(--color-gray-500);
  font-size: 0.85rem;
  margin: 0 0 0.75rem 0;
}

.related-footer {
  padding-top: 0.75rem;
  border-top: 1px solid var(--color-gray-100);
  color: var(--color-purple-dark);
  font-weight: 700;
}

/* ========== Responsive ========== */
@media (max-width: 768px) {
  .related-grid {
    grid-template-columns: 1fr;
  }
}
</style>