<template>
  <div class="page-container">
    <h1 class="title">Contacto</h1>
    <va-card outlined>
      <va-card-content>
        <va-form @submit.prevent="sendMessage">
          <va-input v-model="form.name" label="Nombre" required />
          <va-input v-model="form.email" label="Correo" type="email" required />
          <va-textarea v-model="form.message" label="Mensaje" required />
          <div class="mt-4">
            <va-button type="submit" color="primary">Enviar</va-button>
          </div>
        </va-form>
      </va-card-content>
    </va-card>
  </div>
</template>

<script setup>
import { ref } from "vue"

const form = ref({ name: "", email: "", message: "" })

function sendMessage() {
  console.log("Mensaje enviado:", form.value)
  // Aquí conectas con tu backend Django (API POST /contact)
}
</script>

<style scoped>
.page-container {
  padding: 2rem;
  max-width: 600px;
  margin: auto;
}
.title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #6a1b9a;
}
</style>
