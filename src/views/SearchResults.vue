<template>
  <Search_bar />

  <div class="flex flex-col space-y-8">
    <div v-for="group in sortedArticlesByYear" :key="group.year" class="space-y-4">
      <h2 class="text-2xl font-semibold">{{ group.year }}</h2>

      <div class="flex w-full max-w-none flex-col gap-6">
        <div v-for="article in group.articles" :key="article.id" class="w-full">
          <Tarjeta
            :id="article.id"
            :title="article.title"
            :abstract="article.abstract"
            :year="article.year"
            :journal="article.journal"
            :doi="article.doi"
            :author="article.author"
            :affiliation="article.affiliation"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Search_bar from '../components/SearchBar.vue'
import Tarjeta from '../components/Tarjeta.vue'
import { publicationYearValue } from '../data/articleItems.js'

export default {
  components: {
    Tarjeta,
    Search_bar,
  },
  data() {
    return {
      results: [],
    }
  },
  methods: {
    loadResultsFromRoute() {
      const raw = this.$route.query.searchResults
      if (raw == null || raw === '') {
        this.results = []
        return
      }
      try {
        this.results = typeof raw === 'string' ? JSON.parse(raw) : raw
      } catch {
        this.results = []
      }
    },
  },
  created() {
    this.loadResultsFromRoute()
  },
  watch: {
    '$route.query.searchResults'() {
      this.loadResultsFromRoute()
    },
  },
  computed: {
    sortedArticlesByYear() {
      const sortedArticles = [...this.results].sort((a, b) => {
        const ya = publicationYearValue(a.year)
        const yb = publicationYearValue(b.year)
        if (ya !== yb) return yb - ya
        return (b.id ?? 0) - (a.id ?? 0)
      })

      const groupedByYear = sortedArticles.reduce((acc, article) => {
        const y = publicationYearValue(article.year)
        const key = y > 0 ? String(y) : 'No year'
        if (!acc[key]) acc[key] = []
        acc[key].push(article)
        return acc
      }, {})

      return Object.keys(groupedByYear)
        .sort((a, b) => {
          if (a === 'No year') return 1
          if (b === 'No year') return -1
          return Number(b) - Number(a)
        })
        .map((year) => ({
          year,
          articles: groupedByYear[year],
        }))
    },
  },
}
</script>
