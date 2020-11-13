<template>
    <nav class="navbar bg-white shadow">
        <img src="@/assets/logo.png" width="100" class="d-inline-block align-top" alt="">
        <div id="title">工会场地预定系统</div>
        <div>
            <button class="btn btn-danger" v-if="this.$store.state.logged_in" @click="logout">登出 as {{ this.$store.state.logged_in_user}}</button>
            <button class="btn btn-primary" v-else  @click="gotoLogin">登录</button>
            <br/>
            <small v-if="this.$store.state.logged_in">最近登陆：{{ now() }}</small>
        </div>
        
        
    </nav>
</template>

<script>
import Swal from 'sweetalert2'
import moment from 'moment'

export default {
    data(){
        return {
            timer:0
        }
    },
    methods:{
        gotoLogin(){
            this.$router.push('Login');
        },
        logout()
        {
            this.$store.commit('logout');
            this.$router.replace('Login');
            Swal.fire({
            title: "成功登出",
            text: "感谢您的使用",
            icon: "success",
            timer: 1500});
        },
        now(){
            let stored_time = this.$store.state.logged_in_time
            if(stored_time == "Notime")
            {
                return "Not logged in";
            }
            let first_half = stored_time.split("T")[0];
            let second_half_time = stored_time.split("T")[1].split("+")[0];
            
            return moment(first_half + " " + second_half_time,"YYYY-MM-DD hh:mm:ss").fromNow();
        }
    },
    beforeUpdate(){
        clearInterval(this.timer);
        
    },
    updated(){

        //force recompute
        this.timer = setInterval(()=>{
            this.$forceUpdate();            

        },3000);
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