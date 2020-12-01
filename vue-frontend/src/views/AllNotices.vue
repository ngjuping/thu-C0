<template>
    <!-- notices -->
        <div class="rounded p-2 p-sm-3 p-lg-5 text-left shadow bg-light">
            <div class="container-fluid pl-0">
                <div class="row">
                    <div class="col">
                        <h1 id="notice">最新通知
                            <span class="spinner-border" v-if="loading">
                                <span class="sr-only">Loading...</span>
                            </span>
                        </h1>
                    </div>
                    <div class="col text-right pr-0">
                        <span class="btn btn-danger" @click="$router.go(-1)">
                            回到主页
                        </span>
                    </div>
                </div>
            </div>
            
            <div class="alert alert-danger" v-if="failToLoad">
                {{ err_msg }}
            </div>
            <ul class="pagination">
                <li class="page-item"><a class="page-link" @click="back" v-if="current_page !== 1">前一页</a></li>
                <li class="page-item"><a class="page-link">{{ current_page }}</a></li>
                <li class="page-item"><a class="page-link" @click="updateNotices(current_page+1)" v-if="current_page<total/5">{{ current_page+1 }}</a></li>
                <li class="page-item"><a class="page-link" @click="updateNotices(current_page+2)" v-if="current_page+1<total/5">{{ current_page+2 }}</a></li>
                <li class="page-item"><a class="page-link" @click="next" v-if="current_page<total/5">下一页</a></li>
            </ul>
            <hr>
            <div v-for="notice in all_notices" :key="notice.id" class="list-group-item shadow text-left mb-1">
                <div class="w-75 d-inline-block ">
                <h4><span class="bg-white title">{{ notice.title }}&nbsp;&nbsp;<span class="badge badge-pill badge-dark">New</span></span></h4>
                <p class="lead content"><span class="bg-white">{{ notice.content }}</span></p>
                </div>
                <div class="d-inline-block w-25 h-100 display-4 text-right">
                    <div class="d-inline-block w-100">
                    <font-awesome-icon icon="arrow-circle-right" class="rightarrow"/>
                    </div>
                </div>
            </div>
            
        </div>
</template>

<script>
export default {
    props:['notices'],
    data(){
        return {
            failToLoad:false,
            loading:true,
            all_notices:[],
            total:0,
            current_page:1,
            err_msg:"出现错误"
        }
    },
    methods:{
        updateNotices(page=this.current_page){
            this.current_page = page;
            this.getNotices();
        },
        back(){
            this.current_page--;
            this.updateNotices();
        },
        next(){
            this.current_page++;
            this.updateNotices();
        },
        getNotices(){
            this.failToLoad = false;
            this.loading = true;
            this.$axios
            .get(`/api/notices?page=${this.current_page}&size=5`)
            .then(res => 
            {
                this.all_notices = res.data.notices;
                this.total = res.data.total;
            })
            .catch((err)=>{
                this.failToLoad = true;
                this.err_msg = err.response.data.message;
            })
            .finally(()=>{this.loading = false;})
        }
    },
    mounted(){
        this.getNotices();
    }
}
</script>

<style scoped>
@media(max-width:600px){
    #notice{
        font-size:30px;
    }
    .title{
        font-size:20px;
    }
    .content{
        font-size:15px;
    }
    .rightarrow{
        font-size:40px;
    }
}
</style>