<template>
    <div class="train-manager">
        <button
            type="button"
            class="btn btn-primary"
            data-toggle="modal" 
            data-target="#editTrainModal"
            style="float: left; margin-bottom: 5px"
            @click="handleShowEditModal(item, 'add')"
        >新增</button>
        <table class="table">
            <thead class="thead-dark">
                <tr>
                <th scope="col">序号</th>
                <th scope="col">课程名称</th>
                <th scope="col">价格</th>
                <th scope="col">操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in trainList" :key="index">
                    <th scope="row">{{item.id}}</th>
                    <td>
                        <a
                            href="javascript:void(0)" 
                            class="card-link" 
                            data-toggle="modal" 
                            data-target="#trainDetailModal" 
                        >{{item.name}}</a>
                    </td>
                    <td>{{item.price}}</td>
                    <td>
                        <button 
                            type="button" 
                            class="btn btn-primary btn-sm" 
                            data-toggle="modal" 
                            data-target="#editTrainModal"
                            style="margin-right: 5px"
                            @click="handleShowEditModal(item, 'edit')"
                        >编辑</button>
                        <button 
                            type="button" 
                            class="btn btn-danger btn-sm" 
                            data-toggle="modal" 
                            data-target="#delTrainModal"
                            style="margin-right: 5px"
                            @click="handleShowEditModal(item, 'delete')"
                        >删除</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <ul class="pagination">
            <li class="page-item"><a class="page-link" href="javascript:void(0)" @click="goPage(0)">上一页</a></li>
            <li class="page-item"><a class="page-link" href="javascript:void(0)" @click="goPage(1)">下一页</a></li>
        </ul>

        <train-edit-modal
            :train-detail="trainDetail"
            :status="status"
            @edit-success="getTrain"
        />
        <train-del-modal
            :train-detail="trainDetail"
            :status="status"
            @edit-success="getTrain"
        />
    </div>
</template>

<script>
// import moment from 'moment'
import TrainEditModal from '../components/TrainEditModal'
import TrainDelModal from '../components/TrainDelModal'
export default {
    name: 'ReplyFeedback',
    components: { TrainEditModal, TrainDelModal },
    data() {
        return {
            trainList: [],
            form: {
                page: 1,
                size: 5
            },
            total: 0,
            trainDetail: {},
            trainId: '',
            status: 'add'
        }
    },
    mounted() {
        this.getTrain();
    },
    methods: {
        handleShowEditModal(item, status) {
            this.status = status;
            this.trainDetail = item;
        },
        getTrain() {
            this.$axios.request({
                method: 'get',
                url: `/api/courses?page=${this.form.page}&size=${this.form.size}`,
            }).then(res => {
                this.trainList = res.data.courses;
                this.total = res.data.total;
            }).catch(err => {
                console.log(err);
            })
        },
        goPage(type) {
            if (type == 0) {
                // 上一页
                if (this.form.page > 1) {
                    this.form.page--;
                    this.getTrain();
                }
            } else {
                // 下一页
                if ((this.form.page+1) * this.form.size - this.total < this.form.size) {
                    this.form.page++;
                    this.getTrain();
                }
            }
        },
    }
}
</script>

<style scoped>
.train-manager {
  padding: 20px;
}
</style>