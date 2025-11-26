#!/bin/bash

# Script de Testing - Sincronización Job Creation con Nueva Estructura

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0MTE2NDQ1LCJpYXQiOjE3NjQxMTI4NDUsImp0aSI6IjA2MjdkMDdhMzc1MzQ3OTY4YmNhMDI3NTU0YTkwMTVhIiwidXNlcl9pZCI6IjkifQ.NTKZ8CMzu1ZqMg3ZIZArsOcAPsQ8bLWsRYr_TvNeOFQ"
BASE_URL="http://localhost:8000/api"

echo "========================================="
echo "TESTING: Job Creation con Nueva Estructura"
echo "========================================="
echo ""

# 1. TEST: Crear un trabajo con TODOS los campos nuevos
echo "TEST 1: Crear trabajo con todos los campos (incluyendo softSkills, municipality, vacancies)"
echo ""

JOB_DATA='{
  "title": "Community Manager Senior",
  "companyName": "Startup Innovadora Bolivia",
  "companyAnonymous": false,
  "description": "Buscamos un profesional para gestionar comunidad en redes sociales",
  "jobCategory": "Marketing y Comunicación",
  "city": "La Paz",
  "municipality": "La Paz",
  "subcategory": "",
  "contractType": "Tiempo Completo",
  "expiryDate": "2025-12-31",
  "requirements": "Experiencia en gestión de redes sociales y comunidades online",
  "responsibilities": "Gestionar redes sociales, responder comentarios, crear contenido",
  "education": "Licenciatura en Comunicación o Marketing",
  "experience": "3+ años en gestión de redes sociales",
  "languages": "Español nativo, Inglés intermedio",
  "technicalSkills": "Herramientas: Meta Business Suite, Buffer, Hootsuite, Canva, Adobe Creative Suite",
  "softSkills": "Comunicación efectiva, empatía, creatividad, gestión de crisis, liderazgo colaborativo",
  "salaryType": "range",
  "salaryMin": 2500,
  "salaryMax": 4000,
  "benefits": "Bono anual, seguro de salud, flexibilidad horaria, capacitaciones",
  "vacancies": 2,
  "email": "careers@startupbolivia.com",
  "whatsapp": "+591 71234567",
  "website": "https://startupbolivia.com",
  "applicationInstructions": "Envía tu CV y portafolio de trabajos anteriores",
  "applicationType": "internal",
  "selectedPlan": "purpura",
  "screeningQuestions": []
}'

echo "Enviando datos de job..."
RESPONSE=$(curl -s -X POST "$BASE_URL/jobs/publish" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$JOB_DATA")

echo "RESPUESTA DEL SERVIDOR:"
echo "$RESPONSE" | python -m json.tool 2>/dev/null || echo "$RESPONSE"
echo ""

# Extraer ID del trabajo
JOB_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4 | head -1)

if [ -z "$JOB_ID" ]; then
  echo "❌ Error: No se pudo obtener el ID del trabajo"
  exit 1
fi

echo "✅ Job creado con ID: $JOB_ID"
echo ""

# 2. TEST: Recuperar el trabajo y verificar TODOS los campos
echo "TEST 2: Recuperar trabajo y verificar sincronización de TODOS los campos"
echo ""

GET_RESPONSE=$(curl -s -X GET "$BASE_URL/jobs/$JOB_ID" \
  -H "Authorization: Bearer $TOKEN")

echo "DATOS RECUPERADOS DEL SERVIDOR:"
echo "$GET_RESPONSE" | python -m json.tool 2>/dev/null || echo "$GET_RESPONSE"
echo ""

# 3. VERIFICACIÓN DE CAMPOS
echo "TEST 3: Verificación detallada de campos críticos"
echo ""

echo "Verificando campos de la nueva estructura..."
echo ""

# Verificar softSkills
if echo "$GET_RESPONSE" | grep -q '"softSkills"'; then
  echo "✅ softSkills: PRESENTE"
else
  echo "❌ softSkills: FALTA"
fi

# Verificar municipality
if echo "$GET_RESPONSE" | grep -q '"municipality"'; then
  echo "✅ municipality: PRESENTE"
else
  echo "❌ municipality: FALTA"
fi

# Verificar vacancies
if echo "$GET_RESPONSE" | grep -q '"vacancies"'; then
  echo "✅ vacancies: PRESENTE"
else
  echo "❌ vacancies: FALTA"
fi

# Verificar email
if echo "$GET_RESPONSE" | grep -q '"email"'; then
  echo "✅ email: PRESENTE"
else
  echo "❌ email: FALTA"
fi

# Verificar whatsapp
if echo "$GET_RESPONSE" | grep -q '"whatsapp"'; then
  echo "✅ whatsapp: PRESENTE"
else
  echo "❌ whatsapp: FALTA"
fi

# Verificar website
if echo "$GET_RESPONSE" | grep -q '"website"'; then
  echo "✅ website: PRESENTE"
else
  echo "❌ website: FALTA"
fi

# Verificar applicationInstructions
if echo "$GET_RESPONSE" | grep -q '"applicationInstructions"'; then
  echo "✅ applicationInstructions: PRESENTE"
else
  echo "❌ applicationInstructions: FALTA"
fi

# Verificar responsibilities
if echo "$GET_RESPONSE" | grep -q '"responsibilities"'; then
  echo "✅ responsibilities: PRESENTE"
else
  echo "❌ responsibilities: FALTA"
fi

echo ""
echo "========================================="
echo "TESTING COMPLETADO"
echo "========================================="
