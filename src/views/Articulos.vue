<template>
    <div class="space-y-10">
      <h1 class="text-2xl font-bold">Artículos de Ciencia, en los que Salvadoreños han participado.</h1>
      <p>Aquí encontrarás artículos de diferentes materias en los cuales salvadoreños han formado parte.</p>
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