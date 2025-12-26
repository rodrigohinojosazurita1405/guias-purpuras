# 🔐 Sistema de Recuperación de Contraseña - Guías Púrpuras

## ✅ Implementación Completada

Se ha implementado un sistema completo de recuperación de contraseña que funciona tanto en **localhost** como en **producción (Render)**.

---

## 📦 Archivos Creados/Modificados

### Backend:
1. **`backend/auth_api/models.py`** - Modelo `PasswordResetToken` agregado
2. **`backend/auth_api/views.py`** - Endpoints `forgot_password` y `reset_password` implementados
3. **`backend/auth_api/urls.py`** - Ruta `/api/auth/reset-password` agregada
4. **`backend/core/settings.py`** - Configuración de email agregada
5. **`backend/auth_api/migrations/0003_passwordresettoken.py`** - Migración aplicada ✓
6. **`backend/test_password_recovery.py`** - Script de pruebas creado

### Frontend:
1. **`frontend/src/components/Auth/ForgotPasswordForm.vue`** - Rediseñado (eliminadas animaciones pesadas)
2. **`frontend/src/components/Auth/ResetPasswordForm.vue`** - Nuevo componente creado
3. **`frontend/src/views/Auth/ResetPasswordView.vue`** - Nueva vista creada
4. **`frontend/src/router/index.js`** - Ruta `/reset-password/:token` agregada

---

## 🚀 Cómo Probar en Localhost

### Paso 1: Iniciar el Servidor Backend
```bash
cd backend
python manage.py runserver
```

**IMPORTANTE**: Los emails se mostrarán en esta consola (no se envían realmente)

### Paso 2: Iniciar el Frontend
```bash
cd frontend
npm run dev
```

### Paso 3: Probar el Flujo Completo

#### Opción A: Prueba Manual
1. Ve a `http://localhost:5173/login`
2. Haz clic en "¿Olvidaste tu contraseña?"
3. Ingresa un email registrado
4. Ve a la consola del backend y copia el **TOKEN** y la **URL**
5. Abre la URL en el navegador: `http://localhost:5173/reset-password/TOKEN`
6. Ingresa tu nueva contraseña
7. Inicia sesión con la nueva contraseña

#### Opción B: Script de Pruebas Automático
```bash
cd backend
python test_password_recovery.py
```

Este script probará:
- ✓ Registro de usuario
- ✓ Solicitud de recuperación
- ✓ Cambio de contraseña
- ✓ Login con nueva contraseña
- ✓ Rechazo de tokens inválidos

---

## 🌐 Configuración para Producción (Render)

Cuando despliegues en Render, necesitarás configurar **variables de entorno**:

### Variables Requeridas en Render

Ve a tu dashboard de Render → Settings → Environment Variables y agrega:

#### 1. Email Backend (Obligatorio)
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tuempresa@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password_de_gmail
DEFAULT_FROM_EMAIL=noreply@guiaspurpuras.com
```

#### 2. URL del Frontend (Obligatorio)
```
FRONTEND_URL=https://tuapp.vercel.app
```

---

## 📧 Opciones de Email en Producción

### Opción 1: Gmail (Recomendado para empezar)

#### Configurar App Password de Gmail:
1. Ve a https://myaccount.google.com/security
2. Habilita "Verificación en 2 pasos"
3. Ve a "Contraseñas de aplicaciones"
4. Selecciona "Correo" y "Otro dispositivo"
5. Genera una contraseña de 16 caracteres
6. Usa esa contraseña en `EMAIL_HOST_PASSWORD`

#### Variables de Entorno para Gmail:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tuempresa@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx  (16 caracteres sin espacios)
DEFAULT_FROM_EMAIL=noreply@guiaspurpuras.com
```

### Opción 2: SendGrid (100 emails/día gratis)

```
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu_api_key_de_sendgrid
DEFAULT_FROM_EMAIL=noreply@guiaspurpuras.com
```

### Opción 3: Mailgun (5,000 emails/mes gratis)

```
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=postmaster@tudominio.mailgun.org
EMAIL_HOST_PASSWORD=tu_password_de_mailgun
DEFAULT_FROM_EMAIL=noreply@guiaspurpuras.com
```

---

## 🔒 Características de Seguridad

✅ **Tokens seguros**: Generados con `secrets.token_urlsafe(32)`
✅ **Expiración de tokens**: 1 hora de validez
✅ **Uso único**: Cada token solo se puede usar una vez
✅ **Invalidación automática**: Tokens anteriores se invalidan al crear uno nuevo
✅ **No revela si el email existe**: Mismo mensaje para emails existentes y no existentes
✅ **Validación de contraseñas**: Mínimo 6 caracteres

---

## 📍 Endpoints del API

### POST `/api/auth/forgot-password`
Solicita recuperación de contraseña

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Si el email existe en nuestros registros, recibirás instrucciones de recuperación."
}
```

### POST `/api/auth/reset-password`
Restablece la contraseña con un token válido

**Request:**
```json
{
  "token": "token_de_recuperacion",
  "password": "nueva_contraseña"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Contraseña restablecida exitosamente"
}
```

---

## 🎨 Frontend - Rutas

- `/forgot-password` - Solicitar recuperación
- `/reset-password/:token` - Cambiar contraseña

---

## 🐛 Troubleshooting

### Email no se envía en localhost
✅ **Normal**: En desarrollo los emails se muestran en la consola del servidor, no se envían

### Email no se envía en producción
❌ Verifica:
- Variables de entorno configuradas correctamente en Render
- App password de Gmail generado correctamente
- EMAIL_HOST_USER es el email completo

### Token inválido o expirado
❌ Verifica:
- El token tiene menos de 1 hora
- No se ha usado antes
- Se copió correctamente (sin espacios)

### Error 404 en /reset-password/:token
❌ Verifica:
- El frontend se reinició después de agregar la ruta
- La ruta está en `router/index.js`

---

## 📊 Modelo de Base de Datos

```python
class PasswordResetToken(models.Model):
    user = ForeignKey(CustomUser)  # Usuario dueño del token
    token = CharField(max_length=100, unique=True)  # Token único
    created_at = DateTimeField(auto_now_add=True)  # Fecha de creación
    expires_at = DateTimeField()  # Fecha de expiración (1 hora)
    used = BooleanField(default=False)  # Si ya fue usado
```

---

## ✨ Mejoras Futuras (Opcional)

- [ ] Email HTML con mejor diseño
- [ ] Límite de intentos de recuperación por día
- [ ] Notificación al usuario cuando se cambia la contraseña
- [ ] Historial de cambios de contraseña
- [ ] Autenticación de dos factores (2FA)

---

## 📞 Soporte

Si tienes problemas:
1. Revisa la consola del servidor Django para ver logs
2. Revisa la consola del navegador para ver errores de frontend
3. Ejecuta `python test_password_recovery.py` para diagnosticar

---

**Desarrollado para Guías Púrpuras Bolivia** 🇧🇴
