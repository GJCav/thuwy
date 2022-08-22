import Vue from 'vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import App from './App.vue';

Vue.config.productionTip = false;

const prevHandler = Vue.config.errorHandler;
Vue.config.errorHandler = (err, vm, info) => {
  store.dispatch('showMessage', { message: err });
  prevHandler && prevHandler(err, vm, info);
};

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app');
