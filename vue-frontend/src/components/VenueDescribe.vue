<template>

<div class="row p-3 shadow rounded" id="venue_panel">
    <div class="col-12 col-lg-4 pt-4 shadow p-4" id="venue_select_panel">
        <h1 class="text-left">选择场馆 &nbsp;&nbsp;<font-awesome-icon icon="basketball-ball" class="text-danger" /></h1>
        <div v-if="loadingVenue" class="text-info">
            <span>正在加载场地信息...</span>
        </div>
        <hr>
        <div class="list-group overflow-auto pb-2" style="max-height:400px;">
            <div class="list-group-item list-group-item-action container" v-for="venue in venues" :key="venue.id">
                <div class="row">
                    <div class="col-8 d-flex align-items-center"  @click="getVenueInfo(venue.id)"><a>{{ venue.name }}</a></div>
                    <button type="button" class="col btn btn-dark h-100" @click="goBooking(venue.id)">订场</button>
                </div>
            </div>
        </div>
    </div>
    <div class="col-12 col-lg-8">
        <div class="container">
            <div class="row mb-4">
                <div class="col container">
                    <div class="alert alert-danger" v-if="failedToGetVenueInfo">
                        无法获得场地信息...
                    </div>
                    <div class="row">
                        <div class="col-12 col-lg-6 p-4">
                            <h1>{{ currentvenue.name }}</h1>
                        </div>
                        <div class="col-12 col-lg-6 d-flex align-items-center">
                            <div class="btn-group shadow w-100">
                                <div class="btn btn-primary d-flex align-items-center justify-content-center gobookcontainer" @click="goBooking(currentvenue.id)">
                                    <span class="gobook mr-2">
                                    前往订场</span>
                                    <font-awesome-icon icon="arrow-circle-right" id="gobookarrow" />
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row mb-4">
                <div class="col rounded bg-secondary p-0" id="venue_description">
                    <div class="d-flex align-items-center justify-content-start rounded w-100 h-100 text-left">
                        <span class="bg-light d-inline-block w-100 p-3">{{ currentvenue.description }}</span>
                    </div>
                </div>
                <div class="col">
                    <img :src="currentvenue.img" class="img-thumbnail">
                </div>
            </div>
            <div class="row">
                <div class="col-12 col-lg-8 list-group">
                    <Notice v-for="notice in currentvenue.notices" :notice="notice" :key="notice.id" class="list-group-item text-left mb-3"></Notice>
                </div>
                <div class="col-12 col-lg-4  pl-0">
                    
                    <div class="card" v-if="hasReview" >
                        <h5 class="card-header">最新反馈</h5>
                        <div class="card-body overflow-auto" id="feedback_body">
                            <h6 class="card-subtitle mb-2 text-muted"><font-awesome-icon icon="star" v-for="i in currentvenue.review.stars" :key="i"/></h6>
                            <p class="card-text" v-html="currentvenue.review.content"></p>
                        </div>
                        <div class="card-footer">
                            <p v-if="!loadingVenue" class="mb-0">{{ now() }}</p>
                            
                            <div class="alert alert-danger" v-else>
                                没有找到回馈
                            </div>
                        </div>
                    </div>
                    <div class="w-100 text-right d-flex align-item-end justify-content-end py-2">
                        <button class="btn btn-warning" @click="$router.push({name:'AllFeedbacks'})">查看所有反馈</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

</template>

<script>
import moment from 'moment'
import Notice from '@/components/Notice.vue'
export default {
    props:["venues"],
    components:{Notice},
    data(){
        return {
            failedToGetVenueInfo:false,
            currentvenue: {
                id:1,
                name:"默认场馆", 
                description:"默认形容", 
                img:"https://miro.medium.com/max/1140/0*16bH8WYK3fOtu-kJ.jpg", 
                notices:[{ id:1,title:"无通知",content:"默认通知内容" }],
                review:{stars:4,content:"默认评论",publish_date:moment().format()}
            },
            hasReview:true,
            loadingVenue:true
        }
    },
    methods:{
        getVenueInfo(x){

            //set state variables
            this.hasReview = true;
            this.loadingVenue = true;
            
            //get details on specific venue x
            this.$axios
            .get(`/api/main/venues?id=${x}`)
            .then(res => {
                if(!Object.keys(res.data.venue_info.review).length){
                    this.hasReview = false;
                }
                this.currentvenue = res.data.venue_info;
                
                this.currentvenue.notices.forEach(function (notice, i) { notice["id"] = i });
            })
            .catch(() => {
                this.failedToGetVenueInfo = true;
            })
            .finally(() => {this.loadingVenue = false;})
        },
        goBooking(x){
            this.$router.push({name:'Booking',params:{venueid:x}});
        },
        //get relative time of the review publish date
        now(){
            let review_time = this.currentvenue.review.publish_date
            let first_half = review_time.split("T")[0];
            let second_half_time = review_time.split("T")[1].split("+")[0];
            return moment(first_half + " " + second_half_time,"YYYY-MM-DD hh:mm:ss").fromNow();
        }
    },
    mounted(){
        //get details on specific venue 1 (default venue)
        this.getVenueInfo(1);
    }
}
</script>

<style scoped>

#venue_panel{
    border-radius:20px;
    background-image:url("../assets/prototype_bg2.jpg");
    background-size:100%;
    background-position: 0% 100%;
    background-repeat:no-repeat;

}

#venue_select_panel{
    position:relative;
    z-index:0;
}

#venue_select_panel::after{
    content:"";
    position:absolute;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background-image:url("../assets/venue_select_bg.jpg");
    background-size:cover;
    background-repeat:no-repeat;
    opacity:0.8;
    z-index:-1;
    border-radius:50px;
}

#venue_description{
    background-color:rgb(73, 136, 190);
}

#feedback_body{
    max-height:200px;
}

.gobook{
    font-size: 3em;
}

.gobookcontainer:hover #gobookarrow{
    font-size:50px;
}

#gobookarrow{
    font-size:0px;
    transition: font-size 0.4s
}


@media(max-width:600px){
    .gobook{
        font-size: 30px;
    }
    .gobookcontainer:hover #gobookarrow{
        font-size:30px;
    }
    .noticetitle{
        font-size:20px;
    }
    .noticecontent{
        font-size:15px;
    }
    .rightarrow{
        font-size:40px;
    }
}
</style>