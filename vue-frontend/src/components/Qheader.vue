<template>
    <nav class="navbar navbar-expand-lg bg-white shadow">
                <div @click="$router.push({name:'Mainpage'})" id="logo" class="d-flex align-items-center w-50 my-2">
                    <img src="@/assets/logo.png" width="100" class="d-inline-block align-top" alt="" id="logoimg">
                    <span id="logotext" class="rounded bg-dark text-light p-2">回到主页</span>
                </div>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo02">
                    <font-awesome-icon icon="bars" class="w-50 h-50" style="max-width:50px;" />
                </button>
                <div class="btn-group mr-2 collapse navbar-collapse" 
                v-if="this.$store.state.logged_in && !this.$store.state.privilege" 
                id="navbarTogglerDemo02">
                    <div class="btn btn-primary" @click="$router.push({name:'Manage'})">我的场地</div>
                    <div class="btn btn-success" @click="$router.push({name:'AllShares'})">拼场广场</div>
                    <div class="btn btn-warning" @click="$router.push({name:'AllFeedbacks'})">反馈天地</div>
                    <div class="btn btn-info" @click="$router.push({name:'AllCourses'})">培训武馆</div>
                <button class="btn btn-primary" v-if="!this.$store.state.logged_in"  @click="gotoLogin">登录</button>
                <button class="btn btn-danger" v-else @click="logout">登出</button>
                
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
    #logo *:hover{
        cursor:pointer;
        transition: opacity 0.3s;
    }

    #logotext{
        opacity:0;
        font-size:20px;
    }
    nav:hover #logotext{
        opacity: 1;
    }

    nav:hover #logoimg{
        opacity:0.5;
    }
    #title{
        font-size:30px;
    }

    @media (max-width:760px) {
        #title{
            font-size:25px;
        }

        #logo{
            width:100%;
        }

        #logotext{
            opacity:1;
            font-size:20px;
        }

        #logoimg{
            display:none !important;
        }
    }
    @media (max-width:500px) {
        #title{
            font-size:20px;
        }
        #logoimg{
            width:50px;
        }
    }
    @media (max-width:400px) {
        #title{
            font-size:15px;
        }
        #logoimg{
            width:40px;
        }
    }
</style>