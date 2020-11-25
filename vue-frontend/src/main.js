import Vue from 'vue';
import App from './App.vue';
import store from './store';
import router from './router';
import axios from 'axios';
<<<<<<< HEAD
import { makeServer } from "./server";
=======
//import { makeServer } from "./server";
>>>>>>> 3b88c374a7e3d91ea0709ac264af5bd2a7aaa013
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap/dist/css/bootstrap.min.css';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faArrowCircleRight,faStar,faAngleUp } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faArrowCircleRight,faStar,faAngleUp)

Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.config.productionTip = false
Vue.prototype.$axios = axios
axios.defaults.baseURL="http://127.0.0.1:8000/"
/*
if(process.env.NODE_ENV == "development")
{
  makeServer();
} 
*/
new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
