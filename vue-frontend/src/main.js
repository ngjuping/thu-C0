import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import axios from 'axios';
import { makeServer } from "./server"
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

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
