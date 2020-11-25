<template>
  <div class="review-modal">
    <div class="modal fade" id="editVenueModal" aria-hidden="true" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">编辑场馆</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="form-group row">
                <label class="col-sm-2 col-form-label">名称</label>
                <div class="col-sm-10">
                  <input type="text" v-model="formMessage.name" class="form-control" placeholder="请输入"/>
                </div>
              </div>
              <div class="form-group row">
                <label class="col-sm-2 col-form-label">描述</label>
                <div class="col-sm-10">
                  <textarea v-model="formMessage.description" class="form-control" rows="3" placeholder="请输入"/>
                </div>
              </div>
              <div class="form-group row">
                <label class="col-sm-2 col-form-label">场馆图片</label>
                <div class="col-sm-10">
                  <div class="col-sm-6">
                    <input type="file" class="form-control-file">
                  </div>
                  <div class="col-sm-6">
                    <img :src="formMessage.img" alt="" />
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">取消</button>
            <button type="button" class="btn btn-primary" @click="handleSave">保存</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReviewModal',
  props: {
    venueDetail: {
      type: Object,
      default() {
        return {}
      }
    }
  },
  data() {
    return {
      formMessage: {
        name: '',
        description: '',
        img: ''
      }
    }
  },
  methods: {
    handleSave() {
      const params = Object.assign({}, this.formMessage)
      this.$axios.request({
        method: 'post',
        url: '/api/admin/modify/venue',
        data: params
      }).then(() => {

      }).catch(() => {

      })
    }
  },
  watch: {
    venueDetail (val) {
      console.log(val);
      this.formMessage = {
        name: val.name,
        description: val.description,
        img: val.img
      }
    }
  }
}
</script>

<style scoped>

</style>