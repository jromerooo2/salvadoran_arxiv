<template>
  <div class="space-y-10">
    <section
      class="mx-auto w-full max-w-3xl rounded-xl bg-[#0047ab] px-5 py-8 text-center shadow-md sm:px-8"
    >
      <h2 class="mb-6 text-xl font-semibold leading-snug text-white sm:text-2xl">
        Discover science by Salvadoran researchers
      </h2>
      <SearchBar layout="hero" :centered="true" />
    </section>

    <div class="flex w-full max-w-none flex-col gap-6">
      <div v-for="article in sortedArticles" :key="article.id" class="w-full">
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
</template>

<script>
import SearchBar from '../components/SearchBar.vue'
import Tarjeta from '../components/Tarjeta.vue'
import { publicationYearValue } from '../data/articleItems.js'

export default {
  components: {
    Tarjeta,
    SearchBar,
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
    /** Newest first; year headers removed — flat list only */
    sortedArticles() {
      return [...this.results].sort((a, b) => {
        const ya = publicationYearValue(a.year)
        const yb = publicationYearValue(b.year)
        if (ya !== yb) return yb - ya
        return (b.id ?? 0) - (a.id ?? 0)
      })
    },
  },
}
</script>
