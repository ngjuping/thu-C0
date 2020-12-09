<template>
    <div class="reply-delModal">
        <div class="modal fade" id="delReplyModal" aria-hidden="true" tabindex="-1" role="dialog">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">提示</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>是否删除该反馈</p>
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
    name: 'ReplyDelModal',
    props: {
        replyDetail: {
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
                user_id: '',
                feedback_id: 0,
                content: '',
                stars: '',
                img: '',
            },
            file: null
        }
    },
    methods: {
        handleSave() {
            // 删除
            this.$axios.post('/api/manage/feedback/delete', this.formMessage).then((res) => {
                console.log(res, 'res')
                this.$emit('edit-success');
            }).catch(err => {
                console.log(err);
            })
        },
    },
    watch: {
        replyDetail(val) {
            this.formMessage = {
                user_id: val.user_id,
                feedback_id: val.feedback_id,
                content: val.content,
                stars: val.stars,
                img: val.img
            }
        }
    },
}
</script>

<style scoped>
    
</style>