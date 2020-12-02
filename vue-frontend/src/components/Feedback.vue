<template>
<div class="card shadow mb-3" style="width:20rem;">
    <div class="card-img-top" style="height:200px; ">
        <img :src="feedback.img" class="w-100 h-100" style="object-fit:cover">
    </div>
    <div class="card-body">
        <h6 class="card-subtitle mb-2 text-muted"><font-awesome-icon icon="star" v-for="i in feedback.stars" :key="i"/></h6>
        <p class="card-text">{{ feedback.content }}</p>
        <p class="card-text">{{ chineseTime(feedback.publish_date) }}</p>
        <div v-if="byLoggedInUser">
            <small class="text-left text-primary">
                您的反馈
            </small>
            <div class="text-right">
                <br/>
                <div class="btn btn-info shadow">
                    修改
                </div>
            </div>
        </div>
    </div>
    <div class="card-footer" :class="{'bg-success':feedback.solved,'bg-danger':!feedback.solved}">
        <p class="card-text text-white" v-if="feedback.reply">管理员回复:{{ feedback.reply }}</p>
        <p v-else class="card-text text-white">无回复</p>
    </div>
</div>  
</template>

<script>
export default {
    props:["feedback"],
    methods:{
        chineseTime(time){
            try{
                let [year,month,day] = time.split("T")[0].split("-");
            
            let [hour,min] = time.split("T")[1].split("+")[0].split(":");
            
            return `${year}年${month}月${day}日 ${hour}点 ${min}分`;
            }
            catch(e){
                return "没有时间";
            }
        }
    },
    computed:{
        byLoggedInUser(){
            let result = this.$store.state.logged_in_user_id == this.feedback.user_id;
            return result;
        }
    }
}
</script>
<style scoped>
.card:hover img{
    transform:scale(1.1);
    transition: transform 0.3s;
}

.card-img-top{
    overflow:hidden;
}
</style>