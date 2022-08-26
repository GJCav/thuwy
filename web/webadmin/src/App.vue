<template>
  <v-app>
    <v-app-bar app color="primary" dark clipped-left>
      <v-app-bar-nav-icon @click="navDrawerVisibility = true"></v-app-bar-nav-icon>
      <v-toolbar-title>微未央管理后台</v-toolbar-title>
    </v-app-bar>

    <v-navigation-drawer 
      v-model="navDrawerVisibility" 
      app clipped permane 
    >

      <!-- home page -->
      <v-list 
        nav dense 
        active-class="deep-purple--text text--accent-4"
      >
        <v-list-group
          no-action
          prepend-icon="home"
          value="true"
        >
          <template v-slot:activator>
            <v-list-item-title>Home</v-list-item-title>
          </template>

          <!-- <v-list-item link to="/" :disabled="!isLogin">
            <v-list-item-title>My Profile</v-list-item-title>
            <v-list-item-icon>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-icon>
          </v-list-item> -->

          <v-list-item link to="/login" class="text--lighten-2" :disabled="isLogin">
            <v-list-item-title>Login</v-list-item-title>
            <v-list-item-icon>
              <v-icon color="">mdi-login</v-icon>
            </v-list-item-icon>
          </v-list-item>

          <v-list-item link @click="logout" class="red--text text--lighten-2" :disabled="!isLogin">
            <v-list-item-title>Logout</v-list-item-title>
            <v-list-item-icon>
              <v-icon color="red">mdi-account</v-icon>
            </v-list-item-icon>
          </v-list-item>

        </v-list-group>
      </v-list>

      <!-- user management -->
      <v-list 
        nav dense 
        active-class="deep-purple--text text--accent-4"
      >
        <v-list-group
          no-action
          prepend-icon="mdi-account-circle"
          value="true"
        >
          <template v-slot:activator>
            <v-list-item-title>User</v-list-item-title>
          </template>

          <v-list-item link to="/userlist" :disabled="!hasPrivilege('UserAdmin')">
            <v-list-item-title>User List</v-list-item-title>
            <v-list-item-icon>
              <v-icon>mdi-card-account-mail-outline</v-icon>
            </v-list-item-icon>
          </v-list-item>

          <!-- <v-list-item link :disabled="!hasPrivilege('UserAdmin')">
            <v-list-item-title>Binding Info</v-list-item-title>
            <v-list-item-icon>
              <v-icon>mdi-link-variant</v-icon>
            </v-list-item-icon>
          </v-list-item> -->

          <v-list-item link to="/user_privilege" :disabled="!hasPrivilege('ScopeAdmin')">
            <v-list-item-title>User Privilege</v-list-item-title>
            <v-list-item-icon>
              <v-icon>mdi-key</v-icon>
            </v-list-item-icon>
          </v-list-item>

        </v-list-group>
      </v-list>

      <!-- group management -->
      <v-list 
        nav dense 
        active-class="deep-purple--text text--accent-4"
      >
        <v-list-group
          no-action
          prepend-icon="mdi-account-group"
          value="true"
        >
          <template v-slot:activator>
            <v-list-item-title>Group</v-list-item-title>
          </template>

          <v-list-item link to="/grouplist" :disabled="!hasPrivilege('ScopeAdmin')">
            <v-list-item-title>Management</v-list-item-title>
            <v-list-item-icon>
              <v-icon>mdi-file-tree</v-icon>
            </v-list-item-icon>
          </v-list-item>

          <!-- <v-list-item link :disabled="!hasPrivilege('ScopeAdmin')">
            <v-list-item-title>Group Privilege</v-list-item-title>
            <v-list-item-icon>
              <v-icon>mdi-key</v-icon>
            </v-list-item-icon>
          </v-list-item> -->

        </v-list-group>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'App',

  data: () => ({
  }),

  computed: {
    navDrawerVisibility: {
      get() { return this.$store.state.navDrawerVisibility; },
      set(vis) { this.$store.commit('setNavDrawerVisibility', vis); }
    },
    
    ...mapGetters(["isLogin", "allPrivileges"]),

    hasPrivilege() { return (scopeName) => {
      return this.$store.getters.allPrivileges.indexOf(scopeName) != -1;
    }},
  },

  methods: {
    logout() {
      localStorage.removeItem("session");
      this.$store.commit("setSession", "");
      this.$router.push("/login")
    },
  },

  mounted() {
    const session = this.$store.getters.session || localStorage.getItem("session");
    this.$store.dispatch("verifySession", { session }).then((r) => {
      if (!r) {
        this.$router.push("/login");
      }
    })
  },
};
</script>
