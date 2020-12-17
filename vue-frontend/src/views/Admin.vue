<template>
    <div class="admin">
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item active">
                        <a class="nav-link" href="/#/admin">Home <span class="sr-only">(current)</span></a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/#/admin/venues">场馆管理</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/#/admin/bookingManage">场地管理</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/#/admin/fieldInit">学期场地管理</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/#/admin/replyFeedback">回复反馈</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/#/admin/noticeManager">通知管理</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/#/admin/trainManager">培训课程管理</a>
                    </li>
                </ul>
            </div>
        </nav>
        <router-view />
    </div>
</template>

<script>
export default {
    name: 'Admin'
}
</script>

<style scoped>
.admin {}
</style>