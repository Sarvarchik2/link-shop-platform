<template>
    <div class="chart-container">
        <Line v-if="type === 'line'" :data="chartData" :options="chartOptions" />
        <Doughnut v-else-if="type === 'doughnut'" :data="chartData" :options="chartOptions" />
    </div>
</template>

<script setup>
import { Line, Doughnut } from 'vue-chartjs'
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
    ArcElement
} from 'chart.js'

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
    ArcElement
)

const props = defineProps({
    type: {
        type: String,
        default: 'line'
    },
    data: {
        type: Object,
        required: true
    },
    options: {
        type: Object,
        default: () => ({})
    }
})

const chartData = computed(() => props.data)
const chartOptions = computed(() => ({
    responsive: true,
    maintainAspectRatio: false,
    ...props.options
}))
</script>

<style scoped>
.chart-container {
    width: 100%;
    height: 100%;
    min-height: 250px;
}
</style>
