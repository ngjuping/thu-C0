<template>
    <div>
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content shadow-lg">
                    <div class="modal-header">
                        <h4 class="modal-title">发出拼场邀请</h4>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        
                        <div class="alert alert-danger" v-if="failedToSubmit">
                            无法提交... {{ err_msg }}
                        </div>
                        <div class="alert alert-success" v-if="success">
                            提交成功
                        </div>
                        <div class="pt-1">
                            <WysiwygEditor  ref="share-editor"
                                            placeholder="邀请信息"
                                            initial-content="" >

                            </WysiwygEditor>
                            <div class="mt-1 pb-2 mx-2 flex justify-end">
                                
                                <div class="spinner-border" v-if="submitting"><span class="sr-only"></span></div>
                                <button class="btn btn-primary" v-else @click="shareCourtPost" :disabled="success">
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
        }
    },
    methods:{
        shareCourtPost(){
            let content = this.sharePostContent;
            // XSS 过滤
            content = xss(content);

            // 去掉html tags 之后检查长度
            if(this.sharePostRawContent.length < 10){
                this.failedToSubmit = true;
                this.err_msg = "内容过短(少于10字)";
                return;
            }

            // 设置UI控制变量
            this.failedToSubmit = false;
            this.submitting = true;

            // 创建拼场帖子
            
            this.$axios
            .post('/api/manage/share/create',{
                    user_id: this.$store.state.logged_in_user_id,
                    content,
                    reservation_id:this.reservation.reservation_id
                }
            )
            .then(() => 
            {
                // 设置UI控制变量,获取成功
                this.failedToSubmit = false;
                this.success = true;

                // 关闭弹窗
                setTimeout(() => {
                    this.success = false;
                    this.$emit('hide-modal');
                },1000);
            })
            .catch((err)=>{
                this.failedToSubmit = true;
                this.err_msg = err.response.data.message;
                
            })
            .finally(()=>{this.submitting = false;})
            
        },
    },
    computed:{
        // 获取WYSIWYG文本框对象
        sharePostEditor () {
        return this.$refs['share-editor'].editor
        },
        // 获取WYSIWYG文本框对象的纯html文本
        sharePostContent () {
            return this.sharePostEditor.getHTML().replace(/<p>\s*<\/p>/g, '<br>')
        },
        // 获取WYSIWYG文本框对象的无html文本
        sharePostRawContent () {
            let regex = /(<([^>]+)>)/ig;
            return this.sharePostEditor.getHTML().replace(regex, "");
        }
    }
}
</script>