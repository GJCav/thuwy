<template>
  <v-col lg="8" offset-lg="2" cols="12" offset="0">
    <h1>查看Issue#{{ id }}细节</h1>
    <!-- 当 ID=0的时候，表示新增一个Issue -->
    <v-row>
      <v-col cols="10">
        <v-timeline align-top dense>
          <v-timeline-item
            v-for="(issue, key) in issues"
            :key="issue.id"
            :color="colors[key]"
          >
            <v-card :color="colors[key]" dark>
              <v-card-title class="text-h6"> {{ issue.title }} </v-card-title>
              <v-card-subtitle class="text-h9">{{
                issue.author
              }}</v-card-subtitle>
              <v-card-text class="white text--primary" v-if="issue.content">
                <p>
                  {{ issue.content }}
                </p>
                <v-btn
                  href="#comment"
                  :color="colors[key]"
                  class="mx-0"
                  outlined
                >
                  Reply
                </v-btn>
              </v-card-text>
            </v-card>
          </v-timeline-item>
        </v-timeline>
        <v-card id="comment" elevation="4" class="mt-10">
          <v-card-title class="font-weight-black text-h6"
            >回复评论</v-card-title
          >
          <v-card-text v-if="issues !== null">
            <send-issue :reply_id="issues[0].id"></send-issue>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="2">
        <h3>Labels</h3>
        <v-chip-group v-if="issues !== null" column active-class="warning">
          <v-chip
            v-for="(tag, key) in issues[0].tags"
            :key="key"
            outlined
            small
            class="ma-2"
            color="cyan"
            ripple
            >{{ tag }}</v-chip
          >
        </v-chip-group>
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
import { getIssue } from "@/api/issue.js";
import SendIssue from "../../components/Issue/SendIssue.vue";

export default {
  components: { SendIssue },
  data() {
    return {
      issues: null,
      colors: []
    };
  },
  methods: {
    randColor() {
      var tmp = Math.ceil(Math.random() * 10);
      switch (tmp) {
        case 1:
          return "red darken-1";
        case 2:
          return "pink darken-1";
        case 3:
          return "purple darken-1";
        case 4:
          return "deep-purple darken-1";
        case 5:
          return "indigo darken-1";
        case 6:
          return "blue darken-1";
        case 7:
          return "cyan darken-1";
        case 8:
          return "teal darken-1";
        case 9:
          return "orange darken-1";
        case 10:
          return "blue-grey darken-1";
      }
    },
    async doGetIssue() {
      const data = await getIssue(this.id, this.$store.state.session);
      this.issues = data.issues;
      for (let i = 0; i < this.issues.length; i++) {
        this.colors.push(this.randColor());
      }
    }
  },
  mounted() {
    this.doGetIssue();
  },
  computed: {
    id() {
      return this.$route.params.id;
    }
  }
};
</script>
<!-- 








































































































































































































































































































































































































































































































































































































































































































































































































































































































































    
 -->