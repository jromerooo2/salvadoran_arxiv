<template>
    <div class="my-4">
      <!-- Smaller search input with blue background -->
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="Search..." 
        class="w-full md:w-2/5 px-3 py-1 bg-white border border-black rounded-md text-black text-sm focus:bg-gray-100 focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-600 mb-2"
      />
  
      <!-- Smaller select dropdown with blue background -->
      <select 
        v-model="searchField" 
        class="w-full md:w-1/5 px-3 py-1 bg-white border border-black rounded-md text-black text-sm focus:bg-gray-100 focus:outline-none focus:border-gray-600 focus:ring-2 focus:ring-gray-600 mb-2"
      >
        <option value="all">All fields</option>
        <option value="title">Title</option>
        <option value="description">Description</option>
        <option value="author">Author</option>
        <option value="date_published">Date Published</option>
        <option value="subject">Subject</option>
      </select>
  
      <!-- Smaller search button -->
      <button 
        @click="performSearch" 
        class="w-full md:w-auto bg-blue-600 hover:bg-blue-700 text-white font-semibold py-1 px-4 rounded-md text-sm transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        Search
      </button>
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

                window.location.assign(`/results?searchResults=${encodeURIComponent(JSON.stringify(searchResults))}`);

            }
        }
    };
</script>
  