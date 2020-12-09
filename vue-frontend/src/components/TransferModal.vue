<template>
    <div>
            <div class="modal-dialog modal-dialog-centered modal-lg" @click="show_user_list=false;parent_clicked=true;">
                <div class="modal-content shadow-lg">
                    <div class="modal-header">
                        <h4 class="modal-title">转让场地</h4>
                        <button type="button" class="close" data-dismiss="modal">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        
                        <div class="alert alert-danger" v-if="failedToSubmit">
                            无法提交... {{ err_msg }}
                        </div>
                        <div class="alert alert-success" v-if="success">
                            提交成功
                        </div>
                        <div class="pt-1">
                            
                            <div class="container jumbotron p-2 px-4 rounded" v-if="selected_user">
                                <div class="row">
                                    <div class="col-9 d-flex justify-content-end align-items-center">
                                        <span class="mb-0 align-middle lead">您选择了用户api_id为 <b>{{ selected_user.api_id }}</b>的用户</span> 
                                    </div>
                                    <div class="col text-left d-flex align-items-center">
                                        <button class="btn btn-danger" @click="clearSelectedUser">清空</button>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <label><b>请输入目标用户的名字</b></label>
                                <input class="form-control" @keyup.stop="checkUser" @click.stop="checkUser" v-model="target_user_name">
                                <div class="dropdown-menu position-relative" :class="{'show':show_user_list}" v-if="user_list.length">
                                    <a class="dropdown-item" 
                                    v-for="user in user_list" 
                                    :key="user.user_id" 
                                    @click="updateSelectedUser(user)">{{ user.api_id }}</a>
                                </div>
                            </div>
                            <hr>
                            <div class="mt-1 pb-2 mx-2 flex justify-end">
                                
                                <div class="spinner-border" v-if="submitting"><span class="sr-only"></span></div>
                                <button class="btn btn-primary" v-else @click="transferCourt" :disabled="success">
                                    提交
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
</template>

<script>
// import xss from 'xss';
// import $ from 'jquery'

export default {
    props:["reservation"],
    data(){
        return {
            failedToSubmit:false,
            err_msg:"默认错误",
            submitting:false,
            success:false,
            selected_user:null,
            disabledAPIcall:false,
            target_user_name: "",
            user_list:[],
            show_user_list:true,
            parent_clicked:false
        }
    },
    methods:{
        updateSelectedUser(user){
            this.selected_user = user;
        },
        clearSelectedUser(){
            this.selected_user = null;
        },
        get_userid(){
            // 输入字符串不能为空
            if(this.target_user_name === ""){
                this.user_list = [];
                return;
            }

            // 通过真名获取api_id和user_id
            this.$axios
            .get(`/api/manage/getuserids?user_name=${this.target_user_name}`)
            .then((res) => {
                if(!res.users) this.user_list = res.data.users;
            })
        },
        checkUser(){

            // 显示用户匹配结果
            this.show_user_list = true;
            
            if(this.disabledAPIcall) return;
            
            // 未来1秒内停止发请求
            this.disabledAPIcall = true;

            // 1秒后回复正常
            setTimeout(() => {
                this.disabledAPIcall = false;
                this.get_userid();
            },1000)


            this.get_userid();

        },
        transferCourt(){
            // 没有选中转让场地的目标
            if(this.selected_user == null){
                this.err_msg = "还没有选中转让场地的目标用户";
                this.failedToSubmit = true;
                return;
            }

            // 转让场地
            this.$axios
            .post('/api/manage/reservation/transfer',{
                    new_user_id: this.selected_user.user_id,
                    reservation_id:this.reservation.reservation_id
                }
            )
            .then(() => 
            {
                // 设置UI控制变量,获取成功
                this.failedToSubmit = false;
                this.success = true;

                // 关闭弹窗
                setTimeout(() => {
                    this.success = false;
                    this.$emit('hide-modal');
                    this.$router.go()
                },1000);
            })
            .catch((err)=>{
                this.failedToSubmit = true;
                this.err_msg = err.response.data.message;
                
            })
            .finally(()=>{this.submitting = false;})
            
        },
    }
}
</script>