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
          <v-list-item-title class="text-h6">物品预约</v-list-item-title>
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
    <!-- <tool-bar></tool-bar> -->
    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </div>
</template>

<script>
// import ToolBar from '@/components/ToolBar.vue';

export default {
  data() {
    return {
      drawer: true,
      mini: true,
      items: [
        {
          icon: 'mdi-home',
          title: '预约主页',
          to: '/rsv/home'
        },
        {
          icon: 'mdi-file',
          title: '物品',
          to: '/rsv/item',
        },
        {
          icon: 'mdi-certificate',
          title: '审批',
          to: '/rsv/reservation',
        },
        // {
        //   icon: 'mdi-account',
        //   title: '用户管理',
        //   to: '/user',
        // },
      ],
    };
  },
  // components: {
  //   ToolBar,
  // },
};
</script>