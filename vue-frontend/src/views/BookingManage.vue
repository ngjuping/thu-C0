<template>
  <div class="booking-manage">
    <div class="form-wrapper">
      <form class="form-inline">
        <div class="form-group mx-sm-3 mb-2">
          <label for="inputPassword2" style="margin-right: 19px;">场馆</label>
          <select v-model="venueId" class="form-control" style="width: 120px;">
            <option disabled value="">请选择</option>
            <option v-for="item in venuesList" :key="item.id" :value="item.id">{{item.name}}</option>
          </select>
        </div>
        <button type="button" class="btn btn-primary mb-2" @click="handleGetCourts">查询</button>
      </form>
    </div>
    <div class="content" v-if="courts">
        <div class="row">
            <div class="d-flex justify-content-start mb-4">
                <div class="btn btn-danger mr-2" @click="$router.go(-1)">回到前一页</div>
                <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    根据运动类型筛选
                </button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <a class="dropdown-item" @click="setFilter(1)">羽球</a>
                    <a class="dropdown-item" @click="setFilter(2)">乒乓</a>
                    <a class="dropdown-item" @click="setFilter(3)">网球</a>
                    <a class="dropdown-item" @click="setFilter(3)">篮球</a>
                </div>
                </div>
                <button
                    type="button"
                    class="btn btn-primary"
                    data-toggle="modal" 
                    data-target="#editCourtModal"
                    style="margin-left: 5px"
                    @click="addCourt('add')"
                >新增</button>
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
        </div>
      <div>
          <court-manage v-for="court in filteredcourts" :key="court.id" :info="court" @court-change="handleGetCourts" @edit="handleEdit"></court-manage>
          <court-edit-modal
            :show="show"
            :court-info="info"
            :status="status"
            @success-edit="handleGetCourts"
            @close="show=false"
        />
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import CourtManage from '../components/CourtManage.vue'
import CourtEditModal from '../components/CourtEditModal.vue';

export default {
  name: 'BookingManage',
  components: {CourtManage, CourtEditModal},
  data() {
    return {
      venuesList: [],
      venueId: '',
      courts: null,
      venue_name: null,
      filter_type: -1,
      info: {},
      show: false,
      status: 'add',
      selected_date: this.today(),
      failedToLoadCourts: false,
      loadingCourts: false,
    }
  },
  computed:{
    filteredcourts(){
    
      if(this.filter_type === -1) {
        return this.courts;
      }
      return this.courts.filter((court)=>{return court.type === this.filter_type});
    }
  },
  methods: {
    handleGetCourts() {
      let day = moment().date()
      let month = parseInt(moment().month())+1
      let year = moment().year()
      const params = {
        id: this.venueId,
        day,
        month,
        year
      }
      this.$axios.request({
        method: 'get',
        url: '/api/booking',
        params
      }).then(res => {
          console.log(res.data)
        this.courts = res.data.courts;
      }).catch(error => {
        console.log(error)
      })
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
    handleEdit(info) {
      this.status = 'edit'
      this.info = info
      this.show = true
    },
    addCourt() {
        // 增加新场地
        this.show = true
        this.info = {
            type: 1,
            status: [],
            //id: this.venueId,
            venue_id:this.venueId
        };
        this.status = 'add';
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
        .get(`/api/booking?id=${this.venueId}&day=${day}&month=${month}&year=${year}`)
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
    },
  },
  mounted() {
    this.$axios.request({
      method: 'get',
      url: '/api/main/venues/list',
    }).then(response => {
      this.venuesList = response.data.venues
    }).catch(error => {
      console.log(error)
    })
  }
}
</script>

<style scoped>
.booking-manage {
  padding: 20px;
}
.form-wrapper {
  margin-bottom: 10px;
}
</style>