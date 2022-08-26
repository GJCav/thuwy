<template>
  <v-col 
  md="8" 
  offset-lg="2" 
  cols="12" 
  offset="0">
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
      <v-col md="2" cols="4">
        <v-btn :loading="loading" color="primary" block>search</v-btn>
      </v-col>
      <v-col md="2" cols="4">
        <AddLabel
          :labelList="labelList"
          @pushLabel="deleteLabel"
          @addLabel="addLabel"
        />
      </v-col>
      <v-col md="2" cols="4">
        <v-btn :loading="loading" to="/issue/0/" color="success" block
          >new issue</v-btn
        >

      </v-col>
      <v-col 
      cols="12"
      >
        <v-expand-transition>
          <v-card 
          v-show="labelListExpand"
          >
            <v-card-title> Label列表 </v-card-title>
            <span 
            v-for="label in labelList" 
            :key="label"
            >
              {{ label }}
            </span>
          </v-card>
        </v-expand-transition>
      </v-col>
    </v-row>
    <v-row justify="center">

      <v-col 
      cols="12" 
      md="4">
        <v-select
          label="Author"
          :loading="loading"
          outlined
          :items="authors"
          v-model="selectedAuthor"
          clearable
        ></v-select>
      </v-col>
      <v-col 
      cols="12" 
      md="4">
        <v-select
          label="Label"
          :loading="loading"
          outlined
          :items="labelList"
          v-model="selectedLabel"
          multiple
          clearable
        ></v-select>
      </v-col>
      <v-col 
      cols="12" 
      md="4">
        <v-select
          label="Sort"
          :loading="loading"
          outlined
          :items="sorts"
          v-model="selectedSort"
          clearable
        ></v-select>
      </v-col>
    </v-row>
    <v-card
      :color="randColor()"
      :to="`/issue/${issue.id}/`"
      v-for="issue in issueList"
      :key="issue.id"
      class="my-5"
    >
      <v-row 
      align="center"
      >
        <v-col 
        cols="2"
        >
          <v-icon 
          class="mx-5 green--text"
            >mdi-map-marker-question-outline</v-icon
          >
        </v-col>
        <v-col 
        cols="6"
        >
          <div>
            <h2>{{ issue.title }}</h2>
          </div>

          <span class="subtitle-2">{{ issue.author }}</span>
        </v-col>
        <v-col 
        cols="3"
        >
            <span 
            class="grey--text caption"
            >{{ issue.date }}</span>
            <br>
          <span 
          class="black--text caption"
          >Last msg:{{ issue.last_modified_at }}</span>
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
import axios from 'axios';
import 'animate.css';
import AddLabel from '@/components/Issue/AddLabel';

export default {
  components: { AddLabel },
  name: 'IssueList',
  data() {
    return {
      issueList: [{title:'This is a question', id:1, content:'Who are you?', author:'张三', date:'XX.XX.XX', last_modified_at:'xx.xx.xx'}, {title:'Why is the Earth round?', id:1, content:'As far as we know, ...', author:'李四',date:'XX.XX.XX', last_modified_at:'xx.xx.xx'},{title:'Why is the Earth round?', id:1, content:'As far as we know, ...', author:'李四',date:'XX.XX.XX', last_modified_at:'xx.xx.xx'},{title:'Why is the Earth round?', id:1, content:'As far as we know, ...', author:'李四',date:'XX.XX.XX', last_modified_at:'xx.xx.xx'}],
      labelList: ['C++', 'python', 'JavaScript', 'HTML'],
      authors: ['all', 'system', 'teacher', 'stusent'],
      sorts:['date', 'ID', 'popularity'],
      selectedAuthor: '',
      selectedLabel: '',
      selectedSort:'',
      labelListExpand: false,
      keywords:''

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
    deleteLabel(par) {
      console.log(par);
      let getLocation = this.labelList.indexOf(par);
      this.labelList.splice(getLocation, 1);
    },
    addLabel(par) {
      this.labelList.push(par);
    },
    search() {
      var author;
      author = this.selectedAuthor;
      if (this.authors == 'all')
        author = '';
      var searchLabel = '';
      for (let i = 0, len = this.selectedLabel.length; i < len; i++) {
        searchLabel += this.selectedLabel[i];
        searchLabel += ' ';
      }
      console.log(this.keywords, author, searchLabel, this.selectedSort);
      alert();
      axios.get('http://dev-api.thuwy.top/issue/', {
        params: {
          keywords: this.keywords,
          authors: author,
          tags: searchLabel,
          sort_by: this.selectedSort
        }
      }
      ).then(
        response => {
          console.log('成功了', response.data);
          this.issueList = (JSON.parse(response.data)).issues;
        },
        error => {
          console.log('失败了', error)
          alert('搜索失败，请检查网络，按要求重新搜索')
        }
      )
    },
      randColor() {
        var r = Math.floor(Math.random() * 32) + 224;
        var g = Math.floor(Math.random() * 32) + 224;
        var b = Math.floor(Math.random() * 32) + 224;
        return `#${r.toString(16)}${g.toString(16)}${b.toString(16)}`
      },
    
  
    mounted() {
    this.doGetIssueList();
    }
  }
};
</script>
