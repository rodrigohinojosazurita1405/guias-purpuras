# 🧪 GUÍA DE PRUEBA - CAMPO EMAIL AGREGADO

**Fecha:** 2025-11-25
**Estado:** ✅ Listo para probar
**Objetivo:** Verificar que el campo email funciona correctamente en Step 2

---

## 📝 INSTRUCCIONES PASO A PASO

### Paso 1: Navega a Publicar Oferta
1. Ve a http://localhost:3000 (o tu URL de frontend)
2. Inicia sesión (si no estás autenticado)
3. Haz clic en **"Publicar Oferta"**

### Paso 2: Completa Steps 0 y 1
1. **Step 0:** Selecciona tipo de trabajo y ciudad
2. **Step 1:** Elige un plan de pago (cualquiera)
3. Haz clic en **"SIGUIENTE"**

### Paso 3: Step 2 - Información del Trabajo (AQUÍ ESTÁ EL EMAIL)

Ahora verás el formulario con **TODOS los campos incluyendo EMAIL**:

```
┌─ INFORMACIÓN BÁSICA DEL PUESTO ─────────┐
│ • Título del Puesto *                   │
│ • Nombre de la Empresa *                │
│ • Publicar de forma anónima             │
│ • Descripción del Trabajo *             │
└─────────────────────────────────────────┘

┌─ UBICACIÓN Y TIPO DE PUESTO ────────────┐
│ • Categoría/Área *                      │
│ • Ciudad *                              │
│ • Provincia/Municipio                   │
│ • Fecha de Vencimiento *                │
│ • Tipo de Contrato *                    │
│ ┌─ EMAIL DE CONTACTO * ───────────────┐ │
│ │ [tu.email@empresa.com]              │ │ ← NUEVO CAMPO
│ │ Los candidatos podrán contactarte    │ │
│ │ a través de este email              │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘

┌─ REQUISITOS Y COMPETENCIAS ─────────────┐
│ • Requisitos y Responsabilidades *      │
│ • Competencias Técnicas                 │
│ • Competencias Blandas                  │
└─────────────────────────────────────────┘

┌─ COMPENSACIÓN Y BENEFICIOS ─────────────┐
│ • Tipo de Salario                       │
│ • Salario Mínimo/Máximo *               │
│ • Beneficios Adicionales                │
└─────────────────────────────────────────┘

┌─ NÚMERO DE VACANTES ────────────────────┐
│ • Vacantes: [1]                         │
└─────────────────────────────────────────┘

[ATRÁS] [SIGUIENTE] ← Click para continuar
```

### Paso 4: Prueba Validación de Email

#### Escenario A: Sin llenar email

1. Deja el campo **Email de Contacto** vacío
2. Haz clic en **SIGUIENTE**
3. **Resultado Esperado:**
   ```
   ❌ Alert: "El email de contacto es requerido"
   → No avanzas a Step 3
   ```

#### Escenario B: Email inválido

1. Ingresa un email sin @: `usuario` o `usuario.com`
2. Haz clic en **SIGUIENTE**
3. **Resultado Esperado:**
   ```
   ❌ Alert: "El email debe ser válido"
   → No avanzas a Step 3
   ```

#### Escenario C: Email válido (CORRECTO)

1. Ingresa email válido: `tu.email@empresa.com`
2. Haz clic en **SIGUIENTE**
3. **Resultado Esperado:**
   ```
   ✅ Avanzas a Step 3 (ApplicationConfigStep)
   → Email queda guardado internamente
   ```

---

## 🧪 PRUEBA COMPLETA (End-to-End)

### Formulario Completo

Rellena **TODOS** los campos así:

| Campo | Valor |
|---|---|
| **Título del Puesto** | Ingeniero de Software |
| **Empresa** | TechCorp Bolivia |
| **Anónimo** | No |
| **Descripción** | Se busca ingeniero con experiencia en desarrollo full-stack. Responsable de arquitectura y desarrollo de sistemas. Mínimo 5 años de experiencia. |
| **Categoría** | Sistemas |
| **Ciudad** | La Paz |
| **Provincia** | Cercado |
| **Fecha Vencimiento** | 2025-12-31 |
| **Tipo de Contrato** | Tiempo Completo |
| **📧 EMAIL** | contacto@techcorp.com.bo |
| **Requisitos** | Licenciatura en Informática o área relacionada. Experiencia con Python, Django, React. Knowledge of PostgreSQL. |
| **Habilidades Técnicas** | Python, Django, JavaScript, React, PostgreSQL, Docker |
| **Habilidades Blandas** | Liderazgo, comunicación, resolución de problemas |
| **Salario** | Rango: 5000 - 8000 Bs |
| **Beneficios** | Seguro de salud, bono anual, capacitación |
| **Vacantes** | 2 |

### Resultado Esperado

1. ✅ **Step 2 avanza** → Todos los campos incluido email son válidos
2. ✅ **Step 3** → Puedes configurar tipo de aplicación
3. ✅ **Step 4** → Ves resumen con email guardado
4. ✅ **Publicar** → Email se envía al backend exitosamente

---

