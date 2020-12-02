<template>
    <div class="col-12 col-md-6">
        <div class="card mb-3">
            <div class="card-header">{{ court.details.name }}</div>
            <div class="card-body text-left">
                
                <form>
                    <fieldset disabled>
                        <div class="form-group">
                        <label>预定日期</label>
                        <input type="text" class="form-control" 
                        :placeholder="`${chineseTime(court.details.start)} 到 ${chineseTime(court.details.end)}`">
                        </div>
                        <div class="form-group">
                        <label>场地状态&nbsp;
                            <font-awesome-icon icon="exclamation-triangle" class="text-danger" v-if="court.status === 1"/>
                            <font-awesome-icon icon="check-circle" class="text-info" v-if="court.status === 2"/>
                            </label>
                        <input type="text" class="form-control text-info" :placeholder="status_str[court.status]">
                        </div>
                        <div class="form-group">
                        <label>预定类型</label>
                        <input type="text" class="form-control" :placeholder="reservation_type_str[court.type]">
                        </div>
                    </fieldset>
                </form>

                <small>下单于 &nbsp; {{ chineseTime(court.details.created) }}</small>
                <hr>
                <small v-if="court.details.paid_at">支付于 &nbsp; {{ chineseTime(court.details.paid_at) }}</small>
                <hr v-if="court.details.paid_at">

                <div class="btn-group">
                    <div class="btn btn-secondary" 
                    v-if="court.details.end < today">反馈</div>
                    <div class="btn-group" v-else>
                        <div class="btn btn-primary" data-toggle="modal" :data-target="`#share_modal`">拼场</div>
                        <div class="btn btn-danger" @click="confirmQuit">退场</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal fade" id="share_modal" ref="create_share_modal">
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
                        <div class="pt-1">
                            <WysiwygEditor class="w-full post-editor" ref="post-editor"
                                            placeholder="邀请信息"
                                            initial-content="">

                                
                            </WysiwygEditor>
                            <div class="mt-1 pb-2 mx-2 flex justify-end">
                                
                                <div class="spinner-border" v-if="submitting">
                                    <span class="sr-only">Loading...</span>
                                </div>
                                <div class="btn btn-primary" v-else @click="shareCourtPost(sharePostContent)">
                                    提交
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
    
    </div>
</template>

<script>
import moment from 'moment';
import WysiwygEditor from '@/components/WYSIWYG.vue';
import $ from 'jquery';
import Swal from 'sweetalert2'

export default {
    props:["court"],
    components:{WysiwygEditor},
    data(){
        return {
            today:moment().format(),
            reservation_type_str:[null,'先到先得','抽签','长期预定','队列'],
            status_str:[null,'成功预约未付款','已付款','已取消','已转让','未抽签','已抽签','队列中'],
            failedToSubmit:false,
            err_msg:"默认错误",
            submitting:false
        }
    },
    methods:{
        chineseTime(time){
            try{
                let [year,month,day] = time.split("T")[0].split("-");
            
            let [hour,min] = time.split("T")[1].split("+")[0].split(":");
            
            return `${year}年${month}月${day}日 ${hour}点 ${min}分`;
            }
            catch(e){
                return "没有时间";
            }
        },
        shareCourtPost(content){
            this.failedToSubmit = false;
            this.submitting = true;
            this.$axios
            .post('/api/manage/share/create',{
                user_id: this.$store.state.logged_in_user_id,
                content,
                reservation_id:this.court.reservation_id
            }
            )
            .then(() => 
            {
                this.failedToSubmit = false;
                console.log("Submitted");
                $("#share_modal").modal('hide');
            })
            .catch((err)=>{
                this.failedToSubmit = true;
                this.err_msg = err.response.data.message;
                
            })
            .finally(()=>{this.submitting = false;})
            
        },
        confirmQuit(){
            Swal.fire({
                title: '是否确定退场',
                text: "该行动将无法撤回！",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                showLoaderOnConfirm: true,
                cancelButtonText: '取消',
                confirmButtonText: '确认',
                preConfirm:()=> {
                    return this.$axios
                    .post('/api/manage/reservation/cancel',{
                        reservation_id:this.court.reservation_id
                        }
                    )
                    .then(() => 
                    {
                        Swal.fire({
                        title:'退场成功!',
                        text:'已将该场地让出。',
                        icon:'success',
                        timer:1000}
                        )
                    })
                    .catch((err)=>{
                        console.log(err);
                        Swal.showValidationMessage(
                        `请求失败: ${err.response.data.message}`
                        )
                    })
                    
                }
                })
        }
    },
    computed:{
        
        sharePostEditor () {
        return this.$refs['post-editor'].editor
        },

        sharePostContent () {
            return this.sharePostEditor.getHTML().replace(/<p>\s*<\/p>/g, '<br>')
        },
    }
}
</script>