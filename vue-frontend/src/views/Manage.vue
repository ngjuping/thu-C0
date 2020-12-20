<template>
    <div class="container">
        
        <div id="title" class="p-3 px-4 bg-dark rounded shadow text-white mb-5">管理场地</div>
        <div class="alert alert-danger" v-if="!loadCourtsSuccess && !freshLoad">
            无法加载您的场地信息
        </div>
        <span class="spinner-border spinner-border-md text-dark" v-if="freshLoad"></span>
        <div class="container mb-3">
            <div class="row">
                <div class="col text-left">
                    <div class="btn btn-danger" @click="$router.go(-1)">前一页</div>
                </div>
                <div class="col-8 text-right">
                    <div class="btn-group">
                        <div class="btn-group">
                            <button class="btn btn-light dropdown-toggle" type="button" data-toggle="dropdown">
                                过滤
                            </button>
                            <div class="dropdown-menu bg-light">
                                <a class="dropdown-item bg-danger text-light" @click="filter_status(1)">尚未付款</a>
                                <a class="dropdown-item bg-success text-light" @click="filter_status(2)">已付款</a>
                                <a class="dropdown-item bg-secondary text-light" @click="filter_status(-1)">过期订单</a>
                                <hr>
                                <a class="dropdown-item bg-light text-dark" @click="filter_type(1)">羽球</a>
                                <a class="dropdown-item bg-light text-dark" @click="filter_type(2)">乒乓</a>
                                <a class="dropdown-item bg-light text-dark" @click="filter_type(3)">网球</a>
                                <a class="dropdown-item bg-light text-dark" @click="filter_type(4)">篮球</a>
                                <hr/>
                                <a class="dropdown-item bg-light text-dark" @click="filter_status(0)">全部订单</a>
                            </div>
                        </div>
                        <div class="btn btn-info" @click="show_calendar = !show_calendar">您的行程</div>
                    </div>
                     
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
            <div class="container overflow-auto" style="box-sizing:border-box;">
            
            <ul class="pagination pagination-lg overflow-auto">
                    <li class="page-item"  v-for="(resv,index) in courts" :key="resv.reservation_id">
                        <a class="page-link px-3" :class="`resvStatus-${resv.status}`" @click="scrollToTarget(`resv-${resv.reservation_id}`)">{{ index+1 }}</a></li>
            </ul>
            <ul class="legend">
                <li v-for="(str,index) in allStatusExceptFirst" :key="`${index+1}${str}`">
                    <span :class="`resvStatus-${index+1}`"></span> {{ str }}</li>
            </ul>

            </div>
            <br/>
            <div class="row" v-for="court in courts" :key="court.reservation_id" :ref="`resv-${court.reservation_id}`">
                
                    <Reservation  :resv="court" ></Reservation>
                    
            </div>
            
                    <div class="alert alert-dark" v-if="!courts.length && !freshLoad">
                        没有找到数据...
                    </div>
        </div>
    </div>
    
</template>

<script>
import Swal from 'sweetalert2';
import Reservation from '@/components/Reservation.vue';
import moment from 'moment';
import smoothScroll from 'smoothscroll'

export default {
    components:{
        Reservation,
    },
    data(){
        return {
            loadCourtsSuccess:false,
            courts:[],
            original_courts:[],
            show_calendar:false,
            today:moment().format(),
            freshLoad:true,
        }
    },
    methods:{
        scrollToTarget(target){
            smoothScroll(this.$refs[target][0]);
        },
        between(data,x,y){
            return parseInt(data) >= x && parseInt(data) <= y;
        },
        filter_type(type){
            this.courts = this.original_courts.filter((court) => {return court.type === type});
        },
        filter_status(status_code){
            // 查看所有订单
            if(!status_code){
                this.courts = this.original_courts;
            }
            else if(status_code === -1){
                // 已退场，转让，过期的场地
                this.courts = this.original_courts.filter((court) => {return this.between(court.status,3,4) || this.outDated(court)  });
            }
            else{
                // 过滤订单
                this.courts = this.original_courts.filter((court) => {return court.status === status_code});
            }

        },
        chineseTime(time){
            try{
                let [hour,min] = time.split("T")[1].split("+")[0].split(":");
                
                return `${hour}点 ${min}分`;
            }
            catch(e){
                return "没有时间";
            }
        },
        getReservations(){
            this.$axios
            .get(`/api/manage/courts?user_id=${this.$store.state.logged_in_user_id}`)
            .then((res) => {
                this.loadCourtsSuccess = true;
                this.original_courts = res.data.courts;
                this.courts = this.original_courts;
            })
            .catch(()=>{
                this.loadCourtsSuccess = false;
            })
            .finally(() => {
                this.freshLoad = false;
            })
        },
        outDated(resv){
            return resv.details.end < this.today;
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
        this.getReservations();
    },
    computed:{
        allStatusExceptFirst(){
            return this.$store.state.reservationStatus.filter((v,i) => {return !!i});
        },
        attributes(){
            return [...this.original_courts.map(court => ({
                    key: 'today',
                    highlight: 'purple',
                    dates: court.details.start,
                    popover: {
                        label: `${this.chineseTime(court.details.start)} to ${this.chineseTime(court.details.end)}  ${court.details.name}`,
                        hideIndicator: true,
                    },
                }))]
            
        },
    }
}
</script>

<style scoped>
#title{
    font-size:50px;
}

li > *{
    border-width:0px;
    border-color:transparent;
    opacity:0.8;
}

a:hover{
    opacity:1;
    cursor:pointer;
}

li{
    border-width:0px;
    border-color:transparent;
}

.resvStatus-1{
    color:rgb(255, 255, 255);
    background-color:rgb(255, 0, 0);
}

.resvStatus-2{
    color:white;
    background-color:rgb(4, 138, 49);
    
}

.resvStatus-3{
    color:white;
    background-color:rgb(77, 77, 77);
}

.resvStatus-4{
    color:white;
    background-color: rgb(0, 140, 255);
}

.resvStatus-5{
    color:white;
    background-color:rgb(255, 0, 234);
}

.resvStatus-6{
    color:white;
    background-color:rgb(140, 0, 255);
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