<template>
  <div class="review-modal" id="venue_edit_modal">
    <div class="modal fade" id="editVenueModal" aria-hidden="true" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">{{status=='add'?'新增':'编辑'}}场馆</h5>
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
                    <input type="file" class="form-control-file" @change="handleFileChange">
                  </div>
                </div>
              </div>
              
              <div class="alert alert-danger" v-if="err_msg">
                  {{err_msg}}
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" id="closeVenueEdit">取消</button>
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
  name: 'VenueEditModal',
  props: {
    venueDetail: {
      type: Object,
      default() {
        return {}
      }
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
        name: '',
        description: '',
        img: '',
        venue_id:''
      },
      file: null,
      err_msg:null,
      loading:false
    }
  },
  methods: {
    handleFileChange(e) {
      
      this.err_msg = null;
      this.file = e.target.files[0]
    },
    handleSave() {
      
      if(!this.file || this.file.value === ''){
        this.err_msg = "必须上传图片"
        return;
      }
      const params = new FormData()
      params.set('name', this.formMessage.name)
      params.set('description', this.formMessage.description)
      params.set('venue_id',this.formMessage.venue_id)
      params.append('img', this.file)
      this.formMessage.img = this.file;
      
      this.loading = true;
      if (this.status == 'add') {
        // 新增
        this.$axios.post('/api/admin/create/venue', params,{headers:{'Content-Type':'multipart/form-data'}}).then((res) => {
            console.log(res, 'res')
            this.$emit('edit-success');
        }).catch(err => {
            console.log(err.response.data);

        })
        .finally(() => {
          $('#closeVenueEdit').click();
          this.loading = false;
        })
      } else {
        this.$axios.request({
            method: 'post',
            url: '/api/admin/update/venue',
            data: params,
            headers: {
                    'Content-Type':'multipart/form-data'
                }
        }).then(() => {
            this.$emit('edit-success')
        }).catch((error) => {
            console.log(error.response.data.message)
        })
        .finally(() => {
          $('#closeVenueEdit').click();
          this.loading = false;
        })
      }
    }
  },
  watch: {
    venueDetail (val) {
      console.log(val);
      this.formMessage = {
        name: val.name,
        description: val.description,
        img: val.img,
        venue_id: val.id
      }
    }
  }
}
</script>

<style scoped>

</style>