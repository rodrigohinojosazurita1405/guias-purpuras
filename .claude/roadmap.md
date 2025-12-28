# Guías Púrpuras - ROADMAP Completo MVP

## 📊 ESTADO ACTUAL - PROGRESO GENERAL
FASE 1: Wizard de Publicación              ✅ 100% COMPLETADA
FASE 1.1: Preguntas de Filtrado            ✅ 100% COMPLETADA
FASE 1.2: Formulario Aplicación Candidato  ✅ 100% COMPLETADA
FASE 2: Flujo de Publicación Completo      ✅ 100% COMPLETADA
FASE 3: Búsqueda y Filtrado GuideView      ✅ 100% COMPLETADA
FASE 3.6: Autenticación Real               ✅ 100% COMPLETADA
FASE 3.6.1: Recuperación de Contraseña     ✅ 100% COMPLETADA
FASE 3.6.2: Mejoras UX/UI Auth Forms       ✅ 100% COMPLETADA
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
FASE 11.1: Mejoras UX/UI Admin + Frontend  ✅ 100% COMPLETADA


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

### ✅ FASE 3.6.1: Sistema de Recuperación de Contraseña (100% COMPLETADA) - Diciembre 2024
**Archivos:** `auth_api/models.py`, `auth_api/views.py`, `core/settings.py`, `ForgotPasswordForm.vue`, `ResetPasswordForm.vue`
**Commits:** `e3bbf25` - Correcciones UX/UI auth forms

#### Backend Completado:
- ✅ **Modelo PasswordResetToken**
  - ✅ Token seguro generado con `secrets.token_urlsafe(32)`
  - ✅ Validación de 1 hora de expiración
  - ✅ Método `is_valid()` para verificar tokens no usados y no expirados
  - ✅ Método estático `create_for_user()` - invalida tokens anteriores y crea nuevo
  - ✅ Relación ForeignKey con CustomUser

- ✅ **Endpoints API**
  - ✅ `POST /api/auth/forgot-password` - Solicitar recuperación
  - ✅ `POST /api/auth/reset-password` - Restablecer contraseña con token
  - ✅ Validación robusta de email y contraseña
  - ✅ Seguridad: No revela si email existe o no

- ✅ **Configuración de Email**
  - ✅ Desarrollo: Console backend para localhost
  - ✅ Producción: SMTP con variables de entorno
  - ✅ Documentación completa para deployment en Render
  - ✅ Email con URL de reset personalizada según entorno
  - ✅ Plantilla de email profesional

#### Frontend Completado:
- ✅ **ForgotPasswordForm.vue**
  - ✅ Formulario de solicitud de recuperación
  - ✅ Validación de email en tiempo real
  - ✅ Mensajes de éxito/error claros
  - ✅ Diseño consistente con LoginForm y RegisterForm
  - ✅ Responsive design completo

- ✅ **ResetPasswordForm.vue**
  - ✅ Formulario de nueva contraseña con token
  - ✅ Validación de contraseña y confirmación
  - ✅ Mostrar/ocultar contraseña
  - ✅ Indicador de fortaleza de contraseña
  - ✅ Manejo de tokens inválidos o expirados
  - ✅ Redirección automática a login después de éxito

#### Testing Completado:
- ✅ **Scripts de prueba automatizados**
  - ✅ `test_password_recovery.py` - Pruebas manuales paso a paso
  - ✅ `test_password_recovery_auto.py` - Pruebas automatizadas (5/5 pasadas)
  - ✅ Extracción automática de tokens desde base de datos
  - ✅ Validación de flujo completo: registro → forgot → reset → login

### ✅ FASE 3.6.2: Mejoras UX/UI en Formularios de Autenticación (100% COMPLETADA) - Diciembre 2024
**Archivos:** `LoginForm.vue`, `RegisterForm.vue`, `ForgotPasswordForm.vue`, `ResetPasswordForm.vue`
**Commits:** `e3bbf25` - fix: Corregir alineación de íconos y mejorar UX

#### Mejoras Aplicadas en Todos los Formularios:
- ✅ **Alineación de íconos corregida**
  - ✅ Cambio de `top: 50%; transform: translateY(-50%)` a `top: 14px` fijo
  - ✅ Íconos ahora se mantienen alineados con inputs incluso cuando aparecen mensajes de error
  - ✅ Soluciona problema de desplazamiento vertical al validar

