<template>
    <nav class="navbar bg-white shadow">
        <img src="@/assets/logo.png" width="100" class="d-inline-block align-top" alt="">
        <div id="title">工会场地预定系统</div>
        <div>
            <button class="btn btn-danger" v-if="this.$store.state.logged_in" @click="logout">登出 as {{ this.$store.state.logged_in_user}}</button>
            <button class="btn btn-primary" v-else  @click="gotoLogin">登录</button>
            <br/>
            <!-- <small v-if="this.$store.state.logged_in">已上线：{{ now() }}</small> -->
        </div>
        
        
    </nav>
</template>

<script>
import Swal from 'sweetalert2'
//import moment from 'moment'

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
            this.$axios
            .post('/api/logout',{id: this.$store.state.logged_in_user})
            .then(() => {
                this.$store.commit('logout');
                this.$router.replace('Login');

                Swal.fire({
                title: "成功登出",
                text: "感谢您的使用",
                icon: "success",
                timer: 1000});
            })
            .catch((err) => {
                Swal.fire({
                title: "无法登出",
                text: `错误信息${err.response.data.message}`,
                icon: "error",
                timer: 1000});
            })
            
        },
        // now(){
        //     let stored_time = this.$store.state.logged_in_time
        //     if(stored_time == "Notime")
        //     {
        //         return "Not logged in";
        //     }
        //     let first_half = stored_time.split("T")[0];
        //     let second_half_time = stored_time.split("T")[1].split("+")[0];
            
        //     return moment(first_half + " " + second_half_time,"YYYY-MM-DD hh:mm:ss").fromNow();
        // }
    },
    // //use timer to simulate real time update
    // beforeUpdate(){
    //     clearInterval(this.timer);
        
    // },
    // updated(){

    //     //force recompute last logged in time
    //     this.timer = setInterval(()=>{
    //         this.$forceUpdate();            

    //     },3000);
    // }
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