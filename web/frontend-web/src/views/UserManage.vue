<template>
  <v-col lg="6" offset-lg="3" cols="12" offset="0">
    <h1>
      用户管理<v-btn
        @click="reloadLists"
        :disabled="loading"
        :loading="loading"
        icon
        large
        ><v-icon>mdi-refresh</v-icon></v-btn
      >
    </h1>
    <br />

    <v-tabs v-model="tab" background-color="transparent" grow>
      <v-tab v-for="tabItem in tabs" :key="tabItem">
        {{ tabItem }}
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab" style="background-color: transparent">
      <v-tab-item>
        <v-data-table :headers="headers" :items="users">
          <template v-slot:[`item.admin`]="{ item }"
            ><v-simple-checkbox
              color="cyan"
              :value="item.admin"
              :disabled="!item.admin"
              @input="changeAdminState(item, !item.admin)"
            ></v-simple-checkbox
          ></template>
          <template v-slot:[`item.action`]="{ item }"
            ><v-btn small @click="unbindUserProfile(item)"
              >解绑</v-btn
            ></template
          >
        </v-data-table>
      </v-tab-item>

      <v-tab-item
        ><v-data-table :headers="headers2" :items="requestList">
          <template v-slot:[`item.name`]="{ item }">{{
            item.requestor.name
          }}</template>
          <template v-slot:[`item.action`]="{ item }">
            <v-btn
              @click="auditAdminRequest(item, true)"
              color="success"
              class="ml-2"
              outlined
              small
              >通过</v-btn
            >
            <v-btn
              @click="auditAdminRequest(item, false)"
              color="error"
              class="ml-2"
              outlined
              small
              >拒绝</v-btn
            >
          </template>
        </v-data-table></v-tab-item
      >
    </v-tabs-items>

    <confirm-box
      v-model="dialog"
      title="管理员变更"
      :text="confirmboxText"
      @confirm="confirmChange"
    ></confirm-box>
    <confirm-box
      v-model="dialog2"
      title="解除绑定"
      :text="confirmboxText"
      @confirm="confirmUnbind"
    ></confirm-box>
    <confirm-box
      v-model="msgbox"
      :title="msgboxTitle"
      text="请填写理由"
      @confirm="confirmSubmit"
      @update="reasonToAudit = $event"
      :editDefault="reasonToAudit"
      edit
      persistent
    ></confirm-box>
  </v-col>
</template>

<script>
import ConfirmBox from '@/components/ConfirmBox.vue';
import {
  getAllUsers,
  revokeAdmin,
  unbindUser,
  getAdminRequestList,
  auditAdminRequest,
} from '@/api/user';

export default {
  name: 'UserManage',
  data() {
    return {
      tab: null,
      tabs: ['用户管理', '管理员申请'],
      dialog: false,
      dialog2: false,
      msgbox: false,
      loading: false,
      confirmboxText: '',
      openidToEdit: 0,
      adminStateToChange: false,
      msgboxTitle: '',
      reasonToAudit: '',
      requestIdToAudit: '',
      stateToAudit: false,
      headers: [
        {
          text: '学号',
          value: 'school-id',
        },
        {
          text: '姓名',
          value: 'name',
          sortable: false,
        },
        {
          text: '班级',
          value: 'clazz',
        },
        {
          text: '管理员',
          value: 'admin',
        },
        {
          text: '操作',
          value: 'action',
          sortable: false,
        },
      ],
      headers2: [
        {
          text: '姓名',
          value: 'name',
          sortable: false,
        },
        {
          text: '操作',
          value: 'action',
          sortable: false,
        },
      ],
      users: [],
      requestList: [],
    };
  },
  methods: {
    async loadUsers() {
      this.users = await getAllUsers();
    },
    async loadAdminRequestList() {
      this.requestList = await getAdminRequestList();
    },
    changeAdminState(item, state) {
      this.confirmboxText = `${state ? '授予' : '解除'}${
        item.name
      }管理员权限吗`;
      this.openidToEdit = item.openid;
      this.adminStateToChange = state;
      this.dialog = true;
    },
    unbindUserProfile(item) {
      this.confirmboxText = `确认解除绑定${item.name}吗`;
      this.openidToEdit = item.openid;
      this.dialog2 = true;
    },
    auditAdminRequest(item, state) {
      this.msgboxTitle = state ? '同意申请' : '拒绝申请';
      this.reasonToAudit = state ? '同意' : '拒绝';
      this.requestIdToAudit = item.id;
      this.stateToAudit = state;
      this.msgbox = true;
    },
    async reloadLists() {
      this.loading = true;
      await Promise.all([this.loadUsers(), this.loadAdminRequestList()]);
      this.loading = false;
    },
    async confirmChange(confirm) {
      if (!confirm) {
        return;
      }
      if (!this.adminStateToChange) {
        await revokeAdmin(this.openidToEdit);
        this.$store.dispatch('showMessage', {
          message: '操作成功',
          timeout: 2000,
        });
        return this.loadUsers();
      }
    },
    async confirmUnbind(confirm) {
      if (confirm) {
        await unbindUser(this.openidToEdit);
        this.$store.dispatch('showMessage', {
          message: '操作成功',
          timeout: 2000,
        });
        return this.loadUsers();
      }
    },
    async confirmSubmit(confirm) {
      if (confirm) {
        await auditAdminRequest(
          this.requestIdToAudit,
          this.reasonToAudit,
          this.stateToAudit ? 1 : 0
        );
        this.$store.dispatch('showMessage', {
          message: '操作成功',
          timeout: 2000,
        });
        return Promise.all([this.loadUsers(), this.loadAdminRequestList()]);
      }
    },
  },
  async mounted() {
    return Promise.all([this.loadUsers()], [this.loadAdminRequestList()]);
  },
  components: {
    ConfirmBox,
  },
};
</script>