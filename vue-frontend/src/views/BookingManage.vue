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
      <div class="d-flex justify-content-start mb-4">
        <div class="btn btn-danger mr-2" @click="$router.go(-1)">回到前一页</div>
        <div class="dropdown">
          <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            根据运动类型筛选
          </button>
          <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
              <a class="dropdown-item" @click="setFilter(1)">羽球</a>
              <a class="dropdown-item" @click="setFilter(2)">篮球</a>
              <a class="dropdown-item" @click="setFilter(3)">乒乓</a>
          </div>
        </div>
      </div>
      <div>
          <court-manage v-for="court in filteredcourts" :key="court.id" :info="court"></court-manage>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
import CourtManage from '../components/CourtManage.vue'

export default {
  name: 'BookingManage',
  components: {CourtManage},
  data() {
    return {
      venuesList: [],
      venueId: '',
      courts: null,
      filter_type: -1
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
        this.courts = res.data.courts;
      }).catch(error => {
        console.log(error)
      })
    },
    setFilter(x){
      this.filter_type = x;
    }
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