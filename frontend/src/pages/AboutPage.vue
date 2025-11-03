<template>
  <div class="about-page">
    <!-- Hero -->
    <section class="hero">
      <h1>Sobre Guías Púrpuras</h1>
      <p>
        El futuro es ahora: conectamos a Bolivia desde lo profesional, laboral, gastronómico y empresarial,
        ordenando el caos digital y potenciando la visibilidad local.
      </p>
    </section>

    <!-- Propósito -->
    <section class="purpose">
      <va-card outlined>
        <va-card-title>
          <va-icon name="emoji_objects" color="warning" size="large" />
          <span class="ml-2">Nuestro Propósito</span>
        </va-card-title>
        <va-card-content>
          <p>
            Creemos que Bolivia está llena de talento, esfuerzo y creatividad. Pero ese potencial
            muchas veces se pierde en el ruido de redes caóticas y plataformas impersonales.
            Guías Púrpuras nace para dar orden, diseño y propósito al mundo digital boliviano.
          </p>
        </va-card-content>
      </va-card>
    </section>

    <!-- Misión, Visión, Valores -->
    <section class="values">
      <va-card v-for="(item, i) in valores" :key="i" outlined>
        <va-card-title>
          <va-icon :name="item.icon" color="primary" size="large" />
          <span class="ml-2">{{ item.titulo }}</span>
        </va-card-title>
        <va-card-content>
          <p>{{ item.texto }}</p>
        </va-card-content>
      </va-card>
    </section>
   
</div>
</template>

<script setup>
const valores = [
  { titulo: "Misión", texto: "Dar visibilidad a profesionales y negocios bolivianos.", icon: "flag" },
  { titulo: "Visión", texto: "Ser la plataforma líder de conexión y oportunidades en Bolivia.", icon: "visibility" },
  { titulo: "Valores", texto: "Transparencia, innovación y compromiso local.", icon: "favorite" },
]


</script>

<style scoped>
.about-page {
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
  font-size: 2.8rem;
  margin-bottom: 1rem;
}
.hero p {
  font-size: 1.2rem;
  max-width: 800px;
  margin: auto;
}

/* Purpose */
.purpose {
  margin-bottom: 3rem;
}

/* Valores */
.values {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

/* Cómo funciona */
.how-it-works {
  margin-bottom: 3rem;
  text-align: center;
}
.how-it-works h2 {
  font-size: 2rem;
  color: #6a1b9a;
  margin-bottom: 1rem;
}
.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

/* Ecosistema */
.ecosystem {
  margin-bottom: 3rem;
  text-align: center;
}
.ecosystem h2 {
  font-size: 2rem;
  color: #6a1b9a;
  margin-bottom: 1rem;
}
.ecosystem-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}
</style>
