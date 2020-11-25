<template>
  <div id="app" ref="app_top">
    <Qheader></Qheader>
    <div id="nav">
    </div>
    <router-view/>
    <Qfooter></Qfooter>
    <div id="gotoTop" class="shadow d-flex justify-content-center align-items-center" @click="scrollToTop()">
        <font-awesome-icon icon="angle-up" class="text-white" id="up"/>
    </div>
  </div>
</template>
<script>
import Qheader from '@/components/Qheader.vue'
import Qfooter from '@/components/Qfooter.vue'
let smoothScroll = require('smoothscroll');

export default {
  components:{
    Qheader,
    Qfooter
  },
  methods:{
        scrollToTop(){
            smoothScroll(this.$refs["app_top"]);
        }
    }
}
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-image:url("assets/prototype_bg.jpg");
  background-size:100%;
  background-repeat:no-repeat;
  
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

#gotoTop{
    position:fixed;
    bottom:20px;
    right:20px;
    width:60px;
    height:60px;
    border-radius:30px;
    background-color:grey;
    font-size:40px;
    cursor:pointer;
    opacity:0.7
}

#gotoTop:hover{
    opacity:1;
}

</style>
