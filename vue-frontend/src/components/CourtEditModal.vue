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
                <label class="col-sm-3 col-form-label">命名场地</label>
                <div class="col-sm-8">
                  <input type="text" v-model="newCourtName" class="form-control" :placeholder="defaultCourtName"/>
                </div>
              </div>
              <div class="form-group row">
                <label class="col-sm-3 col-form-label">输入场地价格：</label>
                <div class="col-sm-8">
                  <input type="text" v-model.number="formMessage.price" class="form-control" placeholder="请输入"/>
                </div>
              </div>
              <div class="row form-group">
                <label class="col-sm-2">球类</label>
                <div class="col-sm-10">
                  <select v-model.number="formMessage.type" v-if="status=='add'" class="form-control" style="width: 100px">
                      <option
                        v-for="(item, index) in actualSportsType"
                        :value="index+1"
                        :key="index"
                      >{{item}}</option>
                  </select>
                  <span v-else>{{$store.state.sportsType[formMessage.type]}}</span>
                </div>
              </div>   
              <div class="alert alert-danger" v-if="err_msg"> {{err_msg}} </div>      
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="closeModal" id="closeCreateCourtButton">取消</button>
            <button type="button" class="btn btn-primary" @click="handleSave">保存</button>
            <span class="spinner-border spinner-border-md text-info" v-if="loading"></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';

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
        type: 1,
        timelist:[{start: '',end: '',code: 0 },],
        timeInfoList: [],
      },
      timeList: [],
      newCourtName:"",
      err_msg:null,
      loading:false
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
      if(this.formMessage.price === ''){
        this.err_msg = "请输入价格";
        return;
      }
      else if(isNaN(parseInt(this.formMessage.price))){
        this.err_msg = "价格必须为数字";
        return;
      }
      const params_add = {
          price:this.formMessage.price,
          venue_id:this.courtInfo.venue_id,
          type: this.formMessage.type,
          name: this.newCourtName,
          status: []
      }

      if(this.newCourtName.length === 0){
        params_add.name = this.defaultCourtName
      }
      this.loading=true;
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
      .finally(()=>{
          $('#closeCreateCourtButton').click();
          this.loading=false;
          this.$router.go();
      });
    }
  },
  computed:{
    actualSportsType(){
      let len = this.$store.state.sportsType.length;
      return this.$store.state.sportsType.slice(1,len);
    },
    defaultCourtName(){
      return this.$store.state.sportsType[this.formMessage.type] + "场地";
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