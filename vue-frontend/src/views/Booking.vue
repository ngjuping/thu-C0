<template>
    <div class="container bg-gradient-light rounded">
        <div id="title" class="p-3 px-4 bg-dark rounded shadow text-white mb-5">预定<span class="text-warning mx-3">{{ this.venue_name }}</span>场地</div>
        
        <div class="container mb-4" id="filter_panel">
            <div class="row">
                <div class="col-12 col-md-4 col-lg-3 d-flex justify-content-start mb-4 pl-0">
                    <div class="btn-group shadow">
                        <div class="btn btn-danger" @click="$router.go(-1)">前一页</div>
                        <div class="dropdown btn-group">
                            <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                筛选球类
                            </button>
                            <div class="dropdown-menu">
                                <a class="dropdown-item" @click="setFilter(1)">羽球</a>
                                <a class="dropdown-item" @click="setFilter(2)">乒乓</a>
                                <a class="dropdown-item" @click="setFilter(3)">网球</a>
                                <a class="dropdown-item" @click="setFilter(4)">篮球</a>
                                <hr>
                                <a class="dropdown-item" @click="setFilter(-1)">清除过滤</a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md col-lg  d-flex justify-content-start mb-4 px-0">
                    <div class="container">
                        <div class="row">
                            <div class="btn-group shadow col-12 col-md px-0">
                                <div class="btn btn-dark" @click="updateCourts(today())">
                                    今天
                                </div>
                                <div class="btn btn-dark" @click="updateCourts(today(1))">
                                    明天
                                </div>
                                <div class="btn-group dropdown" style="position: static;">
                                    <div class="btn btn-dark dropdown-toggle" type="button" data-toggle="dropdown">
                                        更多
                                    </div>
                                    <div class="dropdown-menu" >
                                        <a class="dropdown-item" @click="updateCourts(today(2))">{{ today(2).join("-") }}</a>
                                        <a class="dropdown-item" @click="updateCourts(today(3))">{{ today(3).join("-") }}</a>
                                        <a class="dropdown-item" @click="updateCourts(today(4))">{{ today(4).join("-") }}</a>
                                        <a class="dropdown-item" @click="updateCourts(today(5))">{{ today(5).join("-") }}</a>
                                        <a class="dropdown-item" @click="updateCourts(today(6))">{{ today(6).join("-") }}</a>
                                    </div>
                                </div>
                                
                            </div>

                            <div class="card px-2 pt-1 col-12 col-md">
                                <span class="card-text vertical-align-center">
                                    当前预定日期：{{ selected_date.join("-") }}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="spinner-border shadow text-primary" v-if="loadingCourts">
                    <span class="sr-only">Loading...</span>
                </div>
            </div>
        </div>
        <vc-calendar mode="range" is-expanded @dayclick='updateByCalendarClick' :attributes="attributes" :min-date='new Date()'></vc-calendar>
        <br/>
        <div v-if="courts">
            <CourtStatus v-for="court in filteredcourts" :key="court.id" :info="court" :date="selected_date"></CourtStatus>
        </div>
        <div class="alert alert-danger" v-if="failedToLoadCourts">
            无法加载场地信息
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
            filter_type:-1,
            failedToLoadCourts:false,
            loadingCourts:false,
            selected_date:this.today(),
            timer:0,
        };
    },
    components:{
        CourtStatus
    },
    methods:{
        updateByCalendarClick(dayEvent){

            if(dayEvent.isDisabled) return;

            let parsed_date = dayEvent.id.split("-");
            let day = parsed_date[2];
            let month = parsed_date[1];
            let year = parsed_date[0];
            this.updateCourts([day,month,year]);
        },
        setFilter(x){
            this.filter_type = x;
        },
        today(offset=0){
            let day,month,year;
            if(!offset) //if is today
            {
                day = moment().date().toString();
                month = (parseInt(moment().month())+1).toString();
                year = moment().year().toString();
            }
            else // x days after today
            {
                let date = moment();
                let x_days_later_arr = date.add(offset,'day').format('DD-MM-YYYY').split("-");
                [day,month,year] = x_days_later_arr;
            }
            return [day,month,year];
        },
        updateCourts(date=this.selected_date){
            //reset load failure
            this.failedToLoadCourts = false;

            //loading courts
            this.loadingCourts = true;
            
            //upload select date for courtstatus to capture current date
            this.selected_date = date;

            let day = date[0];
            let month = date[1];
            let year = date[2];

            this.$axios
            .get(`/api/booking?id=${this.venue_id}&day=${day}&month=${month}&year=${year}`)
            .then(res => {
                this.courts = res.data.courts;
                this.venue_name = res.data.venue_name;
            })
            .catch(() => {
                this.failedToLoadCourts = true;
            })
            .finally(() => {
                this.loadingCourts = false;
            })
        }
    },
    mounted(){
        this.venue_id = this.$route.params.venueid
        let today = this.today();
        this.updateCourts(today);
        this.timer = setInterval(this.updateCourts,4000);
    },
    destroyed(){
        clearInterval(this.timer);
    },
    computed:{
        filteredcourts(){
            if(this.filter_type === -1)
            {
                return this.courts;
            }
            return this.courts.filter((court)=>{return court.type === this.filter_type});
        },
        attributes(){
            // selected_date 格式 = [day,month,year]
            let date = this.selected_date;

            // 需要返回一个数组的对象
            return [{
                key: 'today',
                highlight: 'purple',

                // 月份从0开始
                dates: new Date(date[2],date[1]-1,date[0]),
                popover: {
                    label: "选择这天",
                    hideIndicator: true,
                }
            }]
        }
    }
}
</script>

<style scoped>

#title{
    font-size:50px;
}

.dayDisabled{
    pointer-events: none;
}

.dayContentDisabled {
    pointer-events: none;
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