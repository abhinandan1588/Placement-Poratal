<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
      <h3 class="mb-0">Available Drives</h3>
      <div class="d-flex gap-2 align-items-center">
        <div class="form-check">
          <input id="elig" v-model="onlyEligible" type="checkbox" class="form-check-input" @change="load" />
          <label for="elig" class="form-check-label small">Eligible only</label>
        </div>
        <input v-model="q" @input="load" class="form-control form-control-sm" placeholder="Search job title..." />
      </div>
    </div>

    <div class="row g-3">
      <div class="col-md-6 col-lg-4" v-for="d in drives" :key="d.id">
        <div class="card h-100">
          <div class="card-body d-flex flex-column">
            <div class="d-flex justify-content-between">
              <h5 class="mb-1">{{ d.job_title }}</h5>
              <span v-if="d.package" class="badge bg-light text-dark align-self-start">{{ d.package }}</span>
            </div>
            <p class="text-primary mb-2"><i class="bi bi-building me-1"></i>{{ d.company_name }}</p>
            <p class="text-muted small flex-grow-1">{{ d.job_description || "No description provided." }}</p>
            <ul class="list-unstyled small mb-3">
              <li><i class="bi bi-mortarboard me-1"></i> CGPA ≥ {{ d.min_cgpa }}</li>
              <li><i class="bi bi-diagram-3 me-1"></i> {{ d.eligible_branches.length ? d.eligible_branches.join(", ") : "All branches" }}</li>
              <li v-if="d.location"><i class="bi bi-geo-alt me-1"></i> {{ d.location }}</li>
              <li :class="d.deadline_passed ? 'text-danger' : ''">
                <i class="bi bi-calendar me-1"></i> Deadline: {{ d.application_deadline || "open" }}
              </li>
            </ul>

            <div v-if="!d.eligible" class="alert alert-warning py-1 small mb-2">{{ d.eligibility_reason }}</div>

            <button
              class="btn btn-sm"
              :class="d.already_applied ? 'btn-success' : 'btn-primary'"
              :disabled="d.already_applied || !d.eligible || d.deadline_passed || applying === d.id"
              @click="apply(d)"
            >
              <span v-if="d.already_applied"><i class="bi bi-check-lg"></i> Applied</span>
              <span v-else-if="d.deadline_passed">Closed</span>
              <span v-else>Apply Now</span>
            </button>
          </div>
        </div>
      </div>
      <div v-if="!drives.length" class="col-12">
        <p class="text-center text-muted py-5">No approved drives match your filters.</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";

export default {
  name: "StudentDashboard",
  data() {
    return { drives: [], q: "", onlyEligible: false, applying: null };
  },
  created() {
    this.load();
  },
  methods: {
    async load() {
      const { data } = await api.get("/student/drives", {
        params: { q: this.q, eligible: this.onlyEligible ? "true" : "false" },
      });
      this.drives = data.drives;
    },
    async apply(d) {
      this.applying = d.id;
      try {
        await api.post(`/student/drives/${d.id}/apply`);
        this.$store.dispatch("notify", { message: "Application submitted!" });
        this.load();
      } catch (e) {
        this.$store.dispatch("notify", { message: e.response?.data?.message || "Could not apply", type: "error" });
      } finally {
        this.applying = null;
      }
    },
  },
};
</script>
