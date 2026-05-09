<template>

  <div class="space-y-10">
    <section
      class="mx-auto w-full max-w-3xl rounded-xl px-5 py-8 text-center shadow-md sm:px-8"
      style="background-color: #0047ab"
    >
      <h2 class="mb-6 text-xl font-semibold leading-snug text-white sm:text-2xl">
        Discover science by Salvadoran researchers
      </h2>
      <Search_bar layout="hero" :centered="true" />
    </section>

    <Tarjetas />
  </div>

</template>

<script>

  import Tarjetas from '../components/Tarjetas.vue';
  import Search_bar from '../components/SearchBar.vue';
  
  export default {
    components: {
      Tarjetas,
      Search_bar,
    }
  }
</script>
