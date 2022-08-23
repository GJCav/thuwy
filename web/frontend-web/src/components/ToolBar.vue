<template>
  <div>
    <!-- <v-app-bar app color="cyan darken-4" dark> -->
    <v-app-bar app color="cyan darken-1">
      <router-link
        to="/"
        class="v-toolbar__content"
        style="text-decoration: none; color: white"
      >
        <div style="max-width: 54px" class="mr-3">
          <v-img to="/" :src="require('@/assets/wy_white.png')"></v-img>
        </div>
        <div class="text-h5">微未央</div>
      </router-link>

      <v-spacer></v-spacer>

      <v-btn to="/" plain>主页</v-btn>
      <v-btn to="/issue/" plain>答疑坊</v-btn>
      <v-btn to="/rsv/" plain>物品预约</v-btn>
      <v-btn to="/blog/" plain>博客</v-btn>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn to="/login/" icon v-bind="attrs" v-on="on">
            <v-icon>mdi-login</v-icon>
          </v-btn>
        </template>
        <span>{{ user ? "切换用户" : "登录" }}</span>
      </v-tooltip>

      <v-tooltip bottom v-if="user">
        <template v-slot:activator="{ on, attrs }">
          <v-btn to="/profile/" icon v-bind="attrs" v-on="on">
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>
        <span>用户信息</span>
      </v-tooltip>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  computed: {
    user() {
      return this.$store.state.user;
    },
  },
};
</script>