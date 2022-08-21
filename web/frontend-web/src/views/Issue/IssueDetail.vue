<template>
  <v-col lg="8" offset-lg="2" cols="12" offset="0">
    <h1>{{ id == 0 ? "新建Issue" : `查看Issue#${id}细节` }}</h1>
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
              <v-card-title class="text-h6"> Lorem Ipsum Dolor </v-card-title>
              <v-card-text class="white text--primary">
                <p>
                  Lorem ipsum dolor sit amet, no nam oblique veritus. Commune
                  scaevola imperdiet nec ut, sed euismod convenire principes at.
                  Est et nobis iisque percipit, an vim zril disputando
                  voluptatibus, vix an salutandi sententiae.
                </p>
                <v-btn :color="item.color" class="mx-0" outlined>
                  Button
                </v-btn>
              </v-card-text>
            </v-card>
          </v-timeline-item>
        </v-timeline>
      </v-col>
      <v-col cols="2">
        <h3>Labels</h3>
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
import { getIssue } from '@/api/issue';

export default {
  data() {
    return {
      issue: null,
      items: [
        {
          color: 'red lighten-2',
          icon: 'mdi-star',
        },
        {
          color: 'purple darken-1',
          icon: 'mdi-book-variant',
        },
        {
          color: 'green lighten-1',
          icon: 'mdi-airballoon',
        },
        {
          color: 'indigo',
          icon: 'mdi-buffer',
        },
      ],
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