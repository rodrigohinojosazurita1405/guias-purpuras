# FASE 2: PUBLICACIÓN DE TRABAJOS - GUÍA DE TESTING

## 📋 Estado Actual

✅ **Backend**: Endpoint mejorado con validaciones robustas
✅ **Frontend**: Error handling completo y timeout management
✅ **Autenticación**: Token_required decorator validado
✅ **Sincronización**: Frontend-Backend datos sincronizados

---

## 🧪 TESTING END-TO-END

### Opción 1: Testing Manual (Recomendado para primera verificación)

#### Pasos:

1. **Asegurar que backend está corriendo:**
   ```bash
   # En una terminal
   python manage.py runserver
   # Debería estar en http://localhost:8000
   ```

2. **Asegurar que frontend está corriendo:**
   ```bash
   # En otra terminal
   cd frontend
   npm run dev
   # Debería estar en http://localhost:3000
   ```

3. **Registrarse/Loguearse:**
   - Ir a http://localhost:3000/register
   - Crear una cuenta (ej: test@company.com / password123)
   - O ir a http://localhost:3000/login si ya existe cuenta

4. **Publicar un trabajo:**
   - Hacer click en "Publicar" en el navbar
   - Llenar el formulario:
     - **Paso 0:** Seleccionar tipo de trabajo y ciudad
     - **Paso 1:** Llenar información del trabajo (REQUERIDO: título, descripción, email, ciudad, tipo contrato, fecha, requisitos)
     - **Paso 2:** Seleccionar plan (free, featured, top)
     - **Paso 3:** Configurar postulaciones (tipo interno/externo)
     - **Paso 4:** Revisar resumen y publicar

5. **Verificar éxito:**
   - Debería aparecer toast verde: "¡Oferta publicada exitosamente! 🎉"
   - Debería redirigir a `/guias/trabajos/{ID}`
   - En la BD debería existir el trabajo con el ID correspondiente

#### Verificar en Base de Datos:

```bash
# Abre shell de Django
python manage.py shell

# Verifica que el trabajo se creó
from jobs.models import Job
jobs = Job.objects.all().order_by('-createdAt')[:1]
print(jobs[0])  # Debería mostrar tu trabajo reciente
```

---

### Opción 2: Testing Automatizado (Script Python)

#### Requisitos:
```bash
pip install requests
```

#### Ejecutar:

1. **Sin token (te pedirá que ingreses uno):**
   ```bash
   python test_publish_job.py
   ```

2. **Con token (copia de login):**
   ```bash
   python test_publish_job.py "YOUR_JWT_TOKEN_HERE"
   ```

3. **Con variable de entorno:**
   ```bash
   export JWT_TOKEN="YOUR_JWT_TOKEN_HERE"
   python test_publish_job.py
   ```

#### Qué prueba el script:

✅ Publicación válida completa
✅ Publicación con datos mínimos
❌ Sin título (error requerido)
❌ Título muy corto
❌ Sin descripción
❌ Sin email
❌ Email inválido
❌ Sin ciudad
❌ Sin tipo contrato
❌ Sin fecha vencimiento
❌ Sin requisitos
❌ Modalidad inválida
❌ Tipo de salario inválido
❌ Tipo de aplicación inválido
❌ Plan inválido
❌ Rango de salario inválido
❌ Valores de salario no numéricos

---

### Opción 3: Testing con cURL (En terminal)

#### 1. Obtener un token (después de login):
```bash
# El token está en localStorage después de login
# Abre DevTools > Application > LocalStorage > token
# O cópialo del JWT_TOKEN cuando hagas login
```

#### 2. Publicar un trabajo:
```bash
TOKEN="your_jwt_token_here"
curl -X POST http://localhost:8000/api/jobs/publish \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Senior Developer",
    "description": "Buscamos un senior developer con experiencia en Django y Vue.js",
    "email": "recruiter@company.com",
    "city": "La Paz",
    "contractType": "Tiempo Completo",
    "expiryDate": "2025-12-31",
    "requirements": "Mínimo 5 años de experiencia",
    "companyName": "Tech Solutions",
    "selectedPlan": "featured"
  }'
```

#### 3. Respuesta exitosa:
```json
{
  "success": true,
  "message": "¡Oferta publicada exitosamente!",
  "id": "a1b2c3d4",
  "createdAt": "2025-11-24T10:30:00Z"
}
```

---

## 🐛 DEBUGGING

### Si falla la publicación:

1. **Abre DevTools (F12)** en el navegador
2. **Tab "Console"**: Busca logs con 📝 📥 ❌ ✅
3. **Tab "Network"**:
   - Busca request POST a `/api/jobs/publish`
   - Verifica status code (201 = éxito, 400 = validación, 401 = auth, 500 = servidor)
   - Mira el response para detalles del error

