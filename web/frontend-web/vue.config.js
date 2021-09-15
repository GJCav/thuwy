module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  configureWebpack: {
    externals: {
      axios: 'axios',
      marked: 'marked'
    }
  }
};
