# 🟣 Guías Púrpuras

Plataforma de clasificados para Bolivia - Encuentra profesionales, restaurantes, trabajos y servicios.

## 🚀 Tecnologías

- **Frontend**: Vue 3 + Vuestic UI
- **Backend**: Django + PostgreSQL (En desarrollo)

## 📦 Instalación
```bash
cd frontend
npm install
npm run dev
```

## 🎨 Paleta de Colores

- Púrpura Principal: `#5C0099`
- Amarillo: `#FDC500`
- btns:background: linear-gradient(135deg, #7c3aed, #6d28d9);

## 📋 Estado del Proyecto

### FASE 7: Sistema de Publicación de Anuncios de Trabajo

#### FASE 7.1: Validación de Pago - ✅ COMPLETADO
- ✅ Modelo Job con campo proofOfPayment (ImageField)
- ✅ Campo paymentVerified en Job model
- ✅ Validación de imagen (PNG, JPG, GIF, max 5MB)
- ✅ Almacenamiento en media/payment_proofs/
- ✅ Vista publish_job con validación de pago obligatorio
- ✅ Decorador token_required con validación JWT (AccessToken)
- ✅ Componente Vue PublishForm con 5 pasos
- ✅ Comprobante de pago como paso final obligatorio
- ✅ Conexión frontend-backend funcionando correctamente
- ✅ Anuncios se crean y guardan exitosamente

#### FASE 7.2: Configuración de Aplicación - ✅ COMPLETADO
- ✅ Campo applicationType (internal, external, both)
- ✅ Componente ApplicationConfigStep con renderizado condicional
- ✅ Campo externalApplicationUrl para aplicaciones externas
- ✅ Campo applicationInstructions (mostrado solo en externas)
- ✅ Campos de contacto directo: email, whatsapp, website
- ✅ Campos de contact visible solo para external/both
- ✅ Preguntas de filtrado (screeningQuestions) solo para internal/both
- ✅ Validación de al menos un método de contacto

#### FASE 7.3: Gestión de Anuncios - ⏳ PENDIENTE
- ⏳ Edición de anuncios publicados
- ⏳ Eliminación de anuncios
- ⏳ Renovación de anuncios
- ⏳ Cambio de estado (activo/pausado/archivado)

#### FASE 7.4: Aplicaciones a Anuncios - ⏳ PENDIENTE
- ⏳ Sistema de aplicaciones (interno)
- ⏳ Filtrado por preguntas screening
- ⏳ Vista de aplicaciones para publicador
- ⏳ Cambio de estado de aplicaciones
- ⏳ Notificaciones a candidatos

#### FASE 7.5: Dashboard de Publicador - ⏳ PENDIENTE
- ⏳ Estadísticas de anuncios
- ⏳ Anuncios publicados activos
- ⏳ Anuncios con aplicaciones
- ⏳ Historial de actividad

### Otros Módulos

#### Autenticación y Usuarios
- ✅ Sistema JWT con rest_framework_simplejwt
- ✅ Decorador token_required con validación AccessToken
- ✅ Login/Register endpoints
- ✅ Validación de tokens expirados

#### Frontend
- ✅ Paleta de colores púrpura
- ✅ Componentes Vuestic UI
- ✅ Navegación entre pasos
- ✅ Validación de formularios
- ✅ Integración con API

## 🔄 Bugs Solucionados Recientemente (c7620a7)

1. **Estructura de excepciones rotas** - Mensaje de éxito dentro del bloque except
2. **Validación JWT incorrecta** - Cambio de UntypedToken a AccessToken
3. **Problemas Unicode** - Reemplazo de emojis por texto ASCII

## 👨‍💻 Autor

Tu Nombre - Cochabamba, Bolivia