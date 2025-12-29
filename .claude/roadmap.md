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
FASE 7.7: Notificaciones de Estado         ✅ 100% COMPLETADA
FASE 7.9: Sistema de Notificaciones        ✅ 100% COMPLETADA

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

### ✅ FASE 9: Sistema Completo de Reportes (100% COMPLETADA) - Diciembre 2024
**App:** `reports`
**Modelos:** `DailyReport`, `Report`
**Archivos:** `reports/models.py`, `reports/admin.py`, `reports/views.py`, `reports/services/metrics.py`, `reports/services/pdf_generator.py`
**Commits:** Múltiples commits de mejora (ver detalle abajo)

#### **Modelos Implementados:**
- ✅ **DailyReport** - Reportes diarios automáticos con snapshots
  - Usuarios: nuevos usuarios, empresas, postulantes, activos totales
  - Trabajos: nuevos, activos, cerrados, vistas totales
  - Planes: vendidos por tipo (estándar, púrpura, impulso)
  - Ingresos: total y desglosado por plan

- ✅ **Report** - Sistema de reportes dinámicos (HTML moderno)
  - Tipos: `daily`, `weekly`, `last_7_days`, `monthly`
  - Estados: `pending`, `generating`, `completed`, `failed`
  - Métricas JSON almacenadas en BD (no PDFs físicos)
  - Campo `period_label` con formato legible

#### **Servicio de Métricas Completo (`services/metrics.py`):**
- ✅ **calculate_period_metrics()** - Cálculo completo de métricas para cualquier período
  - Métricas de usuarios (nuevos, totales, por rol)
  - Métricas de trabajos (nuevos, activos, cerrados, vistas)
  - Métricas de planes vendidos (por tipo, distribución %)
  - Métricas de ingresos (total, por plan, ticket promedio)
  - Métricas de aplicaciones (total, promedio por trabajo)
  - Top empresas por compras y gastos
  - Top trabajos por aplicaciones y vistas

- ✅ **Comparaciones con Período Anterior**
  - Cálculo automático de período anterior equivalente
  - Cambio porcentual (%, dirección: up/down/neutral)
  - Comparación de ingresos, planes, usuarios, trabajos

- ✅ **Insights Automáticos**
  - Análisis inteligente de tendencias
  - Alertas de ingresos bajos o cero
  - Plan más vendido del período
  - Crecimiento de usuarios
  - Promedio de aplicaciones por trabajo

#### **Generador de Reportes (`services/pdf_generator.py`):**
- ✅ `generate_daily_report()` - Reporte de HOY
- ✅ `generate_weekly_report()` - **Semana PASADA completa** (Lun-Dom)
- ✅ `generate_last_7_days_report()` - **Últimos 7 días** (hoy - 6 días)
- ✅ `generate_monthly_report()` - Mes actual o especificado
- ✅ `regenerate_report()` - Re-generar métricas de reporte existente

**Nota importante:** PDFs eliminados, ahora se usan **reportes HTML modernos**

#### **Templates HTML Profesionales:**
- ✅ **report_view.html** - Vista web con toolbar sticky
  - Botones: "Imprimir / Guardar PDF" (window.print())
  - Botón: "Descargar HTML"
  - Diseño moderno con gradientes, cards, tablas responsive
  - Sección "Resumen Ejecutivo" con métricas clave
  - **Sección "Insights Clave"** con gradiente púrpura y cards
  - Comparaciones con período anterior (flechas ↑↓→)
  - Print-ready con `@media print`

- ✅ **report_download.html** - HTML standalone para descarga
  - Sin toolbar (auto-contenido)
  - CSS inline completo
  - Mismo diseño que report_view

- ✅ **report_content.html** - Template reutilizable
  - Incluido por ambos templates anteriores
  - Resumen ejecutivo con 4 métricas principales
  - Insights con alertas visuales
  - Ingresos detallados por plan
  - Usuarios y empresas
  - Ofertas de trabajo
  - Comparación con período anterior

#### **Admin Django Mejorado:**
- ✅ **Botones de Generación Manual** (change_list.html personalizado)
  - Botón azul: "Reporte Diario"
  - Botón verde: "Semanal (Lun-Dom)"
  - Botón naranja: "Últimos 7 Días" **[NUEVO]**
  - Botón púrpura: "Reporte Mensual"
  - Botón rojo: "Limpiar Antiguos" (elimina reportes 30+ días)

