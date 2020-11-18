<template>
    <div class="jumbotron text-left shadow p-2">
        <h3>{{ sports[info.type] }}场地{{ info.id }}</h3>
        <table class="table">
            <tbody>
                <tr>
                    <td scope="col"  v-for="status in info.status" 
                    :class="[`courtstatus-${status.code}`]" 
                    :key="status.start" 
                    :title="statustext[status.code]"
                    @click="selectCourt(status)"
                    data-toggle="tooltip" 
                    data-placement="top"></td>
                </tr>
            </tbody>
        </table>
        <div class="d-flex justify-content-end" v-if="selectedCourt">
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
.courtstatus-0{
    background-color:greenyellow;
    opacity:0.5;
}

.courtstatus-1{
    background-color:red;
    opacity:0.5;
}

td:hover{
    cursor:pointer;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}
</style>