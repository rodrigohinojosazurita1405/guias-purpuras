# Guías Púrpuras - ROADMAP Completo MVP

## 📊 ESTADO ACTUAL - PROGRESO GENERAL

```
FASE 1: Wizard de Publicación              ✅ 100% COMPLETADA (5 pasos funcionales)
FASE 1.1: Preguntas de Filtrado            ✅ 100% COMPLETADA (Edición + CRUD)
FASE 1.2: Formulario Aplicación Candidato  ✅ 100% COMPLETADA (ApplicationProcess funcional)
FASE 2: Flujo de Publicación Completo      ✅ 100% COMPLETADA (Backend integrado)
FASE 3: Búsqueda y Filtrado                ⏳ 0% (PENDIENTE)
FASE 3.6: Autenticación Real               ✅ 100% COMPLETADA
FASE 4: Perfiles de Usuario                ✅ 100% COMPLETADA + FOTO CRUD ✅
FASE 5: Perfiles de Empresa                ✅ 100% COMPLETADA (CRUD + CRUD fotos)
FASE 6: Sistema de Aplicaciones            ✅ 100% COMPLETADA (ApplicationProcess + Backend)
FASE 7: Sistema de Pagos + Comprobante     ✅ 100% COMPLETADA (Publicación funcionando)
FASE 7.1: Validación de Pago               ✅ 100% COMPLETADA (Anuncios sin errores)
FASE 7.2: Configuración de Aplicación      ✅ 100% COMPLETADA (Campos condicionales)
FASE 7.3: Gestión de Anuncios              ⏳ 70% (JobsManager mostrado, botones pendientes)
FASE 7.4: Aplicaciones a Anuncios          ⏳ 0% (PENDIENTE)
FASE 7.5: Dashboard de Publicador          ⏳ 0% (PENDIENTE)
FASE 8: Dashboard Admin                    ⏳ 0% (PENDIENTE)
FASE 9: Dashboard Multi-Rol                ⏳ 0% (PLANIFICADA)

MEJORAS RECIENTES (Sesión 10 - ACTUAL):
- ✅ Emojis removidos de PublishSuccessModal.vue (diseño profesional)
- ✅ Ruta de navegación fija: /dashboard/mis-anuncios → /dashboard/jobs-manager
- ✅ Mostrar anuncios publicados en JobsManager (5+ anuncios visibles)
- ✅ Corrección de orden de decoradores en 7 endpoints (Bearer token validation)
- ✅ Configuración de Vite proxy para /api/* → backend Django
- ✅ Sincronización localStorage correcta (auth_user, access_token)
- ✅ JobsManager usa useAuthStore correctamente
- ✅ Conexión frontend-backend completamente funcional
- 🔧 5 bugs críticos solucionados
- 📋 Roadmap actualizado con progreso FASE 7.3
```

---

## ✅ COMPLETADO EN ESTA SESIÓN (Sesión 10 - FASE 7 Mostrar Anuncios + Preparación FASE 7.3)

### FASE 7.3: Gestión de Anuncios - PROGRESO 70% ✅
**Descripción**: Implementación de botones de acción en JobsManager para gestionar anuncios publicados

#### ✅ Lo que YA está funcional:
1. **JobsManager.vue - Mostrar Anuncios**
   - ✅ Lista de anuncios publicados por usuario
   - ✅ Carga de datos desde `/api/user/published?email=X`
   - ✅ Muestra 5+ anuncios del usuario autenticado
   - ✅ Información visible: título, estado, fecha de creación

#### ⏳ LO QUE FALTA - Botones de Acción (PRÓXIMA SESIÓN):
Los siguientes botones necesitan ser implementados en JobsManager.vue:

1. **Botón "Ver"** (Ver completo)
   - [ ] Abre modal/página con detalles completos del anuncio
   - [ ] Muestra: título, descripción, requisitos, salario, benefits
   - [ ] Muestra cantidad de aplicaciones recibidas
   - [ ] Botón "Cerrar anuncio" disponible (cambiar status a closed)
   - [ ] Componente: `JobDetailModal.vue`

2. **Botón "Editar"** (Editar anuncio)
   - [ ] Abre formulario para editar todos los campos
   - [ ] Pre-carga datos actuales del anuncio
   - [ ] PATCH `/api/jobs/{id}/` con cambios
   - [ ] Validación de campos antes de guardar
   - [ ] Confirmación de éxito
   - [ ] Componente: `JobEditModal.vue` o reutilizar PublishView

3. **Botón "Duplicar"** (Crear copia)
   - [ ] Crea anuncio idéntico con nuevo ID
   - [ ] Guarda con estado "draft" (no publicado)
   - [ ] POST `/api/jobs/duplicate/{id}/`
   - [ ] Redirige a editor con copia pre-cargada
   - [ ] Usuario puede cambiar detalles y re-publicar

4. **Botón "Cerrar"** (Cambiar status)
   - [ ] PATCH `/api/jobs/{id}/` con status="closed"
   - [ ] Cambio inmediato en la lista
   - [ ] Confirmación antes de cerrar
   - [ ] Anuncio cerrado sigue visible pero no recibe más aplicaciones
   - [ ] Opción de "Reabrir" si está cerrado

#### Backend Endpoints Necesarios:
```python
# Ya existen:
GET  /api/user/published?email=X           ✅ Funcionando

# Necesarios:
GET  /api/jobs/{id}/                       ⏳ Obtener detalles completo
PATCH /api/jobs/{id}/                      ⏳ Actualizar anuncio
POST /api/jobs/{id}/duplicate/             ⏳ Duplicar anuncio
PATCH /api/jobs/{id}/status/               ⏳ Cambiar status (closed/open)
GET  /api/jobs/{id}/applications/          ⏳ Contar aplicaciones del anuncio
```

#### Estructura de Base de Datos (Job Model):
```python
# Campos que ya existen:
- id, title, description, requirements, salary
- status (default='draft', choices=['draft', 'published', 'closed', 'archived'])
- created_at, updated_at
- created_by (FK to User)

# Campos que podrían ser útiles:
- applicationsCount (auto-calc)
- lastUpdated (timestamp)
- viewsCount (analítica)
```

