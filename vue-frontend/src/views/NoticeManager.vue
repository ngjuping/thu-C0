<template>
    <div class="notice-manager">
        <table class="table">
            <thead class="thead-dark">
                <tr>
                <th scope="col">序号</th>
                <th scope="col">标题</th>
                <th scope="col">内容</th>
                <th scope="col">操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item,index) in noticeList" :key="index">
                <th scope="row">{{index + 1}}</th>
                <td>
                    <a
                        href="javascript:void(0)" 
                        class="card-link" 
                        data-toggle="modal" 
                        data-target="#venueDetailModal" 
                        @click="handleShowDetailModal(item)"
                    >{{item.title}}</a>
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
    name: 'NoticeManager',
    data() {
        return {
            noticeList: []
        }
    },
    mounted() {
        this.getNotice();
    },
    methods: {
        getNotice() {
            this.$axios.request({
                method: 'get',
                url: '/api/notices?page=1&size=5'
            }).then(res => {
                console.log(res.data)
                this.noticeList = res.data.notices;
            }).catch(err => {
                console.log(err);
            })
        }
    }
}
</script>

<style scoped>
.notice-manager {
  padding: 20px;
}
</style>