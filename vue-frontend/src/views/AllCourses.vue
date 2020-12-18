<template>
    <div class="rounded p-2 p-sm-3 p-lg-5 text-left shadow bg-light">
            <div class="container-fluid pl-0">
                <div class="row">
                    <div class="col">
                        <h1 id="notice">所有培训课程
                            <span class="spinner-border" v-if="loading">
                                <span class="sr-only">Loading...</span>
                            </span>
                        </h1>
                    </div>
                </div>
            </div>
            
            <div class="alert alert-danger" v-if="failToLoad">
                {{ err_msg }}
            </div>
            <ul class="pagination">
                <li class="page-item" @click="$router.go(-1)"><a class="page-link bg-danger text-light">回到前一页</a></li>
                <li class="page-item" @click="back" v-if="current_page !== 1"><a class="page-link">前一页</a></li>
                <li class="page-item" disabled><a class="page-link">{{ current_page }}</a></li>
                <li class="page-item" @click="getCourses(current_page+1)" v-if="current_page<total/5"><a class="page-link" >{{ current_page+1 }}</a></li>
                <li class="page-item" @click="getCourses(current_page+2)" v-if="current_page+1<total/5"><a class="page-link">{{ current_page+2 }}</a></li>
                <li class="page-item" @click="next" v-if="current_page<total/5"><a class="page-link">下一页</a></li>
            </ul>
            <hr>
            <div class="d-flex justify-content-around w-100 flex-wrap">
                <Course v-for="(course,index) in all_courses" :key="index" :course="course"></Course>
            </div>
            
        </div>
</template>

<script>
import Course from '@/components/Course.vue'

export default {
    data(){
        return {
            all_courses:[],
            total:0,
            current_page:1,
            err_msg: "",
            failToLoad: false,
            loading: false,
        }
    },
    components:{Course},
    methods:{
        getCourses(){
            this.$axios
            .get(`/api/courses?page=${this.current_page}&size=5`)
            .then(res => 
            {
                this.all_courses = res.data.courses
                console.log(this.all_courses);
                this.total = res.data.total
            })
            .catch((err)=>{
                this.failToLoad = true;
                this.err_msg = err.response.data.message;
            })
            .finally(()=>{this.loading = false;})
        },
        back(){
            this.current_page--;
            this.getCourses();
        },
        next(){
            this.current_page++;
            this.getCourses();
        },
    },
    mounted(){
        this.getCourses();
    }
}
</script>