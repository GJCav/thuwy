<template>
  <div>
    <v-main>
      <v-container>
        <v-col
          class="text-center mt-9"
          cols="12"
          sm="8"
          offset-sm="2"
          xl="6"
          offset-xl="3"
        >
          <!-- <v-row class="justify-center">
            <v-col cols="8">
              <v-img :src="require('@/assets/wy_color.png')"></v-img>
            </v-col>
          </v-row>
          <br /> -->

          <v-card :loading="loginState === 'unlogged'" class="pl-5 pr-5">
            <v-card-title class="justify-center"> 登录到微未央 </v-card-title>

            <v-row class="justify-center" v-if="qrmode">
              <v-row class="justify-center ma-5" v-if="code !== ''">
                <v-img
                  style="max-width: 360px"
                  alt="正在拉取二维码……"
                  :src="qrSrc"
                ></v-img>
              </v-row>
              <div v-else>正在拉取二维码……</div>
            </v-row>
            <!-- </div> -->
            <v-card-text class="justify-center" v-else>
              <v-row class="justify-center">
                <v-form>
                  <v-text-field label="用户名" required></v-text-field>
                  <v-text-field label="密码" required></v-text-field>
                  <v-btn>登录</v-btn>
                </v-form>
              </v-row>
            </v-card-text>
            <v-row class="justify-center">
              <v-switch
                inset
                label="使用小程序码登录"
                v-model="qrmode"
              ></v-switch>
            </v-row>
          </v-card>
        </v-col>
      </v-container>
    </v-main>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      qrmode: true,
      ws: null,
      code: '',
      config: this.$store.state.config,
      loginState: 'unlogged',
    };
  },
  methods: {
    async establishWS() {
      this.requestId = this.credential = '';
      if (this.ws !== null) {
        this.ws.disconnect();
      }
      // eslint-disable-next-line no-undef
      this.ws = io(this.config.BackAPIAddr + '/auth');

      this.ws.on('code', code => { this.code = code; console.log(code); });

      this.ws.on('session', session => {
        this.$store.commit('setSession', session);
        this.doLogin();
      });
    },
    async doLogin() {
      try {
        await this.$store.dispatch('refreshProfile');
        this.loginState = 'success';
        this.$store.dispatch('showMessage', {
          message: '登录成功',
          timeout: 2000,
        });
        setTimeout(() => {
          this.$router.push('/');
        }, 2000);
      } catch (e) {
        this.loginState = 'fail';
        throw e;
      }
    },
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
    qrSrc() {
      return `${this.config.BackAPIAddr}/auth/qrcode/${this.code}`;
    },
  },
  async mounted() {
    return this.establishWS();
  },
  async beforeMount() {
    if (this.ws !== null) {
      this.ws.disconnect();
    }
  },
};
</script>
