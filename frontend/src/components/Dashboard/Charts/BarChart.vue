<!-- Componente de Gráfico de Barras -->
<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import {
  Chart,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from 'chart.js'

// Registrar elementos de Chart.js
Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

// ========== PROPS ==========
const props = defineProps({
  data: {
    type: Object,
    required: true,
    // Formato: { labels: ['Ene', 'Feb'], datasets: [{ label: 'Postulaciones', data: [10, 20], color: '#7c3aed' }] }
  },
  title: {
    type: String,
    default: ''
  }
})

// ========== DATA ==========
const chartCanvas = ref(null)
let chartInstance = null

// ========== LIFECYCLE ==========
onMounted(() => {
  createChart()
})

watch(() => props.data, () => {
  updateChart()
}, { deep: true })

// ========== METHODS ==========
const createChart = () => {
  if (!chartCanvas.value) return

  const ctx = chartCanvas.value.getContext('2d')

  // Preparar datasets
  const datasets = (props.data.datasets || []).map(dataset => ({
    label: dataset.label,
    data: dataset.data,
    backgroundColor: dataset.color || '#7c3aed',
    borderRadius: 6,
    borderSkipped: false
  }))

  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: props.data.labels || [],
      datasets: datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: datasets.length > 1,
          position: 'top',
          labels: {
            padding: 15,
            font: {
              size: 12,
              family: "'Inter', sans-serif",
              weight: 600
            },
            color: '#4B5563',
            usePointStyle: true,
            pointStyle: 'circle'
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleFont: {
            size: 14,
            weight: 'bold'
          },
          bodyFont: {
            size: 13
          },
          padding: 12,
          cornerRadius: 8,
          displayColors: true
        }
      },
      scales: {
        x: {
          grid: {
            display: false
          },
          ticks: {
            color: '#6B7280',
            font: {
              size: 11,
              weight: 600
            }
          }
        },
        y: {
          beginAtZero: true,
          grid: {
            color: '#F3F4F6',
            drawBorder: false
          },
          ticks: {
            color: '#6B7280',
            font: {
              size: 11,
              weight: 600
            },
            precision: 0
          }
        }
      },
      animation: {
        duration: 1000,
        easing: 'easeInOutQuart'
      }
    }
  })
}

const updateChart = () => {
  if (!chartInstance) return

  chartInstance.data.labels = props.data.labels || []
  chartInstance.data.datasets = (props.data.datasets || []).map(dataset => ({
    label: dataset.label,
    data: dataset.data,
    backgroundColor: dataset.color || '#7c3aed',
    borderRadius: 6,
    borderSkipped: false
  }))
  chartInstance.update()
}
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 280px;
}

canvas {
  max-height: 280px;
}
</style>
