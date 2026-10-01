<template>
  <nav class="navbar navbar-expand-lg navbar-dark" style="background: var(--ppa-primary)">
    <div class="container-fluid px-3 px-lg-4">
      <router-link class="navbar-brand" :to="homeLink">
        <i class="bi bi-mortarboard-fill me-1"></i> Placement Portal
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        @click="open = !open"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" :class="{ show: open }">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0" @click="open = false">
          <template v-if="role === 'admin'">
            <li class="nav-item"><router-link class="nav-link" to="/admin">Dashboard</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/companies">Companies</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/students">Students</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/drives">Drives</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/admin/reports">Reports</router-link></li>
          </template>

          <template v-else-if="role === 'company'">
            <li class="nav-item"><router-link class="nav-link" to="/company">Dashboard</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/company/drives">My Drives</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/company/profile">Profile</router-link></li>
          </template>

          <template v-else-if="role === 'student'">
            <li class="nav-item"><router-link class="nav-link" to="/student">Browse Drives</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/student/applications">My Applications</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/student/profile">Profile</router-link></li>
          </template>

          <template v-if="isAuthenticated">
            <li class="nav-item d-flex align-items-center text-white-50 ms-lg-3 me-2">
              <small><i class="bi bi-person-circle me-1"></i>{{ email }}</small>
            </li>
            <li class="nav-item">
              <button class="btn btn-sm btn-outline-light" @click="doLogout">Logout</button>
            </li>
          </template>
          <template v-else>
            <li class="nav-item"><router-link class="nav-link" to="/login">Login</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/register/student">Register</router-link></li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "Navbar",
  data() {
    return { open: false };
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
    role() {
      return this.$store.getters.role;
    },
    email() {
      return this.$store.state.user ? this.$store.state.user.email : "";
    },
    homeLink() {
      if (this.role) return "/" + this.role;
      return "/";
    },
  },
  methods: {
    doLogout() {
      this.$store.dispatch("logout");
      this.$router.push("/login");
    },
  },
};
</script>
