<template>
  <div id="app" ref="app_top">
    <Qheader></Qheader>
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

/* basic positioning */
.legend { list-style: none; }
.legend li { float: left; margin-right: 10px; }
.legend span { border: 1px solid #ccc; float: left; width: 12px; height: 12px; margin: 2px; }

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

blockquote {
    border-left: 3px solid rgba(0, 0, 0, .1);
    color: rgba(0, 0, 0, .8);
    padding-left: .8rem;
    font-style: italic;
}

blockquote:first-child {
    margin-top: 0;
}

blockquote:last-child {
    margin-bottom: 0;
}

.modal-backdrop {
   background: none !important;
}

</style>
