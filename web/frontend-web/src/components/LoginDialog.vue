<template>
  <v-dialog
    max-width="512px"
    @input="$emit('input', false)"
    :value="show"
    persistent
  >
    <v-card :loading="loginState !== 'success' && loginState !== 'fail'">
      <v-card-title>请扫码登录</v-card-title>
      <v-card-subtitle>「微未央」-「管理」-「右上角扫码」</v-card-subtitle>
      <v-img v-if="requestId !== ''" max-width="512px" :src="qrSrc"></v-img>
      <v-card-text v-else>正在拉取二维码……</v-card-text>
      <v-card-text v-if="loginState === 'success'" class="text-center"
        >登录成功！</v-card-text
      >
      <v-card-text v-if="loginState === 'fail'" class="text-center"
        >登录失败，请刷新重试</v-card-text
      >
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="establishWS" outlined rounded color="primary">
          <v-icon>mdi-refresh</v-icon>刷新
        </v-btn>
        <v-btn @click="$emit('input', false)" outlined rounded color="red">
          <v-icon>mdi-close</v-icon>关闭
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { Login } from '@/api/user';

export default {
  props: {
    show: Boolean,
  },
  model: {
    prop: 'show',
    event: 'input',
  },
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

        this.doLogin();
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
        setTimeout(() => {
          this.$emit('input', false);
        }, 2000);
      } catch (e) {
        this.loginState = 'fail';
        throw e;
      }
    },
  },
  computed: {
    qrSrc() {
      return `${this.config.ServerAddr}/qr/${this.requestId}`;
    },
  },
  async mounted() {
    this.establishWS();
  },
  async beforeDestroy() {
    if (this.ws !== null) {
      this.ws.disconnect();
    }
  },
};
</script>