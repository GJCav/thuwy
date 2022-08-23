<template>
  <!-- <v-app :style="{ backgroundImage: `url(${bg})` }"> -->
  <v-app>
    <tool-bar></tool-bar>
    <router-view />
    <v-snackbar
      dark
      color="deep-purple accent-1"
      app
      @input="$store.commit('updateSnackbarStatus', false)"
      :value="$store.state.snackbar"
      :timeout="$store.state.snackbarTimeout"
      ><b>{{ $store.state.snackbarMsg }}</b
      ><template
        v-if="$store.state.snackbarTimeout === -1"
        v-slot:action="{ attrs }"
      >
        <v-btn
          color="yellow yellow darken-1"
          text
          v-bind="attrs"
          @click="$store.commit('updateSnackbarStatus', false)"
          >关闭</v-btn
        >
      </template></v-snackbar
    >
    <div style="height: 128px"></div>
    <v-footer absolute style="background-color: #053239; height: 96px" dark>
      <v-row class="justify-center">
        @ {{ new Date().getFullYear() }}清华大学未央书院 微未央网站
      </v-row>
    </v-footer>
  </v-app>
</template>

<script>
import ToolBar from "@/components/ToolBar.vue";

export default {
  name: "App",

  data: () => ({
    bg: require("@/assets/bg.jpg"),
  }),
  created() {
    var session = localStorage.getItem("session");
    if (session) {
      this.$store.commit("setSession", session);
    }
    this.$store.dispatch("refreshProfile");
  },
  components: {
    ToolBar,
  },
};
</script>

<style scoped>
div[data-app="true"] {
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-color: #eeeeee;
}
</style>