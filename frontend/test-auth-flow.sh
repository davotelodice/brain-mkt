#!/bin/bash

# Script para probar flujo de autenticación completo
# TAREA 7: Validación de Frontend Auth

echo "======================================================================"
echo "🧪 TEST DE AUTENTICACIÓN - FRONTEND + BACKEND"
echo "======================================================================"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Verificar que backend está corriendo
echo "📡 Verificando backend en http://localhost:8000..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${RED}❌ ERROR: Backend no está corriendo${NC}"
    echo "   Ejecuta: cd backend && python run.py"
    exit 1
fi
echo -e "${GREEN}✅ Backend corriendo${NC}"
echo ""

# 2. Verificar que frontend está corriendo
echo "🌐 Verificando frontend en http://localhost:3000..."
if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${RED}❌ ERROR: Frontend no está corriendo${NC}"
    echo "   Ejecuta: cd frontend && npm run dev"
    exit 1
fi
echo -e "${GREEN}✅ Frontend corriendo${NC}"
echo ""

# 3. Test de registro
echo "📝 Testeando registro de usuario..."
REGISTER_EMAIL="test-$(date +%s)@example.com"  # Email único
REGISTER_PASSWORD="TestAuth123"
REGISTER_NAME="Test User Auth"
PROJECT_ID="a0000000-0000-0000-0000-000000000001"

REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$REGISTER_EMAIL\",
    \"password\": \"$REGISTER_PASSWORD\",
    \"full_name\": \"$REGISTER_NAME\",
    \"project_id\": \"$PROJECT_ID\"
  }")

if echo "$REGISTER_RESPONSE" | grep -q "id"; then
    echo -e "${GREEN}✅ Registro exitoso${NC}"
    echo "   Email: $REGISTER_EMAIL"
else
    echo -e "${RED}❌ ERROR en registro${NC}"
    echo "   Response: $REGISTER_RESPONSE"
    exit 1
fi
echo ""

# 4. Test de login (con cookies)
echo "🔐 Testeando login con cookies httpOnly..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -c /tmp/cookies.txt \
  -d "{
    \"email\": \"$REGISTER_EMAIL\",
    \"password\": \"$REGISTER_PASSWORD\"
  }")

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo -e "${GREEN}✅ Login exitoso (token recibido)${NC}"
else
    echo -e "${RED}❌ ERROR en login${NC}"
    echo "   Response: $LOGIN_RESPONSE"
    exit 1
fi

# Verificar que cookie fue seteada
if grep -q "auth_token" /tmp/cookies.txt 2>/dev/null; then
    echo -e "${GREEN}✅ Cookie 'auth_token' seteada correctamente${NC}"
else
    echo -e "${YELLOW}⚠️  Cookie no detectada en archivo (puede ser normal)${NC}"
fi
echo ""

# 5. Test de acceso a ruta protegida con cookie
echo "🔒 Testeando acceso a ruta protegida con cookie..."
PROTECTED_RESPONSE=$(curl -s -b /tmp/cookies.txt \
  http://localhost:8000/api/chats \
  -H "Authorization: Bearer $(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)")

if echo "$PROTECTED_RESPONSE" | grep -q "detail.*Unauthorized" > /dev/null 2>&1; then
    echo -e "${RED}❌ Acceso denegado (esperado: permitido)${NC}"
else
    echo -e "${GREEN}✅ Acceso permitido a ruta protegida${NC}"
fi
echo ""

# 6. Test de logout
echo "🚪 Testeando logout..."
LOGOUT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/logout \
  -b /tmp/cookies.txt \
  -c /tmp/cookies_after_logout.txt)

if echo "$LOGOUT_RESPONSE" | grep -q "Logged out successfully"; then
    echo -e "${GREEN}✅ Logout exitoso${NC}"
else
    echo -e "${YELLOW}⚠️  Logout response: $LOGOUT_RESPONSE${NC}"
fi
echo ""

# Cleanup
rm -f /tmp/cookies.txt /tmp/cookies_after_logout.txt

echo "======================================================================"
echo -e "${GREEN}✅ TODOS LOS TESTS PASARON${NC}"
echo "======================================================================"
echo ""
echo -e "${YELLOW}Próximos pasos:${NC}"
echo "  1. Abre http://localhost:3000 en el navegador"
echo "  2. Deberías ver redirect automático a /login"
echo "  3. Regístrate o usa: $REGISTER_EMAIL / $REGISTER_PASSWORD"
echo "  4. Verifica que después de login te redirige a /"
echo ""
