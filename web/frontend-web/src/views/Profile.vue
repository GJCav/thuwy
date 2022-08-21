<template>
  <v-main>
    <v-container>
      <v-col lg="6" offset-lg="3" cols="12" offset="0">
        <h1>个人信息页</h1>
        <!-- 展示个人基本信息 -->
        <v-form>
          <v-text-field></v-text-field>
          <v-text-field></v-text-field>
          <v-text-field></v-text-field>
        </v-form>
        <!-- 一些修改操作 -->
        <v-btn color="success">保存修改</v-btn>
        <v-btn color="error">用户解绑</v-btn>
      </v-col>
    </v-container>
  </v-main>
</template>

<script>
export default {
  name: 'Profile',
  computed: {
    user() {
      return this.$store.state.user;
    }
  }
};
</script>
