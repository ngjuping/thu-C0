<template>
    <div class="reply-modal">
        <div class="modal fade" id="ReplyModal" aria-hidden="true" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">回复反馈</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="form-group row">
                            <label class="col-sm-2 col-form-label">回复</label>
                            <div class="col-sm-10">
                            <input type="text" v-model="formMessage.reply" class="form-control" placeholder="请输入"/>
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
// import $ from 'jquery'
export default {
    name: 'ReplyModal',
    props: {
        feedbackId: {
            type: Number,
            default() {
                return {}
            }
        },
    },
    data() {
        return {
            formMessage: {
                feedback_id: 0,
                reply: '',
                solved:'',
            },
        }
    },
    methods: {
        handleSave() {
            this.$axios.post('/api/admin/reply/feedback', this.formMessage).then((res) => {
                console.log(res, 'res')
                this.$emit('reply-success');
            }).catch(err => {
                console.log(err);
            })
        },
    },
    watch: {
        feedbackId(val) {
            this.formMessage.feedback_id = val;
            this.formMessage.solved = true;
        }
    },
}
</script>

<style scoped>
    
</style>