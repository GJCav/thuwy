<template>
  <v-main>
    <v-container>
      <!-- <v-col
        class="text-center mt-9"
        cols="12"
        sm="10"
        offset-sm="1"
        xl="6"
        offset-xl="3"
      > -->
      <v-row class="justify-center">
        <v-col cols="3">
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
      <v-parallax src="@/assets/bg_welcome.jpg" class="elevation-15">
        <div class="text-center">
          <p
            class="text-h4 mt-8 font-weight-black"
            style="text-shadow: 3px 3px 3px black"
          >
            WELCOME TO
          </p>
          <h1
            class="text-h1 font-weight-black mb-4 white--text"
            style="text-shadow: 8px 8px 5px black"
          >
            微 未 央
          </h1>
          <p
            class="text-h4 mt-8 font-weight-black"
            style="text-shadow: 3px 3px 3px black"
          >
            清华大学未央书院的专属网站
          </p>
        </div>
      </v-parallax>
      <!-- Some New Notices -->
      <h1 class="my-10" style="text-align: center">最新通知</h1>
      <v-row>
        <v-col class="d-flex justify-center" v-for="notice in noticelist" :key="notice.id" lg="3" sm="6" cols="12">
          <v-card
            class="mx-5"
            max-width="400"
            data-aos="zoom-in"
            data-aos-anchor-placement="top-center"
            :data-aos-delay="notice.delay"
          >
            <v-img
              class="white--text align-end"
              height="200px"
              :src="notice.src"
            >
              <v-card-title>{{ notice.title }}</v-card-title>
            </v-img>
            <v-card-subtitle class="pb-0">{{
              notice.subtitle
            }}</v-card-subtitle>
            <v-card-text class="text--primary">
              {{ notice.content }}
            </v-card-text>
            <v-card-actions>
              <v-btn color="info" text> Learn more </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <v-col
        class="text-center mt-9"
        cols="12"
        sm="10"
        offset-sm="1"
        xl="6"
        offset-xl="3"
      >
        <div>
          <h1 class="my-10">更多功能</h1>
          <v-timeline>
            <v-timeline-item
              data-aos="zoom-in"
              data-aos-anchor-placement="top-bottom"
              color="cyan"
            >
              <v-hover>
                <template v-slot:default="{ hover }">
                  <v-card
                    :elevation="hover ? 24 : 6"
                    color="cyan lighten-2"
                    dark
                    ripple
                    to="/rsv/"
                    class="transition-swing"
                  >
                    <!-- <v-img
                      :src="require('@/assets/wy_white.png')"
                      class="white--text align-end"
                      gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                    > -->
                    <v-card-title class="text-h5"> 物品预约 </v-card-title>
                    <!-- </v-img> -->
                  </v-card>
                </template>
              </v-hover>
            </v-timeline-item>
            <v-timeline-item
              data-aos="zoom-in"
              data-aos-anchor-placement="top-bottom"
              color="cyan"
            >
              <v-hover>
                <template v-slot:default="{ hover }">
                  <v-card
                    :elevation="hover ? 24 : 6"
                    color="cyan lighten-2"
                    dark
                    ripple
                    to="/issue/"
                    class="transition-swing"
                  >
                    <!-- <v-img
                      :src="require('@/assets/wy_blue.png')"
                      class="white--text align-end"
                      gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                    > -->
                    <v-card-title class="text-h5"> 答疑坊 </v-card-title>
                    <!-- </v-img> -->
                  </v-card>
                </template>
              </v-hover>
            </v-timeline-item>
            <v-timeline-item
              data-aos="zoom-in"
              data-aos-anchor-placement="top-bottom"
              color="cyan"
            >
              <v-hover>
                <template v-slot:default="{ hover }">
                  <v-card
                    :elevation="hover ? 24 : 6"
                    color="cyan lighten-2"
                    dark
                    ripple
                    to="/user/"
                    class="transition-swing"
                  >
                    <!-- <v-img
                      :src="require('@/assets/wy_white.png')"
                      class="white--text align-end"
                      gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                    > -->
                    <v-card-title class="text-h5"> 用户管理后台 </v-card-title>
                    <!-- </v-img> -->
                  </v-card>
                </template>
              </v-hover>
            </v-timeline-item>
            <v-timeline-item
              data-aos="zoom-in"
              data-aos-anchor-placement="top-bottom"
              color="cyan"
            >
              <v-hover>
                <template v-slot:default="{ hover }">
                  <v-card
                    :elevation="hover ? 24 : 6"
                    color="cyan lighten-2"
                    dark
                    ripple
                    to="/profile/"
                    class="transition-swing"
                  >
                    <!-- <v-img
                      :src="require('@/assets/wy_blue.png')"
                      class="white--text align-end"
                      gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
                    > -->
                    <v-card-title class="text-h5"> 我的profile </v-card-title>
                    <!-- </v-img> -->
                  </v-card>
                </template>
              </v-hover>
            </v-timeline-item>
          </v-timeline>
        </div>
      </v-col>
    </v-container>
  </v-main>
</template>

<script>
import AOS from "aos";
export default {
  name: "Home",
  data: () => ({
    noticelist: [
      {
        id: 1,
        title: "New Notice 1",
        src: "https://cdn.vuetifyjs.com/images/cards/docks.jpg",
        content: "This is the content of the notice.Just for test.",
        delay: 0,
      },
      {
        id: 2,
        title: "New Notice 2",
        src: "https://cdn.vuetifyjs.com/images/cards/docks.jpg",
        content: "This is the content of the notice.Just for test.",
        delay: 200,
      },
      {
        id: 3,
        title: "New Notice 3",
        src: "https://cdn.vuetifyjs.com/images/cards/docks.jpg",
        content: "This is the content of the notice.Just for test.",
        delay: 400,
      },
      {
        id: 4,
        title: "New Notice 4",
        src: "https://cdn.vuetifyjs.com/images/cards/docks.jpg",
        content: "This is the content of the notice.Just for test.",
        delay: 600,
      },
    ],
  }),
  computed: {
    user() {
      return this.$store.state.user;
    },
  },
  async mounted() {
    AOS.init();
    await this.$store.dispatch('refreshProfile');
    if (!this.user) {
      this.$store.dispatch("showMessage", { message: "未登录", timeout: 2000 });
    }
    // setTimeout(() => {
    //   this.$router.push({ name: 'Login' });
    // }, 2000);
  },
};
</script>
