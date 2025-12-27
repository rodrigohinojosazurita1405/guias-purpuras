<!--
  ═══════════════════════════════════════════════════════════
  JobListCompact.vue - Card Compacto para Lista Lateral
  ═══════════════════════════════════════════════════════════

  Diseño inspirado en OCC - Vista compacta para lista izquierda
  Muestra información esencial del trabajo en formato condensado
-->
<template>
  <div
    class="job-list-compact"
    :class="{ 'selected': isSelected }"
    @click="$emit('select', listing)"
  >
    <!-- Borde izquierdo indicador (cuando está seleccionado) -->
    <div class="selection-indicator"></div>

    <!-- Logo de Empresa GRANDE (lado izquierdo) -->
    <!-- NO mostrar logo si la empresa es anónima -->
    <div v-if="listing.companyLogo && !listing.companyAnonymous" class="company-logo-large">
      <img :src="listing.companyLogo" :alt="listing.companyName" />
    </div>
    <div v-else class="company-logo-placeholder">
      <va-icon name="business" size="large" />
    </div>

    <!-- Contenido Principal -->
    <div class="job-content">
      <!-- Header: Fecha + Badges -->
      <div class="job-header">
        <div class="date-info">
          <span class="publish-date">{{ publishDate }}</span>
          <span v-if="daysRemaining !== null" class="expiry-date" :class="expiryClass">
            <va-icon name="schedule" size="12px" />
            {{ expiryText }}
          </span>
        </div>
        <div class="badges">
          <span v-if="daysRemaining < 0" class="badge closed">CERRADO</span>
          <span v-else-if="listing.planType === 'impulso'" class="badge impulso">Patrocinado</span>
          <span v-else-if="listing.planType === 'purpura'" class="badge purpura">Destacado</span>
          <span v-if="listing.urgent && daysRemaining >= 0" class="badge urgent">Urgente</span>
        </div>
      </div>

      <!-- Título del Puesto -->
      <h3 class="job-title">{{ listing.title }}</h3>

      <!-- Salario -->
      <div class="job-salary">
        <va-icon name="payments" size="small" />
        <span>{{ formattedSalary }}</span>
      </div>

      <!-- Empresa + Verificación -->
      <div class="job-company">
        <span class="company-name">{{ listing.companyName }}</span>
        <va-icon
          v-if="listing.verified"
          name="verified"
          size="small"
          class="verified-icon"
          title="Empresa verificada"
        />
      </div>

      <!-- Ciudad -->
      <div class="job-location">
        <va-icon name="place" size="small" />
        <span>{{ listing.city }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'JobListCompact',

  props: {
    listing: {
      type: Object,
      required: true
    },
    isSelected: {
      type: Boolean,
      default: false
    }
  },

  emits: ['select'],

  computed: {
    publishDate() {
      const days = this.listing.publishedDaysAgo || 0

      // Casos especiales
      if (days === 0) return 'Publicado hoy'
      if (days === 1) return 'Publicado ayer'

      // Días recientes (menos de una semana)
      if (days < 7) {
        return `Publicado hace ${days} días`
      }

      // Semanas (7-29 días)
      if (days < 30) {
        const weeks = Math.floor(days / 7)
        if (weeks === 1) return 'Publicado hace una semana'
        return `Publicado hace ${weeks} semanas`
      }

      // Meses (30+ días)
      const months = Math.floor(days / 30)
      if (months === 1) return 'Publicado hace un mes'
      return `Publicado hace ${months} meses`
    },

    daysRemaining() {
      // CRÍTICO: Usar applicationDeadline (fecha límite de postulación) NO expiryDate (fecha de vencimiento del plan)
      const deadline = this.listing.applicationDeadline || this.listing.expiryDate
      if (!deadline) return null

      const today = new Date()
      today.setHours(0, 0, 0, 0)

      // Parsear como fecha local para evitar problemas de zona horaria
      const [year, month, day] = deadline.split('-')
      const deadlineDate = new Date(year, month - 1, day)
      deadlineDate.setHours(0, 0, 0, 0)

      const diff = deadlineDate - today
      const days = Math.ceil(diff / (1000 * 60 * 60 * 24))

      return days
    },

    expiryText() {
      // CRÍTICO: Mostrar applicationDeadline (cuándo cierra la convocatoria) NO expiryDate
      const deadline = this.listing.applicationDeadline || this.listing.expiryDate
      if (!deadline) return ''

      // Parsear como fecha local para evitar problemas de zona horaria
      const [year, month, day] = deadline.split('-')
      const deadlineDate = new Date(year, month - 1, day)
      const options = { day: '2-digit', month: 'short', year: 'numeric' }
      const formattedDate = deadlineDate.toLocaleDateString('es-ES', options)

      return `Cierra: ${formattedDate}`
    },

    expiryClass() {
      if (this.daysRemaining === null) return ''

      if (this.daysRemaining < 0) return 'expired'
      if (this.daysRemaining <= 3) return 'urgent'
      if (this.daysRemaining <= 7) return 'warning'
      return 'normal'
    },

    formattedSalary() {
      if (!this.listing.salary || this.listing.salary === 'A convenir') {
        return 'A convenir'
      }

      // Si ya viene formateado desde el backend
      if (this.listing.salaryMin && this.listing.salaryMax) {
        return `Bs ${this.formatNumber(this.listing.salaryMin)} - ${this.formatNumber(this.listing.salaryMax)}`
      }

      return this.listing.salary
    }
  },

  methods: {
    formatNumber(num) {
      return new Intl.NumberFormat('es-BO').format(num)
    }
  }
}
</script>

