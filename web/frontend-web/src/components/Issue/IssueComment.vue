<template>
  <v-list-item>
    <!-- Image -->
    <v-list-item-avatar class="align-self-start">
      <img src="@/assets/wy_blue.png" />
    </v-list-item-avatar>
    <!-- Nickname Comment Reply... -->
    <v-list-item-content>
      <v-list-item-title class="font-weight-black grey--text text--darken-1">{{
        nickname
      }}</v-list-item-title>
      <v-list-item-subtitle class="text-body-1 grey--text pt-1">{{
        content
      }}</v-list-item-subtitle>
      <v-list-item-subtitle class="mt-3">
        <v-chip color="error" outlined label small class="mr-2">置顶</v-chip>
        <v-chip color="warning" outlined label small class="mr-2"
          >作者赞过</v-chip
        >
        <span class="mr-2">{{ time }}</span>
        <v-hover v-slot="{ hover }">
          <a
            class="mr-2"
            :class="{ 'grey--text text--darken-1': !hover }"
            @click="reply = !reply"
            >回复</a
          >
        </v-hover>
      </v-list-item-subtitle>
      <v-list-item-subtitle>
        <send-comment v-if="reply"></send-comment>
      </v-list-item-subtitle>
      <!-- <v-list-item-subtitle>展开更多评论</v-list-item-subtitle> -->
    </v-list-item-content>
  </v-list-item>
</template>

<script>
import SendComment from "@/components/Issue/SendComment.vue";
export default {
  name: "IssueComment",
  components: { SendComment },
  data: () => ({
    reply: false,
    nickname: "WEI XIAO YANG",
    content: "评论的内容",
    time: "2 hours ago",
  }),
};
</script>

<style>
</style>