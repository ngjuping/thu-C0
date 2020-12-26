<template>
<div class="form_container d-flex justify-content-center my-5">
  <div class="card shadow p-4" id="login_panel">
      <div class="card-img-top w-100 d-flex justify-content-center">
        <img src="@/assets/logo.png" class="logoimg">
      </div>
      
      <form class="card-body h-50 pb-5">
          <div class="form-group text-left">
            <label>账号</label>
            <input class="form-control" :disabled="logging_in" v-model="api_id">
            <small class="form-text text-muted text-center">欢迎回来 {{api_id}}</small>
          </div>

          <div class="form-group text-left">
            <label >密码</label>
            <input type="password" class="form-control" required :disabled="logging_in" v-model="pwd">
          </div>
          
          <button type="submit" class="btn btn-primary text-white" @click.prevent="login" v-show="!logging_in" autofocus>登录</button>
          <button class="btn btn-primary" v-show="logging_in" disabled>
            <span class="spinner-border spinner-border-sm"></span>
            正在登陆....
          </button>
          <hr>
          <div class="container">
            <div class="row">
              <div class="col-8 d-flex justify-content-end align-items-center">
                <small>没有账户?</small>
              </div>
              <div class="col d-flex justify-content-end align-items-center">
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

export default {
  data()
  {
    return {
      api_id: "",
      pwd: "",
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
      .post('/api/login',{
          api_id: this.api_id,
          pwd: this.pwd
        }
      )
      .then(res => 
      {
        this.logging_in = false;
        let data = res.data
        this.$store.commit('login',data.user_info)
        //this.$router.push({name:'Mainpage'});
        // 如果privilege是1代表管理员
        if(data.user_info.privilege===1) {
          this.$router.push({name:'Admin'})
        } else {
          this.$router.push({name:'Mainpage'});
        }

        Swal.fire({
          title: "欢迎! " + data.user_info.name,
          text: "成功登陆", 
          icon: "success",
          timer: 1000}
        );
      })
      .catch((err)=>{
        this.logging_in = false;
        Swal.fire({
          title: "资料有误",
          text: `错误信息: ${err.response.data.message}`,
          icon: "error",
          timer: 1500});
        
        });
    }
  },
  mounted(){
    if(this.$store.state.logged_in)
    {
      if(this.$store.state.privilege===1) {
          this.$router.replace({name:'Admin'})
        } else {
          this.$router.replace({name:'Mainpage'});
        }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.logoimg{
  max-width:200px;
}

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
