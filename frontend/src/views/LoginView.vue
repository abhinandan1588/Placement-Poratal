<template>
  <div class="row justify-content-center">
    <div class="col-md-5">
      <div class="card">
        <div class="card-body p-4">
          <h4 class="mb-3"><i class="bi bi-box-arrow-in-right me-2"></i>Login</h4>
          <form @submit.prevent="submit">
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input v-model.trim="email" type="email" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Password</label>
              <input v-model="password" type="password" class="form-control" required />
            </div>
            <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
            <button class="btn btn-primary w-100" :disabled="loading">
              {{ loading ? "Signing in..." : "Login" }}
            </button>
          </form>
          <hr />
          <p class="small text-muted mb-1">
            New student? <router-link to="/register/student">Register</router-link>
          </p>
          <p class="small text-muted mb-2">
            New company? <router-link to="/register/company">Register</router-link>
          </p>
          <p class="small text-muted mb-0">
            Admin demo: <code>admin@ppa.com</code> / <code>admin123</code>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  name: "Login",
  data() {
    return { email: "", password: "", error: "", loading: false };
  },
  methods: {
    async submit() {
      this.error = "";
      this.loading = true;
      try {
        const { data } = await api.post("/auth/login", {
          email: this.email,
          password: this.password,
        });
        this.$store.dispatch("login", { token: data.access_token, user: data.user });
        this.$store.dispatch("notify", { message: "Welcome back!" });
        this.$router.push("/" + data.user.role);
      } catch (e) {
        this.error = e.response?.data?.message || "Login failed";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
