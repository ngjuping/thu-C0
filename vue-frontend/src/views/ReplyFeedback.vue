<template>
    <div class="reply-feedback">
        <button
            type="button"
            class="btn btn-primary"
            data-toggle="modal" 
            data-target="#editReplyModal"
            style="float: left; margin-bottom: 5px"
            @click="handleShowEditModal(item, 'add')"
        >新增</button>
        <table class="table">
            <thead class="thead-dark">
                <tr>
                <th scope="col">序号</th>
                <th scope="col">内容</th>
                <th scope="col">星级</th>
                <th scope="col">回复</th>
                <th scope="col">操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in replyList" :key="index">
                    <th scope="row">{{index + 1}}</th>
                    <td>
                        <a
                            href="javascript:void(0)" 
                            class="card-link" 
                            data-toggle="modal" 
                            data-target="#replyDetailModal" 
                            @click="handleShowDetailModal(item)"
                        >{{item.content}}</a>
                    </td>
                    <td>{{item.stars}}</td>
                    <td>{{item.reply}}</td>
                    <td>
                        <button 
                            type="button" 
                            class="btn btn-danger btn-sm" 
                            data-toggle="modal" 
                            data-target="#delReplyModal"
                            style="margin-right: 5px"
                            @click="handleShowEditModal(item, 'delete')"
                        >删除</button>
                        <button 
                            type="button" 
                            class="btn btn-info btn-sm"
                            @click="handleShowEditModal(item, 'reply')"
                        >回复</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <ul class="pagination">
            <li class="page-item"><a class="page-link" href="javascript:void(0)" @click="goPage(0)">上一页</a></li>
            <li class="page-item"><a class="page-link" href="javascript:void(0)" @click="goPage(1)">下一页</a></li>
        </ul>

        <reply-edit-modal
            :reply-detail="replyDetail"
            :status="status"
            @edit-success="getFeedBack"
        />
        <reply-del-modal
            :reply-detail="replyDetail"
            :status="status"
            @edit-success="getFeedBack"
        />
        <reply-detail-modal :reply-id="replyId" />
    </div>
</template>

<script>
// import moment from 'moment'
import ReplyDetailModal from '../components/ReplyDetailModal'
import ReplyDelModal from '../components/ReplyDelModal'
export default {
    name: 'ReplyFeedback',
    components: { ReplyDetailModal, ReplyDelModal },
    data() {
        return {
            replyList: [],
            form: {
                page: 1,
                size: 5
            },
            total: 0,
            replyDetail: {},
            replyId: '',
            status: 'add'
        }
    },
    mounted() {
        this.getFeedBack();
    },
    methods: {
        handleShowEditModal(item, status) {
            this.status = status;
            this.replyDetail = item;
        },
        getFeedBack() {
            this.$axios.request({
                method: 'get',
                url: `/api/manage/feedback?page=${this.form.page}&size=${this.form.size}`,
            }).then(res => {
                this.replyList = res.data.feedbacks;
                this.total = res.data.total;
            }).catch(err => {
                console.log(err);
            })
        },
        handleShowDetailModal(item) {
            // 展示详情
            this.replyId = item.user_id;
        },
        goPage(type) {
            if (type == 0) {
                // 上一页
                if (this.form.page > 1) {
                    this.form.page--;
                    this.getFeedBack();
                }
            } else {
                // 下一页
                if ((this.form.page+1) * this.form.size - this.total < this.form.size) {
                    this.form.page++;
                    this.getFeedBack();
                }
            }
        },
    }
}
</script>

<style scoped>
.reply-feedback {
  padding: 20px;
}
</style>