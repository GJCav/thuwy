<template>
  <v-row>
    <v-col lg="1" offset-lg="2" cols="12" offset="0">
      <v-btn @click="$router.back()" icon>
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
    </v-col>

    <v-col lg="6" cols="12" offset="0" v-if="item !== null"
      ><h1 class="text-h3 text-center">物品编辑</h1>
      <v-divider></v-divider>
      <v-row>
        <v-col cols="6">
          <v-switch
            v-model="item.available"
            :label="`${item.available ? '' : '不'}可预约`"
          ></v-switch>
          <br />

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

          <div class="text-h5">封面图</div>
          <v-btn
            block
            outlined
            @click="$refs.file.click()"
            :loading="uploading"
            :disabled="uploading"
            ><v-icon>mdi-cloud-upload-outline</v-icon>&nbsp;上传
          </v-btn>
          <input
            type="file"
            ref="file"
            style="display: none"
            @change="doUpload"
          />
          <v-text-field
            label="封面图URL"
            v-model="item.thumbnail"
          ></v-text-field>
          <v-img :src="item.thumbnail"></v-img>
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
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6">
          <v-textarea
            outlined
            label="详细信息（支持MarkDown）"
            v-model="item['md-intro']"
            auto-grow
          ></v-textarea>
          <br />
        </v-col>
        <v-col cols="6" v-html="renderedHtml"></v-col>
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
          <v-btn color="error" outlined :disabled="submitting">删除</v-btn>
        </v-btn-toggle>
      </v-row>
      <br />
    </v-col>
  </v-row>
</template>

<script>
import { getItem, postItem } from '@/api/item';
import { upload } from '@/api/file';
import marked from 'marked';

export default {
  name: 'ItemEdit',
  data() {
    return {
      id: Number(this.$route.params.id),
      item: null,
      uploading: false,
      submitting: false,
    };
  },
  async mounted() {
    this.item = await getItem(this.id);
    console.log(this.item);
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
    handler(e) {
      console.log(e);
    },
    async doPostItem() {
      this.submitting = true;
      try {
        await postItem(this.item);
      } catch (e) {
        this.submitting = false;
        throw e;
      }
      setTimeout(() => {
        this.$router.push(`/item/${this.item.id}`);
        this.submitting=false;
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
      this.item.thumbnail = url;
      e.target.value = '';
      this.uploading = false;
    },
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