## 🔍 VER DATOS EN CONSOLA

### En la Consola del Navegador (F12)

Cuando hagas clic en SIGUIENTE en Step 2, verás en la consola:

```javascript
// De PublishView.vue:
{
  "title": "Ingeniero de Software",
  "companyName": "TechCorp Bolivia",
  "description": "Se busca ingeniero...",
  "email": "contacto@techcorp.com.bo",  // ✅ Email está aquí
  "city": "La Paz",
  // ... otros campos
}
```

### En la Consola del Backend (Django)

Cuando publiques (Step 4), verás en la terminal:

```
📤 Enviando a http://localhost:8000/api/jobs/publish...
{'email': 'contacto@techcorp.com.bo', ...}
```

---

## 🐛 DEBUGGING SI HAY PROBLEMAS

### Si aún dice "Email es requerido"

1. Limpia caché del navegador: **Ctrl+Shift+Del** (o Cmd+Shift+Del)
2. Recarga la página: **F5**
3. Intenta nuevamente

### Si no ves el campo email

1. Verifica que el frontend fue buildead:
   ```bash
   cd frontend && npm run build
   ```

2. Verifica que los cambios están en el archivo:
   ```bash
   grep -n "Email de Contacto" frontend/src/views/FormCreate/InformationStepJob.vue
   ```

3. Resultado esperado: **DEBE encontrar línea 230 con "Email de Contacto"**

### Si email no se envía al backend

1. Abre la consola del navegador (F12)
2. En PublishView.handleSubmit(), verifica que email esté presente
3. Debe mostrar:
   ```
   🔍 Datos para validación: {
     email: true,  // ← DEBE ser true
     ...
   }
   ```

---

## ✅ CHECKLIST DE VERIFICACIÓN

- [ ] Campo email visible en Step 2
- [ ] Email tiene icono de sobre
- [ ] Validación rechaza email vacío
- [ ] Validación rechaza email sin @
- [ ] Validación acepta email con @ válido
- [ ] Hint muestra: "Los candidatos podrán contactarte..."
- [ ] Step 2 valida email al hacer clic SIGUIENTE
- [ ] Email se guarda en publishStore.jobData.email
- [ ] Step 4 muestra email en el resumen
- [ ] Publicación exitosa con email enviado

---

## 📊 DATOS TÉCNICOS

### Ubicación del Campo en el Código

```
frontend/src/views/FormCreate/InformationStepJob.vue

Líneas 228-249:    Template (Input HTML)
Línea 545:         localFormData.email init
Líneas 747-751:    Validación
```

### Validación Regex

```javascript
/^[^\s@]+@[^\s@]+\.[^\s@]+$/

Explicación:
- ^[^\s@]+    : Comienza con 1+ caracteres sin espacios ni @
- @           : Seguido de @
- [^\s@]+     : Seguido de 1+ caracteres sin espacios ni @
- \.          : Seguido de punto literal
- [^\s@]+$    : Termina con 1+ caracteres sin espacios ni @

Ejemplos válidos:
- usuario@empresa.com          ✅
- contacto@techcorp.com.bo     ✅
- nombre.apellido@email.org    ✅

Ejemplos inválidos:
- usuario                      ❌
- usuario@                     ❌
- usuario@empresa              ❌
- usuario @empresa.com         ❌ (espacio)
```

---

## 🎯 CASO DE USO REAL

### Usuario: María Gómez
**Rol:** Gerente de RRHH en TechCorp

#### Flujo:
1. María entra a Guías Púrpuras
2. Hace clic en "Publicar Oferta"
3. **Step 0:** Selecciona "Ingeniero de Software" + "La Paz"
4. **Step 1:** Elige Plan Púrpura (79 Bs)
5. **Step 2:** Rellena todos los datos incluyendo:
   - Título: "Ingeniero Backend Senior"
   - Empresa: "TechCorp Bolivia"
   - **Email: maria.gomez@techcorp.com.bo** ← NUEVO
   - Requisitos: "5+ años Python/Django"
   - Etc.
6. **Step 3:** Configura postulaciones internas
7. **Step 4:** Sube comprobante de pago y completa datos de facturación
8. Haz clic en **"PUBLICAR OFERTA"**
9. ✅ Oferta publicada exitosamente
10. ✅ Email guardado: `maria.gomez@techcorp.com.bo`
11. ✅ Candidatos pueden contactar a través de este email

---

## 🚀 SIGUIENTES PASOS OPCIONALES

Si quieres mejorar más:

1. **Agregar validación de dominio:**
   ```javascript
   // Evitar emails de prueba
   const prohibidoDomains = ['test.com', 'temp.com']
   ```

2. **Verificación de email por OTP:**
   - Enviar código de verificación al email
   - Usuario debe confirmar antes de publicar

3. **Sugerencias de autocompletado:**
   - Cuando usuario tipea email, mostrar sugerencias

4. **Sincronización con perfil de empresa:**
   - Usar email del perfil si disponible

---

**Status:** ✅ COMPLETADO Y PROBADO
**Commit:** f45632d
**Fecha:** 2025-11-25
