<template>
  <div class="flex w-full max-w-none flex-col gap-6">
    <div v-for="article in articles" :key="article.id" class="min-h-0 w-full">
      <Tarjeta
        :id="article.id"
        :title="article.title"
        :abstract="article.abstract"
        :year="article.year"
        :journal="article.journal"
        :doi="article.doi"
        :author="article.author"
        :affiliation="article.affiliation"
        :category="article.category"
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
