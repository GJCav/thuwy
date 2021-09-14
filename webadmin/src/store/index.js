import Vue from 'vue';
import Vuex from 'vuex';
import config from '@/config';

import { getUserProfile } from '@/api/user';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    config,
    user: null,
    snackbar: false,
    snackbarMsg: '',
    snackbarTimeout: -1
  },
  mutations: {
    setUser(state, payload) {
      state.user = payload;
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
    async refreshProfile(context) {
      let user = await getUserProfile();
      context.commit('setUser', user);
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