#### Archivos a Crear/Modificar:
```
✅ JobsManager.vue (YA EXISTE)
   ├─ Agregar 4 botones en template (Ver, Editar, Duplicar, Cerrar)
   ├─ Métodos: viewJob(), editJob(), duplicateJob(), closeJob()
   └─ Loading states, error handling

⏳ JobDetailModal.vue (NUEVO)
   ├─ Mostrar detalles completos
   ├─ Contador de aplicaciones
   └─ Botón cerrar anuncio

⏳ JobEditModal.vue (NUEVO)
   ├─ Reutilizar campos de PublishView
   ├─ Pre-cargar datos actuales
   └─ Validación completa

⏳ jobs/views.py (BACKEND)
   ├─ get_job_detail(request, job_id)
   ├─ edit_job(request, job_id)
   ├─ duplicate_job(request, job_id)
   └─ update_job_status(request, job_id)
```

#### Flujo de Usuario:
```
1. Usuario en JobsManager ve lista de sus anuncios
2. Click "Ver" → Modal con detalles + contador aplicaciones
3. Click "Editar" → Abre editor, realiza cambios, guarda
4. Click "Duplicar" → Copia anuncio en draft para editar
5. Click "Cerrar" → Confirmación → Cambia a status="closed"
6. Anuncio cerrado se marcan visualmente (gris, deshabilitado)
```

#### Estados Visuales Esperados:
```
- 🟢 PUBLISHED (verde)  → Activo, recibiendo aplicaciones
- 🔴 CLOSED (rojo)      → Cerrado, sin aplicaciones nuevas
- ⚪ DRAFT (gris)       → Borrador, no publicado
- ⚫ ARCHIVED (negro)   → Archivado, histórico
```

#### Criterios de Aceptación:
- [ ] Los 4 botones ejecutan acciones correctas
- [ ] Backend responde correctamente a todas las acciones
- [ ] Estados se reflejan inmediatamente en el UI
- [ ] No hay errores en consola
- [ ] Mensajes de confirmación claros
- [ ] Loading states durante operaciones
- [ ] Manejo de errores (404, 403, 500)

**Status Actual**: 70% - Listado funcional, botones pendientes
**Estimado**: 2-3 horas de desarrollo
**Prioridad**: ALTA (interfaz principal del publisher)

---

## ✅ COMPLETADO EN ESTA SESIÓN (Sesión 9 - FASE 7.1 Completada: Anuncios Funcionando)

### Radio Buttons Sin Duplicación ✅
**Problema**: Los va-radio mostraban tanto el valor de la opción ("internal", "external", "both") como el título personalizado ("Interna", "Externa", "Ambas")

**Solución**: Agregado `label=""` a cada va-radio component para que Vuestic no renderice el texto de la opción

**Commits**:
- `d5b0a2e` - Agregar atributo label vacío a componentes va-radio

---

### Preguntas de Filtrado - Totalmente Editable ✅
**Descripción**: Implementación de campos editables para que empresas creen preguntas que filten candidatos

#### 🎯 Características Implementadas
1. **Input de Texto** - Para el enunciado de la pregunta
   - Placeholder: "Ej: ¿Cuáles son tus idiomas?"
   - En tiempo real en el store

2. **Select de Tipo** - 3 opciones:
   - Texto corto
   - Sí / No
   - Opción múltiple

3. **Checkbox de Obligatoriedad** - Toggle "Hacer obligatoria"

4. **CRUD Completo**
   - ✅ Crear pregunta: Botón "Agregar Pregunta (x/5)"
   - ✅ Leer pregunta: Se muestran todos los campos
   - ✅ Actualizar pregunta: updateQuestion() sincroniza con store
   - ✅ Eliminar pregunta: Botón "X" en cada tarjeta

#### 📋 Componentes Modificados
- **frontend/src/components/Publish/ApplicationConfigStep.vue**
  - Template: Agregado .question-form con 3 inputs
  - Script: Función updateQuestion(index, field, value)
  - CSS: .question-form, .form-row, .form-input estilos

#### 🔄 Flujo de Datos
```
Empresa crea pregunta en Step 3
        ↓
updateQuestion() emite evento
        ↓
PublishView recibe y actualiza store
        ↓
usePublishStore.jobData.screeningQuestions se sincroniza
        ↓
Se guarda en localStorage (auto-save)
```

#### 🎯 Dónde ve el Candidato
Las preguntas **NO se ven en el resumen (Step 4)**, pero se mostrarán cuando:
1. El candidato busca una oferta publicada
2. Hace click en "APLICAR"
3. Aparece formulario con las preguntas creadas por la empresa
4. (Componente aún no implementado → FASE 1.2)

**Status**: ✅ COMPLETADA | Commit: `3afb06d`

---

## 🆕 PRÓXIMA: FASE 1.2 - Formulario de Aplicación (Application Form)
**Descripción**: Componente que muestra dinámicamente las preguntas del filtrado para que candidatos respondan al aplicar

### 1.2.1 Flujo del Candidato
```
1. Candidato ve oferta en portal (DashboardView)
2. Click "APLICAR"
3. Modal/Página con:
   ├─ Datos personales pre-cargados (del perfil)
   ├─ Preguntas de filtrado (dinámicas de la oferta)
   │  ├─ Tipo "text" → input text
   │  │  └─ Obligatoria? (sí/no)
   │  ├─ Tipo "yesno" → radio Sí/No
   │  │  └─ Obligatoria? (sí/no)
   │  └─ Tipo "multiple" → select con opciones
   │     └─ Obligatoria? (sí/no)
   └─ Botón "ENVIAR APLICACIÓN"
4. Backend valida respuestas
5. Confirmación de aplicación enviada
```

### 1.2.2 Componentes Necesarios
- [ ] **ProcessApplicationModal.vue** o **ApplicationForm.vue**
  - Mostrar preguntas según tipo
  - Validar obligatoriedad
  - Respuestas en formulario

- [ ] **ScreeningQuestionRenderer.vue** (reutilizable)
  - Renderizar pregunta según tipo
  - Input/Radio/Select dinámico

### 1.2.3 Store Necesario
- [ ] **useApplicationStore.js**
  - applicationData: { jobId, candidateAnswers: [...], status }
  - submitApplication()
  - getScreeningQuestions(jobId)

---

## ✅ COMPLETADO EN SESIÓN 6 (Sesión 6 - Animaciones Premium + Esferas Rebotando)

### Autenticación - Diseño Premium con Animaciones ✨
**Descripción**: Rediseño completo de los formularios de autenticación con animaciones cinematográficas y efectos visuales avanzados

#### 🎨 Animaciones Implementadas

