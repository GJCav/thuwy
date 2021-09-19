<template>
  <v-row>
    <v-col lg="1" offset-lg="2" cols="12" offset="0">
      <v-btn @click="$router.back()" icon>
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
    </v-col>

    <v-col lg="6" cols="12" offset="0" v-if="item !== null"
      ><h1 class="text-h3 text-center">
        <template v-if="createMode">新增物品</template>
        <template v-else>物品编辑</template>
      </h1>
      <v-divider></v-divider>
      <v-row>
        <v-col cols="7">
          <v-switch
            v-model="item.available"
            :label="`${item.available ? '' : '不'}可预约`"
          ></v-switch>
          <br />

          <div class="text-h5">预约方式</div>
          <v-row>
            <v-checkbox
              @change="
                $event
                  ? (item['rsv-method'] |= 0x1)
                  : (item['rsv-method'] &= ~0x1)
              "
              :input-value="(item['rsv-method'] & 0x1) !== 0"
              label="时间段预约"
            ></v-checkbox>
            <v-checkbox
              @change="
                $event
                  ? (item['rsv-method'] |= 0x2)
                  : (item['rsv-method'] &= ~0x2)
              "
              :input-value="(item['rsv-method'] & 0x2) !== 0"
              label="灵活预约"
            ></v-checkbox>
          </v-row>
          <br />

          <div class="text-h5">特殊属性</div>
          <v-row>
            <v-checkbox
              @change="$event ? (item['attr'] |= 0x1) : (item['attr'] &= ~0x1)"
              :input-value="(item['attr'] & 0x1) !== 0"
              label="自动通过审批"
            ></v-checkbox>
          </v-row>
          <br />

          <div class="text-h5">封面图</div>
          <v-btn
            block
            outlined
            @click="startUpload('thumbnail')"
            :loading="uploading"
            :disabled="uploading"
            ><v-icon>mdi-cloud-upload-outline</v-icon>&nbsp;上传</v-btn
          >
          <v-text-field
            label="封面图URL"
            v-model="item.thumbnail"
          ></v-text-field>
          <v-img :src="item.thumbnail" contain></v-img>
          <br />

          <v-text-field
            label="物品名称"
            outlined
            v-model="item.name"
          ></v-text-field>
          <br />

          <v-text-field
            label="简介"
            outlined
            v-model="item['brief-intro']"
          ></v-text-field>
          <br />

          <v-text-field
            label="物品分组"
            outlined
            v-model="item['group']"
          ></v-text-field>
          <br />
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="7">
          <v-textarea
            outlined
            label="详细信息（支持MarkDown）"
            v-model="item['md-intro']"
            auto-grow
            append-icon="mdi-image"
            @click:append="startUpload('textarea')"
          ></v-textarea>
          <br />
        </v-col>
        <v-col cols="5" v-html="renderedHtml"></v-col>
      </v-row>

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
      <br />
    </v-col>
    <confirm-box
      v-model="dialog"
      title="确认删除"
      text="该操作不可逆！"
      @confirm="confirmDelete"
    ></confirm-box>
    <input type="file" ref="file" style="display: none" @change="doUpload" />
  </v-row>
</template>

<script>
import { getItem, postItem, deleteItem } from '@/api/item';
import { upload } from '@/api/file';
import marked from 'marked';
import ConfirmBox from '@/components/ConfirmBox.vue';

export default {
  name: 'ItemEdit',
  data() {
    return {
      id: Number(this.$route.params.id),
      item: null,
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
      this.item = {
        name: '',
        available: true,
        'brief-intro': '',
        'md-intro': '',
        thumbnail: '',
        'rsv-method': '',
        group: '',
        attr: 0,
        id: 0,
      };
    } else {
      this.item = await getItem(this.id);
    }
  },
  computed: {
    renderedHtml() {
      if (this.item) {
        return marked(this.item['md-intro']);
      }
      return '';
    },
  },
  methods: {
    async doPostItem() {
      this.submitting = true;
      try {
        var itemId = await postItem(this.item);
      } catch (e) {
        this.submitting = false;
        throw e;
      }
      setTimeout(() => {
        this.submitting = false;
        this.$store.dispatch('showMessage', {
          message: '提交成功',
          timeout: 2000,
        });
        this.$router.push(`/item/${itemId}`);
      }, 1000);
    },
    async doUpload(e) {
      this.uploading = true;
      let file = e.target.files[0];
      try {
        var url = await upload(file);
      } catch (e) {
        this.uploading = false;
        throw e;
      }
      e.target.value = '';
      this.uploading = false;
      this.onUploadFinish(url);
    },
    async confirmDelete(confirm) {
      if (confirm) {
        this.deleting = true;
        try {
          await deleteItem(this.id);
        } catch (e) {
          this.deleting = false;
          throw e;
        }
        setTimeout(() => {
          this.deleting = false;
          this.$store.dispatch('showMessage', {
            message: '删除',
            timeout: 2000,
          });
          this.$router.push('/item');
        }, 1000);
      }
    },
    startUpload(type) {
      this.fileUploadType = type;
      this.$refs.file.click();
    },
    onUploadFinish(url) {
      if (this.fileUploadType === 'thumbnail') {
        this.item.thumbnail = url;
      } else if (this.fileUploadType === 'textarea') {
        this.item['md-intro'] += `![](${url})\n`;
      }
    },
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

.v-textarea {
  word-break: break-all;
}
</style>