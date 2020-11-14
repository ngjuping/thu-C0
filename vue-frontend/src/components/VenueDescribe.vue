<template>

<div class="row p-3 shadow" id="venue_panel">
    <div class="col-12 col-md-4 pt-4 shadow" id="venue_select_panel">
        <h1>选择场馆</h1>
        <hr>
        <div class="list-group">
        <div class="list-group-item list-group-item-action container" v-for="venue in venues" :key="venue.id">
            <div class="row">
                <div class="col-8 d-flex align-items-center"  @click="getVenueInfo(venue.id)"><a>{{ venue.name }}</a></div>
                <button type="button" class="col btn btn-dark h-100">前往订场</button>
            </div>
        </div>
        
        </div>
    </div>
    <div class="col-12 col-md-8">
        <div class="container">
            <div class="row mb-4">
                <div class="col container">
                    <div class="row">
                        <div class="col-12 col-md-6 p-4">
                            <h1>{{ currentvenue.name }}</h1>
                        </div>
                        <div class="col-12 col-md-6 d-flex align-items-center">
                            <div class="btn-group shadow w-100">
                                <button type="button" class="btn btn-light h-100">导航</button>
                                <button type="button" class="btn btn-light h-100">前往订场</button>
                                <button type="button" class="btn btn-dark h-100">长期预约</button>
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
                <div class="col-12 col-md-8 list-group">
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
                <div class="col-12 col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">最新反馈</h5>
                            <h6 class="card-subtitle mb-2 text-muted"><font-awesome-icon icon="star" v-for="i in latestreview.stars" :key="i"/></h6>
                            <p class="card-text">{{ latestreview.content }}</p>
                            <button class="btn btn-primary">查看更多</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

</template>

<script>
export default {
    props:["currentvenue","venues","latestreview"],
    
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
}
</script>