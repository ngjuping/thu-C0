<template>
    <div class="w-100 h-100 bg-white">
    <div class="bg d-flex justify-content-start">
        <div class="card w-50-md mt-4">
            <div class="card-body">
                <ul class="list-group">
                    <li class="list-group-item list-group-item-action" @click="$router.push({name:'Mainpage'})"><h3>主页</h3></li>
                    <li class="list-group-item" >
                        
                    <h3>预定场地</h3>
                    <ul class="list-group">
                        <li class="list-group-item list-group-item-action bg-dark text-white" 
                        v-for="(venue,index) in venues" 
                        :key="venue.id" 
                        @click="$router.push({name:'Booking',params:{venueid:index+1}})"> <b>{{venue.name}}</b></li>
                    </ul>
                    </li>
                    <li class="list-group-item list-group-item-action" @click="$router.push({name:'Manage'})"><h3>管理场地</h3></li>
                </ul>
            </div>
            <div class="card-footer">
                ceshi1
            </div>
        </div>
    </div>
    
    </div>
</template>
<script>
export default {
    data(){
        return {
            failedToGetVenues:false,
            venues:[]
        }
    },
    mounted(){
        //get venues list
        this.$axios
        .get('/api/main/venues/list')
        .then(res => {
            this.venues = res.data.venues;
        })
        .catch(() => {
            this.failedToGetVenues = true;
        })
    },
}
</script>
<style scoped>
    .card{
        background:transparent;
        border-width: 0px;
    }
    .bg{
        height:100vh;
        background-image:url('../assets/notfound.png');
        background-repeat:no-repeat;
        background-size: cover;
        background-position-x: 50%;
    }
</style>