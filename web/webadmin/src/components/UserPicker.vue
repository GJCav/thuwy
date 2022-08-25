<template>
<v-card v-bind="card_props">
  <v-card-title>
    已选择用户
  </v-card-title>
  <v-card-text class="text--primary pb-1">
    <v-row class="ma-0">
    <v-chip
      color="teal" outlined
      class="pr-1 mx-1"
      v-for="user in users"
      :key="user.name"
    >
      {{ user.name }}
      <v-btn icon small>
        <v-icon 
          small @click="unselect(user)"
        >mdi-close</v-icon>
      </v-btn>
    </v-chip>

    <v-spacer></v-spacer>
    <v-btn
      color="warning"
      @click="confirmDialog"
    >
      确认
    </v-btn>
    </v-row>
  </v-card-text>

  <!-- 确认选择 -->
  <v-card-text>
    <v-row class="justify-end mx-0 mb-2">
      
    </v-row>
  </v-card-text>

  <v-divider class="mb-2"></v-divider>

  <v-card-text class="text--primary">
    <!-- filters -->
    <v-row class="ma-0">
      <v-checkbox 
        hide-details 
        class="shrink mr-2" 
        v-model="filter_clazz"
        :disabled="loading"
      ></v-checkbox>
      <v-text-field 
        label="班级" 
        :disabled="(!filter_clazz) || loading"
        v-model="clazz"
        @keydown="pressEnterToUpdate"
      ></v-text-field>
    </v-row>
    <v-row class="ma-0">
      <v-checkbox 
        hide-details 
        class="shrink mr-2" 
        v-model="filter_name"
        :disabled="loading"
      ></v-checkbox>
      <v-text-field 
      label="姓名" 
      :disabled="(!filter_name) || loading"
      v-model="name"
      @keydown="pressEnterToUpdate"
    ></v-text-field>
    </v-row>
    <v-row class="mx-0 mt-0 mb-2 justify-end align-center">
      <v-btn 
        color="primary" small outlined
        @click="loadData"
        :disabled="loading"
      >
        Filter
      </v-btn>
    </v-row>

    <!-- tables -->
    <v-data-table
      :headers="table.headers"
      :items="table.items"
      item-key="name"
      :items-per-page="30"
      hide-default-footer
      loading-text="click SEARCH to load data"
    >
      <!-- 操作列 -->
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template v-slot:item.actions="{ item }">
        <v-btn 
          tile icon small
          color="secondary"
          @click="select(item)"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </template>
    </v-data-table>

    <!-- 错误警告窗口 -->
    <v-alert 
      type="error"
      v-model="error"
      dense dismissible
      transition="scroll-y-transition"
    >
      {{ errmsg }}
    </v-alert>
    
    <!-- 分页 -->
    <v-row class="mx-0 mb-4 mt-2 justify-end">
      <v-pagination 
        :length="page_count" 
        v-model="cur_page"
        @input="loadData()"
      ></v-pagination>
    </v-row>
  </v-card-text>
</v-card>
</template>

<script>
import * as auth from "../backend-api/auth"

export default {
  name: "UserPicker",

  props: {
    card_props: { type: Object, default: () => ({

    })},
    multi_select: { type: Boolean, default: false }
  },


  data: () => ({
    filter_name: false,
    name: "",
    filter_clazz: false,
    clazz: "",
    cur_page: 1,
    page_count: 1,

    loading: false,
    error: false,
    errmsg: "",

    users: [],

    table: {
      headers: [
        { text: "班级", value: "clazz" },
        { text: "姓名", value: "name" },
        { text: "学号", value: "school-id" },
        { text: "操作", value: "actions", sortable: false }
      ],
      items: [],
    },
  }),

  methods: {
    confirmDialog() {
      this.$emit("confirmSelect", this.users);
      this.users = [];
    },

    async loadData() {
      if (this.loading) return;
      this.loading = true;
      this.table.items = [];

      try {
        const data = await auth.fetchUserList({
          session: this.$store.getters.session,
          clazz: this.filter_clazz ? this.clazz : null,
          name: this.filter_name? this.name : null,
          p: this.cur_page
        })

        if (data.code !== 0) {
          throw new Error(data.errmsg);
        }

        this.table.items = data.profiles;
        this.page_count = data.page_count;
      } catch (e) {
        this.error = true;
        this.errmsg = e.message;
      }

      this.loading = false;
    },

    pressEnterToUpdate(keyEvent){
      if (keyEvent.key === "Enter") {
        this.loadData();
      }
    },

    indexOf(openid) {
      for(let i = 0;i < this.users.length;i++){
        if (openid == this.users[i].openid)
          return i;
      }
      return -1;
    },

    unselect(user) {
      const idx = this.indexOf(user.openid);
      if (idx >= 0 && idx < this.users.length){
        this.users.splice(idx, 1)
      }
    },

    select(user){
      const idx = this.indexOf(user.openid);
      if (idx == -1){
        if (this.multi_select) {
          this.users.push(user);
        } else {
          this.users = [user]
        }
      } else {
        this.error = true;
        this.errmsg = "该用户已被选择"
      }
    }
  },
}
</script>