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
            <input class="form-control" :required="!signing_up" :disabled="signing_up" v-model="realname" >
          </div>

          <div class="form-group">
            <label >账号名称/ID</label>
            <input class="form-control" :disabled="signing_up" v-model="userid" :required="userid===''">
          </div>

          <div class="form-group">
            <label >密码</label>
            <input type="password" class="form-control" required :disabled="signing_up" v-model="password">
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
        this.errors.push('请输入您的真实姓名.');
      }
      if (!this.userid) {
        this.errors.push('账号名称不能为空.');
      }
      if (!this.password) {
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
          title: "注册完成" + data.nickname,
          text: "现在帮您登陆",
          icon: "success",
          timer: 1000}
        );
      })
      .catch(()=>{
        this.signing_up = false;
        Swal.fire({
          title: "注册出现问题",
          text:  "可能是您的用户名或密码不满足要求",
          icon:  "error",
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
