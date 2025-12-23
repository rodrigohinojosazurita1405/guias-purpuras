# Guías Púrpuras - ROADMAP Completo MVP

## 📊 ESTADO ACTUAL - PROGRESO GENERAL
FASE 1: Wizard de Publicación              ✅ 100% COMPLETADA
FASE 1.1: Preguntas de Filtrado            ✅ 100% COMPLETADA
FASE 1.2: Formulario Aplicación Candidato  ✅ 100% COMPLETADA
FASE 2: Flujo de Publicación Completo      ✅ 100% COMPLETADA
FASE 3: Búsqueda y Filtrado GuideView      ✅ 100% COMPLETADA
FASE 3.6: Autenticación Real               ✅ 100% COMPLETADA
FASE 4: Perfiles de Usuario                ✅ 100% COMPLETADA
FASE 5: Perfiles de Empresa                ✅ 100% COMPLETADA
FASE 6: Sistema de Aplicaciones            ✅ 100% COMPLETADA
FASE 7: Sistema de Pagos + Comprobante     ✅ 100% COMPLETADA
FASE 7.1: Validación de Pago               ✅ 100% COMPLETADA
FASE 7.2: Configuración de Aplicación      ✅ 100% COMPLETADA
FASE 7.3: Gestión de Anuncios              ✅ 100% COMPLETADA
FASE 7.4: Gestión de Órdenes y Facturas    ✅ 100% COMPLETADA
FASE 7.5: Sistema de Mensajes              ⏳ 60% (Interfaz lista, falta backend)
FASE 7.6: Aplicaciones a Anuncios          ✅ 100% COMPLETADA
FASE 7.7: Notificaciones de Estado         ⏳ 0% PENDIENTE

FASE 8: Sistema de Auditoría               ✅ 100% COMPLETADA
FASE 9: Sistema de Reportes Diarios        ✅ 100% COMPLETADA
FASE 10: CRUD dinámico de categorías       ✅ 100% COMPLETADA
FASE 11: Admin Django mejorado             ✅ 100% COMPLETADA


---

## 📝 DETALLES DE FASES COMPLETADAS RECIENTEMENTE

### ✅ FASE 8: Sistema de Auditoría (100% COMPLETADA) - Diciembre 2024
**App:** `audit`
**Modelos:** `AuditLog`, `AuditLogSummary`
**Archivos:** `audit/models.py`, `audit/admin.py`, `audit/signals.py`

- ✅ Modelo genérico de auditoría con ContentTypes
- ✅ Rastreo de usuario, acción, cambios (before/after), IP, user agent
- ✅ Acciones: create, update, delete, verify_payment, pause, activate, etc.
- ✅ Niveles de severidad: info, warning, critical
- ✅ Signals automáticos para Jobs, PlanOrders, CompanyProfiles, Users
- ✅ Admin Django con badges de colores, visualización de cambios
- ✅ Filtros avanzados por usuario, acción, modelo, fecha
- ✅ Resúmenes diarios de auditoría
- ✅ Logs de seguridad (intentos de acceso, cambios críticos)

### ✅ FASE 9: Sistema de Reportes Diarios (100% COMPLETADA) - Diciembre 2024
**App:** `reports`
**Modelos:** `DailyReport`
**Archivos:** `reports/models.py`, `reports/admin.py`

- ✅ Reporte diario automático con métricas clave
- ✅ Usuarios: nuevos usuarios, empresas, postulantes, activos totales
- ✅ Trabajos: nuevos, activos, cerrados, vistas totales
- ✅ Planes: vendidos por tipo (estándar, púrpura, impulso)
- ✅ Ingresos: total y desglosado por plan
- ✅ Admin con visualizaciones y badges de colores
- ✅ Botón "Generar Reporte" para crear/actualizar reportes
- ✅ Método `generate_report()` para automatización
- ✅ Vista de tendencias y análisis de crecimiento

### ✅ FASE 10: CRUD Dinámico de Categorías (100% COMPLETADA) - Diciembre 2024
**Modelos:** `JobCategory`, `ContractType`, `City`
**Archivos:** `jobs/models.py`, `jobs/admin.py`, `jobs/views.py`

