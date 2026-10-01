<template>
  <div>
    <router-link to="/company/drives" class="btn btn-sm btn-link px-0 mb-2">
      <i class="bi bi-arrow-left"></i> Back to drives
    </router-link>
    <h3 class="mb-1">{{ drive.job_title }}</h3>
    <p class="text-muted">{{ applications.length }} applicant(s)</p>

    <div class="card">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr><th>Student</th><th>Branch</th><th>CGPA</th><th>Applied</th><th>Status</th><th>Interview</th><th class="text-end">Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="a in applications" :key="a.id">
              <td><strong>{{ a.student_name }}</strong><br /><small class="text-muted">{{ a.student_email }}</small></td>
              <td>{{ a.student_branch || "-" }}</td>
              <td>{{ a.student_cgpa }}</td>
              <td>{{ formatDate(a.application_date) }}</td>
              <td><span class="badge badge-status" :class="statusClass(a.status)">{{ a.status }}</span></td>
              <td>
                <small>{{ a.interview_datetime ? formatDate(a.interview_datetime) : "-" }}</small>
              </td>
              <td class="text-end">
                <div class="btn-group btn-group-sm">
                  <button class="btn btn-outline-info" @click="setStatus(a, 'shortlisted')">Shortlist</button>
                  <button class="btn btn-outline-success" @click="setStatus(a, 'selected')">Select</button>
                  <button class="btn btn-outline-danger" @click="setStatus(a, 'rejected')">Reject</button>
                </div>
                <button class="btn btn-sm btn-outline-secondary ms-1" @click="scheduleInterview(a)">
                  <i class="bi bi-calendar-event"></i>
                </button>
              </td>
            </tr>
            <tr v-if="!applications.length"><td colspan="7" class="text-center text-muted py-4">No applicants yet</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";

export default {
  name: "DriveApplicants",
  data() {
    return { drive: {}, applications: [] };
  },
  created() {
    this.load();
  },
  methods: {
    async load() {
      const { data } = await api.get(`/company/drives/${this.$route.params.id}/applications`);
      this.drive = data.drive;
      this.applications = data.applications;
    },
    statusClass(s) {
      return { applied: "bg-secondary", shortlisted: "bg-info text-dark", selected: "bg-success", rejected: "bg-danger" }[s] || "bg-secondary";
    },
    formatDate(d) {
      return d ? new Date(d).toLocaleString() : "-";
    },
    async setStatus(a, status) {
      await api.patch(`/company/applications/${a.id}`, { status });
      this.$store.dispatch("notify", { message: `Marked as ${status}` });
      this.load();
    },
    async scheduleInterview(a) {
      const value = prompt("Interview date/time (YYYY-MM-DDTHH:MM):", "2026-07-01T10:00");
      if (!value) return;
      try {
        await api.patch(`/company/applications/${a.id}`, { interview_datetime: value });
        this.$store.dispatch("notify", { message: "Interview scheduled" });
        this.load();
      } catch (e) {
        this.$store.dispatch("notify", { message: e.response?.data?.message || "Invalid date", type: "error" });
      }
    },
  },
};
</script>
