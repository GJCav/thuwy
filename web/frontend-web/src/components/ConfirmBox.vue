<template>
  <v-dialog
    :value="show"
    @input="$emit('input', $event)"
    max-width="290"
    :persistent="persistent"
  >
    <v-card>
      <v-card-title class="text-h5">
        {{ title }}
      </v-card-title>
      <v-card-text v-if="edit"
        ><v-textarea
          @input="$emit('update', $event)"
          :value="editDefault"
          :label="text"
          outlined
        ></v-textarea
      ></v-card-text>
      <v-card-text v-else>{{ text }}</v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="error darken-1" text @click="fail"> 取消 </v-btn>
        <v-btn color="success darken-1" text @click="success"> 确认 </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  methods: {
    success() {
      this.$emit('input', false);
      this.$emit('confirm', true);
    },
    fail() {
      this.$emit('input', false);
      this.$emit('confirm', false);
    },
  },
  model: {
    prop: 'show',
    event: 'input',
  },
  props: {
    title: String,
    text: String,
    persistent: Boolean,
    show: Boolean,
    editDefault: String,
    edit: {
      type: Boolean,
      default: false,
    },
  },
};
</script>