<template>
    <div class="container">
        <Notices :notices="notices"></Notices>
        <div class="row p-3 shadow-lg" id="venue_panel">
            <div class="col-4">
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
                        <div class="col d-flex align-items-center justify-content-start" id="venue_description">
                            {{ currentvenue.description }}
                        </div>
                        <div class="col">
                            <img :src="currentvenue.img" class="img-thumbnail">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">

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
//     computed:{
//     // Test moment js if it works
//     now(){
//       let first_half = this.$store.state.logged_in_time.split("T")[0];
//       let second_half_time = this.$store.state.logged_in_time.split("T")[1].split("+")[0];
      
//       return moment(first_half + " " + second_half_time,"YYYY-MM-DD hh:mm:ss").fromNow();
//     }
//   }


}
</script>

<style scoped>


#venue_panel{
    border-radius:20px;
    background-image:url("../assets/prototype_bg2.jpg");
    background-size:100%;
    background-repeat:no-repeat;

}

#venue_name{
    border-radius:10px;
    background-color:white;
}

#venue_description{
    border-radius:10px;
    background-color:grey;
}

</style>