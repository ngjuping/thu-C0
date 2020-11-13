<template>
<div class="form_container d-flex justify-content-center">
  <div class="card shadow p-4" id="login_panel">
      <div class="card-img-top w-100 d-flex justify-content-center">
        <img src="@/assets/logo.png" class="">
      </div>
      
      <form class="card-body h-50 pb-5">
          <div class="form-group text-left">
            <label>账号</label>
            <input class="form-control" :disabled="logging_in" v-model="userid" :required="userid===''">
            <small class="form-text text-muted text-center">欢迎回来 {{userid}}</small>
          </div>

          <div class="form-group text-left">
            <label >密码</label>
            <input type="password" class="form-control" required :disabled="logging_in" v-model="password">
          </div>
          
          <button type="submit" class="btn btn-primary text-white" @click.prevent="login" v-show="!logging_in" autofocus>登录</button>
          <button class="btn btn-primary" v-show="logging_in" disabled>
            <span class="spinner-border spinner-border-sm"></span>
            正在登陆....
          </button>
          <hr>
          <div class="container">
            <div class="row">
              <div class="col-9 d-flex justify-content-end align-items-center">
                <small>没有账户?</small>
              </div>
              <div class="col">
                <button type="submit" class="btn btn-secondary" @click.prevent="gotoSignup">注册</button>
              </div>
            </div>
            
          </div>
          
          
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
    gotoSignup(){
      this.$router.push({name:'Signup'});
    },
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
        this.$store.state.logged_in = true
        this.$router.push({name:'Mainpage'});
        this.logging_in = false;
        let data = res.data
        Swal.fire({
          title: "欢迎! " + data.name,
          text: "成功登陆",
          icon: "success",
          timer: 1000}
        );
      })
      .catch(()=>{
        this.logging_in = false;
        Swal.fire({
          title: "资料有误",
          text: "请检查",
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

#login_panel
{
    width:30%;
}

@media(max-width:1200px)
{
  #login_panel
  {
      width:50%;
  }
}

@media(max-width:768px)
{
  #login_panel
  {
      width:70%;
  }
}
</style>
