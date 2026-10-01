<template>
  <div class="card stat-card h-100" :style="{ background: bg }">
    <div class="card-body d-flex align-items-center">
      <i class="bi me-3" :class="icon" style="font-size: 2rem; opacity: 0.85"></i>
      <div>
        <div class="num">{{ value }}</div>
        <div class="small text-white-50">{{ title }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "StatCard",
  props: {
    title: String,
    value: [Number, String],
    icon: { type: String, default: "bi-bar-chart" },
    bg: { type: String, default: "#2563eb" },
  },
};
</script>