### Errores comunes:

| Error | Causa | Solución |
|-------|-------|----------|
| 401 Unauthorized | Token inválido/expirado | Cierra sesión y vuelve a loguearte |
| 400 Bad Request | Campos faltantes | Verifica que completaste todos los campos requeridos |
| 500 Internal Server Error | Error en BD | Verifica logs de Django: `python manage.py runserver` |
| TIMEOUT | Servidor lento | Espera o reinicia: `python manage.py runserver` |
| Connection refused | Servidor no corre | Inicia: `python manage.py runserver` |

---

## 📊 CHECKLIST DE PRUEBAS

### Antes de considerar FASE 2 completa:

- [ ] **Frontend validation**
  - [ ] Se valida título (5-200 caracteres)
  - [ ] Se valida descripción (min 20 caracteres)
  - [ ] Se valida email
  - [ ] Se valida campos requeridos antes de enviar
  - [ ] Toast de error muestra campos específicos

- [ ] **Backend validation**
  - [ ] Rechaza sin título
  - [ ] Rechaza descripción corta
  - [ ] Rechaza email inválido
  - [ ] Rechaza datos incompletos (ciudad, contrato, fecha, requisitos)
  - [ ] Rechaza modalidad inválida
  - [ ] Rechaza rango de salario inválido
  - [ ] Rechaza plan inválido

- [ ] **Authentication**
  - [ ] Rechaza request sin token (401)
  - [ ] Rechaza token expirado (401)
  - [ ] Rechaza token inválido (401)
  - [ ] Permite request con token válido (201)

- [ ] **Response handling**
  - [ ] Status 201 para éxito
  - [ ] Status 400 para validación
  - [ ] Status 401 para auth
  - [ ] Status 500 para servidor
  - [ ] Response incluye `id` y `createdAt`

- [ ] **UX/Frontend**
  - [ ] Toast de éxito aparece
  - [ ] Toast de error aparece con mensaje
  - [ ] Loading state visual (isSubmitting)
  - [ ] Redirección a `/guias/trabajos/{id}` funciona
  - [ ] Timeout manejo (30s)

- [ ] **Database**
  - [ ] Job se crea en BD
  - [ ] Todos los campos se guardan correctamente
  - [ ] ID se genera automáticamente
  - [ ] Timestamps (createdAt, updatedAt) son correctos
  - [ ] Status por defecto es 'active'

- [ ] **Data persistence**
  - [ ] Trabajo aparece en GET /api/jobs/
  - [ ] Trabajo aparece en GET /api/jobs/{id}
  - [ ] Logo de empresa se carga (si existe)
  - [ ] Salary se formatea correctamente

---

## 📈 PRÓXIMOS PASOS (Después de FASE 2)

1. **FASE 3**: Búsqueda y filtrado
   - GET /api/jobs con parámetros
   - Filtros: ciudad, categoría, salario
   - Paginación

2. **FASE 6**: Sistema de postulaciones
   - Modelo Application
   - POST /api/jobs/{id}/apply
   - CV Formato Harvard

3. **FASE 9**: Dashboard Multi-Rol
   - Reclutador ve postulaciones
   - Postulante ve estado
   - Sistema de mensajería

---

## 📝 NOTAS IMPORTANTES

### Cambios realizados en FASE 2:

#### Backend (`jobs/views.py`)
- ✅ Validaciones de campos requeridos (title, description, email, city, contractType, expiryDate, requirements)
- ✅ Validaciones de longitud (title 5-200, description min 20)
- ✅ Validaciones de enums (modality, salaryType, applicationType, selectedPlan)
- ✅ Validaciones de rango de salario
- ✅ Conversión de tipos (float para salario, int para vacancies)
- ✅ Logging detallado (📝 📥 ❌ ✅)
- ✅ Errores estructurados con campo específico

#### Frontend (`frontend/src/views/PublishView.vue`)
- ✅ Validación pre-submit de campos requeridos
- ✅ Manejo granular de errores por status code (400, 401, 500)
- ✅ Timeout management (30s)
- ✅ Diferenciación de errores de red
- ✅ Logging para debugging
- ✅ Validación de respuesta antes de usar datos
- ✅ AbortController para timeout

#### Security
- ✅ Token_required decorator en endpoint
- ✅ Bearer token validation
- ✅ User authentication check en frontend
- ✅ Logout y redirect en token expirado

---

## 🎯 Criterios de éxito

✅ Trabajo se publica exitosamente
✅ Trabajo aparece en BD
✅ Trabajo es accesible via GET /api/jobs/{id}
✅ Errores de validación se muestran correctamente
✅ Autenticación se valida
✅ Redirección post-publicación funciona
✅ Todos los campos se guardan correctamente
