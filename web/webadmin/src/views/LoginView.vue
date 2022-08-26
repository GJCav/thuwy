<template>
<v-card class="mx-auto" max-width="400px">
  <v-card-title class="elevation-10">
    <v-icon large left>mdi-login</v-icon>
    <h3>Login to thuwy</h3>
  </v-card-title>

  <v-skeleton-loader type="image" v-if="qrcode_src == null"></v-skeleton-loader>
  <v-img contain :src="qrcode_src" v-else></v-img>
</v-card>
</template>

<script>
import { io } from "socket.io-client"
import { API_URL } from "../backend-api/url"

export default {
  name: "LoginView",
  data: () => ({
    qrcode_src: null,
  }),

  mounted() {
    const app = this;

    const session = this.$store.getters.session || localStorage.getItem("session");
    this.$store.dispatch("verifySession", { session }).then((r) => {
      if (r) { // 已经登陆，直接跳转到根
        this.$router.push("/");
      } else {
        const socket = io(API_URL + "/auth")
        socket.on("code", function(code){ 
          app.qrcode_src = API_URL + `/auth/qrcode/${code}/`
          console.log(code)
        })
        socket.on("session", function(session) {
          app.$store.dispatch("verifySession", { session })
            .then((isValid) => {
              if (isValid) {
                app.$router.push("/")
              } else {
                alert("登陆失败");
                location.reload();
              }
            })
        })
      }
    })
  },
}


</script>
