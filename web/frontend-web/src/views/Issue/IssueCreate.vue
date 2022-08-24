<template>
  <v-col lg="8" offset-lg="2" cols="12" offset="0">
    <h1>新建Issue</h1>
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
                  {{ item.content }}
                </p>
                <v-btn :color="item.color" class="mx-0" outlined>
                  Button
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
            label
            color="success"
            v-for="label in labels"
            :key="label.id"
            :value="label.id"
          >
            {{ label.name }}
          </v-chip>
        </v-chip-group>
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
import SendComment from "../../components/Issue/SendComment.vue";

export default {
  components: { SendComment },
  data() {
    return {
      issue: {
        title: "",
        content: "",
        tag: []
      },
    };
  },
};
</script>
