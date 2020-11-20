<template>
  <div id="app">
    <Qheader></Qheader>
    <div id="nav">
    </div>
    <router-view/>
    <Qfooter></Qfooter>
  </div>
</template>
<script>
import Qheader from '@/components/Qheader.vue'
import Qfooter from '@/components/Qfooter.vue'

export default {
  components:{
    Qheader,
    Qfooter
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
</style>
