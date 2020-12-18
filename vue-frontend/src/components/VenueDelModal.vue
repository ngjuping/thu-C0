<template>
    <div class="venue-delModal">
        <div class="modal fade" id="delVenueModal" aria-hidden="true" tabindex="-1" role="dialog">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">提示</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>是否删除该场馆</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">取消</button>
                        <button type="button" class="btn btn-primary" data-dismiss="modal" @click="handleSave">删除</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'VenueDelModal',
    props: {
        venueDetail: {
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
                venue_id: '',
            },
        }
    },
    methods: {
        handleSave() {
            // 删除
            this.$axios.post('/api/admin/delete/venue', this.formMessage).then((res) => {
                console.log(res, 'res')
                this.$emit('edit-success');
            }).catch(err => {
                console.log(err);
            })
        },
    },
    watch: {
        venueDetail(val) {
            this.formMessage = {
                venue_id: val.id,
            }
        }
    },
}
</script>

<style scoped>
    
</style>