- ✅ Modelo JobCategory (categorías de trabajo dinámicas)
- ✅ Modelo ContractType (tipos de contrato dinámicos)
- ✅ Modelo City (ciudades dinámicas)
- ✅ Campos: name, label, icon, display_order, is_active
- ✅ Admin Django para gestión CRUD completa
- ✅ API endpoints: /api/jobs/categories/, /api/jobs/contract-types/, /api/jobs/cities/
- ✅ Frontend actualizado para consumir endpoints
- ✅ Migración de datos hardcodeados a base de datos
- ✅ Ordenamiento personalizable
- ✅ Activación/desactivación de opciones

### ✅ FASE 11: Admin Django Mejorado (100% COMPLETADA) - Diciembre 2024
**Archivos:** `jobs/admin.py`, `plans/admin.py`, `audit/admin.py`, `reports/admin.py`, `core/settings.py`

- ✅ Badges de colores tenues y sutiles (colores más suaves, tamaños reducidos)
- ✅ Visualización mejorada de PlanOrder con datos de facturación
- ✅ Filtros avanzados en todos los modelos
- ✅ Búsqueda optimizada con múltiples campos
- ✅ Acciones bulk personalizadas
- ✅ Vistas de solo lectura para logs de auditoría
- ✅ Displays personalizados con format_html
- ✅ Ordenamiento por defecto optimizado
- ✅ CustomUser admin con roles y permisos
- ✅ Django Jazzmin instalado y configurado
- ✅ Menús jerárquicos organizados (TRABAJOS como dropdown principal)
- ✅ Logo de Guías Púrpuras en sidebar, login y favicon
- ✅ Colores por defecto de Jazzmin (tema flatly)
- ✅ Íconos FontAwesome para todos los modelos
- ✅ Badge de vencimiento muestra días restantes + fecha exacta
- ✅ Badge de verificación más sutil ("✓ Verificado" en lugar de "✓✓ VERIFICADO")
- ✅ Tab "Verificación de Pago" como primer fieldset por defecto
- ✅ Textos profesionales (removidos textos de desarrollo como "FASE 7.1")

### ✅ FASE 7.3: Gestión de Anuncios (100% COMPLETADA)
**Componente:** `JobsManager.vue`
- ✅ Switch activar/desactivar anuncio con validación de pago
- ✅ Botones estilizados (Ver, Editar, Eliminar)
- ✅ Modal de edición de anuncio
- ✅ Indicadores de estado (pending, active, closed, draft)
- ✅ Contador de vistas y aplicaciones
- ✅ Información de plan y vencimiento
- ✅ Validación: switch bloqueado hasta que admin verifique pago
- ✅ Estados visuales claros (badges de colores)

### ✅ FASE 7.4: Gestión de Órdenes y Facturas (100% COMPLETADA)
**Componente:** `MisOrdenes.vue`
**Modelos Backend:** `PlanOrder`, `BlockedUser`
- ✅ Vista de órdenes de planes con facturación
- ✅ Campos: razón social, NIT, CI, complemento CI
- ✅ Email y WhatsApp para factura electrónica
- ✅ Estados simplificados: "En Proceso" y "Completado"
- ✅ Badge verde con gradiente para estado "Completado"
- ✅ Búsqueda avanzada (CI, NIT, email, WhatsApp, empresa, anuncio)
- ✅ Filtros por estado
- ✅ Vista de detalles de orden con logo de empresa
- ✅ Descarga de comprobante de pago
- ✅ Lógica robusta para facturación (validación de razón social y NIT)
- ✅ Mensaje estilizado con gradiente azul para facturas no solicitadas
- ✅ Admin Django para gestión de órdenes
- ✅ Sistema de usuarios bloqueados
- ✅ Script de migración de jobs a órdenes

### ✅ FASE 7.6: Sistema de Aplicaciones a Anuncios (100% COMPLETADA) - Diciembre 2024
**Componentes:** `CandidatesView.vue`, `ApplicationModal.vue`, `ApplyModal.vue`
**Modelos Backend:** `ApplicantCV`, `JobApplication`, `SavedJob`
**Composables:** `useApplications.js`

