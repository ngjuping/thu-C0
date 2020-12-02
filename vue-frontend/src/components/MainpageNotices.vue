<template>
    <!-- notices -->
        <div class="rounded p-2 p-sm-3 p-lg-5 text-left shadow bg-light">
            <div class="container">
                <div class="row">
                    <div class="col">
                        <h1 id="notice">最新通知</h1>
                    </div>
                    <div class="col text-right pr-0">
                        <span class="btn btn-dark align-middle" @click="$router.push({name:'AllNotices'})">显示所有通告</span>
                    </div>
                </div>
            </div>
            
            <hr>
            <Notice v-for="notice in notices" :key="notice.id" :notice="notice"></Notice>
            
        </div>
</template>

<script>
import Notice from '@/components/Notice.vue'
export default {
    props:['notices'],
    components:{Notice}
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