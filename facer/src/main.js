import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store/store";
import axios from "axios";

import '@stout/vue-dashed-spinner';
import BootstrapVue from 'bootstrap-vue'

Vue.use(BootstrapVue)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.prototype.$axios = axios;
Vue.config.productionTip = false;


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
