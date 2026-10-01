<template>
  <div class="row justify-content-center">
    <div class="col-md-7">
      <div class="card">
        <div class="card-body p-4">
          <h4 class="mb-3"><i class="bi bi-building me-2"></i>Company Registration</h4>
          <p class="text-muted small">
            Your account will be reviewed by the placement cell. You can create
            drives once approved.
          </p>
          <form @submit.prevent="submit">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Company Name *</label>
                <input v-model.trim="form.company_name" class="form-control" required />
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
                <label class="form-label">HR Name</label>
                <input v-model.trim="form.hr_name" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">HR Contact</label>
                <input v-model.trim="form.hr_contact" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Website</label>
                <input v-model.trim="form.website" class="form-control" placeholder="https://" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Location</label>
                <input v-model.trim="form.location" class="form-control" />
              </div>
              <div class="col-12">
                <label class="form-label">Description</label>
                <textarea v-model.trim="form.description" class="form-control" rows="2"></textarea>
              </div>
            </div>
            <div v-if="error" class="alert alert-danger py-2 mt-3">{{ error }}</div>
            <button class="btn btn-primary w-100 mt-3" :disabled="loading">
              {{ loading ? "Creating..." : "Register Company" }}
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
  name: "RegisterCompany",
  data() {
    return {
      form: {
        company_name: "", email: "", password: "", hr_name: "",
        hr_contact: "", website: "", location: "", description: "",
      },
      error: "",
      loading: false,
    };
  },
  methods: {
    async submit() {
      this.error = "";
      this.loading = true;
      try {
        const { data } = await api.post("/auth/register/company", this.form);
        this.$store.dispatch("login", { token: data.access_token, user: data.user });
        this.$store.dispatch("notify", { message: "Company registered. Awaiting approval." });
        this.$router.push("/company");
      } catch (e) {
        this.error = e.response?.data?.message || "Registration failed";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
