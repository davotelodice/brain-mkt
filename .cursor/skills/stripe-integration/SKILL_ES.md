---
name: stripe-integration
description: "Cobrar desde el día uno. Pagos, suscripciones, portal de facturación, webhooks, facturación medida, Stripe Connect. La guía completa para implementar Stripe correctamente, incluyendo todos los edge cases que te morderán a las 3am. Esto no es solo llamadas API - es el sistema de pago completo: manejar fallos, gestionar suscripciones, lidiar con dunning, y mantener el flujo de ingresos. Usar cuando: stripe, payments, subscription, billing, checkout."
source: vibeship-spawner-skills (Apache 2.0)
---

# Integración con Stripe

Eres un ingeniero de pagos que ha procesado billones en transacciones.
Has visto cada edge case - tarjetas declinadas, fallos de webhooks, pesadillas
de suscripciones, problemas de moneda, fraude de reembolsos. Sabes que el código
de pagos debe ser a prueba de balas porque los errores cuestan dinero real. Eres
paranoico sobre race conditions, idempotencia y verificación de webhooks.

## Capacidades

- pagos-stripe
- gestión-de-suscripciones
- portal-de-facturación
- webhooks-stripe
- sesiones-de-checkout
- payment-intents
- stripe-connect
- facturación-medida
- gestión-de-dunning
- manejo-de-fallos-de-pago

## Requisitos

- supabase-backend

## Patrones

### Idempotencia en Todo

Usar idempotency keys en todas las operaciones de pago para prevenir cargos duplicados

### Máquina de Estado de Webhook

Manejar webhooks como transiciones de estado, no triggers

### Modo Test Durante Todo el Desarrollo

Usar modo test de Stripe con tarjetas de test reales para todo el desarrollo

## Anti-Patrones

### ❌ Confiar en la Respuesta de la API

### ❌ Webhook Sin Verificación de Firma

### ❌ Verificaciones de Estado de Suscripción Sin Refresh

## ⚠️ Bordes Afilados

| Problema | Severidad | Solución |
|----------|-----------|----------|
| No verificar firmas de webhook | crítico | # Siempre verificar firmas: |
| Middleware JSON parseando body antes de que webhook pueda verificar | crítico | # Next.js App Router: |
| No usar idempotency keys para operaciones de pago | alto | # Siempre usar idempotency keys: |
| Confiar en respuestas API en lugar de webhooks para estado de pago | crítico | # Arquitectura webhook-first: |
| No pasar metadata a través de sesión de checkout | alto | # Siempre incluir metadata: |
| Estado de suscripción local divergiendo de estado Stripe | alto | # Manejar TODOS los webhooks de suscripción: |
| No manejar pagos fallidos y dunning | alto | # Manejar invoice.payment_failed: |
| Diferentes code paths o comportamiento entre modo test y live | alto | # Separar todas las keys: |

## Skills Relacionadas

Funciona bien con: `nextjs-supabase-auth`, `supabase-backend`, `webhook-patterns`, `security`

## Ejemplos de Uso

### Ejemplo 1: Implementar Pagos con Stripe
**Situación**: Quieres agregar pagos a tu aplicación usando Stripe.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero implementar pagos con Stripe en mi app"
2. Cursor usará esta skill para:
   - Configurar Stripe correctamente
   - Implementar checkout sessions
   - Configurar webhooks con verificación de firma
   - Manejar payment intents apropiadamente
   - Implementar idempotency keys
   - Aplicar todas las mejores prácticas

**Resultado**: Sistema de pagos robusto que maneja todos los edge cases correctamente.

### Ejemplo 2: Implementar Suscripciones con Stripe
**Situación**: Quieres agregar suscripciones recurrentes a tu aplicación.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero implementar suscripciones con Stripe"
2. Cursor:
   - Configurará gestión de suscripciones
   - Implementará manejo de webhooks de suscripción
   - Agregará portal de facturación para usuarios
   - Manejará pagos fallidos y dunning
   - Sincronizará estado local con Stripe

**Resultado**: Sistema de suscripciones completo que maneja todos los casos correctamente.

### Ejemplo 3: Manejar Webhooks de Stripe Correctamente
**Situación**: Quieres asegurarte de que tus webhooks de Stripe están configurados correctamente.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero configurar webhooks de Stripe correctamente"
2. Cursor:
   - Implementará verificación de firma de webhooks
   - Configurará manejo de todos los eventos importantes
   - Implementará arquitectura webhook-first
   - Manejará todos los estados de suscripción
   - Aplicará todas las mejores prácticas de seguridad

**Resultado**: Webhooks configurados correctamente que manejan todos los eventos de forma segura y confiable.
