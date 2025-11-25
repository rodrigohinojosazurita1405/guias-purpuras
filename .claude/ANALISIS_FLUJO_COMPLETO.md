# 📊 ANÁLISIS DETALLADO DE TODOS LOS PASOS - WIZARD DE PUBLICACIÓN DE EMPLEOS

## 🎯 RESUMEN EJECUTIVO

**Estado Actual:** 5 pasos (0-4) con solapamiento de responsabilidades
**Problema Principal:** Información de contacto y aplicación está fragmentada

---

## 🔍 ANÁLISIS DETALLADO POR PASO

### **PASO 0: JobPublishStart** ✅ BIEN ESTRUCTURADO
**Archivo:** `frontend/src/components/Publish/JobPublishStart.vue`
**Responsabilidad:** Primera selección rápida

**¿Qué Contiene?**
- 5 opciones de tipo de empleo (Tiempo Completo, Medio Tiempo, Remoto, Freelance, Pasantías)
- Selector de Ciudad (9 ciudades de Bolivia)
- Botones: Cancelar / Continuar

**Validaciones:**
- ✅ Tipo de empleo requerido
- ✅ Ciudad requerida

**Flujo:**
- Usuario → Selecciona tipo + ciudad → Click "Continuar" → Va a Paso 1 (PlanStep)

**Análisis:**
- **Pros:** Simple, rápido, sin saturación
- **Contras:** No captura Municipio (lo hace en Paso 2)
- **Mejora Propuesta:** Agregar Municipio aquí sería redundante ya que lo tiene Paso 2

---

### **PASO 1: PlanStep** ✅ BIEN ESTRUCTURADO
**Archivo:** `frontend/src/components/Publish/PlanStep.vue`
**Responsabilidad:** Selección de plan de pago

**¿Qué Contiene?**
1. **Plan Escencial** (35 Bs., 15 días)
   - Visibilidad Normal
   - 1 Aviso de Trabajo
   - 1 Post en Redes

2. **Plan Púrpura** (79 Bs., 30 días) - RECOMENDADO
   - Destacado (10 días)
   - 1 Aviso de Trabajo
   - 4 Posts en Redes
   - Etiqueta Urgente
   - 1 Cambio Incluido

3. **Plan Impulso Pro** (169 Bs., indefinido)
   - Todas las features de Púrpura +
   - Mayor alcance y visibilidad

**Validaciones:**
- ✅ Plan requerido (con notificación toast si no selecciona)

**Flujo:**
- Usuario → Selecciona plan → Click "Siguiente" → Va a Paso 2 (InformationStepJob)

**Análisis:**
- **Pros:** Claro, validado, bien separado
- **Contras:** Ninguno observado
- **Mejora Propuesta:** Podría ir DESPUÉS del Paso 2 (ver propuesta final)

---

### **PASO 2: InformationStepJob** ⚠️ SATURADO Y DESORDENADO
**Archivo:** `frontend/src/views/FormCreate/InformationStepJob.vue`
**Responsabilidad:** Capturar TODA la información de la oferta laboral

**¿Qué Contiene? (4 Acordeones)**

#### **Acordeón 1: Información Básica del Puesto** ✅
- Título del Puesto *
- Nombre de la Empresa + Switch Anónimo
- Descripción del Trabajo *

#### **Sección 2: Ubicación y Tipo de Puesto** ✅
- Categoría/Área *
- Ciudad *
- Provincia / Municipio (opcional)
- Tipo de Contrato *
- Fecha de Vencimiento *

#### **Sección 3: Requisitos y Competencias** ✅
- Requisitos y Responsabilidades *
- Formación Requerida
- Experiencia Necesaria (select dropdown)
- Idiomas Requeridos (textarea)
- Habilidades Técnicas (textarea)
- Habilidades Blandas (textarea) - NUEVO

#### **Acordeón 2: Compensación y Beneficios** ✅
- Tipo de Salario (rango/fijo/negociable/oculto)
- Salario Mínimo/Máximo
- Beneficios

#### **Acordeón 3: Número de Vacantes** ✅
- Selector +-
- Visualización gráfica de vacantes

#### **❌ Acordeón 4: Información de Contacto (PROBLEMA!)**
- Email de Contacto *
- WhatsApp *
- Sitio Web (opcional)
- **Instrucciones Especiales para Postular (opcional)**

**Validaciones:**
- ✅ Múltiples validaciones con rules de Vuestic
- ✅ Método validate() que se llama desde padre

**Análisis:**
- **Pros:**
  - Datos de oferta bien organizados en 3 secciones lógicas
  - Validaciones completas

