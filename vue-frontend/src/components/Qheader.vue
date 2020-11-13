<template>
    <nav class="navbar bg-white shadow">
        <img src="@/assets/logo.png" width="100" class="d-inline-block align-top" alt="">
        <div id="title">工会场地预定系统</div>
        <button class="btn btn-danger" v-if="this.$store.state.logged_in" @click="logout">登出</button>
        <button class="btn btn-primary" v-else  @click="gotoLogin">登录</button>
        
    </nav>
</template>

<script>
import Swal from 'sweetalert2'

export default {
    methods:{
        gotoLogin(){
            this.$router.push('Login');
        },
        logout()
        {
            this.$store.state.logged_in = false;
            this.$router.replace('Login');
            Swal.fire({
            title: "成功登出",
            text: "感谢您的使用",
            icon: "success",
            timer: 1500});
        }
    }
}
</script>

<style>
    nav{
        position:fixed;
        top:0px;
        left:0px;
        width:100%;

    }

    #title{
        font-size:2vw
    }
</style>