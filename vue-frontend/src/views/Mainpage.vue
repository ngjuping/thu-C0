<template>
    <div class="container">
        <div class="alert alert-danger" v-if="failedToGetNotices">
            无法获得通告
        </div>
        <MainpageNotices :notices="notices"></MainpageNotices>
        <br/>
        <br/>
        <div class="alert alert-danger" v-if="failedToGetVenues">
            无法获得场地列表
        </div>
        <VenueDescribe :venues="venues" ></VenueDescribe>
    </div>
</template>

<script>
import MainpageNotices from '@/components/MainpageNotices.vue'
import VenueDescribe from '@/components/VenueDescribe.vue'
import Swal from 'sweetalert2'

export default {
    components:{
        MainpageNotices,
        VenueDescribe
    },
    data(){
        return{
            failedToGetNotices:false,
            failedToGetVenues:false,
            notices:[],
            venues:[],
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
        .get('/api/main/notices')
        .then(res => {
            this.notices = res.data.notices;
        })
        .catch(() => {
            this.failedToGetNotices = true;
        })

        //get venues list
        this.$axios
        .get('/api/main/venues/list')
        .then(res => {
            this.venues = res.data.venues;
        })
        .catch(() => {
            this.failedToGetVenues = true;
        })
        
    }

}
</script>

