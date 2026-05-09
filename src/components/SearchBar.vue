<template>
  <div
    :class="[
      isHero ? 'w-full' : 'my-4 w-full rounded-lg border-2 border-[#0047ab]/20 bg-slate-50 px-4 py-4 sm:px-5',
    ]"
  >
    <div
      :class="[
        'flex flex-col gap-4',
        isHero && centered ? 'mx-auto max-w-2xl items-center' : '',
      ]"
    >
      <div
        :class="[
          'flex w-full flex-col gap-3 sm:flex-row sm:items-stretch',
          isHero && centered ? 'sm:justify-center' : '',
        ]"
      >
        <input
          v-model="searchQuery"
          type="search"
          autocomplete="off"
          placeholder="Buscar artículos, autores, revistas…"
          :class="inputClass"
          @keydown.enter.prevent="performSearch"
        />

        <select v-model="searchField" :class="selectClass">
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
          :class="buttonClass"
          @click="performSearch"
        >
          Buscar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { getAllArticles } from '../data/articleItems.js'
import { articleMatchesQuery } from '../utils/searchMatch.js'

export default {
  props: {
    /** Centrar controles (página principal) */
    centered: {
      type: Boolean,
      default: false,
    },
    /** hero = campos claros sobre fondo azul (el padre debe pintar #0047ab). default = franja clara en resultados */
    layout: {
      type: String,
      default: 'default',
      validator: (v) => ['default', 'hero'].includes(v),
    },
  },
  computed: {
    isHero() {
      return this.layout === 'hero'
    },
    inputClass() {
      const base =
        'min-h-[44px] flex-1 rounded-lg border-2 px-4 py-2.5 shadow-inner placeholder:text-slate-400 focus:outline-none focus:ring-2 sm:min-w-0'
      if (this.isHero) {
        return `${base} border-white/40 bg-white text-[#0047ab] focus:border-white focus:ring-white/80`
      }
      return `${base} border-[#0047ab]/25 bg-white text-slate-900 focus:border-[#0047ab] focus:ring-[#0047ab]/30`
    },
    selectClass() {
      const base =
        'min-h-[44px] w-full rounded-lg border-2 px-3 py-2.5 text-sm font-medium focus:outline-none focus:ring-2 sm:w-48'
      if (this.isHero) {
        return `${base} border-white/40 bg-white/95 text-[#0047ab] focus:border-white focus:ring-white/80`
      }
      return `${base} border-[#0047ab]/25 bg-white text-[#0047ab] focus:border-[#0047ab] focus:ring-[#0047ab]/25`
    },
    buttonClass() {
      const base =
        'min-h-[44px] shrink-0 rounded-lg border-2 px-6 py-2.5 text-sm font-bold transition focus:outline-none focus:ring-2 sm:px-8'
      if (this.isHero) {
        return `${base} border-white bg-white text-[#0047ab] hover:bg-white/90 focus:ring-white focus:ring-offset-2 focus:ring-offset-[#0047ab]`
      }
      return `${base} border-[#0047ab] bg-[#0047ab] text-white hover:bg-[#003d96] focus:ring-[#0047ab] focus:ring-offset-2`
    },
  },
  data() {
    return {
      searchQuery: '',
      searchField: 'all',
    }
  },
  methods: {
    performSearch() {
      const articles = getAllArticles()
      const searchResults = articles.filter((article) =>
        articleMatchesQuery(article, this.searchQuery, this.searchField),
      )

      this.$router.push({
        path: '/results',
        query: {
          searchResults: JSON.stringify(searchResults),
        },
      })
    },
  },
}
</script>
