<template>
    <div class="container">
        
        <div id="title" class="p-3 px-4 bg-dark rounded shadow text-white mb-5">管理场地</div>
        <div class="alert alert-danger" v-if="!loadCourtsSuccess">
            无法加载您的场地信息
        </div>
        <div class="container mb-3">
            <div class="row">
                <div class="col text-left">
                    <div class="btn btn-danger" @click="$router.go(-1)">前一页</div>
                </div>
                <div class="col text-right">
                    <div class="btn btn-info" @click="show_calendar = !show_calendar">打开日历</div>
                </div>
            </div>
        </div>
        <div class="container">
            <div class="row text-right mb-4">
                <div class="col"></div>
                <div class="col">
                    
                </div>
            </div>
            <div class="row mb-4" v-if="show_calendar">
                <div class="col">
                    <vc-calendar :attributes="attributes" mode="range" is-expanded class="shadow"></vc-calendar>
                </div>
            </div>
            <div class="row">
                
                    <Reservation  v-for="court in courts" :key="court.reservation_id" :resv="court"></Reservation>
                    
            </div>
        </div>
    </div>
    
</template>

<script>
import Swal from 'sweetalert2';
import Reservation from '@/components/Reservation.vue';

export default {
    components:{
        Reservation,
    },
    data(){
        return {
            loadCourtsSuccess:false,
            courts:[],
            show_calendar:false
        }
    },
    methods:{
        chineseTime(time){
            try{
            
                let [hour,min] = time.split("T")[1].split("+")[0].split(":");
                
                return `${hour}点 ${min}分`;
            }
            catch(e){
                return "没有时间";
            }
        },
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
    },
    computed:{
        attributes(){
            return [...this.courts.map(court => ({
                    key: 'today',
                    highlight: 'purple',
                    dates: court.details.start,
                    popover: {
                        label: `${this.chineseTime(court.details.start)} to ${this.chineseTime(court.details.end)}`,
                        hideIndicator: true,
                    },
                }))]
            
        }
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