# QA Plan 3: Validación de Técnicas Aplicadas

## Objetivo

Verificar que el agente realmente aplica técnicas del entrenamiento (transcripciones de Andrea Estratega) y las reporta correctamente en el campo `tecnicas_aplicadas` de cada idea generada.

## Métricas a Validar

- **`tecnicas_aplicadas_count`**: Total de técnicas reportadas en todas las ideas
- **Consistencia**: Las técnicas reportadas deben reflejarse en el contenido real (hook, estructura, CTA, etc.)
- **Especificidad**: Las técnicas deben ser concretas y extraídas del entrenamiento, no genéricas

## Pruebas Manuales Repetibles

### Prueba 1: Técnicas Obligatorias Específicas

**Prompt de prueba:**
```
Dame 5 ideas de contenido para TikTok. OBLIGATORIO: usa las técnicas "contraste", "metáfora_visual" y "CTA_específico" en cada idea.
```

**Validación:**
1. ✅ Verificar que `tecnicas_aplicadas_count` en Trace >= 15 (5 ideas × 3 técnicas mínimas)
2. ✅ Verificar que cada idea en el JSON tiene `tecnicas_aplicadas` como array
3. ✅ Verificar que cada idea contiene al menos: `"contraste"`, `"metáfora_visual"`, `"CTA_específico"` (case-insensitive)
4. ✅ **Validación de consistencia**: Revisar manualmente que:
   - El `hook` refleja "contraste" (ej: "Antes vs Después", "Problema vs Solución")
   - La `estructura` refleja "metáfora_visual" (ej: comparaciones visuales, analogías)
   - El `cta` refleja "CTA_específico" (ej: acción concreta, no genérico como "sígueme")

**Criterio de éxito:**
- ✅ Todas las ideas tienen `tecnicas_aplicadas` con las 3 técnicas solicitadas
- ✅ El contenido real refleja las técnicas (no solo las menciona)
- ✅ `tecnicas_aplicadas_count` >= 15

---

### Prueba 2: Técnicas del Entrenamiento (Sin Especificar)

**Prompt de prueba:**
```
Dame 5 ideas de contenido para Instagram Reels sobre [tema relevante al buyer persona].
```

**Validación:**
1. ✅ Verificar que `tecnicas_aplicadas_count` > 0 (al menos algunas técnicas reportadas)
2. ✅ Verificar que cada idea tiene `tecnicas_aplicadas` como array no vacío
3. ✅ Verificar que las técnicas reportadas son específicas (no genéricas como "marketing", "contenido")
4. ✅ **Validación de consistencia**: Revisar manualmente que las técnicas reportadas se reflejan en:
   - `hook`: si reporta "hook_emocional", el hook debe ser emocional
   - `estructura`: si reporta "storytelling", debe tener narrativa
   - `cta`: si reporta "CTA_específico", debe ser acción concreta

**Criterio de éxito:**
- ✅ Todas las ideas tienen `tecnicas_aplicadas` con al menos 1 técnica
- ✅ Las técnicas son específicas y relacionadas con el entrenamiento
- ✅ El contenido refleja las técnicas reportadas

---

### Prueba 3: Validación de Técnicas Únicas

**Prompt de prueba:**
```
Dame 10 ideas de contenido para TikTok sobre [tema].
```

**Validación:**
1. ✅ Verificar que `tecnicas_aplicadas_count` >= 10 (al menos 1 técnica por idea)
2. ✅ Extraer todas las técnicas únicas de todas las ideas
3. ✅ Verificar que hay variedad (no todas las ideas usan las mismas 2-3 técnicas)
4. ✅ Verificar que las técnicas son del dominio del entrenamiento (no inventadas)

**Criterio de éxito:**
- ✅ Al menos 5 técnicas únicas diferentes entre las 10 ideas
- ✅ Las técnicas son del dominio del marketing de contenido viral

---

### Prueba 4: Caso Edge - Técnicas No Encontradas

**Prompt de prueba:**
```
Dame 3 ideas usando las técnicas "técnica_inexistente_xyz" y "otra_falsa_abc".
```

**Validación:**
1. ✅ Verificar que el agente NO inventa técnicas que no existen
2. ✅ Verificar que el agente usa técnicas reales del entrenamiento (aunque no sean las solicitadas)
3. ✅ Verificar que `tecnicas_aplicadas` contiene técnicas válidas del entrenamiento

**Criterio de éxito:**
- ✅ El agente usa técnicas reales del entrenamiento, no inventa nombres
- ✅ Si no puede usar las técnicas solicitadas, usa alternativas válidas

---

## Checklist de Ejecución

Antes de ejecutar cada prueba:

- [ ] Verificar que `AGENT_TRACE=1` y `SSE_DEBUG=1` están activos en `.env`
- [ ] Verificar que el proyecto tiene buyer persona y customer journey configurados
- [ ] Verificar que hay transcripciones de entrenamiento en la base de datos (RAG)
- [ ] Abrir el panel "Ver trace" en el frontend

Durante la ejecución:

- [ ] Enviar el prompt de prueba
- [ ] Esperar respuesta completa
- [ ] Abrir el Trace panel y verificar `tecnicas_aplicadas_count`
- [ ] Verificar el JSON de respuesta en el chat
- [ ] Validar consistencia manual (contenido vs técnicas reportadas)

Después de cada prueba:

- [ ] Documentar resultados en esta tabla:

| Prueba | tecnicas_aplicadas_count | Ideas con técnicas | Consistencia | Notas |
|--------|-------------------------|-------------------|--------------|-------|
| 1      |                         |                   | ✅/❌        |       |
| 2      |                         |                   | ✅/❌        |       |
| 3      |                         |                   | ✅/❌        |       |
| 4      |                         |                   | ✅/❌        |       |

---

## Técnicas Esperadas del Entrenamiento

Basadas en las transcripciones de Andrea Estratega, las técnicas comunes incluyen:

- `contraste` / `contraste_visual`
- `metáfora_visual` / `analogía`
- `hook_emocional` / `hook_curiosidad`
- `CTA_específico` / `CTA_accionable`
- `storytelling` / `narrativa`
- `pregunta_retórica`
- `estadística_impactante`
- `testimonial` / `social_proof`
- `problema_solución`
- `antes_después`

**Nota:** Esta lista puede variar según el contenido real de las transcripciones. El agente debe reportar técnicas que realmente aparecen en el `training_summary`.

---

## Validación Automatizada (Futuro)

Para automatizar estas pruebas, se podría:

1. Crear un script de prueba que envíe los prompts y valide el JSON
2. Extraer `tecnicas_aplicadas` de cada idea y verificar:
   - Que existe y es un array
   - Que contiene strings no vacíos
   - Que las técnicas son del dominio esperado
3. Validar consistencia usando un LLM de validación (ej: "¿El hook refleja la técnica 'contraste'?")

**Estado:** Manual por ahora, automatización pendiente.

---

## Notas de Implementación

- El campo `tecnicas_aplicadas` es **obligatorio** en modo `ideas_json`
- Si falta, se añade un array vacío `[]` y se registra un warning en logs
- El conteo `tecnicas_aplicadas_count` suma todas las técnicas de todas las ideas
- Las técnicas se normalizan a lowercase para comparación
