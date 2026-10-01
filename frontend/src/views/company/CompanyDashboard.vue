<template>
  <div>
    <h3 class="mb-1">{{ company.company_name }}</h3>
    <p class="text-muted">
      Approval status:
      <span class="badge" :class="approvalClass">{{ company.approval_status }}</span>
    </p>

    <div v-if="company.approval_status === 'pending'" class="alert alert-warning">
      <i class="bi bi-hourglass-split me-1"></i>
      Your company is awaiting admin approval. You can create drives once approved.
    </div>
    <div v-if="company.approval_status === 'rejected'" class="alert alert-danger">
      Your company registration was rejected. Please contact the placement cell.
    </div>

    <div class="row g-3 mb-4">
      <div class="col-6 col-lg-3"><StatCard title="Total Drives" :value="stats.total_drives" icon="bi-briefcase" bg="#2563eb" /></div>
      <div class="col-6 col-lg-3"><StatCard title="Approved" :value="stats.approved_drives" icon="bi-check-circle" bg="#16a34a" /></div>
      <div class="col-6 col-lg-3"><StatCard title="Applicants" :value="stats.total_applicants" icon="bi-people" bg="#0ea5e9" /></div>
      <div class="col-6 col-lg-3"><StatCard title="Selected" :value="stats.selected" icon="bi-trophy" bg="#7c3aed" /></div>
    </div>

    <router-link to="/company/drives" class="btn btn-primary">
      <i class="bi bi-briefcase me-1"></i> Manage Drives
    </router-link>
  </div>
</template>

<script>
import api from "../../services/api";
import StatCard from "../../components/StatCard.vue";

export default {
  name: "CompanyDashboard",
  components: { StatCard },
  data() {
    return { company: {}, stats: {} };
  },
  computed: {
    approvalClass() {
      return { approved: "bg-success", pending: "bg-warning text-dark", rejected: "bg-danger" }[this.company.approval_status] || "bg-secondary";
    },
  },
  async created() {
    const { data } = await api.get("/company/dashboard");
    this.company = data.company;
    this.stats = data.stats;
  },
};
</script>
