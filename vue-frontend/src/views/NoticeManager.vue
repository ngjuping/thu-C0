<template>
    <div class="notice-manager">
        <button
            type="button"
            class="btn btn-primary"
            data-toggle="modal" 
            data-target="#editNoticeModal"
            style="float: left; margin-bottom: 5px"
            @click="handleShowEditModal(item, 'add')"
        >新增</button>
        <table class="table">
            <thead class="thead-dark">
                <tr>
                <th scope="col" width="25%">序号</th>
                <th scope="col" width="25%">标题</th>
                <th scope="col" width="25%">内容</th>
                <th scope="col" width="25%">操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item,index) in noticeList" :key="index">
                <th scope="row">{{index + 1}}</th>
                <td data-class="xd-table-th">
                    <!-- <a
                        href="javascript:void(0)" 
                        class="card-link textOverflow"
                        data-toggle="modal" 
                        data-target="#venueDetailModal" 
                        @click="handleShowDetailModal(item)"
                    >{{item.title}}</a> -->
                    <span class="textOverflow">{{item.title}}</span>
                </td>
                <td data-class="xd-table-th">
                    <!-- <a
                        href="javascript:void(0)" 
                        class="card-link textOverflow" 
                        data-toggle="modal" 
                        data-target="#venueDetailModal"
                        @click="handleShowDetailModal(item)"
                    >{{item.content}}</a> -->
                    <span class="textOverflow">{{item.content}}</span>
                </td>
                <td>
                    <button 
                        type="button" 
                        class="btn btn-primary btn-sm" 
                        data-toggle="modal" 
                        data-target="#editNoticeModal" 
                        style="margin-right: 5px"
                        @click="handleShowEditModal(item, 'edit')"
                    >
                    编辑
                    </button>
                    <button 
                        type="button" 
                        class="btn btn-danger btn-sm" 
                        data-toggle="modal" 
                        data-target="#delNoticeModal" 
                        @click="handleShowEditModal(item, 'delete')"
                    >
                    删除
                    </button>
                </td>
                </tr>
            </tbody>
        </table>
        <ul class="pagination">
            <li class="page-item"><a class="page-link" href="javascript:void(0)" @click="goPage(0)">上一页</a></li>
            <li class="page-item"><a class="page-link" href="javascript:void(0)" @click="goPage(1)">下一页</a></li>
        </ul>

        <notice-edit-modal
            :notice-detail="noticeDetail"
            :status="status"
            @edit-success="getNotice"
        />
        <notice-del-modal
            :notice-detail="noticeDetail"
            :status="status"
            @edit-success="getNotice"
        />
    </div>
</template>

<script>
// import moment from 'moment'
import NoticeDelModal from '../components/NoticeDelModal'
import NoticeEditModal from '../components/NoticeEditModal'
export default {
    name: 'NoticeManager',
    components: { NoticeEditModal, NoticeDelModal },
    data() {
        return {
            noticeList: [],
            form: {
                page: 1,
                size: 5
            },
            total: 0,
            noticeDetail: {},
            noticeId: '',
            status: 'add'
        }
    },
    mounted() {
        this.getNotice();
    },
    methods: {
        handleShowEditModal(item, status) {
            this.status = status;
            this.noticeDetail = item;
        },
        getNotice() {
            this.$axios.request({
                method: 'get',
                url: `/api/notices?page=${this.form.page}&size=${this.form.size}`
            }).then(res => {
                console.log(res.data)
                this.noticeList = res.data.notices;
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
                    this.getNotice();
                }
            } else {
                // 下一页
                if ((this.form.page+1) * this.form.size - this.total < this.form.size) {
                    this.form.page++;
                    this.getNotice();
                }
            }
        },
    }
}
</script>

<style scoped>
.notice-manager {
  padding: 20px;
}
.textOverflow {
    display: inline-block;
    overflow: hidden;
    text-overflow:ellipsis;
    white-space: nowrap;
}
table{
    text-align:center;
    table-layout:fixed;
    word-break:break-all;
}

table td>span{
    display: inline-block;
    width: 100%;
    overflow: hidden;
    white-space: nowrap;
    text-overflow:ellipsis;
}
</style>