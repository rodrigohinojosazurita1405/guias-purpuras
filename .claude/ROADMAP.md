# Guías Púrpuras - ROADMAP Completo MVP

## 📊 ESTADO ACTUAL - PROGRESO GENERAL
FASE 1: Wizard de Publicación              ✅ 100% COMPLETADA
FASE 1.1: Preguntas de Filtrado            ✅ 100% COMPLETADA
FASE 1.2: Formulario Aplicación Candidato  ✅ 100% COMPLETADA
FASE 2: Flujo de Publicación Completo      ✅ 100% COMPLETADA
FASE 3: Búsqueda y Filtrado GuideView      ⏳ 0% PENDIENTE
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
FASE 7.6: Aplicaciones a Anuncios          ⏳ 0% PENDIENTE

FASE 8: Sistema de Auditoría               ✅ 100% COMPLETADA
FASE 9: Sistema de Reportes Diarios        ✅ 100% COMPLETADA
FASE 10: CRUD dinámico de categorías       ✅ 100% COMPLETADA
FASE 11: Admin Django mejorado             ✅ 85% (Falta Jazzmin)
FASE 12: Dashboard multi-rol               ⏳ 0% PENDIENTE
FASE 13: Multi-guía (gastronomía, etc)     ⏳ 0% PENDIENTE

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

### ✅ FASE 11: Admin Django Mejorado (85% COMPLETADA) - Diciembre 2024
**Archivos:** `jobs/admin.py`, `plans/admin.py`, `audit/admin.py`, `reports/admin.py`

- ✅ Badges de colores para estados (pending, active, completed, etc.)
- ✅ Visualización mejorada de PlanOrder con datos de facturación
- ✅ Filtros avanzados en todos los modelos
- ✅ Búsqueda optimizada con múltiples campos
- ✅ Acciones bulk personalizadas
- ✅ Vistas de solo lectura para logs de auditoría
- ✅ Displays personalizados con format_html
- ✅ Ordenamiento por defecto optimizado
- ✅ CustomUser admin con roles y permisos
- ⏳ Pendiente: Integración con Jazzmin para menús anidados

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
  - ⏳ Modelo `Notification` en Django
  - ⏳ API endpoints para notificaciones
  - ⏳ Sistema de chat interno completo (inbox)
  - ⏳ WebSockets o polling para tiempo real
  - ⏳ Modelo `Conversation` y `Message`

---

## 🎯 PRÓXIMAS PRIORIDADES

### 1. **FASE 7.6: Sistema de Aplicaciones a Trabajos** (ALTA PRIORIDAD)
- Modelo `Application` en Django para postulaciones
- Botón "Aplicar" en `JobDetailView`
- Formulario de aplicación con:
  - Preguntas de filtrado del anuncio
  - Subida de CV (PDF, DOC, DOCX)
  - Carta de presentación opcional
  - Respuestas a preguntas personalizadas
- Vista de aplicaciones recibidas en dashboard empresa
- Contador de aplicaciones nuevas en tiempo real
- Filtrado y búsqueda de candidatos
- Estados: nueva, en revisión, descartada, preseleccionada

### 2. **FASE 3: Búsqueda y Filtrado en GuideView** (ALTA PRIORIDAD)
- Destacar anuncios según plan:
  - Impulso: Banner destacado superior
  - Púrpura: Badge especial "Destacado" + borde morado
  - Estándar: Vista normal
- Filtros avanzados:
  - Por categoría, ciudad, tipo de contrato
  - Rango salarial
  - Fecha de publicación
  - Experiencia requerida
- Paginación con scroll infinito
- Anuncios similares/relacionados
- Guardado de búsquedas favoritas

### 3. **Completar Sistema de Mensajes** (Backend)
- Modelo `Notification` en Django
- Endpoints API: /api/notifications/, /api/notifications/mark-read/
- Generación automática de notificaciones:
  - Nueva aplicación recibida
  - Pago verificado
  - Anuncio próximo a vencer (3 días antes)
  - Plan activado
- Sistema de chat interno (futuro)
- WebSockets o polling para actualizaciones en tiempo real

### 4. **Integrar Jazzmin en Admin Django**
- Instalar y configurar django-jazzmin
- Menús anidados por secciones
- Dashboard con widgets de métricas
- Tema personalizado con colores de marca
- Gráficos de tendencias integrados




## 🔴 Observaciones Críticas del CEO (Rodrigo)
(tachadas = ya completadas)

### ✅ COMPLETADAS
- ~~Login separado postulantes vs empresas~~
- ~~Planes actualizados en PlanStep con archivo planesupdate.png~~
- ~~Dashboard Postulante → menú limitado (Perfil, CV máx 2, Postulaciones, Favoritos, Mensajes, Historial)~~
- ~~Dashboard Empresa → menú con Perfil Empresa, Mis anuncios, Solicitudes recibidas, Candidatos guardados, Mensajes, Mis órdenes/facturas, Bloqueos~~
- ~~Publicar anuncio → solo usuarios registrados con perfil completo + foto/logo obligatorio~~
- ~~JobsManager.vue → botones estilizados, switch activar/desactivar anuncio, edición en modal~~
- ~~CustomUser con roles → candidate vs company, perfiles vinculados~~
- ~~Sistema de órdenes de planes con facturación~~
- ~~Validación de pagos con switch bloqueado hasta aprobación admin~~
- ~~Gestión de usuarios bloqueados por empresas~~
- ~~CRUD dinámico de categorías y subcategorías (JobCategory, ContractType, City)~~
- ~~Sistema de auditoría completo para rastrear todas las acciones~~
- ~~Sistema de reportes diarios con métricas de usuarios, trabajos, planes e ingresos~~
- ~~Admin Django mejorado con badges de colores y filtros avanzados~~
- ~~Badge verde gradiente para órdenes completadas~~
- ~~Mensaje estilizado para facturas no solicitadas~~
- ~~Logo de empresa en vista de órdenes~~

### ⏳ EN PROGRESO
- Mensajes → Interfaz híbrida lista (notificaciones + contactos con email/WhatsApp), falta backend para chat interno completo

### 📋 PENDIENTES (ALTA PRIORIDAD)
- **Sistema de aplicaciones desde JobDetailView** - Permitir a postulantes aplicar a trabajos
- **GuideView mejorado** - Destacar anuncios según plan, filtros avanzados, paginación
- **JobDetailView** - Mejor UI, guardar/compartir anuncios, mostrar similares
- **Backend de notificaciones** - Crear modelo Notification y endpoints API
- **Admin Django con Jazzmin** - Menús anidados, dashboard con gráficos