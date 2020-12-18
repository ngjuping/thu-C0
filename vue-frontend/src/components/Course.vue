<template>
    <div class="card">
        <div class="card-header">{{ course.name }}</div>
        <div class="card-body">
            价格: {{ course.price }}
            <br/>
            教练介绍：
            <div class="jumbotron">
                {{ course.intro }}
            </div>
            <br/>
            <div class="card-footer">
            联络方式：{{ course.tel }}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props:["course"]
}
</script>