<template>
<div class="form_container d-flex justify-content-center">
  <div class="card w-25 shadow p-4">
      <div class="card-img-top w-100 d-flex justify-content-center">
        <img src="@/assets/logo.png">
      </div>
      
      <form class="card-body h-50 pb-5">
          <div class="form-group">
            <label >User ID</label>
            <input class="form-control" :disabled="logging_in" v-model="userid" :required="userid===''">
            <small class="form-text text-muted">Glad to see you back {{userid}}</small>
          </div>

          <div class="form-group">
            <label >Password</label>
            <input type="password" class="form-control" required :disabled="logging_in" v-model="password">
          </div>
          
          <button type="submit" class="btn btn-primary text-white" @click.prevent="login" v-show="!logging_in" autofocus>Submit</button>
          
          <button class="btn btn-primary" v-show="logging_in" disabled>
          <span class="spinner-border spinner-border-sm"></span>
          Loggin in...
          </button>
        </form>
  </div>
</div>
</template>

<script>
import Swal from 'sweetalert2'
import moment from 'moment'

export default {
  data()
  {
    return {
      userid: "admin",
      password: "123456",
      logging_in: false
    }
  },
  methods:{
    login(){
      this.logging_in = true;
      this.$axios
      .post('/api/v1/login',{
          user_id: this.userid,
          password: this.password
        }
      )
      .then(res => 
      {
        this.$store.state.logged_in_time = moment().format(); 
        this.$router.push({name:'Mainpage'});
        this.logging_in = false;
        let data = res.data
        Swal.fire({
          title: "Welcome! " + data.nickname,
          text: "You have been logged in.",
          icon: "success",
          timer: 1000}
        );
      })
      .catch(()=>{
        this.logging_in = false;
        Swal.fire({
          title: "Wrong credentials",
          text: "Please check your details carefully",
          icon: "error",
          timer: 1500});
        
        });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
form_container{

}

form{
  height:30vw;
}
</style>
