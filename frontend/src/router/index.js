import { createRouter, createWebHistory } from "vue-router";
import store from "../store";

const routes = [
  { path: "/", name: "home", component: () => import("../views/HomeView.vue") },
  { path: "/login", name: "login", component: () => import("../views/LoginView.vue") },
  {
    path: "/register/student",
    component: () => import("../views/RegisterStudent.vue"),
  },
  {
    path: "/register/company",
    component: () => import("../views/RegisterCompany.vue"),
  },

  // Admin
  {
    path: "/admin",
    component: () => import("../views/admin/AdminDashboard.vue"),
    meta: { role: "admin" },
  },
  {
    path: "/admin/companies",
    component: () => import("../views/admin/AdminCompanies.vue"),
    meta: { role: "admin" },
  },
  {
    path: "/admin/students",
    component: () => import("../views/admin/AdminStudents.vue"),
    meta: { role: "admin" },
  },
  {
    path: "/admin/drives",
    component: () => import("../views/admin/AdminDrives.vue"),
    meta: { role: "admin" },
  },
  {
    path: "/admin/reports",
    component: () => import("../views/admin/AdminReports.vue"),
    meta: { role: "admin" },
  },

  // Company
  {
    path: "/company",
    component: () => import("../views/company/CompanyDashboard.vue"),
    meta: { role: "company" },
  },
  {
    path: "/company/drives",
    component: () => import("../views/company/CompanyDrives.vue"),
    meta: { role: "company" },
  },
  {
    path: "/company/drives/:id/applicants",
    component: () => import("../views/company/DriveApplicants.vue"),
    meta: { role: "company" },
  },
  {
    path: "/company/profile",
    component: () => import("../views/company/CompanyProfile.vue"),
    meta: { role: "company" },
  },

  // Student
  {
    path: "/student",
    component: () => import("../views/student/StudentDashboard.vue"),
    meta: { role: "student" },
  },
  {
    path: "/student/applications",
    component: () => import("../views/student/StudentApplications.vue"),
    meta: { role: "student" },
  },
  {
    path: "/student/profile",
    component: () => import("../views/student/StudentProfile.vue"),
    meta: { role: "student" },
  },

  { path: "/:pathMatch(.*)*", redirect: "/" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Role-based route guard.
router.beforeEach((to, from, next) => {
  const requiredRole = to.meta.role;
  if (!requiredRole) return next();

  if (!store.getters.isAuthenticated) {
    return next("/login");
  }
  if (store.getters.role !== requiredRole) {
    // Send the user to their own dashboard.
    return next("/" + store.getters.role);
  }
  next();
});

export default router;
