<template>
  <div class="court-edit-modal">
    <div class="modal fade" id="editCourtModal" aria-hidden="true" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">{{status=='add'?'新增':'编辑'}}场地</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="closeModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body" style="text-align: left;">
            <form>
              <div class="form-group row">
                <label class="col-sm-3 col-form-label">输入场地价格：</label>
                <div class="col-sm-8">
                  <input type="text" v-model.number="formMessage.price" class="form-control" placeholder="请输入"/>
                </div>
              </div>
              <div class="row form-group">
                <label class="col-sm-2">场地</label>
                <div class="col-sm-10">
                  <select v-model="formMessage.type" v-if="status=='add'" class="form-control" style="width: 100px">
                      <option
                        v-for="(item, index) in actualSportsType"
                        :value="index+1"
                        :key="index"
                      >{{item}}</option>
                  </select>
                  <span v-else>{{$store.state.sportsType[formMessage.type]}}</span>
                </div>
              </div>
              <div class="row form-group">
                <div class="col-sm-2">场地配置</div>
              </div>
              <div class="row form-group" v-for="(item,index) in formMessage.timeInfoList" :key="index">
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
                    <!-- <option :value="''" disabled>状态</option> -->
                    <option :value="0">未开放</option>
                    <option :value="1">空场地</option>
                    <option :value="2">已有人预定</option>
                    <option :value="4">可抽签</option>
                  </select>
                </div>
                <div class="col-sm-3" v-if="index === formMessage.timeInfoList.length - 1">
                </div>
              </div>

              
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="closeModal">取消</button>
            <button type="button" class="btn btn-primary" data-dismiss="modal" @click="handleSave">保存</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment'
export default {
  name: 'CourtEditModal',
  props: {
    courtInfo: {
      type: Object,
      required: true
    },
    show: {
      type: Boolean,
      default: false
    },
    status: {
        type: String,
        default() {
            return {}
        }
    },
  },
  data() {
    return {
      formMessage: {
        price:'',
        type: 0,
        timelist:[{start: '',end: '',code: 0 },],
        timeInfoList: []
      },
      timeList: []
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    handleAddItem() {
      const temp = this.formMessage.timeInfoList
      temp.push({
        start: '',
        end: '',
        code: 0
      })
      this.formMessage.timeInfoList = temp
    },
    handleDeleteItem() {
      const temp = this.formMessage.timeInfoList
      temp.pop()
      this.formMessage.timeInfoList = temp
    },
    handleSave() {
      const params_add = {
          price:this.formMessage.price,
          venue_id:this.courtInfo.venue_id,
          type: this.formMessage.type-1,
          name: this.$store.state.sportsType[this.formMessage.type] + "场地",
          status: []
      }
      const params_update = {
        court:[
          {
            price:this.formMessage.price,
            id:this.courtInfo.id,
            type:this.courtInfo.type,
            status: []
          }
        ]
      }
      this.formMessage.timeInfoList.forEach(item => {
        const startDate = moment().utc()
        const startHour = parseInt(item.start.substr(0,2))
        startDate.hour(startHour)
        startDate.minute(0)
        startDate.second(0)
        const endDate = moment().utc()
        const endHour = parseInt(item.end.substr(0,2))
        endDate.hour(endHour)
        endDate.minute(0)
        endDate.second(0)
        params_add.status.push({
          start: startDate.format(),
          end: endDate.format(),
          code: item.code
        })
        params_update.court[0].status.push({
          start: startDate.format(),
          end: endDate.format(),
          code: item.code
        })
      })
      if (this.status == 'add') {
        this.$axios.request({
            method: 'post',
            url: '/api/admin/create/court',
            data: params_add,
        }).then(() => {
            this.$emit('success-edit')
        }).catch(error => {
            console.log(error);
            console.log(params_add);
        })
      } else {
        this.$axios.request({
            method: 'post',
            url: '/api/admin/update/court',
            data: params_update
        }).then(() => {
            this.$emit('success-edit')
        }).catch(error => {
            console.log(error);
            console.log(params_update);
            //console.log(error.response.data.message);
        })
      }
    }
  },
  computed:{
    actualSportsType(){
      let len = this.$store.state.sportsType.length;
      return this.$store.state.sportsType.slice(1,len);
    }
  },
  mounted() {
    this.timeList = []
    for (let i = 7; i <= 22; i++) {
      let item = ''
      if (i < 10) {
        item = '0' + (i).toString() + ':00 - '
      } else {
        item = (i).toString() + ':00'
      }
      this.timeList.push(item)
    }
  },
  watch: {
    courtInfo(val) {
        const timeInfoList = []
        if (this.courtInfo.status.length > 0) {
            this.courtInfo.status.forEach(item => {
                timeInfoList.push({
                    start: item.start,
                    end: item.end,
                    code: item.code ? item.code : 0
                })
            })
        } else {
            timeInfoList.push({
                start: '',
                end: '',
                code: 0
            })
        }
        this.formMessage = {
          type: val.type,
          timeInfoList
        }
    },
    show(val) {
      if (val) {
        //const id = this.courtInfo.id
        const type = this.courtInfo.type
        const timeInfoList = []
        if (this.courtInfo.status.length > 0) {
            this.courtInfo.status.forEach(item => {
                timeInfoList.push({
                    start: item.start,
                    end: item.end,
                    code: item.code ? item.code : 0
                })
            })
        } else {
            timeInfoList.push({
                start: '',
                end: '',
                code: 0
            })
        }
        this.formMessage = {
          type,
          timeInfoList
        }
      } else {
        this.formMessage = {
          type: 0,
          timeInfoList: []
        }
      }
    },

  }
}
</script>

<style scoped>
.court-edit-modal {}
</style>