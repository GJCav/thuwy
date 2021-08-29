<template>
  <v-app>
    <router-view />
    <v-snackbar
      dark
      color="deep-purple accent-1"
      app
      @input="$store.commit('updateSnackbarStatus', false)"
      :value="$store.state.snackbar"
      :timeout="$store.state.snackbarTimeout"
      ><b>{{ $store.state.snackbarMsg }}</b
      ><template
        v-if="$store.state.snackbarTimeout === 0"
        v-slot:action="{ attrs }"
      >
        <v-btn
          color="yellow yellow darken-1"
          text
          v-bind="attrs"
          @click="$store.commit('updateSnackbarStatus', false)"
          >关闭</v-btn
        >
      </template></v-snackbar
    >
  </v-app>
</template>

<script>
export default {
  name: 'App',

  data: () => ({
    //
  }),
  created() {
    this.$store.dispatch('refreshProfile');
  },
};
</script>
