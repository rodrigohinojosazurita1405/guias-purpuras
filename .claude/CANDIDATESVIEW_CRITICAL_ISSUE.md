# 🔴 ISSUE CRÍTICO: CandidatesView - CVs PDF no se visualizan

## ✅ RESUELTO

**Fecha de resolución**: 22 de diciembre de 2025

---

## Descripción del Problema

El dashboard de empleador (`/dashboard/candidates`) no mostraba las postulaciones con CVs PDF aunque:
- ✅ El backend guardaba correctamente el CV
- ✅ El backend creaba correctamente la aplicación
- ✅ Los datos se enviaban correctamente desde el API
- ❌ El frontend NO renderizaba las aplicaciones

### Síntomas

1. La vista mostraba "No hay candidatos registrados" aunque existía 1 aplicación
2. Los logs del composable mostraban que los datos SÍ se cargaban
3. El computed `filteredApplications` NUNCA se ejecutaba
4. Vue no establecía dependencias reactivas correctamente

---

## Causa Raíz

**Problema de Reactividad de Vue 3**:

1. **Vue no detectaba cambios** en el array `applications` del composable singleton
2. **El computed no se ejecutaba** porque las condiciones `v-if` del template evaluaban otras propiedades primero
3. **Error almacenado** de sesiones previas hacía que siempre se mostrara el estado de error
4. **Falta de `triggerRef()`** después de asignar el array de aplicaciones

---

## Solución Implementada

### 1. **Composable `useApplications.js`**

#### Cambio 1: Forzar reactividad con `triggerRef()`
```javascript
import { ref, computed, triggerRef } from 'vue'

// Después de asignar applications
applications.value = allApplications
triggerRef(applications)  // ← CRÍTICO: Forzar actualización reactiva
```

#### Cambio 2: Limpiar logs de debugging
- Removidos todos los `console.log()` de debugging
- Mantenida lógica de negocio limpia y eficiente

### 2. **Componente `CandidatesView.vue`**

#### Cambio 1: Renombrar y simplificar computed
```javascript
// ANTES: filteredApplications (problemático)
// DESPUÉS: displayApplications (funcionando)

const displayApplications = computed(() => {
  const rawApps = applicationMgr.applications.value

  if (!rawApps || rawApps.length === 0) {
    return []
  }

  let result = [...rawApps]

  // Filter by status
  if (filterStatus.value) {
    result = result.filter(app => app.status === filterStatus.value)
  }

  // Filter by search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(app =>
      (app.applicantName || '').toLowerCase().includes(query) ||
      (app.applicantEmail || '').toLowerCase().includes(query) ||
      (app.jobTitle || '').toLowerCase().includes(query)
    )
  }

  return result
})
```

#### Cambio 2: Agregar watch profundo
```javascript
watch(
  () => applicationMgr.applications.value,
  () => {
    // Force reactivity update
  },
  { deep: true, immediate: true }
)
```

#### Cambio 3: Simplificar onMounted
```javascript
onMounted(async () => {
  // Limpiar error anterior antes de cargar
  applicationMgr.error = null  // ← CRÍTICO: Evita mostrar errores antiguos

  try {
    await applicationMgr.loadApplications()

    // Forzar acceso al computed para establecer dependencia reactiva
    displayApplications.value.length

    await nextTick()

    localIsReady.value = true
  } catch (error) {
    localIsReady.value = true
  }
})
```

#### Cambio 4: Fix descarga de CV
```javascript
const downloadCV = (fileUrl) => {
  if (!fileUrl) return

  // Asegurar URL absoluta
  const fullUrl = fileUrl.startsWith('http')
    ? fileUrl
    : `http://localhost:8000${fileUrl}`

  window.open(fullUrl, '_blank')
}
```

#### Cambio 5: Actualizar template v-if conditions
```vue
<!-- ANTES -->
<div v-else-if="localIsReady && filteredApplications.length > 0">

<!-- DESPUÉS -->
<div v-else-if="localIsReady && displayApplications.length > 0">
```

---

## Verificación

### Backend (Django Shell)
```bash
python manage.py shell -c "from G_Jobs.applicants.models import JobApplication; apps = JobApplication.objects.filter(applicant__email='mauge@gmail.com'); print(f'Total: {apps.count()}, Job: {apps.first().job.title if apps.exists() else \"N/A\"}, CV: {\"SI\" if apps.first().cv else \"NO\" if apps.exists() else \"N/A\"}')"
```

**Resultado**: `Total: 1, Job: ENCARGADO DE MARKETING DIGITAL, CV: SI`

### Frontend (Console)
```javascript
// Los logs mostraban:
✅ Total de aplicaciones cargadas: 1
✅ displayApplications.length: 1
✅ localIsReady = true
```

### Datos completos del CV
```json
{
  "id": "d7d6dd5d-84e9-49db-a64e-ca6589f05580",
  "applicantName": "maria varquera",
  "applicantEmail": "mauge@gmail.com",
  "cv": {
    "id": "20bf74e1-4635-4744-8306-9979081ae6c3",
    "name": "CV 22/12/2025",
    "type": "uploaded",
    "file_url": "/media/applicant_cvs/Proyección_Guías_Púrpuras_-_Excel.pdf",
    "file_name": "CV 22/12/2025"
  },
  "status": "submitted",
  "jobTitle": "ENCARGADO DE MARKETING DIGITAL",
  "jobId": "8a1263ec"
}
```

---

## Funcionalidades Verificadas ✅

1. ✅ **Visualización de postulaciones** - Las tarjetas se muestran correctamente
2. ✅ **Descarga de CV PDF** - Abre el PDF en nueva pestaña
3. ✅ **Cambio de estado** - Los botones de estado funcionan
4. ✅ **Notas del reclutador** - Se guardan correctamente
5. ✅ **Búsqueda y filtros** - Funcionan correctamente

---

## Lecciones Aprendidas

### Vue 3 Reactivity
1. **Usar `triggerRef()`** cuando se asignan arrays completos en refs
2. **Watch profundo** es necesario para arrays de objetos complejos
3. **Limpiar estados previos** (especialmente errores) antes de cargar datos nuevos
4. **Forzar acceso a computeds** en lifecycle hooks para establecer dependencias

### Debugging
1. **Verificar primero el backend** con Django shell
2. **Logs estratégicos** en puntos clave del flujo de datos
3. **Probar reactividad** con cambios manuales en consola
4. **No asumir** que los datos están cuando los logs dicen que sí

---

## Archivos Modificados

1. `frontend/src/composables/useApplications.js`
   - Agregado `triggerRef()`
   - Limpieza de logs

2. `frontend/src/components/Dashboard/CandidatesView.vue`
   - Renombrado computed a `displayApplications`
   - Agregado watch profundo
   - Simplificado onMounted
   - Fix URL descarga CV
   - Limpieza de logs

---

## Estado Final

🎉 **COMPLETAMENTE FUNCIONAL**

- Postulaciones se visualizan correctamente
- CV PDF se puede descargar
- Cambio de estado funciona
- Notas del reclutador funcionan
- Código limpio sin logs de debugging
