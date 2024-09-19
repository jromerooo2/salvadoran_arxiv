<template>
    <div class="md:grid md:grid-cols-3 md:gap-8 flex flex-col">
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