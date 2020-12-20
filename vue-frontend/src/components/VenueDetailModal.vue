<template>
  <div class="venue-detail-modal">
    <div class="modal fade" id="venueDetailModal" aria-hidden="true" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">场馆详情</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="detail-wrapper">
              <div class="info-row">
                <div class="label">场馆名称: </div>
                <div class="value">{{venueDetail.name}}</div>
              </div>
              <div class="info-row">
                <div class="label">场馆描述: </div>
                <div class="value">{{venueDetail.description}}</div>
              </div>
              <div class="info-row">
                <div class="label">场馆图片: </div>
                <div class="value">
                  <img :src="`http://58.87.86.11:8000/${this.venueDetail.img}`" class="img-thumbnail" style="width: 100px; height: 100px" />
                </div>
              </div>
              <div v-if="venueDetail.review">
                <h6 class="title">最新评论: </h6>
                <div class="info-row">
                  <div class="label" v-if="venueDetail.review.stars">星级: </div>
                  <div class="value">{{venueDetail.review.stars}}</div>
                </div>
                <div class="info-row">
                  <div class="label" v-if="venueDetail.review.content">评论内容: </div>
                  <div class="value" v-html="venueDetail.review.content"></div>
                </div>
                <div class="info-row">
                  <div class="label" v-if="venueDetail.review.publish_date">评论日期: </div>
                  <div class="value">{{venueDetail.review.publish_date}}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'VenueDetailModal',
  props: {
    venueId: {
      type: Number,
      required: true
    }
  },
  data () {
    return {
      venueDetail: {}
    }
  },
  watch: {
    venueId(val) {
      const params = {
        id: val
      }
      this.$axios.request({
        method: 'get',
        url: '/api/main/venues',
        params
      }).then(response => {
        this.venueDetail = response.data.venue_info
      }).catch(error => {
        console.log(error)
      })
    }
  }
}
</script>

<style scoped>
.detail-wrapper {
  padding: 20px;
  text-align: left;
}
.detail-wrapper .info-row {
  margin-bottom: 10px;
  font-size: 14px;
  display: flex;
  align-items: center;
}
.info-row .label {
  flex: 0 0 20%;
  width: 20%;
  font-weight: 500;
}
.info-row .value {
  flex: 0 0 80%;
  width: 80%;
}
</style>