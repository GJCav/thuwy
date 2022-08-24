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
            <v-card :color="item.color" dark>
              <v-card-title class="text-h6"> {{ item.title }} </v-card-title>
              <v-card-text class="white text--primary">
                <p>
                  {{ item.content }}
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
        <v-chip-group column active-class="warning">
          <v-chip
            outlined
            small
            class="ma-2"
            color="cyan"
            ripple
            v-for="label in labels"
            :key="label.id"
            :value="label.id"
            >{{ label.name }}</v-chip
          >
        </v-chip-group>
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
import { getIssue } from "@/api/issue";
import SendComment from "../../components/Issue/SendComment.vue";
// import IssueComment from "../../components/Issue/IssueComment.vue";

export default {
  components: { SendComment },
  data() {
    return {
      issue: null,
      items: [
        {
          color: "red lighten-2",
          icon: "mdi-star",
          title: "卷",
          content: `未央大卷院，是兄弟就来卷我`
        },
        {
          color: "purple darken-1",
          icon: "mdi-book-variant",
          title: `乐`,
          content: "别在这理发店"
        },
        {
          color: "green lighten-1",
          icon: "mdi-airballoon",
          title: `躺平`,
          content: "卷不动了，开摆开摆"
        }
      ],
      labels: [
        {
          id: 1,
          name: "内卷"
        },
        {
          id: 2,
          name: "躺平"
          },
        {
          id: 3,
          name: "未央"
          },
        {
          id: 4,
          name: "长乐"
        },
      ]
    };
  },
  methods: {
    async doGetIssue() {
      this.issue = await getIssue(this.id, this.$store.state.session);
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
