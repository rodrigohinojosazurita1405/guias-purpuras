# Guías Púrpuras - ROADMAP Completo MVP

## 📊 ESTADO ACTUAL - PROGRESO GENERAL

```
FASE 1: Wizard de Publicación         ✅ 100% COMPLETADA
FASE 2: Flujo de Publicación Completo ⏳ 10% (EN PROGRESS - Backend pendiente)
FASE 3: Búsqueda y Filtrado          ⏳ 0% (PENDIENTE)
FASE 3.6: Autenticación Real         ✅ 100% COMPLETADA
FASE 4: Perfiles de Usuario          ✅ 100% COMPLETADA + FOTO CRUD ✅
FASE 5: Perfiles de Empresa          ✅ 50% COMPLETADA (modelo + componentes)
FASE 6: Sistema de Aplicaciones      ⏳ 0% (PENDIENTE)
FASE 7: Subida de Comprobante        ⏳ 0% (PENDIENTE)
FASE 8: Dashboard Admin              ⏳ 0% (PENDIENTE)

MEJORAS RECIENTES:
- ✅ Dashboard visual unified (todos botones con mismo gradient)
- ✅ Error 404 en sidebar solucionado
- ✅ Sincronización de nombre de usuario en DashboardHome
```

---

## ✅ COMPLETADO EN ESTA SESIÓN (Sesión 2)

### CRUD Foto de Perfil + Dashboard Styling + Profile Name Sync
**Descripción**: Funcionalidad CRUD completa para fotos de perfil, unificación visual del dashboard y sincronización de nombre de usuario

#### ✅ CRUD Foto de Perfil
- ✅ Backend: Endpoints CREATE (POST) y DELETE para fotos
  - POST `/api/profiles/user/{user_id}/photo/` - Subir foto (reemplaza anterior automáticamente)
  - DELETE `/api/profiles/user/{user_id}/photo/delete` - Eliminar foto
- ✅ Política 1 foto por usuario: Auto-delete de foto anterior
- ✅ Frontend: Componente AvatarUpload.vue con upload, display y delete
  - Preview en tiempo real
  - Botón delete visible cuando existe foto
- ✅ Corrección JWT: Token rotation deshabilitada
- ✅ URLs absolutas para cross-origin (puerto 5173 ↔ 8000)

#### ✅ Unificación de Colores Dashboard
- ✅ Gradient púrpura estándar aplicado a TODOS los botones: `linear-gradient(135deg, #7c3aed, #6d28d9)`
- ✅ Reemplazo de va-button por HTML buttons con clases CSS personalizadas
- ✅ Componentes actualizados:
  - MisOrdenes.vue: "Ver Trabajo", "Ver Aplicación", "Explorar Trabajos"
  - CompanyProfileEdit.vue: "Crear Perfil De Empresa", "Guardar Cambios"
  - UserProfileEdit.vue: "Actualizar Perfil"
  - DashboardHome.vue: 4 botones de acciones rápidas
  - Dashboard.vue: Botón sidebar "Publicar Un Nuevo Trabajo" (ahora funcional, error 404 fix)
- ✅ Efectos hover mejorados: gradient más oscuro + sombra + elevación (translateY -2px)
- ✅ Estados disabled soportados en botones de formulario

#### ✅ Fix: Error 404 en Sidebar "Publicar Un Nuevo Trabajo"
- ✅ Ruta incorrecta: `/dashboard/publish` → Ruta correcta: `/publicar`
- ✅ Botón highlight con gradient mejorado

#### ✅ Sincronización de Nombre en DashboardHome
- ✅ Frontend: watch reactivo en DashboardHome.vue
  - Observa cambios en `authStore.user.name`
  - Actualiza el saludo "Bienvenido, [nombre]" automáticamente
- ✅ Backend: Mejorado handleProfileUpdated en DashboardView.vue
  - Actualiza authStore cuando se guarda el perfil
  - Persiste cambios en localStorage
  - Redirige al home automáticamente

**Status**: 🎉 COMPLETADA Y FUNCIONANDO

---

### FASE 4: Perfiles de Usuario (COMPLETADA) ⭐ REFERENCIA
**Descripción**: Sistema completo de perfiles de usuario con modelos, API y componentes Vue

- ✅ **Backend Django**
  - Modelo UserProfile con campos: fullName, email, phone, location, bio, profilePhoto, timestamps
  - Modelo CompanyProfile con relación a UserProfile (OneToMany)
  - 6 endpoints: create_user_profile, get_user_profile, get_user_profile_by_email, update_user_profile
  - 5 endpoints empresa: create_company_profile, get_company_profile, update_company_profile, list_user_companies
  - Migrations ya aplicadas
  - Validación completa de datos

