<template>
    <div class="col-12 col-md-6">
        <div class="card mb-3">
            <div class="card-header">{{ court.details.name }}</div>
            <div class="card-body text-left">
                
                <form>
                    <fieldset>
                        <div class="form-group">
                        <label><b>预定日期</b></label>
                        <input type="text" class="form-control-plaintext" 
                        :placeholder="`${chineseTime(court.details.start)} 到 ${chineseTime(court.details.end)}`">
                        </div>
                        <div class="form-group">
                        <label><b>场地状态</b>&nbsp;
                            <font-awesome-icon icon="exclamation-triangle" class="text-danger" v-if="court.status === 1"/>
                            <font-awesome-icon icon="check-circle" class="text-info" v-if="court.status === 2"/>
                            </label>
                        <input type="text" class="form-control-plaintext" :placeholder="$store.state.reservationStatus[court.status]">
                        </div>
                        <div class="form-group">
                        <label><b>预定类型</b></label>
                        <input type="text" class="form-control-plaintext" :placeholder="$store.state.reservationType[court.type]">
                        </div>
                    </fieldset>
                </form>

                <small>下单于 &nbsp; {{ chineseTime(court.details.created) }}</small>
                <hr>
                <small v-if="court.details.paid_at">支付于 &nbsp; {{ chineseTime(court.details.paid_at) }}</small>
                <hr v-if="court.details.paid_at">

                <div class="btn-group">
                    <div class="btn btn-secondary" 
                    v-if="court.details.end < today" data-toggle="modal" :data-target="`#feedback_modal-${this.court.reservation_id}`">反馈</div>
                    <div class="btn-group" v-else>
                        <div class="btn btn-primary" data-toggle="modal" :data-target="`#share_modal-${this.court.reservation_id}`">拼场</div>
                        <div class="btn btn-danger" @click="confirmQuit">退场</div>
                    </div>
                </div>
            </div>
        </div>
        <ShareModal :reservation="court"
                    class="modal fade" :id="`share_modal-${court.reservation_id}`"
                    @hide-modal="hideShareModal"></ShareModal>
        <FeedbackModal :reservation="court" 
                       class="modal fade" :id="`feedback_modal-${court.reservation_id}`"
                       @hide-modal="hideFeedbackModal"></FeedbackModal>
            
    
    </div>
</template>

<script>
import moment from 'moment';
import FeedbackModal from'@/components/FeedbackModal.vue'
import ShareModal from'@/components/ShareModal.vue'
import $ from 'jquery';
import Swal from 'sweetalert2'

export default {
    props:["court"],
    components:{FeedbackModal,ShareModal},
    data(){
        return {
            today:moment().format(),
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
        
        // 退场函数
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
        },
        hideFeedbackModal(){
            $(`#feedback_modal-${this.court.reservation_id}`).modal('hide');
        },
        hideShareModal(){
            $(`#share_modal-${this.court.reservation_id}`).modal('hide');
        },
    }
}
</script>