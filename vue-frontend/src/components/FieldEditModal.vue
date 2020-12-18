<template>
    <div class="field-modal">
        <div class="modal fade" id="editFieldModal" aria-hidden="true" tabindex="-1" role="dialog">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">场地初始化</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form>
                        <div class="form-group row">
                            <label class="col-sm-3 col-form-label">输入场地价格：</label>
                            <div class="col-sm-8">
                                <input type="text" v-model="formMessage.price" class="form-control" placeholder="请输入"/>
                            </div>
                        </div>
                        <div class="form-group row">
                            <div style="margin: 10px auto">请设置场地状态，其中0 表示未开放，1 表示可供先到先得，3 表示可供预定抽签</div>
                            <table class="table">
                                <thead>
                                    <tr>
                                    <th scope="col" style="width: 120px">时间</th>
                                    <th scope="col">周一</th>
                                    <th scope="col">周二</th>
                                    <th scope="col">周三</th>
                                    <th scope="col">周四</th>
                                    <th scope="col">周五</th>
                                    <th scope="col">周六</th>
                                    <th scope="col">周日</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(item, index) in formMessage.matrix" :key="index">
                                        <th scope="row">
                                            <span>{{index+7}}:00-{{index+8}}:00</span>
                                        </th>
                                        <th scope="row">
                                            <input type="text" v-model="item[0]" class="form-control" />
                                        </th>
                                        <th scope="row">
                                            <input type="text" v-model="item[1]" class="form-control" />
                                        </th>
                                        <th scope="row">
                                            <input type="text" v-model="item[2]" class="form-control" />
                                        </th>
                                        <th scope="row">
                                            <input type="text" v-model="item[3]" class="form-control" />
                                        </th>
                                        <th scope="row">
                                            <input type="text" v-model="item[4]" class="form-control" />
                                        </th>
                                        <th scope="row">
                                            <input type="text" v-model="item[5]" class="form-control" />
                                        </th>
                                        <th scope="row">
                                            <input type="text" v-model="item[6]" class="form-control" />
                                        </th>
                                    </tr>
                                    <tr>
                                        <th scope="row">
                                            <span>快速设定</span>
                                        </th>
                                        <th scope="row" v-for="col_no in 7" :key="'col'+col_no">
                                            <select @change="initCol($event,col_no)">
                                                <option value="0">未开放</option>
                                                <option value="1">先到先得</option>
                                                <option value="3">抽签</option>
                                            </select>
                                        </th>
                                    </tr>
                                </tbody>
                            </table>
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
    name: 'FieldModal',
    props: {
        fieldDetail: {
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
                court_id: '',
                matrix: [
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]
                ],
                price: '',
            },
        }
    },
    methods: {
        initCol(e,col_no){
            console.log("New value:" + e.target.value);
            console.log("Column no:" + col_no)

            //每周场地状态矩阵
            let time_matrix = this.formMessage.matrix;

            //为一整列每一行赋值
            for(let rows in time_matrix){
                console.log(parseInt(e.target.value));
                time_matrix[rows][parseInt(col_no)-1] = parseInt(e.target.value);
            }

            console.log(this.formMessage.matrix)
        },
        handleSave() {
            if (this.status == 'add') {
                // 新增
                this.$axios.post('/api/admin/schedule', this.formMessage).then((res) => {
                    console.log(res, 'res')
                    this.$emit('edit-success');
                }).catch(err => {
                    console.log(err);
                })
            }
        },
    },
    // watch: {
    //     fieldDetail(val) {
    //         console.log(val, 'fieldDetail-watch');
    //         this.formMessage = {
    //             court_id: val.id,
    //             matrix: val.matrix,
    //             price: val.price
    //         }
    //     }
    // },
}
</script>

<style scoped>
    
</style>