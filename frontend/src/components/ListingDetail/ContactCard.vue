<template>
  <!--
  ═══════════════════════════════════════════════════════════
  ContactCard.vue - Card de contacto lateral
  ═══════════════════════════════════════════════════════════
  Propósito: Sidebar con info del vendedor y botones de contacto
  Props: listing (objeto con datos del anuncio)
  Emits: contact (cuando se hace clic en contactar)
  Conecta con: ListingDetailView (componente padre)
  -->
  
  <div class="contact-card sticky-card">
    <!-- ========== Precio (si existe) ========== -->
    <div v-if="listing.price" class="price-section">
      <div class="price-label">Precio</div>
      <div class="price-amount">Bs. {{ listing.price.toLocaleString() }}</div>
      <div v-if="listing.negotiable" class="price-note">Negociable</div>
    </div>
    
    <!-- ========== Info del Vendedor ========== -->
    <div class="seller-info">
      <div class="seller-avatar">
        <div class="avatar-placeholder">
          {{ listing.sellerName.charAt(0) }}
        </div>
        <div v-if="listing.verified" class="verified-badge-small">
          <VaIcon name="verified" size="small" color="#ffffff" />
        </div>
      </div>
      <div class="seller-details">
        <h3>{{ listing.sellerName }}</h3>
        <p>Miembro desde {{ listing.memberSince }}</p>
      </div>
    </div>
    
    <!-- ========== Botones de Contacto ========== -->
    <div class="contact-actions">
      <VaButton
        block
        size="large"
        color="var(--color-purple-dark)"
        @click="$emit('contact', 'phone')"
      >
        <VaIcon name="phone" />
        Ver Teléfono
      </VaButton>
      
      <VaButton
        block
        size="large"
        preset="secondary"
        @click="$emit('contact', 'whatsapp')"
      >
        <VaIcon name="chat" />
        WhatsApp
      </VaButton>
      
      <VaButton
        block
        size="large"
        preset="secondary"
        @click="$emit('contact', 'email')"
      >
        <VaIcon name="email" />
        Email
      </VaButton>
    </div>
    
    <!-- ========== Consejos de Seguridad ========== -->
    <div class="safety-tips">
      <div class="tips-header">
        <VaIcon name="security" color="var(--color-yellow-primary)" />
        <h4>Consejos de Seguridad</h4>
      </div>
      <ul>
        <li>Reúnete en lugares públicos</li>
        <li>Verifica antes de pagar</li>
        <li>No pagues por adelantado</li>
        <li>Desconfía de precios muy bajos</li>
      </ul>
    </div>
  </div>
</template>

<script>
/**
 * ContactCard Component
 * 
 * Props:
 * - listing: Object con datos del anuncio
 * 
 * Emits:
 * - contact: (type) donde type = 'phone' | 'whatsapp' | 'email'
 */
export default {
  name: 'ContactCard',
  props: {
    listing: {
      type: Object,
      required: true
    }
  },
  emits: ['contact']
}
</script>

<style scoped>
/* ========== Card Principal ========== */
.contact-card {
  background: #ffffff;
  border: 2px solid var(--color-gray-200);
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.sticky-card {
  position: sticky;
  top: 100px;
}

/* ========== Precio ========== */
.price-section {
  text-align: center;
  padding-bottom: 1.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid var(--color-gray-200);
}

.price-label {
  color: var(--color-gray-500);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.price-amount {
  font-size: 2.5rem;
  font-weight: 800;
  color: var(--color-purple-dark);
  margin-bottom: 0.5rem;
}

.price-note {
  color: var(--color-success);
  font-size: 0.9rem;
  font-weight: 600;
}

/* ========== Info Vendedor ========== */
.seller-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--color-gray-200);
}

.seller-avatar {
  position: relative;
  width: 60px;
  height: 60px;
  flex-shrink: 0;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: var(--color-purple-dark);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
}

.verified-badge-small {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 20px;
  height: 20px;
  background: var(--color-success);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #ffffff;
}

.seller-details h3 {
  margin: 0 0 0.25rem 0;
  color: var(--color-gray-900);
  font-size: 1.1rem;
}

.seller-details p {
  margin: 0;
  color: var(--color-gray-500);
  font-size: 0.85rem;
}

/* ========== Botones ========== */
.contact-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

/* ========== Consejos ========== */
.safety-tips {
  background: #FEF3C7;
  padding: 1.5rem;
  border-radius: 12px;
}

.tips-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.tips-header h4 {
  margin: 0;
  color: #92400E;
  font-size: 1rem;
}

.safety-tips ul {
  margin: 0;
  padding-left: 1.5rem;
  color: #92400E;
  font-size: 0.9rem;
}

.safety-tips li {
  margin-bottom: 0.5rem;
}
</style>