- ✅ **RegisterForm - Mejoras específicas**
  - ✅ Labels dinámicos según rol seleccionado (empresa/postulante)
  - ✅ "Nombre Completo" → "Nombre de la Empresa" si rol = company
  - ✅ "Correo Electrónico" → "Correo Electrónico de la Empresa" si rol = company
  - ✅ Header con Bolivia flag y gradiente púrpura
  - ✅ Animación suave "gentle-float" en bandera (3px vertical)
  - ✅ Checkbox de términos y condiciones alineado correctamente
  - ✅ Labels de estadísticas en blanco con `!important` (forzar override)
  - ✅ Fix de espacios vacíos en dropdowns con `select.form-input option { padding-left: 0.5rem; }`

- ✅ **LoginForm - Mejoras de navegación**
  - ✅ Redirección post-login unificada a `/dashboard` para todos los usuarios
  - ✅ Simplificación de lógica de redirección (antes: empresa → jobs-manager, postulante → profile)
  - ✅ Header con Bolivia flag y gradiente
  - ✅ Diseño consistente con RegisterForm

- ✅ **Optimizaciones móviles (todos los formularios)**
  - ✅ Breakpoints consistentes: 1024px (tablets), 640px (móviles), 375px (móviles pequeños)
  - ✅ Input `font-size: 16px` en móvil para prevenir auto-zoom en iOS
  - ✅ Áreas táctiles mejoradas: `min-height: 48px` en inputs y botones (WCAG 2.1)
  - ✅ Padding y espaciado optimizado por breakpoint
  - ✅ Íconos y logos escalados apropiadamente
  - ✅ Bandera de Bolivia responsive (28px → 22px → 20px)
  - ✅ Headers con tamaños de fuente progresivos

#### Resultado:
- ✅ Íconos perfectamente alineados en todos los estados de validación
- ✅ Dropdowns sin espacios vacíos molestos
- ✅ Labels de estadísticas visibles en blanco sobre fondo púrpura
- ✅ Navegación post-login más intuitiva y consistente
- ✅ Experiencia móvil optimizada y profesional

### ✅ FASE 11.1: Mejoras de UX/UI Admin y Frontend (100% COMPLETADA) - Diciembre 2024
**Archivos:** `jobs/admin.py`, `PublishSuccessModal.vue`, `SummaryCard.vue`, `InformationStepJob.vue`, `PublishView.vue`
**Commits:**
- `a2a4931` - Mejorar interfaz del admin de Django para verificación de pagos
- `49d530d` - Mejoras en editor Quill y UI del formulario de publicación

