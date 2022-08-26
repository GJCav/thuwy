<template>
  <v-col lg="8" offset-lg="2" cols="12" offset="0">
    <h1>新建Issue</h1>
    <!-- 当 ID=0的时候，表示新增一个Issue -->
    <v-row>
      <v-col cols="10">
        <v-card elevation="4" class="mt-10">
          <v-card-title class="font-weight-black text-h6"
            >发布新答疑</v-card-title
          >
          <v-card-text>
            <send-issue :reply_id="0"></send-issue>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
import SendIssue from "../../components/Issue/SendIssue.vue";

export default {
  components: { SendIssue },
  data() {
    return {
      issue: {
        title: "",
        content: {},
        tag: []
      },
    };
  },
};
</script>
