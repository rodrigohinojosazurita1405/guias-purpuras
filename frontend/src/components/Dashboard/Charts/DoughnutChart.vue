<!-- Componente de Gráfico de Torta/Dona -->
<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js'

// Registrar elementos de Chart.js
Chart.register(ArcElement, Tooltip, Legend)

// ========== PROPS ==========
const props = defineProps({
  data: {
    type: Object,
    required: true,
    // Formato: { labels: ['Label1', 'Label2'], values: [10, 20], colors: ['#color1', '#color2'] }
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

  chartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: props.data.labels || [],
      datasets: [{
        data: props.data.values || [],
        backgroundColor: props.data.colors || [
          '#7c3aed', '#3B82F6', '#F59E0B', '#10B981', '#EF4444'
        ],
        borderWidth: 0,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: 'bottom',
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
          displayColors: true,
          callbacks: {
            label: function(context) {
              const label = context.label || ''
              const value = context.parsed || 0
              const total = context.dataset.data.reduce((a, b) => a + b, 0)
              const percentage = ((value / total) * 100).toFixed(1)
              return `${label}: ${value} (${percentage}%)`
            }
          }
        }
      },
      cutout: '65%', // Hace el efecto de dona
      animation: {
        animateRotate: true,
        animateScale: true,
        duration: 1000,
        easing: 'easeInOutQuart'
      }
    }
  })
}

const updateChart = () => {
  if (!chartInstance) return

  chartInstance.data.labels = props.data.labels || []
  chartInstance.data.datasets[0].data = props.data.values || []
  chartInstance.data.datasets[0].backgroundColor = props.data.colors || [
    '#7c3aed', '#3B82F6', '#F59E0B', '#10B981', '#EF4444'
  ]
  chartInstance.update()
}
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
}

canvas {
  max-height: 280px;
}
</style>
