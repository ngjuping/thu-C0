<template>
    <div class="card mb-3">
        <div class="card-header bg-dark text-light">{{ course.name }}</div>
        <div class="card-body">
            价格: {{ course.price }}
            <br/>
            课程介绍：
            <div class="jumbotron">
                {{ course.intro }}
            </div>
            <br/>
        </div>
        <div class="card-footer bg-dark text-light">
        联络方式：{{ course.tel }}
        </div>
    </div>
</template>

<script>
export default {
    props:["course"]
}
</script>