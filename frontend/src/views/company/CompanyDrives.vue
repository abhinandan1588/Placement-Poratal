<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3 class="mb-0">My Drives</h3>
      <button class="btn btn-primary" @click="showForm = !showForm" :disabled="!approved">
        <i class="bi bi-plus-lg me-1"></i> New Drive
      </button>
    </div>

    <div v-if="!approved" class="alert alert-warning">
      You can create drives only after the admin approves your company.
    </div>

    <div v-if="showForm && approved" class="card mb-4">
      <div class="card-body">
        <h6 class="mb-3">Create Placement Drive</h6>
        <form @submit.prevent="create">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">Job Title *</label>
              <input v-model.trim="form.job_title" class="form-control" required />
            </div>
            <div class="col-md-3">
              <label class="form-label">Package</label>
              <input v-model.trim="form.package" class="form-control" placeholder="e.g. 12 LPA" />
            </div>
            <div class="col-md-3">
              <label class="form-label">Openings</label>
              <input v-model="form.openings" type="number" min="1" class="form-control" />
            </div>
            <div class="col-12">
              <label class="form-label">Job Description</label>
              <textarea v-model.trim="form.job_description" class="form-control" rows="2"></textarea>
            </div>
            <div class="col-md-4">
              <label class="form-label">Eligible Branches (comma separated)</label>
              <input v-model.trim="form.eligible_branches" class="form-control" placeholder="CSE, IT (blank = all)" />
            </div>
            <div class="col-md-2">
              <label class="form-label">Min CGPA</label>
              <input v-model="form.min_cgpa" type="number" step="0.01" min="0" max="10" class="form-control" />
            </div>
            <div class="col-md-3">
              <label class="form-label">Graduation Year</label>
              <input v-model="form.eligible_year" type="number" class="form-control" placeholder="any" />
            </div>
            <div class="col-md-3">
              <label class="form-label">Deadline</label>
              <input v-model="form.application_deadline" type="date" class="form-control" />
            </div>
            <div class="col-md-12">
              <label class="form-label">Location</label>
              <input v-model.trim="form.location" class="form-control" />
            </div>
          </div>
          <div v-if="error" class="alert alert-danger py-2 mt-3">{{ error }}</div>
          <button class="btn btn-success mt-3" :disabled="loading">Create Drive</button>
          <button type="button" class="btn btn-link mt-3" @click="showForm = false">Cancel</button>
        </form>
      </div>
    </div>

    <div class="card">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr><th>Job Title</th><th>Eligibility</th><th>Deadline</th><th>Applicants</th><th>Status</th><th class="text-end">Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="d in drives" :key="d.id">
              <td><strong>{{ d.job_title }}</strong><br /><small class="text-muted">{{ d.package }}</small></td>
              <td><small>CGPA ≥ {{ d.min_cgpa }}<br />{{ d.eligible_branches.length ? d.eligible_branches.join(", ") : "All" }}</small></td>
              <td>{{ d.application_deadline || "-" }}</td>
              <td>{{ d.applicants_count }}</td>
              <td><span class="badge badge-status" :class="statusClass(d.status)">{{ d.status }}</span></td>
              <td class="text-end">
                <router-link :to="`/company/drives/${d.id}/applicants`" class="btn btn-sm btn-outline-primary me-1">
                  View Applicants
                </router-link>
                <button v-if="d.status === 'approved'" class="btn btn-sm btn-outline-secondary" @click="close(d)">Close</button>
              </td>
            </tr>
            <tr v-if="!drives.length"><td colspan="6" class="text-center text-muted py-4">No drives yet</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";

export default {
  name: "CompanyDrives",
  data() {
    return {
      drives: [],
      approved: false,
      showForm: false,
      loading: false,
      error: "",
      form: this.blankForm(),
    };
  },
  created() {
    this.load();
  },
  methods: {
    blankForm() {
      return {
        job_title: "", package: "", openings: 1, job_description: "",
        eligible_branches: "", min_cgpa: 0, eligible_year: "",
        application_deadline: "", location: "",
      };
    },
    async load() {
      const dash = await api.get("/company/dashboard");
      this.approved = dash.data.company.approval_status === "approved";
      const { data } = await api.get("/company/drives");
      this.drives = data.drives;
    },
    statusClass(s) {
      return { approved: "bg-success", pending: "bg-warning text-dark", rejected: "bg-danger", closed: "bg-secondary" }[s] || "bg-secondary";
    },
    async create() {
      this.error = "";
      this.loading = true;
      try {
        const payload = { ...this.form };
        payload.eligible_branches = payload.eligible_branches
          ? payload.eligible_branches.split(",").map((b) => b.trim()).filter(Boolean)
          : [];
        await api.post("/company/drives", payload);
        this.$store.dispatch("notify", { message: "Drive created. Awaiting approval." });
        this.showForm = false;
        this.form = this.blankForm();
        this.load();
      } catch (e) {
        this.error = e.response?.data?.message || "Could not create drive";
      } finally {
        this.loading = false;
      }
    },
    async close(d) {
      await api.put(`/company/drives/${d.id}`, { status: "closed" });
      this.$store.dispatch("notify", { message: "Drive closed" });
      this.load();
    },
  },
};
</script>
