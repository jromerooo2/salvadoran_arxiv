<template>
    <!-- Search bar -->
    <Search_bar />

    <!-- Main results content with articles grouped by year -->
    <div class="flex flex-col space-y-8">
      <!-- Loop through each year group -->
      <div v-for="group in sortedArticlesByYear" :key="group.year" class="space-y-4">
        <!-- Year subtitle -->
        <h2 class="text-2xl font-semibold">{{ group.year }}</h2>
  
        <!-- Articles grid for each year -->
        <div class="md:grid md:grid-cols-3 md:gap-8 flex flex-col">
          <div v-for="article in group.articles" :key="article.id">
            <Tarjeta 
              :id="article.id" 
              :title="article.title" 
              :subject="article.subject" 
              :description="article.description" 
              :author="article.author" 
              :date_published="article.date_published" 
            />
          </div>
        </div>
      </div>
    </div>
  </template>
 
<script>
  // Import the SearchBar component
  import Search_bar from '../components/SearchBar.vue';
  import Tarjeta from '../components/Tarjeta.vue';
  
  export default {
    components: {
      Tarjeta,
      Search_bar
    },
    data() {
      return {
        results: []
      };
    },
    created() {
      // Get the search results from the query parameters
      const searchResults = this.$route.query.searchResults;
      this.results = searchResults ? JSON.parse(searchResults) : [];
    },
    computed: {
        sortedArticlesByYear() {
            // Sort the articles by most recent date first
            const sortedArticles = [...this.results].sort((a, b) => {
            return new Date(b.date_published) - new Date(a.date_published);
            });

            // Group articles by year
            const groupedByYear = sortedArticles.reduce((acc, article) => {
            const year = new Date(article.date_published).getFullYear();
            if (!acc[year]) {
                acc[year] = [];
            }
            acc[year].push(article);
            return acc;
            }, {});

            // Return an array of year groups sorted in descending order
            return Object.keys(groupedByYear)
            .sort((a, b) => b - a) // Sort years in descending order (newest year first)
            .map(year => ({
                year,
                articles: groupedByYear[year]
            }));
        }
    }
  };
  </script>
