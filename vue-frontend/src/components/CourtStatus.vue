<template>
    <div class="jumbotron text-left shadow p-3">
        <div class="container">
            <div class="row">
                <div class="col-12 col-sm-4 mb-sm-0 mb-3"><span id="title">{{ info.name }}</span></div>
                <div class="col-12 col-sm d-flex align-items-center justify-content-end"><span class="card-footer bg-dark text-white rounded p-2">剩余 {{availableTimes}} 时间段可预定</span></div>
            </div>
        </div>
        
            <div class="my-3 container">
                <div class="row">
                    <div class="col-12 col-md-12">
                        <div class="row d-flex justify-content-around" id="ranges">
                            <div class="jumbotron p-2 d-flex align-items-center justify-content-center" v-if="!info.status.length">
                                <span class="lead">没有可预定的时间段</span>
                                <font-awesome-icon icon="frown-open" class="w-50 h-50" style="max-width:50px;" />
                            </div>
                            <div class="col-12 col-md range d-flex justify-content-center align-items-center"  
                            v-for="status in info.status"
                            :class="[`${courtStatusCode(status)} border border-success rounded`]"
                            :id="selectedCourt && selectedCourt.start === status.start?'activeCourt':'notActive'"
                            :key="`range${status.start}`"
                            :title="courtState(status)"
                            @click="selectCourt(status)"
                            data-toggle="tooltip" 
                            data-placement="top">
                            <span class="d-inline d-md-none bg-white">{{ getTimeOnly(status.start) }} -- {{ getTimeOnly(status.end) }}</span>
                            </div>
                        </div>
                        
                    </div>
                    <div class="col-6 col-md-12 d-none d-md-block">
                        <div class="row d-flex justify-content-end">
                            <div class="col px-0" v-for="(status) in info.status" :key="`label${status.start}`">
                                <div class="pl-0">
                                    {{ getTimeOnly(status.start) }}
                                </div>      
                            </div>
                            <div class="pr-0" v-if="info.status.length">
                                {{ getTimeOnly(info.status[info.status.length-1].end) }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        <div class="d-flex justify-content-between" v-if="selectedCourt">
            <span>
                您选中了时段&nbsp;<b>{{ getTimeOnly(selectedCourt.start) }}</b> &nbsp;至&nbsp; <b>{{ getTimeOnly(selectedCourt.end) }}</b>
            </span>
            <button type="button" class="btn btn-secondary" @click="submitBooking">
                预定这个场地！
            </button>
        </div>
            
           
    </div>
    
</template>
<script>
import $ from 'jquery'
import Swal from 'sweetalert2'

export default {
    props:["info","date","clear"],
    data(){
        return {
            selectedCourt:null
        }
    },
    watch:{
        async info(){
            await $('[data-toggle="tooltip"]').tooltip('dispose');
            $('[data-toggle="tooltip"]').tooltip();
        },
        clear(val){
            if(val === true){
                this.selectedCourt = null;
            }
        }
    },
    mounted(){
        $('[data-toggle="tooltip"]').tooltip();
    },
    computed:{
        availableTimes(){
            let total = 0;
            this.info.status.forEach((curr) => { total += (curr.code === 1 || curr.code === 3) && !this.outDated(curr)? 1:0 });
            return total;
        },
        sportsType(){
            return this.$store.state.sportsType[parseInt(this.info.type)];
        },
        usingPhone(){
            return /Mobi|Android/i.test(navigator.userAgent) ;
        }
    },
    methods:{
        outDated(status){
            let now = new Date();
            return new Date(status.start) < now;
        },
        courtStatusCode(status){
            let final_code = status.code;
            if(this.outDated(status)){
                final_code = 4;
            }
            return `courtStatus-${final_code}`;
        },
        courtState(status){
            if(this.outDated(status)){
                return `无法预定`;
            }
            return this.$store.state.courtStatus[parseInt(status.code)];
        },
        selectCourt(courtinfo){
            if(this.outDated(courtinfo)){
                return;
            }
            this.selectedCourt = courtinfo
        },
        getTimeOnly(date){
            if(!date) return "解析日期错误"
            try{
                //input: "1999-03-01T00:00:00+01:00"
                let date_second_part = date.split("T")[1]; //["1999-03-01","00:00:00+01:00"][1] = "00:00:00+01:00"
                let [hour,minutes] = date_second_part.split(":").slice(0,2); 
                return hour + ':' + minutes;
            }
            catch(err){
                return "解析日期错误"
            }
        },
        getBookStartTime(){
            return this.selectedCourt.start;
        },
        getBookEndTime(){
            return this.selectedCourt.end;
        },
        submitBooking(){
            if(!this.$store.state.logged_in)
            {
                Swal.fire({
                title: "您还没有登陆",
                text: `请先点击右上角登陆或注册`,
                icon: "error",
                timer: 1500});
                return;
            }
            Swal.fire({
            title: '请检查订单：',
            html: `
            <div class="text-left card mb-4">
                <div class="card-header">
                    您的订单
                </div>
                <div class="card-body">
                    <h5 class="card-title">${ this.info.name }</h5>
                    <p class="card-text">
                    球类：<b>${this.$store.state.sportsType[this.info.type]}</b>
                    <br/>
                    日期：${this.date.join("/")}
                    <hr>
                    <b>${this.getTimeOnly(this.selectedCourt.start)}</b> 到 <b>${this.getTimeOnly(this.selectedCourt.end)}</b></p>
                </div>
            </div>`,
            showCancelButton: true,
            cancelButtonText:"取消",
            confirmButtonText: '预定',
            showLoaderOnConfirm: true,
            icon:"info",
            preConfirm: () => {

                // 根据场地状态调整api路径, switch提升可扩展性
                let api_url = '/api/book';
                
                switch(this.selectedCourt.code){
                    case 3:
                        api_url = '/api/draw';
                    break;
                }

                // 发出订场POST请求
                return this.$axios
                .post(api_url,{
                    court_id:this.info.id,
                    start:this.getBookStartTime(),
                    end:this.getBookEndTime(),
                    }
                )
                .then((res) => {
                    if(this.selectedCourt.code === 3){
                        Swal.fire({
                        title: `预定成功`,
                        icon:"success",
                        text:"您已经加入抽签队列，本周日将进行抽签。您可以随时到“我的场地”查看结果。",
                        showCloseButton:true,
                        showConfirmButton:true,
                        confirmButtonText:"明白"
                        });
                        return;
                    }

                    let chosenPaymentMethod;

                    // 订场成功
                    Swal.fire({
                        title: `预定成功`,
                        icon:"success",
                        showCloseButton:true,
                        showConfirmButton:true,
                        confirmButtonText:"支付",
                        showDenyButton: true,
                        denyButtonText:"继续预定",
                        denyButtonColor: 'grey',
                        showLoaderOnConfirm: true,
                        text:`服务器返回信息：${res.data.message}`,
                        html:`<div class="lead">您可以待会儿支付。</div>
                        <br/>
                        选择您的支付方式：
                        <select name="payments">
                            <option value="alipay">支付宝</option>
                            <option value="offline">线下支付</option>
                        </select><hr/>`,
                        preConfirm: () => {
                            
                            let content = Swal.getContent();
                            chosenPaymentMethod = content.querySelector('select').value;
                            console.log(chosenPaymentMethod);

                            // 进一步支付
                            return this.$axios.post(`/api/pay/${chosenPaymentMethod}`,{
                                reservation_id: res.data.reservation_id,
                                isPhone:this.usingPhone
                            })
                            .then((res) => {
                                // axios只允许200-299状态码进入then
                                // 线下支付选择后会，请求成功就会进入这里
                                if(chosenPaymentMethod === 'offline'){
                                    Swal.fire({
                                        title: `请持学生证到柜台支付！`,
                                        icon:"info",
                                        showCloseButton:true,
                                        showConfirmButton:true,
                                        confirmButtonText:"我知道了"
                                    })
                                }
                                // 线上支付
                                else{
                                    // 跳转到支付api
                                    window.location.href = res.headers.location;
                                    return;
                                }
                            })
                            .catch((err) => {
                                Swal.showValidationMessage(
                                    `跳转失败: ${err.response.data.message}`
                                )
                            })
                        }
                    })
                })
                .catch((err) => {
                    Swal.showValidationMessage(
                    `订场失败: ${err.response.data.message}`
                    )
                })
            },
            allowOutsideClick: () => !Swal.isLoading()
            });
        }
    }
}
</script>

<style scoped>
#title{
    font-size:30px;
}

#activeCourt{
    background-color:yellow;
    opacity:0.8;
}
.courtStatus-1{
    background-color:greenyellow;
    opacity:0.5;
}

.courtStatus-2{
    background-color:red;
    opacity:0.5;
}

.courtStatus-3{
    background-color:orange;
    opacity:0.5;
}

.courtStatus-4{
    background-color:grey;
    opacity:0.5;
}

.range,.label{
    height:50px;
}

.range:hover{
    cursor:pointer !important;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    transform:scale(1.1);
    opacity:1;
    z-index:1
}

@media (max-width:760px) {
    #title{
        font-size:25px;
    }
    
    #ranges{
        max-height:300px;
        overflow-y:scroll;
    }
}
</style>