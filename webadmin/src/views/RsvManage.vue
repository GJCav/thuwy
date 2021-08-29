<template>
  <v-col lg="6" offset-lg="3" cols="12" offset="0">
    <h1>预约审批</h1>
    <v-tabs v-model="tab" background-color="transparent" grow>
      <v-tab v-for="tabItem in tabs" :key="tabItem">
        {{ tabItem }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-col>
          <!--待审批-->
          <template v-for="rsv in rsvList">
            <v-card
              :key="rsv.id"
              v-if="(rsv.state & 0x1) > 0"
              style="margin-top: 20px"
            >
              <div class="d-flex flex-no-wrap justify-space-between">
                <div>
                  <v-card-title class="text-h5"
                    >{{ rsv.item
                    }}<v-chip class="ma-1" color="purple" dark ripple>
                      审批中
                    </v-chip></v-card-title
                  >
                  <v-card-subtitle class="subtitle-1">
                    <div><b>预约人</b>：{{ rsv.guest }}</div>
                    <div><b>事由</b>：{{ rsv.reason }}</div>
                    <div>
                      <b>预约方式</b>：{{
                        rsv.method === 1 ? '时间段预约' : '自由时段预约'
                      }}
                    </div>
                    <div>
                      <b>预约时段</b>：
                      <ul v-if="rsv.method === 1">
                        <li v-for="itvl in rsv.interval" :key="itvl">
                          {{ Itvl2Time(itvl) }}
                        </li>
                      </ul>
                      <ul v-else>
                        <li>{{ rsv.interval }}</li>
                      </ul>
                    </div>
                    <div><b>编号</b>：{{ rsv.id }}</div>
                  </v-card-subtitle>
                  <v-card-actions>
                    <v-btn
                      @click="auditSubmit(rsv.id, true)"
                      outlined
                      rounded
                      small
                      color="success"
                    >
                      <v-icon small>mdi-check</v-icon>
                      通过
                    </v-btn>
                    <v-btn
                      @click="auditSubmit(rsv.id, false)"
                      color="error"
                      outlined
                      rounded
                      small
                    >
                      <v-icon small>mdi-close</v-icon>
                      拒绝
                    </v-btn>
                  </v-card-actions>
                </div>
                <v-avatar class="ma-3" size="125" tile>
                  <v-img :src="rsv.thumbnail"></v-img>
                </v-avatar>
              </div>
            </v-card>
          </template>
        </v-col>
      </v-tab-item>
      <v-tab-item>
        <v-col>
          <!--进行中-->
          <template v-for="rsv in rsvList">
            <v-card
              :key="rsv.id"
              v-if="(rsv.state & 0x2) > 0"
              style="margin-top: 20px"
            >
              <div class="d-flex flex-no-wrap justify-space-between">
                <div>
                  <v-card-title class="text-h5"
                    >{{ rsv.item
                    }}<v-chip class="ma-1" color="success" dark ripple>
                      通过
                    </v-chip>
                    <v-chip class="ma-1" color="primary" dark ripple>
                      进行中
                    </v-chip>
                  </v-card-title>
                  <v-card-subtitle class="subtitle-1">
                    <div><b>预约人</b>：{{ rsv.guest }}</div>
                    <div><b>事由</b>：{{ rsv.reason }}</div>
                    <div>
                      <b>预约方式</b>：{{
                        rsv.method === 1 ? '时间段预约' : '自由时段预约'
                      }}
                    </div>
                    <div>
                      <b>预约时段</b>：
                      <ul v-if="rsv.method === 1">
                        <li v-for="itvl in rsv.interval" :key="itvl">
                          {{ Itvl2Time(itvl) }}
                        </li>
                      </ul>
                      <ul v-else>
                        <li>{{ rsv.interval }}</li>
                      </ul>
                    </div>
                    <div><b>编号</b>：{{ rsv.id }}</div>
                  </v-card-subtitle>
                  <template v-if="(rsv.state & 0x8) === 0">
                    <v-divider></v-divider>
                    <v-card-subtitle>
                      <div><b>审批人</b>：{{ rsv.approver }}</div>
                      <div>
                        <b>审批理由</b>：{{ rsv['exam-rst'] }}
                      </div></v-card-subtitle
                    >
                  </template>
                  <v-card-actions>
                    <v-btn
                      @click="reserveFinish(rsv.id)"
                      outlined
                      rounded
                      small
                      color="success"
                    >
                      <v-icon small>mdi-pencil</v-icon>
                      完成预约
                    </v-btn>
                  </v-card-actions>
                </div>
                <v-avatar class="ma-3" size="125" tile>
                  <v-img :src="rsv.thumbnail"></v-img>
                </v-avatar>
              </div>
            </v-card>
          </template>
        </v-col>
      </v-tab-item>
      <v-tab-item>
        <v-col>
          <!--已结束-->
          <template v-for="rsv in rsvList">
            <v-card
              :key="rsv.id"
              v-if="(rsv.state & 0x4) > 0"
              style="margin-top: 20px"
            >
              <div class="d-flex flex-no-wrap justify-space-between">
                <div>
                  <v-card-title class="text-h5"
                    >{{ rsv.item }}
                    <template v-if="(rsv.state & 0x8) > 0">
                      <v-chip class="ma-1" color="grey" dark ripple>
                        用户取消
                      </v-chip>
                    </template>
                    <template v-else-if="(rsv.state & 0x10) > 0">
                      <v-chip class="ma-1" color="error" dark ripple>
                        已拒绝
                      </v-chip>
                    </template>
                    <template v-else>
                      <v-chip class="ma-1" color="success" dark ripple>
                        通过
                      </v-chip>
                      <v-chip class="ma-1" color="warning" dark ripple>
                        已完成
                      </v-chip>
                    </template>
                  </v-card-title>
                  <v-card-subtitle class="subtitle-1">
                    <div><b>预约人</b>：{{ rsv.guest }}</div>
                    <div><b>事由</b>：{{ rsv.reason }}</div>
                    <div>
                      <b>预约方式</b>：{{
                        rsv.method === 1 ? '时间段预约' : '自由时段预约'
                      }}
                    </div>
                    <div>
                      <b>预约时段</b>：
                      <ul v-if="rsv.method === 1">
                        <li v-for="itvl in rsv.interval" :key="itvl">
                          {{ Itvl2Time(itvl) }}
                        </li>
                      </ul>
                      <ul v-else>
                        <li>{{ rsv.interval }}</li>
                      </ul>
                    </div>
                    <div><b>预约编号</b>：{{ rsv.id }}</div>
                  </v-card-subtitle>
                  <template v-if="(rsv.state & 0x8) === 0">
                    <v-divider></v-divider>
                    <v-card-subtitle>
                      <div><b>审批人</b>：{{ rsv.approver }}</div>
                      <div>
                        <b>审批理由</b>：{{ rsv['exam-rst'] }}
                      </div></v-card-subtitle
                    >
                  </template>
                </div>
                <v-avatar class="ma-3" size="125" tile>
                  <v-img :src="rsv.thumbnail"></v-img>
                </v-avatar>
              </div>
            </v-card>
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
    };
  },
  async mounted() {
    this.loadRsvList();
  },
  methods: {
    async loadRsvList() {
      this.rsvList = await getRsvList();
      let promises = [];
      let newRsvList = [];
      for (let i = 0; i < this.rsvList.length; i++) {
        promises.push(
          (async () => {
            let item = await getItem(this.rsvList[i]['item-id']);
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
    },
    Itvl2Time(itvl, method = 1) {
      if (method === 1) {
        let t = itvl.split(' ');
        const [year, month, day] = t[0].split('-');
        if (t[1] === '4') {
          return `${year}-${month}-${day} 周末整体`;
        } else {
          const mapper = [
            '',
            '早上8:00-12:00',
            '下午13:00-17:00',
            '晚上18:00-23:00',
          ];
          return `${year}-${month}-${day} ${mapper[Number(t[1])]}`;
        }
      }
    },
    auditSubmit(id, type) {
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
        return this.loadRsvList();
      }
    },
    reserveFinish(id) {
      this.idToSubmit = id;
      this.dialog = true;
    },
    async confirmFinish(confirm) {
      if (confirm) {
        await finishRsv(this.idToSubmit);
        return this.loadRsvList();
      }
    },
  },
  components: {
    ConfirmBox,
  },
  name: 'RsvManage',
};
</script>