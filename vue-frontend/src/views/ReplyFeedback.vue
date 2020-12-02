<template>
    <div class="reply-feedback">
        <table class="table">
            <thead class="thead-dark">
                <tr>
                <th scope="col">序号</th>
                <th scope="col">内容</th>
                <th scope="col">评级</th>
                <th scope="col">回复</th>
                <th scope="col">操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item,index) in replyList" :key="index">
                <th scope="row">{{index + 1}}</th>
                <td>
                    <a
                        href="javascript:void(0)" 
                        class="card-link" 
                        data-toggle="modal" 
                        data-target="#venueDetailModal" 
                        @click="handleShowDetailModal(item)"
                    >{{item.name}}</a>
                </td>
                <td>
                    <button 
                        type="button" 
                        class="btn btn-primary btn-sm" 
                        data-toggle="modal" 
                        data-target="#editVenueModal" 
                        @click="handleShowEditModal(item)"
                    >
                    编辑
                    </button>
                </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
// import moment from 'moment'
export default {
    name: 'ReplyFeedback',
    data() {
        return {
            replyList: []
        }
    },
    mounted() {
        this.getFeedBack();
    },
    methods: {
        getFeedBack() {
            this.$axios.request({
                method: 'get',
                url: '/api/manage/feedback?page=1&size=5'
            }).then(res => {
                console.log(22)
                this.replyList = res.data.feedbacks;
            }).catch(err => {
                console.log(err);
            })
        }
    }
}
</script>

<style scoped>
.reply-feedback {
  padding: 20px;
}
</style>