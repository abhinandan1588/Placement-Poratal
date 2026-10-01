<template>
  <div class="row justify-content-center">
    <div class="col-md-8">
      <h3 class="mb-3">Company Profile</h3>
      <div class="card">
        <div class="card-body p-4">
          <form @submit.prevent="save">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Company Name</label>
                <input v-model.trim="form.company_name" class="form-control" required />
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
                <input v-model.trim="form.website" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Location</label>
                <input v-model.trim="form.location" class="form-control" />
              </div>
              <div class="col-12">
                <label class="form-label">Description</label>
                <textarea v-model.trim="form.description" class="form-control" rows="3"></textarea>
              </div>
            </div>
            <button class="btn btn-primary mt-3" :disabled="loading">Save Changes</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";

export default {
  name: "CompanyProfile",
  data() {
    return { form: {}, loading: false };
  },
  async created() {
    const { data } = await api.get("/company/profile");
    this.form = data.company;
  },
  methods: {
    async save() {
      this.loading = true;
      try {
        await api.put("/company/profile", this.form);
        this.$store.dispatch("notify", { message: "Profile saved" });
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
