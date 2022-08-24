<template>
  <div class="text-center">
    <v-dialog v-model="dialog" max-width="600">
      <template v-slot:activator="{ on, attrs }">
        <v-btn v-bind="attrs" v-on="on" block> Label </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5 green darken-2 white--text">
          Edit Labels Here
        </v-card-title>
        <v-container>
          <v-row>
            <v-col cols="8">
              <v-text-field v-model="newLabel" class="mx-2"></v-text-field>
            </v-col>

            <v-col cols="3">
              <v-btn
                block
                @click="
                  $emit('addLabel', newLabel);
                  newLabel = '';
                "
                class="blue white--text"
              >
                <span>add label</span>
              </v-btn>
            </v-col>
            <v-col>
              <v-chip
                v-for="label in labelList"
                :key="label"
                class="mx-1 yellow lighten-3 my-1"
              >
                <span>{{ label }}</span>
                <v-icon
                  right
                  class="mb-3 red--text"
                  @click="$emit('pushLabel', label)"
                  >mdi-close-circle</v-icon
                >
              </v-chip>
            </v-col>
          </v-row>
        </v-container>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="red" text @click="dialog = false"> Close </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialog: 0,
      labels: [],
      newLabel: ''
    };
  },
  props: {
    labelList: Array
  },
  methods: {
    remove(par) {
      this.$emit('pushLabel', par);
    }
  }

};
</script>