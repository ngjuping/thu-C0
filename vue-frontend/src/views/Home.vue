<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>

    <div class="container">
      <div class="row">
        <div class="card col">
          <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <small v-text="now"></small>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
          </div>
        </div>
        <div class="card col">
          <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <small v-text="now"></small>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
          </div>
        </div>
        <div class="card col">
          <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <small v-text="now"></small>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
          </div>
        </div>
        <div class="card col">
          <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <small v-text="now"></small>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import moment from 'moment'

export default {
  name: 'Home',
  components: {
    HelloWorld
  },
  mounted()
  {
      this.$axios.get('/api/v1/hello').then(res => console.log(res));
  },
  computed:{
    now(){
      let now_js = moment().format();  
      let first_half = now_js.split("T")[0];
      let second_half_time = now_js.split("T")[1].split("+")[0];
      
      return moment(first_half + " " + second_half_time,"YYYY-MM-DD hh:mm:ss").fromNow();
    }
  }
}
</script>
