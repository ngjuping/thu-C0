<template>
    <!-- notices -->
        <div class="rounded p-2 p-sm-3 p-lg-5 text-left shadow bg-light">
            <h1 id="notice">最新通知</h1>
            <hr>
            <div v-for="notice in notices" :key="notice.id" class="list-group-item shadow text-left mb-1">
                <div class="w-75 d-inline-block ">
                <h4><span class="bg-white title">{{ notice.title }}&nbsp;&nbsp;<span class="badge badge-pill badge-dark">New</span></span></h4>
                <p class="lead content"><span class="bg-white">{{ notice.content }}</span></p>
                </div>
                <div class="d-inline-block w-25 h-100 display-4 text-right">
                    <div class="d-inline-block w-100">
                    <font-awesome-icon icon="arrow-circle-right" class="rightarrow"/>
                    </div>
                </div>
            </div>
            
        </div>
</template>

<script>
export default {
    props:['notices'],
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