<template>
  <div class="blog-page">
    <!-- Hero -->
    <section class="hero">
      <h1>Blog de Guías Púrpuras</h1>
      <p>
        Historias, consejos y tendencias para potenciar tu presencia digital en Bolivia.
      </p>
    </section>

    <!-- Grid de Posts -->
    <section class="posts">
      <div class="posts-grid">
        <va-card
          v-for="(post, i) in posts"
          :key="i"
          outlined
          class="post-card"
        >
          <img :src="post.image" alt="" class="post-img" />
          <va-card-title>{{ post.title }}</va-card-title>
          <va-card-content>
            <p>{{ post.excerpt }}</p>
          </va-card-content>
          <va-card-actions>
            <va-button color="primary" class="btn-read">Leer más</va-button>
          </va-card-actions>
        </va-card>
      </div>
    </section>
  </div>
</template>

<script setup>
const posts = [
  {
    title: "Cómo destacar tu negocio online",
    excerpt: "Tips prácticos para mejorar tu visibilidad en el ecosistema digital boliviano...",
    image: "https://via.placeholder.com/400x200",
  },
  {
    title: "Tendencias gastronómicas en Bolivia",
    excerpt: "Lo que está marcando la pauta en 2025 para restaurantes y foodtrucks...",
    image: "https://via.placeholder.com/400x200",
  },
  {
    title: "Guía para profesionales independientes",
    excerpt: "Construye tu reputación digital paso a paso con estrategias efectivas...",
    image: "https://via.placeholder.com/400x200",
  },
  {
    title: "El futuro del trabajo en Bolivia",
    excerpt: "Cómo las plataformas digitales están transformando la búsqueda de empleo...",
    image: "https://via.placeholder.com/400x200",
  },
]
</script>

<style scoped>
.blog-page {
  padding: 2rem;
  max-width: 1200px;
  margin: auto;
}

/* Hero */
.hero {
  background: linear-gradient(135deg, #6a1b9a, #fdd835);
  color: white;
  text-align: center;
  padding: 4rem 2rem;
  border-radius: 12px;
  margin-bottom: 3rem;
}
.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}
.hero p {
  font-size: 1.2rem;
  max-width: 800px;
  margin: auto;
}

/* Posts */
.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}
.post-card {
  transition: transform 0.2s, box-shadow 0.2s, border 0.2s;
  border-radius: 12px;
  overflow: hidden;
}
.post-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
  border: 2px solid #fdd835;
}
.post-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}
.btn-read {
  background: linear-gradient(135deg, #6a1b9a, #fdd835);
  color: white;
  font-weight: 600;
}
</style>
