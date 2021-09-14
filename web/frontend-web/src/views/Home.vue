<template>
  <v-col
    class="text-center"
    cols="12"
    sm="6"
    offset-sm="3"
    lg="4"
    offset-lg="4"
  >
    <v-row class="justify-center">
      <v-img :src="require('@/assets/wy_blue.png')" />
    </v-row>
    <h1>微未央（管理端）</h1>
    <br />
    <v-card color="blue lighten-5" class="rounded" elevation="12">
      <v-list-item two-line>
        <v-list-item-content v-if="user === null">
          <v-list-item-title class="text-h5">未登录</v-list-item-title>
          <v-list-item-subtitle>请点击右上角登录</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-content v-else>
          <v-list-item-title class="text-h5"
            >你好，{{ user.name
            }}<template v-if="user.admin"
              >（管理员）</template
            ></v-list-item-title
          >
          <v-list-item-subtitle
            >{{ user.clazz }} {{ user.id }}</v-list-item-subtitle
          >
        </v-list-item-content>
      </v-list-item>
    </v-card>
  </v-col>
</template>

<script>
export default {
  name: 'Home',
  computed: {
    user() {
      return this.$store.state.user;
    },
  },
};
</script>
