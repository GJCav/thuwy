<template>
  <v-col md="8" offset-lg="2" cols="12" offset="0">
    <h1>答疑列表</h1>
    <v-row>
      <v-col md="6" cols="12">
        <v-text-field
          :loading="loading"
          prepend-inner-icon="mdi-magnify"
          outlined
          clearable
          label="搜索"
        ></v-text-field>
      </v-col>
      <v-col md="3" cols="6">
        <v-btn
          :loading="loading"
          block
          @click="labelListExpand = !labelListExpand"
          >Labels</v-btn
        >
      </v-col>
      <v-col md="3" cols="6">
        <v-btn :loading="loading" to="/issue/0/" color="success" block
          >new issue</v-btn
        >
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
    <v-row>
      <v-col cols="12" md="4"
        ><v-select :loading="loading" outlined label="Author"></v-select
      ></v-col>
      <v-col cols="12" md="4"
        ><v-select :loading="loading" outlined label="Label"></v-select
      ></v-col>
      <v-col cols="12" md="4"
        ><v-select :loading="loading" outlined label="Sort"></v-select
      ></v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" md="6" md-offset="3">
        <v-card
          :color="randColor()"
          class="mt-5"
          :to="`/issue/${issue.id}/`"
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
      labelListExpand: false,
      loading: false
    };
  },
  methods: {
    async doGetIssueList() {
      this.loading = true;
      try {
        this.issueList = (await getIssueList({ page: 1 }))?.issues;
      } catch (e) {
        this.loading = false;
        throw (e);
      }
      this.loading = false;
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
  }
};
</script>