<template>
  <div class="space-y-10">
    <OrcidSubmissionBox />

    <section class="mx-auto w-full space-y-6 font-sans">
      <header class="space-y-2">
        <p class="text-sm text-gray-600">
          Public members of our community
        </p>
      </header>

      <ul class="divide-y divide-gray-200">
        <li
          v-for="(p, i) in people"
          :key="(p.correo_institucional || p.name || '') + i"
          class="py-3"
        >
          <div
            class="flex flex-col gap-1 sm:grid sm:grid-cols-12 sm:items-baseline sm:gap-6"
          >
            <p class="min-w-0 text-base font-semibold text-gray-900 sm:col-span-3">
              {{ p.name }}
            </p>
            <p
              v-if="p.titulo_afiliacion"
              class="min-w-0 text-sm leading-relaxed text-gray-700 sm:col-span-6"
            >
              {{ p.titulo_afiliacion }}
            </p>
            <a
              v-if="p.correo_institucional"
              :href="`mailto:${p.correo_institucional}`"
              class="break-all text-sm text-blue-700 hover:underline sm:col-span-3 sm:text-right"
            >
              {{ p.correo_institucional }}
            </a>
          </div>
        </li>
      </ul>
    </section>
  </div>
</template>

<script>
import peopleData from '../../comunidad/people.json'
import OrcidSubmissionBox from '../components/OrcidSubmissionBox.vue'

export default {
  name: 'People',
  components: {
    OrcidSubmissionBox,
  },
  data() {
    return {
      people: [],
    }
  },
  mounted() {
    this.people = [...peopleData].sort((a, b) =>
      (a?.name ?? '').localeCompare(b?.name ?? '', undefined, {
        sensitivity: 'base',
      }),
    )
  },
}
</script>