- ✅ **Pinia Store (useProfileStore)**
  - Estado: userProfile, isLoading, error, successMessage
  - Computed: isProfileComplete, profileProgress (0-100%)
  - Métodos: createProfile, getProfileById, getProfileByEmail, updateProfile
  - Gestión de errores y mensajes
  - Persistencia de datos

- ✅ **Componentes Vue3**
  - ProfileForm.vue: Formulario editable con validaciones en tiempo real
  - AvatarUpload.vue: Carga de foto de perfil con preview y validación de tamaño (5MB max)
  - ProfileCard.vue: Vista de perfil en formato tarjeta con información visual
  - UserProfileEdit.vue: Actualizado para usar useProfileStore (integración existente)

- ✅ **Features**
  - Indicador de progreso de perfil (0-100%)
  - Validación de campos en tiempo real
  - Mensajes de éxito y error animados
  - Carga de archivos con preview
  - Integración con dashboard
  - API endpoints completamente funcionales

- ✅ **Testing**
  - Todos los endpoints de API probados y funcionales
  - POST /api/profiles/user/create ✅
  - GET /api/profiles/user/{id}/ ✅
  - GET /api/profiles/user/email/{email}/ ✅
  - PATCH /api/profiles/user/{id}/edit ✅
  - POST /api/profiles/company/create ✅
  - GET /api/profiles/company/{id}/ ✅
  - GET /api/profiles/user/{id}/companies ✅

**Status**: 🎉 COMPLETADA Y FUNCIONANDO

---

### FASE 3.6: Autenticación Real (COMPLETADA)
**Descripción**: Sistema de autenticación JWT con login, registro y recuperación de contraseña

- ✅ **Backend JWT**
  - 5 endpoints: register, login, logout, refresh_token, verify_token
  - Token blacklisting en logout
  - Validación de credenciales
  - Endpoint forgot-password

- ✅ **Frontend Components**
  - LoginForm.vue con validación en tiempo real
  - RegisterForm.vue con indicador de fortaleza
  - ForgotPasswordForm.vue
  - Todas con animaciones y diseño moderno

- ✅ **State Management**
  - AuthStore (Pinia) con gestión de tokens
  - Persistencia en localStorage
  - Auto-refresh de tokens
  - Logout con blacklist

- ✅ **Router & Guards**
  - Rutas protegidas (/dashboard, /publicar, etc.)
  - Redireccionamiento automático a login
  - Guards para rutas autenticadas

- ✅ **Navbar Integration**
  - Botón "Ingresar" navegando a /login
  - Menú dropdown con usuario autenticado
  - Opción de logout

**Endpoint de Producción**: Falta integración de email real para forgot-password

---

## 🚀 PRÓXIMAS FASES (RECOMENDADO ORDER)

---

## 🏢 FASE 5: PERFILES DE EMPRESA (⭐ SIGUIENTE)
**Descripción**: Perfiles empresariales vinculados a usuarios

### 5.1 Modelo Backend
- [ ] Modelo CompanyProfile con:
  - Nombre empresa
  - Logo
  - Descripción
  - Sector/industria
  - Ubicación
  - Sitio web
  - Contacto
  - Número de empleados
- [ ] Relación con User

### 5.2 API REST
- [ ] CRUD completo para company profiles
- [ ] GET companies - Listar todas
- [ ] Búsqueda por nombre/sector

### 5.3 Frontend
- [ ] CompanyForm.vue
- [ ] CompanyCard.vue
- [ ] Integración en dashboard

---

## 💼 FASE 2: FLUJO DE PUBLICACIÓN COMPLETO
**Descripción**: Completar el wizard y enviar datos al backend

### 2.1 Revisión de componentes existentes
- [ ] ApplicationConfigStep - Verificar y completar
- [ ] SummaryCard - Mostrar resumen y permitir edición

### 2.2 Backend Integration
- [ ] POST /api/jobs/publish - Crear trabajo
  - Validar datos
  - Asociar con usuario autenticado
  - Guardar en BD
  - Retornar ID
- [ ] Manejo de errores

### 2.3 Frontend Integration
- [ ] Integrar endpoint en PublishView
- [ ] Loading states
- [ ] Error handling
- [ ] Confirmación de éxito
- [ ] Redireccionar a detalle

### 2.4 Mejoras
- [ ] Auto-save de borradores
- [ ] Validación completa antes de submit
- [ ] Toast notifications
- [ ] Confirmación antes de publicar

