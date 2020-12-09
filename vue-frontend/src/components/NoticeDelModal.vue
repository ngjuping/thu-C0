<template>
    <div class="notice-delModal">
        <div class="modal fade" id="delNoticeModal" aria-hidden="true" tabindex="-1" role="dialog">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">提示</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>是否删除该通知</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">取消</button>
                        <button type="button" class="btn btn-primary" data-dismiss="modal" @click="handleSave">删除</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'NoticeDelModal',
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
                notice_id: '',
                title: '',
                content: '',
            },
        }
    },
    methods: {
        handleSave() {
            // 删除
            this.$axios.post('/api/admin/delete/notice', this.formMessage).then((res) => {
                console.log(res, 'res')
                this.$emit('edit-success');
            }).catch(err => {
                console.log(err);
            })
        },
    },
    watch: {
        noticeDetail(val) {
            this.formMessage = {
                notice_id: val.id,
                title: val.title,
                content: val.content
            }
        }
    },
}
</script>

<style scoped>
    
</style>