<template>
  <v-row>
    <v-col lg="1" offset-lg="2" cols="12" offset="0">
      <v-btn @click="$router.push('/rsv/item/')" icon>
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
    </v-col>
    <v-col lg="6" cols="12" offset="0">
      <h1 class="text-h3 text-center">物品信息</h1>
      <br />
      <v-row class="justify-center">
        <v-btn-toggle v-if="user !== null && isAdmin">
          <v-btn :to="`/rsv/item/${this.id}/edit`" color="success" outlined
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
      <article v-if="item !== null">
        <v-row class="justify-center">
          <v-img :src="item.thumbnail" max-width="384px"></v-img>
        </v-row>
        <div class="text-h5">名称</div>
        <div class="subtitle-1">
          {{ item.name
          }}<v-chip outlined small class="ma-2" color="cyan" ripple>{{
            item.group
          }}</v-chip>
        </div>
        <br />

        <div class="text-h5">简介</div>
        <div class="subtitle-1">{{ item["brief-intro"] }}</div>
        <br />

        <div class="text-h5">详细信息</div>
        <div v-html="renderedHtml"></div>
        <br />

        <div class="text-h5">当前状态</div>
        <div class="subtitle-1">
          {{ item["available"] ? "可预约" : "不可预约" }}
        </div>
        <br />

        <div class="text-h5">特殊属性</div>
        <div class="subtitle-1" v-if="item['attr'] === 0">无</div>
        <ul class="subtitle-1">
          <li v-if="(item['attr'] & 0x1) > 0">自动通过审批</li>
        </ul>
        <br />

        <div class="text-h5">预约方式</div>
        <v-radio-group v-model="rsvMethod" row>
          <v-radio
            label="时间段预约"
            :disabled="!(item['rsv-method'] & 0x1)"
            value="1"
          ></v-radio>
          <v-radio
            label="灵活预约"
            :disabled="!(item['rsv-method'] & 0x2)"
            value="2"
          ></v-radio>
        </v-radio-group>
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
import { getItem, deleteItem } from '@/api/item';
import marked from 'marked';
import ConfirmBox from '@/components/ConfirmBox.vue';

export default {
  name: 'ItemInfo',
  data() {
    return {
      id: Number(this.$route.params.id),
      item: null,
      rsvMethod: 0,
      dialog: false,
      deleting: false,
    };
  },
  async mounted() {
    this.item = await getItem(this.id);
  },
  methods: {
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
            message: '删除成功',
            timeout: 2000,
          });
          this.$router.push('/rsv/item');
        }, 1000);
      }
    }
  },
  computed: {
    renderedHtml() {
      if (this.item) {
        return marked(this.item['md-intro']);
      }
      return '';
    },
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