---

## 🔍 FASE 3: BÚSQUEDA Y FILTRADO
**Descripción**: Sistema de búsqueda y filtrado avanzado

### 3.1 Backend
- [ ] GET /api/jobs - Con parámetros de filtro
- [ ] Filtros: categoría, ubicación, salario, tipo contrato
- [ ] Búsqueda por texto
- [ ] Paginación

### 3.2 Frontend
- [ ] SearchBar en header
- [ ] FilterPanel con opciones
- [ ] ResultsGrid responsive
- [ ] Pagination
- [ ] No results message

### 3.3 Features
- [ ] Guardado de filtros favoritos
- [ ] Búsqueda por ubicación
- [ ] Filtro de salario con rango

---

## 📋 FASE 6: SISTEMA DE APLICACIONES
**Descripción**: Usuarios pueden aplicar a trabajos, empresas ven candidatos

### 6.1 Modelo Backend
- [ ] Modelo Application con:
  - Job (FK)
  - Applicant (FK)
  - Respuestas a preguntas
  - Estado (pendiente, revisada, etc.)
  - Timestamps

### 6.2 API REST
- [ ] POST /api/applications - Crear aplicación
- [ ] GET /api/jobs/{id}/applications - Ver candidatos
- [ ] PUT /api/applications/{id}/status - Cambiar estado
- [ ] GET /api/me/applications - Mis aplicaciones

### 6.3 Frontend
- [ ] ApplicationForm.vue
- [ ] CandidatesList.vue
- [ ] ApplicationDetail.vue
- [ ] Integración en dashboard

### 6.4 Features
- [ ] Preguntas de screening dinámicas
- [ ] Estados de aplicación (pendiente/revisada/aceptada/rechazada)
- [ ] Contacto con candidato
- [ ] Historial de aplicaciones

---

## 💳 FASE 7: PLANES DE PAGO Y COMPROBANTE
**Descripción**: Sistema de planes y subida de comprobante de pago

### 7.1 Modelos Backend
- [ ] Modelo Payment con:
  - Plan (Estándar/Top/Destacado)
  - Comprobante (URL)
  - Estado (pendiente/aprobado/rechazado)
  - Monto

### 7.2 API REST
- [ ] POST /api/payments - Crear pago
- [ ] POST /api/payments/{id}/upload - Subir comprobante
- [ ] GET /api/payments - Ver mis pagos

### 7.3 Frontend
- [ ] PaymentModal.vue
- [ ] PlanSelector.vue
- [ ] ProofUpload.vue
- [ ] PaymentStatus.vue

### 7.4 QR Predefinidos
- [ ] Generar QR para cada plan
- [ ] Mostrar en modal de pago
- [ ] Instrucciones de pago

### 7.5 Features
- [ ] Validación de comprobante
- [ ] Previsualización de imagen
- [ ] Estados de pago
- [ ] Historial de pagos

---

## 👨‍💼 FASE 8: DASHBOARD ADMIN
**Descripción**: Panel admin para aprobar pagos y activar anuncios

### 8.1 Backend
- [ ] Crear modelo Admin (o usar Django admin mejorado)
- [ ] API para obtener pagos pendientes
- [ ] API para aprobar/rechazar pagos
- [ ] API para activar/desactivar anuncios

### 8.2 Frontend
- [ ] AdminDashboard.vue
- [ ] PendingPayments.vue
- [ ] JobApproval.vue
- [ ] PaymentManagement.vue
- [ ] Analytics/Stats.vue

### 8.3 Features
- [ ] Visualización de comprobantes
- [ ] Aprobación en masa
- [ ] Rechazo con motivo
- [ ] Estadísticas de pagos
- [ ] Historial de acciones

---

## 📊 TAREAS INMEDIATAS (PRÓXIMA SESIÓN - Sesión 3)

### 🎯 Prioridad 1: FASE 2 - Publicación de Trabajos (CRITICAL)
**Estado**: Frontend 100% (wizard completo), Backend 0% (pendiente)
1. **Backend**:
   - ✅ Job model exists - Revisar campos faltantes
   - [ ] Endpoint POST `/api/jobs/publish` - Crear trabajo
   - [ ] Endpoint GET `/api/jobs/{id}` - Obtener detalle
   - [ ] Endpoint PATCH `/api/jobs/{id}/edit` - Editar trabajo
   - [ ] Validación completa de datos
   - [ ] Asociar con usuario autenticado

