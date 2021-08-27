<template>
  <v-dialog
    max-width="512px"
    @click:outside="$emit('input', false)"
    @input="$emit('input', false)"
    :value="show"
  >
    <v-card :loading="credential === ''">
      <v-card-title>请扫码登录</v-card-title>
      <v-img v-if="requestId !== ''" max-width="512px" :src="qrSrc"></v-img>
      <v-card-text v-else>正在拉取二维码……</v-card-text>
      <v-card-actions>
        <v-btn @click="establishWS" outlined rounded color="primary">
          <v-icon>mdi-refresh</v-icon>刷新
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { getUserProfile, Login } from '@/api/user';

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
        // setTimeout(() => {
        //   fetch(`${this.config.WSAddr}/weblogin`, {
        //     method: 'POST',
        //     headers: {
        //       Accept: 'application/json',
        //       'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({
        //       requestId: requestId,
        //       credential: `Credential is ${requestId}`,
        //     }),
        //   });
        // }, 1000);
        console.log('RequestId: %s', requestId);
      });

      this.ws.on('credential', async (credential) => {
        console.log('Credential: %s', credential);
        this.credential = credential;

        await Login(credential);
        let user = await getUserProfile();
        console.log(user);
      });
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