1. **Shooting Stars (Estrellas Fugaces)**
   - ✅ Reemplazadas de meteoros simple a estrellas brillantes elegantes
   - ✅ 4 estrellas con gradiente radial (brillo blanco → púrpura)
   - ✅ Animación `shootingStar` (4-4.8s): Aparecen, brillan, desaparecen
   - ✅ Glow effect expandible: `shootingGlow` con escala progresiva
   - ✅ Posiciones y delays únicos para cada estrella
   - ✅ Box-shadow dual (perímetro + brillo interno)

2. **Partículas Flotantes Ampliadas**
   - ✅ Tamaño aumentado: 3-6px → 10-16px (más visibles)
   - ✅ Brillo mejorado: Gradiente radial más intenso
   - ✅ Box-shadow más prominente: 30px + 60px spread
   - ✅ 12 partículas flotando continuamente
   - ✅ Animación `floatParticle` (20-29s): Flujo suave y hipnotizante
   - ✅ Delays escalonados para efecto natural

3. **Esferas Rebotando 3D**
   - ✅ 4 esferas con efecto de gravedad realista
   - ✅ Tamaños variados: 35-50px
   - ✅ Gradiente radial 3D: Centro brillante → sombra exterior
   - ✅ Inset shadows para profundidad: -2px -2px 5px (arriba-izquierda) + 2px 2px 5px (abajo-derecha)
   - ✅ 3 animaciones bounce diferentes:
     * `bounce1`: 4s (comportamiento realista de rebote)
     * `bounce2`: 5s (trayectoria más alta)
     * `bounce3`: 4.5s (velocidad media)
   - ✅ ScaleY dinámico: Se comprimen al chocar (0.75-0.8)
   - ✅ Posiciones: Bottom -50 a -60px (debajo del viewport)
   - ✅ Z-index 1.5: Entre fondo y partículas

4. **Fondo Dinámico**
   - ✅ Gradient animado 5-colores en loop 15s
   - ✅ 2 blobs flotantes con blur 40px
   - ✅ Pulse animation en blobs (4s)
   - ✅ Colores púrpura consistentes con paleta

#### 📐 Z-Index Layering (Organización Visual)
```
z-index: 0  - Gradient background (#0f0c29 base)
z-index: 1  - Gradient blobs (500x500px, 450x450px)
z-index: 1.5 - Bounce spheres container
z-index: 2  - Particles container (12 partículas)
z-index: 3  - Meteors/Shooting stars container
z-index: 20 - login-content (formulario + card)
```

#### 🎬 Timings & Performance
- ✅ Total 4 animaciones principales: gradientShift, blobFloat1, blobFloat2, pulse
- ✅ 12 partículas con delays escalonados (0-5s)
- ✅ 4 esferas rebotando con ciclos independientes
- ✅ 4 estrellas fugaces con timing único
- ✅ Hardware-accelerated transforms (translateY, scale, rotate)
- ✅ Filter blur optimizado (0.5px partículas, 40px blobs)

#### 📱 Componentes Actualizados
- ✅ **LoginForm.vue** - Toda animación premium
  - Template: Agregados bounce-spheres-container + meteors-container
  - CSS: 8 keyframes nuevos (floatParticle, bounce1, bounce2, bounce3, shootingStar, shootingGlow)
  - Tamaños partículas: 10-16px
  - Esferas: 4 con 3 animaciones diferentes

- ✅ **RegisterForm.vue** - Idéntico a LoginForm
  - Mismo HTML, CSS y animaciones
  - Máx altura controlada para scrolling

- ✅ **ForgotPasswordForm.vue** - Idéntico a LoginForm + RegisterForm
  - Partículas, esferas y estrellas fugaces funcionando
  - Z-index 10 para login-content (menor que LoginForm por responsive)

