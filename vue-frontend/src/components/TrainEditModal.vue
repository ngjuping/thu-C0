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
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">取消</button>
                    <button type="button" class="btn btn-primary" data-dismiss="modal" @click="handleSave">保存</button>
                </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// import $ from 'jquery'
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
        }
    },
    methods: {
        handleSave() {
            if (this.status == 'add') {
                // 新增
                this.$axios.post('/api/admin/create/course', this.formMessage).then((res) => {
                    console.log(res, 'res')
                    this.$emit('edit-success');
                }).catch(err => {
                    console.log(err);
                })
            } else if (this.status == 'edit') {
                // 编辑
                this.$axios.post('/api/admin/update/course', this.formMessage).then((res) => {
                    console.log(res, 'res')
                    this.$emit('edit-success');
                }).catch(err => {
                    console.log(err);
                })
            } else if (this.status == 'delete') {
                // 删除
                this.$axios.post('/api/admin/delete/course', this.formMessage).then((res) => {
                    console.log(res, 'res')
                    this.$emit('edit-success');
                }).catch(err => {
                    console.log(err);
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