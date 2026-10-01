<template>
  <div>
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default {
  name: "BarChart",
  props: {
    labels: { type: Array, default: () => [] },
    values: { type: Array, default: () => [] },
    label: { type: String, default: "Count" },
    color: { type: String, default: "#2563eb" },
  },
  data() {
    return { chart: null };
  },
  watch: {
    values() {
      this.render();
    },
    labels() {
      this.render();
    },
  },
  mounted() {
    this.render();
  },
  beforeDestroy() {
    if (this.chart) this.chart.destroy();
  },
  methods: {
    render() {
      if (this.chart) this.chart.destroy();
      this.chart = new Chart(this.$refs.canvas, {
        type: "bar",
        data: {
          labels: this.labels,
          datasets: [
            {
              label: this.label,
              data: this.values,
              backgroundColor: this.color,
              borderRadius: 6,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
        },
      });
    },
  },
};
</script>
