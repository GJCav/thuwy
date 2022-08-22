import Vue from 'vue';
import Vuex from 'vuex';
import { fetchMyProfile } from "./backend-api/auth"
import * as auth from "./backend-api/auth"

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    appBarVisibility: true,
    navDrawerVisibility: false,

    sessionState: {
      session: "",
      login: false,
      profile: {
        clazz: null, email: null, name: null, openid: null
      },
      userPrivileges: [],
      groupPrivilegeInfo: {}
    },
  },
  
  getters: {
    isLogin(state) { 
      return state.sessionState.login; 
    },

    session(state) { return state.sessionState.session; },

    userProfile(state) { return state.sessionState.profile; },

    userPrivileges(state) { return state.sessionState.userPrivileges; },

    groupPrivilegeInfo(state) { return state.sessionState.groupPrivilegeInfo; },

    allPrivileges(state) { return auth.getAllPrivileges({
      privileges: state.sessionState.userPrivileges,
      group_privileges: state.sessionState.groupPrivilegeInfo
    })},
  },


  mutations: {
    setAppBarVisibility(state, vis) { state.appBarVisibility = vis; },
    
    setNavDrawerVisibility(state, vis) { state.navDrawerVisibility = vis; },
    
    setSession(state, key) { state.sessionState.session = key; },

    setLogin(state, v) { state.sessionState.login = v; },
    
    setProfile(state, key) {
      state.sessionState.profile.clazz  = key.clazz;
      state.sessionState.profile.email  = key.email;
      state.sessionState.profile.name   = key.name;
      state.sessionState.profile.openid = key.openid;
    },
    
    setUserPrivileges(state, privileges) { state.sessionState.userPrivileges = privileges; },

    setGroupPrivilegeInfo(state, priInfo) { state.sessionState.groupPrivilegeInfo = priInfo; },
  },


  actions: {
    /**
     * verify and set session key, if this key is valid, otherwise
     * clear session and reset session in localStorage.
     * @param { commit } 
     * @param { session, next } `session` will be verified and `next` is provided by router guard
     */
    async verifySession({ commit }, { session }) {
      console.log("balablala")

      const json = await fetchMyProfile({ session });
      if (json.code !== 0) {
        return false;
      }

      commit("setLogin", true)

      commit("setSession", session)
      localStorage.setItem("session", session)
      
      commit("setProfile", json);
      commit("setUserPrivileges", json.privilege_info.privileges)
      commit("setGroupPrivilegeInfo", json.privilege_info.group_privileges)
      
      return true;
    },
  },

  modules: {
  },
});
