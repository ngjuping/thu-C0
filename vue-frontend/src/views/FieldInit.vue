<template>
    <div class="field-init">
        <span class="spinner-border spinner-border-md text-info" v-if="loading"></span>
        <BookingManage></BookingManage>
        <table class="table table-striped bg-light table-hover rounded">
            <thead class="thead-dark">
                <tr>
                <th scope="col">ID</th>
                <th scope="col">所属场馆</th>
                <th scope="col">名字</th>
                <th scope="col">球類</th>
                <th scope="col">操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in fieldList" :key="index">
                    <th scope="row">{{item.id}}</th>
                    <td>{{item.venue}}</td>
                    <td>{{item.name}}</td>
                    <td>{{sports[item.type]}}</td>
                    <td>
                        <button
                            type="button"
                            class="btn btn-primary btn-sm"
                            data-toggle="modal" 
                            data-target="#editFieldModal"
                            style="margin-right: 5px"
                            @click="handleShowEditModal(item, 'add')"
                        >初始化</button>
                        <button 
                            type="button" 
                            class="btn btn-danger btn-sm" 
                            data-toggle="modal" 
                            data-target="#delFieldModal"
                            style="margin-right: 5px"
                            @click="handleShowEditModal(item, 'delete')"
                        >删除</button>
                    </td>
                </tr>
            </tbody>
        </table>
        
        <div
            type="button"
            class="btn btn-primary"
            data-toggle="modal" 
            style=" margin-bottom: 5px"
            @click="exportInfo()"
            >导出</div>
        <ul class="pagination">
            <li class="page-item"><a class="page-link" href="javascript:void(0)" @click="goPage(0)">上一页</a></li>
            <li class="page-item"><a class="page-link" href="javascript:void(0)" @click="goPage(1)">下一页</a></li>
        </ul>

        <field-edit-modal
            :field-detail="fieldDetail"
            :status="status"
            @edit-success="getField"
        />
        <field-del-modal
            :field-detail="fieldDetail"
            :status="status"
            @edit-success="getField"
        />
    </div>
</template>

<script>
// import moment from 'moment'
import FieldEditModal from '../components/FieldEditModal'
import FieldDelModal from '../components/FieldDelModal'
import BookingManage from '../views/BookingManage.vue'
export default {
    name: 'FieldInit',
    components: { FieldEditModal, FieldDelModal,BookingManage },
    data() {
        return {
            fieldList: [],
            form: {
                page: 1,
                size: 5
            },
            total: 0,
            sports: [null, "羽球", "篮球", "乒乓"],
            fieldDetail: {},
            status: 'add',
            loading:true
        }
    },
    mounted() {
        this.getField();
    },
    methods: {
        exportInfo(){
            this.loading = true;
            this.$axios.post("/api/admin/csv/generate")
            .then((res) => {
                let data = res.data;
                window.location.href = data.path;
            })
            .catch((e) => {
                console.log(e.response.data.message);
            })
            .finally(()=>{this.loading = false});

        },
        handleShowEditModal(item, status) {
            this.status = status;
            this.fieldDetail = item;
        },
        getField() {
            this.loading = true;
            this.$axios.request({
                method: 'get',
                url: `/api/admin/court/list?page=${this.form.page}&size=${this.form.size}`,
            }).then(res => {
                this.fieldList = res.data.courts;
                this.total = res.data.total;
            }).catch(err => {
                console.log(err);
            })
            .finally(()=>{this.loading = false});
        },
        goPage(type) {
            if (type == 0) {
                // 上一页
                if (this.form.page > 1) {
                    this.form.page--;
                    this.getField();
                }
            } else {
                // 下一页
                if ((this.form.page+1) * this.form.size - this.total < this.form.size) {
                    this.form.page++;
                    this.getField();
                }
            }
        },
    }
}
</script>

<style scoped>
.field-init {
  padding: 20px;
}
</style>