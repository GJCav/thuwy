import Vue from 'vue';
import Vuex from 'vuex';
import config from '@/config';

import { getUserProfile } from '@/api/user';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    config,

    user: null,
    session: '',
    userPrivileges: [],
    groupPrivilegeInfo: {},

    snackbar: false,
    snackbarMsg: '',
    snackbarTimeout: -1
  },
  mutations: {
    setUser(state, payload) {
      state.user = payload;
      state.userPrivileges = payload?.privilege_info?.privileges;
      state.groupPrivilegeInfo = payload?.privilege_info?.group_privileges;
    },
    setSession(state, payload) {
      state.session = payload;
      localStorage.setItem('session', payload);
    },
    updateSnackbarStatus(state, payload) {
      state.snackbar = payload;
    },
    setSnackbarMessage(state, payload) {
      state.snackbarMsg = payload;
    },
    setSnackbarTimeout(state, payload) {
      state.snackbarTimeout = payload;
    }
  },
  actions: {
    async refreshProfile({ state, commit }) {
      let user = await getUserProfile(state.session);
      commit('setUser', user);
      return user;
    },
    showMessage(context, { message, timeout = -1 }) {
      context.commit('setSnackbarMessage', message);
      context.commit('setSnackbarTimeout', timeout);
      context.commit('updateSnackbarStatus', true);
    }
  },
  modules: {
  }
});
