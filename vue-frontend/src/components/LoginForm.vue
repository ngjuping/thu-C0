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

export default {
  data()
  {
    return {
      userid: "2018080120",
      password: "365391",
      logging_in: false
    }
  },
  methods:{
    login(){
      this.logging_in = true;
      this.$axios
      .patch('/api/v1/login',{
          username: this.userid,
          password: this.password
        }
      )
      .then(res => 
      {
        this.$router.push({name:'Welcome'});
        this.logging_in = false;
        let data = res.data
        Swal.fire({
          title: "Welcome! " + data.nickname,
          text: "You have been logged in.",
          icon: "success",
          timer: 1000}
        );

        localStorage.setItem('my-jwt',data.jwt);
        

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
