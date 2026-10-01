<template>
  <div class="row justify-content-center">
    <div class="col-md-7">
      <div class="card">
        <div class="card-body p-4">
          <h4 class="mb-3"><i class="bi bi-person-plus me-2"></i>Student Registration</h4>
          <form @submit.prevent="submit">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Full Name *</label>
                <input v-model.trim="form.name" class="form-control" required />
              </div>
              <div class="col-md-6">
                <label class="form-label">Email *</label>
                <input v-model.trim="form.email" type="email" class="form-control" required />
              </div>
              <div class="col-md-6">
                <label class="form-label">Password *</label>
                <input v-model="form.password" type="password" class="form-control" minlength="6" required />
              </div>
              <div class="col-md-6">
                <label class="form-label">Roll Number</label>
                <input v-model.trim="form.roll_number" class="form-control" />
              </div>
              <div class="col-md-4">
                <label class="form-label">Branch</label>
                <input v-model.trim="form.branch" class="form-control" placeholder="e.g. CSE" />
              </div>
              <div class="col-md-4">
                <label class="form-label">CGPA</label>
                <input v-model="form.cgpa" type="number" step="0.01" min="0" max="10" class="form-control" />
              </div>
              <div class="col-md-4">
                <label class="form-label">Graduation Year</label>
                <input v-model="form.graduation_year" type="number" class="form-control" placeholder="2026" />
              </div>
            </div>
            <div v-if="error" class="alert alert-danger py-2 mt-3">{{ error }}</div>
            <button class="btn btn-primary w-100 mt-3" :disabled="loading">
              {{ loading ? "Creating..." : "Create Account" }}
            </button>
          </form>
          <p class="small text-muted mt-3 mb-0">
            Already registered? <router-link to="/login">Login</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  name: "RegisterStudent",
  data() {
    return {
      form: { name: "", email: "", password: "", roll_number: "", branch: "", cgpa: "", graduation_year: "" },
      error: "",
      loading: false,
    };
  },
  methods: {
    async submit() {
      this.error = "";
      this.loading = true;
      try {
        const { data } = await api.post("/auth/register/student", this.form);
        this.$store.dispatch("login", { token: data.access_token, user: data.user });
        this.$store.dispatch("notify", { message: "Account created!" });
        this.$router.push("/student");
      } catch (e) {
        this.error = e.response?.data?.message || "Registration failed";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
