<template>
  <div>
    <h3 class="mb-4">Admin Dashboard</h3>
    <div class="row g-3 mb-4">
      <div class="col-6 col-lg-3">
        <StatCard title="Students" :value="stats.total_students" icon="bi-people-fill" bg="rgba(209, 232, 63, 0.916)" />
      </div>
      <div class="col-6 col-lg-3">
        <StatCard title="Companies" :value="stats.total_companies" icon="bi-building" bg="#0ea5e9" />
      </div>
      <div class="col-6 col-lg-3">
        <StatCard title="Placement Drives" :value="stats.total_drives" icon="bi-briefcase-fill" bg="#7c3aed" />
      </div>
      <div class="col-6 col-lg-3">
        <StatCard title="Selections" :value="stats.total_selected" icon="bi-trophy-fill" bg="#16a34a" />
      </div>
    </div>

    <div class="row g-3">
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <h6 class="text-muted">Pending Approvals</h6>
            <ul class="list-group list-group-flush">
              <li class="list-group-item d-flex justify-content-between">
                Companies awaiting approval
                <span class="badge bg-warning text-dark">{{ stats.pending_companies }}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between">
                Drives awaiting approval
                <span class="badge bg-warning text-dark">{{ stats.pending_drives }}</span>
              </li>
            </ul>
            <router-link to="/admin/companies?status=pending" class="btn btn-sm btn-outline-primary mt-3 me-2">
              Review Companies
            </router-link>
            <router-link to="/admin/drives" class="btn btn-sm btn-outline-primary mt-3">
              Review Drives
            </router-link>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <h6 class="text-muted">Activity</h6>
            <ul class="list-group list-group-flush">
              <li class="list-group-item d-flex justify-content-between">
                Approved companies <span class="badge bg-success">{{ stats.approved_companies }}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between">
                Approved drives <span class="badge bg-success">{{ stats.approved_drives }}</span>
              </li>
              <li class="list-group-item d-flex justify-content-between">
                Total applications <span class="badge bg-secondary">{{ stats.total_applications }}</span>
              </li>
            </ul>
            <router-link to="/admin/reports" class="btn btn-sm btn-outline-primary mt-3">
              View Reports
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";
import StatCard from "../../components/StatCard.vue";

export default {
  name: "AdminDashboard",
  components: { StatCard },
  data() {
    return { stats: {} };
  },
  async created() {
    const { data } = await api.get("/admin/dashboard");
    this.stats = data.stats;
  },
};
</script>