- **Contras:**
  - ❌ Acordeón 4 NO DEBERÍA ESTAR AQUÍ (datos de contacto)
  - ❌ Las instrucciones de postulación tampoco
  - ❌ Estos datos pertenecen al Paso 3 (ApplicationConfigStep)
  - Acordeón está saturado (6 campos de contacto/instrucciones)

**Mejora Propuesta:**
- Eliminar Acordeón 4 completamente
- Mover datos de contacto al Paso 3

---

### **PASO 3: ApplicationConfigStep** ⚠️ INCOMPLETO
**Archivo:** `frontend/src/components/Publish/ApplicationConfigStep.vue`
**Responsabilidad:** Configurar CÓMO se reciben las aplicaciones

**¿Qué Contiene Actualmente?**

1. **Tipo de Aplicación** (3 opciones)
   - Interna (formulario en Guías Púrpuras)
   - Externa (tu sitio/plataforma)
   - Ambas

2. **URL Externa** (si es Externa o Ambas)
   - Campo URL con validación

3. **Preguntas de Filtrado** (solo para aplicación Interna)
   - Máximo 5 preguntas
   - Tipos: Texto corto, Sí/No, Opción múltiple
   - Campos: Texto, Tipo, ¿Obligatoria?

**Validaciones:**
- ✅ URL validada
- ✅ Preguntas de 0-5 máximo

**Análisis:**
- **Pros:**
  - Buena estructura modular
  - Preguntas de filtrado bien implementadas

- **Contras:**
  - ❌ **FALTA toda la información de CONTACTO** (email, whatsapp, website, horarios)
  - ❌ **FALTA instrucciones de postulación** para candidatos
  - ❌ **FALTA dónde/cómo enviar documentos**
  - ❌ No está integrado con datos de Paso 2

**Lo que DEBERÍA tener:**
- Datos de contacto (email, whatsapp, teléfono, horarios)
- Instrucciones de postulación
- Dónde enviar CV (email, form, link)
- Documentos requeridos
- Info adicional para candidatos

---

### **PASO 4: SummaryCard** ✅ BIEN ESTRUCTURADO
**Archivo:** `frontend/src/components/Cards/SummaryCard.vue`
**Responsabilidad:** Resumen final antes de publicar

**¿Qué Contiene?**
- Selección Inicial (Tipo de empleo, Ubicación)
- Plan seleccionado
- Info de la oferta
- Botones: Atrás / Confirmar y Pagar

**Validaciones:**
- ✅ Revisa autenticación
- ✅ Revisa token JWT
- ✅ Hace POST a backend

**Análisis:**
- **Pros:**
  - Resumen visual claro
  - Confirmación antes de pagar

- **Contras:**
  - No muestra información de contacto/aplicación (porque está parcialmente en Paso 2)
  - Debería mostrar configuración de aplicaciones

---

## 🔴 PROBLEMAS IDENTIFICADOS

### **1. Acordeón 4 en Paso 2 - FUERA DE LUGAR**
```
❌ Información de Contacto está en InformationStepJob (Paso 2)
✅ Debería estar en ApplicationConfigStep (Paso 3)

Afecta:
- Usuario confundido: "¿Por qué mi email está en 'Información del Trabajo'?"
- Saturación del Paso 2 (4 acordeones → 6 con contacto)
- Responsabilidad poco clara
```

### **2. ApplicationConfigStep Incompleto**
```
❌ Solo tiene tipo de aplicación + preguntas de filtrado
✅ Debería tener TODA la configuración de cómo aplicar

Falta:
- Email, WhatsApp, teléfono, horarios de contacto
- Instrucciones para postulantes
- Dónde enviar CV/documentos
- Documentos requeridos
- Info adicional
```

### **3. Falta Paso de Revisión Real**
```
❌ SummaryCard existe pero no es visible/destacado
❌ No muestra configuración de aplicaciones
✅ Debería ser un paso bien definido después de todo lo demás
```

### **4. Orden de Pasos Subóptimo**
```
Actual:
0. Selección → 1. Plan → 2. Info → 3. Aplicación → 4. Resumen

Propuesto:
0. Selección → 1. Info → 2. Aplicación → 3. Plan → 4. Resumen

Razón: Financiero va justo antes de la confirmación final
```

---

## 🎨 FLUJO PROPUESTO FINAL

