<template>
  <div>
    <LoginForm/>
  </div>
</template>

<script>
// @ is an alias to /src
import LoginForm from '@/components/LoginForm.vue'
import moment from 'moment'

export default {
  components: {
    LoginForm
  },
  methods:
  {
  },
  mounted()
  {
    // Test axios api calls if it works
    this.$axios.get('/api/v1/hello').then(res => console.log(res));
  },
  computed:{
    // Test moment js if it works
    now(){
      let now_js = moment().format();  
      let first_half = now_js.split("T")[0];
      let second_half_time = now_js.split("T")[1].split("+")[0];
      
      return moment(first_half + " " + second_half_time,"YYYY-MM-DD hh:mm:ss").fromNow();
    }
  }
}
</script>
