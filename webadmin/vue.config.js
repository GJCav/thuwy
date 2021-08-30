module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  configureWebpack: {
    externals: {
      vue: 'Vue',
      vuetify: 'Vuetify',
      'vue-router': 'VueRouter',
      vuex: 'Vuex',
      axios: 'axios',
      marked: 'marked'
    }
  }
};
