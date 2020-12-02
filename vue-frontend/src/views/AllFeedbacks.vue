<template>
    <div class="rounded p-2 p-sm-3 p-lg-5 text-left shadow bg-light">
            <div class="container-fluid pl-0">
                <div class="row">
                    <div class="col">
                        <h1 id="notice">所有反馈
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
                <li class="page-item" @click="updateFeedbacks(current_page+1)" v-if="current_page<total/5"><a class="page-link" >{{ current_page+1 }}</a></li>
                <li class="page-item" @click="updateFeedbacks(current_page+2)" v-if="current_page+1<total/5"><a class="page-link">{{ current_page+2 }}</a></li>
                <li class="page-item" @click="next" v-if="current_page<total/5"><a class="page-link">下一页</a></li>
                <li class="page-item" @click="toggleGetFeedbacks" v-if="!getmycourts"><a class="page-link">我的反馈</a></li>
                <li class="page-item" @click="toggleGetFeedbacks" v-else><a class="page-link">查看全部</a></li>
            </ul>
            <hr>
            <div class="d-flex justify-content-around w-100 flex-wrap">
                    <Feedback v-for="feedback in all_feedbacks" :key="feedback.feedback_id" :feedback="feedback"></Feedback>
            </div>
            
        </div>
</template>

<script>
import Feedback from '@/components/Feedback.vue'
export default {
    data(){
        return {
            all_feedbacks:[],
            total:0,
            current_page:1,
            loading:false,
            failToLoad:false,
            err_msg:"",
            getmycourts:false
        }
    },
    components: {Feedback},
    methods:{
        getFeedbacks(){
            let url = `/api/manage/feedback?page=${this.current_page}&size=5`;
            if(this.getmycourts){
                url = `/api/manage/feedback/user?user_id=${this.$store.state.logged_in_user_id}&page=${this.current_page}&size=5`
            }
            this.failToLoad = false;
            this.loading = true;
            this.$axios
            .get(url)
            .then(res => 
            {
                this.all_feedbacks = res.data.feedbacks
                this.total = res.data.total
            })
            .catch((err)=>{
                this.failToLoad = true;
                this.err_msg = err.response.data.message;
            })
            .finally(()=>{this.loading = false;})
        },
        toggleGetFeedbacks(){
            //reset current_page
            this.current_page = 1;
            this.getmycourts = !this.getmycourts
            this.getFeedbacks();
        },
        updateFeedbacks(page=this.current_page){
                this.current_page = page;
                this.getFeedbacks();
        },
        back(){
            this.current_page--;
            this.updateFeedbacks();
        },
        next(){
            this.current_page++;
            this.updateFeedbacks();
        },
        
    },
    mounted(){
        this.getFeedbacks();
    }
}
</script>