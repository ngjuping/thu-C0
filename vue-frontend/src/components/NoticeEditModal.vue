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
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">取消</button>
                    <button type="button" class="btn btn-primary" data-dismiss="modal" @click="handleSave">保存</button>
                </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
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
        }
    },
    methods: {
        handleSave() {
            if (this.status == 'add') {
                // 新增
                this.$axios.post('/api/admin/create/notice', this.formMessage).then((res) => {
                    console.log(res, 'res')
                    this.$emit('edit-success');
                }).catch(err => {
                    console.log(err);
                })
            } else if (this.status == 'edit') {
                // 编辑
                this.$axios.post('/api/admin/update/notice', this.formMessage).then((res) => {
                    console.log(res, 'res')
                    this.$emit('edit-success');
                }).catch(err => {
                    console.log(err);
                })
            } else if (this.status == 'delete') {
                // 删除
                this.$axios.post('/api/admin/delete/notice', this.formMessage).then((res) => {
                    console.log(res, 'res')
                    this.$emit('edit-success');
                }).catch(err => {
                    console.log(err);
                })
            }
        },
    },
    watch: {
        noticeDetail(val) {
            console.log(val, 'noticeDetail-watch');
            this.formMessage = {
                id: val.id,
                notice_id: val.notice_id,
                title: val.title,
                content: val.content,
            }
        }
    },
}
</script>

<style scoped>
    
</style>