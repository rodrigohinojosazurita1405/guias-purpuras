# 📋 ANÁLISIS DETALLADO - PASO 1: INFORMACIÓN DEL TRABAJO

## 📊 ESTADO ACTUAL EVALUADO

### ✅ FORTALEZAS ACTUALES
1. **Estructura Clara**: 5 acordeones bien organizados (Básica, Requisitos, Salario, Vacantes, Contacto)
2. **Validación Robusta**: Sistema de validación completo en el script
3. **Componentes Vuestic**: Uso consistente de componentes de UI framework
4. **Responsive Design**: Media queries para móvil, tablet y desktop
5. **Visual Feedback**: Hints y tips para guiar al usuario
6. **Estado de Datos**: Sincronización en tiempo real con el store padre

---

## ⚠️ PROBLEMAS IDENTIFICADOS

### 1. **DISEÑO VISUAL**
#### Problemas:
- ❌ Header tiene gradiente monótono azul (#F8FAFC → #F1F5F9)
- ❌ Acordeones sin animaciones suaves al abrir/cerrar
- ❌ Inconsistencia de iconos (algunos tienen 1.5rem, otros varían)
- ❌ Fondo blanco de acordeones muy plano
- ❌ Bordes de acordeones grises sin variación

#### Impacto:
- Interfaz percibida como "robótica" y menos moderna
- Falta de jerarquía visual clara
- Difícil identificar qué sección es la activa

---

### 2. **TIPOGRAFÍA**
#### Problemas:
- ❌ `step-title`: 2rem con weight 800 (muy pesado)
- ❌ `step-subtitle`: 0.95rem color #64748B (muy sutil)
- ❌ `accordion-title`: 1.25rem en desktop, 1.1rem mobile (salto brusco)
- ❌ Labels de inputs sin formato consistente
- ❌ Hints con tamaño fijo 0.85rem (pequeño en móvil)

#### Impacto:
- Difícil lectura en pantallas pequeñas
- Jerarquía visual poco clara
- Inconsistencia en familias tipográficas

---

### 3. **ESPACIADO (SPACING)**
#### Problemas:
- ❌ Gaps muy grandes entre secciones (2rem)
- ❌ Padding inconsistente (2.5rem en header, 2rem en contenido, 1.5rem en acordeones)
- ❌ Form-grid con gap 1.5rem (muy grande para inputs pequeños)
- ❌ Mobile: reducción no proporcional de espacios

#### Impacto:
- Desperdicio de espacio en mobile
- Sensación de "separación" excesiva
- Scroll innecesario

---

### 4. **COLORES & DEGRADADOS**
#### Problemas:
- ❌ Fondo: Gradiente azul muy sutil sin contraste
- ❌ Acordeones: Borde #E2E8F0 sin variación de estado
- ❌ Hover: Solo cambia border a #CBD5E1 (muy sutil)
- ❌ Hint boxes: Colores fijos sin jerarquía
- ❌ Falta de micro-interacciones con color

#### Impacto:
- Interfaz percibida como aburrida
- Estados de interacción poco claros
- Difícil identificar elementos interactivos

---

### 5. **COMPONENTES VUESTIC**
#### Problemas:
- ❌ No se aprovechan props disponibles (size, color, variant)
- ❌ va-input sin clear button option
- ❌ va-textarea sin contador visual mejorado
- ❌ va-select sin search/filtrado
- ❌ va-radio sin estilos personalizados
- ❌ Campos sin validación visual en tiempo real

#### Impacto:
- Experiencia de usuario plana
- No se aprovechan características del framework
- UX podría ser más interactiva

---

### 6. **INTERACTIVIDAD & FEEDBACK**
#### Problemas:
- ❌ Acordeón se abre sin transición suave
- ❌ Sin loading states
- ❌ Sin confirmación visual al cambiar valores
- ❌ Hints con fondo color sólido, sin enfoque
- ❌ Salary inputs sin mini-vista previa

#### Impacto:
- Sensación de "click" muerto
- Usuario no sabe si su acción fue registrada
- Experiencia poco pulida

---

### 7. **ESTRUCTURA HTML/ACCESSIBILITY**
#### Problemas:
- ❌ Labels no están correctamente asociados con inputs (missing `for` attribute)
- ❌ Accordion sin ARIA roles (aria-expanded, aria-controls)
- ❌ Sin semantic HTML (missing `<section>`, `<fieldset>`)
- ❌ Iconos sin aria-label
- ❌ Sin skip links o focus management

#### Impacto:
- Accesibilidad reducida para screen readers
- Cumplimiento WCAG bajo
- Experiencia pobre para usuarios con discapacidades

---

## 🎨 PROPUESTAS DE MEJORA DETALLADAS

### MEJORA 1: REDISEÑO DE HEADER
**Prioridad**: 🔴 Alta
**Impacto**: Visual 10/10

#### Cambios Propuestos:
```css
/* ANTES */
background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
border-top: 3px solid #7C3AED;

/* DESPUÉS */
background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
border-top: 4px solid #A855F7;
color: white;
box-shadow: 0 8px 24px rgba(124, 58, 237, 0.2);
```

#### Detalles:
- Cambiar gradiente a púrpura (coincide con marca)
- Texto blanco y emojis blancos
- Mayor sombra para elevar el header
- Icon box permanece igual o con más brillo

#### Resultado:
```
═══════════════════════════════════════
║  [💜] Información del Trabajo        ║
║      Completa los datos...           ║
═══════════════════════════════════════
```

---

### MEJORA 2: ACCORDEONES MÁS VISUALES
**Prioridad**: 🔴 Alta
**Impacto**: Usabilidad 9/10

#### Cambios Propuestos:

##### A) Añadir gradient al header expandido
```css
.accordion-section.expanded .accordion-header {
  background: linear-gradient(90deg, #F9F5FF 0%, rgba(124, 58, 237, 0.05) 100%);
  border-bottom: 2px solid #DDD6FE;
}
```

##### B) Mejorar el icono con animación
```css
.accordion-icon {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #E0E7FF 0%, #DDD6FE 100%);
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.accordion-section.expanded .accordion-icon {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  transform: scale(1.08) rotate(-5deg);
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35);
}
```

##### C) Borde dinámico del acordeón
```css
.accordion-section {
  border: 2px solid #E2E8F0;
  border-left: 4px solid transparent;
  transition: all 0.3s ease;
}

.accordion-section:hover {
  border-left-color: #CBD5E1;
}

.accordion-section.expanded {
  border-left-color: #7C3AED;
  border-color: #DDD6FE;
}
```

#### Resultado Visual:
- Acordeón se "levanta" al expandir
- Icono gira y brilla
- Borde izquierdo cambia de color

---

### MEJORA 3: MEJORAR TIPOGRAFÍA
**Prioridad**: 🟡 Media
**Impacto**: Legibilidad 8/10

#### Cambios Propuestos:

| Elemento | Actual | Propuesto | Motivo |
|----------|--------|-----------|---------|
| step-title | 2rem/800 | 2.2rem/700 | Menos pesado, más elegante |
| step-subtitle | 0.95rem/#64748B | 1rem/#6B7280 | Más legible y visible |
| accordion-title | 1.25rem/700 | 1.3rem/600 | Mejor jerarquía |
| form-row label | Sin etiqueta explícita | 0.95rem/600 | Consistencia |
| input-hint | 0.85rem | 0.9rem | Mejor legibilidad móvil |
| button text | Vuestic default | 1rem/600 | Consistencia |

#### Detalles Específicos:
```css
/* NUEVO: Escala de tipografía consistente */
h1 { font-size: 2.2rem; font-weight: 700; } /* step-title */
h2 { font-size: 1.5rem; font-weight: 600; } /* section titles */
h3 { font-size: 1.3rem; font-weight: 600; } /* accordion-title */
h4 { font-size: 1.1rem; font-weight: 600; } /* form labels */
p { font-size: 1rem; font-weight: 400; } /* body text */
small { font-size: 0.9rem; font-weight: 400; } /* hints */

/* NUEVO: Altura de línea mejorada */
h1, h2, h3, h4 { line-height: 1.3; }
p, small { line-height: 1.6; }
```

---

### MEJORA 4: REFACTORIZAR ESPACIADO
**Prioridad**: 🟡 Media
**Impacto**: UX 8/10

#### Propuesta de Sistema de Espaciado:
```
8px  = 0.5rem  (xs)
12px = 0.75rem (sm)
16px = 1rem    (md)
24px = 1.5rem  (lg)
32px = 2rem    (xl)
48px = 3rem    (2xl)
```

#### Aplicar:
- Header: `padding: 2rem` (simplificar)
- Form-content: `gap: 1.5rem` (reducir de 2rem)
- Form-grid: `gap: 1rem` (reducir de 1.5rem)
- Mobile: 50% de los valores desktop

#### Ejemplo:
```css
.information-step-job {
  padding: 1.5rem; /* reducir de 2rem */
}

.form-content {
  gap: 1.5rem; /* reducir de 2rem */
}

.form-grid {
  gap: 1rem; /* reducir de 1.5rem */
}

@media (max-width: 768px) {
  .information-step-job { padding: 0.75rem; }
  .form-content { gap: 0.75rem; }
}
```

---

### MEJORA 5: SISTEMA DE COLORES MEJORADO
**Prioridad**: 🔴 Alta
**Impacto**: Diseño 9/10

#### Nueva Paleta:
```css
/* Primarios */
:root {
  --color-primary-50: #F9F5FF;   /* lightest */
  --color-primary-100: #F3E8FF;
  --color-primary-500: #7C3AED;  /* main */
  --color-primary-600: #6D28D9;
  --color-primary-700: #5B21B6;  /* darkest */

  /* Secundarios */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-danger: #EF4444;

  /* Neutral */
  --color-gray-50: #F9FAFB;
  --color-gray-100: #F3F4F6;
  --color-gray-400: #9CA3AF;
}
```

#### Cambios en Componentes:
```css
/* Hints Box - Ahora con más variedad */
.input-hint {
  background: var(--color-primary-50);
  border-left: 3px solid var(--color-primary-500);
  color: var(--color-primary-700);
}

.input-hint.success {
  background: #ECFDF5;
  border-left-color: var(--color-success);
  color: #047857;
}

.input-hint.warning {
  background: #FEF3C7;
  border-left-color: var(--color-warning);
  color: var(--color-warning);
}

/* Accordion - Transición de color al expandir */
.accordion-section {
  transition: all 0.3s ease;
}

.accordion-section.expanded {
  background: linear-gradient(135deg, white 0%, var(--color-primary-50) 100%);
}
```

---

### MEJORA 6: MEJORAR INPUTS & VALIDACIÓN
**Prioridad**: 🟡 Media
**Impacto**: UX 8/10

#### A) Validación Visual en Tiempo Real
```vue
<template>
  <div class="form-row" :class="{
    'has-error': showError && !value,
    'has-success': showSuccess && value && isValid
  }">
    <va-input
      v-model="localFormData.title"
      label="Título del Puesto"
      :error="showError && !value"
      :error-messages="showError ? ['Campo requerido'] : []"
      @blur="showError = true"
    />
  </div>
</template>

<style scoped>
.form-row.has-error :deep(.va-input) {
  --va-input-border-color: #EF4444;
  --va-input-border-color-focused: #DC2626;
}

.form-row.has-success :deep(.va-input) {
  --va-input-border-color: #10B981;
  --va-input-border-color-focused: #059669;
}
</style>
```

#### B) Mini Preview para Salario
```css
.salary-preview {
  padding: 1rem;
  background: linear-gradient(135deg, #F9F5FF 0%, #F3E8FF 100%);
  border-radius: 8px;
  text-align: center;
  font-weight: 600;
  color: #7C3AED;
  margin-top: 0.5rem;
}

/* Mostrar: Bs. 3,000 - Bs. 5,000 */
```

#### C) Contador mejorado para textarea
```css
.textarea-counter {
  font-size: 0.85rem;
  color: #94A3B8;
  text-align: right;
  margin-top: 0.25rem;
}

.textarea-counter.warning {
  color: #F59E0B;
}

.textarea-counter.error {
  color: #EF4444;
}
```

---

### MEJORA 7: MICROINTERACCIONES
**Prioridad**: 🟢 Baja
**Impacto**: Polish 7/10

#### A) Hover en Vacancy Icons
```css
.vacancy-icon {
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.vacancy-icon:hover {
  transform: scale(1.15) translateY(-2px);
  box-shadow: 0 6px 12px rgba(124, 58, 237, 0.3);
}
```

#### B) Loading State para Validación
```vue
<template>
  <va-button
    preset="primary"
    @click="handleNext"
    :disabled="isValidating"
    :loading="isValidating"
  >
    {{ isValidating ? 'Validando...' : 'Siguiente' }}
  </va-button>
</template>
```

#### C) Transición suave entre datos
```css
.form-row {
  animation: slideInUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

---

### MEJORA 8: ACCESIBILIDAD
**Prioridad**: 🔴 CRÍTICA
**Impacto**: Inclusión 10/10

#### A) Labels asociados correctamente
```html
<!-- ANTES -->
<label>Título del Puesto</label>
<va-input v-model="title" />

<!-- DESPUÉS -->
<label for="job-title">Título del Puesto *</label>
<va-input id="job-title" v-model="title" />
```

#### B) Accordion ARIA
```html
<div
  class="accordion-header"
  role="button"
  tabindex="0"
  :aria-expanded="expandedSections.basicInfo"
  aria-controls="accordion-content-basicInfo"
>
  ...
</div>

<div
  id="accordion-content-basicInfo"
  role="region"
  v-if="expandedSections.basicInfo"
>
  ...
</div>
```

#### C) Form Fieldsets
```html
<fieldset>
  <legend>Información Salarial</legend>
  <!-- radio buttons agrupados -->
</fieldset>
```

---

### MEJORA 9: RESPONSIVE MEJORADO
**Prioridad**: 🟡 Media
**Impacto**: Mobile UX 8/10

#### Propuesta de Breakpoints Refinados:
```css
/* Tablet grande (1024px) */
.form-grid { grid-template-columns: repeat(2, 1fr); }

/* Tablet (768px) */
@media (max-width: 768px) {
  .form-grid { grid-template-columns: 1fr; }
  .accordion-header { padding: 1rem 1.25rem; }
}

/* Mobile (480px) */
@media (max-width: 480px) {
  .step-title { font-size: 1.5rem; }
  .accordion-title { font-size: 1.1rem; }
  .form-grid { gap: 0.75rem; }
}
```

#### Mobile-First para Salary Inputs:
```css
/* Mobile: Stacked */
.salary-inputs {
  flex-direction: column;
  gap: 1rem;
}

.salary-separator {
  display: none;
}

/* Tablet+: Side by side */
@media (min-width: 640px) {
  .salary-inputs {
    flex-direction: row;
    align-items: flex-end;
  }

  .salary-separator {
    display: block;
  }
}
```

---

### MEJORA 10: SKELETON LOADING
**Prioridad**: 🟢 Baja
**Impacto**: UX Perceived 6/10

#### Mostrar skeleton cuando se carga
```css
.skeleton {
  background: linear-gradient(
    90deg,
    #E0E0E0 25%,
    #F0F0F0 50%,
    #E0E0E0 75%
  );
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

---

## 📱 COMPARATIVA DESKTOP vs MOBILE (CON MEJORAS)

### DESKTOP (Actual)
```
┌─────────────────────────────────────────┐
│  [💜] Información del Trabajo           │ Header azul plano
│      Completa los datos...              │
└─────────────────────────────────────────┘
        Padding: 2.5rem | 2.5rem

┌─────────────────────────────────────────┐
│  [📋] Información Básica    [>]         │ Acordeón estático
│      Título - Ciudad (resumen)          │
├─────────────────────────────────────────┤
│ • Título del Puesto                     │
│   [input con 100 chars]                 │
│ • Empresa                               │
│   [input] [Switch Anónimo]              │
└─────────────────────────────────────────┘
```

### MOBILE (Actual)
```
┌──────────────────┐
│ [💜] Información │ Header comprimido
│ Completa...      │
└──────────────────┘

┌──────────────────┐
│ [📋] Información │ Acordeón pequeño
│ Básica  [>]      │
└──────────────────┘
```

### DESKTOP (Propuesto)
```
┌─────────────────────────────────────────┐
│ [💜] Información del Trabajo        ✨  │ Header púrpura
│      Completa los datos de la oferta    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  [📋] Información Básica               ▼│ Acordeón con gradiente
│      "Agonomía - Cochabamba (resumen)"  │
├─────────────────────────────────────────┤
│ • Título del Puesto *                   │ Label mejorado
│   [input] ✓ Campo completado            │
│                                         │
│ • Empresa                               │
│   [input] [Switch Anónimo]              │
│   Esto ocultará el nombre               │ Hint mejorado
└─────────────────────────────────────────┘
```

### MOBILE (Propuesto)
```
┌──────────────────────┐
│[💜]Información Trab. │ Más compacto
│ Completa...          │
└──────────────────────┘

┌──────────────────────┐
│[📋]Info Básica    ▼ │ Mejor espaciado
│ "Agronomía - Coch"  │
├──────────────────────┤
│• Título *            │
│[input] ✓             │ Validación visual
│                      │
│• Empresa             │
│[input]               │
│[Switch]              │
└──────────────────────┘
```

---

## 🎯 RESUMEN DE CAMBIOS POR PRIORIDAD

### 🔴 CRÍTICO (Hacer primero)
1. **Rediseño Header** - Purple gradient + white text
2. **Accesibilidad** - ARIA labels, semantic HTML
3. **Acordeones Visuales** - Animaciones suaves

### 🟡 IMPORTANTE (Segunda oleada)
4. **Tipografía** - Escala consistente
5. **Espaciado** - Sistema 8px
6. **Colores** - Paleta CSS variables

### 🟢 NICE-TO-HAVE (Tercera oleada)
7. **Microinteracciones** - Transiciones suaves
8. **Validación mejorada** - Visual feedback
9. **Skeleton loading** - Loading states
10. **Responsive refinado** - Mobile-first

---

## 💰 ESFUERZO ESTIMADO

| Mejora | Tiempo | Complejidad |
|--------|--------|-------------|
| 1. Header | 30 min | 🟢 Fácil |
| 2. Acordeones | 1 h | 🟡 Medio |
| 3. Tipografía | 45 min | 🟢 Fácil |
| 4. Espaciado | 1 h | 🟡 Medio |
| 5. Colores | 45 min | 🟢 Fácil |
| 6. Inputs | 1.5 h | 🟡 Medio |
| 7. Interacciones | 1.5 h | 🔴 Difícil |
| 8. Accesibilidad | 2 h | 🔴 Difícil |
| 9. Responsive | 1 h | 🟡 Medio |
| 10. Skeleton | 1 h | 🟡 Medio |
|  |  |  |
| **TOTAL** | **~10 h** | **Medio-Alto** |

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [ ] Rediseñar header con gradiente púrpura
- [ ] Mejorar acordeones con animaciones
- [ ] Actualizar tipografía a escala consistente
- [ ] Refactorizar espaciado con sistema 8px
- [ ] Implementar paleta CSS variables
- [ ] Mejorar componentes de input con validación
- [ ] Agregar ARIA labels y semantic HTML
- [ ] Ajustar responsive para mobile
- [ ] Agregar microinteracciones
- [ ] Agregar skeleton loading states

---

## 🚀 SIGUIENTE PASO
¿Cuáles de estas mejoras quieres que implemente primero? Recomiendo:

1. **Header + Acordeones** (Visual impact máximo)
2. **Tipografía + Espaciado** (UX mejorado)
3. **Accesibilidad** (Crítica para compliance)

¿Comenzamos?
