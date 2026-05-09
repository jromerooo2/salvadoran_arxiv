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
          placeholder="Search articles, authors, journals…"
          :class="inputClass"
          @keydown.enter.prevent="performSearch"
        />

        <select v-model="searchField" :class="selectClass">
          <option value="all">All fields</option>
          <option value="title">Title</option>
          <option value="abstract">Abstract</option>
          <option value="journal">Journal</option>
          <option value="year">Year</option>
          <option value="doi">DOI</option>
          <option value="author">Author</option>
        </select>

        <button
          type="button"
          :class="buttonClass"
          @click="performSearch"
        >
          Search
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { getAllArticles } from '../data/articleItems.js'
import { articleMatchesQuery } from '../utils/searchMatch.js'

export default {
  name: 'SearchBar',
  props: {
    /** Center controls (home page hero) */
    centered: {
      type: Boolean,
      default: false,
    },
    /** hero = light fields on blue (#0047ab) background; default = light strip on results */
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
