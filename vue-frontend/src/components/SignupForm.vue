<template>
<div class="form_container d-flex justify-content-center">
  <div class="card shadow p-4" id="signup_panel">
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
            <label >您的名字</label>
            <input class="form-control" :disabled="signing_up" v-model="realname" >
          </div>

          <div class="form-group">
            <label >账号名称/ID</label>
            <input class="form-control" :disabled="signing_up" v-model="user_id">
          </div>

          <div class="form-group">
            <label >密码</label>
            <input type="password" class="form-control" required :disabled="signing_up" v-model="pwd">
          </div>
          
          <button type="submit" class="btn btn-primary text-white" @click.prevent="signup" v-show="!signing_up" autofocus>提交</button>
          
          <button class="btn btn-primary" v-show="signing_up" disabled>
          <span class="spinner-border spinner-border-sm"></span>
          正在帮您注册...
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
      user_id: "admin",
      pwd: "123456",
      realname: "",
      signing_up: false,
      errors:[]
    }
  },
  methods:{
    tryLogin(){
        this.$axios
        .post('/api/login',{
            user_id: this.user_id,
            pwd: this.pwd
          }
        )
        .then(res => 
        {
          this.logging_in = false;
          let data = res.data
          this.$store.commit('login',data.user_info.user_id)
          this.$router.push({name:'Mainpage'});

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

    },
    checkForm(){
        
      this.errors = [];

        if (this.user_id && this.pwd && this.realname) {
        return true;
      }

      if (!this.realname) {
        this.errors.push('请输入您的真实姓名.');
      }
      if (!this.user_id) {
        this.errors.push('账号名称不能为空.');
      }
      if (!this.pwd) {
        this.errors.push('密码不能为空.');
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
      .post('/api/signup',{
          user_id: this.user_id,
          pwd: this.pwd,
          name: this.realname,
        }
      )
      .then(() => 
      {
        this.signing_up = false;
        this.tryLogin();
        
      })
      .catch((err)=>{
        this.signing_up = false;
        Swal.fire({
          title: "注册出现问题",
          text:  `错误信息：${err.response.data.message}`,
          icon:  "error",
          timer: 1000});
        
        });
    }
  },
  mounted(){
    if(this.$store.state.logged_in)
    {
      this.$router.go(-1);
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
form{
  height:30vw;
}

#signup_panel
{
    width:30%;
}

@media(max-width:1200px)
{
  #signup_panel
  {
      width:50%;
  }
}

@media(max-width:768px)
{
  #signup_panel
  {
      width:70%;
  }
}
</style>
