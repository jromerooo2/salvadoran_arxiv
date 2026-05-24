<template>
  <div class="space-y-10">
    <section
      class="mx-auto w-full rounded-xl bg-[#0047ab] px-5 py-8 text-center shadow-md sm:px-8"
    >
      <h2 class="mb-6 text-xl font-semibold leading-snug text-white sm:text-2xl">
        Discover science by Salvadoran researchers
      </h2>
      <SearchBar layout="hero" :centered="true" />
    </section>

    <OrcidSubmissionBox />

    <nav
      class="category-index mx-auto flex w-full flex-col gap-6"
      aria-label="Browse by field"
    >
      <article
        v-for="(category, index) in table_of_content"
        :key="index"
        class="relative flex w-full max-w-none flex-col overflow-hidden rounded-lg border border-gray-100 bg-white p-4 font-sans shadow-sm sm:p-5"
      >
        <span
          class="pointer-events-none absolute inset-x-0 bottom-0 h-1.5 bg-gradient-to-r from-blue-100 via-blue-400 to-blue-700"
        ></span>

        <header class="pr-1">
          <h2 class="text-base font-bold leading-snug text-gray-900 sm:text-lg">
            {{ category.category_name }}
          </h2>
          <p class="mt-1 text-sm text-gray-600">
            (<a
              class="cursor-pointer text-blue-700 hover:underline"
              href="#"
              @click.prevent="searchByCategoryGroup(category)"
            >recent articles</a>,
            <a
              class="cursor-pointer text-blue-700 hover:underline"
              href="#"
              @click.prevent="researchersByCategoryGroup(category)"
            >researchers</a>)
          </p>
        </header>

        <section class="mt-3 min-h-0 flex-1 border-t border-gray-100 pt-3">
          <h3 class="sr-only">Subfields</h3>
          <ul class="m-0 list-none space-y-2.5 p-0">
            <li
              v-for="(subcategory, subIndex) in category.subcategories"
              :key="subIndex"
              class="text-sm leading-relaxed text-gray-600"
            >
              <span class="font-medium text-gray-800">
                {{ subcategory.subcategories_name }}<span v-if="subcategory.subcategories_code"> ({{ subcategory.subcategories_code }})</span>
              </span>
              <span class="font-normal text-gray-600">
                (<a
                  class="cursor-pointer text-blue-700 hover:underline"
                  href="#"
                  @click.prevent="searchByCategory(subcategory.subcategories_code)"
                >recent articles</a>,
                <a
                  class="cursor-pointer text-blue-700 hover:underline"
                  href="#"
                  @click.prevent="researchersByCategory(subcategory.subcategories_code)"
                >researchers</a>)
              </span>
            </li>
          </ul>
        </section>
      </article>
    </nav>
  </div>
</template>

<script>
import SearchBar from '../components/SearchBar.vue'
import OrcidSubmissionBox from '../components/OrcidSubmissionBox.vue'
import contentData from '../assets/content.json'
import { getAllArticles } from '../data/articleItems.js'

export default {
  components: {
    SearchBar,
    OrcidSubmissionBox,
  },
  data() {
    return {
      table_of_content: [],
    }
  },
  mounted() {
    this.table_of_content = contentData
  },
  methods: {
    searchByCategory(code) {
      const target = (code ?? '').toString().trim()
      if (!target) return
      const articles = getAllArticles()
      const searchResults = articles.filter(
        (a) => (a.category ?? '').toString().trim() === target,
      )
      this.$router.push({
        path: '/results',
        query: {
          searchResults: JSON.stringify(searchResults),
        },
      })
    },
    searchByCategoryGroup(category) {
      const codes = new Set(
        (category?.subcategories ?? [])
          .map((s) => (s?.subcategories_code ?? '').toString().trim())
          .filter(Boolean),
      )
      if (codes.size === 0) return
      const articles = getAllArticles()
      const searchResults = articles.filter((a) =>
        codes.has((a.category ?? '').toString().trim()),
      )
      this.$router.push({
        path: '/results',
        query: {
          searchResults: JSON.stringify(searchResults),
        },
      })
    },
    researchersByCategory(code) {
      const target = (code ?? '').toString().trim()
      if (!target) return
      this.$router.push({
        path: '/researchers',
        query: { category: target },
      })
    },
    researchersByCategoryGroup(category) {
      let prefix = (category?.category_code ?? '').toString().trim()
      if (!prefix) {
        const codes = (category?.subcategories ?? [])
          .map((s) => (s?.subcategories_code ?? '').toString().trim())
          .filter(Boolean)
        if (codes.length === 0) return
        const first = codes[0]
        const dash = first.indexOf('-')
        prefix = dash >= 0 ? first.slice(0, dash) : first
      }
      if (!prefix) return
      this.$router.push({
        path: '/researchers',
        query: { prefix },
      })
    },
  },
}
</script>
