<template>
  <div class="my-4">
    <input
      v-model="searchQuery"
      type="text"
      placeholder="Buscar…"
      class="mb-2 w-full rounded-md border border-black bg-white px-3 py-1 text-sm text-black focus:border-gray-600 focus:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-600 md:w-2/5"
    />

    <select
      v-model="searchField"
      class="mb-2 w-full rounded-md border border-black bg-white px-3 py-1 text-sm text-black focus:border-gray-600 focus:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-600 md:w-1/5"
    >
      <option value="all">Todos los campos</option>
      <option value="title">Título</option>
      <option value="abstract">Resumen</option>
      <option value="journal">Revista</option>
      <option value="year">Año</option>
      <option value="doi">DOI</option>
      <option value="author">Autor</option>
    </select>

    <button
      type="button"
      class="w-full rounded-md bg-blue-600 px-4 py-1 text-sm font-semibold text-white transition-all duration-300 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 md:w-auto"
      @click="performSearch"
    >
      Buscar
    </button>
  </div>
</template>

<script>
import { getAllArticles } from '../data/articleItems.js'

export default {
  data() {
    return {
      searchQuery: '',
      searchField: 'all',
    }
  },
  methods: {
    performSearch() {
      const articles = getAllArticles()
      const q = this.searchQuery.toLowerCase().trim()

      const searchResults = articles.filter((article) => {
        if (!q) return true
        if (this.searchField === 'all') {
          return Object.values(article)
            .join(' ')
            .toLowerCase()
            .includes(q)
        }
        const field = article[this.searchField]
        return String(field ?? '')
          .toLowerCase()
          .includes(q)
      })

      window.location.assign(
        `/results?searchResults=${encodeURIComponent(JSON.stringify(searchResults))}`,
      )
    },
  },
}
</script>
