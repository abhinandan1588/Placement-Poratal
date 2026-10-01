<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
      <h3 class="mb-0">Students</h3>
      <input v-model="q" @input="load" class="form-control form-control-sm" style="max-width: 280px" placeholder="Search name / roll / branch..." />
    </div>

    <div class="card">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr><th>Name</th><th>Roll</th><th>Branch</th><th>CGPA</th><th>Year</th><th>Account</th><th class="text-end">Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="s in students" :key="s.id">
              <td><strong>{{ s.name }}</strong><br /><small class="text-muted">{{ s.email }}</small></td>
              <td>{{ s.roll_number || "-" }}</td>
              <td>{{ s.branch || "-" }}</td>
              <td>{{ s.cgpa }}</td>
              <td>{{ s.graduation_year || "-" }}</td>
              <td>
                <span v-if="s.is_blacklisted" class="badge bg-dark">Blacklisted</span>
                <span v-else-if="!s.is_active" class="badge bg-secondary">Deactivated</span>
                <span v-else class="badge bg-success">Active</span>
              </td>
              <td class="text-end">
                <button class="btn btn-sm btn-outline-secondary me-1" @click="toggleStatus(s, 'is_active', !s.is_active)">
                  {{ s.is_active ? "Deactivate" : "Activate" }}
                </button>
                <button class="btn btn-sm btn-outline-dark" @click="toggleStatus(s, 'is_blacklisted', !s.is_blacklisted)">
                  {{ s.is_blacklisted ? "Unblacklist" : "Blacklist" }}
                </button>
              </td>
            </tr>
            <tr v-if="!students.length"><td colspan="7" class="text-center text-muted py-4">No students found</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";

export default {
  name: "AdminStudents",
  data() {
    return { students: [], q: "" };
  },
  created() {
    this.load();
  },
  methods: {
    async load() {
      const { data } = await api.get("/admin/students", { params: { q: this.q } });
      this.students = data.students;
    },
    async toggleStatus(s, field, value) {
      await api.patch(`/admin/users/${s.user_id}/status`, { [field]: value });
      this.$store.dispatch("notify", { message: "Status updated" });
      this.load();
    },
  },
};
</script>
