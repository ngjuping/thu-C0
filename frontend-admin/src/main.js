import Vue from 'vue';
import App from './App.vue';
import store from './store';
import router from './router';
import axios from 'axios';
import { makeServer } from "./server";
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faArrowCircleRight,faStar,faAngleUp } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faArrowCircleRight,faStar,faAngleUp)

Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.productionTip = false
Vue.prototype.$axios = axios

if(process.env.NODE_ENV == "development")
{
  makeServer();
} 

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
