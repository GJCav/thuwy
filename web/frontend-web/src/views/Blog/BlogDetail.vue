<template>
  <v-row class="mt-3">
    <v-col lg="1" offset-lg="2" cols="12" offset="0">
      <v-btn @click="$router.push('/blog/')" icon>
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
    </v-col>
    <v-col lg="6" cols="12" offset="0">
      <h1 class="text-h3 text-center">文章标题（ID={{id}}）</h1>
      <br />
      <v-row class="justify-center">
        <v-btn-toggle v-if="user !== null && isAdmin">
          <v-btn :to="`/blog/${this.id}/edit`" color="success" outlined
            ><v-icon dense color="success">mdi-pencil</v-icon>编辑</v-btn
          >
          <v-btn
            color="error"
            outlined
            @click="dialog = true"
            :loading="deleting"
            :disabled="deleting"
            ><v-icon dense color="error">mdi-trash-can-outline</v-icon
            >删除</v-btn
          >
        </v-btn-toggle>
      </v-row>
      <br />
      <v-divider></v-divider>
      <article>
        <p>正文正文正文正文正文正文正文正文正文正文正文正文</p>
      </article>
      <br />
    </v-col>
    <confirm-box
      v-model="dialog"
      title="确认删除"
      text="该操作不可逆！"
      @confirm="confirmDelete"
    ></confirm-box>
  </v-row>
</template>

<script>
import ConfirmBox from '@/components/ConfirmBox.vue';

export default {
  name: 'BlogDetail',
  data() {
    return {
      id: Number(this.$route.params.id),
      blog: null,
      dialog: false,
      deleting: false,
    };
  },
  methods: {
    async confirmDelete(confirm) {
      if (confirm) {
        this.deleting = true;
        setTimeout(() => {
          this.deleting = false;
          this.$store.dispatch('showMessage', {
            message: '删除成功',
            timeout: 2000,
          });
          this.$router.push('/blog/');
        }, 1000);
      }
    }
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
    isAdmin() {
      return this.$store.state.userPrivileges?.indexOf('admin') > -1;
    }
  },
  components: {
    ConfirmBox,
  },
};
</script>

<style scoped>
.v-divider {
  margin-top: 10px;
  margin-bottom: 30px;
}

a {
  text-decoration: none;
  color: unset;
}
</style>