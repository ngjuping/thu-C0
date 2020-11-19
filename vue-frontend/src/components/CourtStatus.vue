<template>
    <div class="jumbotron text-left shadow p-3">
        <span id="title">{{ sports[info.type] }}场地{{ info.id }}</span>
            <div class="container">
                <div class="row">
                    <div class="col-12 col-md-12">
                        <div class="row d-flex justify-content-around" id="ranges">
                            <div class="col-12 col-md ranges d-flex justify-content-center align-items-center"  v-for="status in info.status" 
                            :class="[`courtstatus-${status.code} border border-success rounded`]"
                            :key="`range${status.start}`"
                            :title="statustext[status.code]"
                            @click="selectCourt(status)"
                            data-toggle="tooltip" 
                            data-placement="top">
                            <span class="d-inline d-md-none bg-light lead">{{ status.start }} -- {{ status.end }}</span>
                            </div>
                        </div>
                        
                    </div>
                    <div class="col-6 col-md-12 d-none d-md-block">
                        <div class="row d-flex justify-content-end">
                            <div class="col px-0" v-for="(status) in info.status" :key="`label${status.start}`">
                                <div class="pl-0">
                                    {{ status.start }}
                                </div>      
                            </div>
                            <div class="pr-0">
                                {{ info.status[info.status.length-1].end }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        <div class="d-flex justify-content-between" v-if="selectedCourt">
            <span>
                您选中了FROM{{ selectedCourt.start }}TO{{ selectedCourt.end }}
            </span>
            <button type="button" class="btn btn-secondary" >
                预定这个场地！
            </button>
        </div>
        
           
    </div>
</template>
<script>
import $ from 'jquery'
export default {
    props:["info"],
    data(){
        return {
            sports:["羽球","篮球","乒乓"],
            statustext:["空场地","已有人预定"],
            selectedCourt:null
        }
    },
    mounted(){
        $('[data-toggle="tooltip"]').tooltip();
    },
    methods:{
        selectCourt(courtinfo){
            this.selectedCourt = courtinfo
        }

    }

}
</script>

<style scoped>
#title{
    font-size:30px;
}

.courtstatus-0{
    background-color:greenyellow;
    opacity:0.5;
}

.courtstatus-1{
    background-color:red;
    opacity:0.5;
}

.interval{
    border:3px solid white;
}

.interval:hover{
    cursor:pointer !important;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}


#lastlabel{
    right:-10px;
    top:0px;
}

.ranges,.label{
    height:50px;
}

@media (max-width:760px) {
    #title{
        font-size:25px;
    }
    
    #ranges{
        max-height:300px;
        overflow-y:scroll;
    }
}
</style>