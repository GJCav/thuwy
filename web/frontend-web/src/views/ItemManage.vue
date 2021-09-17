<template>
  <v-col lg="6" offset-lg="3" cols="12" offset="0">
    <h1>物品管理</h1>
    <v-btn
      v-if="user !== null && user.admin"
      to="/item/0/edit"
      color="success"
      dark
      ><v-icon>mdi-plus</v-icon>新增物品</v-btn
    >
    <v-hover v-slot="{ hover }" v-for="item in itemList" :key="item.id">
      <v-card
        :elevation="hover ? 12 : 2"
        color="cyan lighten-5"
        style="margin-top: 50px"
        :class="{ 'on-hover': hover }"
      >
        <router-link :to="`/item/${item.id}`">
          <v-img
            :src="item.thumbnail"
            max-height="384px"
            class="white--text align-end"
          >
            <v-card-title
              style="font-weight: 700; text-shadow: 0 0 2px black"
              class="text-h5"
              v-text="item.name"
            ></v-card-title>
            <v-card-subtitle
              style="font-weight: 700; text-shadow: 0 0 1px black"
              v-text="item['brief-intro']"
            ></v-card-subtitle></v-img
        ></router-link>

        <v-expand-transition>
          <v-card-actions
            v-if="user !== null && user.admin"
            v-show="hover"
            style="padding: 0"
          >
            <v-btn
              :to="`/item/${item.id}/edit`"
              class="ml-3 mt-2 mb-2"
              outlined
              rounded
              color="success"
            >
              <v-icon small>mdi-pencil</v-icon>
              编辑
            </v-btn>
            <v-btn
              class="ml-3 mt-2 mb-2"
              color="error"
              outlined
              rounded
              @click="dialog = (itemToDelete = item.id) > 0"
              :loading="deleting && itemToDelete === item.id"
              :disabled="deleting && itemToDelete === item.id"
            >
              <v-icon small>mdi-trash-can-outline</v-icon>
              删除
            </v-btn>
          </v-card-actions>
        </v-expand-transition>
      </v-card>
    </v-hover>
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
        try {
          await deleteItem(this.itemToDelete);
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
  computed: {
    user() {
      return this.$store.state.user;
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

.v-card {
  transition: opacity 0.2s ease-in-out;
}

.v-card:not(.on-hover) {
  opacity: 0.6;
}
</style>