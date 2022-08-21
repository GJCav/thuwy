<template>
    <v-main>
      <v-container>
        <v-col
          class="text-center mt-9"
          cols="12"
          sm="10"
          offset-sm="1"
          xl="6"
          offset-xl="3"
        >
          <v-row class="justify-center">
            <v-col cols="6">
              <v-img :src="require('@/assets/wy_color.png')"></v-img>
            </v-col>
          </v-row>
          <br />
          <template v-if="user">
            <v-row class="justify-center">
              <v-card dark color="pink" hover>
                <v-card-title>欢迎回来，{{ user.name }}</v-card-title>
                <v-card-text
                  >班级：{{ user.clazz }} <br />
                  权限：{{ user.privilege_info.privileges.join(" ") }}<br />
                  OpenID：{{ user.openid }}</v-card-text
                >
              </v-card>
            </v-row>
            <br />
          </template>
          <v-row class="justify-center">
            <v-col cols="6">
              <v-hover>
                <template v-slot:default="{ hover }">
                  <v-card
                    :elevation="hover ? 24 : 6"
                    color="#008aa4"
                    dark
                    ripple
                    to="/rsv/"
                    class="transition-swing"
                  >
                    <v-img
                      :src="require('@/assets/wy_white.png')"
                      class="white--text align-end"
                      gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                    >
                      <v-card-title class="text-h5"> 物品预约 </v-card-title>
                    </v-img>
                  </v-card>
                </template>
              </v-hover>
            </v-col>
            <v-col cols="6">
              <v-hover>
                <template v-slot:default="{ hover }">
                  <v-card
                    :elevation="hover ? 24 : 6"
                    color="#c3f3fd"
                    dark
                    ripple
                    to="/issue/"
                    class="transition-swing"
                  >
                    <v-img
                      :src="require('@/assets/wy_blue.png')"
                      class="white--text align-end"
                      gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                    >
                      <v-card-title class="text-h5"> 答疑坊 </v-card-title>
                    </v-img>
                  </v-card>
                </template>
              </v-hover>
            </v-col>
            <v-col cols="6">
              <v-hover>
                <template v-slot:default="{ hover }">
                  <v-card
                    :elevation="hover ? 24 : 6"
                    color="#670875"
                    dark
                    ripple
                    to="/user/"
                    class="transition-swing"
                  >
                    <v-img
                      :src="require('@/assets/wy_white.png')"
                      class="white--text align-end"
                      gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                    >
                      <v-card-title class="text-h5">
                        用户管理后台
                      </v-card-title>
                    </v-img>
                  </v-card>
                </template>
              </v-hover>
            </v-col>
            <v-col cols="6">
              <v-hover>
                <template v-slot:default="{ hover }">
                  <v-card
                    :elevation="hover ? 24 : 6"
                    color="#abccdf"
                    dark
                    ripple
                    to="/profile/"
                    class="transition-swing"
                  >
                    <v-img
                      :src="require('@/assets/wy_blue.png')"
                      class="white--text align-end"
                      gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                    >
                      <v-card-title class="text-h5"> 我的profile </v-card-title>
                    </v-img>
                  </v-card>
                </template>
              </v-hover>
            </v-col>
          </v-row>
        </v-col>
      </v-container>
    </v-main>
</template>

<script>
export default {
  name: 'Home',
  computed: {
    user() {
      return this.$store.state.user;
    },
  },
  async mounted() {
    if (!this.user) {
      this.$store.dispatch('showMessage', { message: '未登录', timeout: 2000 });
    }
    // setTimeout(() => {
    //   this.$router.push({ name: 'Login' });
    // }, 2000);
  }
};
</script>
