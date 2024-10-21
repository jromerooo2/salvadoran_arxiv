<template>
    <div>
        <input type="text" v-model="searchQuery" placeholder="Search..." />
        <select v-model="searchField">
            <option value="all">All fields</option>
            <option value="title">Title</option>
            <option value="description">Description</option>
            <option value="author">Author</option>
            <option value="date_published">Date Published</option>
            <option value="subject">Subject</option>
        </select>
        <button @click="performSearch">Search</button>
    </div>
</template>
  
<script>

    import axios from 'axios';  

    export default {
        data() {
            return {
                searchQuery: '',
                searchField: 'all',
                articles: []
            };
        },
        methods: {
            async performSearch() {
                
                // Fetch data from data.json
                const response = await axios.get('/data.json');
                const articles = response.data;
        
                // Filter based on the selected field
                const searchResults = articles.filter(article => {
                    if (this.searchField === 'all') {
                        return Object.values(article)
                        .join(' ')
                        .toLowerCase()
                        .includes(this.searchQuery.toLowerCase());
                    } else {
                        return article[this.searchField]
                        .toLowerCase()
                        .includes(this.searchQuery.toLowerCase());
                    }
                });

                // Redirect to the results page with searchResults as prop
                this.$router.push({
                    path: '/results',
                    query: { searchResults: JSON.stringify(searchResults) }       
                });
            }
        }
    };
</script>
  