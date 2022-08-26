<template>
  <v-list-item>
    <!-- Icon -->
    <v-list-item-avatar size="45" class="align-self-start">
      <v-img src="@/assets/wy_blue.png"></v-img>
    </v-list-item-avatar>
    <!-- Text -->
    <v-list-item-content>
      <v-list-item-title>
        <v-text-field
          v-model="issueTitle"
          counter="25"
          hint="请在此输入标题"
          label="New Title"
        ></v-text-field>
      </v-list-item-title>
      <v-list-item-title>
        <editor v-model="issueText"></editor>
      </v-list-item-title>
      <!-- tags -->
      <v-list-item-subtitle class="py-2">
        <template>
          <v-card class="my-2">
            <v-skeleton-loader :loading="loading" type="card">
              <v-card-text>
                <div class="d-flex align-center mt-2">
                  <h3 class="d-inline-block">标签：</h3>

                  <!-- 一系列标签 chips -->
                  <v-menu
                    v-for="tag in tags"
                    :key="tag.key"
                    transition="slide-y-transition"
                    bottom
                    :offset-y="true"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-chip
                        class="mx-2 pr-1"
                        color="cyan"
                        outlined
                        v-bind="attrs"
                        v-on="on"
                      >
                        {{ tag }}
                        <v-menu
                          :offset-y="true"
                          transition="scroll-y-transition"
                        >
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn icon small v-bind="attrs" v-on="on">
                              <v-icon>mdi-close-circle-outline</v-icon>
                            </v-btn>
                          </template>

                          <v-btn color="error" @click="delTag(tag)">
                            Sure to delete?
                          </v-btn>
                        </v-menu>
                      </v-chip>
                    </template>
                  </v-menu>

                  <!-- 添加标签 -->
                  <v-menu
                    transition="slide-x-transition"
                    right
                    :offset-x="true"
                    :close-on-content-click="false"
                    :close-on-click="true"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        icon
                        color="cyan"
                        outlined
                        small
                        v-bind="attrs"
                        v-on="on"
                        :loading="add_tag_loading"
                        :disabled="add_tag_loading"
                      >
                        <v-icon>mdi-plus</v-icon>
                      </v-btn>
                    </template>
                    <v-card>
                      <v-card-title>添加标签：</v-card-title>
                      <v-divider></v-divider>
                      <v-card-text class="my-0">
                        <v-text-field
                          class="my-0"
                          label="Tag: "
                          prepend-icon="mdi-key"
                          append-icon="mdi-check"
                          v-model="add_tag"
                          @click:append="addTag"
                        ></v-text-field>
                      </v-card-text>
                    </v-card>
                  </v-menu>
                </div>
              </v-card-text>
            </v-skeleton-loader>
          </v-card>
        </template>
      </v-list-item-subtitle>
    </v-list-item-content>
    <!-- Send Button -->
    <v-list-item-action class="align-self-start">
      <v-btn @click="doCreateIssue()" height="66" color="info">发送</v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
import Editor from "@/components/Issue/Editor.vue";
import { createIssue } from "@/api/issue.js";

export default {
  name: "SendIssue",
  data: () => ({
    loading: false,
    tabValue: 1,
    issueText: "",
    issueTitle: "",
    visibility: "public",
    tags: [],
    add_tag: "",
    add_tag_loading: false
  }),
  props: ["reply_id"],
  methods: {
    async addTag() {
      this.add_tag_loading = true;
      if (this.add_tag !== "") {
        this.tags.push(this.add_tag);
        this.loading = false;
        for (let i = 0; i < this.tags.length; i++) {
          for (let j = i + 1; j < this.tags.length; j++) {
            if (this.tags[i] === this.tags[j]) {
              this.tags.splice(j, 1);
              j--;
            }
          }
        }
      }
      this.add_tag_loading = false;
      this.add_tag = "";
    },
    async delTag(tag) {
      this.tags.forEach(function(item, index, arr) {
        if (item === tag) {
          arr.splice(index, 1);
        }
      });
    },
    async doCreateIssue() {
      if (this.issueTitle !== "" && this.issueText !== "") {
        var id;
        if (this.reply_id === 0) {
          id = await createIssue({
            title: this.issueTitle,
            content: {
              text: this.issueText
            },
            tags: this.tags.join(";"),
            visibility: "public"
          });
          this.$router.push(`/issue/${id}`);
        } else {
          id = await createIssue({
            title: this.issueTitle,
            content: {
              text: this.issueText
            },
            reply_to: this.reply_id,
            tags: this.tags.join(";"),
            visibility: "public"
          });
          this.$router.go(0);
        }
      }
    }
  },
  components: { Editor }
};
</script>
