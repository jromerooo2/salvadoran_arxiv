<template>
    <nav class="nav-salvador w-full border-b border-black/10 px-4 py-4 sm:px-6 lg:px-8">
      <div class="mx-auto flex w-full max-w-none items-center justify-between">
        <!-- Brand Logo -->
        <router-link to="/" class="brand-mark" aria-label="Salvadoran Society of Sciences">
          <img
            :src="logo"
            alt="Salvadoran Society of Sciences"
          />
        </router-link>
        
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
              <router-link to="/researchers" class="block text-white py-2" @click="isOpen = false">Researchers</router-link>
            </li>
            <li>
              <router-link to="/articles" class="block text-white py-2" @click="isOpen = false">Articles</router-link>
            </li>
            <li>
              <router-link to="/people" class="block text-white py-2" @click="isOpen = false">People</router-link>
            </li>
            <li>
              <router-link to="/about" class="block text-white py-2" @click="isOpen = false">About</router-link>
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
  import logo from '../../images/SSS_logo_page-3_white_transparent.png';
  
  export default {
    data() {
      return {
        isOpen: false, // Controls the mobile menu toggle
        logo,
      };
    },
  };
  </script>
  
  <style scoped>
  /* Cobalt blue of the El Salvador flag stripes (~RGB 0, 71, 171) */
  .nav-salvador {
    background-color: #0047ab;
  }

  /* The PNG canvas is mostly transparent padding. Crop to the mark
     (bbox 889,1487–7212,2641 on an 8000×4500 image) so the wordmark
     fills the bar instead of shrinking inside the empty canvas. */
  .brand-mark {
    position: relative;
    display: block;
    height: 44px;
    width: calc(44px * 6324 / 1155);
    overflow: hidden;
    flex-shrink: 0;
  }

  .brand-mark img {
    position: absolute;
    height: calc(44px * 4500 / 1155);
    width: calc(44px * 8000 / 1155);
    max-width: none;
    left: calc(44px * -889 / 1155);
    top: calc(44px * -1487 / 1155);
  }
  </style>