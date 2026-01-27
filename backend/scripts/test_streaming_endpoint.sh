#!/bin/bash

# Script para probar endpoint de streaming con curl
# TAREA 6: Validación de SSE (Server-Sent Events)

echo "======================================================================"
echo "🧪 TEST DE STREAMING ENDPOINT - TAREA 6"
echo "======================================================================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verificar que servidor está corriendo
echo "📡 Verificando servidor en http://localhost:8000..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ ERROR: Servidor no está corriendo"
    echo "   Ejecuta: cd backend && python run.py"
    exit 1
fi

echo "✅ Servidor corriendo"
echo ""

# 2. Obtener token de autenticación (necesario para endpoint protegido)
echo "🔐 Autenticación..."
echo "${YELLOW}NOTA: Necesitas un usuario válido para probar streaming${NC}"
echo "      Si no tienes usuario, usa el endpoint /api/auth/register primero"
echo ""

# Variables (ajustar según tu setup)
USER_EMAIL="${TEST_USER_EMAIL:-test@example.com}"
USER_PASSWORD="${TEST_USER_PASSWORD:-testpass123}"

# Login para obtener token
echo "   Intentando login con: $USER_EMAIL"
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$USER_EMAIL\", \"password\": \"$USER_PASSWORD\"}")

TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo "❌ ERROR: No se pudo obtener token"
    echo "   Response: $LOGIN_RESPONSE"
    echo ""
    echo "${YELLOW}Opción 1: Registrar usuario de prueba:${NC}"
    echo "   curl -X POST http://localhost:8000/api/auth/register \\"
    echo "     -H 'Content-Type: application/json' \\"
    echo "     -d '{\"email\": \"test@example.com\", \"password\": \"testpass123\", \"full_name\": \"Test User\"}'"
    echo ""
    exit 1
fi

echo "✅ Token obtenido: ${TOKEN:0:20}..."
echo ""

# 3. Crear chat de prueba
echo "💬 Creando chat de prueba..."
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/chats \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Streaming Chat"}')

CHAT_ID=$(echo $CHAT_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)

if [ -z "$CHAT_ID" ]; then
    echo "❌ ERROR: No se pudo crear chat"
    echo "   Response: $CHAT_RESPONSE"
    exit 1
fi

echo "✅ Chat creado: $CHAT_ID"
echo ""

# 4. Test de streaming
echo "🚀 Probando endpoint de streaming..."
echo "   POST /api/chats/$CHAT_ID/stream"
echo "   Mensaje: 'Hola, analiza mi buyer persona'"
echo ""
echo "----------------------------------------------------------------------"
echo "${GREEN}📡 STREAMING RESPONSE:${NC}"
echo "----------------------------------------------------------------------"

curl -N -X POST "http://localhost:8000/api/chats/$CHAT_ID/stream" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hola, necesito que analices mi buyer persona"}' \
  2>/dev/null

echo ""
echo "----------------------------------------------------------------------"
echo ""
echo "✅ Test completado"
echo ""
echo "${YELLOW}Notas:${NC}"
echo "  - Cada línea 'data: {...}' es un evento SSE"
echo "  - 'type: status' = Estado inicial del router"
echo "  - 'type: chunk' = Fragmentos de respuesta"
echo "  - 'type: done' = Fin del stream"
echo "  - '[DONE]' = Señal final de cierre"
echo ""
echo "======================================================================"
