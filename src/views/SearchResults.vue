<template>
    <div>
        <h1>Search Results</h1>
        <ul v-if="results.length > 0">
            <li v-for="article in results" :key="article.id">
                <h2>{{ article.title }}</h2>
                <p>{{ article.description }}</p>
                <p><strong>Author:</strong> {{ article.author }}</p>
                <p><strong>Date Published:</strong> {{ article.date_published }}</p>
                <p><strong>Subject:</strong> {{ article.subject }}</p>
                </li>
            </ul>
        <p v-else>No articles found.</p>
    </div>
</template>
  
<script>
    export default {
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