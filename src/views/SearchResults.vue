<template>
  <Search_bar />

  <div class="flex flex-col space-y-8">
    <div v-for="group in sortedArticlesByYear" :key="group.year" class="space-y-4">
      <h2 class="text-2xl font-semibold">{{ group.year }}</h2>

      <div class="flex flex-col gap-6 md:grid md:grid-cols-2 md:gap-6 lg:grid-cols-3">
        <div v-for="article in group.articles" :key="article.id">
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
    </div>
  </div>
</template>

<script>
import Search_bar from '../components/SearchBar.vue'
import Tarjeta from '../components/Tarjeta.vue'

function publicationYear(article) {
  const y = article.year
  if (y === undefined || y === null || String(y).trim() === '') return 0
  const n = parseInt(String(y), 10)
  return Number.isFinite(n) ? n : 0
}

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
  created() {
    const searchResults = this.$route.query.searchResults
    this.results = searchResults ? JSON.parse(searchResults) : []
  },
  computed: {
    sortedArticlesByYear() {
      const sortedArticles = [...this.results].sort(
        (a, b) => publicationYear(b) - publicationYear(a),
      )

      const groupedByYear = sortedArticles.reduce((acc, article) => {
        const y = publicationYear(article)
        const key = y > 0 ? String(y) : 'Sin año'
        if (!acc[key]) acc[key] = []
        acc[key].push(article)
        return acc
      }, {})

      return Object.keys(groupedByYear)
        .sort((a, b) => {
          if (a === 'Sin año') return 1
          if (b === 'Sin año') return -1
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
