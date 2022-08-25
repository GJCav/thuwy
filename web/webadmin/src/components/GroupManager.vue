<template>
<v-card class="my-2">
  <ErrorDialog 
    :msg="errDialog.msg" 
    v-model="errDialog.enable"
  ></ErrorDialog>

  <v-skeleton-loader
    :loading="loading"
    type="card"
  >
    <v-card-title>{{group_name}} </v-card-title>
    <v-card-text>
      <div class="d-flex align-center">
        <h3 class="d-inline-block">组员：</h3>

        <!-- 一系列用户 chips -->
        <v-menu
          v-for="user in members"
          :key="user.openid"
          transition="slide-y-transition"
          bottom :offset-y="true"
        >
          <template v-slot:activator="{ on, attrs }">
              <v-chip
                class="mx-2 pr-1" color="teal"
                outlined
                v-bind="attrs"
                v-on="on"
              >
                {{user.name}}
                <v-menu :offset-y="true" transition="scroll-y-transition">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn 
                      icon small
                      v-bind="attrs"
                      v-on="on"
                    >
                      <v-icon>mdi-close-circle-outline</v-icon>
                    </v-btn>
                  </template>
      
                  <v-btn color="error" @click="delMember(user)">
                    Sure to delete?
                  </v-btn>
                </v-menu>
              </v-chip>
          </template>
          <v-card>
            <v-card-text class="text--primary">
            <span>学号: {{user["school-id"]}}</span><br/>
            <span>班级: {{user.clazz}}</span> <br/>
            <span>ID: {{user.openid}}</span>
            </v-card-text>
          </v-card>
        </v-menu>

        <!-- 添加用户 chip -->
        <v-dialog v-model="add_member_dialog" max-width="600px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn 
              icon 
              color="teal" outlined small
              v-bind="attrs"
              v-on="on"
              :loading="add_member_loading"
              :disabled="add_member_loading"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
          <UserPicker 
            multi_select 
            @confirmSelect="addMembers"
          ></UserPicker>
        </v-dialog>
      </div>

      <div class="d-flex align-center mt-2">
        <h3 class="d-inline-block">权限：</h3>

        <!-- 一系列权限 chips -->
        <v-menu
          v-for="pri in privileges"
          :key="pri.scope.name"
          transition="slide-y-transition"
          bottom :offset-y="true"
        >
          <template v-slot:activator="{ on, attrs }">
              <v-chip
                class="mx-2 pr-1" color="cyan"
                outlined
                v-bind="attrs"
                v-on="on"
              >
                {{ pri.scope.name }}
                <v-menu :offset-y="true" transition="scroll-y-transition">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn 
                     icon small
                      v-bind="attrs"
                      v-on="on"
                    >
                      <v-icon>mdi-close-circle-outline</v-icon>
                    </v-btn>
                  </template>
      
                  <v-btn color="error" @click="delScope(pri)">
                    Sure to delete?
                  </v-btn>
                </v-menu>
              </v-chip>
          </template>

          <!-- 权限详细信息 -->
          <v-card>
            <v-card-text class="text--primary">
              <span>{{ pri.scope.description }}</span><br/>
              <span v-if="pri.expire_at == 0">长期有效</span>
              <span v-else>在 {{ (new Date(pri.expire_at)).toLocaleDateString() }} 到期</span>
            </v-card-text>
          </v-card>
        </v-menu>

        <!-- 添加权限 -->
        <v-dialog 
          max-width="768px" 
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn 
              icon
              color="cyan" outlined small
              v-bind="attrs"
              v-on="on"
              :loading="add_scope_loading"
              :disabled="add_scope_loading"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
          <ScopePicker title="新增权限" @confirm="addScopes"></ScopePicker>
        </v-dialog>
      </div>
      
    </v-card-text>
  </v-skeleton-loader>
</v-card>
</template>


<script>
import ErrorDialog from './ErrorDialog.vue';
import * as auth from "../backend-api/auth"
import UserPicker from './UserPicker.vue';

export default {
  name: "GroupManager",

  props: {
    group_name: { type: String, default: null }
  },

  data: () => ({
    loading: true,

    errDialog: {
      msg: "",
      enable: false,
    },

    expire_at: 0,

    members: {},

    privileges: [],

    add_member_dialog: false,
    add_member_loading: false,
    add_scope_loading: false,
  }),


  methods: {
    showError(msg) {
      this.errDialog.msg = msg;
      this.errDialog.enable = true;
    },

    async loadData() {
      try {
        const json = await auth.fetchGroupInfo({
          session: this.$store.getters.session,
          name: this.group_name
        })
      
        if (json.code !== 0) {
          throw new Error(json.errmsg)
        }

        this.loading = false;
        this.expire_at = json.expire_at
        this.members = json.members
        this.privileges = json.privileges
      } catch(e) {
        this.showError(e.message)
      }
    },

    async addMember(user, reload = true) {
      this.add_member_loading = true;
      try {
        const json = await auth.addGroupMember({
          session: this.$store.getters.session,
          openid: user.openid,
          group_name: this.group_name
        })
        if(json.code !== 0){
          throw new Error(json.errmsg)
        }
        if (reload) await this.loadData();
      } catch(e) {
        this.showError(e.message)
      }
      this.add_member_loading = false;
    },

    async addMembers(users) {
      this.add_member_dialog = false;
      for(const user of users){
        await this.addMember(user, false);
      }
      this.loadData();
    },

    async delMember(user) {
      const { openid } = user;
      try{
        const json = await auth.delGroupMember({
          session: this.$store.getters.session,
          openid,
          group_name: this.group_name
        })
        if(json.code !== 0){
          throw new Error(json.errmsg)
        }
        await this.loadData()
      }catch(e){
        this.showError(e.message)
      }
    },

    async addScope({ scope, expire_at }){
      const json = await auth.addGroupScope({
        session: this.$store.getters.session,
        scope: scope,
        group_name: this.group_name,
        expire_at
      })
      if(json.code !== 0){
        throw new Error(json.errmsg)
      }
    },

    async addScopes({ scopes, expire_at }) {
      this.add_scope_loading = true;

      const err = []

      for(const scope of scopes) {
        try {
          await this.addScope({ scope, expire_at })
        } catch (e) {
          err.push("添加 " + scope + ": " + e.message)
        }
      }

      this.add_scope_loading = false;

      if (err.length > 0){
        this.showError(err.join("\n"))
      }
    },

    async delScope(pri) {
      const scope = pri.scope.name;
      try{
        const json = await auth.delGroupScope({
          session: this.$store.getters.session,
          scope,
          group_name: this.group_name
        })
        if(json.code !== 0){
          throw new Error(json.errmsg)
        }
        await this.loadData()
      }catch(e){
        this.showError(e.message)
      }
    },
  },

  mounted() {
    this.loadData();
  },

  components: { ErrorDialog, UserPicker }
}
</script>