<template>
    <div class="admin">
        <nav class="navbar navbar-expand navbar-light bg-light">
                <div class="navbar-nav mr-auto">
                    <a class="nav-item nav-link">Home <span class="sr-only">(current)</span></a>
                    <a class="nav-item nav-link" @click="$router.push({'name':'Venues'})">场馆管理</a>
                    <a class="nav-item nav-link" @click="$router.push({'name':'BookingManage'})">场地管理</a>
                    <a class="nav-item nav-link" @click="$router.push({'name':'FieldInit'})">学期场地管理</a>
                    <a class="nav-item nav-link" @click="$router.push({'name':'ReplyFeedback'})">回复反馈</a>
                    <a class="nav-item nav-link" @click="$router.push({'name':'NoticeManager'})">通知管理</a>
                    <a class="nav-item nav-link" @click="$router.push({'name':'TrainManager'})">培训课程管理</a>
                </div>
        </nav>
        <router-view />
    </div>
</template>

<script>
import Swal from 'sweetalert2'
export default {
    name: 'Admin',
    mounted(){
        if(!this.$store.state.privilege)
        {
            Swal.fire({
            title: "您并非管理员",
            text: "并非管理员，没有操作权限",
            icon: "error",
            timer: 1500});
        }

    }
    
}
</script>

<style scoped>
.nav-item:hover{
        background-color: white;
        color:white;
        cursor:pointer;
        border-radius:5px;
    }
</style>