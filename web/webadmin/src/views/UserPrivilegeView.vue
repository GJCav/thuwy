<template>
<v-container>
  <ErrorDialog title="Error" :msg="errDialog.msg" v-model="errDialog.enable"></ErrorDialog>

  <h1 class="mt-4">用户权限管理</h1>

  <v-tabs v-model="tab" color="black">
    <v-tab class="">管理</v-tab>
    <!-- <v-tab class="">说明</v-tab> -->
  </v-tabs>

  <v-tabs-items v-model="tab">
    <!-- 用户权限管理 tab -->
    <v-tab-item> 
      <v-card flat>
        <v-data-table
          :headers="table.headers"
          :items="privilege_list"
          sort-by="name"
        >
          <!-- 表标题位置 -->
          <template v-slot:top>
            <v-toolbar flat color="white">
              <v-toolbar-title>
                <div class="d-flex align-center">
                  <!-- 切换用户 -->
                  <v-menu 
                    :offset-y="true" transition="scroll-y-transition"
                    v-model="switch_menu"
                    :nudge-width="300"
                    :close-on-content-click="false"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn 
                        fab icon small
                        v-bind="attrs"
                        v-on="on"
                        :loading="switch_loading"
                        :disabled="switch_loading"
                      >
                        <v-icon color="primary">mdi-account-convert-outline</v-icon>
                      </v-btn>
                    </template>
                    <v-card>
                      <v-card-text>
                        <v-text-field
                          v-model="switch_openid"
                          @keydown="pressToSwitch"
                          label="User Openid"
                          clearable
                        ></v-text-field>
                        <v-row class="justify-space-between align-center mx-0 my-0">
                          <span>
                            或者，可以通过
                            <router-link to="/userlist" class="text-decoration-none font-italic">User List</router-link>
                            页面选择用户
                          </span>
                          <v-btn 
                            icon color="primary"
                            outlined small
                            class="pa-0"
                            @click="switchUser()"
                          >
                            <v-icon small>mdi-check</v-icon>
                          </v-btn>
                        </v-row>
                      </v-card-text>
                    </v-card>
                  </v-menu>
                  <h3 class="ml-4">{{currentUser.name}} 的权限</h3>
                  <h5
                    class="text--secondary ml-5"
                    style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;"
                  >ID: {{currentUser.openid}}</h5>
                </div>
              </v-toolbar-title>
              <v-spacer></v-spacer>
              <v-dialog 
                max-width="768px" 
                @click:outside="clearAddScopeResult"
              >
              <!-- 关闭对话框时删除错误信息 -->
                <template v-slot:activator="{ on, attrs }">
                  <v-btn 
                    small color="primary" 
                    outlined icon 
                    v-bind="attrs" v-on="on"
                    :loading="add_scope.loading"
                    :disabled="disableAddScopeBtn"
                  >
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </template>
                <!-- 添加 Scope 对话框  -->
                <ScopePicker 
                  title="新增权限"
                  @confirm="addScopes"
                >
                  <template v-slot:bottom>
                    <v-card-text class="mt-4" v-if="add_scope.results.length != 0">
                      <v-alert 
                        v-for="result in add_scope.results"
                        :key="result.name"
                        :type="result.type"
                      >
                        Add <span class="font-weight-bold font-italic">
                          {{ result.name }}</span> {{ result.type }}. {{ result.msg }}
                      </v-alert>
                    </v-card-text>
                  </template>
                </ScopePicker>
              </v-dialog>
            </v-toolbar>
          </template>
          
          <!-- 操作列 -->
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
  
              <v-btn color="error" @click="delScope(item)">
                Sure to delete?
              </v-btn>
            </v-menu>
          </template>

          <!-- 到期时间列 -->
          <!-- eslint-disable-next-line vue/valid-v-slot -->
          <template v-slot:item.expire_at="{ item }">
            <span v-if="item.expire_at == 0">长期有效</span>
            <span v-else>{{ (new Date(item.expire_at)).toLocaleDateString() }}</span>
          </template>
        </v-data-table>
      </v-card>
    </v-tab-item>

    <!-- 权限说明页面
    <v-tab-item>
      <v-card flat>
        <v-card-text>there</v-card-text>
      </v-card>
    </v-tab-item> -->
  </v-tabs-items>
