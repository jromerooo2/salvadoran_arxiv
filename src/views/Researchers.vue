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
      <article
        v-for="(r, index) in researchers"
        :key="r.orcid + index"
        class="relative flex w-full max-w-none flex-col overflow-hidden rounded-lg border border-gray-100 bg-white p-4 font-sans shadow-sm sm:p-5"
      >
        <span
          class="pointer-events-none absolute inset-x-0 bottom-0 h-1.5 bg-gradient-to-r from-blue-100 via-blue-400 to-blue-700"
        ></span>

        <header class="pr-1">
          <h2 class="text-base font-bold leading-snug text-gray-900 sm:text-lg">
            {{ r.name }}
          </h2>
          <p class="mt-1 text-sm text-gray-600">
            <span class="font-medium text-gray-500">ORCID:</span>
            <a
              v-if="r.orcid"
              :href="r.orcid"
              class="ml-1 text-blue-700 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >{{ orcidDisplayId(r.orcid) }}</a>
            <span v-else class="text-gray-400">—</span>
          </p>
          <p v-if="r.recentAffiliation" class="mt-2 text-sm leading-relaxed text-gray-700">
            <span class="font-medium text-gray-500">Affiliation</span>
            <span class="text-gray-800">: </span>
            {{ r.recentAffiliation }}
          </p>
          <p v-else class="mt-2 text-sm italic text-gray-400">
            No affiliation on record in recent publications.
          </p>
        </header>

        <section class="mt-3 min-h-0 flex-1 border-t border-gray-100 pt-3">
          <h3 class="text-xs font-semibold uppercase tracking-wide text-gray-500">
            Recent articles
          </h3>
          <ol v-if="r.recentTitles.length" class="mt-2 list-decimal space-y-1.5 pl-5 text-sm leading-relaxed text-gray-700">
            <li v-for="(title, ti) in r.recentTitles" :key="ti" class="text-pretty">
              {{ title }}
            </li>
          </ol>
          <p v-else class="mt-2 text-sm italic text-gray-400">No articles listed.</p>

          <div class="mt-4 border-t border-gray-100 pt-3">
            <button
              type="button"
              class="text-sm font-medium text-blue-700 hover:text-blue-800 hover:underline"
              @click="seeMorePapers(r.orcid)"
            >
              See more papers…
            </button>
          </div>
        </section>
      </article>
    </div>
  </div>
</template>

<script>
import SearchBar from '../components/SearchBar.vue'
import { getResearchers, orcidDisplayId } from '../data/researchers.js'
import { getAllArticles } from '../data/articleItems.js'

export default {
  name: 'Researchers',
  components: {
    SearchBar,
  },
  data() {
    return {
      researchers: [],
    }
  },
  mounted() {
    this.researchers = getResearchers()
  },
  methods: {
    orcidDisplayId: (url) => orcidDisplayId(url),
    seeMorePapers(orcid) {
      const all = getAllArticles()
      const list = orcid ? all.filter((a) => a.orcid === orcid) : []
      this.$router.push({
        path: '/results',
        query: {
          searchResults: JSON.stringify(list),
        },
      })
    },
  },
}
</script>
