<template>
  <div class="flex min-h-screen flex-col bg-white">
    <Navbar />
    <main class="flex-1 p-10">
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