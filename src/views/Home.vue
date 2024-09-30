<template>

  <!-- Home page initial description -->
  <div class="container">
    <h3>El Repositorio Salvadoreño de Ciencia (RSC) es una plataforma dedicada a la difusion gratuita de artículos científicos realizados por investigadores salvadoreños. Este repositorio permite que la ciencia producida en El Salvador sea visible y accesible tanto a nivel local como internacional. Los temas abarcan desde las ciencias naturales, ingeniería, ciencias sociales y otros campos del conocimiento, y buscan promover la colaboración y difusión de la ciencia hecha en El Salvador.</h3>
  </div>

  <!-- Search bar -->
  <div class="search-bar">
    <input
      type="text"
      class="search-input"
      placeholder="Search..."
      v-model="searchQuery"
    />
    <select v-model="selectedField" class="search-select">
      <option>All fields</option>
      <option>Title</option>
      <option>Author</option>
      <option>Abstract</option>
    </select>
    <button @click="performSearch" class="search-button">Search</button>
  </div>
  
  <!-- Table of content -->
  <div class="category-index">
    <ul>
      <li v-for="(category, index) in table_of_content" :key="index">
        <h1>{{ category.category_name }}
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
  export default {

    data() {
      return {
        searchQuery: '',
        selectedField: 'All fields',

        table_of_content: [
          {

            category_name : "Fisica",
            category_recentLink: "#",
            category_searchLink: "#",

            subcategories: [
              {
                subcategories_name: "Astrophysics (astro-ph)",
                subcategories_recentLink: "#",
                subcategories_searchLink: "#",
              },
              {
                subcategories_name: "Condensed Matter (cond-mat)",
                subcategories_recentLink: "#",
                subcategories_searchLink: "#",
              },
              {
                subcategories_name: "General Relativity and Quantum Cosmology (gr-qc)",
                subcategories_recentLink: "#",
                subcategories_searchLink: "#",
              }
            ],
          },
          {

            category_name : "Fisica",
            category_recentLink: "#",
            category_searchLink: "#",

            subcategories: [
              {
                subcategories_name: "Astrophysics (astro-ph)",
                subcategories_recentLink: "#",
                subcategories_searchLink: "#",
              },
              {
                subcategories_name: "Condensed Matter (cond-mat)",
                subcategories_recentLink: "#",
                subcategories_searchLink: "#",
              },
              {
                subcategories_name: "General Relativity and Quantum Cosmology (gr-qc)",
                subcategories_recentLink: "#",
                subcategories_searchLink: "#",
              }
            ],
          },
          {

            category_name : "Fisica",
            category_recentLink: "#",
            category_searchLink: "#",

            subcategories: [
              {
                subcategories_name: "Astrophysics (astro-ph)",
                subcategories_recentLink: "#",
                subcategories_searchLink: "#",
              },
              {
                subcategories_name: "Condensed Matter (cond-mat)",
                subcategories_recentLink: "#",
                subcategories_searchLink: "#",
              },
              {
                subcategories_name: "General Relativity and Quantum Cosmology (gr-qc)",
                subcategories_recentLink: "#",
                subcategories_searchLink: "#",
              }
            ],
          }
        ],
      };
    },

    methods: {
      performSearch() {
        // This is where the search logic would go
        console.log(`Searching for "${this.searchQuery}" in ${this.selectedField}`);
      }
    }

  };
</script>












<style scoped>
  
  .container {
    /* max-width: 900px; */
    /* margin: 0 auto; */
    font-family: Arial, sans-serif;
  }

  h3 {
    font-family: Arial;
    font-size: 15px; /* Increase the size */
    text-align: left; /* Center it on the page */
    color: #06080e; /* Change the color */
    margin-top: 10px; /* Add some space below the title */
    margin-bottom: 10px; /* Add some space below the title */
    letter-spacing: 0px; /* Add some spacing between letters */
  }

  .search-bar {
    display: flex;
    align-items: center;
    background-color: #ffffff; /* Red background color */
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
    text-decoration: none;
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

  /* Table of content style */

  h1 {
    font-size: 24px;
    color: #333;
  }

  h2 {
    font-size: 20px;
    color: #555;
  }

  ul {
    list-style-type: none;
    padding-left: 0;
  }

  li {
    margin: 5px 0;
  }

</style>