#### Frontend Completado:
- ✅ **Dashboard Empleador (`CandidatesView.vue`)**
  - ✅ Vista de postulaciones recibidas con CVs PDF
  - ✅ Tarjetas de candidatos con información completa
  - ✅ Cambio de estados: Recibida → En revisión → Preseleccionado → Entrevistado → Aceptado/Rechazado
  - ✅ Descarga de CV PDF (uploaded y created)
  - ✅ Notas del reclutador con auto-guardado
  - ✅ Filtros por estado y búsqueda
  - ✅ Estadísticas de postulaciones (recibidas, en revisión, preseleccionados, aceptados)
  - ✅ Fix crítico de reactividad Vue 3 (triggerRef, watch profundo)

- ✅ **Modal de Postulación (`ApplyModal.vue`)**
  - ✅ Formulario completo de aplicación
  - ✅ CV Builder integrado o subida de PDF
  - ✅ Preguntas de filtrado del anuncio
  - ✅ Carta de presentación
  - ✅ Validación completa
  - ✅ Integración con backend

- ✅ **Modal de Detalles (`ApplicationModal.vue`)**
  - ✅ Vista expandida de postulación
  - ✅ Información del candidato
  - ✅ CV visualización y descarga
  - ✅ Respuestas a preguntas de filtrado
  - ✅ Historial de cambios de estado

#### Backend Completado:
- ✅ Modelo `ApplicantCV` - CVs guardados (uploaded/created)
- ✅ Modelo `JobApplication` - Postulaciones a trabajos
- ✅ Modelo `SavedJob` - Trabajos guardados por postulantes
- ✅ Endpoints API completos:
  - `POST /api/applicants/cv/save/` - Guardar CV
  - `GET /api/applicants/cv/` - Listar CVs del usuario
  - `POST /api/jobs/{id}/apply/` - Aplicar a trabajo
  - `GET /api/jobs/{id}/applications/` - Listar postulaciones (empleador)
  - `PATCH /api/jobs/{id}/applications/{app_id}/` - Actualizar estado
  - `GET /api/user/applications/` - Postulaciones del usuario
  - `POST /api/jobs/{id}/save/` - Guardar trabajo
  - `GET /api/user/saved-jobs/` - Trabajos guardados

#### Composable Completado:
- ✅ `useApplications.js` - Singleton para gestión de postulaciones
- ✅ Carga de aplicaciones por trabajo
- ✅ Actualización de estados con notificación
- ✅ Guardado de notas del reclutador
- ✅ Reactividad forzada con `triggerRef()`
- ✅ Computed con filtros (estado, búsqueda)

### ⏳ FASE 7.7: Notificaciones de Cambio de Estado (0% PENDIENTE)
**Objetivo:** Notificar al postulante cuando el reclutador cambie el estado de su postulación

#### Funcionalidad Requerida:
- ⏳ **Backend: Sistema de Notificaciones**
  - ⏳ Modelo `Notification` en Django con campos:
    - `user` - Usuario destinatario
    - `type` - Tipo (application_status_change, new_message, etc.)
    - `title` - Título de la notificación
    - `message` - Mensaje descriptivo
    - `related_application` - FK a JobApplication
    - `old_status` - Estado anterior
    - `new_status` - Estado nuevo
    - `is_read` - Boolean
    - `created_at` - Timestamp
  - ⏳ Signal en `JobApplication.save()` para crear notificación automática al cambiar estado
  - ⏳ API endpoints:
    - `GET /api/notifications/` - Listar notificaciones del usuario
    - `PATCH /api/notifications/{id}/mark-read/` - Marcar como leída
    - `DELETE /api/notifications/{id}/` - Eliminar notificación

- ⏳ **Frontend: Dashboard Postulante**
  - ⏳ Tab "Mensajes" en dashboard debe mostrar notificaciones
  - ⏳ Contador de notificaciones no leídas en navbar
  - ⏳ Badge rojo con número en ícono de mensajes
  - ⏳ Listado de notificaciones con:
    - Título y mensaje descriptivo
    - Estado anterior → nuevo estado
    - Nombre del trabajo
    - Timestamp relativo
    - Acción para marcar como leída
  - ⏳ Polling o WebSocket para notificaciones en tiempo real
  - ⏳ Sonido/vibración al recibir notificación nueva

