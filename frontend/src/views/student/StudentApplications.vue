<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
      <h3 class="mb-0">My Applications</h3>
      <button class="btn btn-outline-primary" @click="exportCsv" :disabled="exporting">
        <i class="bi bi-download me-1"></i>
        {{ exporting ? "Exporting..." : "Export as CSV" }}
      </button>
    </div>

    <div v-if="exportMessage" class="alert alert-info py-2">
      {{ exportMessage }}
      <a v-if="downloadName" href="#" @click.prevent="download">Download file</a>
    </div>

    <div class="card">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead>
            <tr><th>Job Title</th><th>Company</th><th>Applied On</th><th>Interview</th><th>Status</th></tr>
          </thead>
          <tbody>
            <tr v-for="a in applications" :key="a.id">
              <td><strong>{{ a.job_title }}</strong></td>
              <td>{{ a.company_name }}</td>
              <td>{{ formatDate(a.application_date) }}</td>
              <td>{{ a.interview_datetime ? formatDate(a.interview_datetime) : "-" }}</td>
              <td><span class="badge badge-status" :class="statusClass(a.status)">{{ a.status }}</span></td>
            </tr>
            <tr v-if="!applications.length"><td colspan="5" class="text-center text-muted py-4">You haven't applied to any drives yet</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";

export default {
  name: "StudentApplications",
  data() {
    return { applications: [], exporting: false, exportMessage: "", downloadName: "", pollTimer: null };
  },
  created() {
    this.load();
  },
  beforeDestroy() {
    clearInterval(this.pollTimer);
  },
  methods: {
    async load() {
      const { data } = await api.get("/student/applications");
      this.applications = data.applications;
    },
    statusClass(s) {
      return { applied: "bg-secondary", shortlisted: "bg-info text-dark", selected: "bg-success", rejected: "bg-danger" }[s] || "bg-secondary";
    },
    formatDate(d) {
      return d ? new Date(d).toLocaleString() : "-";
    },
    async exportCsv() {
      this.exporting = true;
      this.exportMessage = "";
      this.downloadName = "";
      try {
        const { data } = await api.post("/student/export");
        this.exportMessage = "Export started. Preparing your file...";
        this.pollExport(data.task_id);
      } catch (e) {
        this.exporting = false;
        this.$store.dispatch("notify", { message: "Export failed to start", type: "error" });
      }
    },
    pollExport(taskId) {
      clearInterval(this.pollTimer);
      let attempts = 0;
      this.pollTimer = setInterval(async () => {
        attempts++;
        try {
          const { data } = await api.get(`/student/export/${taskId}`);
          if (data.state === "SUCCESS" && data.result && data.result.filename) {
            clearInterval(this.pollTimer);
            this.exporting = false;
            this.downloadName = data.result.filename;
            this.exportMessage = "Your CSV export is ready.";
            this.$store.dispatch("notify", { message: "Export complete!" });
          } else if (data.state === "FAILURE" || attempts > 20) {
            clearInterval(this.pollTimer);
            this.exporting = false;
            this.exportMessage = "Export could not be completed. Is the Celery worker running?";
          }
        } catch (e) {
          clearInterval(this.pollTimer);
          this.exporting = false;
        }
      }, 1500);
    },
    async download() {
      const res = await api.get(`/student/export/download/${this.downloadName}`, { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", this.downloadName);
      document.body.appendChild(link);
      link.click();
      link.remove();
    },
  },
};
</script>
