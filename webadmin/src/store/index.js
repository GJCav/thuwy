import Vue from 'vue';
import Vuex from 'vuex';
import config from '@/config';

import { getUserProfile } from '@/api/user';

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
    async refreshProfile(context) {
      let user = await getUserProfile();
      context.commit('setUser', user);
      return user;
    }
  },
  modules: {
  }
});
