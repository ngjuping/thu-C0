<template>
    <div class="container">
        
        <div id="title" class="p-3 px-4 bg-dark rounded shadow text-white mb-5">管理场地</div>
        <div class="alert alert-danger" v-if="!loadCourtsSuccess">
            无法加载您的场地信息
        </div>
        <div class="container text-left pl-0 mb-3">
            <div class="btn-group">
                    <div class="btn btn-danger" @click="$router.go(-1)">前一页</div>
            </div>
        </div>
        <div class="">
            <div class="card bg-light mb-3" v-for="court in courts" :key="court.id" >
                <div class="card-header">{{ court.details.name }}</div>
                <div class="card-body">
                    <h5 class="card-title">预定类型: {{ court.status }}</h5>
                    <h6 class="card-subtitle">下单于: {{ relativeTime(court.details.start) }}</h6>
                    <div class="card-text"> 生效日期: {{ relativeTime(court.details.end) }}</div>
                </div>
            </div>
        </div>
    </div>
    
</template>

<script>
import Swal from 'sweetalert2';
import moment from 'moment';

export default {
    data(){
        return {
            loadCourtsSuccess:false,
            courts:[]
        }
    },
    methods:{
        relativeTime(time){

            let first_half = time.split("T")[0];
            let second_half_time = time.split("T")[1].split("+")[0];
            
            return moment(first_half + " " + second_half_time,"YYYY-MM-DD hh:mm:ss").fromNow();
        }
    },
    mounted(){
        if(!this.$store.state.logged_in)
        {
            Swal.fire({
            title: "您还没有登陆",
            text: `请先点击右上角登陆或注册`,
            icon: "error",
            timer: 1500});
            return;
        }
        this.$axios
        .get(`/api/manage/courts?user_id=${this.$store.state.logged_in_user_id}`)
        .then((res) => {
            this.loadCourtsSuccess = true;
            this.courts = res.data.courts;
        })
        .catch(()=>{
            this.loadCourtsSuccess = false;
        })
    }
}
</script>

<style scoped>
#title{
    font-size:50px;
}

@media (max-width:760px) {
    #title{
        font-size:30px;
    }
}

@media (max-width:500px) {
    #title{
        font-size:20px;
    }
}
</style>