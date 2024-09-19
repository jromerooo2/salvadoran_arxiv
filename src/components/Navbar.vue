<template>
    <nav class="bg-blue-600 p-4">
      <div class="container flex justify-between items-center">
        <!-- Brand Logo -->
        <router-link to="/" class="text-white font-bold text-xl">Repositorio Salvadoreño de Ciencia.</router-link>
        
        <!-- Hamburger Icon for Mobile -->
        <button
          @click="isOpen = !isOpen"
          class="text-white block md:hidden focus:outline-none"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 6h16M4 12h16M4 18h16"
            ></path>
          </svg>
        </button>
        
        <!-- Links (shown or hidden depending on screen size) -->
        <div :class="isOpen ? 'block' : 'hidden'" class="w-full md:flex md:items-center md:w-auto">
          <ul class="flex flex-col md:flex-row md:space-x-4">
            <li>
              <router-link to="/" class="block text-white py-2" @click="isOpen = false">Home</router-link>
            </li>
            <li>
              <router-link to="/about" class="block text-white py-2" @click="isOpen = false">About</router-link>
            </li>
            <li>
              <router-link to="/articulos" class="block text-white py-2" @click="isOpen = false">Artículos</router-link>
            </li>
            <li>
              <router-link to="/contact" class="block text-white py-2" @click="isOpen = false">Contact</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  
  export default {
    data() {
      return {
        isOpen: false, // Controls the mobile menu toggle
      };
    },
  };
  </script>
  
  <style scoped>
  /* Add custom styles if needed */
  </style>