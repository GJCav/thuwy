<template>
  <v-col lg="6" offset-lg="3" cols="12" offset="0">
    <h1>
      预约审批
      <v-btn
        @click="loadRsvList"
        :disabled="loading"
        :loading="loading"
        icon
        large
        ><v-icon>mdi-refresh</v-icon></v-btn
      >
    </h1>
    <v-tabs v-model="tab" background-color="transparent" grow>
      <v-tab v-for="tabItem in tabs" :key="tabItem">
        {{ tabItem }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab" style="background-color: transparent">
      <v-tab-item>
        <v-col>
          <!--待审批-->
          <template v-for="rsv in rsvList">
            <rsv-item
              v-if="(rsv.state & 0x1) > 0"
              :rsv="rsv"
              :key="rsv.id"
              @auditSubmit="auditSubmit($event)"
            ></rsv-item>
          </template>
        </v-col>
      </v-tab-item>
      <v-tab-item>
        <v-col>
          <!--进行中-->
          <template v-for="rsv in rsvList">
            <rsv-item
              v-if="(rsv.state & 0x2) > 0"
              :rsv="rsv"
              :key="rsv.id"
              @reserveFinish="reserveFinish($event)"
            ></rsv-item>
          </template>
        </v-col>
      </v-tab-item>
      <v-tab-item>
        <v-col>
          <!--已结束-->
          <template v-for="rsv in rsvList">
            <rsv-item
              v-if="(rsv.state & 0x4) > 0"
              :rsv="rsv"
              :key="rsv.id"
            ></rsv-item>
          </template>
        </v-col>
      </v-tab-item>
    </v-tabs-items>
    <confirm-box
      v-model="msgbox"
      :title="msgboxTitle"
      text="请填写理由"
      @confirm="confirmSubmit"
      @update="reasonToSubmit = $event"
      :editDefault="reasonToSubmit"
      edit
      persistent
    ></confirm-box>
    <confirm-box
      v-model="dialog"
      title="完成预约"
      text="确认完成预约吗？"
      @confirm="confirmFinish"
      persistent
    ></confirm-box>
  </v-col>
</template>

<script>
import { getRsvList, submitAudit, finishRsv } from '@/api/rsv';
import { getItem } from '@/api/item';
import ConfirmBox from '@/components/ConfirmBox.vue';
import RsvItem from '@/components/RsvItem.vue';

export default {
  data() {
    return {
      tab: null,
      tabs: ['待审核', '进行中', '已结束'],
      rsvList: [],
      msgboxTitle: '',
      msgbox: false,
      reasonToSubmit: '',
      idToSubmit: undefined,
      typeToSubmit: undefined,
      dialog: false,
      loading: false,
    };
  },
  async mounted() {
    this.loadRsvList();
  },
  methods: {
    async loadRsvList() {
      this.loading = true;
      try {
        this.rsvList = await getRsvList();
      } catch (e) {
        this.loading = false;
        throw e;
      }
      let promises = [];
      let newRsvList = [];
      for (let i = 0; i < this.rsvList.length; i++) {
        promises.push(
          (async () => {
            try {
              var item = await getItem(this.rsvList[i]['item-id']);
            } catch (e) {
              this.loading = false;
              throw e;
            }
            newRsvList.push({
              ...this.rsvList[i],
              // name: item.name,
              thumbnail: item.thumbnail,
            });
          })()
        );
      }
      await Promise.all(promises);
      this.rsvList = newRsvList;
      console.log(this.rsvList);
      this.loading = false;
    },
    auditSubmit({ id, type }) {
      this.idToSubmit = id;
      this.typeToSubmit = type;
      this.msgboxText = '请填写理由';
      this.msgboxTitle = type ? '通过申请' : '拒绝申请';
      this.reasonToSubmit = type ? '同意' : '拒绝';
      this.msgbox = true;
    },
    async confirmSubmit(confirm) {
      if (confirm) {
        await submitAudit(
          this.idToSubmit,
          this.typeToSubmit,
          this.reasonToSubmit
        );
        this.$store.dispatch('showMessage', {
          message: '审批成功',
          timeout: 2000,
        });
        return this.loadRsvList();
      }
    },
    reserveFinish({ id }) {
      this.idToSubmit = id;
      this.dialog = true;
    },
    async confirmFinish(confirm) {
      if (confirm) {
        await finishRsv(this.idToSubmit);
        this.$store.dispatch('showMessage', {
          message: '操作成功',
          timeout: 2000,
        });
        return this.loadRsvList();
      }
    },
  },
  components: {
    ConfirmBox,
    RsvItem,
  },
  name: 'RsvManage',
};
</script>