<template>
  <div>
    <h3 class="mb-4">Placement Reports</h3>

    <div class="row g-3 mb-4">
      <div class="col-md-7">
        <div class="card h-100">
          <div class="card-body">
            <h6 class="text-muted mb-3">Applications by Status</h6>
            <BarChart :labels="statusLabels" :values="statusValues" label="Applications" color="#2563eb" />
          </div>
        </div>
      </div>
      <div class="col-md-5">
        <div class="card h-100">
          <div class="card-body">
            <h6 class="text-muted mb-3">Selections by Branch</h6>
            <BarChart v-if="branchLabels.length" :labels="branchLabels" :values="branchValues" label="Selected" color="#16a34a" />
            <p v-else class="text-muted">No selections yet.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-body">
        <h6 class="text-muted mb-3">Top Drives by Applicants</h6>
        <table class="table mb-0">
          <thead><tr><th>Job Title</th><th>Company</th><th class="text-end">Applicants</th></tr></thead>
          <tbody>
            <tr v-for="(d, i) in report.top_drives" :key="i">
              <td>{{ d.job_title }}</td><td>{{ d.company }}</td><td class="text-end">{{ d.applicants }}</td>
            </tr>
            <tr v-if="!report.top_drives || !report.top_drives.length">
              <td colspan="3" class="text-center text-muted py-3">No data</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../../services/api";
import BarChart from "../../components/BarChart.vue";

export default {
  name: "AdminReports",
  components: { BarChart },
  data() {
    return { report: { status_counts: {}, branch_selected: {}, top_drives: [] } };
  },
  computed: {
    statusLabels() {
      return Object.keys(this.report.status_counts || {});
    },
    statusValues() {
      return Object.values(this.report.status_counts || {});
    },
    branchLabels() {
      return Object.keys(this.report.branch_selected || {});
    },
    branchValues() {
      return Object.values(this.report.branch_selected || {});
    },
  },
  async created() {
    const { data } = await api.get("/admin/reports");
    this.report = data;
  },
};
</script>
