import Vue from 'vue';
import App from './App.vue';
import store from './vuex';
import router from './router';
import vuetify from './vuetify';

Vue.config.productionTip = false;

const vue = new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');