#### Admin Django - Verificación de Pagos:
- ✅ **Widget personalizado destacado para checkbox 'Pago verificado'**
  - ✅ Diseño tipo tarjeta con fondo de color según estado
  - ✅ Verde (#ECFDF5) si verificado / Amarillo (#FFFBEB) si pendiente
  - ✅ Íconos SVG profesionales (check ✓ o reloj según estado)
  - ✅ Tamaño compacto y discreto (14px 18px padding)
  - ✅ Bordes sutiles (2px) y sombras suaves (0.15 opacity)
  - ✅ Label descriptivo según estado con colores coordinados
  - ✅ Checkbox escalado 1.3x para mejor visibilidad

- ✅ **Mejoras en badges de lista de ofertas**
  - ✅ Badge 'Estado de Pago' ahora sutil e igual a los demás
  - ✅ Eliminados gradientes y sombras exageradas
  - ✅ Etiquetas simplificadas: "Verificado", "Pendiente", "Sin Comprobante"
  - ✅ Removido emoji 💰 del título de columna
  - ✅ Reemplazados emojis por íconos SVG en badges:
    - ✅ Aplicaciones: ícono SVG de usuarios (reemplaza 👥)
    - ✅ Vistas: ícono SVG de ojo (reemplaza 👁️)
    - ✅ Publicado: ícono SVG de calendario (reemplaza 📅)
    - ✅ Plan: ícono SVG de estrella (reemplaza 💎)
  - ✅ Mantenidos emojis en badge de vencimiento (🔴🟡🟢) - funcionan mejor que SVG
  - ✅ Todos los badges ahora con estilo consistente y profesional

#### Frontend - Modal de Éxito y SummaryCard:
- ✅ **Modal de publicación exitosa más compacto**
  - ✅ Tamaño reducido de 'large' a 'medium'
  - ✅ Padding reducido de 30px a 20px (33% menor)
  - ✅ Ícono de éxito de 70px (antes 100px)
  - ✅ Título de 22px (antes 28px)
  - ✅ Fuentes reducidas en 15-20%
  - ✅ Márgenes y espaciados reducidos en 30-50%
  - ✅ Sin pérdida de funcionalidad ni contenido

- ✅ **SummaryCard responsive mejorado**
  - ✅ Layout de header reorganizado a 3 columnas más compacto
  - ✅ Badges responsivos con tamaños específicos por breakpoint
  - ✅ Logo de empresa más grande en móvil (140px en 480px, 120px en 768px)
  - ✅ Título y logo lado a lado en responsive
  - ✅ Gap reducido en badges (0.2rem en móvil)
  - ✅ Alineación a la izquierda en móvil
  - ✅ Fuentes aumentadas para mejor legibilidad
  - ✅ Color púrpura (#7C3AED) en label "Oferta laboral"
  - ✅ **Badges limpios sin iconos** (Destacado, Urgente, Patrocinado)
  - ✅ **Badges más compactos en desktop** (0.4rem padding, font 0.7rem)
  - ✅ **Headers H1-H6 neutralizados** en descripción de trabajo (forzados a <p>)

#### Frontend - Editor Quill y Formulario:
- ✅ **InformationStepJob.vue - Editor Quill mejorado**
  - ✅ **Conversión automática H1-H6 → <p>** en evento `text-change`
  - ✅ Filtro de expresiones regulares para limpiar headers del HTML
  - ✅ CSS neutralizador de headers en editor (font-size 1rem, peso normal)
  - ✅ Restricción de formatos permitidos (sin 'header' en array)
  - ✅ Consistencia visual entre editor, resumen y Django admin

- ✅ **PublishView.vue - Modal de confirmación "Limpiar borrador"**
  - ✅ Reemplazo de `confirm()` nativo por VaModal personalizado
  - ✅ Sin efecto blur (fondo semi-transparente limpio)
  - ✅ Ancho máximo 450px en desktop (compacto y centrado)
  - ✅ Diseño responsive optimizado para móvil
  - ✅ Botones apilados verticalmente en móvil (fácil de usar)
  - ✅ Botón principal primero en móvil ("Sí, limpiar" arriba)
  - ✅ Mensaje personalizado sin referencias a localhost

- ✅ **jobs/views.py - Limpieza de código**
  - ✅ Eliminados prints de debug en endpoint de categorías dinámicas

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

### 1. **FASE 7.9: Mejoras Dashboard Reclutador - CandidatesView** (ALTA PRIORIDAD)
**Descripción:** Funcionalidades críticas para gestión eficiente de candidatos con alto volumen de solicitudes

**Contexto:**
- Con 50+ candidatos por trabajo, se vuelve imposible gestionar sin herramientas avanzadas
- Basado en análisis de plataformas profesionales (LinkedIn Recruiter, Greenhouse, Lever)

**Tareas Priorizadas:**

#### **FASE 1 - LO MÁS CRÍTICO** (2-3 horas total)
1. ⏳ **Puntuación/Rating de Candidatos** ⭐ (2-3 horas)
   - Sistema de estrellas 1-5 para calificar candidatos
   - Ordenar por mejor puntuación
   - Campo `rating` en modelo `JobApplication`
   - Componente de estrellas clickeable en cada tarjeta
   - Filtro adicional "Ordenar por: Rating"
   - **JUSTIFICACIÓN:** Esencial para priorizar rápidamente. Usado DIARIAMENTE en 90%+ de ATS profesionales

2. ⏳ **Filtros Avanzados** 🔍 (4-6 horas)
   - Filtrar por fecha de aplicación (última semana, último mes, etc.)
   - Filtrar por años de experiencia (si se captura en CV)
   - Filtrar por ubicación/ciudad
   - Filtro combinado (múltiples criterios simultáneos)
   - **JUSTIFICACIÓN:** Crítico con volumen alto. Sin esto, 50+ candidatos es caos total

#### **FASE 2 - MUY ÚTIL** (5-7 horas total)
3. ⏳ **Acciones en Lote** ⚡ (3-4 horas)
   - Checkbox para seleccionar múltiples candidatos
   - Botón "Cambiar estado de seleccionados"
   - Botón "Rechazar seleccionados"
   - Botón "Mover a preseleccionados"
   - Confirmar antes de acción masiva
   - **JUSTIFICACIÓN:** Ahorra MUCHO tiempo. Cuando recibes 100 CVs y 70 no califican, rechazar todos de golpe

4. ⏳ **Exportación a Excel/CSV** 📊 (2-3 horas)
   - Botón "Exportar a Excel"
   - Incluir: Nombre, Email, Teléfono, WhatsApp, Estado, Rating, Fecha aplicación
   - Opción de exportar solo seleccionados o todos
   - Formato profesional con headers
   - **JUSTIFICACIÓN:** Muy pedido para reportes a gerencia. Común en todas las empresas

#### **FASE 3 - SI HAY TIEMPO** (6-8 horas)
5. ⏳ **Comunicación Directa con Templates** 💬 (6-8 horas)
   - Botón "Enviar Email" en cada candidato
   - Modal con editor de email
   - Templates predefinidos:
     - "Gracias por aplicar"
     - "Rechazado cortésmente"
     - "Invitación a entrevista"
     - "Solicitud de más información"
   - Variables dinámicas: {nombre}, {puesto}, {empresa}
   - Registro de emails enviados en notas
   - **JUSTIFICACIÓN:** Ahorra horas de escribir emails repetitivos. Muy valorado pero no crítico

**Estimación total:** 15-20 horas de desarrollo

**Orden de implementación sugerido:**
1. Puntuación/Rating (impacto inmediato, fácil)
2. Filtros Avanzados (crítico con volumen)
3. Acciones en Lote (gran ahorro de tiempo)
4. Exportación Excel (rápido de hacer, muy pedido)
5. Templates Email (si hay tiempo)

### 2. **FASE 7.7: Sistema de Notificaciones de Estado** (ALTA PRIORIDAD)
**Descripción:** Notificar automáticamente al postulante cuando el reclutador cambie el estado de su postulación

**Tareas Pendientes:**
- ⏳ Crear modelo `Notification` en Django
- ⏳ Implementar signals para crear notificaciones automáticamente
- ⏳ Crear endpoints API de notificaciones
- ⏳ Integrar notificaciones en dashboard postulante (tab Mensajes)
- ⏳ Contador de notificaciones no leídas en navbar
- ⏳ Sistema de polling o WebSocket para tiempo real

### 2. **FASE 7.8: Gestión de CVs en Dashboard Postulante** (🔴 CRÍTICO - EN PROGRESO 85%)
**Descripción:** Permitir crear, editar, eliminar y gestionar CVs desde el dashboard del postulante

**Tareas Completadas:**
- ✅ Vista "Mis CVs" en dashboard postulante (`CVManager.vue`)
- ✅ Botón "Crear CV en Plataforma" que abre modal con CV Builder
- ✅ Listado de CVs guardados (creados y subidos) con grid responsivo
- ✅ Límite de 2 CVs máximo validado (frontend y backend)
- ✅ Warnings visuales cuando se alcanza el límite
- ✅ Backend: Endpoint `POST /api/cvs/save/` - Guardar CV creado
- ✅ Backend: Endpoint `GET /api/cvs/list/` - Listar CVs del usuario
- ✅ Backend: Endpoint `DELETE /api/cvs/{id}/delete/` - Eliminar CV
- ✅ Backend: Endpoint `PATCH /api/cvs/{id}/update/` - Actualizar CV completo
- ✅ Backend: Endpoint `GET /api/cvs/{id}/` - Obtener detalle de CV para edición
- ✅ Integración CreateCV.vue en modal (formato Harvard completo)
- ✅ Validación de campos obligatorios (Nombre, Email, Teléfono)
- ✅ Sistema de badges temporales inteligentes:
  - ✅ Badge "NUEVO" (morado) para CVs creados hace menos de 48 horas
  - ✅ Badge "ACTUALIZADO" (verde) para CVs modificados hace menos de 24 horas
  - ✅ Badges desaparecen automáticamente después del tiempo establecido
- ✅ Metadata de CVs (creado, actualizado)
- ✅ Fix de reactividad v-model entre CVManager ↔ CreateCV
- ✅ Modal sin overlay oscuro (UX mejorada)
- ✅ **CRUD Completo de CVs**:
  - ✅ Editar CV creado en plataforma (wizard con datos precargados vía query param)
  - ✅ Componente `CVBuilderView.vue` - Wizard de 6 pasos para crear/editar CV
  - ✅ Componente `CVStepsIndicator.vue` - Indicador visual de progreso (estilo PublishStepsIndicator)
  - ✅ Eliminar CV con confirmación
  - ✅ Navegación dedicada en `/dashboard/cv/builder`
  - ✅ Edición inline del nombre del CV (click-to-edit con Enter/Esc)
  - ✅ Reorganización de archivos a carpeta `ProcessCV/`
  - ✅ Sincronización completa frontend-backend verificada
  - ✅ Corrección de ruta de endpoint de detalle de CV
- ✅ **Mejoras de UX/UI**:
  - ✅ Header mejorado con información del formato Harvard
  - ✅ Título con gradiente: "Mis CVs Profesionales"
  - ✅ Descripción ampliada sobre ventajas del formato Harvard
  - ✅ 3 badges informativos: "Formato Profesional", "Creación Rápida", "Mayor Impacto"
  - ✅ Diseño moderno con fondo degradado y bordes sutiles
  - ✅ Tarjetas de CV rediseñadas con mejor jerarquía visual
  - ✅ Edición inline de nombres con iconos y feedback visual
  - ✅ Responsive design completo (mobile-first)

**Tareas Pendientes (🔴 CRÍTICAS):**
- 🔴 **Vista Previa y Descarga de CV**:
  - ⏳ Descargar CV en formato PDF (para CVs creados en plataforma)

- 🔴 **Vista Previa HTML de CV Creado**:
  - ⏳ Componente `CVPreview.vue` para renderizar CV en formato Harvard profesional
  - ⏳ Diseño HTML/CSS profesional con estilos de CV (inspirado en Harvard)
  - ⏳ Secciones: Datos personales, perfil, educación, experiencia, habilidades, certificaciones, idiomas, proyectos
  - ⏳ Botón "Vista Previa" que abra modal con CV renderizado
  - ⏳ Generación de PDF desde HTML (usar jsPDF o html2pdf.js)
  - ⏳ Vista previa debe ser lo que vea el reclutador si el postulante elige CV del sistema

- 🔴 **Mejoras Críticas de UX/UI**:
  - ⏳ Rediseñar tarjeta de CV (`cv-card`) - actualmente muy básica
  - ⏳ Agregar avatares o íconos más atractivos según tipo de CV
  - ⏳ Animaciones suaves en hover y transiciones
  - ⏳ Mejor visualización de metadata (fecha creación/actualización)
  - ⏳ Badge de "CV Predeterminado" si se implementa esa funcionalidad
  - ⏳ Indicador visual de "CV usado en X postulaciones"
  - ⏳ Skeleton loaders mientras carga CVs
  - ⏳ Empty state más atractivo con ilustración

- 🔴 **Funcionalidades Adicionales Recomendadas**:
  - ⏳ Marcar CV como predeterminado (se pre-selecciona al aplicar)
  - ⏳ Duplicar CV (crear copia para modificar sin perder original)
  - ⏳ Historial de versiones de CV (opcional, futuro)
  - ⏳ Compartir CV vía link público (opcional, futuro)
  - ⏳ Estadísticas: "Este CV fue usado en X postulaciones"
  - ⏳ Vista comparativa lado a lado de 2 CVs
  - ⏳ Sugerencias de IA para mejorar CV (futuro con OpenAI)

- 🔴 **Integración con ApplicationModal**:
  - ⏳ Al aplicar a trabajo, si usuario selecciona "Mis CVs":
    - Debe poder elegir entre sus CVs guardados
    - Si selecciona CV creado en plataforma → enviar vista previa HTML al reclutador
    - Si selecciona CV subido (PDF) → enviar archivo PDF
  - ⏳ Backend debe soportar `application.cv_preview_html` para CVs creados
  - ⏳ CandidatesView debe mostrar vista previa HTML si existe, sino PDF

- 🔴 **Validaciones y Seguridad**:
  - ⏳ Validar que usuario no pueda eliminar CV si está siendo usado en postulación activa
  - ⏳ Confirmar eliminación con mensaje: "Este CV está siendo usado en X postulaciones"
  - ⏳ Sanitizar HTML de vista previa para evitar XSS
  - ⏳ Rate limiting en creación de CVs (evitar spam)

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

---

## 📅 SESIÓN DE TRABAJO - 27 Diciembre 2024

### ✅ MEJORAS Y CORRECCIONES COMPLETADAS

#### 1. Nueva Opción de Salario: "Pretensión Salarial" ✅
**Commits:** `6bdc343`
**Archivos modificados:** 8 archivos (backend + frontend)

**Backend:**
- ✅ `models.py`: Agregada opción 'pretension_salarial' al campo salaryType
- ✅ `views.py`: Actualizada validación para aceptar 'pretension_salarial'
- ✅ `views.py`: Actualizada función `format_salary()` para mostrar "Indique su pretensión salarial"
- ✅ Migración `0034_add_pretension_salarial_option.py` creada y aplicada

**Frontend:**
- ✅ `InformationStepJob.vue`: Agregado 4to radio button "Pretensión Salarial"
- ✅ `InformationStepJob.vue`: Limpieza de logs de debug en validateApplicationDeadline
- ✅ `SummaryCard.vue`: Agregados templates para mostrar "Indique su pretensión salarial" en ambas secciones de salario
- ✅ `SummaryCard.vue`: Cambiado label "Rango Salarial:" a "Salario:" (más genérico)
- ✅ `useApplicationStore.js`: Actualizado `requiresSalaryExpectation` y `salaryDisplayText`
- ✅ `JobDetailPanel.vue`: Agregado case para pretension_salarial en formattedSalary
- ✅ `ShortlistedView.vue`: Agregado mapping en getSalaryLabel()

**Comportamiento:**
- Cuando el reclutador selecciona "Pretensión Salarial", no se muestran campos de entrada
- El sistema muestra "Indique su pretensión salarial" en todas las vistas
- Los candidatos DEBEN proporcionar su expectativa salarial al postular (obligatorio)

#### 2. Fix: Visualización de Aplicación Externa en SummaryCard ✅
**Commits:** `5d9aec2`, `57514f0`, `b579e27`, `78c63a5`

**Problema identificado:**
- SummaryCard tiene DOS layouts: antiguo (líneas 13-373) y nuevo para jobs "Estilo Trabajito" (línea 378+)
- Los datos de aplicación externa solo se mostraban en layout antiguo
- Los datos SÍ llegaban correctamente al componente (verificado con console.log)

**Solución implementada:**
- ✅ Agregada sección completa "Información de Aplicación Externa" en layout de jobs
- ✅ Nueva sección muestra:
  - URL del formulario (clickeable con ícono external)
  - Instrucciones de aplicación (formato especial destacado)
  - Email de contacto (condicional)
  - WhatsApp/Teléfono (condicional)
  - Sitio Web (condicional)
- ✅ Estilos CSS profesionales con cards individuales y hover effects
- ✅ Íconos específicos para cada tipo de contacto
- ✅ Todos los íconos en color púrpura (#7C3AED)
- ✅ Espaciado mejorado (margin-bottom: 2rem) entre secciones

#### 3. Fix: Preservar applicationDeadline al Navegar entre Pasos ✅
**Commits:** `a5b9bc3`
**Archivo:** `InformationStepJob.vue`

**Problema:**
- Al volver atrás desde SummaryCard, el campo "Fecha límite postulación" se reseteaba
- Usuario debía llenar nuevamente el campo cada vez

**Causa:**
- La función `initializeFormData()` no incluía `applicationDeadline` en la inicialización

**Solución:**
- ✅ Agregado `applicationDeadline: modelValue.applicationDeadline || null` en línea 416
- ✅ Ahora el valor se preserva correctamente al navegar entre pasos

#### 4. Fix: Limpiar Datos al Cambiar Tipo de Aplicación ✅
**Commits:** `63decf8`
**Archivos:** `ApplicationConfigStep.vue`, `JobDetailModal.vue`

**Problema:**
- Al cambiar de "Aplicación Interna" a "Externa" (o viceversa), los datos del tipo anterior NO se limpiaban
- Esto causaba que se guardaran preguntas de filtrado en aplicaciones externas (donde no deberían existir)
- En JobDetailModal, las preguntas de filtrado se mostraban SIEMPRE, incluso para aplicaciones externas

**Solución:**
1. **ApplicationConfigStep.vue:**
   - ✅ Modificada función `updateData()` para limpiar datos específicos al cambiar tipo
   - ✅ Si cambia a "external": limpia screeningQuestions (array vacío)
   - ✅ Si cambia a "internal": limpia campos externos (URL, instrucciones, email, whatsapp, website)

2. **JobDetailModal.vue:**
   - ✅ Agregada condición `v-if="['internal', 'both'].includes(job.applicationType)"`
   - ✅ Sección "Preguntas de Filtrado" solo aparece cuando es aplicable

**Resultado:**
- Al cambiar entre tipos de aplicación, se limpian automáticamente los campos del tipo anterior
- No más mezcla de datos entre tipos de aplicación diferentes

#### 5. Mejoras de Experiencia de Usuario (UX) ✅
**Commits:** `5d9aec2`, `b579e27`, `78c63a5`

- ✅ Console.log de debug agregado en SummaryCard (líneas 1295-1306) para diagnóstico
- ✅ Íconos en color púrpura consistente con diseño del sitio
- ✅ Links clickeables con ícono "abrir en nueva ventana"
- ✅ Instrucciones con formato especial (borde izquierdo morado, fondo suave, texto itálico)
- ✅ Separación visual mejorada entre secciones

### 📊 RESUMEN DE LA SESIÓN

**Commits creados:** 7 commits
1. `6bdc343` - feat: Agregar opción 'Pretensión Salarial' al sistema de salarios
2. `5d9aec2` - fix: Mostrar todos los campos de contacto en SummaryCard para aplicación externa (primer intento)
3. `a5b9bc3` - fix: Preservar applicationDeadline al navegar entre pasos del formulario
4. `57514f0` - fix: Mostrar información de aplicación externa en layout de jobs de SummaryCard (fix completo)
5. `b579e27` - style: Cambiar íconos de aplicación externa a color púrpura
6. `78c63a5` - style: Mejorar espaciado entre secciones en SummaryCard
7. `63decf8` - fix: Limpiar datos al cambiar tipo de aplicación y ocultar preguntas si es externa

**Archivos modificados:** 10 archivos únicos
- Backend: `models.py`, `views.py`, migración 0034
- Frontend: `InformationStepJob.vue`, `SummaryCard.vue`, `ApplicationConfigStep.vue`, `JobDetailModal.vue`, `useApplicationStore.js`, `JobDetailPanel.vue`, `ShortlistedView.vue`

**Líneas de código:** ~200+ líneas agregadas/modificadas

**Problemas resueltos:**
1. ✅ Sistema de salarios ahora soporta "Pretensión Salarial" como 4ta opción
2. ✅ Información de aplicación externa se muestra correctamente en SummaryCard
3. ✅ Fecha límite de postulación se preserva al navegar entre pasos
4. ✅ Datos se limpian automáticamente al cambiar tipo de aplicación
5. ✅ Preguntas de filtrado solo se muestran para aplicaciones internas

**Calidad del código:**
- ✅ Commits descriptivos con mensajes detallados
- ✅ Separación clara de responsabilidades (backend/frontend)
- ✅ Código bien documentado
- ✅ Estilos CSS profesionales y consistentes
- ✅ Validaciones robustas
- ✅ UX/UI mejorada significativamente

--- 