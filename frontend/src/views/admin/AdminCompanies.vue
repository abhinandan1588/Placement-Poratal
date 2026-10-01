<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
      <h3 class="mb-0">Companies</h3>
      <div class="d-flex gap-2">
        <select v-model="status" class="form-select form-select-sm" @change="load">
          <option value="">All statuses</option>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
        </select>
        <input v-model="q" @input="load" class="form-control form-control-sm" placeholder="Search name..." />
      </div>
    </div>

    <div class="card">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr>
              <th>Company</th><th>HR Contact</th><th>Drives</th>
              <th>Approval</th><th>Account</th><th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in companies" :key="c.id">
              <td>
                <strong>{{ c.company_name }}</strong><br />
                <small class="text-muted">{{ c.email }}</small>
              </td>
              <td>{{ c.hr_name || "-" }}<br /><small class="text-muted">{{ c.hr_contact || "" }}</small></td>
              <td>{{ c.drives_count }}</td>
              <td><span class="badge badge-status" :class="approvalClass(c.approval_status)">{{ c.approval_status }}</span></td>
              <td>
                <span v-if="c.is_blacklisted" class="badge bg-dark">Blacklisted</span>
                <span v-else-if="!c.is_active" class="badge bg-secondary">Deactivated</span>
                <span v-else class="badge bg-success">Active</span>
              </td>
              <td class="text-end">
                <button v-if="c.approval_status !== 'approved'" class="btn btn-sm btn-success me-1" @click="approve(c, 'approved')">Approve</button>
                <button v-if="c.approval_status !== 'rejected'" class="btn btn-sm btn-outline-danger me-1" @click="approve(c, 'rejected')">Reject</button>
                <button class="btn btn-sm btn-outline-secondary me-1" @click="toggleStatus(c, 'is_active', !c.is_active)">
                  {{ c.is_active ? "Deactivate" : "Activate" }}
                </button>
                <button class="btn btn-sm btn-outline-dark" @click="toggleStatus(c, 'is_blacklisted', !c.is_blacklisted)">
                  {{ c.is_blacklisted ? "Unblacklist" : "Blacklist" }}
                </button>
              </td>
            </tr>
            <tr v-if="!companies.length"><td colspan="6" class="text-center text-muted py-4">No companies found</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";

export default {
  name: "AdminCompanies",
  data() {
    return { companies: [], q: "", status: this.$route.query.status || "" };
  },
  created() {
    this.load();
  },
  methods: {
    async load() {
      const { data } = await api.get("/admin/companies", { params: { q: this.q, status: this.status } });
      this.companies = data.companies;
    },
    approvalClass(s) {
      return { approved: "bg-success", pending: "bg-warning text-dark", rejected: "bg-danger" }[s] || "bg-secondary";
    },
    async approve(c, decision) {
      await api.patch(`/admin/companies/${c.id}/approval`, { decision });
      this.$store.dispatch("notify", { message: `Company ${decision}` });
      this.load();
    },
    async toggleStatus(c, field, value) {
      await api.patch(`/admin/users/${c.user_id}/status`, { [field]: value });
      this.$store.dispatch("notify", { message: "Status updated" });
      this.load();
    },
  },
};
</script>
