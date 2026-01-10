<!-- Mini Donut Chart - Gráfico pequeño y simple -->
<template>
  <div class="mini-donut-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, DoughnutController, ArcElement, Tooltip } from 'chart.js'

// Registrar solo los componentes necesarios (ligero)
Chart.register(DoughnutController, ArcElement, Tooltip)

// ========== PROPS ==========
const props = defineProps({
  value: {
    type: Number,
    default: 0
  },
  total: {
    type: Number,
    default: 100
  },
  color: {
    type: String,
    default: '#7c3aed' // Púrpura por defecto
  }
})

// ========== DATA ==========
const chartCanvas = ref(null)
let chartInstance = null

// ========== METHODS ==========
const createChart = () => {
  if (!chartCanvas.value) return

  // Destruir chart anterior si existe
  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = chartCanvas.value.getContext('2d')
  const percentage = props.total > 0 ? (props.value / props.total) * 100 : 0
  const remaining = 100 - percentage

  chartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      datasets: [{
        data: [percentage, remaining],
        backgroundColor: [
          props.color,
          '#E5E7EB'
        ],
        borderWidth: 0,
        cutout: '75%' // Más delgado
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        tooltip: {
          enabled: false // Sin tooltips para mantenerlo simple
        },
        legend: {
          display: false
        }
      },
      animation: {
        animateRotate: true,
        animateScale: false
      }
    }
  })
}

// ========== LIFECYCLE ==========
onMounted(() => {
  createChart()
})

// Observar cambios en los datos
watch(() => [props.value, props.total, props.color], () => {
  createChart()
})
</script>

<style scoped>
.mini-donut-container {
  width: 60px;
  height: 60px;
  position: relative;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
