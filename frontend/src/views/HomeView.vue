<template>
  <div>
    <div class="hero mb-4">
      <div class="row align-items-center">
        <div class="col-lg-8">
          <h1 class="display-5 fw-bold">Campus Placement Portal</h1>
          <p class="lead mb-4">
            One place for the institute, companies and students to manage
            recruitment drives, applications and selections.
          </p>
          <router-link to="/register/student" class="btn btn-light btn-lg me-2">
            <i class="bi bi-person-plus me-1"></i> I'm a Student
          </router-link>
          <router-link to="/register/company" class="btn btn-outline-light btn-lg">
            <i class="bi bi-building me-1"></i> I'm a Company
          </router-link>
        </div>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-md-4" v-for="f in features" :key="f.title">
        <div class="card h-100">
          <div class="card-body">
            <i class="bi me-2 text-primary" :class="f.icon" style="font-size: 1.6rem"></i>
            <h5 class="mt-2">{{ f.title }}</h5>
            <p class="text-muted mb-0">{{ f.text }}</p>
          </div>
        </div>
      </div>
    </div>

    <p class="text-center text-muted mt-4">
      Already have an account?
      <router-link to="/login">Login here</router-link>
    </p>
  </div>
</template>
<script>
export default{
    name:"HomeView",
    data() {
        return {
            features : [
                { icon: "bi-briefcase", title: "Placement Drives", text: "Companies post drives, admin approves, students apply." },
                { icon: "bi-funnel", title: "Eligibility Filtering", text: "Drives are matched to branch, CGPA and graduation year." },
                { icon: "bi-graph-up", title: "Reports & Tracking", text: "Live dashboards, placement statistics and history." },
            ]
        }
    },
    created(){
        if (this.$store.getters.isAuthenticated){
            this.$router.replace("/" + this.$store.getters.role)
        }
    }
}
</script>