# 🟣 Guías Púrpuras

Plataforma de clasificados para Bolivia - Encuentra profesionales, restaurantes, trabajos y servicios.

## 📁 Estructura del Proyecto

```
GuiasPurpuras_V1.0/
├── backend/              # Backend Django (API REST)
│   ├── auth_api/        # Autenticación y usuarios
│   ├── jobs/            # Ofertas de trabajo (core)
│   ├── catalogs/        # Catálogos dinámicos
│   ├── payments/        # Órdenes y facturación
│   ├── moderation/      # Moderación de usuarios
│   ├── dashboard/       # Estadísticas de usuario
│   ├── profiles/        # Perfiles de empresa
│   ├── plans/           # Planes de publicación
│   ├── audit/           # Sistema de auditoría
│   ├── reports/         # Sistema de reportes
│   ├── core/            # Configuración Django
│   ├── static/          # Archivos estáticos
│   ├── media/           # Uploads de usuarios
│   ├── manage.py        # CLI de Django
│   └── db.sqlite3       # Base de datos
│
├── frontend/            # Frontend Vue 3
│   ├── src/            # Código fuente Vue
│   ├── public/         # Archivos públicos
│   ├── package.json    # Dependencias NPM
│   └── vite.config.js  # Configuración Vite
│
├── env/                # Entorno virtual Python
└── README.MD          # Este archivo
```

## 🚀 Tecnologías

### Backend
- **Framework**: Django 5.2.7
- **Base de datos**: SQLite (desarrollo) → PostgreSQL (producción)
- **API**: Django REST Framework
- **Autenticación**: JWT (Simple JWT)
- **Admin**: Django Jazzmin

### Frontend
- **Framework**: Vue 3 + Composition API
- **UI**: Vuestic UI
- **Build**: Vite
- **Routing**: Vue Router

## 📦 Instalación

### Backend
```bash
# Activar entorno virtual
cd backend
source ../env/bin/activate  # Linux/Mac
../env/Scripts/activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🎨 Paleta de Colores

- Púrpura Principal: `#5C0099`
- Amarillo: `#FDC500`

## 🏗️ Arquitectura Backend (Modular)

El backend está organizado en **apps modulares especializadas**:

- **jobs** → Gestión de ofertas de trabajo
- **catalogs** → Catálogos dinámicos (categorías, ciudades, tipos de contrato)
- **payments** → Órdenes de pago y facturación
- **moderation** → Bloqueo y moderación de usuarios
- **dashboard** → Estadísticas y métricas de usuario
- **profiles** → Perfiles de empresa
- **plans** → Planes de publicación
- **audit** → Registro de cambios y auditoría
- **reports** → Sistema de reportes

## 📋 Estado del Proyecto

### Completado ✅
- ✅ Frontend básico con Vue 3
- ✅ Sistema de rutas
- ✅ Backend Django modular
- ✅ API REST completa
- ✅ Autenticación JWT
- ✅ Admin personalizado (Jazzmin)
- ✅ Sistema de pagos
- ✅ Sistema de moderación
- ✅ Auditoría automática

### En Desarrollo 🔄
- 🔄 Integración frontend-backend
- 🔄 Sistema de notificaciones
- 🔄 Dashboard de estadísticas
- 🔄 Migración a PostgreSQL

### Pendiente ⏳
- ⏳ Deploy en producción
- ⏳ Sistema de mensajería
- ⏳ Pasarela de pagos

## 🌐 URLs de Desarrollo

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:5173
- **Admin Django**: http://localhost:8000/admin

## 👨‍💻 Autor

**RodrigoHinojosaZ** - Cochabamba, Bolivia

## 📄 Licencia

Proyecto privado - Todos los derechos reservados
