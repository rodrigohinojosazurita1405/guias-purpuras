# 🛣️ ROADMAP - Guías Púrpuras V1.0

## 📊 Estado General del Proyecto
**Última Actualización:** 2025-11-21
**Rama:** main
**Versión:** 1.0 (En Desarrollo)
**Sesión Actual:** Sesión 2 (Completada - Mejoras UI/UX + Navbar)
**Progreso General:** ~40% (Frontend básico completo, Backend parcial)

---

## ✅ COMPLETADO EN ESTA SESIÓN

### 1. **Funcionalidad CRUD de Foto de Perfil** ✓
- [x] Endpoint Django para upload de foto (`POST /api/profiles/user/{user_id}/photo/`)
- [x] Endpoint Django para delete de foto (`DELETE /api/profiles/user/{user_id}/photo/delete`)
- [x] Componente Vue AvatarUpload con preview
- [x] Botón visible para eliminar foto de perfil
- [x] Política de 1 sola foto por perfil (auto-delete de foto anterior)
- [x] Corrección JWT: Token rotation deshabilitada en settings.py
- [x] Absolutización de URLs de media para funcionar cross-origin (puerto 5173 ↔ 8000)

### 2. **Unificación de Colores Dashboard** ✓
- [x] Gradient púrpura estándar: `linear-gradient(135deg, #7c3aed, #6d28d9)`
- [x] Actualización MisOrdenes.vue:
  - Botones "Ver Trabajo" y "Ver Aplicación" con gradient
  - Botón "Explorar Trabajos" (empty state) con gradient
- [x] Actualización CompanyProfileEdit.vue:
  - Botón "Crear Perfil De Empresa" con gradient
  - Botón "Guardar Cambios" con gradient
- [x] Actualización UserProfileEdit.vue:
  - Botón "Actualizar Perfil" con gradient
- [x] Actualización DashboardHome.vue:
  - 4 botones de acciones rápidas con gradient
  - Iconos en blanco
  - Efectos hover mejorados
- [x] Actualización JobsManager.vue (ya estaba correcto):
  - Botones "Publicar Nuevo" y "Publicar Trabajo" con gradient
- [x] Actualización BranchManager.vue (ya estaba correcto):
  - Botón "Actualizar" con gradient

### 3. **Reemplazo de va-button por HTML buttons** ✓
- [x] MisOrdenes: Botones de acciones reemplazados por `<button>` con clases `.action-btn-gradient` y `.explore-btn`
- [x] CompanyProfileEdit: Botones reemplazados por `<button>` con clase `.purple-btn-gradient`
- [x] UserProfileEdit: Botón reemplazado por `<button>` con clase `.purple-btn-gradient`
- [x] Todos con efectos hover: gradient más oscuro + sombra + elevación (translateY -2px)

### 4. **Corrección del Error 404 en Sidebar** ✓
- [x] Identificado: Botón "Publicar Un Nuevo Trabajo" apuntaba a `/dashboard/publish` (no existe)
- [x] Solucionado: Cambio de ruta a `/publicar` (ruta correcta en router)
- [x] Mejorado: Styling del botón highlight con gradient y hover effects

### 5. **Sincronización de Nombre de Perfil en Dashboard** ✓
- [x] Implementado watch reactivo en DashboardHome.vue para observar cambios en authStore.user.name
- [x] Actualizado handleProfileUpdated en DashboardView.vue para sincronizar estado
- [x] Persistencia en localStorage de cambios de perfil

### 6. **Mejora del Navbar - Propuesta A Implementada** ✓
- [x] Agregado VaDropdown para categoría "Guías" (Desktop)
- [x] Categoría Empleos (activa)
- [x] Categorías futuras: Profesionales, Negocios, Restaurantes (deshabilitadas + label "Próximamente")
- [x] Agregado link "Sobre Nosotros" en navegación desktop
- [x] Implementado submenu expandible para Guías en mobile
- [x] Estilos profesionales para dropdown con hover effects
- [x] Transiciones suaves (.expand-enter/leave)
- [x] Responsivo en desktop y mobile

---

## 🚀 POR HACER - PRÓXIMAS SESIONES

### **🔴 FASE 2: Página de Publicación de Trabajos (CRITICAL PRIORITY - SESIÓN 3)**
**Estado Actual:** Frontend 100% (wizard visual completo), Backend 0% (pendiente endpoints)

#### Frontend (Ya Implementado):
- [x] PublishView.vue con estructura completa
- [x] CategoryStep (seleccionar categoría)
- [x] JobPublishStart (información básica del trabajo)
- [x] ApplicationConfigStep (configuración de cómo aceptar candidatos)
- [x] PublishStepsIndicator (indicador de progreso visual)
- [x] Validación de formularios frontend
- [x] Preview visual del anuncio

#### Backend (POR HACER - SESIÓN 3):
- [ ] Crear/verificar modelo Job en Django (con todos los campos)
- [ ] Endpoint POST `/api/jobs/publish/` para crear nuevo trabajo
- [ ] Endpoint PATCH `/api/jobs/{job_id}/` para actualizar trabajo
- [ ] Endpoint GET `/api/jobs/user/` para listado de trabajos del usuario
- [ ] Validación en backend (campos requeridos, limites, etc.)
- [ ] Asociar trabajos con usuario autenticado
- [ ] Subida de imágenes para el anuncio (si aplica)

