<template>
  <div class="flex min-h-screen flex-col bg-white font-sans text-stone-900 antialiased">
    <Navbar />
    <main class="mx-auto w-full max-w-7xl flex-1 p-10">
      <router-view />
    </main>
  </div>
</template>

<script>
  import Navbar from './components/Navbar.vue';
  export default {
    components: {
      Navbar,
    },
  };
</script>