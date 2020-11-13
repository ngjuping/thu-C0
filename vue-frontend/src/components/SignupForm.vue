<template>
<div class="form_container d-flex justify-content-center">
  <div class="card w-25 shadow p-4">
      <div class="card-img-top w-100 d-flex justify-content-center">
        <img src="@/assets/logo.png">
      </div>
      
      <form class="card-body h-50 pb-5">
          <div v-if="errors.length">
            <div class="alert alert-danger" role="alert" v-for="error in errors" :key="error">
                {{ error }}
            </div>
          </div>
          <div class="form-group">
            <label >Name</label>
            <input class="form-control" :required="!signing_up" :disabled="signing_up" v-model="realname" >
          </div>

          <div class="form-group">
            <label >User ID</label>
            <input class="form-control" :disabled="signing_up" v-model="userid" :required="userid===''">
          </div>

          <div class="form-group">
            <label >Password</label>
            <input type="password" class="form-control" required :disabled="signing_up" v-model="password">
          </div>
          
          <button type="submit" class="btn btn-primary text-white" @click.prevent="signup" v-show="!signing_up" autofocus>Submit</button>
          
          <button class="btn btn-primary" v-show="signing_up" disabled>
          <span class="spinner-border spinner-border-sm"></span>
          Signing up...
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
      userid: "admin",
      password: "123456",
      realname: "",
      signing_up: false,
      errors:[]
    }
  },
  methods:{
    checkForm(){
        
      this.errors = [];

        if (this.userid && this.password && this.realname) {
        return true;
      }

      if (!this.realname) {
        this.errors.push('Real name required.');
      }
      if (!this.userid) {
        this.errors.push('Username required.');
      }
      if (!this.password) {
        this.errors.push('Password required.');
      }
        return false;
    },

    signup(){

      if (!this.checkForm())
      {
          return;
      }

      this.signing_up = true;
      this.$axios
      .post('/api/v1/signup',{
          user_id: this.userid,
          password: this.password,
          name: this.realname,
        }
      )
      .then(res => 
      {
        this.$router.push({name:'Mainpage'});
        this.signing_up = false;
        let data = res.data
        console.log(data);
        Swal.fire({
          title: "Congratulations " + data.nickname,
          text: "Your now logged in.",
          icon: "success",
          timer: 1000}
        );
      })
      .catch(()=>{
        this.signing_up = false;
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
form{
  height:30vw;
}
</style>