#### Mensajes de Notificación por Estado:
```
submitted → reviewing:
"Tu postulación a {job_title} está siendo revisada"

reviewing → shortlisted:
"¡Felicidades! Has sido preseleccionado para {job_title}"

shortlisted → interviewed:
"Has sido seleccionado para entrevista en {job_title}"

interviewed → accepted:
"¡Enhorabuena! Has sido aceptado para {job_title}"

* → rejected:
"Lamentablemente tu postulación a {job_title} no ha sido seleccionada"
```

### ⏳ FASE 7.5: Sistema de Mensajes (60% COMPLETADA)
**Componente:** `MessagesView.vue`
**Estado:** Interfaz frontend completa, backend pendiente
- ✅ Tab de Notificaciones
  - ✅ Lista de notificaciones con tipos (postulaciones, pagos, vencimientos)
  - ✅ Contador de no leídas
  - ✅ Marcar como leída
  - ✅ Timestamps relativos
  - ✅ Iconos y colores por tipo
- ✅ Tab de Contactos
  - ✅ Lista de personas interactuadas
  - ✅ Búsqueda en tiempo real
  - ✅ Botón email directo
  - ✅ Botón WhatsApp directo
  - ✅ Contexto de interacción
- ⏳ **PENDIENTE: Backend**
  - ⏳ Integrar con sistema de notificaciones (FASE 7.7)
  - ⏳ Sistema de chat interno completo (inbox)
  - ⏳ WebSockets o polling para tiempo real
  - ⏳ Modelo `Conversation` y `Message`

---

## 🎯 PRÓXIMAS PRIORIDADES

### 1. **FASE 7.7: Sistema de Notificaciones de Estado** (ALTA PRIORIDAD)
**Descripción:** Notificar automáticamente al postulante cuando el reclutador cambie el estado de su postulación

**Tareas Pendientes:**
- ⏳ Crear modelo `Notification` en Django
- ⏳ Implementar signals para crear notificaciones automáticamente
- ⏳ Crear endpoints API de notificaciones
- ⏳ Integrar notificaciones en dashboard postulante (tab Mensajes)
- ⏳ Contador de notificaciones no leídas en navbar
- ⏳ Sistema de polling o WebSocket para tiempo real

### 2. **FASE 7.8: Gestión de CVs en Dashboard Postulante** (ALTA PRIORIDAD)
**Descripción:** Permitir crear, editar, eliminar y gestionar CVs desde el dashboard del postulante

**Tareas Pendientes:**
- ⏳ Vista "Mis CVs" en dashboard postulante
- ⏳ Botón "Crear Nuevo CV" que abra CV Builder
- ⏳ Listado de CVs guardados (creados y subidos)
- ⏳ Acciones por CV:
  - Editar CV (abrir CV Builder con datos precargados)
  - Eliminar CV (con confirmación)
  - Descargar CV (para PDFs subidos)
  - Vista previa CV
  - Marcar como CV predeterminado
- ⏳ Limite de 2 CVs máximo (según requerimiento CEO)
- ⏳ Indicador de CV usado en postulaciones
- ⏳ Backend: Endpoint `PUT /api/applicants/cv/{id}/` para editar CV
- ⏳ Backend: Endpoint `DELETE /api/applicants/cv/{id}/` para eliminar CV

### ✅ FASE 3: GuideView - Vista Split Mejorada (100% COMPLETADA) - Diciembre 2024
**Componentes:** `GuideView.vue`, `JobListCompact.vue`, `JobDetailPanel.vue`
- ✅ Split view con lista compacta + panel de detalles
- ✅ Lista ancha sin selección, se reduce al hacer clic (40% lista / 60% panel)
- ✅ Panel sticky con tabs: "Oferta Laboral" | "Perfil de Empresa"
- ✅ Logo de empresa en panel junto al título
- ✅ Badges con gradientes (Patrocinado, Destacado, Urgente)
- ✅ Sistema de tabs sin modales
- ✅ Alineación perfecta de tabs con primer card
- ✅ Modal responsive en móvil con overlay
- ✅ Botón X grande y visible
- ✅ Timezone correcto Bolivia (La Paz) para fechas
- ✅ Transición suave entre estados

