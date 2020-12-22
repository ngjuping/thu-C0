<template>
<div class="jumbotron text-left shadow p-3">
  <div class="row top">
    <span id="title">{{ $store.state.sportsType[info.type] }}场地{{ info.id }}</span>
    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#editCourtModal" @click="showModal">编辑场地</button>
  </div>
  <div class="container">
    <div class="row">
      <div class="col-12 col-md-12">
        <div class="row d-flex justify-content-around" id="ranges">
            <div class="col-12 col-md ranges d-flex justify-content-center align-items-center"  v-for="status in info.status" 
            :class="[`courtstatus-${status.code} border border-success rounded`]"
            :key="`range${status.start}`"
            :title="$store.state.courtStatus[status.code]"
            data-toggle="tooltip" 
            data-placement="top">
            <span class="d-inline d-md-none bg-light lead">{{ getTimeOnly(status.start) }} -- {{ getTimeOnly(status.end) }}</span>
            </div>
        </div>
      </div>
      <div class="col-6 col-md-12 d-none d-md-block">
        <div class="row d-flex justify-content-end">
          <div class="col px-0" v-for="(status) in info.status" :key="`label${status.start}`">
            <div class="pl-0">
                {{ getTimeOnly(status.start) }}
            </div>      
          </div>
          <div class="pr-0" v-if="info.status.length">
            {{ getTimeOnly(info.status[info.status.length-1].end) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>
<script>
import $ from 'jquery'
export default {
    props:["info"],
    data(){
        return {
            selectedCourt:null,
            courtInfo: {},
            show: false
        }
    },
    mounted(){
      $('[data-toggle="tooltip"]').tooltip();
    },
    methods:{
      showModal() {
        this.show = true
        this.$emit('edit', this.info)
      },
      getTimeOnly(date){
            if(!date) return "解析日期错误"
            try{
                //input: "1999-03-01T00:00:00+01:00"
                let date_second_part = date.split("T")[1]; //["1999-03-01","00:00:00+01:00"][1] = "00:00:00+01:00"
                let [hour,minutes] = date_second_part.split(":").slice(0,2); 
                return hour+minutes;
            }
            catch(err){
                return "解析日期错误"
            }
        },
      handleSuccessEdit() {
        this.$emit('court-change')
      }
    }

}
</script>

<style scoped>
#title{
    font-size:30px;
    margin-right: 30px;
}

.top {
  margin-bottom: 20px;
}

.courtstatus-1{
    background-color:greenyellow;
    opacity:0.5;
}

.courtstatus-2{
    background-color:red;
    opacity:0.5;
}

.courtstatus-3{
    background-color:orange;
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