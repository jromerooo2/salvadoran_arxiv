<template>
  <div class="h-screen p-10 bg-white">
    <Navbar />
    <router-view/>
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
