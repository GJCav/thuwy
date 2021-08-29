<template>
  <v-col lg="6" offset-lg="3" cols="12" offset="0">
    <h1>物品管理</h1>
    <v-btn to="/item/0/edit" color="success" dark>新增物品</v-btn>
    <v-card v-for="item in itemList" :key="item.id" style="margin-top: 20px">
      <div class="d-flex flex-no-wrap justify-space-between">
        <div>
          <router-link :to="`/item/${item.id}`">
            <v-card-title class="text-h5" v-text="item.name"></v-card-title>
            <v-card-subtitle v-text="item['brief-intro']"></v-card-subtitle
          ></router-link>

          <v-card-actions>
            <v-btn
              :to="`/item/${item.id}/edit`"
              class="ml-2 mt-5"
              outlined
              rounded
              small
              color="success"
            >
              <v-icon small>mdi-pencil</v-icon>
              编辑
            </v-btn>
            <v-btn
              class="ml-2 mt-5"
              color="error"
              outlined
              rounded
              small
              @click="dialog = (itemToDelete = item.id) > 0"
              :loading="deleting && itemToDelete === item.id"
              :disabled="deleting && itemToDelete === item.id"
            >
              <v-icon small>mdi-trash-can-outline</v-icon>
              删除
            </v-btn>
          </v-card-actions>
        </div>

        <v-avatar class="ma-3" size="125" tile>
          <v-img :src="item.thumbnail"></v-img>
        </v-avatar>
      </div>
    </v-card>
    <!-- <v-pagination @next="turnPage(1)" @previous="turnPage(2)"></v-pagination> -->
    <confirm-box
      v-model="dialog"
      title="确认删除"
      text="该操作不可逆！"
      @confirm="confirmDelete"
    ></confirm-box>
  </v-col>
</template>

<script>
import { getItemList, deleteItem } from '@/api/item';
import ConfirmBox from '@/components/ConfirmBox.vue';

export default {
  name: 'ItemManage',
  data() {
    return {
      itemList: [],
      itemToDelete: null,
      dialog: false,
      deleting: false,
    };
  },
  async mounted() {
    this.loadItemList();
  },
  methods: {
    async loadItemList() {
      this.itemList = await getItemList();
    },
    async confirmDelete(confirm) {
      if (confirm) {
        this.deleting = true;
        await deleteItem(this.itemToDelete);
        setTimeout(() => {
          this.deleting = false;
          this.loadItemList();
        }, 1000);
      }
    },
    async turnPage(type) {
      if (type == 1) {
        if (this.itemList.length < 20) {
          return;
        }
        this.page++;
      } else {
        if (this.page === 1) {
          return;
        }
        this.page--;
      }
      return this.loadItemList();
    },
  },
  components: {
    ConfirmBox,
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
  color: unset;
}
</style>