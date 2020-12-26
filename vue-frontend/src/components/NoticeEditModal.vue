<template>
    <div class="notice-modal">
        <div class="modal fade" id="editNoticeModal" aria-hidden="true" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">更新通知</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form>
                    <div class="form-group row">
                        <label class="col-sm-2 col-form-label">标题</label>
                        <div class="col-sm-10">
                        <textarea v-model="formMessage.title" class="form-control" rows="3" placeholder="请输入"/>
                        </div>
                    </div>
                    <div class="form-group row">
                        <label class="col-sm-2 col-form-label">内容</label>
                        <div class="col-sm-10">
                        <input type="text" v-model="formMessage.content" class="form-control" placeholder="请输入"/>
                        </div>
                    </div>
                    <div class="alert alert-danger" v-if="err_msg">
                        {{ err_msg }}
                    </div>  
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" id="closeNoticeEditModal" data-dismiss="modal">取消</button>
                    <button type="button" class="btn btn-primary" @click="handleSave">保存</button>
                    
                </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import $ from 'jquery';

export default {
    name: 'NoticeModal',
    props: {
        noticeDetail: {
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
        }
    },
    data() {
        return {
            formMessage: {
                id: '',
                notice_id: '',
                content: '',
                title: '',
            },
            err_msg:null
        }
    },
    methods: {
        handleSave() {

            // 通知标题长度
            if(!this.formMessage.title || this.formMessage.title.length < 3){
                this.err_msg = "通知标题过短(不能少于3个字)"
                return;
            }
            else if(this.formMessage.title.length > 10){
                this.err_msg = "通知标题过长(不能多于10字)"
                return;
            }
            // 通知内容长度
            if(!this.formMessage.content || this.formMessage.content.length < 3){
                this.err_msg = "通知内容过短(不能少于3个字)"
                return;
            }
            else if(this.formMessage.content.length > 100){
                this.err_msg = "通知内容过长(不能多于100字)"
                return;
            }

            if (this.status == 'add') {
                // 新增
                this.$axios.post('/api/admin/create/notice', this.formMessage)
                .then(() => {
                    this.$emit('edit-success');
                    $('#closeNoticeEditModal').click();
                })
                .catch(err => {
                    console.log(err);
                    this.err_msg = err.response.data.message;
                })
            } 
            else if (this.status == 'edit') {
                // 编辑
                this.$axios.post('/api/admin/update/notice', this.formMessage)
                .then(() => {
                    this.$emit('edit-success');
                    $('#closeNoticeEditModal').click();
                }).catch(err => {
                    console.log(err);
                    this.err_msg = err.response.data.message;
                })
            } 
            else if (this.status == 'delete') {
                // 删除
                this.$axios.post('/api/admin/delete/notice', this.formMessage)
                .then(() => {
                    this.$emit('edit-success');
                    $('#closeNoticeEditModal').click();
                }).catch(err => {
                    console.log(err);
                    this.err_msg = err.response.data.message;
                })
            }
        },
    },
    watch: {
        noticeDetail(val) {
            console.log(val, 'noticeDetail-watch');
            this.formMessage = {
                notice_id: val.id,
                title: val.title,
                content: val.content,
            }
        }
    },
}
</script>

<style scoped>
    
</style>