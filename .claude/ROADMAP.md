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

FASE 8: Admin Django Jazzmin con menús anidados y reportes
FASE 9: Dashboard multi-rol y multi-guía (trabajos, gastronomía, negocios, profesionales)
FASE 10: CRUD dinámico de categorías y subcategorías
FASE 11: CRUD y visualización mejorada en app Plans

---

## 📝 DETALLES DE FASES COMPLETADAS RECIENTEMENTE

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
- ✅ Búsqueda avanzada (CI, NIT, email, WhatsApp, empresa, anuncio)
- ✅ Filtros por estado
- ✅ Vista de detalles de orden
- ✅ Descarga de comprobante de pago
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

### 1. **Completar Sistema de Mensajes** (Backend)
- Crear modelo `Notification` en Django
- Endpoints para crear/leer/actualizar notificaciones
- Generar notificaciones automáticas (nueva postulación, pago verificado, anuncio por vencer)
- Sistema de chat interno (futuro)

### 2. **FASE 7.6: Sistema de Aplicaciones**
- Aplicar a anuncios desde `JobDetailView`
- Formulario de aplicación con preguntas de filtrado
- Subida de CV
- Gestión de aplicaciones en dashboard empresa

### 3. **Mejoras en GuideView**
- Destacar anuncios según plan (Púrpura con badge especial)
- Filtros avanzados
- Paginación
- Anuncios similares

### 4. **Admin Django con Jazzmin**
- Configurar menús anidados
- Reportes y estadísticas
- Gestión avanzada de roles




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

### ⏳ EN PROGRESO
- Mensajes → Interfaz híbrida lista (notificaciones + contactos con email/WhatsApp), falta backend para chat interno completo

### 📋 PENDIENTES
- GuideView → destacar anuncios recomendados/destacados según plan
- JobDetailView → sincronización DB + endpoints, mejor UI, guardar/compartir anuncios, mostrar similares
- Admin Django con Jazzmin → menús anidados, reportes, roles, perfiles, CRUD categorías/subcategorías
- CRUD dinámico de categorías y subcategorías (no hardcodeadas)
- Cambios similares en app Plans
- Sistema de aplicaciones desde JobDetailView