- ✅ **Vista de Lista Mejorada**
  - Badges coloridos por tipo de reporte
  - Badge de estado (completado/generando/fallido)
  - Resumen de métricas inline
  - Botones "Ver Reporte" y "Descargar HTML"
  - Filtros por tipo, estado y fecha

- ✅ **Vistas Personalizadas**
  - `view_report(report_id)` - Ver HTML en navegador
  - `download_report_html(report_id)` - Descargar archivo .html
  - `cleanup_old_reports_view()` - Limpiar desde admin

#### **Comando de Limpieza (`cleanup_old_reports.py`):**
- ✅ **Management Command** para mantenimiento
  - `python manage.py cleanup_old_reports [--days=30] [--dry-run]`
  - Elimina reportes antiguos de la BD
  - Elimina carpeta `media/reports/` (PDFs obsoletos)
  - Modo simulación con `--dry-run`
  - Estadísticas detalladas de eliminación

#### **URLs y Navegación:**
- ✅ `/reports/<id>/view/` - Ver reporte HTML
- ✅ `/reports/<id>/download/` - Descargar HTML
- ✅ `/admin/reports/report/generate/daily/` - Generar diario
- ✅ `/admin/reports/report/generate/weekly/` - Generar semanal
- ✅ `/admin/reports/report/generate/last7days/` - Generar últimos 7 días
- ✅ `/admin/reports/report/generate/monthly/` - Generar mensual
- ✅ `/admin/reports/report/cleanup/` - Limpiar antiguos

