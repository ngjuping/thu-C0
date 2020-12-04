<template>
  <div class="reply-detail-modal">
    <div class="modal fade" id="replyDetailModal" aria-hidden="true" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">用户反馈详情</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="detail-wrapper">
              <div class="info-row">
                <div class="label">反馈id: </div>
                <div class="value">{{replyDetail.feedback_id}}</div>
              </div>
              <div class="info-row">
                <div class="label">反馈内容: </div>
                <div class="value">{{replyDetail.content}}</div>
              </div>
              <div class="info-row">
                <div class="label">反馈图片: </div>
                <div class="value">
                  <img :src="replyDetail.img" class="img-thumbnail" style="width: 100px; height: 100px" />
                </div>
              </div>
              <div class="info-row">
                <div class="label">回复: </div>
                <div class="value">{{replyDetail.reply}}</div>
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
  name: 'ReplyDetailModal',
  props: {
    replyId: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      replyDetail: {}
    }
  },
  watch: {
    replyId(val) {
      const params = {
        user_id: val,
        page: 1
      }
      this.$axios.request({
        method: 'get',
        url: '/api/manage/feedback/user',
        params
      }).then(res => {
        this.replyDetail = res.data.feedbacks[0]
      }).catch(err => {
        console.log(err)
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