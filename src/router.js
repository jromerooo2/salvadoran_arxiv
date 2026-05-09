import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import About from './views/About.vue';
import Articulos from './views/Articulos.vue';
import Contact from './views/Contacto.vue';
import Researchers from './views/Researchers.vue';
import Results from './views/SearchResults.vue';

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/about', name: 'About', component: About },
  { path: '/articulos', redirect: '/articles' },
  { path: '/articles', name: 'Articles', component: Articulos },
  { path: '/researchers', name: 'Researchers', component: Researchers },
  { path: '/contact', name: 'Contact', component: Contact },
  { path: '/results', name: 'Results', component: Results},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;