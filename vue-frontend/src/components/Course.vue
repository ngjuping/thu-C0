<template>
    <div class="card">
        <div class="card-header">{{ course.name }}</div>
        <div class="card-body">
            价格: {{ course.price }}
        </div>
    </div>
</template>

<script>
export default {
    props:["course"]
}
</script>