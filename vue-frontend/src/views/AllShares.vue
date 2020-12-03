<template>
    <div class="rounded p-2 p-sm-3 p-lg-5 text-left shadow bg-light">
            <div class="container-fluid pl-0">
                <div class="row">
                    <div class="col">
                        <h1 id="notice">所有拼场
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
                <li class="page-item" @click="$router.go(-1)"><a class="page-link bg-danger text-light">回到前一页</a></li>
                <li class="page-item" @click="back" v-if="current_page !== 1"><a class="page-link">前一页</a></li>
                <li class="page-item" disabled><a class="page-link">{{ current_page }}</a></li>
                <li class="page-item" @click="updateShares(current_page+1)" v-if="current_page<total/5"><a class="page-link" >{{ current_page+1 }}</a></li>
                <li class="page-item" @click="updateShares(current_page+2)" v-if="current_page+1<total/5"><a class="page-link">{{ current_page+2 }}</a></li>
                <li class="page-item" @click="next" v-if="current_page<total/5"><a class="page-link">下一页</a></li>
                <li class="page-item" @click="toggleGetShares" v-if="!getmyshares"><a class="page-link">我的拼场</a></li>
                <li class="page-item" @click="toggleGetShares" v-else><a class="page-link">查看全部</a></li>
            </ul>
            <hr>
            <Share v-for="share in all_shares" :key="share.share_id" :share="share"></Share>
            
            
        </div>
</template>

<script>
import Share from '@/components/Share.vue'
export default {
    data(){
        return {
            all_shares:[],
            total:0,
            current_page:1,
            loading:false,
            failToLoad:false,
            err_msg:"",
            getmyshares:false
        }
    },
    components: {Share},
    methods:{
        getShares(){
            let url = `/api/manage/share?page=${this.current_page}&size=5`;
            if(this.getmyshares){
                url = `/api/manage/share/user?user_id=${this.$store.state.logged_in_user_id}&page=${this.current_page}&size=5`
            }
            this.failToLoad = false;
            this.loading = true;
            this.$axios
            .get(url)
            .then(res => 
            {
                this.all_shares = res.data.shares
                this.total = res.data.total
            })
            .catch((err)=>{
                this.failToLoad = true;
                this.err_msg = err.response.data.message;
            })
            .finally(()=>{this.loading = false;})
        },
        toggleGetShares(){
            //reset current_page
            this.current_page = 1;
            this.getmyshares = !this.getmyshares
            this.getShares();
        },
        updateShares(page=this.current_page){
                this.current_page = page;
                this.getShares();
        },
        back(){
            this.current_page--;
            this.updateShares();
        },
        next(){
            this.current_page++;
            this.updateShares();
        },
        
    },
    mounted(){
        this.getShares();
    }
}
</script>