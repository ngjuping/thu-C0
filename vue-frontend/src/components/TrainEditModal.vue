<template>
    <div class="train-modal">
        <div class="modal fade" id="editTrainModal" aria-hidden="true" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">更新课程</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form>
                    <div class="form-group row">
                        <label class="col-sm-2 col-form-label">课程名称</label>
                        <div class="col-sm-10">
                        <input type="text" v-model="formMessage.name" class="form-control" placeholder="请输入"/>
                        </div>
                    </div>
                    <div class="form-group row">
                        <label class="col-sm-2 col-form-label">课程介绍</label>
                        <div class="col-sm-10">
                        <input type="text" v-model="formMessage.intro" class="form-control" placeholder="请输入"/>
                        </div>
                    </div>
                    <div class="form-group row">
                        <label class="col-sm-2 col-form-label">联系方式</label>
                        <div class="col-sm-10">
                        <input type="text" v-model="formMessage.tel" class="form-control" placeholder="请输入"/>
                        </div>
                    </div>
                    <div class="form-group row">
                        <label class="col-sm-2 col-form-label">价格</label>
                        <div class="col-sm-10">
                        <input type="text" v-model="formMessage.price" class="form-control" placeholder="请输入"/>
                        </div>
                    </div>
                    <div class="alert alert-danger" v-if="err_msg">
                        {{ err_msg }}
                    </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal" id="closeTrainEditModal">取消</button>
                    <button type="button" class="btn btn-primary" @click="handleSave">保存</button>
                </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import $ from 'jquery'
export default {
    name: 'TrainModal',
    props: {
        trainDetail: {
            type: Object,
            default() {
                return {}
            }
        },
        status: {
            type: String,
            default() {
                return {}
            }
        }
    },
    data() {
        return {
            formMessage: {
                course_id: '',
                intro:'',
                tel:'',
                name: '',
                price: '',
            },
            err_msg:null
        }
    },
    methods: {
        handleSave() {
            let course_name = this.formMessage.name;
            let course_intro = this.formMessage.intro;
            let course_tel = this.formMessage.tel;
            let course_price = this.formMessage.price;

            // 培训课程名称长度判断
            if(!course_name || course_name.length < 3){
                this.err_msg = "课程名称过短(不能少于3个字)";
                return;
            }
            else if(course_name.length > 10){
                this.err_msg = "课程名称过长(不能多于10个字)";
                return;
            }

            // 培训课程介绍长度判断
            if(!course_intro || course_intro.length < 3){
                this.err_msg = "课程介绍过短(不能少于3个字)";
                return;
            }
            else if(course_intro.length > 100){
                this.err_msg = "课程介绍过长(不能多于100个字)";
                return;
            }

            // 培训课程联系方式长度判断
            if(!course_tel || course_tel.length < 3){
                this.err_msg = "联系方式过短(不能少于3个字)";
                return;
            }
            else if(course_tel.length > 20){
                this.err_msg = "联系方式过长(不能多于20个字)";
                return;
            }

            // 培训课程价格
            if(!course_price || course_price.length === 0){
                this.err_msg = "请输入价格！";
                return;
            }

            // 下面的代码可以重构，近期(12月25日左右)先不要碰

            if (this.status == 'add') {
                // 新增
                this.$axios.post('/api/admin/create/course', this.formMessage)
                .then((res) => {
                    console.log(res, 'res')
                    this.$emit('edit-success');
                    this.err_msg = null;
                    $('#closeTrainEditModal').click();
                })
                .catch(err => {
                    console.log(err);
                    this.err_msg = err.response.data.message;
                })
            } 
            else if (this.status == 'edit') {
                // 编辑
                this.$axios.post('/api/admin/update/course', this.formMessage)
                .then((res) => {
                    console.log(res, 'res')
                    this.err_msg = null;
                    this.$emit('edit-success');
                    $('#closeTrainEditModal').click();
                })
                .catch(err => {
                    console.log(err);
                    this.err_msg = err.response.data.message;
                })
            } 
            else if (this.status == 'delete') {
                // 删除
                this.$axios.post('/api/admin/delete/course', this.formMessage)
                .then((res) => {
                    console.log(res, 'res')
                    this.err_msg = null;
                    this.$emit('edit-success');
                    $('#closeTrainEditModal').click();
                })
                .catch(err => {
                    console.log(err);
                    this.err_msg = err.response.data.message;
                })
            }
        },
    },
    watch: {
        trainDetail(val) {
            console.log(val, 'trainDetail-watch');
            this.formMessage = {
                course_id: val.id,
                name: val.name,
                intro:val.intro,
                tel:val.tel,
                price: val.price
            }
        }
    },
}
</script>

<style scoped>
    
</style>