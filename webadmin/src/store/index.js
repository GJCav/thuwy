import Vue from 'vue';
import Vuex from 'vuex';
import config from '@/config';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    config,
    user: null,
  },
  mutations: {
    setUser(state, payload) {
      state.user = payload;
    }
  },
  actions: {
  },
  modules: {
  }
});