### 2. **Completar Sistema de Mensajes** (Backend) - Ver FASE 7.7
- ⏳ Modelo `Notification` en Django (ver FASE 7.7)
- ⏳ Endpoints API: /api/notifications/, /api/notifications/mark-read/
- ⏳ Generación automática de notificaciones:
  - ✅ Nueva aplicación recibida (cuando postulante aplica)
  - Cambio de estado de postulación (FASE 7.7)
  - Pago verificado
  - Anuncio próximo a vencer (3 días antes)
  - Plan activado
- ⏳ Sistema de chat interno (futuro)
- ⏳ WebSockets o polling para actualizaciones en tiempo real

### ✅ 3. **Jazzmin Admin Django** (COMPLETADO)
- ✅ Instalado y configurado django-jazzmin
- ✅ Menús jerárquicos organizados (TRABAJOS dropdown principal)
- ✅ Logo personalizado en sidebar, login y favicon
- ✅ Íconos FontAwesome para todos los modelos
- ✅ Tema por defecto Jazzmin (flatly)
- ✅ Badges mejorados con colores tenues
- ⏳ Pendiente: Dashboard con widgets de métricas y gráficos (futuro)




## 🔴 Observaciones Críticas del CEO (Rodrigo)
(tachadas = ya completadas)

### ✅ COMPLETADAS
- ~~Login separado postulantes vs empresas~~
- ~~Planes actualizados en PlanStep con archivo planesupdate.png~~
- ~~Dashboard Postulante → menú limitado (Perfil, CV máx 2, Postulaciones, Favoritos, Mensajes, Historial)~~
- ~~Dashboard Empresa → menú con Perfil Empresa, Mis anuncios, Solicitudes recibidas, Candidatos guardados, Mensajes, Mis órdenes/facturas, Bloqueos~~
- Publicar anuncio → solo usuarios registrados con perfil completo por lo menos el 80% 
- ~~JobsManager.vue → botones estilizados, switch activar/desactivar anuncio, edición en modal~~
- ~~CustomUser con roles → candidate vs company, perfiles vinculados~~
- ~~Sistema de órdenes de planes con facturación~~
- ~~Validación de pagos con switch bloqueado hasta aprobación admin~~
- Gestión de usuarios bloqueados por empresas falta funcionalidad
- ~~CRUD dinámico de categorías y subcategorías (JobCategory, ContractType, City)~~
- Sistema de auditoría completo para rastrear todas las acciones(errores: el sitema a menudo confunde las acciones ejemplo estoy
logeado como empresa pero al registrarse algun evento editar o eliminar detecta como postulante error critico corregir)
- Sistema de reportes diarios con métricas de usuarios, trabajos, planes e ingresos falta funcionalidad
- ~~Admin Django mejorado con badges de colores y filtros avanzados~~
- ~~Badge verde gradiente para órdenes completadas~~
- ~~Mensaje estilizado para facturas no solicitadas~~
- ~~Logo de empresa en vista de órdenes~~

### ⏳ EN PROGRESO
- Mensajes → Interfaz híbrida lista (notificaciones + contactos con email/WhatsApp), falta backend para chat interno completo

### 📋 PENDIENTES (ALTA PRIORIDAD)
- ~~**Sistema de aplicaciones desde JobDetailView**~~ ✅ COMPLETADO (FASE 7.6)
- **Sistema de notificaciones de cambio de estado** - Ver FASE 7.7 (ALTA PRIORIDAD)
- **Gestión de CVs en dashboard postulante** - Ver FASE 7.8 (ALTA PRIORIDAD)
- **Backend de notificaciones** - Crear modelo Notification y endpoints API (FASE 7.7)
- ~~**Admin Django con Jazzmin** - Menús anidados sobre Jobs en sidebar izquierdo dropdown~~ ✅ COMPLETADO
- **Dashboard con gráficos en Admin** - Widgets de métricas visuales y tendencias (futuro) 