<template>
  <div class="booking-manage pl-0">
    <div class="form-wrapper">
      <form class="form-inline">
        <div class="form-group mx-sm-3 mb-2">
          <label for="inputPassword2" style="margin-right: 19px;">场馆</label>
          <select v-model="venueId" class="form-control" style="width: 120px;">
            <option disabled value="">请选择</option>
            <option v-for="item in venuesList" :key="item.id" :value="item.id">{{item.name}}</option>
          </select>
        </div>
        <button
              type="button"
              class="btn btn-primary"
              data-toggle="modal" 
              data-target="#editCourtModal"
              style="margin-left: 5px"
              @click="addCourt('add')"
          >新增场地</button>
      </form>
    </div>
    <court-edit-modal
      :show="show"
      :court-info="info"
      :status="status"
      @close="show=false"
    />
  </div>
</template>

<script>
import CourtEditModal from '../components/CourtEditModal.vue';

export default {
  name: 'BookingManage',
  components: {CourtEditModal},
  data() {
    return {
      venuesList: [],
      venueId: 1,
      info: {},
      show: false,
      status: 'add',
    }
  },
  methods: {
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