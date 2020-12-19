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
                <div class="col-8 text-right">
                    <div class="btn-group">
                        <div class="btn-group">
                            <button class="btn btn-light dropdown-toggle" type="button" data-toggle="dropdown">
                                过滤
                            </button>
                            <div class="dropdown-menu bg-light">
                                <a class="dropdown-item bg-danger text-light" @click="filter_status(1)">尚未付款</a>
                                <a class="dropdown-item bg-success text-light" @click="filter_status(2)">已付款</a>
                                <a class="dropdown-item bg-secondary text-light" @click="filter_status(-1)">历史订单</a>
                                <hr>
                                <a class="dropdown-item bg-light text-dark" @click="filter_type(1)">羽球</a>
                                <a class="dropdown-item bg-light text-dark" @click="filter_type(2)">乒乓</a>
                                <a class="dropdown-item bg-light text-dark" @click="filter_type(3)">网球</a>
                                <a class="dropdown-item bg-light text-dark" @click="filter_type(4)">篮球</a>
                                <hr/>
                                <a class="dropdown-item bg-light text-dark" @click="filter_status(0)">查看全部</a>
                            </div>
                        </div>
                        <div class="btn btn-info" @click="show_calendar = !show_calendar">您的行程</div>
                    </div>
                     
                </div>
            </div>
        </div>
        <div class="container overflow-auto">

            <ul class="pagination pagination-lg">
                    <li class="page-item"  v-for="(resv,index) in courts" :key="resv.reservation_id">
                        <a class="page-link px-3" :class="`resvStatus-${resv.status}`" @click="scrollToTarget(`resv-${resv.reservation_id}`)">{{ index+1 }}</a></li>
            </ul>
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
            <div class="row" v-for="court in courts" :key="court.reservation_id" :ref="`resv-${court.reservation_id}`">
                
                    <Reservation  :resv="court" ></Reservation>
                    
            </div>
            
                    <div class="alert alert-dark" v-if="!courts.length">
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

.resvStatus-1{
    color:red;
}

.resvStatus-2{
    color:green;
}

.resvStatus-3{
    color:grey;
}

.resvStatus-4{
    color:grey;
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