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
                    <div class="btn btn-secondary" v-if="court.details.end < today">反馈</div>
                    <div class="btn-group" v-else>
                        <div class="btn btn-primary">拼场</div>
                        <div class="btn btn-danger">退场</div>
                    </div>
                </div>
            </div>
        </div>
    
    </div>
</template>

<script>
import moment from 'moment';

export default {
    props:["court"],
    data(){
        return {
            today:moment().format(),
            reservation_type_str:[null,'先到先得','抽签','长期预定','队列'],
            status_str:[null,'成功预约未付款','已付款','已取消','已转让','未抽签','已抽签','队列中']
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
        }
    },
}
</script>