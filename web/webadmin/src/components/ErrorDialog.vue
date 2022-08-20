<template>
<v-dialog
    transition="dialog-transition"
    max-width="384px"
    :value="enable"
    @click:outside="dialogClose"
  >
  <v-card>
  <v-card-title class="headline">{{title}}</v-card-title>
  <v-card-text>{{msg}}</v-card-text>
  <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="warning" @click="dialogClose">Continue</v-btn>
  </v-card-actions>
  </v-card>
</v-dialog>
</template>


<script>
export default {
  name: "ErrorDialog",
  props: {
    enable: { type: Boolean, default: false },
    title: { type: String, default: "Error" },
    msg: { type: String, default: ""}
  },
  model: { prop: "enable", event: "dialogChange" },
  methods: {
    dialogClose() { 
      this.$emit("dialogChange", false)
    }
  }
}
</script>