<template>
  <div>
    <Navbar />
    <router-view />
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
<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
