<template>
    <nav class="navbar bg-white shadow">
        <img src="@/assets/logo.png" width="100" class="d-inline-block align-top" alt="" id="headerimg" @click="$router.push({name:'Mainpage'})">
        <div id="title">工会场地预定系统</div>
        <div>
            <div class="btn-group" v-if="this.$store.state.logged_in && !this.$store.state.privilege">
                <div class="btn btn-primary" @click="$router.push({name:'Manage'})">我的场地</div>
                <div class="btn btn-success" @click="$router.push({name:'AllShares'})">拼场广场</div>
                <div class="btn btn-warning" @click="$router.push({name:'AllFeedbacks'})">反馈天地</div>
            </div>
            
            <button class="btn btn-primary" v-if="!this.$store.state.logged_in"  @click="gotoLogin">登录</button>
            <button class="btn btn-danger" v-else @click="logout">登出</button>
            <br/>
            <!-- <small v-if="this.$store.state.logged_in">已上线：{{ now() }}</small> -->
        </div>
        
    </nav>
</template>

<script>
import Swal from 'sweetalert2'

export default {
    data(){
        return {
            timer:0
        }
    },
    methods:{
        gotoLogin(){
            this.$router.push({name:'Login'});
        },
        logout()
        {
            this.$axios
            .post('/api/logout',{user_id: this.$store.state.logged_in_user_id})
            .then(() => {
                this.$store.commit('logout');
                this.$router.replace({name:'Login'});

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
        font-size:30px;
    }

    @media (max-width:760px) {
        #title{
            font-size:25px;
        }
    }
    @media (max-width:500px) {
        #title{
            font-size:20px;
        }
        #headerimg{
            width:50px;
        }
    }
    @media (max-width:400px) {
        #title{
            font-size:15px;
        }
        #headerimg{
            width:40px;
        }
    }
</style>