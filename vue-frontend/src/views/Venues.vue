<template>
  <div class="venues">
    <button
        type="button"
        class="btn btn-primary"
        data-toggle="modal" 
        data-target="#editVenueModal"
        style="float: left; margin-bottom: 5px"
        @click="handleShowEditModal(item, 'add')"
    >新增</button>
    <table class="table">
      <thead class="thead-dark">
        <tr>
          <th scope="col">序号</th>
          <th scope="col">名称</th>
          <th scope="col">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item,index) in venuesList" :key="index">
          <th scope="row">{{index + 1}}</th>
          <td>
            <a href="javascript:void(0)" 
              class="card-link" 
              data-toggle="modal" 
              data-target="#venueDetailModal" 
              @click="handleShowDetailModal(item)">{{item.name}}</a>
          </td>
          <td>
            <button 
              type="button" 
              class="btn btn-primary btn-sm" 
              data-toggle="modal" 
              data-target="#editVenueModal" 
              @click="handleShowEditModal(item, 'edit')">
              编辑
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <venue-edit-modal :venue-detail="venueDetail" @edit-success="handleGetVenues" :status="status" />
    <venue-detail-modal :venue-id="venueId" />
  </div>
</template>

<script>
import VenueDetailModal from '../components/VenueDetailModal.vue'
import VenueEditModal from '../components/VenueEditModal'
export default {
  name: 'Venues',
  components: {VenueEditModal,VenueDetailModal},
  data() {
    return {
      venuesList: [],
      venueId: '',
      venueDetail: {},
      status: 'add'
    }
  },
  methods: {
    handleShowEditModal(item, status) {
      this.status = status;
      this.venueDetail = item;
    },
    handleShowDetailModal(item) {
      this.venueId = item.id
    },
    handleGetVenues() {
      this.$axios.request({
        method: 'get',
        url: '/api/main/venues/list',
      }).then(response => {
        this.venuesList = response.data.venues
      }).catch(error => {
        console.log(error)
      })
    }
  },
  mounted() {
    this.handleGetVenues()
  }
}
</script>

<style scoped>
.venues {
  padding: 50px;
}
.venues .venue-image {
  width: 100px;
  height: 100px;
}
</style>