<template>
<div>
  <v-skeleton-loader v-if="loading" type="card"></v-skeleton-loader>
  <v-card v-else>
    <v-card-title>
      <span class="headline">{{ title }}</span>
    </v-card-title>
    <v-divider class="mb-4"></v-divider>
    <v-card-text class="text--primary py-0">
      <v-autocomplete v-model="selected" :items="scopes" item-value="name" item-text="name" chips deletable-chips
        prepend-icon="mdi-key" label="Privilege" multiple>
        <template v-slot:item="data">
          <v-list-item-content>
            <v-list-item-title>{{ data.item.name }}</v-list-item-title>
            <v-list-item-subtitle>{{ data.item.description }}</v-list-item-subtitle>
          </v-list-item-content>
        </template>
      </v-autocomplete>
      <v-menu v-model="date_picker.show" :disabled="!date_picker.enable" :close-on-content-click="false"
        transition="scale-transition" offset-y min-width="290px">
        <template v-slot:activator="{ on, attrs }">
          <v-row class="ma-0">
            <v-text-field v-model="date_picker.date" label="Expire Date" prepend-icon="event" readonly v-bind="attrs"
              v-on="on" :disabled="!date_picker.enable"></v-text-field>
            <v-checkbox v-model="date_picker.enable"></v-checkbox>
          </v-row>
        </template>
        <v-date-picker locale="zh-cn" v-model="date_picker.date" @input="date_picker.show = false"></v-date-picker>
      </v-menu>

    </v-card-text>
    <v-card-actions class="">
      <v-spacer></v-spacer>
      <v-btn 
        color="warning" 
        class="mr-2 mb-2"
        @click="confirm"
      >
        Confirm
      </v-btn>
    </v-card-actions>
    
    <slot name="bottom"></slot>
  </v-card>
</div>
</template>

<script>
import * as auth from "../backend-api/auth"
import ErrorDialog from "./ErrorDialog.vue";

export default {
  name: "ScopePicker",

  props: {
    title: { type: String, default: "选择权限" },
  },

  data: () => ({
    loading: true,

    selected: [],
    scopes: [],
    date_picker: {
      show: false,
      enable: false,
      date: null
    }
  }),

  methods: {
    confirm() {
      this.$emit("confirm", {
        expire_at: (
          this.date_picker.enable ? 
            this.date_picker.date : null
        ),
        scopes: this.selected
      });
      this.selected = [];
    },

    async loadData() {
      this.loading = true;
      try {
        const json = await auth.fetchAllScope({
            session: this.$store.getters.session
        });
        if (json.code !== 0) {
            throw new Error(json.errmsg);
        }
        this.scopes = json.scopes;
      }
      catch (e) {
        this.scopes = [{ name: "ERROR: " + e.message + "。请稍后重试"}]
      }
      this.loading = false;
    }
  },

  mounted() {
    this.loadData();
  },
}
</script>