<template>
  <div v-if="visible" class="toast-fixed">
    <div class="alert shadow" :class="alertClass" role="alert">
      <i class="bi me-1" :class="iconClass"></i>{{ toast.message }}
    </div>
  </div>
</template>

<script>
export default {
  name: "Toast",
  data() {
    return { visible: false, timer: null };
  },
  computed: {
    toast() {
      return this.$store.state.toast || {};
    },
    alertClass() {
      return this.toast.type === "error" ? "alert-danger" : "alert-success";
    },
    iconClass() {
      return this.toast.type === "error"
        ? "bi-exclamation-triangle-fill"
        : "bi-check-circle-fill";
    },
  },
  watch: {
    "$store.state.toast"(val) {
      if (!val) return;
      this.visible = true;
      clearTimeout(this.timer);
      this.timer = setTimeout(() => (this.visible = false), 3500);
    },
  },
};
</script>
