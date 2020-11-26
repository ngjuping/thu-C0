<template>
    <div class="jumbotron text-left shadow p-3">
        <span id="title">{{ sports[info.type] }}场地{{ info.id }}</span>
            <div class="container">
                <div class="row">
                    <div class="col-12 col-md-12">
                        <div class="row d-flex justify-content-around" id="ranges">
                            <div class="col-12 col-md range d-flex justify-content-center align-items-center"  v-for="status in info.status" 
                            :class="[`courtstatus-${status.code} border border-success rounded`]"
                            :id="selectedCourt && selectedCourt.start === status.start?'activeCourt':'notActive'"
                            :key="`range${status.start}`"
                            :title="statustext[status.code]"
                            @click="selectCourt(status)"
                            data-toggle="tooltip" 
                            data-placement="top">
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
    props:["info","date"],
    data(){
        return {
            sports:["清除过滤","羽球","乒乓","网球","篮球"],
            statustext:["无状态","空场地","已有人预定"],
            selectedCourt:null
        }
    },
    mounted(){
        $('[data-toggle="tooltip"]').tooltip();
    },
    methods:{
        selectCourt(courtinfo){
            this.selectedCourt = courtinfo
        },
        getTimeOnly(date){
            if(!date) return "解析日期错误"
            try{
                //input: "1999-03-01T00:00:00+01:00"
                let date_second_part = date.split("T")[1]; //["1999-03-01","00:00:00+01:00"][1] = "00:00:00+01:00"
                let [hour,minutes] = date_second_part.split(":").slice(0,2); 
                return hour+minutes;
            }
            catch(err){
                return "解析日期错误"
            }
        },
        getBookStartTime(){
            return this.selectedCourt.start;
        },
        getBookEndTime(){
            return this.selectedCourt.start;
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
                    <h5 class="card-title">${ this.sports[this.info.type] } 场地 ${ this.info.id }</h5>
                    <p class="card-text">${this.date.join("/")}
                    <hr>
                    ${this.getTimeOnly(this.selectedCourt.start)} 到 ${this.getTimeOnly(this.selectedCourt.end)}</p>
                </div>
            </div>`,
            showCancelButton: true,
            cancelButtonText:"取消",
            confirmButtonText: '预定',
            showLoaderOnConfirm: true,
            icon:"info",
            preConfirm: () => {
                return this.$axios
                .post('/api/book',{
                    user_id: this.$store.state.logged_in_user,
                    court_id:this.info.id,
                    start:this.getBookStartTime(),
                    end:this.getBookEndTime(),
                    }
                )
                .then((res) => {
                   Swal.fire({
                    title: `预定成功`,
                    icon:"success",
                    showCloseButton:true,
                    showConfirmButton:true,
                    confirmButtonText:"查看我的预约详情",
                    text:`服务器返回信息：${res.data.message}`,
                    timer: 3000,
                    })
                    .then((result) => {
                        if(result.isConfirmed){
                            this.$router.push({name:'Manage'});
                        }
                    
                })
                })
                
                .catch((err) => {
                    Swal.showValidationMessage(
                    `请求失败: ${err.response.data.message}`
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
.courtstatus-1{
    background-color:greenyellow;
    opacity:0.5;
}

.courtstatus-2{
    background-color:red;
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