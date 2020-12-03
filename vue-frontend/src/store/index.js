import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'
Vue.use(Vuex)

// stored in localStorage, can get using localStorage.getItem("vuex")
const vuexLocal = new VuexPersistence({
  storage: window.localStorage
})

// use this.$store.state.XXX to access the variables
export default new Vuex.Store({
  state: {
    logged_in:false, // use this variable to check log in status
    logged_in_user_id:-1,
    logged_in_user_name:"no-name",
    privilege:-1, // use this variable to check user type
    reservationStatus:["成功预约未付款","已付款","已取消","已转让","未抽签","已抽签","队列中"],
    courtStatus:["无状态","空场地","已有人预定"],
    sportsType:["清除过滤","羽球","乒乓","网球","篮球"],
  },
  mutations: {
    login(state,logged_in_user_info){
      state.logged_in = true;
      state.logged_in_user_id = logged_in_user_info.user_id;
      state.logged_in_user_name = logged_in_user_info.name;
      state.privilege = logged_in_user_info.privilege;
    },
    logout(state){
      state.logged_in = false;
      state.logged_in_user_id = -1;
      state.logged_in_user_name = "no-name";
      state.privilege = -1;
    }
  },
  plugins:[vuexLocal.plugin]
})
