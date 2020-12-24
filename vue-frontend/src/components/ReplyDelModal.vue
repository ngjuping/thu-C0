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
                    <div class="alert alert-danger" v-if="err_msg">
                        {{ err_msg }}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal" id="closeDelFeedbackModal">取消</button>
                        <button type="button" class="btn btn-primary" @click="handleSave">删除</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import $ from 'jquery';

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
            file: null,
            err_msg: null
        }
    },
    methods: {
        handleSave() {
            // 删除
            this.$axios.post('/api/manage/feedback/delete', this.formMessage)
            .then((res) => {
                console.log(res, 'res')
                this.$emit('edit-success');
                $('#closeDelFeedbackModal').click();
            }).catch(err => {
                console.log(err);
                this.err_msg = err.response.data.message;
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