import { createStore } from "vuex";

const store = createStore({
  state: {
    token: localStorage.getItem("ppa_token") || "",
    user: JSON.parse(localStorage.getItem("ppa_user") || "null"),
    toast: null,
  },
  getters: {
    isAuthenticated: (s) => !!s.token,
    role: (s) => (s.user ? s.user.role : null),
  },
  mutations: {
    setAuth(state, { token, user }) {
      state.token = token;
      state.user = user;
      localStorage.setItem("ppa_token", token);
      localStorage.setItem("ppa_user", JSON.stringify(user));
    },
    clearAuth(state) {
      state.token = "";
      state.user = null;
      localStorage.removeItem("ppa_token");
      localStorage.removeItem("ppa_user");
    },
    setToast(state, toast) {
      state.toast = toast;
    },
  },
  actions: {
    login({ commit }, payload) {
      commit("setAuth", payload);
    },
    logout({ commit }) {
      commit("clearAuth");
    },
    notify({ commit }, { message, type = "success" }) {
      commit("setToast", { message, type, id: Date.now() });
    },
  },
});

export default store;