<style scoped>
.job-list-compact {
  position: relative;
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 0.75rem;
}

.job-list-compact:hover {
  background: #F9FAFB;
  border-color: #7C3AED;
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.1);
}

.job-list-compact.selected {
  background: #F5F3FF;
  border-color: #7C3AED;
  border-width: 2px;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
}

/* Indicador de selección (barra izquierda) */
.selection-indicator {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: transparent;
  border-radius: 8px 0 0 8px;
  transition: background 0.2s;
}

.job-list-compact.selected .selection-indicator {
  background: #7C3AED;
}

/* Contenido */
.job-content {
  flex: 1;
  min-width: 0;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
  gap: 0.5rem;
}

.date-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.publish-date {
  font-size: 0.75rem;
  color: #6B7280;
  font-weight: 500;
}

.expiry-date {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.125rem 0.375rem;
  border-radius: 4px;
  width: fit-content;
  transition: all 0.2s ease;
}

.expiry-date.normal {
  color: #059669;
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
}

.expiry-date.warning {
  color: #7c3aed;
  background: #f5f3ff;
  border: 1px solid #c4b5fd;
}

.expiry-date.urgent {
  color: #be123c;
  background: #fff1f2;
  border: 1px solid #fda4af;
  animation: pulse-urgent 2s ease-in-out infinite;
}

.expiry-date.expired {
  color: #6b7280;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  text-decoration: line-through;
}

@keyframes pulse-urgent {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(190, 18, 60, 0.25);
  }
  50% {
    box-shadow: 0 0 0 3px rgba(190, 18, 60, 0);
  }
}

.badges {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.badge {
  font-size: 0.7rem;
  padding: 0.125rem 0.5rem;
  border-radius: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.badge.impulso {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  color: white;
  border: 1px solid rgba(16, 185, 129, 0.5);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.badge.purpura {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  color: white;
  border: 1px solid rgba(124, 58, 237, 0.5);
  box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
}

.badge.urgent {
  background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
  color: white;
  border: 1px solid rgba(220, 38, 38, 0.5);
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3);
}

.badge.closed {
  background: linear-gradient(135deg, #64748B 0%, #475569 100%);
  color: white;
  border: 1px solid rgba(100, 116, 139, 0.5);
  box-shadow: 0 2px 8px rgba(100, 116, 139, 0.3);
  font-weight: 700;
  text-transform: uppercase;
}

.job-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111827;
  margin: 0 0 0.5rem 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.3;
}

.job-salary {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #059669;
  margin-bottom: 0.375rem;
}

.job-company {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin-bottom: 0.25rem;
}

.company-name {
  font-size: 0.85rem;
  color: #374151;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.verified-icon {
  color: #3B82F6;
  flex-shrink: 0;
}

.job-location {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8rem;
  color: #6B7280;
}

/* Logo de Empresa GRANDE */
.company-logo-large,
.company-logo-placeholder {
  width: 80px;
  height: 80px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  overflow: hidden;
  border: 2px solid #E5E7EB;
  background: white;
  margin-right: 1rem;
}

.company-logo-large img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.company-logo-placeholder {
  background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
  color: #9CA3AF;
}

.job-list-compact.selected .company-logo-large,
.job-list-compact.selected .company-logo-placeholder {
  border-color: #7C3AED;
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .job-list-compact {
    padding: 0.75rem;
    gap: 0.5rem;
  }

  .job-title {
    font-size: 0.875rem;
    line-height: 1.4;
  }

  .company-logo-large,
  .company-logo-placeholder {
    width: 56px;
    height: 56px;
    margin-right: 0.5rem;
  }

  .job-salary {
    font-size: 0.8rem;
  }

  .company-name {
    font-size: 0.8rem;
  }

  .job-location {
    font-size: 0.75rem;
  }

  .badge {
    font-size: 0.65rem;
    padding: 0.1rem 0.4rem;
  }

  .publish-date {
    font-size: 0.7rem;
  }
}
</style>
