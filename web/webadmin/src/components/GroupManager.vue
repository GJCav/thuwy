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
        <v-menu
          transition="slide-x-transition"
          right :offset-x="true"
          :close-on-content-click="false"
          :close-on-click="true"
        >
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
          <v-card>
            <v-card-title>添加组员：</v-card-title>
            <v-divider></v-divider>
            <v-card-text class="my-0">
              <v-text-field
                class="my-0"
                label="ID: "
                prepend-icon="mdi-account-circle-outline"
                append-icon="mdi-check"
                v-model="add_openid"
                @click:append="addMember"
              ></v-text-field>
            </v-card-text>
          </v-card>
        </v-menu>
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
              <span v-else>在 {{ (new Date(item.expire_at)).toLocaleDateString() }} 到期</span>
            </v-card-text>
          </v-card>
        </v-menu>

        <!-- 添加权限 -->
        <v-menu
          transition="slide-x-transition"
          right :offset-x="true"
          :close-on-content-click="false"
          :close-on-click="true"
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
          <v-card>
            <v-card-title>添加权限：</v-card-title>
            <v-divider></v-divider>
            <v-card-text class="my-0">
              <v-text-field
                class="my-0"
                label="ID: "
                prepend-icon="mdi-key"
                append-icon="mdi-check"
                v-model="add_scope"
                @click:append="addScope"
              ></v-text-field>
            </v-card-text>
          </v-card>
        </v-menu>
      </div>
      
    </v-card-text>
  </v-skeleton-loader>
</v-card>
</template>


<script>
import ErrorDialog from './ErrorDialog.vue';
import * as auth from "../backend-api/auth"

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

    add_openid: "",
    add_member_loading: false,
    add_scope: "",
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

    async addMember(){
      this.add_member_loading = true;
      try {
        const json = await auth.addGroupMember({
          session: this.$store.getters.session,
          openid: this.add_openid,
          group_name: this.group_name
        })
        if(json.code !== 0){
          throw new Error(json.errmsg)
        }
        await this.loadData();
      } catch(e) {
        this.showError(e.message)
      }
      this.add_member_loading = false;
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

    async addScope(){
      this.add_scope_loading = true;
      try{
        const json = await auth.addGroupScope({
          session: this.$store.getters.session,
          scope: this.add_scope,
          group_name: this.group_name
        })
        if(json.code !== 0){
          throw new Error(json.errmsg)
        }
        await this.loadData();
      }catch(e){
        this.showError(e.message)
      }
      this.add_scope_loading = false;
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

  components: { ErrorDialog }
}
</script>