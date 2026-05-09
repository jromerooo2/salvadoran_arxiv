<template>

  <div class="space-y-10">
    <h1 class="text-2xl font-bold">Publications</h1>
    <p class="text-gray-700">
      Research articles in which Salvadoran scientists have participated, drawn from the society’s catalog.
    </p>
    <Tarjetas />
  </div>

</template>

<script>

  import Tarjetas from '../components/Tarjetas.vue';
  
  export default {
    components: {
      Tarjetas
    }
  }
</script>
