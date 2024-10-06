<template>
    <div class="md:grid md:grid-cols-3 md:gap-8 flex flex-col">
        <div v-for="article in articles" :key="article.id" class="">
          <!-- const props = defineProps(['id', 'title', 'subject', 'description', 'author', 'date_published']) -->
            <Tarjeta :id="article.id" :title="article.title" :subject="article.subject" :description="article.description" :author="article.author" :date_published="article.date_published" />
        </div>
    </div>
</template>

<script>
import Tarjeta from './Tarjeta.vue';
import articlesData from '../assets/data.json';
export default {
    components: {
        Tarjeta
    },
    data() {
    return {
      articles: []
    };
  },
  mounted() {
    // Assign the imported JSON data to the component's data property
    this.articles = articlesData;
  }
}
</script>