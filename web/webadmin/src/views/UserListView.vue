<template>
<v-container grid-list-xs>
  <ErrorDialog :title="dialog.title" :msg="dialog.msg" v-model="dialog.enable"></ErrorDialog>

  <!-- 用户列表 -->
  <h1 class="mt-10">用户列表</h1>
  <v-divider class="mt-2 mb-4"></v-divider>

  <!-- filter -->
  <v-container class="mx-2">
    <v-row class="justify-space-between">
      <h3 class="d-inline-block">Filters:</h3>
    <v-btn 
      color="success" 
      @click="loadData"
      :loading="loadingData"
      :disabled="loadingData"
    >
      Search
    </v-btn>
    </v-row>
    <v-row class="mt-0">
      <v-checkbox hide-details class="shrink mr-2" v-model="filters.enableClazz"></v-checkbox>
      <v-text-field 
        label="班级" 
        :disabled="!filters.enableClazz"
        v-model="filters.clazz"
        @keydown="pressEnterToUpdate"
      ></v-text-field>
    </v-row>
    <v-row class="mt-0">
      <v-checkbox hide-details class="shrink mr-2" v-model="filters.enableName"></v-checkbox>
      <v-text-field 
      label="姓名" 
      :disabled="!filters.enableName"
      v-model="filters.name"
      @keydown="pressEnterToUpdate"
    ></v-text-field>
    </v-row>
  </v-container> 

  <!-- table -->
  <h3 class="mx-2">Uses: </h3>
  <v-data-table
    :headers="table.headers"
    :items="userProfileList"
    item-key="openid"
    loading="true"
    show-expand
    hide-default-footer
    loading-text="click SEARCH to load data"
  >
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template v-slot:item.openid="{ item }">
      <span 
        class="text--secondary" 
        style="width: 8em; display: inline-block; overflow: hidden; text-overflow: ellipsis;"
      >
        {{item.openid}}
      </span>
    </template>

    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length">
        <v-card class="ma-4" outlined>
          <v-card-title>{{item.name}}</v-card-title>
          <v-card-text class="text--primary">
            <p>OpenID: {{item.openid}}</p>
            <p>Class: {{item.clazz}}</p>
            <v-btn outlined color="primary" @click="jumpToScopeManagement(item)">管理权限</v-btn>
          </v-card-text>
        </v-card>
      </td>
    </template>
  </v-data-table>
  <v-divider></v-divider>
  <v-row class="mx-4 mt-2">
    <v-col class="d-flex justify-end py-0 pr-10" cols="6" offset="6">
      <v-pagination :length="table.pageCount" v-model="filters.p"></v-pagination>
    </v-col>
  </v-row>
</v-container>
</template>


<script>
import * as auth from "./../backend-api/auth"
import { mapGetters } from "vuex"
import ErrorDialog from "../components/ErrorDialog.vue"

export default {
  name: "UserListView",
  data: () => ({
    dialog: {
      enable: false,
      title: "Error",
      msg: ""
    },

    loadingData: false,

    filters: {
      enableClazz: false,
      enableName: false,
      clazz: null,
      name: null,
      p: 1
    },

    table: {
      headers: [
        { text: 'ID', value: 'openid', sortable: false },
        { text: '班级', value: 'clazz' },
        { text: '姓名', value: 'name' },
        { text: '学号', value: 'school-id' },
        { text: 'EMail', value: 'email' }
      ],
      pageCount: 1,
    },

    userProfileList: [],
  }),

  computed: {
    ...mapGetters(["userPrivileges", "groupPrivilegeInfo", "allPrivileges"])
  },

  methods: {
    openDialog({ title, msg }) {
      this.dialog = { title, msg, enable: true };
    },

    pressEnterToUpdate(keyEvent) {
      if (keyEvent.key === "Enter") {
        this.loadData();
      }
    },

    async loadData() {
      this.loadingData = true;

      const { filters } = this;

      try{
        const data = await auth.fetchUserList({ 
          session: this.$store.getters.session,
          clazz: filters.enableClazz ? filters.clazz : null,
          name: filters.enableName ? filters.name : null,
          p: filters.clazz
        })

        if (data.code !== 0){
          throw new Error(data.errmsg)
        }

        this.userProfileList = data.profiles;
        this.pageCount = data.page_count;
      } catch (e) {
        this.openDialog({ msg: e.message })
      }

      this.loadingData = false;
    },

    jumpToScopeManagement(item) {
      this.$router.push({
        name: "user_privilege",
        params: { initial_openid: item.openid }
      })
    }
  },

  components: { ErrorDialog }
}
</script>