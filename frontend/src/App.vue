<template>
  <div id="app">
    <Navbar />
    <Toast />
    <div class="page-wrap">
      <router-view />
    </div>
  </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";
import Toast from "./components/Toast.vue";

export default {
  name: "App",
  components: { Navbar, Toast },
};
</script>