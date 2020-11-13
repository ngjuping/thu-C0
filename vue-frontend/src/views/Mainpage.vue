<template>
    <div class="container">
        <Notices :notices="notices"></Notices>
        <br/>
        <br/>
        <div class="row p-3 shadow" id="venue_panel">
            <div class="col-4 pt-4 shadow" id="venue_select_panel">
                <h1>选择场馆</h1>
                <hr>
                <div class="list-group">
                <a class="list-group-item list-group-item-action" v-for="venue in venues" :key="venue.id" @click="getVenueInfo(venue.id)">{{ venue.name }}</a>
                </div>
            </div>
            <div class="col-8">
                <div class="container">
                    <div class="row">
                        <div class="col">
                            <h1 id="venue_name">{{ currentvenue.name }}</h1>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col" id="venue_description">
                            <div class="d-flex align-items-center justify-content-start rounded w-100 h-100">
                                <span class="bg-light">{{ currentvenue.description }}</span>
                            </div>
                        </div>
                        <div class="col">
                            <img :src="currentvenue.img" class="img-thumbnail">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col list-group">
                            <div v-for="notice in currentvenue.notice" :key="notice.id" class="list-group-item text-left mb-1">
                                <div class="w-75 d-inline-block ">
                                <h4><span class="bg-white">{{ notice.title }}&nbsp;&nbsp;<span class="badge badge-pill badge-dark">New</span></span></h4>
                                <p class="lead"><span class="bg-white">{{ notice.content }}</span></p>
                                </div>
                                <div class="d-inline-block w-25 h-100 display-4 text-right">
                                    <div class="d-inline-block w-100">
                                    <font-awesome-icon icon="arrow-circle-right" />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col">

                        </div>
                    </div>
                </div>
            </div>
            </div>
    </div>
</template>

<script>
//import moment from 'moment'
import Notices from '@/components/Notices.vue'
import Swal from 'sweetalert2'

export default {
    components:{
        Notices
    },
    data(){
        return{
            notices:[],
            venues:[],
            currentvenue:{}
        }
    },
    methods:{
        getVenueInfo(x){
            if(x == this.currentvenue.id)
            {
                //already has the data no need to axios again
                return;
            }
            else
            {
                //get details on specific venue x
                this.$axios
                .get(`/api/v1/venues/${x}`)
                .then(res => {
                    this.currentvenue = res.data.venue;
                })
            }
        }
    },
    mounted(){
        if(!this.$store.state.logged_in)
        {
            Swal.fire({
            title: "尚未登陆",
            text: "您可以查看场地信息，但不能做任何操作",
            icon: "error",
            timer: 1500});
        }
        //get the first 3 notices
        this.$axios
        .get('/api/v1/main/notice')
        .then(res => {
            this.notices = res.data.notices;
        })
        //get venues list
        this.$axios
        .get('/api/v1/venues/list')
        .then(res => {
            this.venues = res.data.venues;
        })
        //get details on specific venue 1
        this.$axios
        .get('/api/v1/venues/1')
        .then(res => {
            this.currentvenue = res.data.venue;
        })
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

#venue_name{
    border-radius:10px;
    background-color:white;
}


</style>