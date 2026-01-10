<!-- Mini Bar Chart - Gráfico de barras pequeño y simple -->
<template>
  <div class="mini-bar-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, BarController, BarElement, CategoryScale, LinearScale } from 'chart.js'

// Registrar solo los componentes necesarios (ligero)
Chart.register(BarController, BarElement, CategoryScale, LinearScale)

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

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [''],
      datasets: [{
        data: [percentage],
        backgroundColor: props.color,
        borderWidth: 0,
        borderRadius: 4,
        barPercentage: 0.6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      indexAxis: 'y', // Barra horizontal
      plugins: {
        tooltip: {
          enabled: false
        },
        legend: {
          display: false
        }
      },
      scales: {
        x: {
          display: false,
          min: 0,
          max: 100
        },
        y: {
          display: false
        }
      },
      animation: {
        duration: 750,
        easing: 'easeOutQuart'
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
.mini-bar-container {
  width: 60px;
  height: 60px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

canvas {
  width: 100% !important;
  height: 20px !important;
}
</style>
