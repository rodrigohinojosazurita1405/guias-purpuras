# 📊 ANÁLISIS DETALLADO - InformationStepJob.vue
## Componente: Paso 1 - Información del Trabajo

**Fecha**: 2025-11-24
**Estado Actual**: Funcional ✅ | Necesita Mejoras visuales 🎨
**Prioridad**: ALTA (UI/UX mejorado)

---

## 🎯 RESUMEN EJECUTIVO

El componente `InformationStepJob.vue` es **funcional y completo** pero presenta **deficiencias visuales importantes**:

- ❌ Diseño genérico (falta identidad visual púrpura)
- ❌ Tipografía inconsistente y pesada
- ❌ Espaciado excesivo e ineficiente
- ❌ Acordeones sin animaciones suaves
- ❌ Contraste visual insuficiente entre secciones
- ❌ Mobile: Poor UX experience
- ⚠️ Inputs sin validación visual progresiva

---

## 📋 ÍNDICE DE PROBLEMAS IDENTIFICADOS

1. **Estructura Visual & Layout** (5 problemas)
2. **Tipografía & Textos** (6 problemas)
3. **Colores & Degradados** (4 problemas)
4. **Espaciado & Padding** (5 problemas)
5. **Componentes Vuestic** (5 problemas)
6. **Acordeones** (4 problemas)
7. **Validación & Feedback** (4 problemas)
8. **Responsive Design** (3 problemas)
9. **Interactividad** (3 problemas)
10. **Accesibilidad** (3 problemas)

---

## ❌ PROBLEMAS DETALLADOS

### 1️⃣ ESTRUCTURA VISUAL & LAYOUT

#### 🔴 Problema 1.1: Fondo Genérico Sin Identidad
**Ubicación**: `.information-step-job` (línea 938-943)
```css
background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
```

**Análisis**:
- Gradiente azul GRIS muy sutil y frío
- NO representa marca púrpura de Guías Púrpuras
- Parece un formulario de banco/admin, no de plataforma moderna
- Baja diferenciación visual con respecto a otros pasos

**Impacto**: Visual 3/10 | Brand Recognition 1/10

**Propuesta de Mejora**:
```css
background: linear-gradient(135deg, #F9F5FF 0%, #F3E8FF 100%);
/* o más dramático */
background: linear-gradient(135deg, #FAF8FF 0%, #F4EDFF 100%);
```
Resultado: Fondo apenas visible pero reconocible como púrpura

---

#### 🔴 Problema 1.2: Header sin Elevación Visual
**Ubicación**: `.step-header` (línea 945-959)

**Análisis**:
- Box-shadow suave pero insuficiente
- Border-top sólo 3px (muy tenue)
- El header se funde con el fondo
- Estructura: icono + texto muy básica

**Propuesta de Mejora**:
```css
.step-header {
  /* Cambiar shadow */
  box-shadow: 0 8px 32px rgba(124, 58, 237, 0.15);  /* de 0 4px 20px */

  /* Agregar border gradiente */
  border-top: 4px solid transparent;
  background-image:
    linear-gradient(white, white),
    linear-gradient(90deg, #7C3AED, #A855F7);
  background-origin: border-box;
  background-clip: padding-box, border-box;
}

/* Efecto Glassmorphism en móvil */
@media (max-width: 768px) {
  background: rgba(249, 245, 255, 0.9);
  backdrop-filter: blur(10px);
}
```

---

#### 🔴 Problema 1.3: Separación Débil Header/Form
**Ubicación**: Entre `.step-header` y `.form-content` (línea 994)

**Análisis**:
- Ambos tienen padding y margen similar (2.5rem / 2rem)
- No hay visual separation clara
- Genera confusión espacial

**Propuesta**:
```css
.information-step-job {
  padding: 1.5rem;  /* reducir de 2rem */
}

.step-header {
  margin-bottom: 1.5rem;  /* reducir de 2.5rem */
  gap: 1rem;  /* reducir de 1.5rem */
}

.form-content {
  margin-top: 1rem;  /* Agregar espaciador negativo */
}
```

---

#### 🔴 Problema 1.4: Form Content Max-Width Inconsistente
**Ubicación**: `.form-content` (línea 996)

**Análisis**:
- Max-width: 1100px
- Pero paso anterior (PlanStep) tiene 900px
- Genera inconsistencia entre pasos
- En desktop queda muy ancho

**Propuesta**:
```css
max-width: 1000px;  /* ajustar a arquitectura general */
```

---

#### 🔴 Problema 1.5: Sin Contenedor Máximo Exterior
**Ubicación**: Contenedor raíz

**Análisis**:
- `.information-step-job` sin max-width general
- Contenido se expande en pantallas Ultra-wide (> 1920px)
- Desorden visual en 4K

**Propuesta**:
```css
.information-step-job {
  width: 100%;
  max-width: 1440px;  /* AGREGAR */
  margin: 0 auto;      /* AGREGAR */
}
```

---

### 2️⃣ TIPOGRAFÍA & TEXTOS

#### 🔴 Problema 2.1: Step Title Demasiado Pesado
**Ubicación**: `.step-title` (línea 974-980)

