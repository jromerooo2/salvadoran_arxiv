<script setup>
import { computed } from 'vue'

const props = defineProps({
  id: [String, Number],
  title: String,
  abstract: String,
  year: [String, Number],
  journal: String,
  doi: String,
  author: String,
  affiliation: String,
})

const yearLabel = computed(() => {
  const y = props.year
  if (y === undefined || y === null || String(y).trim() === '') return '—'
  return String(y)
})

const journalLabel = computed(() => {
  const j = props.journal
  if (!j || String(j).trim() === '') return '—'
  return String(j)
})

const doiHref = computed(() => {
  const d = props.doi
  if (!d || String(d).trim() === '') return null
  const s = String(d).trim()
  if (s.startsWith('http')) return s
  if (s.startsWith('10.')) return `https://doi.org/${s}`
  return null
})

const doiDisplay = computed(() => {
  const d = props.doi
  if (!d || String(d).trim() === '') return '—'
  const s = String(d).trim()
  if (s.startsWith('https://doi.org/')) return s.replace('https://doi.org/', '')
  if (s.startsWith('http://doi.org/')) return s.replace('http://doi.org/', '')
  return s
})

const authorLine = computed(() => {
  const auth = (props.author ?? '').trim()
  if (!auth) return ''
  const aff = (props.affiliation ?? '').trim()
  if (!aff || aff.toUpperCase() === 'N/A') return auth
  return `${auth}, ${aff}`
})

const abstractIsMissing = computed(() => {
  const a = (props.abstract ?? '').trim()
  return !a || a === 'N/A' || a.toUpperCase() === 'N/A'
})

const abstractPreview = computed(() => {
  if (abstractIsMissing.value) return ''
  return String(props.abstract).trim()
})
</script>

<template>
  <article
    class="relative flex h-full w-full max-w-none flex-col overflow-hidden rounded-lg border border-gray-100 bg-white p-4 font-sans shadow-sm sm:p-5"
  >
    <span
      class="pointer-events-none absolute inset-x-0 bottom-0 h-1.5 bg-gradient-to-r from-blue-100 via-blue-400 to-blue-700"
    ></span>

    <header class="pr-1">
      <h3 class="text-base font-bold leading-snug text-gray-900 sm:text-lg">
        {{ title }}
      </h3>
      <p v-if="authorLine" class="mt-1 text-sm text-gray-600">
        {{ authorLine }}
      </p>
      <div
        class="mt-2 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-gray-600"
      >
        <span class="inline-flex items-center rounded bg-gray-100 px-2 py-0.5 font-medium text-gray-800">
          {{ yearLabel }}
        </span>
        <span class="text-gray-400" aria-hidden="true">·</span>
        <span class="inline-flex min-w-0 flex-wrap items-center gap-x-1 break-words text-gray-800">
          <span class="shrink-0 font-medium text-gray-500">Journal:</span>
          <span class="min-w-0 font-medium text-gray-700">{{ journalLabel }}</span>
        </span>
        <span class="text-gray-400" aria-hidden="true">·</span>
        <span class="inline-flex min-w-0 flex-wrap items-center gap-x-1 break-all text-gray-800">
          <span class="shrink-0 font-medium text-gray-500">DOI:</span>
          <a
            v-if="doiHref"
            :href="doiHref"
            class="text-blue-700 hover:underline"
            target="_blank"
            rel="noopener noreferrer"
          >{{ doiDisplay }}</a>
          <span v-else>{{ doiDisplay }}</span>
        </span>
      </div>
    </header>

    <section class="mt-3 min-h-0 flex-1 border-t border-gray-100 pt-3">
      <h4 class="sr-only">Abstract</h4>
      <p
        v-if="abstractIsMissing"
        class="text-sm italic text-gray-400"
      >
        No abstract available.
      </p>
      <p
        v-else
        class="line-clamp-5 text-pretty text-sm leading-relaxed text-gray-600"
      >
        {{ abstractPreview }}
      </p>
    </section>
  </article>
</template>
