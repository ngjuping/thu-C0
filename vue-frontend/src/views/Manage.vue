<template>
    <div class="container">
        
        <div id="title" class="p-3 px-4 bg-dark rounded shadow text-white mb-5">管理场地</div>
        <div class="alert alert-danger" v-if="!loadCourtsSuccess">
            无法加载您的场地信息
        </div>
        <div class="container text-left pl-0 mb-3">
            <div class="btn-group">
                    <div class="btn btn-danger" @click="$router.go(-1)">前一页</div>
            </div>
        </div>
        <div class="cotainer">
            <div class="row">
                <div class="col-12 col-md-6" v-for="court in courts" :key="court.reversation_id" >
                    <div class="card mb-3">
                        <div class="card-header">{{ court.details.name }}</div>
                        <div class="card-body text-left">
                            
                            <form>
                                <fieldset disabled>
                                    <div class="form-group">
                                    <label>生效日期</label>
                                    <input type="text" class="form-control" :placeholder="chineseTime(court.details.end)">
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

                            <small>下单于 &nbsp; {{ chineseTime(court.details.start) }}</small>
                            <hr>

                            <div class="btn-group">
                                <div class="btn btn-secondary" v-if="court.details.end < today">反馈</div>
                                <div class="btn-group" v-else>
                                    <div class="btn btn-primary">拼场</div>
                                    <div class="btn btn-danger">退场</div>
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
import Swal from 'sweetalert2';
import moment from 'moment';

export default {
    data(){
        return {
            loadCourtsSuccess:false,
            courts:[],
            today:moment().format(),
            reservation_type_str:[null,'先到先得','抽签','长期预定','队列'],
            status_str:[null,'成功预约未付款','已付款','已取消','已转让','未抽签','已抽签','队列中']
        }
    },
    methods:{
        chineseTime(time){

            let [year,month,day] = time.split("T")[0].split("-");
            
            let [hour,min] = time.split("T")[1].split("+")[0].split(":");
            
            return `${year}年${month}月${day}日 ${hour}点 ${min}分`
        }
    },
    mounted(){
        if(!this.$store.state.logged_in)
        {
            Swal.fire({
            title: "您还没有登陆",
            text: `请先点击右上角登陆或注册`,
            icon: "error",
            timer: 1500});
            return;
        }
        this.$axios
        .get(`/api/manage/courts?user_id=${this.$store.state.logged_in_user_id}`)
        .then((res) => {
            this.loadCourtsSuccess = true;
            this.courts = res.data.courts;
        })
        .catch(()=>{
            this.loadCourtsSuccess = false;
        })
    }
}
</script>

<style scoped>
#title{
    font-size:50px;
}

@media (max-width:760px) {
    #title{
        font-size:30px;
    }
}

@media (max-width:500px) {
    #title{
        font-size:20px;
    }
}
</style>