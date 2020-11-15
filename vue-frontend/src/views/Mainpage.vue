<template>
    <div class="container">
        <Notices :notices="notices"></Notices>
        <br/>
        <br/>
        <VenueDescribe :latestreview="latestreview" :venues="venues" :currentvenue="currentvenue"></VenueDescribe>
    </div>
</template>

<script>
//import moment from 'moment'
import Notices from '@/components/Notices.vue'
import VenueDescribe from '@/components/VenueDescribe.vue'
import Swal from 'sweetalert2'

export default {
    components:{
        Notices,
        VenueDescribe
    },
    data(){
        return{
            notices:[],
            venues:[],
            currentvenue:{},
            latestreview:{stars:4,content:"场地不错，服务还行，稍微贵了些"}
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

