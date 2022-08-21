<template>
  <v-hover v-slot="{ hover }">
    <v-card
      :key="rsv.id"
      style="margin-top: 20px"
      color="cyan lighten-5"
      :elevation="hover ? 6 : 2"
    >
      <div class="d-flex flex-no-wrap justify-space-between">
        <div>
          <v-card-title class="text-h5"
            >{{ rsv.item }}
            <v-chip
              v-if="rsv.state & (0x1 > 0)"
              class="ma-1"
              color="purple"
              dark
              ripple
              >审批中</v-chip
            >
            <v-chip
              v-else-if="(rsv.state & 0x2) > 0"
              class="ma-1"
              color="primary"
              dark
              ripple
              >进行中</v-chip
            >

            <v-chip
              v-if="(rsv.state & 0x8) > 0"
              class="ma-1"
              color="grey"
              dark
              ripple
              >用户取消</v-chip
            >
            <v-chip
              v-else-if="(rsv.state & 0x10) > 0"
              class="ma-1"
              color="error"
              dark
              ripple
              >拒绝</v-chip
            >
            <v-chip
              v-else-if="(rsv.state & 0x20) > 0"
              class="ma-1"
              color="black"
              dark
              ripple
              >出现违规</v-chip
            >
            <template v-else-if="(rsv.state & 0x4) > 0">
              <v-chip class="ma-1" color="warning" dark ripple>已完成</v-chip>
            </template>

            <v-chip
              v-if="(rsv.state & 0x39) === 0"
              class="ma-1"
              color="success"
              dark
              ripple
              >通过</v-chip
            >
          </v-card-title>

          <v-card-subtitle class="subtitle-1">
            <div><b>预约人</b>：{{ rsv.guest }}</div>
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
            <v-expand-transition>
              <div v-show="hover">
                <div><b>事由</b>：{{ rsv.reason }}</div>
                <div>
                  <b>预约方式</b>：{{
                    rsv.method === 1 ? '时间段预约' : '自由时段预约'
                  }}
                </div>
                <div><b>预约编号</b>：{{ rsv.id }}</div>
              </div>
            </v-expand-transition>
          </v-card-subtitle>

          <v-expand-transition>
            <div v-if="(rsv.state & 0x9) === 0" v-show="hover">
              <v-divider></v-divider>
              <v-card-subtitle>
                <div><b>审批人</b>：{{ rsv.approver }}</div>
                <div>
                  <b>审批理由</b>：{{ rsv['exam-rst'] }}
                </div></v-card-subtitle
              >
            </div>
          </v-expand-transition>

          <v-expand-transition>
            <v-card-actions v-if="(rsv.state & 0x3) > 0" v-show="hover">
              <template v-if="(rsv.state & 0x1) > 0">
                <v-btn
                  @click="$emit('auditSubmit', { id: rsv.id, type: true })"
                  outlined
                  rounded
                  color="success"
                >
                  <v-icon small>mdi-check</v-icon>
                  通过
                </v-btn>
                <v-btn
                  @click="$emit('auditSubmit', { id: rsv.id, type: false })"
                  color="error"
                  outlined
                  rounded
                >
                  <v-icon small>mdi-close</v-icon>
                  拒绝
                </v-btn>
              </template>
              <v-btn
                v-if="(rsv.state & 0x2) > 0"
                @click="$emit('reserveFinish', { id: rsv.id })"
                outlined
                rounded
                color="success"
              >
                <v-icon small>mdi-pencil</v-icon>
                完成预约
              </v-btn>
            </v-card-actions>
          </v-expand-transition>
        </div>
        <v-avatar class="ma-3" size="125" tile>
          <v-img :src="rsv.thumbnail"
            ><template v-slot:placeholder>
              <v-row class="fill-height ma-0" align="center" justify="center">
                <v-progress-circular
                  indeterminate
                  color="grey lighten-5"
                ></v-progress-circular>
              </v-row> </template
          ></v-img>
        </v-avatar>
      </div>
    </v-card>
  </v-hover>
</template>

<script>
export default {
  data() {
    return {};
  },
  methods: {
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
  },
  props: ['rsv'],
};
</script>