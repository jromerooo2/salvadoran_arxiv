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
      <Search_bar layout="hero" :centered="true" />
    </section>

    <nav
      class="category-index max-w-3xl text-sm leading-relaxed text-stone-600"
      aria-label="Browse by field"
    >
      <ul class="list-none space-y-5 p-0">
        <li v-for="(category, index) in table_of_content" :key="index">
          <h2 class="text-sm font-semibold leading-relaxed text-stone-900">
            {{ category.category_name }}
            <span class="font-normal text-stone-600">
              (<a class="text-[#0047ab] hover:underline" :href="category.category_articlesLink">recent articles</a>,
              <a class="text-[#0047ab] hover:underline" :href="category.category_researchersLink">researchers</a>)
            </span>
          </h2>
          <ul class="mt-1.5 list-none space-y-1.5 border-l-2 border-stone-200 pl-3">
            <li v-for="(subcategory, subIndex) in category.subcategories" :key="subIndex">
              <span class="text-sm leading-relaxed text-stone-700">
                {{ subcategory.subcategories_name }}
                <span class="font-normal text-stone-600">
                  (<a class="text-[#0047ab] hover:underline" :href="subcategory.subcategories_articlesLink">recent articles</a>,
                  <a class="text-[#0047ab] hover:underline" :href="subcategory.subcategories_researchersLink">researchers</a>)
                </span>
              </span>
            </li>
          </ul>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import Search_bar from '../components/SearchBar.vue'
import contentData from '../assets/content.json'

export default {
  components: {
    Search_bar,
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
