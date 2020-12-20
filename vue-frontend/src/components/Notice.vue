<template>
    <div class="list-group-item text-left mb-1 notice rounded p-0" data-toggle="modal" :data-target="`#modal-${notice.id}`" data-backdrop="false">
        <div class="container-fluid">
            <div class="row">
                <div class="col-12 col-md-10 pt-3">
                    <h4><span class="title">{{ notice.title.slice(0,20) }}&nbsp;&nbsp;<span class="badge badge-pill badge-dark">New</span></span></h4>
                    <p class="lead content"><span class="text-secondary">{{ notice.content.slice(0,50) }}</span></p>
                </div>
                <div class="col-12 col-md-2">
                    <div class="d-inline-block w-100 h-100 d-flex align-items-center justify-content-end">
                    <font-awesome-icon icon="arrow-circle-right" class="rightarrow w-75 h-75" style="max-width:50px;" />
                    </div>
                </div>
            </div>
        </div>
        
        
        <div class="modal fade" :id="`modal-${notice.id}`">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content shadow-lg">
                    <div class="modal-header">
                        <h4 class="modal-title">{{ notice.title }}</h4>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        {{ notice.content }}
                    </div>
                    <div class="modal-footer bg-secondary text-light">
                        <small> 发布时间: {{ chineseTime(notice.time) }} </small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props:["notice"],
    methods:{
        chineseTime(time){
            try{
                let [year,month,day] = time.split("T")[0].split("-");
            
            let [hour,min] = time.split("T")[1].split("+")[0].split(":");
            
            return `${year}年${month}月${day}日 ${hour}点 ${min}分`;
            }
            catch(e){
                return "没有发布时间";
            }
        }
    },
}
</script>
<style scoped>
.notice:hover{
    background-color:lightgrey;
}

@media(max-width:600px){
    .badge{
        font-size:13px;
    }
}
</style>