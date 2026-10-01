<template>
  <div class="row justify-content-center">
    <div class="col-md-8">
      <h3 class="mb-3">My Profile</h3>
      <div class="card mb-4">
        <div class="card-body p-4">
          <form @submit.prevent="save">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Full Name</label>
                <input v-model.trim="form.name" class="form-control" required />
              </div>
              <div class="col-md-6">
                <label class="form-label">Roll Number</label>
                <input v-model.trim="form.roll_number" class="form-control" />
              </div>
              <div class="col-md-4">
                <label class="form-label">Branch</label>
                <input v-model.trim="form.branch" class="form-control" />
              </div>
              <div class="col-md-4">
                <label class="form-label">CGPA</label>
                <input v-model="form.cgpa" type="number" step="0.01" min="0" max="10" class="form-control" />
              </div>
              <div class="col-md-4">
                <label class="form-label">Graduation Year</label>
                <input v-model="form.graduation_year" type="number" class="form-control" />
              </div>
              <div class="col-md-6">
                <label class="form-label">Phone</label>
                <input v-model.trim="form.phone" class="form-control" />
              </div>
              <div class="col-12">
                <label class="form-label">Bio</label>
                <textarea v-model.trim="form.bio" class="form-control" rows="2"></textarea>
              </div>
            </div>
            <button class="btn btn-primary mt-3" :disabled="loading">Save Profile</button>
          </form>
        </div>
      </div>

      <div class="card">
        <div class="card-body p-4">
          <h6 class="mb-3"><i class="bi bi-file-earmark-text me-1"></i>Resume</h6>
          <p v-if="form.resume_filename" class="small text-success">
            <i class="bi bi-check-circle"></i> Uploaded: {{ form.resume_filename }}
          </p>
          <p v-else class="small text-muted">No resume uploaded yet.</p>
          <input ref="file" type="file" class="form-control" accept=".pdf,.doc,.docx" />
          <button class="btn btn-outline-primary mt-2" @click="uploadResume" :disabled="uploading">
            {{ uploading ? "Uploading..." : "Upload Resume" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";

export default {
  name: "StudentProfile",
  data() {
    return { form: {}, loading: false, uploading: false };
  },
  async created() {
    const { data } = await api.get("/student/profile");
    this.form = data.student;
  },
  methods: {
    async save() {
      this.loading = true;
      try {
        await api.put("/student/profile", this.form);
        this.$store.dispatch("notify", { message: "Profile saved" });
      } finally {
        this.loading = false;
      }
    },
    async uploadResume() {
      const file = this.$refs.file.files[0];
      if (!file) {
        this.$store.dispatch("notify", { message: "Choose a file first", type: "error" });
        return;
      }
      const fd = new FormData();
      fd.append("resume", file);
      this.uploading = true;
      try {
        const { data } = await api.post("/student/resume", fd, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        this.form.resume_filename = data.resume_filename;
        this.$store.dispatch("notify", { message: "Resume uploaded" });
      } catch (e) {
        this.$store.dispatch("notify", { message: e.response?.data?.message || "Upload failed", type: "error" });
      } finally {
        this.uploading = false;
      }
    },
  },
};
</script>
