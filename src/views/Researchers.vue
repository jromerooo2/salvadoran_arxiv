<template>
  <div class="space-y-10">

    <OrcidSubmissionBox />

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
          <p class="mt-1 text-sm text-gray-600">
            <span class="font-medium text-gray-500">Papers in catalog:</span>
            <span class="ml-1 text-gray-800">{{ r.paperCount }}</span>
          </p>
          <p v-if="r.recentAffiliation" class="mt-2 text-sm leading-relaxed text-gray-700">
            <span class="font-medium text-gray-500">Affiliation</span>
            <span class="text-gray-800">: </span>
            {{ r.recentAffiliation }}
          </p>
          <p v-else class="mt-2 text-sm italic text-gray-400">
            No affiliation on record in recent publications.
          </p>
          <p v-if="r.categories && r.categories.length" class="mt-2 text-sm leading-relaxed text-gray-700">
            <span class="font-medium text-gray-500">Research fields:</span>
            <span class="ml-1 text-gray-800">
              <template v-for="(c, ci) in r.categories" :key="c.code">
                <span v-if="ci > 0">, </span>{{ c.code }}
              </template>
            </span>
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
import OrcidSubmissionBox from '../components/OrcidSubmissionBox.vue'
import { getResearchers, orcidDisplayId } from '../data/researchers.js'
import { getAllArticles } from '../data/articleItems.js'

export default {
  name: 'Researchers',
  components: {
    OrcidSubmissionBox,
  },
  data() {
    return {
      researchers: [],
    }
  },
  created() {
    this.applyFilterFromRoute()
  },
  watch: {
    '$route.query.category'() {
      this.applyFilterFromRoute()
    },
    '$route.query.prefix'() {
      this.applyFilterFromRoute()
    },
  },
  methods: {
    orcidDisplayId: (url) => orcidDisplayId(url),
    applyFilterFromRoute() {
      const all = getResearchers()
      const code = (this.$route.query.category ?? '').toString().trim()
      const prefix = (this.$route.query.prefix ?? '').toString().trim()

      if (code) {
        this.researchers = all.filter((r) =>
          Array.isArray(r.categories) &&
          r.categories.some((c) => (c?.code ?? '').toString().trim() === code),
        )
        return
      }

      if (prefix) {
        const head = `${prefix}-`
        this.researchers = all.filter((r) =>
          Array.isArray(r.categories) &&
          r.categories.some((c) => {
            const cc = (c?.code ?? '').toString().trim()
            return cc === prefix || cc.startsWith(head)
          }),
        )
        return
      }

      this.researchers = all
    },
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
