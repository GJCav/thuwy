<template>
  <v-col lg="8" offset-lg="2" cols="12" offset="0">
    <h1>查看Issue#{{ id }}细节</h1>
    <!-- 当 ID=0的时候，表示新增一个Issue -->
    <v-row>
      <v-col cols="10">
        <v-timeline align-top dense>
          <v-timeline-item
            v-for="(item, i) in items"
            :key="i"
            :color="item.color"
            :icon="item.icon"
            fill-dot
          >
            <v-card
              :color="issue.color"
              dark
              :to="`${issue.id}/`"
              v-for="issue in issueList"
              :key="issue.id"
            >
              <v-card-title class="text-h6"> {{ issue.title }} </v-card-title>
              <v-card-text class="white text--primary" v-if="issue.content">
                <p>
                  {{ issue.content }}
                </p>
                <v-btn :color="item.color" class="mx-0" outlined>
                  Reply
                </v-btn>
              </v-card-text>
            </v-card>
          </v-timeline-item>
        </v-timeline>
        <v-card elevation="4" class="mt-10">
          <v-card-title class="font-weight-black text-h6"
            >留下精彩评论</v-card-title
          >
          <v-card-text>
            <send-comment></send-comment>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="2">
        <h3>Labels</h3>
        <!-- <v-chip-group column active-class="warning">
          <v-chip
            v-for="(tag, key) in issue.tags"
            :key="key"
            outlined
            small
            class="ma-2"
            color="cyan"
            ripple
            >{{ tag }}</v-chip
          >
        </v-chip-group> -->
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
import { getIssueList } from "@/api/issue.js";
import { getIssue } from "@/api/issue.js";
import SendComment from "../../components/Issue/SendComment.vue";
// import IssueComment from "../../components/Issue/IssueComment.vue";

export default {
  components: { SendComment },
  data() {
    return {
        issue: null,
      issueList: [],
      items: [
        {
          color: "red lighten-2",
          icon: "mdi-star"
        },
        {
          color: "purple darken-1",
          icon: "mdi-book-variant"
        },
        {
          color: "green lighten-1",
          icon: "mdi-airballoon"
        }
      ]
    };
  },
  methods: {
    async doGetIssue() {
      this.issue = await getIssue(this.id, this.$store.state.session);
      },
     async doGetIssueList() {
      this.issueList = (await getIssueList())?.issues;
    },
  },
  mounted() {
    this.doGetIssue();
    this.doGetIssueList();
  },
  computed: {
    id() {
      return this.$route.params.id;
    }
  }
};
</script>
