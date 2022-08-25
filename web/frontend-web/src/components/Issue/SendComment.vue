<template>
  <v-list-item>
    <!-- Icon -->
    <v-list-item-avatar size="45" class="align-self-start">
      <v-img src="@/assets/wy_blue.png"></v-img>
    </v-list-item-avatar>
    <!-- Text -->
    <v-list-item-content>
      <v-list-item-title>
        <!-- <v-textarea
          id="commentInput"
          outlined
          rows="2"
          no-resize
          hide-details
          v-model="commentText"
        >
        </v-textarea> -->
        <editor v-model="commentText"></editor>
      </v-list-item-title>
      <!-- Emoji -->
      <v-list-item-subtitle class="py-2">
        <v-menu offset-y :close-on-content-click="false">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="#FFFFFF" small v-bind="attrs" v-on="on">
              <v-icon>mdi-emoticon-outline</v-icon>
              表情
            </v-btn>
          </template>
          <v-sheet width="500">
            <v-container>
              <v-tabs v-model="tabValue">
                <v-tab-item>2</v-tab-item>
              </v-tabs>
            </v-container>
          </v-sheet>
        </v-menu>
      </v-list-item-subtitle>
    </v-list-item-content>
    <!-- Send Button -->
    <v-list-item-action class="align-self-start">
      <v-btn height="66" color="info">发送</v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
import Editor from '@/components/Issue/Editor.vue';

export default {
  name: "SendComment",
  data: () => ({
    emojis: [],
    tabValue: 1,
    commentText: "",
  }),
  components: { Editor }
};
</script>