#### **Mejoras de UX/UI:**
- ✅ **Sección Insights rediseñada**
  - Fondo con gradiente púrpura suave (#f3e8ff → #e9d5ff)
  - Items en cards blancas con sombra
  - Iconos ✓ para insights positivos
  - Iconos ⚠ para alertas (fondo rojo suave)
  - Sin márgenes innecesarios (diseño limpio)

- ✅ **Responsive Design Completo**
  - Mobile-first approach
  - Grid responsive para métricas
  - Tablas con scroll horizontal en móvil
  - Botones apilados en pantallas pequeñas

#### **Scripts de Prueba:**
- ✅ `test_new_reports.py` - Prueba de generación de reportes
- ✅ `check_weekly_jobs.py` - Verificación de trabajos semanales
- ✅ `test_cleanup_command.py` - Estado de reportes y uso del comando

#### **Decisiones Técnicas Importantes:**
1. ✅ **Eliminado WeasyPrint/xhtml2pdf** - Mala calidad de PDFs
2. ✅ **HTML + window.print()** - Mejor calidad, más rápido
3. ✅ **Métricas en JSON** - No ocupan espacio en disco
4. ✅ **Semana pasada vs actual** - Reportes más útiles
5. ✅ **Nuevo tipo "Últimos 7 días"** - Flexibilidad adicional

#### **Funcionalidades NO Implementadas (fuera de MVP):**
- ❌ Celery + Beat para generación automática (Fase 6)
- ❌ Envío automático por email
- ❌ Gráficas interactivas (Chart.js/ApexCharts)
- ❌ Exportación a Excel/CSV
- ❌ Reportes personalizados por rango de fechas
- ❌ Dashboard en tiempo real

**Nota:** El sistema está 100% funcional para generación manual. La automatización (Fase 6) se pospone intencionalmente.

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

### ✅ FASE 7.7 y 7.9: Sistema Completo de Notificaciones (100% COMPLETADA) - Diciembre 2024
**App:** `G_Jobs.notifications`
**Modelos:** `Notification`
**Archivos:** `notifications/models.py`, `notifications/signals.py`, `notifications/views.py`, `notifications/apps.py`
**Commits:** `7e12599`, `45e5929`, `cfa043b`

#### Backend Completado:
- ✅ **Modelo `Notification` en Django**
  - ✅ Campos: user, notification_type, title, message, metadata (JSON), link, is_read, created_at
  - ✅ Tipos definidos: application_sent, new_application, payment_verified, payment_rejected, job_expiring_soon, saved_job_closed, password_changed
  - ✅ Método estático `create_notification()` para creación estandarizada
  - ✅ Ordenamiento por fecha descendente (más recientes primero)

- ✅ **Signals Automáticos Implementados**
  - ✅ `notify_new_application`: Empresa recibe notificación cuando llega nueva postulación
  - ✅ `notify_application_sent`: Postulante confirmación de postulación enviada
  - ✅ `notify_payment_status`: Empresa cuando pago es verificado/rechazado por admin
  - ✅ `notify_saved_job_closed`: Postulantes cuando trabajo guardado es cerrado
  - ✅ `notify_password_changed`: Usuario cuando contraseña es cambiada (seguridad)
  - ✅ Signal `pre_save` en CustomUser y Job para capturar estado anterior

- ✅ **Management Command para Cron**
  - ✅ `notify_expiring_jobs.py`: Notifica a empresas 3 días antes de vencimiento
  - ✅ Valida trabajos activos con pago verificado
  - ✅ Evita notificaciones duplicadas (verifica si ya existe)
  - ✅ Debe ejecutarse diariamente: `0 9 * * * python manage.py notify_expiring_jobs`

- ✅ **API Endpoints**
  - ✅ `GET /api/notifications/` - Listar notificaciones del usuario autenticado
  - ✅ `PATCH /api/notifications/{id}/mark-read/` - Marcar como leída
  - ✅ `POST /api/notifications/mark-all-read/` - Marcar todas como leídas
  - ✅ `DELETE /api/notifications/{id}/` - Eliminar notificación
  - ✅ Filtrado automático por usuario autenticado
  - ✅ Paginación y ordenamiento

#### Frontend Completado:
- ✅ **Componente `NotificationsView.vue`**
  - ✅ Vista integrada en dashboard (ruta `/dashboard/notifications`)
  - ✅ Contador de notificaciones no leídas en navbar
  - ✅ Badge numérico en ícono de campana
  - ✅ Listado con scroll infinito
  - ✅ Marcar individual como leída
  - ✅ Botón "Marcar todas como leídas"
  - ✅ Eliminar notificación individual
  - ✅ Timestamps relativos (hace 5 minutos, hace 2 horas, etc.)
  - ✅ Íconos personalizados por tipo de notificación
  - ✅ Colores diferenciados por tipo
  - ✅ Empty state cuando no hay notificaciones
  - ✅ Animaciones suaves de entrada/salida

- ✅ **Integración con Dashboard**
  - ✅ Link en navbar (campana con badge)
  - ✅ Tab dedicado "Notificaciones" en MessagesView
  - ✅ Actualización en tiempo real mediante polling (cada 30 segundos)
  - ✅ Notificaciones se cargan automáticamente al montar componente

#### Tipos de Notificaciones Implementados:

**Para Empresas (4/4):**
1. ✅ `new_application` - Nueva postulación recibida
2. ✅ `payment_verified` - Pago verificado exitosamente
3. ✅ `payment_rejected` - Pago rechazado por administrador
4. ✅ `job_expiring_soon` - Anuncio próximo a vencer (3 días)

**Para Postulantes (3/3):**
5. ✅ `application_sent` - Postulación enviada exitosamente
6. ✅ `saved_job_closed` - Trabajo guardado fue cerrado
7. ✅ `password_changed` - Contraseña cambiada (seguridad)

#### Testing y Diagnóstico:
- ✅ Script `test_notifications.py` - Crear notificaciones de prueba manualmente
- ✅ Script `check_notifications.py` - Verificar estado del sistema de notificaciones
- ✅ Logs de consola con prefijo `[NOTIFICATION]` para debug

#### Correcciones Aplicadas:
- ✅ Fix en `jobs/admin.py`: Acción "Rechazar pagos" ahora también cambia estado a 'pending'
- ✅ Apps config con método `ready()` para cargar signals automáticamente

#### Pendientes (Mejoras Futuras):
- ⏳ **Mejorar apariencia de notificaciones** (UX/UI más atractivo)
  - ⏳ Diseño más moderno y visual
  - ⏳ Animaciones más fluidas
  - ⏳ Agrupación de notificaciones por fecha
  - ⏳ Vista previa expandible de notificaciones largas
  - ⏳ Acciones rápidas (eliminar múltiples, filtrar por tipo)
- ⏳ WebSockets para notificaciones en tiempo real (reemplazar polling)
- ⏳ Sonido/vibración al recibir notificación
- ⏳ Push notifications para móvil (PWA)
- ⏳ Preferencias de notificaciones por usuario

### ⏳ FASE 7.5: Sistema de Mensajes (60% COMPLETADA) - ❌ NO INCLUIDO EN MVP
**Componente:** `MessagesView.vue`
**Estado:** Interfaz frontend completa, backend NO se hará para MVP
**Decisión:** Sistema de chat interno se pospone para después del MVP

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

**Backend de mensajería NO se implementará en MVP:**
- ❌ Sistema de chat interno completo (inbox) - POST-MVP
- ❌ WebSockets o polling para tiempo real - POST-MVP
- ❌ Modelo `Conversation` y `Message` - POST-MVP

---

## 🎯 PRÓXIMAS PRIORIDADES PARA MVP

### 1. **Mejorar Apariencia de Notificaciones** (ALTA PRIORIDAD)
**Descripción:** Rediseño visual del componente NotificationsView.vue para mejor UX/UI

**Mejoras a implementar:**
- ⏳ Diseño más moderno y visual (gradientes, sombras, espaciado)
- ⏳ Agrupación de notificaciones por fecha (Hoy, Ayer, Esta semana, Anterior)
- ⏳ Animaciones más fluidas (transiciones de entrada/salida)
- ⏳ Acciones rápidas (eliminar múltiples notificaciones)
- ⏳ Filtrar por tipo de notificación (dropdown con opciones)
- ⏳ Iconos más grandes y destacados
- ⏳ Mejor jerarquía visual (títulos, mensajes, timestamps)

**Archivos a modificar:**
- `frontend/src/components/Dashboard/NotificationsView.vue`

---

### 2. **✅ FASE 7.9: Mejoras Dashboard Reclutador - CandidatesView** (COMPLETADA)
**Descripción:** Funcionalidades críticas para gestión eficiente de candidatos con alto volumen de solicitudes

**Contexto:**
- Con 50+ candidatos por trabajo, se vuelve imposible gestionar sin herramientas avanzadas
- Basado en análisis de plataformas profesionales (LinkedIn Recruiter, Greenhouse, Lever)

**Tareas Completadas:**

#### **✅ FASE 1 - LO MÁS CRÍTICO**
1. ✅ **Puntuación/Rating de Candidatos** ⭐
   - ✅ Sistema de estrellas 1-5 para calificar candidatos
   - ✅ Ordenar por mejor puntuación (rating-desc, rating-asc)
   - ✅ Campo `rating` en modelo `JobApplication`
   - ✅ Componente StarRating.vue reutilizable
   - ✅ Componente de estrellas clickeable en cada tarjeta
   - ✅ Filtro adicional "Ordenar por: Rating"
   - ✅ Rating incluido en exportaciones CSV

#### **✅ FASE 2 - MUY ÚTIL**
2. ✅ **Acciones en Lote** ⚡
   - ✅ Checkbox para seleccionar múltiples candidatos
   - ✅ Toolbar flotante con contador de seleccionados
   - ✅ Botón "Cambiar estado de seleccionados" (5 opciones)
   - ✅ Modal de confirmación personalizado (Vuestic UI)
   - ✅ Confirmar antes de acción masiva
   - ✅ Contador de éxitos/errores en operaciones
   - ✅ Animaciones suaves de entrada/salida

3. ✅ **Exportación a Excel/CSV** 📊
   - ✅ Dropdown con 3 modos de exportación:
     - ✅ Exportar Todo (filtrados en un archivo)
     - ✅ Seleccionar Anuncios (múltiples trabajos por separado)
     - ✅ Exportar Todos por Separado (cada trabajo en archivo CSV)
   - ✅ Incluir: Nombre, Email, Teléfono, WhatsApp, Estado, Rating, Fecha
   - ✅ Formato profesional con UTF-8 BOM para Excel
   - ✅ Notificaciones de progreso para descargas múltiples
   - ✅ Delay entre descargas para evitar bloqueo

#### **⏳ FASE 3 - PENDIENTE (POST-MVP)**
4. ⏳ **Filtros Avanzados** 🔍 - POST-MVP
   - ⏳ Filtrar por fecha de aplicación (última semana, último mes, etc.)
   - ⏳ Filtrar por años de experiencia (si se captura en CV)
   - ⏳ Filtrar por ubicación/ciudad
   - ⏳ Filtro combinado (múltiples criterios simultáneos)

5. ⏳ **Comunicación Directa con Templates** 💬 - POST-MVP
   - ⏳ Botón "Enviar Email" en cada candidato
   - ⏳ Modal con editor de email
   - ⏳ Templates predefinidos (gracias, rechazo, invitación, info)
   - ⏳ Variables dinámicas: {nombre}, {puesto}, {empresa}
   - ⏳ Registro de emails enviados en notas

**Estado:** 3 de 5 funcionalidades completadas (las más críticas) 🎉
**Nota:** FASE 3 se pospone para después del MVP

---

### 3. **FASE 7.8: Gestión de CVs en Dashboard Postulante** (🔴 CRÍTICO - EN PROGRESO 85%)
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