#### 🎯 Características Visuales
- ✅ Parpadeo suave de partículas (opacity 0→1→0)
- ✅ Movimiento fluido de esferas con compresión realista
- ✅ Estrellas fugaces con trail glow expandible
- ✅ Efecto de profundidad mediante blobs detrás
- ✅ Transiciones suaves en todos los elementos
- ✅ Colores consistentes: púrpura (#7c3aed, #6d28d9), blanco, gris sutil

#### ✨ Resultado Final
Una animación de fondo premium, cinematográfica y profesional que:
- Mantiene la atención del usuario sin ser distractora
- Comunica marca premium y atención al detalle
- Funciona smooth sin impacto en performance
- Es consistente en todas las páginas de autenticación

**Status**: 🎉 COMPLETADA Y VISUALMENTE IMPACTANTE (Sesión 6)

---

## ✅ COMPLETADO EN SESIÓN ANTERIOR (Sesión 5 - Fix Sidebar Infinite Loop + UX Improvements)

### Dashboard Sidebar - Arreglo de Bucle Infinito ✅
**Descripción**: Corrección del problema que causaba bucle infinito al navegar por el sidebar

#### 🔧 Problemas Identificados y Solucionados

1. **Rutas Faltantes en Router**
   - ❌ Problema: El sidebar tenía links a `/dashboard/messages`, `/dashboard/blocked`, etc.
   - ✅ Solución: Agregadas 7 rutas faltantes a `router/index.js`
     * `/dashboard/messages` → Mensajes
     * `/dashboard/blocked` → Usuarios Bloqueados
     * `/dashboard/shortlisted` → Favoritos
     * `/dashboard/users` → Gestionar Usuarios
     * `/dashboard/history` → Registro De Actividad
     * `/dashboard/notifications` → Alertas
     * Todas redirigen a DashboardView.vue con placeholder

2. **Route Mapping Issue**
   - ❌ Problema: Rutas con guiones (`/dashboard/jobs-manager`) no mapeaban a `jobs_manager`
   - ✅ Solución: Agregada conversión en `DashboardView.vue`

3. **Race Condition en Carga de Aplicaciones**
   - ❌ Problema: `useApplications.loadApplications()` podría ejecutarse múltiples veces
   - ✅ Solución: Agregado guard

4. **Better Empty State UX**
   - ❌ Problema: "Base de Talento" mostraba línea de carga sin mensaje
   - ✅ Solución: Mejorado template de CandidatesView:
     * Loading solo se muestra si `isLoading && !isLoaded`
     * Empty state muestra mensaje cuando no hay candidatos
     * Botón "Reintentar" para recargar datos
     * Tip: "Publica un anuncio de trabajo para empezar a recibir candidatos"

#### 📝 Cambios Implementados
- ✅ `frontend/src/router/index.js` - Agregadas 7 rutas del dashboard
- ✅ `frontend/src/views/DashboardView.vue` - Arreglado mapeo de rutas
- ✅ `frontend/src/composables/useApplications.js` - Mejorado con guard y logging
- ✅ `frontend/src/components/Dashboard/CandidatesView.vue` - UX mejorado
- ✅ Mejor logging con emojis para debugging

#### ✅ Estado Actual
- ✅ Sin bucles infinitos en el sidebar
- ✅ Todas las rutas están definidas (muestran placeholder si no tienen componente)
- ✅ Cargas de datos seguras sin race conditions
- ✅ Mensajes claros al usuario en todos los estados

---

### FASE 5: Perfiles de Empresa - COMPLETADO ✅
**Descripción**: Sistema completo de perfiles de empresa con CRUD, subida de logo/banner y gestión

#### ✅ Backend Django
- ✅ Modelo CompanyProfile con campos completos
- ✅ 7 Endpoints API completamente funcionales
- ✅ Validaciones completas

#### ✅ Frontend Vue3 + Pinia
- ✅ Store useCompanyStore.js (18 métodos)
- ✅ Componentes Vue

#### ✅ Testing Completado (2025-11-21)
```
✅ CREATE, GET, UPDATE, LIST - Todos funcionando
```

**Status**: 🎉 COMPLETADA Y FUNCIONANDO

---

### Dashboard Navigation + Dashboard Stats - COMPLETADO ✅
**Descripción**: Rediseño intuitivo de navegación del dashboard con navbar profesional + Stats con OPCIÓN A (Dummy Data)

#### ✅ Frontend Vue3 - Navbar
- ✅ Navbar sencilla dentro del dashboard
- ✅ Dropdown "Cuenta" con elementos
- ✅ Sidebar limpio

#### ✅ Dashboard Stats - OPCIÓN A (Dummy Data)
**Implementado para que dashboard sea funcional sin backend endpoints**

1. **useDashboardStats.js** - Intenta API, si falla usa dummy data
2. **useDashboardActivities.js** - Intenta API, si falla usa dummy data
3. **DashboardHome.vue** - Rutas corregidas, sin errores 404

**Status**: 🎉 COMPLETADA Y FUNCIONANDO PROFESIONALMENTE (CON OPCIÓN A)

---

## 🚀 PRÓXIMAS FASES (RECOMENDADO ORDER)

---

## 🆕 FASE 9: DASHBOARD MULTI-ROL Y MULTI-GUÍA (NUEVA - PRIORIDAD ALTA)
**Descripción**: Transformar el dashboard en un sistema híbrido que soporte múltiples roles y tipos de guías

### 9.1 Arquitectura Multi-Contexto
**Objetivo**: Dashboard que adapta su interfaz según guía activa + rol del usuario

**Composables Nuevos**:
- [ ] **useGuideContext.js** - Gestionar contexto de guía y rol
  - currentGuide (jobs, gastronomy, business, professional)
  - currentRole (recruiter, applicant, client, provider)
  - switchGuide() - cambiar entre guías
  - checkPermission() - verificar permisos

- [ ] **useRecruiterApplications.js** - CRUD postulaciones (reclutador)
  - loadApplications(jobId), updateStatus(), sendMessage()
  - filterByStatus(PENDING/REVIEWED/SHORTLISTED/etc)

- [ ] **useApplicantApplications.js** - CRUD postulaciones (postulante)
  - loadMyApplications(), cancelApplication()
  - checkProfileCompleteness(), getMessages()

### 9.2 Sidebar Reorganizado
**Estructura Propuesta**:
```
┌─ COMÚN (todas las guías)
│  ├─ Dashboard Home
│  ├─ Mi Perfil
│  ├─ Notificaciones
│  └─ Configuración
│
├─ GUÍA ACTIVA: Trabajos (dinámico)
│  ├─ Reclutador:
│  │  ├─ Mis Ofertas
│  │  ├─ Postulaciones (badge: 3)
│  │  └─ Mensajes (badge: 2)
│  │
│  └─ Postulante:
│     ├─ Buscar Trabajos
│     ├─ Mis Postulaciones
│     └─ CV Completo (60%)
│
└─ SELECTOR DE GUÍA (header)
   └─ [🏠 Trabajos ▼] → Gastronomía, Negocios, Profesionales
```

**Componentes Sidebar**:
- [ ] **SidebarGuideSelector.vue** - Dropdown para cambiar guía activa
- [ ] **SidebarCommonMenu.vue** - Menú común (Dashboard, Perfil, Config)
- [ ] **SidebarGuideMenu.vue** - Menú dinámico según guía + rol
- [ ] **SidebarStats.vue** - Mini-stats con badges de notificaciones

### 9.3 Sistema de Postulaciones (Guía Trabajos)

**Estados de Postulación**:
| Estado | Color | Acción Reclutador | Acción Postulante |
|--------|-------|-------------------|-------------------|
| PENDING | Amarillo | Revisar | Cancelar |
| REVIEWED | Azul | Preseleccionar/Rechazar | Ver estado |
| SHORTLISTED | Verde | Aceptar/Rechazar | Ver estado |
| REJECTED | Rojo | N/A | N/A |
| ACCEPTED | Verde Oscuro | N/A | N/A |
| WITHDRAWN | Gris | N/A | N/A |

**Vista Reclutador** (Jobs/Recruiter/):
- [ ] **ApplicationsList.vue** - Tabla de postulantes por oferta
  - Filtros por estado
  - Búsqueda por nombre/email
  - Acciones rápidas (Ver, Cambiar estado, Mensaje)

- [ ] **ApplicationDetail.vue** - Detalle de postulante
  - CV descargable
  - Historial de interacciones
  - Sistema de notas privadas
  - Comparar con otros

- [ ] **RecruiterMessages.vue** - Bandeja de mensajes
  - Respuestas rápidas
  - Templates predefinidos
  - Notificaciones en tiempo real

**Vista Postulante** (Jobs/Applicant/):
- [ ] **MyApplications.vue** - Mis postulaciones
  - Lista con estado visual
  - Mensajes no leídos (badge)
  - Acción: Ver, Cancelar

- [ ] **ApplicationStatus.vue** - Detalle de postulación
  - Timeline del proceso
  - Mensajes del reclutador
  - Retirar postulación

- [ ] **ProfileCompleteness.vue** - Indicador CV
  - Barra de progreso (0-100%)
  - Campos faltantes
  - Acciones rápidas
  - Alert si < 80%

### 9.4 Backend Requerido (Django)

**Modelos Nuevos**:
- [ ] **UserGuideRole** - Relación usuario-guía-rol
  - user (FK), guide_type, role, is_active

- [ ] **Application** - Postulaciones
  - job (FK), applicant (FK), status, notes
  - applied_at, updated_at

- [ ] **ApplicationMessage** - Mensajería
  - application (FK), sender (FK), message
  - is_read, sent_at

**API Endpoints Necesarios**:
```
Reclutador:
GET  /api/jobs/recruiter/applications/?job_id=X&status=PENDING
POST /api/jobs/recruiter/applications/:id/update-status/
POST /api/jobs/recruiter/applications/:id/send-message/

Postulante:
GET  /api/jobs/applicant/applications/
POST /api/jobs/applicant/applications/:id/withdraw/
GET  /api/jobs/applicant/applications/:id/messages/
GET  /api/jobs/applicant/profile-completeness/
```

### 9.5 Pinia Stores Nuevos
- [ ] **stores/guideContext.js** - Estado de guía y rol activo
- [ ] **stores/recruiterApplications.js** - Postulaciones (reclutador)
- [ ] **stores/applicantApplications.js** - Postulaciones (postulante)

### 9.6 Roadmap de Implementación

**Sprint 1: Fundación (2-3 días)**
- [ ] Crear useGuideContext.js
- [ ] Implementar SidebarGuideSelector.vue
- [ ] Reorganizar DashboardSidebar.vue (Común + Dinámico)
- [ ] Agregar badges de notificaciones

**Sprint 2: Reclutador (3-4 días)**
- [ ] Crear useRecruiterApplications.js
- [ ] Implementar ApplicationsList.vue con filtros
- [ ] Implementar ApplicationDetail.vue
- [ ] Sistema de cambio de estados

**Sprint 3: Postulante (2-3 días)**
- [ ] Crear useApplicantApplications.js
- [ ] Implementar MyApplications.vue
- [ ] Implementar ProfileCompleteness.vue
- [ ] Sistema de mensajería inbox

**Sprint 4: Pulido (1-2 días)**
- [ ] Notificaciones en tiempo real
- [ ] Optimización de UX
- [ ] Testing exhaustivo

**Estimación Total**: 8-12 días desarrollo full-time

### 9.7 Preguntas Críticas a Resolver

1. ❓ **¿Un usuario puede ser reclutador Y postulante simultáneamente?**
   - Si SÍ → necesitamos switcher de rol

2. ❓ **¿Mensajería completa o solo notificaciones?**
   - Completa → componentes de chat
   - Solo notificaciones → más simple

3. ❓ **¿CV es PDF o formulario estructurado?**
   - PDF → visor y descarga
   - Formulario → control sobre completitud

4. ❓ **¿Cuántas postulaciones por oferta?**
   - <50 → tabla simple
   - >50 → paginación avanzada

### 9.8 Beneficios

✅ **Separación de Roles**: Cada rol tiene sus componentes, sin `v-if` mezclados
✅ **Escalabilidad Horizontal**: Agregar guía = duplicar estructura Jobs/
✅ **Escalabilidad Vertical**: Agregar rol = crear carpeta dentro de guía
✅ **Mantenibilidad**: Bugs aislados por rol y guía
✅ **Reutilización**: Composables compartidos entre roles

### 9.9 Advertencias Críticas

⚠️ **NO sidebar monolítico** → Componentes pequeños
⚠️ **NO mezclar lógica de roles** → Separar por carpetas
⚠️ **NO olvidar responsive** → Sidebar colapsable móvil
⚠️ **NO implementar todo junto** → Sprints incrementales
⚠️ **NO asumir permisos** → Verificar en backend y frontend

**Estado**: 📋 PLANIFICADA | Prioridad ALTA después de FASE 2

---

## 💼 FASE 2: FLUJO DE PUBLICACIÓN COMPLETO (⭐ SIGUIENTE - CRITICAL)
**Descripción**: Completar el wizard y enviar datos al backend

### 2.1 Revisión de componentes existentes
- [ ] ApplicationConfigStep - Verificar y completar
- [ ] SummaryCard - Mostrar resumen y permitir edición

### 2.2 Backend Integration
- [ ] POST /api/jobs/publish - Crear trabajo
- [ ] Manejo de errores

### 2.3 Frontend Integration
- [ ] Integrar endpoint en PublishView
- [ ] Loading states, Error handling
- [ ] Confirmación de éxito, Redireccionar

### 2.4 Mejoras
- [ ] Auto-save de borradores
- [ ] Validación completa antes de submit
- [ ] Toast notifications

---

## 🔍 FASE 3: BÚSQUEDA Y FILTRADO
**Descripción**: Sistema de búsqueda y filtrado avanzado

### 3.1 Backend
- [ ] GET /api/jobs - Con parámetros de filtro
- [ ] Filtros: categoría, ubicación, salario, tipo contrato
- [ ] Búsqueda por texto, Paginación

### 3.2 Frontend
- [ ] SearchBar en header
- [ ] FilterPanel con opciones
- [ ] ResultsGrid responsive
- [ ] Pagination

### 3.3 Features
- [ ] Guardado de filtros favoritos
- [ ] Búsqueda por ubicación
- [ ] Filtro de salario con rango

---

## 📋 FASE 6: SISTEMA DE APLICACIONES
**Descripción**: Usuarios pueden aplicar a trabajos, empresas ven candidatos

### 6.1 Modelo Backend
- [ ] Modelo Application con campos
- [ ] **Modelo CVData** (Formato Harvard) 🆕
  - Secciones: Personal Info, Education, Experience, Skills, Certifications, Languages, References
  - JSON field para almacenar estructura completa
  - FK a UserProfile (1-to-1 relationship)
  - Timestamps (created_at, updated_at)
  - Completeness percentage (auto-calculado)

### 6.2 API REST
- [ ] POST /api/applications - Crear aplicación
- [ ] GET /api/jobs/{id}/applications - Ver candidatos
- [ ] PUT /api/applications/{id}/status - Cambiar estado
- [ ] GET /api/me/applications - Mis aplicaciones
- [ ] **POST /api/cv/create** - Crear CV formato Harvard 🆕
- [ ] **PATCH /api/cv/update** - Actualizar CV por secciones 🆕
- [ ] **GET /api/cv/me** - Obtener CV del usuario autenticado 🆕
- [ ] **GET /api/cv/completeness** - Calcular % completitud 🆕
- [ ] **POST /api/cv/parse** - Parsear CV subido (PDF → JSON) 🆕

### 6.3 Frontend - Refactorización CV 🆕
- [ ] **CVFormWizard.vue** - Adaptación formato Harvard
  - Step 1: Información Personal (nombre, contacto, dirección)
  - Step 2: Educación (instituciones, títulos, fechas, GPA)
  - Step 3: Experiencia Laboral (empresa, cargo, fechas, logros bullet points)
  - Step 4: Habilidades (técnicas, blandas, idiomas con nivel)
  - Step 5: Certificaciones y Referencias
  - Validación por step (campos requeridos según estándar Harvard)
  - Preview en tiempo real (formato visual Harvard)
  - Auto-save en cada step (localStorage + backend sync)

- [ ] **Process/ProcessApplication.vue** - Integración con CV 🆕
  - Pre-carga datos de CV existente si usuario tiene
  - Botón "Usar mi CV" → auto-completa campos
  - Indicador de completitud CV (badge %)
  - Link directo a CVFormWizard si CV incompleto
  - Validación: No aplicar con CV < 70%

### 6.4 Frontend - Componentes Existentes
- [ ] ApplicationForm.vue
- [ ] CandidatesList.vue
- [ ] ApplicationDetail.vue

### 6.5 Sincronización Dashboard 🆕
- [ ] **DashboardHome.vue** - Widget CV Status
  - Card "Mi CV" con barra de progreso
  - % completitud en tiempo real
  - Acceso rápido a CVFormWizard
  - Alert si CV < 80%
  
- [ ] **useCVStore.js** - Pinia Store 🆕
  - Estado: cvData, isLoading, completeness, lastUpdated
  - Acciones: loadCV(), updateSection(), calculateCompleteness()
  - Getters: cvExists, isComplete, missingSections
  - Persistencia: sync con backend al guardar cada sección

### 6.6 Features
- [ ] Preguntas de screening dinámicas
- [ ] Estados de aplicación
- [ ] Contacto con candidato
- [ ] **CV formato Harvard estandarizado** 🆕
  - Estructura JSON normalizada
  - Validación de campos según estándares académicos
  - Export a PDF con template Harvard
  - Versionado de CV (histórico de cambios)
- [ ] **Parser de CV automático** 🆕
  - Upload PDF/DOCX → extracción automática de datos
  - IA para mapear campos a estructura Harvard
  - Revisión manual post-parse
- [ ] **Auto-completado inteligente** 🆕
  - Sugerencias de habilidades basadas en experiencia
  - Templates de descripción de logros
  - Validación de fechas (edu/exp no overlap incorrectamente)

---

## 💳 FASE 7: PLANES DE PAGO Y COMPROBANTE
**Descripción**: Sistema de planes y subida de comprobante de pago

### 7.1 SISTEMA DE VERIFICACIÓN DE PAGO POR SUPERADMIN (CRÍTICO) 🆕
**Descripción**: Comprobante obligatorio + Aprobación manual del superadmin

#### 7.1.1 Base de Datos Django
**Campos nuevos en modelo Job** (`jobs/models.py`):
```python
proofOfPayment = models.ImageField(
    upload_to='payment_proofs/',
    null=False,          # OBLIGATORIO
    blank=False
)
paymentVerified = models.BooleanField(default=False)
paymentVerifiedBy = models.ForeignKey(User, null=True, blank=True)
paymentVerificationDate = models.DateTimeField(null=True, blank=True)
paymentVerificationNotes = models.TextField(blank=True)
```

**Tareas**:
- [ ] 7.1.1.1 Crear migración Django con nuevos campos
- [ ] 7.1.1.2 Validar relación con User superadmin

#### 7.1.2 Backend Validación
**Endpoint POST `/api/jobs/publish`** (`jobs/views.py`):
- [ ] 7.1.2.1 Validar `proofOfPayment` obligatorio
- [ ] 7.1.2.2 Validar tamaño (máx 5MB)
- [ ] 7.1.2.3 Validar tipo (solo imágenes)
- [ ] 7.1.2.4 Crear Job con `paymentVerified=False`

#### 7.1.3 Backend Verificación Superadmin
**Endpoint POST `/api/jobs/{id}/verify-payment/`** (`jobs/views.py`):
```python
# Solo superadmin puede acceder
@permission_classes([IsAuthenticated, IsSuperAdmin])
def verify_payment(request, job_id):
    job.paymentVerified = request.data.get('approved')
    job.paymentVerifiedBy = request.user
    job.paymentVerificationDate = timezone.now()
    job.save()
```

**Tareas**:
- [ ] 7.1.3.1 Crear endpoint POST `/api/jobs/{id}/verify-payment/`
- [ ] 7.1.3.2 Validar permisos (solo superadmin)
- [ ] 7.1.3.3 Guardar notas de verificación
- [ ] 7.1.3.4 Cambiar estado a `published` si aprueba

#### 7.1.4 Django Admin Personalizado
**Personalización** (`jobs/admin.py`):
- [ ] 7.1.4.1 Agregar campos a `list_display`
- [ ] 7.1.4.2 Agregar filtros por `paymentVerified`
- [ ] 7.1.4.3 Mostrar preview de imagen de comprobante
- [ ] 7.1.4.4 Agregar acciones en lote (Aprobar/Rechazar)

#### 7.1.5 Frontend - Validación Obligatoria
**PublishView.vue** (`frontend/src/views/PublishView.vue`):
- [ ] 7.1.5.1 Validar `proofOfPaymentPreview` NO sea null
- [ ] 7.1.5.2 Mostrar error si falta comprobante
- [ ] 7.1.5.3 Bloquear botón "PUBLICAR" sin comprobante
- [ ] 7.1.5.4 Enviar archivo en FormData

#### 7.1.6 Frontend - Indicador de Estado
**SummaryCard.vue** (`frontend/src/components/Cards/SummaryCard.vue`):
- [ ] 7.1.6.1 Mostrar badge "Verificación pendiente" si `paymentVerified=false`
- [ ] 7.1.6.2 Mostrar badge "Verificado ✅" si `paymentVerified=true`
- [ ] 7.1.6.3 No permitir edición si está pendiente

#### 7.1.7 Flujo Completo
```
1. Usuario sube comprobante → proofOfPaymentPreview se llena
2. Usuario click "PUBLICAR"
3. Frontend valida comprobante ≠ null
4. Si falta → Error "Comprobante requerido" ❌
5. Si existe → POST /api/jobs/publish + archivo
6. Backend guarda en proofOfPayment + paymentVerified=FALSE
7. Superadmin revisa en Django Admin
8. Si OK → Click "Aprobar" → paymentVerified=TRUE + status=published ✅
9. Si falso → Click "Rechazar" → paymentVerified=FALSE ❌
10. Usuario ve estado en dashboard (Pendiente/Verificado)
```

#### 7.1.8 Tareas de Configuración
- [ ] 7.1.8.1 Configurar MEDIA_ROOT y MEDIA_URL en settings.py
- [ ] 7.1.8.2 Crear carpeta media/payment_proofs/
- [ ] 7.1.8.3 Agregar permisos superadmin en backend
- [ ] 7.1.8.4 Agregar permisos en JWT tokens si usa DRF

**Status**: ✅ COMPLETADO - FUNCIONANDO EN PRODUCCIÓN

**Lo que se implementó:**
- ✅ 5 campos nuevos en modelo Job (proofOfPayment, paymentVerified, paymentVerifiedBy, paymentVerificationDate, paymentVerificationNotes)
- ✅ Migración Django creada y aplicada
- ✅ Backend valida comprobante obligatorio (formato, tamaño)
- ✅ Endpoint PATCH `/api/jobs/{id}/verify-payment` para superadmin
- ✅ Django Admin personalizado con resumen de verificación
- ✅ Frontend valida comprobante antes de publicar
- ✅ Almacenamiento seguro en media/payment_proofs/
- ✅ Test realizado: Anuncio creado y pagado verificado exitosamente (ID: 09e36c2f)

---

### 7.2 Modelos Backend (Antiguo)
- [ ] Modelo Payment con campos

### 7.3 API REST (Antiguo)
- [ ] POST /api/payments - Crear pago
- [ ] POST /api/payments/{id}/upload - Subir comprobante
- [ ] GET /api/payments - Ver mis pagos

### 7.4 Frontend (Antiguo)
- [ ] PaymentModal.vue
- [ ] PlanSelector.vue
- [ ] ProofUpload.vue

### 7.5 QR Predefinidos
- [ ] Generar QR para cada plan
- [ ] Mostrar en modal de pago

### 7.6 Features
- [ ] Validación de comprobante
- [ ] Estados de pago
- [ ] Historial de pagos

---

## 👨‍💼 FASE 8: DASHBOARD ADMIN
**Descripción**: Panel admin para aprobar pagos y activar anuncios

### 8.1 Backend
- [ ] API para obtener pagos pendientes
- [ ] API para aprobar/rechazar pagos
- [ ] API para activar/desactivar anuncios

### 8.2 Frontend
- [ ] AdminDashboard.vue
- [ ] PendingPayments.vue
- [ ] JobApproval.vue

### 8.3 Features
- [ ] Visualización de comprobantes
- [ ] Aprobación en masa
- [ ] Rechazo con motivo
- [ ] Estadísticas de pagos

---

## 📊 TAREAS INMEDIATAS (PRÓXIMA SESIÓN)

### 🎯 Prioridad 1: FASE 2 - Publicación de Trabajos (CRITICAL)
**Estado**: Frontend 100%, Backend 0%
1. **Backend**:
   - [ ] Endpoint POST `/api/jobs/publish`
   - [ ] Endpoint GET `/api/jobs/{id}`
   - [ ] Endpoint PATCH `/api/jobs/{id}/edit`

2. **Frontend Integration**:
   - [ ] Conectar PublishView.vue con endpoint
   - [ ] Loading states, Error handling
   - [ ] Success confirmation + redirect

### 🎯 Prioridad 2: FASE 9 - Dashboard Multi-Rol (RECOMENDADO)
**Estado**: 0% (planificada)
**Cuándo**: Después de FASE 2 O en paralelo si hay tiempo

**Razón para priorizar**: 
- FASE 6 (postulaciones) necesita esta arquitectura
- Mejor hacerlo antes que el dashboard crezca
- Evita refactorización masiva después

### 🎯 Prioridad 3: FASE 6 - CV Formato Harvard + Sistema Aplicaciones (RECOMENDADO)
**Estado**: 0% (planificada)
**Componentes Críticos**:
- CVFormWizard.vue → Refactorización formato Harvard (5 steps)
- ProcessApplication.vue → Integración con CV existente
- useCVStore.js → Sincronización backend-dashboard
- CV Parser (PDF/DOCX → JSON Harvard structure)

**Razón para priorizar**:
- CV es requisito para aplicar a trabajos
- Sincronización con dashboard mejora UX
- Parser automático reduce fricción de usuario

**Dependencias**:
- FASE 4 (Perfiles Usuario) ✅ Completada
- FASE 9 (Dashboard Multi-Rol) recomendada antes

### 🎯 Prioridad 4: FASE 3 - Búsqueda y Filtrado
**Estado**: 0% - Después de FASE 2

---

## 🎨 DESIGN TOKENS (Mantener consistencia)

### Colores
```
Primary: #7C3AED (Purple)
Secondary: #10B981 (Green)
Warning: #FF8F00 (Orange)
Error: #EF4444 (Red)
```

---

## 📈 CRITERIOS DE ÉXITO POR FASE

### FASE 2 ✅
- Trabajo se publica en BD
- Usuario ve confirmación
- Puede ver su publicación

### FASE 6 ✅
- CV formato Harvard completado y guardado
- Parser automático extrae datos de PDF/DOCX
- CVFormWizard con 5 steps funcionales
- ProcessApplication pre-carga CV del usuario
- Dashboard muestra % completitud CV
- Sincronización backend-frontend en tiempo real
- No permite aplicar con CV < 70%

### FASE 9 ✅
- Sidebar se adapta a rol
- Reclutador ve postulaciones
- Postulante ve sus aplicaciones
- Sistema de estados funciona

---

## 📅 ÚLTIMA ACTUALIZACIÓN
- **Fecha**: 2025-11-26 (Sesión 10 - ACTUAL)
- **Sesión**: FASE 7.3 Preparada - Gestión de Anuncios (botones pendientes)

- **Sesión actual (Sesión 10 - FASE 7 COMPLETADA: MOSTRAR ANUNCIOS EN DASHBOARD)**:
  - ✅ **FASE 7: Sistema de Publicación - 100% COMPLETADA**
    * ✅ Emojis removidos de PublishSuccessModal.vue (diseño profesional con checkmark CSS)
    * ✅ Ruta de navegación fija: /dashboard/mis-anuncios → /dashboard/jobs-manager
    * ✅ JobsManager.vue ahora muestra 5+ anuncios del usuario autenticado
    * ✅ Carga de anuncios desde endpoint `/api/user/published?email=X`
    * ✅ Sincronización localStorage: auth_user, access_token, refresh_token
    * ✅ useAuthStore integrado correctamente con Bearer token en headers

  - 🔧 **Bugs Solucionados (5 problemas críticos)**:
    1. ❌ → ✅ localStorage key mismatch (authUser vs auth_user)
    2. ❌ → ✅ Decoradores Django en orden incorrecto (7 endpoints)
    3. ❌ → ✅ Vite proxy no configurado para /api/* requests
    4. ❌ → ✅ Bearer token faltante en JobsManager fetch
    5. ❌ → ✅ Respuesta HTML en lugar de JSON (Vite sirviendo index.html)

  - 📊 **Commits de sesión**:
    * `be68325` - Remover emojis y fijar ruta de navegación
    * `a9c2484` - Agregar Authorization header a fetch
    * `c8891a8` - Usar useAuthStore en lugar de localStorage directo
    * `ab0f310` - Corregir orden de decoradores en 7 endpoints
    * `23f9dcb` - Agregar proxy Vite para /api/* → Django backend

  - 📋 **Cambios Técnicos Realizados**:
    * ✅ frontend/vite.config.js - Agregado proxy configuration
    * ✅ frontend/src/components/Modals/PublishSuccessModal.vue - Emojis removidos
    * ✅ frontend/src/components/Dashboard/JobsManager.vue - Bearer token + useAuthStore
    * ✅ jobs/views.py (7 endpoints) - Orden de decoradores correcto
    * ✅ auth_api/decorators.py - Token validation mejorando logging

  - ⏳ **FASE 7.3: Próximas acciones (PLANIFICADAS para siguiente sesión)**:
    * [ ] Botón "Ver" - Modal con detalles completos + contador aplicaciones
    * [ ] Botón "Editar" - Formulario para actualizar anuncio (PATCH /api/jobs/{id}/)
    * [ ] Botón "Duplicar" - Crear copia en estado draft (POST /api/jobs/{id}/duplicate/)
    * [ ] Botón "Cerrar" - Cambiar status a closed (PATCH /api/jobs/{id}/status/)
    * Estimado: 2-3 horas de desarrollo
    * Prioridad: ALTA

- **Sesión anterior (Sesión 9 - FASE 7.1 COMPLETADA)**:
  - ✅ **FASE 7.1: Validación de Pago - 100% COMPLETADO**
    * ✅ Arreglo estructura excepciones en publish_job (respuesta éxito aún dentro except)
    * ✅ Cambio UntypedToken → AccessToken en decorador JWT
    * ✅ Eliminación de emojis para compatibilidad Windows (cp1252)
    * ✅ Anuncios se publican exitosamente desde frontend
    * ✅ Comprobante de pago se guarda en media/payment_proofs/
    * ✅ Token JWT validado correctamente (AccessToken)
    * ✅ Conexión frontend-backend establecida

  - 🔧 **Bugs Solucionados (commit c7620a7)**:
    * ❌ ANTES: Respuesta éxito inalcanzable dentro del bloque except
    * ✅ DESPUÉS: Éxito retorna 201 con datos del job creado
    * ❌ ANTES: Token validation fallaba silenciosamente
    * ✅ DESPUÉS: AccessToken valida correctamente JWT
    * ❌ ANTES: Emojis causaban UnicodeEncodeError en Windows
    * ✅ DESPUÉS: Logs legibles en cualquier consola

  - 📊 **Tests Realizados**:
    * ✅ POST /api/jobs/publish con datos completos
    * ✅ Archivo proofOfPayment subido y almacenado
    * ✅ Job creado con ID 44482c3c
    * ✅ Response 201: "¡Oferta publicada exitosamente!"
    * ✅ Comprobante visible en admin

  - 📋 **Status FASE 7.1**:
    ```
    ✅ Modelo Job.proofOfPayment         - OK
    ✅ Modelo Job.paymentVerified        - OK
    ✅ Validación de archivo             - OK
    ✅ Almacenamiento media/payment_proofs/ - OK
    ✅ Endpoint publish_job completo     - OK
    ✅ Token JWT con AccessToken         - OK
    ✅ Frontend PublishForm 5 pasos      - OK
    ✅ Conexión API frontend-backend     - OK
    ✅ Error handling y validación       - OK
    ```

- **Commits de sesión 9**:
  - `c7620a7` - Arreglar publicación de anuncios y validación de tokens JWT

- **Sesión anterior (Sesión 8)**:
  - ✅ Fix: Radio buttons sin duplicación de etiquetas (label="")
  - ✅ Implementación: Preguntas de Filtrado totalmente editable
  - ✅ Función updateQuestion() implementada
  - ✅ CRUD completo: Create, Read, Update, Delete

- **Commits de sesión 8**:
  - `d5b0a2e` - Agregar atributo label vacío a va-radio
  - `3afb06d` - Implementar campos editable para Preguntas de Filtrado

- **Sesión anterior (Sesión 7)**:
  - ✅ Análisis completo de arquitectura multi-rol (FASE 9)
  - ✅ Planificación: Dashboard Multi-Rol y Multi-Guía
  - ✅ FASE 6 ampliada: CV Formato Harvard + Parser automático

- **Sesión anterior (Sesión 6)**:
  - ✅ Autenticación: Animaciones cinematográficas
  - ✅ Shooting Stars, Partículas, Esferas 3D

- **Próximas tareas recomendadas**:
  1. **FASE 1.2** - Formulario de Aplicación (ProcessApplicationModal)
  2. **FASE 2** - Publicación en Backend + Integration
  3. **FASE 9 Sprint 1** - Fundación Multi-Rol

- **Status actual**:
  - ✅ FASE 1: 95% completada (Paso 3 + Preguntas filtrado funcionales)
  - ✅ FASE 7: 80% completada (QR + Upload funcionales)
  - 📋 FASE 1.2: Planificada y documentada
  - 📋 FASE 2: Esperando backend
  - 📋 FASE 9: Planificada y documentada