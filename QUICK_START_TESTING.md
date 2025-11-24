# FASE 2: QUICK START TESTING

## ⚡ Configuración Rápida (5 minutos)

### Prerrequisitos
```bash
# Terminal 1: Backend
cd d:\Proyectos\ Django\GuiasPurpuras_V1.0
python manage.py runserver

# Terminal 2: Frontend
cd d:\Proyectos\ Django\GuiasPurpuras_V1.0\frontend
npm run dev

# Terminal 3: Testing (cuando necesites)
cd d:\Proyectos\ Django\GuiasPurpuras_V1.0
```

---

## 🧪 OPCIÓN 1: TESTING MANUAL (Recomendado)

### Paso 1: Registrarse
- URL: http://localhost:3000/register
- Email: `test@company.com`
- Password: `Test1234!`
- Guardar el token (se ve en console: `📝 Token guardado`)

### Paso 2: Publicar trabajo
- URL: http://localhost:3000/publicar
- Llenar cada paso:
  1. Tipo: "Desarrollo" / Ciudad: "La Paz"
  2. Título: "Senior Python Developer"
     Descripción: "Buscamos un desarrollador Python experimentado con mínimo 5 años"
  3. Plan: "Featured"
  4. Tipo aplicación: "Internal"
  5. Revisar y publicar

### Paso 3: Verificar
- ✅ Toast verde aparece
- ✅ Redirección a `/guias/trabajos/{ID}`
- ✅ Página de detalle carga

### Paso 4: Verificar en BD
```bash
python manage.py shell
>>> from jobs.models import Job
>>> Job.objects.latest('createdAt')
<Job: Senior Python Developer - Tech Solutions Bolivia>
```

---

## 🐍 OPCIÓN 2: TESTING AUTOMATIZADO

### Instalar dependencia:
```bash
pip install requests
```

### Obtener token:
1. Abre DevTools (F12)
2. Consola (Console tab)
3. Ejecuta: `localStorage.getItem('token')`
4. Copia el valor (sin comillas)

### Ejecutar tests:
```bash
python test_publish_job.py "TOKEN_AQUI"
```

### Output esperado:
```
✅ [PASS] Publicación válida completa
✅ [PASS] Publicación válida con datos mínimos
✅ [PASS] Sin título (requerido)
✅ [PASS] Título muy corto (<5 caracteres)
...
```

---

## 📊 CHECKLIST RÁPIDO

- [ ] Backend corre sin errores: `python manage.py runserver`
- [ ] Frontend corre sin errores: `npm run dev`
- [ ] Puedo registrarme
- [ ] Puedo logearme
- [ ] Token se guarda en localStorage
- [ ] Puedo navegar a /publicar
- [ ] Wizard de 5 pasos funciona
- [ ] Puedo llenar todos los campos
- [ ] Toast de éxito aparece
- [ ] Redirección al detalle funciona
- [ ] Trabajo aparece en BD

---

## 🔍 DEBUGGING

### Backend logs (en terminal):
Busca estas líneas:
```
📝 [PUBLISH_JOB] Usuario: test@company.com, Campos recibidos: [...]
[Cualquier error de validación]
✅ [PUBLISH_JOB] Éxito: ID=a1b2c3d4, Título="...", Plan=featured
```

### Frontend logs (F12 Console):
```
📝 Iniciando publicación...
Usuario: test@company.com
📤 Enviando a http://localhost:8000/api/jobs/publish...
📥 Response status: 201
✅ Publicación exitosa:
   ID: a1b2c3d4
🔗 Redirigiendo a /guias/trabajos/a1b2c3d4...
```

### Si falla:
1. Mira los logs de ambos lados
2. Verifica que token es válido
3. Verifica que todos los campos están llenos
4. Si error 500: mira traceback en backend
5. Si timeout: backend es lento, reinicia: `python manage.py runserver`

---

## 📝 Datos para pruebas rápidas

### Minimal (Funciona):
```
Título: Senior Dev
Descripción: Buscamos desarrollador con experiencia en tecnología web moderna
Email: recruiter@tech.com
Ciudad: La Paz
Tipo contrato: Tiempo Completo
Fecha vencimiento: 2025-12-31
Requisitos: Mínimo 3 años experiencia
```

### Completo (Más realista):
```
Título: Senior Full Stack Developer
Descripción: Buscamos un Senior Full Stack Developer con experiencia en Django y Vue.js para unirse a nuestro equipo dinámico de desarrollo.
Empresa: Tech Solutions Bolivia
Email: recruiter@techsolutions.bo
Ciudad: La Paz
Categoría: Tecnología
Subcategoría: Desarrollo Web
Tipo contrato: Tiempo Completo
Modalidad: Híbrido
Fecha vencimiento: 2025-12-31
Requisitos: Mínimo 5 años de experiencia en desarrollo web, conocimiento de Python/Django, Vue.js, PostgreSQL
Responsabilidades: Desarrollar features backend, code review, mentoring
Educación: Licenciatura en Ingeniería Informática
Experiencia: Senior (5+ años)
Idiomas: Español, Inglés
Skills técnicos: Django, Vue.js, PostgreSQL, Docker, Git
Salario: Rango 35000 - 50000 Bs
Beneficios: Bonos, Seguro médico, Home office
Vacantes: 2
WhatsApp: +591 7654321
Website: https://techsolutions.bo
Plan: Featured
Tipo aplicación: Internal
```

---

## 🎯 Test rápido de 5 minutos

```bash
# Terminal 1: Backend
python manage.py runserver

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: Testing
# Abre http://localhost:3000/register
# Crea cuenta: test@company.com / Test1234!
# Copia token: localStorage.getItem('token')
# Abre http://localhost:3000/publicar
# Llena formulario (usa datos minimal arriba)
# Click "Publicar"
# Verifica ✅ Toast verde
# Verifica ✅ Página de detalle carga
# Listo! 🎉
```

---

## ✅ SUCCESS

Cuando todo funciona:
1. Puedes publicar un trabajo
2. El trabajo aparece en la BD
3. El trabajo es accesible via URL
4. Los errores se muestran claramente
5. El flujo es rápido y suave

¡Felicidades! 🎉 FASE 2 está lista.
