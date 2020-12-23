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
                </div>
            </div>
            
            <div class="alert alert-danger" v-if="failToLoad">
                {{ err_msg }}
            </div>
            <ul class="pagination">
                <li class="page-item" @click="$router.go(-1)"><a class="page-link bg-danger text-light">回到主页</a></li>
                <li class="page-item" @click="back" v-if="current_page !== 1"><a class="page-link">前一页</a></li>
                <li class="page-item" disabled><a class="page-link">{{ current_page }}</a></li>
                <li class="page-item" @click="updateNotices(current_page+1)" v-if="current_page<total/5"><a class="page-link" >{{ current_page+1 }}</a></li>
                <li class="page-item" @click="updateNotices(current_page+2)" v-if="current_page+1<total/5"><a class="page-link">{{ current_page+2 }}</a></li>
                <li class="page-item" @click="next" v-if="current_page<total/5"><a class="page-link">下一页</a></li>
            </ul>
            <hr>
            <Notice v-for="notice in all_notices" :key="notice.id" :notice="notice"></Notice>
            
        </div>
</template>

<script>
import Notice from "@/components/Notice.vue"
export default {
    components:{Notice},
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