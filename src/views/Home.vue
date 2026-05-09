<template>

  <!-- Home page initial description -->
  <div class="container">
    <h3>
      La Sociedad Salvadoreña de Ciencia es una organización sin fines de lucro dedicada a fomentar el debate
      científico, el trabajo en red entre investigadoras e investigadores y la difusión del conocimiento en
      beneficio de la sociedad. Este sitio ofrece información general y recursos de interés para la comunidad.
    </h3>
  </div>

  <!-- Search bar -->
  <Search_bar />

  <!-- Table of content -->
  <div class="category-index">
    <ul>
      <li v-for="(category, index) in table_of_content" :key="index">
        <h1>
          {{ category.category_name }}
          <span class="links">
            (<a :href="category.category_recentLink">recent</a>,
            <a :href="category.category_searchLink">search</a>)
          </span>
        </h1>
        <div v-for="(subcategory, subIndex) in category.subcategories" :key="subIndex">
          <b>{{ subcategory.subcategories_name }}
            <span class="links">
              (<a :href="subcategory.subcategories_recentLink">recent</a>,
              <a :href="subcategory.subcategories_searchLink">search</a>)
            </span>
          </b>
        </div>
      </li>
    </ul>
  </div>

</template>

<script>
  
  // Import the SearchBar component
  import Search_bar from '../components/SearchBar.vue';

  // Import the array of data containing the table of contents to be printed on the homepage.
  import contentData from '../assets/content.json';

  export default {
    components: {
      Search_bar
    },
    data() {
      return {
        table_of_content: [],
      };
    },
    mounted() {
      this.table_of_content = contentData;
    },
  };

</script>






<style scoped>

  .container {
    font-family: Arial, sans-serif;
  }

  h3 {
    font-family: Arial;
    font-size: 15px;
    text-align: left;
    color: #06080e;
    margin-top: 10px;
    margin-bottom: 10px;
    letter-spacing: 0px;
  }

  .search-bar {
    display: flex;
    align-items: center;
    background-color: #ffffff;
    padding: 5px;
  }

  .search-input {
    padding: 8px;
    width: 200px;
    border: 1px solid #ddd;
    border-right: none;
    border-radius: 4px 0 0 4px;
  }

  .search-select {
    padding: 8px;
    border: 1px solid #ddd;
    border-left: none;
    border-right: none;
    border-radius: 0;
    background-color: white;
  }

  .search-button {
    padding: 8px 16px;
    background-color: #0025a0;
    color: white;
    border: 1px solid #0025a0;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
  }

  .search-button:hover {
    background-color: #0025a0;
  }

  .category-index {
    font-family: Arial, sans-serif;
    font-size: 14px;
  }

  .category-index ul {
    list-style-type: none;
    padding: 0;
  }

  .category-index li {
    margin-bottom: 5px;
  }

  .category-index a {
    color: #4b0082;
    text-decoration: none;
  }

  .category-index a:hover {
    text-decoration: underline;
  }

  b {
    color: #000000;
    font-size: 12px;
  }

  .links {
    font-size: 12px;
  }

  .subcategories {
    font-size: 12px;
    color: #555;
    margin-left: 10px;
  }

  h1 {
    font-size: 24px;
    color: #333;
  }

</style>
