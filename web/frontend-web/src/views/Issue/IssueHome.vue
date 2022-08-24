<template>
  <div>
    <v-carousel
      :continuous="true"
      :cycle="cycle"
      :show-arrows="true"
      hide-delimiter-background
      delimiter-icon="mdi-circle"
      height="576"
    >
      <v-carousel-item v-for="(slide, i) in slides" :key="i">
        <v-sheet dark :color="colors[i]" height="100%" tile>
          <v-row class="fill-height" align="center" justify="center">
            <div class="text-h2">{{ slide }}答疑坊</div>
          </v-row>
          <v-row justify="center">
            <v-btn
              to="0/"
              large
              outlined
              dark
              style="position: absolute; bottom: 64px"
              >我要提问</v-btn
            >
          </v-row>
        </v-sheet>
      </v-carousel-item>
    </v-carousel>
    <v-col md="8" offset-md="2" cols="12" offset="0">
      <h1>答疑坊-首页</h1>
      <v-row>
        <v-col md="4">
          <v-card color="primary" dark>
            <v-card-title>最新通知</v-card-title>
            <v-card-text>
              <v-list color="primary lighten-1" dark>
                <v-list-item
                  :to="`${key + 1}/`"
                  v-for="(notice, key) in notices"
                  :key="key"
                >
                  <v-list-item-content>{{ notice }}</v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col md="4">
          <v-card color="success" dark>
            <v-card-title>学习</v-card-title>
          </v-card>
        </v-col>
        <v-col md="4">
          <v-card color="warning" dark>
            <v-card-title>生活</v-card-title>
          </v-card>
        </v-col>
      </v-row>
      <v-row justify="center">
        <h1>
          最新提问 <v-btn to="/issue/list/" color="primary">查看所有</v-btn>
          <v-btn to="/issue/0/" color="success">我要提问</v-btn>
        </h1>
      </v-row>
      <v-row justify="center">
        <v-col cols="12" md="6" md-offset="3">
          <v-card
            :color="randColor()"
            class="mt-5"
            :to="`${issue.id}/`"
            v-for="issue in issueList"
            :key="issue.id"
          >
            <v-card-title>{{ issue.title }}</v-card-title>
            <v-card-text v-if="issue.content">
              {{ issue.content }}
            </v-card-text>
            <v-card-actions>
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
            </v-card-actions>
            <v-card-actions> 作者：{{ issue.author }} </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      <!-- </v-row> -->
    </v-col>
  </div>
</template>

<script>
import { getIssueList } from "@/api/issue.js";

export default {
  name: "IssueHome",
  data() {
    return {
      issueList: [],
      colors: [
        "green",
        "secondary",
        "yellow darken-4",
        "red lighten-2",
        "orange darken-1",
      ],
      cycle: false,
      slides: ["First", "Second", "Third", "Fourth", "Fifth"],
      notices: ["notice1", "notice2", "notice3"],
      learns: ["learn1", "learn2"]
    };
  },
  methods: {
    async doGetIssueList() {
      this.issueList = (await getIssueList())?.issues;
    },
    randColor() {
      var r = Math.floor(Math.random() * 32) + 224;
      var g = Math.floor(Math.random() * 32) + 224;
      var b = Math.floor(Math.random() * 32) + 224;
      return `#${r.toString(16)}${g.toString(16)}${b.toString(16)}`
    }
  },
  mounted() {
    this.doGetIssueList();
  },
};
</script>