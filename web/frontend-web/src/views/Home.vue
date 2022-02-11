<template>
  <v-col
    class="text-center mt-9"
    cols="12"
    sm="6"
    offset-sm="3"
    xl="4"
    offset-xl="4"
  >
    <v-row class="justify-center">
      <v-col cols="8">
        <v-img :src="require('@/assets/wy_color.png')"></v-img>
      </v-col>
    </v-row>
    <br />

    <v-card
      v-if="user === null"
      :loading="loginState !== 'success' && loginState !== 'fail'"
    >
      <v-card-text>
        <row class="justify-center">
          <v-col>
            <v-img v-if="requestId !== ''" :src="qrSrc"></v-img>
            <div v-else>正在拉取二维码……</div>
            <div class="text-h5">请扫码登录</div>
            <div>「微未央」-「管理」-「右上角扫码」</div>
          </v-col>
        </row>
      </v-card-text>
      <v-card-text v-if="loginState === 'success'" class="text-center"
        >登录成功！</v-card-text
      >
      <v-card-text v-if="loginState === 'fail'" class="text-center"
        >登录失败，请刷新重试</v-card-text
      >
    </v-card>
    <v-card v-else color="blue lighten-5" class="rounded" elevation="12" ripple>
      <v-list-item two-line>
        <v-list-item-content>
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
import { Login } from '@/api/user';

export default {
  name: 'Home',
  data() {
    return {
      ws: null,
      requestId: '',
      credential: '',
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
      this.ws = io(this.config.WSAddr);

      this.ws.on('connect', () => {
        this.ws.emit('getRequestId');
        console.log('connected');
      });

      this.ws.on('requestId', (requestId) => {
        this.requestId = requestId;
        console.log('RequestId: %s', requestId);
        this.loginState = 'logging';
      });

      this.ws.on('credential', async (credential) => {
        console.log('Credential: %s', credential);
        this.credential = credential;
        return this.doLogin();
      });
    },
    async doLogin() {
      try {
        await Login(this.credential);
        await this.$store.dispatch('refreshProfile');
        this.loginState = 'success';
        this.$store.dispatch('showMessage', {
          message: '登录成功',
          timeout: 2000,
        });
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
      return `${this.config.ServerAddr}/qr/${this.requestId}`;
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
