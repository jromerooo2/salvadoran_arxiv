<template>
    <div class="grid grid-cols-3 gap-8">
        <div v-for="x in 5" class="">
            <Tarjeta />
        </div>
    </div>
</template>

<script>
import Tarjeta from './Tarjeta.vue';
export default {
    components: {
        Tarjeta
    }
}
</script>