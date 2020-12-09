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
              <div class="row form-group">
                <label class="col-sm-2">场地</label>
                <div class="col-sm-10">
                  <select v-model="formMessage.type" v-if="status=='add'" class="form-control" style="width: 100px">
                      <option
                        v-for="(item, index) in sports"
                        :value="index+1"
                        :key="index"
                      >{{item}}</option>
                  </select>
                  <span v-else>{{sports[formMessage.type]}}</span>
                </div>
              </div>
              <div class="row form-group">
                <div class="col-sm-2">场地配置</div>
                <div class="col-sm-10"><button type="button" class="btn btn-primary" @click="handleAddItem">添加</button></div>
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
                    <option :value="0">可预定</option>
                    <option :value="1">已预定</option>
                  </select>
                </div>
                <div class="col-sm-3" v-if="index === formMessage.timeInfoList.length - 1">
                  <button type="button" class="btn btn-danger" @click="handleDeleteItem">删除</button>
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
      sports:[null,"羽球","篮球","乒乓"],
      formMessage: {
        type: 0,
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
      const params = {
        court: [
          {
            id: this.courtInfo.id,
            type: this.status == 'add' ? this.formMessage.type-1 : this.courtInfo.type,
            status: []
          }
        ]
      }
      this.formMessage.timeInfoList.forEach(item => {
        const startDate = moment()
        const startHour = parseInt(item.start.substr(0,2))
        startDate.hour(startHour)
        const endDate = moment()
        const endHour = parseInt(item.end.substr(0,2))
        endDate.hour(endHour)
        params.court[0].status.push({
          start: startDate.format(),
          end: endDate.format(),
          code: item.code
        })
      })
      if (this.status == 'add') {
        this.$axios.request({
            method: 'post',
            url: '/api/admin/create/court',
            data: params
        }).then(() => {
            this.$emit('success-edit')
        }).catch(error => {
            console.log(error)
        })
      } else {
        this.$axios.request({
            method: 'post',
            url: '/api/admin/update/court',
            data: params
        }).then(() => {
            this.$emit('success-edit')
        }).catch(error => {
            console.log(error)
        })
      }
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
    show(val) {
      console.log(val,this.courtInfo)
      if (val) {
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