**Análisis Actual**:
```css
font-size: 2rem;      /* 32px */
font-weight: 800;     /* Ultra Bold - TOO MUCH */
color: #0F172A;       /* Negro puro */
```

**Problemas**:
- Weight 800 es excesivo (solo para headers de landing)
- Font size 2rem + weight 800 = texto "aplastado"
- Letras se ven gruesas, difíciles de leer
- No deja espacio visual al lado del icono

**Comparativa (Benchmark)**:
```
ACTUAL:   "Información del Trabajo"    [32px, 800]  ← Parece título de banco
PROPUESTO: "Información del Trabajo"    [28px, 700]  ← Moderno y legible
```

**Propuesta de Mejora**:
```css
.step-title {
  font-size: 1.75rem;   /* 28px - reducir de 2rem */
  font-weight: 700;     /* reducir de 800 */
  color: #1E293B;       /* Usar color ligeramente más claro */
  letter-spacing: -0.3px;  /* mantener */
  line-height: 1.3;     /* AGREGAR para mejor legibilidad */
}
```

**Resultado Visual**:
```
ANTES: Información del Trabajo  (pesado, 2rem 800)
DESPUÉS: Información del Trabajo (elegante, 1.75rem 700)
```

---

#### 🔴 Problema 2.2: Step Subtitle Invisible
**Ubicación**: `.step-subtitle` (línea 982-987)

**Análisis Actual**:
```css
font-size: 0.95rem;   /* 15px */
color: #64748B;       /* Gris oscuro - muy sutil */
```

**Problemas**:
- Color #64748B es demasiado gris para estar visible
- Parece un placeholder, no texto importante
- Font size 0.95rem es estándar pero color lo hace invisible

**Propuesta**:
```css
.step-subtitle {
  font-size: 1rem;        /* aumentar a 16px */
  color: #475569;         /* Más oscuro de #64748B */
  margin: 0.75rem 0 0 0;  /* aumentar gap */
  line-height: 1.6;       /* aumentar legibilidad */
  font-weight: 500;       /* AGREGAR - no bold, pero visible */
}
```

---

#### 🔴 Problema 2.3: Accordion Title Inconsistente
**Ubicación**: `.accordion-title` (línea 1496-1502)

**Análisis**:
```css
font-size: 1.25rem;   /* 20px */
font-weight: 700;     /* Bold - OK */
color: #1E293B;       /* Negro - OK */
```

**Problema**:
- En mobile (línea 1562-1564): se reduce a 1.1rem (17px)
- Brinca de 20px a 17px = cambio jarring (3px)
- Debería ser más suave (19px → 18px)

**Propuesta**:
```css
/* Desktop */
.accordion-title {
  font-size: 1.2rem;      /* 19.2px, reducir de 1.25rem */
  font-weight: 600;       /* reducir de 700 (menos pesado) */
  line-height: 1.4;       /* AGREGAR */
}

/* Mobile */
@media (max-width: 768px) {
  .accordion-title {
    font-size: 1.1rem;    /* 17.6px - más cercano a desktop */
  }
}

@media (max-width: 480px) {
  .accordion-title {
    font-size: 1rem;      /* 16px */
  }
}
```

---

#### 🔴 Problema 2.4: Accordion Summary Demasiado Sutil
**Ubicación**: `.accordion-summary` (línea 1508-1516)

**Análisis**:
```css
font-size: 0.9rem;    /* 14.4px - pequeño */
color: #64748B;       /* Gris - invisible */
overflow: hidden;
text-overflow: ellipsis;
white-space: nowrap;
```

**Problema**:
- Resumen de sección no visible en header colapsado
- Usuario no sabe qué contiene el acordeón
- Color + tamaño = invisible

**Propuesta**:
```css
.accordion-summary {
  font-size: 0.95rem;     /* aumentar a 15.2px */
  color: #7C3AED;         /* Cambiar a PÚRPURA para que sea visible */
  font-weight: 500;       /* AGREGAR */
  margin: 0.25rem 0 0 0;
  max-width: 400px;       /* AGREGAR - limitar ancho */
}
```

---

#### 🔴 Problema 2.5: Form-Row Labels Sin Estilo Consistente
**Ubicación**: Inputs va-input, va-textarea, va-select

**Análisis**:
- Vuestic maneja labels automáticamente
- No hay control consistente sobre:
  - Font size del label
  - Font weight del label
  - Color del label
  - Spacing label-input

**Propuesta - Agregar CSS Global**:
```css
:deep(.va-input__label),
:deep(.va-textarea__label),
:deep(.va-select__label) {
  font-size: 0.95rem !important;
  font-weight: 600 !important;
  color: #1E293B !important;
  letter-spacing: 0.2px !important;
}
```

---

#### 🔴 Problema 2.6: Hints Text Poco Legible
**Ubicación**: `.input-hint` (línea 1068-1079)

**Análisis**:
```css
font-size: 0.85rem;   /* 13.6px - muy pequeño */
color: #475569;       /* Gris */
padding: 0.75rem 1rem;
```

**Problema**:
- Font size 0.85rem es muy pequeño para hints
- En mobile se vuelve prácticamente ilegible
- Color gris sobre fondo #E0E7FF tiene bajo contraste

