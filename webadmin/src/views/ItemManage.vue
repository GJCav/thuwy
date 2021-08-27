<template>
  <v-col lg="6" offset-lg="3" cols="12" offset="0">
    <h1>物品管理</h1>
    <v-card v-for="item in itemList" :key="item.key" style="margin-top: 20px">
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
            <v-btn class="ml-2 mt-5" color="error" outlined rounded small>
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
  </v-col>
</template>

<script>
import { getItemList } from '@/api/item';

export default {
  name: 'ItemManage',
  data() {
    return {
      itemList: [],
    };
  },
  async mounted() {
    this.itemList = await getItemList();
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
  color: unset;
}
</style>