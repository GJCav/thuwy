<template>
<v-container grid-list-xs>
  <ErrorDialog :title="dialog.title" :msg="dialog.msg" v-model="dialog.enable"></ErrorDialog>

  <!-- 用户组列表 -->
  <h1 class="mt-10">用户组列表</h1>
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
      <v-checkbox hide-details class="shrink mr-2" v-model="filters.enableRegex"></v-checkbox>
      <v-text-field 
      label="组名 (支持正则表达式)" 
      :disabled="!filters.enableRegex"
      v-model="filters.regex"
      @keydown="pressEnterToUpdate"
    ></v-text-field>
    </v-row>
  </v-container> 

  <!-- table -->
  <v-data-table
    :headers="table.headers"
    :items="group_list"
    item-key="name"
    loading="true"
    show-expand :items-per-page="30"
    hide-default-footer
    loading-text="click SEARCH to load data"
  >
    <!-- 表标题位置 -->
    <template v-slot:top>
      <v-toolbar flat color="white">
        <h3>Group List:</h3>
        <v-spacer></v-spacer>
        <v-dialog max-width="768px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn 
              small color="primary" 
              outlined icon 
              v-bind="attrs" v-on="on"
              :loading="add_group.loading"
              :disabled="false"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
          <!-- 添加 Group 对话框  -->
          <v-card>
            <v-card-title><span class="headline">新建组</span></v-card-title>
            <v-divider class="mb-4"></v-divider>
            <v-card-text class="text--primary py-0">
              <v-text-field
                v-model="add_group.name"
                label="Group Name"
                prepend-icon="mdi-pencil"
                clearable
              ></v-text-field>
              <v-menu
                v-model="add_group.date_picker.show"
                :disabled="!add_group.date_picker.enable"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-row class="ma-0">
                    <v-text-field
                      v-model="add_group.date_picker.date"
                      label="Expire Date"
                      prepend-icon="event"
                      readonly 
                      v-bind="attrs"
                      v-on="on"
                      :disabled="!add_group.date_picker.enable"
                    ></v-text-field>
                    <v-checkbox
                      v-model="add_group.date_picker.enable"
                    ></v-checkbox>
                  </v-row>
                </template>
                <v-date-picker
                  locale="zh-cn"
                  v-model="add_group.date_picker.date"
                  @input="add_group.date_picker.show = false"
                ></v-date-picker>
              </v-menu>

            </v-card-text>
            <v-card-actions class="">
              <v-spacer></v-spacer>
              <v-btn 
                color="warning" 
                @click="addGroup"
                :loading="add_group.loading"
                :disabled="add_group.loading"
              >
                Confirm
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>

    <!-- 到期时间列 -->
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template v-slot:item.expire_at="{ item }">
      <span v-if="item.expire_at == 0">长期有效</span>
      <span v-else>{{ (new Date(item.expire_at)).toLocaleString() }}</span>
    </template>

    <!-- 操作列  -->
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template v-slot:item.actions="{ item }">
      <v-menu :offset-y="true" transition="scroll-y-transition">
        <template v-slot:activator="{ on, attrs }">
          <v-btn 
            tile icon small
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>

        <v-btn color="error" @click="delGroup(item)">
          Sure to delete?
        </v-btn>
      </v-menu>
    </template>

    <!-- 展开列 -->
    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length">
        <GroupManager :group_name="item.name"></GroupManager>
      </td>
    </template>
  </v-data-table>
  <v-divider></v-divider>
  <v-row class="mx-4 mt-2">
    <v-col class="d-flex justify-end py-0 pr-10" cols="6" offset="6">
      <v-pagination 
        :length="table.pageCount" 
        v-model="filters.p"
        @input="loadData()"
      ></v-pagination>
    </v-col>
  </v-row>
</v-container>
</template>


<script>
import * as auth from "./../backend-api/auth"
import { mapGetters } from "vuex"
import ErrorDialog from "../components/ErrorDialog.vue"
import GroupManager from "../components/GroupManager.vue"

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
      enableRegex: false,
      regex: null,
      p: 1
    },

    add_group: {
      loading: false,
      name: "",
      date_picker: {
        show: false,
        enable: true,
        date: ""
      }
    },

    table: {
      headers: [
        { text: "ID", value: "id" },
        { text: "组名", value: "name" },
        { text: "到期时间", value: "expire_at" },
        { text: "操作", value: "actions", sortable: false }
      ],
      pageCount: 1,
    },

    group_list: [],
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
        const data = await auth.fetchGroupList({ 
          session: this.$store.getters.session,
          regex: filters.enableRegex ? filters.regex : null,
          p: filters.p
        })

        if (data.code !== 0){
          throw new Error(data.errmsg)
        }

        this.group_list = data.groups;
        this.table.pageCount = data.page_count;
      } catch (e) {
        this.openDialog({ msg: e.message })
      }

      this.loadingData = false;
    },

    async delGroup({ name }) {
      try {
        const json = await auth.delGroup({
          session: this.$store.getters.session,
          name
        })

        if (json.code !== 0){
          throw new Error(json.errmsg)
        }

        let index = 0;
        for (; index < this.group_list.length; index++){
          if (this.group_list[index].name == name) break;
        }
        if (index < this.group_list){
          this.group_list.splice(index, 1);
        }
      } catch(e) {
        this.openDialog({ msg: e.message })
      }
      this.loadData();
    },

    async addGroup() {
      this.add_group.loading = true;
      try {
        const json = await auth.addGroup({
          session: this.$store.getters.session,
          name: this.add_group.name,
          expire_at: (
            this.add_group.date_picker.enable ? 
              (new Date(this.add_group.date_picker.date)).getTime() :
              0
          )
        })
        if (json.code !== 0) { 
          throw new Error(json.errmsg)
        }
      } catch(e) {
        this.openDialog({ msg: e.message })
      }

      this.add_group.loading = false;
      this.loadData();
    }
  },

  mounted() {
    
  },

  components: { ErrorDialog, GroupManager }
}
</script>