<template>
  <v-col md="8" offset-lg="2" cols="12" offset="0">
    <h1>答疑列表</h1>
    <v-row>
      <v-col md="6" cols="12">
        <v-text-field label="搜索"></v-text-field>
      </v-col>
      <v-col md="3" cols="6">
        <v-btn block @click="labelListExpand = !labelListExpand">Labels</v-btn>
      </v-col>
      <v-col md="3" cols="6">
        <v-btn to="0" color="success" block>new issue</v-btn>
      </v-col>
      <v-col cols="12">
        <v-expand-transition>
          <v-card v-show="labelListExpand">
            <v-card-title> Label列表 </v-card-title>
            <span v-for="label in labelList" :key="label">
              {{ label }}
            </span>
          </v-card>
        </v-expand-transition>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-select label="Author"></v-select>
      <v-select label="Label"></v-select>
      <v-select label="Sort"></v-select>
      <v-card :to="issue.id" v-for="issue in issueList" :key="issue.id">
        <v-card-title>{{ issue.title }}</v-card-title>
        <v-card-content>
          {{ issue.content }}
        </v-card-content>
        <v-card-actions> 作者：{{ issue.author }} </v-card-actions>
      </v-card>
    </v-row>
  </v-col>
</template>

<script>
import { getIssueList } from '@/api/issue.js';

export default {
  name: 'IssueList',
  data() {
    return {
      issueList: [],
      labelList: [],
      labelListExpand: false
    };
  },
  methods: {
    async doGetIssueList() {
      this.issueList = (await getIssueList({ page: 1 }))?.issues;
    }
  },
  mounted() {
    this.doGetIssueList();
  }
};
</script>