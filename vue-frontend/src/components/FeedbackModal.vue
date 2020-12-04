<template>
    <div >
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content shadow-lg">
                <div class="modal-header">
                    <h4 class="modal-title">反馈场地</h4>
                    <button type="button" class="close" data-dismiss="modal">
                    <span>&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <!-- 提交状态显示 -->
                    <div class="alert alert-danger" v-if="failedToSubmit">
                        无法提交... {{ err_msg }}
                    </div>
                    <div class="alert alert-success" v-if="success">
                        提交成功
                    </div>

                    <div class="pt-1">
                        <!-- 反馈内容编辑器 -->
                        <WysiwygEditor  ref="feedback-editor"
                                        placeholder="反馈信息"
                                        initial-content="" >                                
                        </WysiwygEditor>
                        
                        <!-- 可上传一张图片 -->
                        <input type="file" class="form-control-file" @change="handleFileChange">

                        <!-- 提交按钮 -->
                        <div class="mt-1 pb-2 mx-2 flex justify-end">
                            <div class="spinner-border" v-if="submitting"><span class="sr-only"></span></div>
                            <button class="btn btn-primary" v-else @click="sendFeedback(feedback_content)" :disabled="success">
                                提交
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>
<script>
import xss from 'xss';
import WysiwygEditor from '@/components/WYSIWYG.vue';

export default {
    props:["reservation"],
    components:{WysiwygEditor},
    data(){
        return {
            failedToSubmit:false,
            err_msg:"默认错误",
            submitting:false,
            success:false,
            img_file:null,
            stars:5,
        }
    },
    methods:{
        handleFileChange(e) {

            // 更新上传文件
            this.img_file = e.target.files[0]
        },
        sendFeedback(content) {
            
            // 去掉html tags 之后检查长度
            if(this.feedback_raw_content.length < 10){
                this.failedToSubmit = true;
                this.err_msg = "内容过短(少于10字)";
                return;
            }

            // 设置UI控制变量
            this.failedToSubmit = false;
            this.submitting = true;

            // 手动创造form请求参数
            let params = new FormData()
            params.set('user_id', this.$store.state.logged_in_user_id)
            params.set('reservation_id', this.reservation.reservation_id)
            params.set('content', content)
            params.set('stars', this.stars)
            params.append('img', this.img_file)

            // FormData私有类对象，访问不到，可以通过get判断值是否传进去
            // console.log(params.get('reservation_id'));

            this.$axios.request({
                method: 'post',
                url: '/api/manage/feedback/create',
                data: params,
                headers: {
                    'Content-Type':'multipart/form-data'
                }
            })
            .then(() => {
                // 设置UI控制变量,获取成功
                this.failedToSubmit = false;
                this.success = true;

                 // 关闭弹窗
                setTimeout(() => {
                    this.success = false;

                    // 发送信号让parent关闭本弹窗
                    this.$emit('hide-modal');
                },1000);

            })
            .catch((err) => {

                // 提示错误存在，更新错误信息
                this.failedToSubmit = true;
                this.err_msg = err.response.data.message;
            })
            .finally(() => {

                // 不管正确或错误，最后都要把spinner隐藏起来
                this.submitting = false;
            })
        }
    },
    computed:{
        feedback_editor(){
            return this.$refs["feedback-editor"].editor;
        },
        feedback_content(){
            return xss(this.feedback_editor.getHTML());
        },
        // 获取WYSIWYG文本框对象的无html文本
        feedback_raw_content() {
            let regex = /(<([^>]+)>)/ig;
            return this.feedback_editor.getHTML().replace(regex, "");
        },
    }
}
</script>