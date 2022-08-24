<template>
  <v-col md="8" offset-lg="2" cols="12" offset="0">
    <h1>答疑列表</h1>
    <v-row>
      <v-col md="6" cols="12">
        <v-text-field label="搜索"></v-text-field>
      </v-col>
      <v-col md="2" cols="4">
        <v-btn block color="blue" class="white--text">Search</v-btn>
      </v-col>
      <v-col md="2" cols="4">
        <AddLabel :labelList="labelList" @pushLabel="deleteLabel" @addLabel="addLabel"/> 
      </v-col>
      <v-col md="2" cols="4">
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
      <v-select label="Author" :items="authors" v-model="selectedAuthor"></v-select>
      <v-select label="Label" :items="labelList" v-model="selectedLabel" multiple></v-select>
      <v-select label="Sort" :items="sorts" v-model="selectedSort"></v-select>

    </v-row>
      <v-card :to="issue.id" v-for="(issue) in issueList" :key="issue.id" class="grey lighten-3 my-5">
        <v-row align="center">
          <v-col cols="2" >
            <v-icon class="mx-5 green--text" >mdi-map-marker-question-outline</v-icon>
            
          </v-col>
          <v-col cols="9">
            <div>
              <h2>{{issue.title}}</h2>
            </div>
            
              <span class="subtitle-2">{{issue.author}}</span>
          </v-col>
          <v-col cols="1">
            <v-chip small class="green lighten-1">
              <span class="white--text">1</span> 
            </v-chip>
          </v-col>
        </v-row>
      </v-card>
    
  </v-col>
  

</template>

<script>
import { getIssueList } from '@/api/issue.js';
import AddLabel from './AddLabel';

export default {
  components: {AddLabel},
  name: 'IssueList',
  data() {
    return {
      issueList: [{title:'This is a question', id:1, content:'Who are you?', author:'张三'}, {title:'Why is the Earth round?', id:1, content:'As far as we know, ...', author:'李四'},{title:'Why is the Earth round?', id:1, content:'As far as we know, ...', author:'李四'},{title:'Why is the Earth round?', id:1, content:'As far as we know, ...', author:'李四'}],
      labelList: ['C++', 'python', 'JavaScript', 'HTML'],
      authors: ['all', '张三', '李四'],
      selectedAuthor: '',
      selectedLabel: '',
      selectedSort:'',
      labelListExpand: false
    };
  },
  methods: {
    async doGetIssueList() {
      this.issueList = (await getIssueList({ page: 1 }))?.issues;
    },
    deleteLabel(par) {
      console.log(par);
      let getLocation = this.labelList.indexOf(par);
      this.labelList.splice(getLocation, 1);
    },
    addLabel(par) {
      this.labelList.push(par);
    }
  },
  mounted() {
    this.doGetIssueList();
  }
};
</script>