**Propuesta**:
```css
.input-hint {
  font-size: 0.9rem;     /* aumentar a 14.4px */
  color: #5B21B6;        /* Púrpura oscuro para mejor contraste */
  padding: 0.85rem 1.125rem;  /* ajustar proporcionalmente */
  line-height: 1.5;      /* AGREGAR */
}

.success-hint {
  color: #047857;        /* Verde oscuro */
}
```

---

### 3️⃣ COLORES & DEGRADADOS

#### 🔴 Problema 3.1: Falta Coherencia de Paleta
**Ubicación**: Todo el componente

**Análisis - Colores Actuales Utilizados**:
```
#7C3AED   - Púrpura primario (OK)
#E0E7FF   - Púrpura muy claro (backgrounds)
#DDD6FE   - Púrpura suave (accents)
#F8FAFC   - Gris azulado claro (backgrounds)
#E2E8F0   - Gris claro (borders)
#CBD5E1   - Gris medio (hover states)
#1E293B   - Negro oscuro (text)
#64748B   - Gris (secondary text) ← TOO SUBTLE
#475569   - Gris oscuro (tertiary text)
#F59E0B   - Ámbar (warnings)
```

**Problemas**:
- Demasiados grises (6 tonos diferentes)
- Paleta desorganizada
- Falta púrpura oscuro para contraste
- Ámbar (#F59E0B) sin armonía con púrpura

**Propuesta - Paleta Coherente**:
```css
:root {
  /* Púrpuras (brand) */
  --color-purple-50:   #F9F5FF;
  --color-purple-100:  #F3E8FF;
  --color-purple-500:  #7C3AED;  /* primary */
  --color-purple-600:  #6D28D9;  /* hover */
  --color-purple-700:  #5B21B6;  /* active */
  --color-purple-800:  #4C1D95;  /* dark */

  /* Grises (neutral) */
  --color-gray-50:     #F9FAFB;
  --color-gray-100:    #F3F4F6;
  --color-gray-300:    #D1D5DB;
  --color-gray-400:    #9CA3AF;
  --color-gray-600:    #4B5563;  /* text */
  --color-gray-800:    #1E293B;  /* text-strong */

  /* Semantic */
  --color-success:     #10B981;
  --color-warning:     #FBBF24;  /* ámbar más cálido */
  --color-danger:      #EF4444;
}
```

---

#### 🔴 Problema 3.2: Acordeón Icon Background Sin Suficiente Contraste
**Ubicación**: `.accordion-icon` (línea 1471-1482)

**Análisis**:
```css
background: linear-gradient(135deg, #E0E7FF 0%, #DDD6FE 100%);
color: #7C3AED;
```

**Problema**:
- Fondo muy claro (#E0E7FF) con icono púrpura (#7C3AED)
- Bajo contraste (ratio ~3.5:1, deberían ser ~4.5:1)
- El icono se pierde visualmente

**Propuesta**:
```css
.accordion-icon {
  background: linear-gradient(135deg, #EDE9FE 0%, #DDD6FE 100%);  /* más oscuro */
  color: #6D28D9;  /* púrpura 600 */
}

/* Cuando expandido */
.accordion-section.expanded .accordion-icon {
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  color: white;  /* contraste perfecto */
  box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);  /* aumentar sombra */
}
```

---

#### 🔴 Problema 3.3: Vacancy Buttons sin Jerarquía Color
**Ubicación**: `.vacancy-btn` (línea 1176-1202)

**Análisis**:
```css
color: #7C3AED;        /* púrpura */
border: 2px solid #E2E8F0;  /* gris suave */
background: white;
```

**Problema**:
- Colores desbalanceados (púrpura + gris + blanco)
- Sin estado visual claro
- Disabled state es gris claro #CBD5E1 (barely visible)

**Propuesta**:
```css
.vacancy-btn {
  border: 2px solid #7C3AED;  /* púrpura */
  background: white;
  color: #7C3AED;
  transition: all 0.3s ease;
}

.vacancy-btn:hover:not(:disabled) {
  background: #7C3AED;
  color: white;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.vacancy-btn:disabled {
  border-color: #E2E8F0;
  color: #94A3B8;
}
```

---

#### 🔴 Problema 3.4: Salary Tip Box Colors Débiles
**Ubicación**: `.salary-tip` (línea 1131-1142)

**Análisis**:
```css
background: linear-gradient(135deg, #FEF3C7 0%, #FEE2B8 100%);
border-left: 4px solid #F59E0B;
color: #78350F;  /* marrón oscuro */
```

**Problema**:
- Ámbar (#F59E0B) choca visualmente con púrpura del resto
- Marrón (#78350F) tiene poco contraste
- No armoniza con paleta de diseño

**Propuesta**:
```css
.salary-tip {
  background: linear-gradient(135deg, #F0FDFB 0%, #ECFDFA 100%);  /* verde agua */
  border-left: 4px solid #06B6D4;  /* cyan/turquoise */
  color: #0D7377;  /* verde oscuro */

  /* Alternativamente: usar púrpura con opacity */
  /* background: linear-gradient(135deg, #F9F5FF 0%, #F3E8FF 100%); */
  /* border-left: 4px solid #7C3AED; */
  /* color: #5B21B6; */
}
```

---

### 4️⃣ ESPACIADO & PADDING

#### 🔴 Problema 4.1: Padding Excesivo en Header
**Ubicación**: `.step-header` (línea 953)

**Análisis**:
```css
padding: 2.5rem;  /* 40px en todos lados */
```

**Problema**:
- En mobile (375px), 2.5rem × 2 = 80px de padding
- Deja solo 295px para contenido
- Desperdicia espacio vertical

**Propuesta**:
```css
/* Desktop */
.step-header {
  padding: 2rem;  /* reducir de 2.5rem */
}

/* Mobile */
@media (max-width: 768px) {
  .step-header {
    padding: 1.5rem;  /* reducir de 2.5rem */
  }
}

@media (max-width: 480px) {
  .step-header {
    padding: 1.25rem;  /* reducir más */
  }
}
```

---

#### 🔴 Problema 4.2: Gap Excesivo entre Acordeones
**Ubicación**: `.form-content` (línea 992)

**Análisis**:
```css
gap: 2rem;  /* 32px entre acordeones */
margin-bottom: 1.5rem;  /* accordion-section margin */
```

**Combinación**:
- Gap 2rem + margin 1.5rem = 3.5rem de espacio
- Visual separation exagerada
- Crea "agujeros" en la página

**Propuesta**:
```css
.form-content {
  gap: 1.25rem;  /* reducir de 2rem */
}

.accordion-section {
  margin-bottom: 0;  /* remover margin-bottom ya que gap lo maneja */
}
```

---

#### 🔴 Problema 4.3: Accordion Content Padding Desequilibrado
**Ubicación**: `.accordion-content` (línea 1530-1533)

**Análisis**:
```css
padding: 2rem;  /* igual en todos lados */
```

**Problema**:
- En mobile (480px): 2rem × 2 = 64px de padding
- Deja 416px para inputs
- Inputs de texto necesitan más espacio horizontal
- Desbalanceado para mobile

**Propuesta**:
```css
/* Desktop */
.accordion-content {
  padding: 2rem;
}

/* Tablet */
@media (max-width: 768px) {
  .accordion-content {
    padding: 1.5rem;  /* reducir */
  }
}

/* Mobile */
@media (max-width: 480px) {
  .accordion-content {
    padding: 1rem 1.25rem;  /* vertical menos que horizontal */
  }
}
```

---

#### 🔴 Problema 4.4: Form Grid Gap Inconsistente
**Ubicación**: `.form-grid` (línea 1047-1051)

**Análisis**:
```css
grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
gap: 1.5rem;
```

**Problema**:
- Gap 1.5rem es mucho para 2 columnas pequeñas
- En tablet 2 cols + 1.5rem = mucho espacio
- Inputs se ven separados

**Propuesta**:
```css
.form-grid {
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.25rem;  /* reducir de 1.5rem */
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
```

---

#### 🔴 Problema 4.5: Form Row Gap Sin Proporción
**Ubicación**: `.form-row` (línea 1041-1045)

**Análisis**:
```css
gap: 0.75rem;  /* 12px entre label y input */
```

**Problema**:
- 0.75rem es la mitad estándar
- Debería coincidir con form-grid (1.5rem reducido)
- Sin jerarquía de espacios

**Propuesta**:
```css
.form-row {
  gap: 0.5rem;  /* reducir a 8px */
}

/* Entre secciones */
.form-row + .form-row {
  margin-top: 1.25rem;  /* espacio vertical entre filas */
}
```

---

### 5️⃣ COMPONENTES VUESTIC

#### 🔴 Problema 5.1: Va-Input sin Variantes de Validación
**Ubicación**: Todos los va-input

**Análisis**:
```vue
<va-input
  v-model="localFormData.title"
  label="Título del Puesto"
  placeholder="Ej: ..."
  required-mark
  counter
  maxlength="100"
  :rules="[...]"
/>
```

**Problemas**:
- Rules se validan pero no hay feedback visual
- Sin color rojo en hover/invalid
- Sin check verde en valid
- Usuario no sabe si campo es válido hasta enviar

**Propuesta - Agregar Validación Visual**:
```vue
<div class="form-field" :class="{ 'has-error': fieldErrors.title, 'has-success': fieldSuccess.title }">
  <va-input
    v-model="localFormData.title"
    label="Título del Puesto"
    placeholder="Ej: ..."
    required-mark
    counter
    maxlength="100"
    :error="fieldErrors.title"
    :error-messages="fieldErrors.title ? ['Campo requerido'] : []"
    :rules="[...]"
    @blur="validateField('title')"
  >
    <template #append v-if="fieldSuccess.title">
      <va-icon name="check_circle" color="success" />
    </template>
  </va-input>
</div>
```

CSS:
```css
.form-field.has-error :deep(.va-input) {
  --va-input-border-color: #EF4444;
  --va-input-border-color-focused: #DC2626;
}

.form-field.has-success :deep(.va-input) {
  --va-input-border-color: #10B981;
  --va-input-border-color-focused: #059669;
}
```

---

#### 🔴 Problema 5.2: Va-Textarea sin Indicador Visual de Largo
**Ubicación**: `.requirements`, `.description`, etc.

**Análisis**:
```vue
<va-textarea
  v-model="localFormData.description"
  counter
  maxlength="1000"
/>
```

**Problemas**:
- Counter no es visible a primera vista
- Usuario no sabe progreso de escritura
- No hay advertencia visual en 80% de límite

**Propuesta**:
```vue
<div class="textarea-wrapper">
  <va-textarea
    v-model="localFormData.description"
    counter
    maxlength="1000"
  />
  <div class="textarea-indicator">
    <div class="indicator-bar"
         :style="{ width: (description.length / 1000) * 100 + '%' }"
         :class="{ 'warning': description.length > 800 }">
    </div>
    <small>{{ description.length }} / 1000</small>
  </div>
</div>
```

CSS:
```css
.textarea-wrapper {
  position: relative;
}

.textarea-indicator {
  margin-top: 0.5rem;
}

.indicator-bar {
  height: 4px;
  background: linear-gradient(90deg, #7C3AED, #A855F7);
  border-radius: 2px;
  transition: width 0.2s ease;
}

.indicator-bar.warning {
  background: linear-gradient(90deg, #F59E0B, #DC2626);
}
```

---

#### 🔴 Problema 5.3: Va-Radio sin Estilos Personalizados
**Ubicación**: Salary options (línea 355-376)

**Análisis**:
```vue
<va-radio
  v-model="localFormData.salaryType"
  option="range"
  label="Rango salarial específico"
/>
```

**Problemas**:
- Radio por defecto es pequeño y gris
- Difícil de ver en mobile
- Sin hover visual
- Etiqueta no es clickeable

**Propuesta - Hacer Cards Clicables**:
```vue
<div class="salary-option-group">
  <div
    v-for="option in salaryOptions"
    :key="option.value"
    class="salary-option"
    :class="{ 'active': localFormData.salaryType === option.value }"
    @click="localFormData.salaryType = option.value"
  >
    <input
      type="radio"
      :value="option.value"
      v-model="localFormData.salaryType"
      :id="`salary-${option.value}`"
    />
    <label :for="`salary-${option.value}`">
      <strong>{{ option.label }}</strong>
      <small>{{ option.description }}</small>
    </label>
  </div>
</div>
```

CSS:
```css
.salary-option {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border: 2px solid #E2E8F0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.salary-option:hover {
  border-color: #7C3AED;
  background: #F9F5FF;
}

.salary-option.active {
  border-color: #7C3AED;
  background: #F3E8FF;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
}

.salary-option input {
  margin-top: 2px;
  cursor: pointer;
}

.salary-option label {
  flex: 1;
  cursor: pointer;
}
```

---

#### 🔴 Problema 5.4: Va-Select sin Icono Visual de Selección
**Ubicación**: Categoría, Ciudad, Tipo Contrato

**Análisis**:
- Select por defecto Vuestic es funcional pero genérico
- Sin preview visual de selección
- En mobile: difícil de distinguir

**Propuesta**:
```vue
<div class="select-wrapper">
  <va-select
    v-model="localFormData.jobCategory"
    label="Categoría/Área"
    :options="categoryOptions"
    :track-by="(option) => option.value"
  >
    <template #prepend>
      <va-icon name="category" color="purple" />
    </template>
    <template #selection="{ option }">
      <span class="select-preview">
        {{ option.text }}
        <va-icon name="check" size="small" class="check-icon" />
      </span>
    </template>
  </va-select>
</div>
```

CSS:
```css
.select-preview {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.check-icon {
  color: #10B981;
}
```

---

#### 🔴 Problema 5.5: Va-Button sin Variantes Estado
**Ubicación**: Botones "Atrás" y "Siguiente"

**Análisis**:
```vue
<va-button preset="secondary" icon="arrow_back">
  Atrás
</va-button>
<va-button preset="primary" icon="arrow_forward">
  Siguiente
</va-button>
```

**Problemas**:
- Sin loading state (mientras valida)
- Sin disabled state (si faltan campos)
- Sin confirmation feedback

**Propuesta**:
```vue
<div class="navigation-buttons">
  <va-button
    preset="secondary"
    icon="arrow_back"
    @click="handleBack"
    :disabled="isLoading"
  >
    Atrás
  </va-button>

  <va-button
    preset="primary"
    icon="arrow_forward"
    @click="handleNext"
    :loading="isLoading"
    :disabled="!isFormValid"
    class="next-button"
  >
    {{ isLoading ? 'Validando...' : 'Siguiente' }}
  </va-button>
</div>
```

---

### 6️⃣ ACORDEONES

#### 🔴 Problema 6.1: Accordion sin Transición Suave
**Ubicación**: `.accordion-content` (línea 1532)

**Análisis**:
```css
animation: accordionSlideDown 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

**Problema**:
- Transición de contenido OK
- Pero falta transición del height
- Se abre "abrupto"

**Propuesta**:
```css
.accordion-section {
  max-height: 0;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);  /* easing más suave */
}

.accordion-section.expanded {
  max-height: 3000px;  /* valor grande suficiente */
  transition: max-height 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.accordion-content {
  animation: accordionSlideDown 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

#### 🔴 Problema 6.2: Accordion Header sin Ripple/Feedback
**Ubicación**: `.accordion-header` (línea 1435-1449)

**Análisis**:
```css
transition: all 0.3s ease;
.accordion-header:hover {
  background: #F8FAFC;
}
```

**Problema**:
- Hover muy sutil (apenas visible)
- Sin efecto de "click"
- No parece interactive

**Propuesta**:
```css
.accordion-header {
  position: relative;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
}

.accordion-header::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(124, 58, 237, 0.15) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
  pointer-events: none;
}

.accordion-header:hover::before {
  width: 300px;
  height: 300px;
}

.accordion-header:hover {
  background: #F9F5FF;
  cursor: pointer;
}
```

---

#### 🔴 Problema 6.3: Accordion Icon sin Suficiente Animación
**Ubicación**: `.accordion-icon` (línea 1471-1489)

**Análisis**:
```css
transform: scale(1.05);  /* solo en expanded */
transition: all 0.3s ease;
```

**Problema**:
- Scale 1.05 es muy sutil
- Sin rotación
- Sin cambio de posición

**Propuesta**:
```css
.accordion-icon {
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.accordion-section.expanded .accordion-icon {
  transform: scale(1.12) translateY(-2px);  /* scale mayor + float */
  background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
  box-shadow: 0 8px 24px rgba(124, 58, 237, 0.35);  /* sombra mayor */
}
```

---

#### 🔴 Problema 6.4: Chevron Icon sin Animación Suave
**Ubicación**: `.accordion-chevron` (línea 1518-1527)

**Análisis**:
```css
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
transform: rotate(180deg);
```

**Problema**:
- Rotación 180deg OK pero easing genérico
- Sin spring/bounce effect
- Parece mecánico

**Propuesta**:
```css
.accordion-chevron {
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  color: #94A3B8;
}

.accordion-section.expanded .accordion-chevron {
  transform: rotate(180deg) scale(1.1);  /* agregar scale */
  color: #7C3AED;
}
```

---

### 7️⃣ VALIDACIÓN & FEEDBACK

#### 🔴 Problema 7.1: Validación Alert Modal Arcaica
**Ubicación**: `validate()` function (línea 921-922)

**Análisis**:
```javascript
alert(`⚠️ Por favor completa los siguientes campos:\n\n• ${errorMessage}`)
```

**Problema**:
- `alert()` es feo y bloquea UI
- No es responsive
- No se puede styling
- Experiencia 2005

**Propuesta**:
```javascript
// Usar Vuestic notification
const showValidationError = (errors) => {
  const message = errors.join('\n')

  useToast().init({
    message: `⚠️ Por favor completa:\n${message}`,
    color: 'danger',
    position: 'top-end',
    duration: 5000,
    closeable: true
  })
}
```

---

#### 🔴 Problema 7.2: Sin Validación en Tiempo Real
**Ubicación**: Script section

**Análisis**:
- Solo valida en handleNext()
- Sin validación mientras escribe
- Usuario no sabe si está correcto

**Propuesta**:
```javascript
const validateField = (fieldName) => {
  const field = localFormData.value[fieldName]

  const validators = {
    title: (v) => v && v.length >= 5,
    email: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v),
    whatsapp: (v) => /^[67]\d{7}$/.test(v),
    // ...
  }

  fieldErrors.value[fieldName] = !validators[fieldName](field)
  fieldSuccess.value[fieldName] = validators[fieldName](field)
}

// En template
@blur="validateField('title')"
@input="validateField('title')"
```

---

#### 🔴 Problema 7.3: Sin Indicador de Progreso de Validación
**Ubicación**: No existe

**Análisis**:
- Componente largo con muchos campos
- Usuario no sabe cuántos campos necesita completar
- Sin progress indicator

**Propuesta**:
```vue
<div class="validation-progress">
  <div class="progress-bar">
    <div class="progress-fill" :style="{ width: completionPercentage + '%' }"></div>
  </div>
  <small>{{ completedFields }} / {{ totalFields }} campos completados</small>
</div>
```

CSS:
```css
.validation-progress {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #F9FAFB;
  border-radius: 8px;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: #E2E8F0;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #7C3AED, #A855F7);
  transition: width 0.3s ease;
}
```

---

#### 🔴 Problema 7.4: Sin Confirmación Visual Post-Envío
**Ubicación**: handleNext() (línea 832-835)

**Análisis**:
```javascript
const handleNext = () => {
  if (validate()) {
    emit('next')
  }
}
```

**Problema**:
- Al hacer click "Siguiente" no hay feedback
- Usuario no sabe si se está procesando
- Pantalla se queda igual

**Propuesta**:
```javascript
const isLoading = ref(false)

const handleNext = async () => {
  if (!validate()) return

  isLoading.value = true

  try {
    // Simular validación/guardado
    await new Promise(resolve => setTimeout(resolve, 300))

    // Success
    useToast().init({
      message: '✅ Información guardada correctamente',
      color: 'success',
      duration: 2000
    })

    emit('next')
  } finally {
    isLoading.value = false
  }
}
```

---

### 8️⃣ RESPONSIVE DESIGN

#### 🔴 Problema 8.1: Header No Adapta Bien en Mobile
**Ubicación**: @media 768px (línea 1283-1302)

**Análisis**:
```css
@media (max-width: 768px) {
  .step-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
}
```

**Problema**:
- Text-align center funciona
- Pero no reduce tamaño de iconos
- Header sigue tomando mucho espacio

**Propuesta**:
```css
@media (max-width: 768px) {
  .step-header {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
    padding: 1.5rem;
  }

  .header-icon {
    width: 56px;
    height: 56px;
  }

  .step-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .step-header {
    padding: 1rem;
    gap: 0.5rem;
  }

  .header-icon {
    width: 48px;
    height: 48px;
  }

  .step-title {
    font-size: 1.25rem;
  }
}
```

---

#### 🔴 Problema 8.2: Salary Inputs Layout Pobre en Mobile
**Ubicación**: `.salary-inputs` (línea 1154-1158)

**Análisis**:
```css
.salary-inputs {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
}

@media (max-width: 768px) {
  .salary-inputs {
    flex-direction: column;
    align-items: stretch;
  }
}
```

**Problema**:
- En mobile se apila pero labels siguen siendo largos
- Inputs se vuelven muy altos
- "Salario Mínimo (Bs.)" + "Salario Máximo (Bs.)" = 2 líneas

**Propuesta**:
```css
.salary-inputs {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1rem;
  align-items: flex-end;
}

@media (max-width: 768px) {
  .salary-inputs {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .salary-separator {
    display: none !important;  /* hidden, no space */
  }
}

/* Labels en mobile más cortos */
@media (max-width: 640px) {
  :deep(.salary-inputs .va-input__label) {
    font-size: 0.85rem;
  }
}
```

---

#### 🔴 Problema 8.3: Form Grid Breakpoints Subóptimos
**Ubicación**: `.form-grid` (línea 1048-1051)

**Análisis**:
```css
grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
```

**Problema**:
- minmax(280px) es muy pequeño
- En tablet (768px): caben 2.7 columnas (inestable)
- Debería ser 1 col en tablet, 2 en desktop

**Propuesta**:
```css
/* Desktop: 2 columnas */
.form-grid {
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

/* Tablet: 1 columna */
@media (max-width: 1024px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}

/* Small: flexible pero mínimo */
@media (max-width: 480px) {
  .form-grid {
    gap: 1rem;
  }
}
```

---

### 9️⃣ INTERACTIVIDAD

#### 🔴 Problema 9.1: Sin Feedback de Hover en Inputs
**Ubicación**: va-input, va-textarea, va-select

**Análisis**:
- Componentes Vuestic tienen hover por defecto
- Pero sin feedback visual suficiente
- En mobile: sin feedback alguno

**Propuesta - Agregar Custom Focus States**:
```css
:deep(.va-input:hover),
:deep(.va-textarea:hover),
:deep(.va-select:hover) {
  --va-input-border-color: #7C3AED !important;
  background: #F9F5FF !important;
}

:deep(.va-input__field:focus),
:deep(.va-textarea__field:focus) {
  box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2) !important;
}
```

---

#### 🔴 Problema 9.2: Vacancy Increment Buttons sin Feedback
**Ubicación**: `.vacancy-btn` (línea 1176)

**Análisis**:
- Buttons funcionan
- Pero sin active state visual
- Sin confirmación de click

**Propuesta**:
```css
.vacancy-btn {
  transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.vacancy-btn:active:not(:disabled) {
  transform: scale(0.95);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

---

#### 🔴 Problema 9.3: Sin Keyboard Navigation
**Ubicación**: Todo el componente

**Análisis**:
- Acordeones no responden a Enter/Space
- Sin Tab order visible
- Inaccesible por keyboard

**Propuesta**:
```vue
<!-- En template -->
<div
  class="accordion-header"
  role="button"
  tabindex="0"
  :aria-expanded="expandedSections.basicInfo"
  @click="toggleSection('basicInfo')"
  @keydown.enter="toggleSection('basicInfo')"
  @keydown.space.prevent="toggleSection('basicInfo')"
>
```

CSS:
```css
.accordion-header:focus {
  outline: 2px solid #7C3AED;
  outline-offset: 2px;
}
```

---

### 🔟 ACCESIBILIDAD

#### 🔴 Problema 10.1: Labels No Asociados Correctamente
**Ubicación**: Todos los inputs

**Análisis**:
```vue
<va-input v-model="title" label="Título" />
```

**Problema**:
- Vuestic maneja label internamente
- Pero sin atributos `for/id` accesibles
- Screen readers no entienden relación

**Propuesta**:
```vue
<div class="form-row">
  <label :for="`input-title`" class="form-label">
    Título del Puesto
    <span class="required-mark">*</span>
  </label>
  <va-input
    :id="`input-title`"
    v-model="title"
    aria-labelledby="input-title"
  />
</div>
```

---

#### 🔴 Problema 10.2: Accordion sin ARIA Roles
**Ubicación**: .accordion-header

**Análisis**:
- Acordeón funciona pero sin semántica
- Screen readers no entienden es expandible

**Propuesta**:
```vue
<div
  role="region"
  :aria-labelledby="`accordion-header-${sectionName}`"
>
  <div
    :id="`accordion-header-${sectionName}`"
    role="button"
    :aria-expanded="expandedSections[sectionName]"
    :aria-controls="`accordion-content-${sectionName}`"
    tabindex="0"
    @click="toggleSection(sectionName)"
  >
    ...
  </div>

  <div
    :id="`accordion-content-${sectionName}`"
    v-if="expandedSections[sectionName]"
    role="region"
  >
    ...
  </div>
</div>
```

---

#### 🔴 Problema 10.3: Sin Indicadores de Error Accesibles
**Ubicación**: Validación

**Análisis**:
- Alert() no es accesible
- Sin aria-live para mensajes dinámicos
- Sin aria-invalid en inputs

**Propuesta**:
```vue
<div
  v-if="fieldErrors.title"
  role="alert"
  aria-live="assertive"
  aria-atomic="true"
  class="error-message"
>
  Campo requerido
</div>

<va-input
  aria-invalid="true"
  aria-describedby="error-title"
/>
```

---

## 📊 RESUMEN DE PROBLEMAS

| Categoría | Problemas | Severidad | Impacto |
|-----------|-----------|-----------|---------|
| Estructura Visual | 5 | 🔴 Alta | Visual 3/10 |
| Tipografía | 6 | 🔴 Alta | Legibilidad 4/10 |
| Colores | 4 | 🟡 Media | Identidad 5/10 |
| Espaciado | 5 | 🔴 Alta | UX 4/10 |
| Componentes Vuestic | 5 | 🟡 Media | Funcionalidad 6/10 |
| Acordeones | 4 | 🟡 Media | Interactividad 5/10 |
| Validación | 4 | 🟡 Media | UX 3/10 |
| Responsive | 3 | 🟡 Media | Mobile 4/10 |
| Interactividad | 3 | 🟢 Baja | Feedback 5/10 |
| Accesibilidad | 3 | 🔴 Alta | Inclusión 2/10 |
| **TOTAL** | **42 PROBLEMAS** | **CRÍTICO** | **Promedio 3.9/10** |

---

## 🎯 PRIORIDAD DE IMPLEMENTACIÓN

### Fase 1: CRÍTICO (Impacto Máximo)
1. ✅ Rediseño Header (purple gradient + elevación)
2. ✅ Tipografía (escala consistente)
3. ✅ Acordeones (animaciones suaves)
4. ✅ Fondo (purple tint)
5. ✅ Espaciado (reducir exceso)

**Esfuerzo**: ~2 horas | **Impacto**: Visual 8/10

### Fase 2: IMPORTANTE (Mejora Funcional)
6. Validación en tiempo real
7. Componentes Vuestic (mejores estados)
8. Colores (paleta coherente)
9. Mobile responsive (breakpoints)
10. Feedback visual (toasts)

**Esfuerzo**: ~3 horas | **Impacto**: UX 7/10

### Fase 3: NICE-TO-HAVE (Polish)
11. Accesibilidad (ARIA roles)
12. Keyboard navigation
13. Microinteracciones (hover effects)
14. Loading states
15. Progress indicators

**Esfuerzo**: ~2 horas | **Impacto**: Polish 6/10

---

## 💰 ESFUERZO ESTIMADO TOTAL

| Fase | Tareas | Tiempo | Complejidad |
|------|--------|--------|-------------|
| 1 | 5 cambios críticos | 2h | 🟢 Media |
| 2 | 5 mejoras funcionales | 3h | 🟡 Media-Alta |
| 3 | 5 mejoras de polish | 2h | 🔴 Alta |
| **TOTAL** | **15 mejoras** | **7 horas** | **Media-Alta** |

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Fase 1 (CRÍTICA)
- [ ] Cambiar background a purple tint
- [ ] Mejorar header (sombra + border gradiente)
- [ ] Ajustar tipografía (escala 1.75rem → 700)
- [ ] Reducir espaciado (padding/gap)
- [ ] Animar acordeones (transiciones suaves)

### Fase 2 (IMPORTANTE)
- [ ] Agregar validación visual en inputs
- [ ] Mejorar radio buttons (cards clicables)
- [ ] Ajustar colores a paleta consistente
- [ ] Mobile: breakpoints optimizados
- [ ] Agregar notifications en lugar de alerts

### Fase 3 (POLISH)
- [ ] ARIA labels y roles
- [ ] Keyboard navigation (Enter/Space)
- [ ] Hover effects mejorados
- [ ] Loading states en botones
- [ ] Progress bar de completación

---

## 🚀 SIGUIENTE PASO

¿Comenzamos con **Fase 1** (cambios críticos)?

Recomendación: Implementar primero los 5 cambios de Fase 1 para máximo impacto visual.
Esto tomará ~2 horas y transformará completamente la apariencia del componente.

---

**Documento Creado**: 2025-11-24
**Versión**: 1.0 - Análisis Completo