```
┌─────────────────────────────────────────────┐
│ PASO 0: JobPublishStart                     │
├─────────────────────────────────────────────┤
│ → Tipo de Empleo (5 opciones)               │
│ → Ubicación (Ciudad)                        │
│ ✓ FIN: Categoría inicial lista              │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ PASO 1: InformationStepJob (REORGANIZADO)   │
├─────────────────────────────────────────────┤
│ Acordeón 1: Info Básica                     │
│ Acordeón 2: Ubicación y Requisitos          │
│ Acordeón 3: Compensación                    │
│ Acordeón 4: Vacantes                        │
│ ✗ ELIMINAR: Acordeón Contacto              │
│ ✓ FIN: Oferta laboral completa              │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ PASO 2: ApplicationConfigStep (REDISEÑADO)  │
├─────────────────────────────────────────────┤
│ Sección 1: Tipo de Aplicación               │
│ Sección 2: Datos de Contacto (NUEVO)        │
│ Sección 3: URL Externa (si aplica)          │
│ Sección 4: Instrucciones de Postulación     │
│ Sección 5: Preguntas de Filtrado            │
│ ✓ FIN: Aplicación configurada               │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ PASO 3: PlanStep                            │
├─────────────────────────────────────────────┤
│ → Seleccionar Plan (Escencial, Púrpura,...)│
│ ✓ FIN: Plan y precio definidos              │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│ PASO 4: SummaryCard (REVISIÓN FINAL)        │
├─────────────────────────────────────────────┤
│ ✓ Resumen de Oferta                         │
│ ✓ Resumen de Aplicación                     │
│ ✓ Resumen de Plan (precio)                  │
│ ✓ FIN: Confirmar y Pagar                    │
└─────────────────────────────────────────────┘
```

---

## ✅ CAMBIOS TÉCNICOS NECESARIOS

### **Frontend**

1. **InformationStepJob.vue**
   - Eliminar Acordeón 4 (Información de Contacto) completamente
   - Mantener Acordeones 1-4 (Info Básica, Ubicación, Compensación, Vacantes)

2. **ApplicationConfigStep.vue**
   - Agregar Sección 2: Datos de Contacto
     - Email de Contacto *
     - WhatsApp *
     - Teléfono (opcional)
     - Horarios de Atención (opcional)
   - Agregar Sección 4: Instrucciones de Postulación
     - Instrucciones Especiales
     - Documentos Requeridos (lista)
     - Información Adicional

3. **PublishView.vue**
   - Cambiar orden de pasos:
     - Paso 0: JobPublishStart
     - Paso 1: InformationStepJob
     - Paso 2: ApplicationConfigStep
     - Paso 3: PlanStep
     - Paso 4: SummaryCard
   - Actualizar wizardSteps array

4. **SummaryCard.vue**
   - Agregar sección para resumen de Aplicación
   - Mostrar tipo de aplicación seleccionado
   - Mostrar datos de contacto configurados
   - Mostrar instrucciones de postulación

### **Backend**

Campos a agregar al modelo Job en `jobs/models.py`:
```python
# Configuración de Aplicación
applicationType = CharField(
    max_length=20,
    choices=[('internal', 'Interna'), ('external', 'Externa'), ('both', 'Ambas')],
    blank=True
)
externalApplicationUrl = URLField(blank=True)
applicationEmail = EmailField(blank=True)  # Para contacto
applicationPhone = CharField(max_length=20, blank=True)
applicationHours = CharField(max_length=100, blank=True)
applicationInstructions = TextField(blank=True)  # Instrucciones para postulantes
requiredDocuments = TextField(blank=True)  # JSON array de documentos
additionalApplicationInfo = TextField(blank=True)
```

---

## 📋 TABLA COMPARATIVA: ACTUAL vs PROPUESTO

| Aspecto | Actual | Propuesto | Mejora |
|---------|--------|-----------|--------|
| **Paso 2 Saturación** | 4 acordeones (6 con contacto) | 4 acordeones | ✅ Limpio |
| **Contacto en Paso** | Paso 2 (confuso) | Paso 2 (dedicado) | ✅ Claro |
| **Aplicación Config** | Incompleta en Paso 3 | Completa en Paso 2 | ✅ Integral |
| **Revisión Final** | SummaryCard genérico | SummaryCard enfocado | ✅ Mejor UX |
| **Orden Lógico** | 0→1→2→3→4 | 0→1→2→3→4 | ✅ Mismo |
| **Experiencia Usuario** | "Dónde va mi email?" | "Claro dónde va todo" | ✅ Intuitivo |

---

## 🎯 CONCLUSIÓN

La arquitectura actual tiene una **buena estructura base** pero sufre de:

1. **Responsabilidades mal distribuidas**
   - Contacto e Instrucciones en Paso 2 (Info de Oferta)

2. **ApplicationConfigStep incompleto**
   - Solo 30% de lo que debería ser

3. **Orden que podría ser más lógico**
   - Plan debería estar más cerca del pago final

**Recomendación:** Implementar la restructuración propuesta para una **UX más clara y arquitectura más mantenible**.

