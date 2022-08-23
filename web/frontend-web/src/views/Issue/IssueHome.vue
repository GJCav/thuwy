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
        <v-sheet :color="colors[i]" height="100%" tile>
          <v-row class="fill-height" align="center" justify="center">
            <div class="text-h2">{{ slide }} Slide</div>
          </v-row>
          <v-row justify="center">
            <v-btn
              to="0"
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
              <v-list> </v-list>
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
        <h1>最新提问 <v-btn to="list" color="primary">查看所有</v-btn></h1>
        <v-card :to="issue.id" v-for="issue in issueList" :key="issue.id">
          <v-card-title>{{ issue.title }}</v-card-title>
          <v-card-content>
            {{ issue.content }}
          </v-card-content>
          <v-card-actions> 作者：{{ issue.author }} </v-card-actions>
        </v-card>
      </v-row>
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
    };
  },
  methods: {
    async doGetIssueList() {
      this.issueList = (await getIssueList())?.issues;
    },
  },
  mounted() {
    this.doGetIssueList();
  },
};
</script>