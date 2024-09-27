<template>


<div class="container">
  <h2> 
    El Repositorio Salvadoreño de Ciencia (RSC) es una plataforma dedicada a la difusion gratuita de artículos científicos realizados por investigadores salvadoreños. Este repositorio permite que la ciencia producida en El Salvador sea visible y accesible tanto a nivel local como internacional. Los temas abarcan desde las ciencias naturales, ingeniería, ciencias sociales y otros campos del conocimiento, y buscan promover la colaboración y difusión de la ciencia hecha en El Salvador.
</h2>
</div>



<!-- SEARCH BAR -->
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


  <div class="category-index">
    <ul>
      <li v-for="(category, index) in categories" :key="index">
        {{ category.name }}
        <span class="links">
          (<a :href="category.newLink">new</a>, 
          <a :href="category.recentLink">recent</a>, 
          <a :href="category.searchLink">search</a>)
        </span>
        <span v-if="category.subcategories.length">
          {{ category.subcategories }}
        </span>
      </li>
    </ul>
  </div>


<div class="container">

    <h1> Abril 2024 </h1>
    <div v-for="(article, index) in articles" :key="index" class="article">
      <p>
        <strong><a :href="article.link">{{ article.id }}</a></strong>
        [<a :href="article.pdfLink">pdf</a>, <a :href="article.htmlLink">html</a>, <a :href="article.otherLink">other</a>]
      </p>
      <h2 class="article-title">{{ article.title }}</h2>
      <p class="authors">{{ article.authors }}</p>
      <p class="comments">{{ article.comments }}</p>
      <p class="subject"><strong>Subjects:</strong> {{ article.subjects }}</p>
    </div>

    <h1> Marzo 2024 </h1>
    <div v-for="(article, index) in articles" :key="index" class="article">
      <p>
        <strong><a :href="article.link">{{ article.id }}</a></strong>
        [<a :href="article.pdfLink">pdf</a>, <a :href="article.htmlLink">html</a>, <a :href="article.otherLink">other</a>]
      </p>
      <h2 class="article-title">{{ article.title }}</h2>
      <p class="authors">{{ article.authors }}</p>
      <p class="comments">{{ article.comments }}</p>
      <p class="subject"><strong>Subjects:</strong> {{ article.subjects }}</p>
    </div>
   
    <h1> Febrero 2024 </h1>
    <div v-for="(article, index) in articles" :key="index" class="article">
      <p>
        <strong><a :href="article.link">{{ article.id }}</a></strong>
        [<a :href="article.pdfLink">pdf</a>, <a :href="article.htmlLink">html</a>, <a :href="article.otherLink">other</a>]
      </p>
      <h2 class="article-title">{{ article.title }}</h2>
      <p class="authors">{{ article.authors }}</p>
      <p class="comments">{{ article.comments }}</p>
      <p class="subject"><strong>Subjects:</strong> {{ article.subjects }}</p>
    </div>
</div>


</template>






<script>
export default {
  data() {
    return {
      searchQuery: '',
      selectedField: 'All fields',

      categories: [
        {
          name: "Astrophysics (astro-ph)",
          newLink: "#",
          recentLink: "#",
          searchLink: "#",
          subcategories: "Astrophysics of Galaxies; Cosmology and Nongalactic Astrophysics; Earth and Planetary Astrophysics"
        },
        {
          name: "Condensed Matter (cond-mat)",
          newLink: "#",
          recentLink: "#",
          searchLink: "#",
          subcategories: "Disordered Systems and Neural Networks; Materials Science; Superconductivity"
        },
        {
          name: "General Relativity and Quantum Cosmology (gr-qc)",
          newLink: "#",
          recentLink: "#",
          searchLink: "#",
          subcategories: ""
        },
        {
          name: "High Energy Physics - Experiment (hep-ex)",
          newLink: "#",
          recentLink: "#",
          searchLink: "#",
          subcategories: ""
        },
        {
          name: "High Energy Physics - Lattice (hep-lat)",
          newLink: "#",
          recentLink: "#",
          searchLink: "#",
          subcategories: ""
        },
        {
          name: "High Energy Physics - Phenomenology (hep-ph)",
          newLink: "#",
          recentLink: "#",
          searchLink: "#",
          subcategories: ""
        },
        {
          name: "High Energy Physics - Theory (hep-th)",
          newLink: "#",
          recentLink: "#",
          searchLink: "#",
          subcategories: ""
        },
        {
          name: "Mathematical Physics (math-ph)",
          newLink: "#",
          recentLink: "#",
          searchLink: "#",
          subcategories: ""
        },
        {
          name: "Nonlinear Sciences (nlin)",
          newLink: "#",
          recentLink: "#",
          searchLink: "#",
          subcategories: "Adaptation and Self-Organizing Systems; Chaotic Dynamics; Exactly Solvable and Integrable Systems"
        },
        {
          name: "Nuclear Theory (nucl-th)",
          newLink: "#",
          recentLink: "#",
          searchLink: "#",
          subcategories: ""
        },
        {
          name: "Physics (physics)",
          newLink: "#",
          recentLink: "#",
          searchLink: "#",
          subcategories: "Accelerator Physics; Applied Physics; Atomic and Molecular Clusters; Instrumentation and Detectors"
        },
        {
          name: "Quantum Physics (quant-ph)",
          newLink: "#",
          recentLink: "#",
          searchLink: "#",
          subcategories: ""
        }
      ],




      articles: [
        {
          id: "RSC:2407.00151",
          title: "Charged Static AdS Black Hole Binaries",
          authors: "William D. Biggs, Jorge E. Santos",
          comments: "17 pages (incl. appendices), 8 figures",
          subjects: "High Energy Physics - Theory (hep-th); General Relativity and Quantum Cosmology (gr-qc)",
          link: "#",
          pdfLink: "#",
          htmlLink: "#",
          otherLink: "#"
        },
        {
          id: "RSC:2407.00318",
          title: "Landscape of QCD Vacuum",
          authors: "George Savvidy",
          comments: "29 pages, 5 figures",
          subjects: "High Energy Physics - Theory (hep-th); High Energy Physics - Lattice (hep-lat); High Energy Physics - Phenomenology (hep-ph)",
          link: "#",
          pdfLink: "#",
          htmlLink: "#",
          otherLink: "#"
        },
        // Add more articles here
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

h1 {
  font-family: Arial;
  font-weight: bold;
  font-size: 24px; /* Increase the size */
  text-align: left; /* Center it on the page */
  color: #132966; /* Change the color */
  margin-top: 20px; /* Add some space below the title */
  margin-bottom: 5px; /* Add some space below the title */
  letter-spacing: 0px; /* Add some spacing between letters */
}


h2 {
  font-family: Arial;
  font-weight: bold;
  font-size: 15px; /* Increase the size */
  text-align: left; /* Center it on the page */
  color: #06080e; /* Change the color */
  margin-top: 10px; /* Add some space below the title */
  margin-bottom: 10px; /* Add some space below the title */
  letter-spacing: 0px; /* Add some spacing between letters */
}

.article {
  padding: 15px 0;
  border-bottom: 1px solid #ddd;
}

.article-title {
  font-size: 18px;
  font-weight: bold;
  color: #4b0082;
}

.authors {
  font-size: 14px;
  color: #333;
}

.comments {
  font-size: 12px;
  color: #777;
}

.subject {
  font-size: 12px;
  color: #777;
}

p {
  margin: 5px 0;
}

a {
  color: #0066cc;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
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

.links {
  font-size: 12px;
}

.subcategories {
  font-size: 12px;
  color: #555;
  margin-left: 10px;
}

</style>
