import Vue from 'vue'
import Vuex from 'vuex'
import moment from 'moment'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    logged_in:false,
    logged_in_user_id:"Nobody",
    logged_in_time:"Notime"
  },
  mutations: {
    login(state,logged_in_user_id){
      state.logged_in = true;
      state.logged_in_user_id = logged_in_user_id;
      state.logged_in_time = moment().format(); 
    },
    logout(state){
      state.logged_in = false;
      state.logged_in_user = "Nobody";
      state.logged_in_time = "Notime";
    }
  },
  actions: {
  },
  modules: {
  }
})
