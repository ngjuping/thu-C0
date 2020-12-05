<template>
    <div class="reply-feedback">
        <table class="table">
            <thead class="thead-dark">
                <tr>
                <th scope="col">序号</th>
                <th scope="col">内容</th>
                <th scope="col">星级</th>
                <th scope="col">回复</th>
                <th scope="col">状态</th>
                <th scope="col">操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in replyList" :key="index">
                    <th scope="row">{{item.feedback_id}}</th>
                    <td>
                        <a
                            href="javascript:void(0)" 
                            class="card-link" 
                            data-toggle="modal" 
                            data-target="#replyDetailModal" 
                            @click="handleShowDetailModal(item)"
                        >{{item.content}}</a>
                    </td>
                    <td>
                        <img
                            src="../assets/star.png"
                            width="16"
                            height="16"
                            v-for="(item2, index2) in item.stars"
                            :key="index2"
                        />
                    </td>
                    <td>{{item.reply}}</td>
                    <td>{{item.solved ? '已回复' : '未回复'}}</td>
                    <td>
                        <button 
                            type="button" 
                            class="btn btn-danger btn-sm" 
                            data-toggle="modal" 
                            data-target="#delReplyModal"
                            style="margin-right: 5px"
                            @click="handleShowEditModal(item, 'delete')"
                        >删除</button>
                        <button v-if="!item.solved"
                            type="button" 
                            class="btn btn-info btn-sm"
                            data-toggle="modal" 
                            data-target="#ReplyModal"
                            @click="handleReplyModal(item, 'reply')"
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
        <reply-detail-modal :reply="reply" />
        <reply-modal
            :feedback-id="feedbackId"
            @reply-success="getFeedBack"    
        />
    </div>
</template>

<script>
// import moment from 'moment'
import ReplyDetailModal from '../components/ReplyDetailModal'
import ReplyDelModal from '../components/ReplyDelModal'
import ReplyModal from '../components/ReplyModal'
export default {
    name: 'ReplyFeedback',
    components: { ReplyDetailModal, ReplyDelModal, ReplyModal },
    data() {
        return {
            replyList: [],
            form: {
                page: 1,
                size: 5
            },
            total: 0,
            replyDetail: {},
            reply: {},
            status: 'add',
            feedbackId: '',  // 管理员回复的反馈id
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
        handleReplyModal(item) {
            // 管理员回复反馈
            this.feedbackId = item.feedback_id;
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
            this.reply = item;
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