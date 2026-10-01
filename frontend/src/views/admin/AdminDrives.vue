<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
      <h3 class="mb-0">Placement Drives</h3>
      <div class="d-flex gap-2">
        <select v-model="status" class="form-select form-select-sm" @change="load">
          <option value="">All</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
          <option value="closed">Closed</option>
        </select>
        <input v-model="q" @input="load" class="form-control form-control-sm" placeholder="Search title..." />
      </div>
    </div>

    <div class="card">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr><th>Job Title</th><th>Company</th><th>Eligibility</th><th>Deadline</th><th>Applicants</th><th>Status</th><th class="text-end">Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="d in drives" :key="d.id">
              <td><strong>{{ d.job_title }}</strong><br /><small class="text-muted">{{ d.package || "" }}</small></td>
              <td>{{ d.company_name }}</td>
              <td>
                <small>
                  CGPA ≥ {{ d.min_cgpa }}<br />
                  {{ d.eligible_branches.length ? d.eligible_branches.join(", ") : "All branches" }}
                </small>
              </td>
              <td>{{ d.application_deadline || "-" }}</td>
              <td>{{ d.applicants_count }}</td>
              <td><span class="badge badge-status" :class="statusClass(d.status)">{{ d.status }}</span></td>
              <td class="text-end">
                <button v-if="d.status !== 'approved'" class="btn btn-sm btn-success me-1" @click="decide(d, 'approved')">Approve</button>
                <button v-if="d.status !== 'rejected'" class="btn btn-sm btn-outline-danger me-1" @click="decide(d, 'rejected')">Reject</button>
                <button v-if="d.status === 'approved'" class="btn btn-sm btn-outline-secondary" @click="decide(d, 'closed')">Close</button>
              </td>
            </tr>
            <tr v-if="!drives.length"><td colspan="7" class="text-center text-muted py-4">No drives found</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";

export default {
  name: "AdminDrives",
  data() {
    return { drives: [], q: "", status: "" };
  },
  created() {
    this.load();
  },
  methods: {
    async load() {
      const { data } = await api.get("/admin/drives", { params: { q: this.q, status: this.status } });
      this.drives = data.drives;
    },
    statusClass(s) {
      return { approved: "bg-success", pending: "bg-warning text-dark", rejected: "bg-danger", closed: "bg-secondary" }[s] || "bg-secondary";
    },
    async decide(d, decision) {
      await api.patch(`/admin/drives/${d.id}/approval`, { decision });
      this.$store.dispatch("notify", { message: `Drive ${decision}` });
      this.load();
    },
  },
};
</script>