### **FASE 3: Gestión de Candidatos**
- [ ] Componente CandidateManager (actualmente placeholder)
- [ ] Listado de candidatos por trabajo
- [ ] Sistema de filtrado de candidatos
- [ ] Estados de aplicación (received, reviewing, shortlisted, accepted, rejected)
- [ ] Notas del reclutador

### **FASE 4: Funcionalidades Adicionales del Dashboard**
- [ ] Usuarios Bloqueados (/dashboard/blocked)
- [ ] Favoritos/Shortlisted (/dashboard/shortlisted)
- [ ] Comunicaciones/Mensajes (/dashboard/messages)
- [ ] Gestionar Usuarios (/dashboard/users) - admin only
- [ ] Registro De Actividad (/dashboard/history)
- [ ] Alertas/Notificaciones (/dashboard/notifications)
- [ ] Cambiar Contraseña (/dashboard/password)

### **FASE 5: Publicación de Otros Tipos (Deshabilitados)**
- [ ] Perfil Profesional
- [ ] Restaurantes/Gastronomía
- [ ] Negocios
- *Nota: Actualmente los componentes están deshabilitados/commented out*

### **FASE 6: Mejoras de UX/UI**
- [ ] Validaciones más robustas en formularios
- [ ] Mensajes de error/éxito más detallados
- [ ] Loading states mejorados
- [ ] Animaciones de transición entre páginas
- [ ] Optimización de imágenes
- [ ] Progressive Web App (PWA) features

### **FASE 7: Autenticación y Seguridad**
- [ ] Recuperación de contraseña (actualmente solo UI)
- [ ] Verificación de email
- [ ] Two-factor authentication (opcional)
- [ ] Refresh token automático mejorado

### **FASE 8: Backend API**
- [ ] Crear endpoints para gestión de trabajos completa
- [ ] Crear endpoints para candidatos
- [ ] Crear endpoints para mensajes
- [ ] Crear endpoints para notificaciones
- [ ] Implementar paginación en listados
- [ ] Filtros avanzados

### **FASE 9: Testing**
- [ ] Unit tests para componentes Vue
- [ ] Integration tests para API endpoints
- [ ] E2E tests para flujos principales

### **FASE 10: Deployment**
- [ ] Setup CI/CD pipeline
- [ ] Configuración de producción
- [ ] Optimización de performance
- [ ] Security audit

---

## 🔧 PROBLEMAS CONOCIDOS Y SOLUCIONES

### ✓ SOLUCIONADOS
1. **JWT Token Blacklist** → Deshabilitado ROTATE_REFRESH_TOKENS y BLACKLIST_AFTER_ROTATION
2. **Foto no visible en dashboard** → Creada función get_absolute_media_url() para URLs absolutas
3. **va-button con color="purple" no mostraba gradient** → Reemplazados por HTML buttons con clases CSS
4. **Error 404 en "Publicar Nuevo Trabajo"** → Ruta corregida de /dashboard/publish a /publicar

### ⚠️ POR REVISAR
- [ ] Validaciones más robustas en backend
- [ ] Limite de tamaño de archivo para fotos
- [ ] Compresión automática de imágenes

---

## 📁 ARCHIVOS CLAVE MODIFICADOS

### Backend
- `core/settings.py` - JWT configuration
- `profiles/views.py` - Photo upload/delete endpoints
- `profiles/urls.py` - Routes para foto

### Frontend
- `src/components/Dashboard/MisOrdenes.vue` - Botones con gradient
- `src/components/Dashboard/DashboardHome.vue` - Action buttons mejorados
- `src/components/Dashboard/JobsManager.vue` - Botones de publicación
- `src/components/Profile/CompanyProfileEdit.vue` - Botón crear empresa
- `src/components/Profile/UserProfileEdit.vue` - Botón actualizar perfil
- `src/components/Profile/Dashboard.vue` - Sidebar + ruta /publicar fix
- `src/components/Profile/AvatarUpload.vue` - Upload y delete foto
- `src/stores/useProfileStore.js` - Store para foto
- `src/router/index.js` - Rutas

---

## 💜 ESTILO Y BRANDING

### Color Scheme Unificado
- **Gradient Primario:** `linear-gradient(135deg, #7c3aed, #6d28d9)`
- **Gradient Hover:** `linear-gradient(135deg, #6d28d9, #5b21b6)` (más oscuro)
- **Color Variable:** `var(--color-purple)` = `#5C0099`
- **Texto Botones:** Blanco (#ffffff)
- **Sombra Hover:** `0 4px 12px rgba(124, 58, 237, 0.3)`
- **Transición:** `all 0.2s` a `all 0.3s ease`

---

## 📝 NOTAS PARA LA PRÓXIMA SESIÓN

1. **Continuar con PublishView:** El componente existe pero necesita implementación completa del wizard
2. **Revisar Backend API:** Asegurar que todos los endpoints estén funcionando correctamente
3. **Testing:** Hacer pruebas exhaustivas de flujos de usuario antes de avanzar
4. **Performance:** Monitorear bundle size y performance de carga

---

## 🎯 OBJETIVO FINAL
Plataforma completa de publicación y gestión de empleos/servicios en Bolivia con interfaz moderna, intuitiva y responsiva.

