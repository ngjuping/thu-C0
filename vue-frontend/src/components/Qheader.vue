<template>
    <nav class="navbar navbar-expand-lg bg-white shadow">
                <div @click="logoClicked" id="logo" class="d-flex align-items-center w-50 my-2">
                    <img src="@/assets/logo.png" width="100" class="d-inline-block align-top" alt="" id="logoimg">
                    <span id="logotext" class="rounded bg-dark text-light p-2" v-if="logged_in">回到主页</span>
                </div>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#menu" v-if="logged_in && hasUserPrivilege">
                    <font-awesome-icon icon="bars" class="w-50 h-50" style="max-width:50px;" />
                </button>
                <div class="d-lg-flex justify-content-center justify-content-lg-end" :class="{'collapse':logged_in,'navbar-collapse':logged_in}" id="menu">
                    <div class="navbar-nav" v-if="logged_in && hasUserPrivilege">
                            <li class="dropdown">
                                <a class="nav-item nav-link dropdown-toggle" data-toggle="dropdown">
                                    订场
                                </a>
                                <div class="dropdown-menu">
                                    <a class="dropdown-item" 
                                    data-toggle="collapse" data-target="#menu"
                                    v-for="venue in venues" 
                                    :key="venue.id" 
                                    @click="goBooking(venue.id)">{{ venue.name }}</a>
                                </div>
                            </li>
                            <a class="nav-item nav-link active" data-toggle="collapse" data-target="#menu" @click="$router.push({name:'Manage'})">我的场地</a>
                            <a class="nav-item nav-link" data-toggle="collapse" data-target="#menu" @click="$router.push({name:'AllShares'})">拼场广场</a>
                            <a class="nav-item nav-link" data-toggle="collapse" data-target="#menu" @click="$router.push({name:'AllFeedbacks'})">反馈天地</a>
                            <a class="nav-item nav-link" data-toggle="collapse" data-target="#menu" @click="$router.push({name:'AllCourses'})">培训武馆</a>
                        <a class="btn btn-danger mt-3 mt-md-0 nav-item" v-if="logged_in" @click="logout">登出</a>
                    </div>
                </div>
                <a class="btn btn-danger mt-3 mt-md-0 nav-item abc" v-if="logged_in && hasAdminPrivilege" @click="logout">登出</a>
                <div class="w-50 text-right" v-if="!logged_in" >
                    <button class="btn btn-primary mt-3 mt-md-0" @click="gotoLogin">登录</button>
                </div>
                
                
        
        
        
    </nav>
</template>

<script>
import Swal from 'sweetalert2'

export default {
    data(){
        return {
            timer:0,
            venues:[],
            failedToGetVenues:false
        }
    },
    mounted(){
        //get venues list
        this.$axios
        .get('/api/main/venues/list')
        .then(res => {
            this.venues = res.data.venues;
        })
        .catch(() => {
            this.failedToGetVenues = true;
        })
    },
    methods:{
        goBooking(x){
            this.$router.push({name:'Booking',params:{venueid:x}});
            if(this.$route.name === "Booking"){
                this.$router.go();
            }
        },
        gotoLogin(){
            this.$router.push({name:'Login'});
        },
        logoClicked(){
            if(!this.$store.state.logged_in){
                this.gotoLogin()
            }
            else{
                this.$router.push({name:'Mainpage'});
            }
            
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
    computed:{
        logged_in(){
            return this.$store.state.logged_in;
        },
        hasUserPrivilege(){
            return !this.$store.state.privilege;
        },
        hasAdminPrivilege(){
            return this.$store.state.privilege;
        }
    }
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
    .nav-item{
        color:black;
    }
    .nav-item:hover{
        background-color: #343a40;
        color:white;
        cursor:pointer;
        border-radius:5px;
    }
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

    @media (max-width:760px) {

        #logo{
            width:100%;
        }

        #logotext{
            font-size:20px;
        }
    }
    @media (max-width:500px) {
        #logoimg{
            width:60px;
        }
        #logotext{
            font-size:15px;
        }
    }
    @media (max-width:400px) {

        #logoimg{
            width:50px;
        }
    }
</style>