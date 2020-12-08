<template>
    <div class="col-12 col-lg-6 mb-3 ">
        
        <div class="card h-100 border border-dark">
            <div class="card-header bg-dark text-light">
                {{ resv.details.name }}
            </div>
            <div class="card-body text-left">
                
                <!-- 订单信息 -->
                <form>
                    <fieldset>
                        <div class="form-group">
                        <label><b>预定日期</b></label>
                        <input type="text" class="form-control-plaintext" 
                        :placeholder="`${chineseTime(resv.details.start)} 到 ${chineseTime(resv.details.end)}`">
                        </div>
                        <div class="form-group">
                        <label><b>场地状态</b>&nbsp;
                            <font-awesome-icon icon="exclamation-triangle" class="text-danger" v-if="resvStatus === 1"/>
                            <font-awesome-icon icon="check-circle" class="text-info" v-if="resvStatus === 2"/>
                            </label>
                        <input type="text" class="form-control-plaintext" :placeholder="resvStatusStr">
                        </div>
                        <div class="form-group">
                        <label><b>预定类型</b></label>
                        <input type="text" class="form-control-plaintext" :placeholder="$store.state.reservationType[resv.type]">
                        </div>
                    </fieldset>
                </form>

                <small>下单于 &nbsp; {{ chineseTime(resv.details.created) }}</small>
                <hr>
                <small v-if="resv.details.paid_at">支付于 &nbsp; {{ chineseTime(resv.details.paid_at) }}</small>
                <div class="m-3"></div>

                <!-- 拼场操作界面 -->
                <div class="btn-group mr-3" v-if="resv.shared">
                    <div class="input-group-prepend">
                    <div class="input-group-text">拼场菜单</div>
                    </div>
                    <div class="btn-group">
                        <div class="btn btn-dark">修改</div>
                        <div class="btn btn-dark">删除</div>
                    </div>
                </div>
                <div class="mb-3" v-if="resv.shared"></div>

                <!-- 反馈操作界面 -->
                <div class="btn-group mr-3" v-if="resv.reviewed">
                    <div class="input-group-prepend">
                    <div class="input-group-text">反馈菜单</div>
                    </div>
                    <div class="btn-group">
                        <div class="btn btn-dark">修改</div>
                        <div class="btn btn-dark">删除</div>
                    </div>
                </div>
                <div class="mb-3" v-if="resv.reviewed"></div>

                <div class="btn-group">
                    <!-- 反馈按钮只能在订单过期后显示 -->
                    <div class="btn btn-secondary" 
                        v-if="outDated && !resv.reviewed" 
                        data-toggle="modal" 
                        :data-target="`#feedback_modal-${this.resvStatus}`">
                        反馈
                    </div>
                    
                    <!-- 还没过期的场地判断可以拼场？退场？转让？ -->
                    <div class="btn-group shadow" v-else>

                        <!-- 如果还没拼过场，显示该按钮 -->
                        <div class="btn btn-primary" 
                            data-toggle="modal" 
                            :data-target="`#share_modal-${this.resvStatus}`"
                            v-if="!resv.shared">拼场</div>

                        <!-- 根据订单状态，如果可以转让，显示该按钮 -->
                        <div class="btn btn-warning" 
                            data-toggle="modal" 
                            :data-target="`#transfer_modal-${this.resvStatus}`"
                            v-if="transferrable">转让</div>

                        <!-- 根据订单状态，如果可以退场，显示该按钮 -->
                        <div class="btn btn-danger" @click="confirmQuit" v-if="cancellable">退场</div>
                    </div>
                </div>
            </div>
        </div>
        <ShareModal :reservation="resv"
                    class="modal fade" :id="`share_modal-${resv.reservation_id}`"
                    @hide-modal="hideShareModal"></ShareModal>
        <FeedbackModal :reservation="resv" 
                       class="modal fade" :id="`feedback_modal-${resv.reservation_id}`"
                       @hide-modal="hideFeedbackModal"></FeedbackModal>
        <TransferModal :reservation="resv" 
                       class="modal fade" :id="`transfer_modal-${resv.reservation_id}`"
                       @hide-modal="hideTransferModal"></TransferModal>
    
    </div>
</template>

<script>
import moment from 'moment';

import FeedbackModal from '@/components/FeedbackModal.vue';
import ShareModal from '@/components/ShareModal.vue';
import TransferModal from '@/components/TransferModal.vue';

import $ from 'jquery';
import Swal from 'sweetalert2'

export default {
    props:["resv"],
    components:{FeedbackModal,ShareModal,TransferModal},
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
                        reservation_id:this.resvStatus
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
            $(`#feedback_modal-${this.resvStatus}`).modal('hide');
        },
        hideShareModal(){
            $(`#share_modal-${this.resvStatus}`).modal('hide');
        },
        hideTransferModal(){
            $(`#transfer_modal-${this.resvStatus}`).modal('hide');
        },
    },
    computed:{
        outDated(){
            return this.resv.details.end < this.today;
        },
        resvStatus(){
            return this.resv.status;
        },
        resvStatusStr(){
            return this.$store.state.reservationStatus[this.resvStatus];
        },
        transferrable(){
            // 如果已付款且还没过期
            return this.resvStatus === 2 && !this.outDated;
        },
        cancellable(){
            // 如果已付款且还没过期
            return this.resvStatus === 2 && !this.outDated;
        }
    }
}
</script>