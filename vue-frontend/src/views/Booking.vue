<template>
    <div class="container">
        <div class="display-4">预定<b>{{ this.venue_name }}</b>场地</div>
        <hr>
        <div class="d-flex justify-content-start">
            
            <div class="btn btn-danger" @click="$router.go(-1)">回到前一页</div>
            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    根据运动类型筛选
                </button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <a class="dropdown-item" href="#">羽球</a>
                    <a class="dropdown-item" href="#">篮球</a>
                    <a class="dropdown-item" href="#">乒乓</a>
                </div>
            </div>
        </div>
        <div  v-if="courts">
            <CourtStatus v-for="court in courts" :key="court.id" :info="court"></CourtStatus>
        </div>
    </div>

</template>

<script>
import moment from 'moment';
import CourtStatus from '@/components/CourtStatus.vue'

export default {
    data(){
        return {
            venue_id:0,
            courts:null,
            venue_name: "默认场馆",
        };
    },
    components:{
        CourtStatus
    },
    mounted(){
        this.venue_id = this.$route.params.venueid
        let day = moment().date()
        let month = parseInt(moment().month())+1
        let year = moment().year()
        this.$axios
        .get(`/api/booking?id=${this.venue_id}&day=${day}&month=${month}&year=${year}`)
        .then(res => {
            this.courts = res.data.courts;
            this.venue_name = res.data.venue_name;
        })
    },
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

<style scoped>

</style>