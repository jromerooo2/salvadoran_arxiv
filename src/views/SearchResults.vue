<template>
    <div class="md:grid md:grid-cols-3 md:gap-8 flex flex-col">
        <div v-for="article in results" :key="article.id" class="">
            <Tarjeta :id="article.id" :title="article.title" :subject="article.subject" :description="article.description" :author="article.author" :date_published="article.date_published" />
        </div>
    </div>
</template>
  
<script>

    import Tarjeta from '../components/Tarjeta.vue';
    
    export default {
        components: {
            Tarjeta
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
        }
    };

</script>