2. **Frontend Integration**:
   - [ ] Conectar PublishView.vue con endpoint
   - [ ] Implementar submit del wizard
   - [ ] Loading states
   - [ ] Error handling
   - [ ] Success confirmation + redirect

3. **Testing**:
   - [ ] Probar creación de trabajo
   - [ ] Probar validaciones
   - [ ] Probar redirección

### 🎯 Prioridad 2: FASE 5 - Perfiles de Empresa (COMPLETAR)
**Estado**: Modelo 100%, Frontend 80% completado
1. [ ] Revisar CompanyProfileEdit.vue (ya existe)
2. [ ] Revisar CompanyProfile model en backend
3. [ ] API endpoints (ya parcialmente creados)
4. [ ] Testing de CRUD

### 🎯 Prioridad 3: FASE 3 - Búsqueda y Filtrado (SIGUIENTE)
**Estado**: 0% (no iniciada)
- Será para después de FASE 2 y FASE 5

---

## 🎨 DESIGN TOKENS (Mantener consistencia)

### Colores
```
Primary: #7C3AED (Purple)
Secondary: #10B981 (Green)
Warning: #FF8F00 (Orange)
Error: #EF4444 (Red)
Gray: #E2E8F0 (Borders)
Dark: #1A1A2E (Text)
```

### Componentes reutilizables
- ✅ LoginForm (con validación y animaciones)
- ✅ RegisterForm (con strength indicator)
- ✅ ForgotPasswordForm
- ⏳ ProfileForm (FASE 4)
- ⏳ CompanyForm (FASE 5)
- ⏳ ApplicationForm (FASE 6)
- ⏳ PaymentModal (FASE 7)

---

## 📈 CRITERIOS DE ÉXITO POR FASE

### FASE 4 ✅
- Usuario puede completar su perfil
- Foto se guarda correctamente
- Perfil es visible en URL pública
- Cambios persisten en BD

### FASE 5 ✅
- Usuario puede crear empresa
- Logo se guarda
- Empresa vinculada a usuario

### FASE 2 ✅
- Trabajo se publica en BD
- Usuario ve confirmación
- Puede ver su publicación

### FASE 3 ✅
- Búsqueda funciona
- Filtros aplican correctamente
- Paginación funciona

### FASE 6 ✅
- Usuario puede aplicar
- Empresa ve candidatos
- Estados funcionan

### FASE 7 ✅
- Comprobante se sube
- Sistema de pagos funciona
- Anuncio se activa al aprobar

### FASE 8 ✅
- Admin aprueba/rechaza pagos
- Anuncios se activan automáticamente
- Estadísticas se muestran

---

## 🔗 RECURSOS CLAVE

### Backend Paths
```
auth_api/views.py - Endpoints de autenticación ✅
profiles/views.py - Perfiles (CREAR FASE 4)
companies/views.py - Empresas (CREAR FASE 5)
jobs/views.py - Trabajos existentes
applications/views.py - Aplicaciones (CREAR FASE 6)
payments/views.py - Pagos (CREAR FASE 7)
```

### Frontend Paths
```
src/views/Auth/* - Auth pages ✅
src/views/DashboardView.vue - Dashboard (actualizar)
src/components/Auth/* - Auth forms ✅
src/components/Profile/* - Profiles (CREAR)
src/components/Company/* - Company (CREAR)
src/components/Job/* - Jobs
src/stores/ - Pinia stores (ampliar)
```

---

## 💡 NOTAS IMPORTANTES

1. **Autenticación**: ✅ Ya está implementada y funcionando
2. **Próximo paso**: FASE 4 (Perfiles) es el más lógico
3. **Testing**: Probar completamente cada fase antes de siguiente
4. **API**: Documentar endpoints a medida que se crean
5. **DB**: Hacer backups antes de migrations importantes

---

## 📅 ÚLTIMA ACTUALIZACIÓN
- **Fecha**: 2025-11-20 (Sesión 2)
- **Sesión**: CRUD Foto + Dashboard Styling + Profile Name Sync
- **Completado**:
  - ✅ CRUD Foto de Perfil (upload/display/delete)
  - ✅ Unificación de colores dashboard (todos botones gradient purple)
  - ✅ Fix error 404 en sidebar "Publicar Un Nuevo Trabajo"
  - ✅ Sincronización de nombre en DashboardHome
- **Commits creados**:
  - `957c355` - Unificación completa de gradientes purple
  - `67c6c62` - Fix: Actualizar nombre de usuario en DashboardHome
- **Próximo foco**: FASE 2 - Publicación de Trabajos (Backend + Integration)
- **Status**: Ready para empezar FASE 2 mañana

