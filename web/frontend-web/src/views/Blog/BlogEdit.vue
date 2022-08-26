<template>
  <v-row class="mt-3">
    <v-col lg="1" offset-lg="2" cols="12" offset="0">
      <v-btn @click="$router.back()" icon>
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
    </v-col>

    <v-col lg="6" cols="12" offset="0"
      ><h1 class="text-h3 text-center">
        <template v-if="createMode">发表博客</template>
        <template v-else>博客编辑（ID={{ id }}）</template>
      </h1>
      <br/>
      <v-row class="justify-center">
        <v-btn-toggle>
          <v-btn @click="$router.back()" outlined :disabled="submitting"
            >返回</v-btn
          >
          <v-btn
            @click="doPostItem"
            color="primary"
            outlined
            :loading="submitting"
            :disabled="submitting"
            >提交</v-btn
          >
          <v-btn
            color="error"
            outlined
            :disabled="deleting || submitting"
            @click="dialog = true"
            :loading="deleting"
            >删除</v-btn
          >
        </v-btn-toggle>
      </v-row>
      <br/>
      <v-divider></v-divider>
      <editor></editor>
      <confirm-box
        v-model="dialog"
        title="确认删除"
        text="该操作不可逆！"
        @confirm="confirmDelete"
      ></confirm-box>
    </v-col>
  </v-row>
</template>

<script>
import Editor from '@/components/Issue/Editor.vue';
import ConfirmBox from '@/components/ConfirmBox.vue';

export default {
  name: 'ItemEdit',
  data() {
    return {
      id: Number(this.$route.params.id),
      blog: null,
      uploading: false,
      submitting: false,
      createMode: false,
      dialog: false,
      deleting: false,
      fileUploadType: '',
    };
  },
  async mounted() {
    if (this.id === 0) {
      this.createMode = true;
    }
  },
  methods: {
    async doPostItem() {
      this.submitting = true;
      setTimeout(() => {
        this.submitting = false;
        this.$store.dispatch('showMessage', {
          message: '提交成功',
          timeout: 2000,
        });
        this.$router.push(`/blog/${this.id}/`);
      }, 1000);
    },
    async confirmDelete(confirm) {
      if (confirm) {
        this.deleting = true;
        setTimeout(() => {
          this.deleting = false;
          this.$store.dispatch('showMessage', {
            message: '删除',
            timeout: 2000,
          });
          this.$router.push('/blog/');
        }, 1000);
      }
    },
    startUpload(type) {
      this.fileUploadType = type;
      this.$refs.file.click();
    },
  },
  components: {
    ConfirmBox,
    Editor
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

.v-textarea {
  word-break: break-all;
}
</style>