</v-container>
</template>

<script>
import * as auth from "../backend-api/auth"
import ScopePicker from "../components/ScopePicker.vue";

export default {
    props: {
        initial_openid: { type: String, default: null }
    },
    data: () => ({
        tab: null,
        errDialog: { msg: "", enable: false },
        switch_openid: "",
        switch_loading: false,
        switch_menu: false,
        addScopeDialog: {},
        table: {
            headers: [
                { text: "权限", value: "name" },
                { text: "到期时间", value: "expire_at" },
                { text: "权限描述", value: "description" },
                { text: "操作", value: "actions", sortable: false }
            ],
        },
        currentUser: {
            name: "<null>",
            openid: null,
        },
        privilege_list_raw: [],
        scopes: [],
        add_scope: {
            loading: false,
            results: []
        }
    }),
    computed: {
        privilege_list() {
            const list = [];
            for (const info of this.privilege_list_raw) {
                list.push({
                    expire_at: info.expire_at,
                    ...info.scope
                });
            }
            return list;
        },
        disableAddScopeBtn() {
            return (!this.currentUser.openid) || this.add_scope.loading;
        }
    },
    methods: {
        showError(msg) {
            this.errDialog.msg = msg;
            this.errDialog.enable = true;
        },
        pressToSwitch(keyEvent) {
            if (keyEvent.key === "Enter")
                this.switchUser();
        },
        async switchUser(targetOpenid) {
            targetOpenid = targetOpenid || this.switch_openid;
            this.switch_loading = true;
            try {
                const profile = await auth.fetchUserProfile({
                    session: this.$store.getters.session,
                    openid: targetOpenid
                });
                if (profile.code !== 0) {
                    throw new Error("fetch profile: " + profile.errmsg);
                }
                this.currentUser.name = profile.name;
                const json = await auth.fetchUserDetailedPrivilegeInfo({
                    session: this.$store.getters.session,
                    openid: targetOpenid
                });
                if (json.code !== 0) {
                    throw new Error("fetch privilege info: " + json.errmsg);
                }
                this.currentUser.openid = targetOpenid;
                this.privilege_list_raw = json.scopes;
            }
            catch (e) {
                this.showError(e.message);
            }
            this.switch_loading = false;
            this.switch_menu = false;
            this.add_scope.loading = false;
        },
        async delScope(item) {
            const { name } = item;
            const { openid } = this.currentUser;
            try {
                const json = await auth.delUserScope({
                    session: this.$store.getters.session,
                    name,
                    openid
                });
                if (json.code !== 0) {
                    throw new Error(json.errmsg);
                }
                // 更新 UI
                let index = 0;
                for (; index < this.privilege_list_raw.length; index++) {
                    if (this.privilege_list_raw[index].scope.name == item.name) {
                        break;
                    }
                }
                if (index >= this.privilege_list_raw.length)
                    return;
                this.privilege_list_raw.splice(index, 1);
            }
            catch (e) {
                this.showError(e.message);
            }
        },

        async addScopes({ expire_at, scopes }) {
            this.add_scope.loading = true;
            const { openid } = this.currentUser;
            const results = [];
            for (const name of scopes) {
                try {
                    const json = await auth.addUserScope({
                        session: this.$store.getters.session,
                        name,
                        openid,
                        expire_at
                    });
                    if (json.code !== 0) {
                        results.push({
                            name,
                            type: "error",
                            msg: json.errmsg
                        });
                    }
                    else {
                        results.push({
                            name,
                            type: "success",
                            msg: ""
                        });
                    }
                }
                catch (e) {
                    results.push({
                        name,
                        type: "error",
                        msg: e.message
                    });
                }
            }
            this.add_scope.results = results;
            this.add_scope.loading = false;
            this.switchUser(this.currentUser.openid); // 刷新权限列表
        },

        clearAddScopeResult(){
          this.add_scope.results = [];
        }
    },
    mounted() {
        // 实现从 User List 选择用户
        this.switch_openid = this.initial_openid;
        if (this.switch_openid)
            this.switchUser();
    },
    components: { ScopePicker }
}
</script>