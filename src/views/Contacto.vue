<template>
  <div class="space-y-10">
    <section class="mx-auto w-full space-y-8 font-sans">
      <div
        v-for="group in contactGroups"
        :key="group.title"
        class="space-y-4"
      >
        <h2 class="text-xl font-bold text-gray-900">{{ group.title }}</h2>
        <p class="text-base leading-relaxed text-gray-700">
          {{ group.description }}
        </p>

        <ul class="divide-y divide-gray-200">
          <li
            v-for="person in group.people"
            :key="person.email"
            class="py-3"
          >
            <div
              class="flex flex-col gap-1 sm:grid sm:grid-cols-12 sm:items-baseline sm:gap-6"
            >
              <p class="min-w-0 text-base font-semibold text-gray-900 sm:col-span-5">
                {{ person.name }}
              </p>
              <a
                :href="`mailto:${person.email}`"
                class="break-all text-sm text-blue-700 hover:underline sm:col-span-7 sm:text-right"
              >
                {{ person.email }}
              </a>
            </div>
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Contact',
  data() {
    return {
      contactGroups: [
        {
          title: 'Our community contacts',
          description:
            'For general inquiries, collaboration ideas, or to get involved with the Salvadoran scientific community.',
          people: [
            {
              name: 'Fernanda Sulantay Vargas',
              email: 'fernandasulantay@gmail.com',
            },
            {
              name: 'Miguel Montalvo',
              email: 'miguelmontalvo@princeton.edu',
            },
            {
              name: 'Erick Urquilla',
              email: 'erickurquilla@gmail.com',
            },
          ],
        },
        {
          title: 'This repository contacts',
          description:
            'For questions, suggestions, or contributions related specifically to this scientific repository.',
          people: [
            {
              name: 'Erick Urquilla',
              email: 'erickurquilla@gmail.com',
            },
            {
              name: 'Juan Romero',
              email: 'juan.romeroramos9@gmail.com',
            },
          ],
        },
      ],
    }
  },
}
</script>
