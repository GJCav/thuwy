<template>
  <div>
    <v-navigation-drawer
      app
      permanent
      v-model="drawer"
      expand-on-hover
      :mini-variant.sync="mini"
      color="cyan darken-2"
      dark
    >
      <v-list-item class="px-2">
        <v-list-item-avatar>
          <v-img :src="require('@/assets/wy_white.png')"></v-img>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title class="text-h6"
            >微未央</v-list-item-title
          >
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item v-for="item in items" :key="item.title" :to="item.to" link>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar app color="cyan darken-4" dark>
      <!-- <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon> -->
      <div class="text-h5">微未央</div>

      <v-spacer></v-spacer>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn @click="dialog = true" icon v-bind="attrs" v-on="on">
            <v-icon v-if="user === null">mdi-account</v-icon>
            <v-icon v-else>mdi-login</v-icon>
          </v-btn>
        </template>
        <span v-if="user === null">登录</span>
        <span v-else>切换用户</span>
      </v-tooltip>
    </v-app-bar>
    <login-dialog v-if="dialog" v-model="dialog"></login-dialog>
  </div>
</template>

<script>
import LoginDialog from './LoginDialog.vue';

export default {
  data() {
    return {
      drawer: true,
      mini: true,
      dialog: false,
      items: [
        {
          icon: 'mdi-home',
          title: '主页',
          to: '/',
        },
        {
          icon: 'mdi-file',
          title: '物品管理',
          to: '/item',
        },
        {
          icon: 'mdi-certificate',
          title: '预约审批',
          to: '/reservation',
        },
        {
          icon: 'mdi-account',
          title: '用户管理',
          to: '/user',
        },
      ],
    };
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
  },
  components: {
    LoginDialog,
  },
};
</script>