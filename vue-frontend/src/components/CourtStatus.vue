<template>
    <div class="jumbotron text-left shadow">
        Court id: {{ info.id }}
        <div v-for="status in info.status" :key="status.start">
            Start: {{ status.start }}
            End: {{ status.end }}
            Sports type: {{ info.type }}
            Status code: {{ status.code }}
        </div>
    </div>
</template>
<script>
export default {
    props:["info"]
}
</script>