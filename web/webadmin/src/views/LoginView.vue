<template>
<v-card class="mx-auto" max-width="400px">
  <v-card-title class="elevation-10">
    <v-icon large left>mdi-login</v-icon>
    <h3>Login to thuwy</h3>
  </v-card-title>
  <v-img contain :src="qrcode_src"></v-img>
</v-card>
</template>

<script>
import { io } from "socket.io-client"
import { API_URL } from "../backend-api/url"

export default {
  name: "LoginView",
  data: () => ({
    qrcode_src: "https://picsum.photos/300/300?random",
  }),

  mounted() {
    const socket = io(API_URL + "/auth")
    const app = this;
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
  },
}


</script>
