<template>
  <div class="flex flex-col gap-6 md:grid md:grid-cols-2 md:gap-6 lg:grid-cols-3">
    <div v-for="article in articles" :key="article.id" class="min-h-0">
      <Tarjeta
        :id="article.id"
        :title="article.title"
        :abstract="article.abstract"
        :year="article.year"
        :journal="article.journal"
        :doi="article.doi"
        :author="article.author"
      />
    </div>
  </div>
</template>

<script>
import Tarjeta from './Tarjeta.vue'
import { getAllArticles } from '../data/articleItems.js'

export default {
  components: {
    Tarjeta,
  },
  data() {
    return {
      articles: [],
    }
  },
  mounted() {
    this.articles = getAllArticles()
  },
}
</script>
