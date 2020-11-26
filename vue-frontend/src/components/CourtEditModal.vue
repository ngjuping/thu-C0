<template>
  <div class="court-edit-modal">
    <div class="modal fade" id="editCourtModal" aria-hidden="true" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">编辑场地</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="row form-group">
                <label class="col-sm-2">type</label>
                <div class="col-sm-10">
                  <select v-model="formMessage.type" class="form-control">
                    <option :value="''" disabled>请选择</option>
                    <option :value="1">1</option>
                    <option :value="2">2</option>
                    <option :value="3">3</option>
                  </select>
                </div>
              </div>
              <h6>场地配置</h6>
              <div class="row form-group" v-for="(item,index) in courtInfo.status" :key="index">
                <div class="col-sm-3">
                  <select v-model="item.start" class="form-control">
                    <option :value="''" disabled>开始时间</option>
                    <option v-for="(time,index) in timeList" :key="index" :value="time">{{time}}</option>
                  </select>
                </div>
                <div class="col-sm-3">
                  <select v-model="item.end" class="form-control">
                    <option :value="''" disabled>结束时间</option>
                    <option v-for="(time,index) in timeList" :key="index" :value="time">{{time}}</option>
                  </select>
                </div>
                <div class="col-sm-3">
                  <select v-model="item.code" class="form-control">
                    <option :value="''" disabled>状态</option>
                    <option :value="0">可预定</option>
                    <option :value="1">已预定</option>
                  </select>
                </div>
                <div class="col-sm-3">
                  <button type="button" class="btn btn-danger">删除</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourtEditModal',
  props: {
    courtInfo: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      formMessage: {
        type: '',
      },
      timeList: []
    }
  },
  mounted() {
    this.timeList = []
    for (let i = 0; i <= 24; i++) {
      let item = ''
      if (i === 0) {
        item = '0000'
      } else if (i < 10) {
        item = '0' + (i*100).toString()
      } else {
        item = (i*100).toString()
      }
      this.timeList.push(item)
    }
  },
  watch: {
    courtInfo(val) {
      this.formMessage.type = val.type
    }
  }
}
</script>

<style scoped>
.court-edit-modal {}
</style>