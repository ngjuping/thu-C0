<template>
    <div class="list-group-item text-left mb-1 share rounded"  data-backdrop="false" >
        <div class="container-fluid">
            <div class="row">
                <div class="col-12 pt-3">
                    <div class="row">
                        <div class="col"  data-toggle="modal" :data-target="`#modal-${share.share_id}`">
                            <h4><span class="title">{{ share.content.slice(0,20) }}&nbsp;&nbsp;<span class="badge badge-pill badge-dark">New</span></span></h4>
                            <p class="lead content"><span class="text-secondary">场地：{{ share.reservation.details.name }}</span></p>
                        </div>
                        <div class="col-1 text-right" v-if="$store.state.logged_in_user_id === share.user_id">
                            <div class="btn btn-info">修改帖子</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        
        <div class="modal fade" :id="`modal-${share.share_id}`">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content shadow-lg">
                    <div class="modal-header">
                        <h4 class="modal-title">{{ share.reservation.details.name }}</h4>
                        <button type="button" class="close" data-dismiss="modal">
                        <span>&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <small>他很有诚意的说：</small>
                        <div class="jumbotron">
                            {{ share.content }}
                        </div>
                        <div class="text-left card mb-4">
                            <div class="card-header">
                                邀请人订单
                            </div>
                            <div class="card-body">
                                <h5 class="card-title">{{ getSportsStr(share.reservation.type) }}</h5>
                                <p class="card-text">{{ getReservationStr(share.reservation.status) }}</p>
                                <hr>
                                <p>{{ chineseTime(share.reservation.details.start) }} 到 {{ chineseTime(share.reservation.details.end) }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer bg-secondary text-light">
                        <small> 发布时间: {{ chineseTime(share.publish_date) }} </small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props:["share"],
    methods:{
        chineseTime(time){
            try{
                let [year,month,day] = time.split("T")[0].split("-");
            
                let [hour,min] = time.split("T")[1].split("+")[0].split(":");
                
                return `${year}年${month}月${day}日 ${hour}点 ${min}分`;
            }
            catch(e){
                return "没有发布时间";
            }
        },
        getSportsStr(index){
            return this.$store.state.sportsType[index];
        },
        getReservationStr(index){
            return this.$store.state.reservationStatus[index];
        }
    },
}
</script>
<style scoped>
.share:hover{
    background-color:lightgrey;
}

@media(max-width:600px){
    .badge{
        font-size:13px;
    }
}
</style>