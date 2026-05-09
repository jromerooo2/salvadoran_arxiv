<template>
  <div>
    <div class="max-w-3xl">
      <p class="text-left text-base leading-relaxed text-stone-800">
        The <strong class="font-semibold text-stone-900">Salvadoran Society of Sciences</strong> is a non-profit
        organization dedicated to fostering scientific debate, networks among researchers, and the dissemination of
        knowledge for the benefit of society. This site offers general information and resources for the community.
      </p>
    </div>

    <section
      class="home-search mx-auto mb-10 mt-6 w-full max-w-3xl rounded-xl bg-[#0047ab] px-5 py-8 text-center shadow-md sm:px-8"
    >
      <h2 class="mb-6 text-xl font-semibold leading-snug text-white sm:text-2xl">
        Discover science by Salvadoran researchers
      </h2>
      <SearchBar layout="hero" :centered="true" />
    </section>

    <nav
      class="category-index mx-auto mt-8 flex w-full max-w-3xl flex-col gap-6"
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
            (<a class="text-blue-700 hover:underline" :href="category.category_articlesLink">recent articles</a>,
            <a class="text-blue-700 hover:underline" :href="category.category_researchersLink">researchers</a>)
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
              <span class="font-medium text-gray-800">{{ subcategory.subcategories_name }}</span>
              <span class="font-normal text-gray-600">
                (<a class="text-blue-700 hover:underline" :href="subcategory.subcategories_articlesLink">recent articles</a>,
                <a class="text-blue-700 hover:underline" :href="subcategory.subcategories_researchersLink">researchers</a>)
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
import contentData from '../assets/content.json'

export default {
  components: {
    SearchBar,
  },
  data() {
    return {
      table_of_content: [],
    }
  },
  mounted() {
    this.table_of_content = contentData
  },
}
</script>
