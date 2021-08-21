<template>
  <v-dialog
    @click:outside="$emit('input', $event.target.show)"
    @input="$emit('input', $event.target.show)"
    @keydown="$emit('input', $event.target.show)"
    :value="show"
  >
    <v-card>
      <v-card-title>假装这里是二维码</v-card-title>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    show: Boolean,
  },
  model: {
    prop: 'show',
    event: 'input',
  },
};
</script>