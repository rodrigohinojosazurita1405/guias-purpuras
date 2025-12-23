# FIX: Overlay Oscuro en Modales - Conflicto CKEditor

## Problema Identificado

Desde la implementación de CKEditor en `InformationStepJob.vue`, se presentaron dos problemas críticos:

### 1. **Overlay Oscuro en Modales**
- Los modales de Vuestic (`va-modal`) mostraban un overlay completamente oscuro (opacidad incorrecta)
- Afectaba a:
  - Modal de validación de campos incompletos en `InformationStepJob.vue`
  - Modal de publicación exitosa en `PublishSuccessModal.vue`

### 2. **CKEditor Superpuesto al Navbar**
- El editor CKEditor y sus dropdowns se superponían al navbar principal
- Los dropdowns de colores, fuentes, etc. aparecían por encima del navbar

## Causa Raíz

CKEditor utiliza z-index muy altos (~9999-10000) por defecto, lo que causaba:
1. Interferencia con los overlays de los modales de Vuestic
2. Superposición sobre el navbar (z-index: 1000)

## Solución Implementada

### Jerarquía de Z-Index Establecida

```
100-500   : CKEditor base (toolbar, editor area)
1000      : Navbar principal
1100-1150 : CKEditor dropdowns y balloons (por encima del navbar)
10500     : Modales - overlay/backdrop
10600     : Modales - dialog
10700+    : Modales - inner content
```

### Archivos Modificados

#### 1. `frontend/src/App.vue`
**Cambios:**
- ✅ Agregados estilos globales para controlar z-index de CKEditor
- ✅ Configurado z-index de modales Vuestic
- ✅ Asegurado overlay semi-transparente (rgba(0, 0, 0, 0.5))
- ✅ CKEditor base mantiene z-index bajo (100-500)
- ✅ CKEditor dropdowns configurados justo por encima del navbar (1100-1150)

```css
/* CKEditor - Mantener BAJO el navbar */
.ck.ck-editor,
.ck.ck-reset,
.ck.ck-reset_all,
.ck-body-wrapper {
  z-index: 100 !important;
  position: relative !important;
}

/* CKEditor Dropdowns - Por encima del navbar pero BAJO los modales */
.ck.ck-balloon-panel,
.ck-dropdown__panel,
.ck.ck-toolbar__items {
  z-index: 1100 !important;
  position: absolute !important;
}

/* Modales Vuestic - MUY por encima de todo */
.va-modal__overlay,
.va-modal__container {
  z-index: 10500 !important;
}

.va-modal__dialog {
  z-index: 10600 !important;
}

.va-modal__overlay {
  background-color: rgba(0, 0, 0, 0.5) !important;
  opacity: 1 !important;
}
```

#### 2. `frontend/src/views/FormCreate/InformationStepJob.vue`
**Cambios:**
- ✅ Agregado `overflow-x: hidden` al contenedor principal
- ✅ Configurado z-index bajo para editor wrapper (z-index: 1)
- ✅ Agregados estilos `:deep()` para controlar z-index del modal de errores

```css
.information-step-job {
  overflow-x: hidden; /* Evitar que CKEditor se salga horizontalmente */
}

.editor-wrapper-ckeditor {
  position: relative;
  z-index: 1; /* Mantener bajo para no superponer navbar */
}

/* Modal de errores */
:deep(.va-modal__overlay) {
  z-index: 10500 !important;
  background-color: rgba(0, 0, 0, 0.5) !important;
}
```

#### 3. `frontend/src/components/Modals/PublishSuccessModal.vue`
**Cambios:**
- ✅ Agregados estilos scoped para controlar z-index del modal

```css
.success-modal :deep(.va-modal__overlay) {
  z-index: 10500 !important;
  background-color: rgba(0, 0, 0, 0.5) !important;
}

.success-modal :deep(.va-modal__container) {
  z-index: 10500 !important;
}

.success-modal :deep(.va-modal__dialog) {
  z-index: 10600 !important;
}
```

## Resultado Esperado

✅ **Overlay de modales correctamente visible** con opacidad 50% (semi-transparente)
✅ **CKEditor no se superpone al navbar**
✅ **Dropdowns de CKEditor funcionan correctamente** (por encima del navbar)
✅ **Modales funcionan correctamente** con overlay visible y contenido accesible

## Testing Recomendado

1. **Test Modal de Validación:**
   - Ir a crear anuncio de trabajo
   - Intentar avanzar sin completar campos
   - Verificar que el overlay sea semi-transparente (no completamente negro)
   - Verificar que el modal sea visible y clickeable

2. **Test Modal de Publicación:**
   - Completar formulario de trabajo
   - Publicar anuncio
   - Verificar que el modal de éxito tenga overlay semi-transparente
   - Verificar que los botones sean clickeables

3. **Test CKEditor vs Navbar:**
   - Abrir formulario de trabajo
   - Usar CKEditor (cambiar colores, fuentes, etc.)
   - Verificar que los dropdowns no se superpongan al navbar
   - Verificar que el editor no se salga del contenedor

## Notas Técnicas

- Se utilizó `!important` para asegurar que los estilos sobrescriban los defaults de CKEditor y Vuestic
- El uso de `:deep()` en Vue 3 permite modificar estilos de componentes hijos
- La jerarquía de z-index está documentada para futuras modificaciones
- Todos los overlays usan `rgba(0, 0, 0, 0.5)` para consistencia visual

## Fecha de Implementación
22 de diciembre de 2025
