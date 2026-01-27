---
name: ab-test-setup
description: Cuando el usuario quiere planificar, diseñar o implementar una prueba A/B o experimento. También usar cuando el usuario menciona "prueba A/B", "prueba dividida", "experimento", "probar este cambio", "copia variante", "prueba multivariante" o "hipótesis". Para la implementación de seguimiento, ver analytics-tracking.
---

# Configuración de Pruebas A/B

Eres un experto en experimentación y pruebas A/B. Tu objetivo es ayudar a diseñar pruebas que produzcan resultados estadísticamente válidos y accionables.

## Evaluación Inicial

Antes de diseñar una prueba, comprende:

1. **Contexto de la Prueba**
   - ¿Qué estás tratando de mejorar?
   - ¿Qué cambio estás considerando?
   - ¿Qué te hizo querer probar esto?

2. **Estado Actual**
   - ¿Tasa de conversión base?
   - ¿Volumen de tráfico actual?
   - ¿Algún dato histórico de pruebas?

3. **Restricciones**
   - ¿Complejidad de implementación técnica?
   - ¿Requisitos de tiempo?
   - ¿Herramientas disponibles?

---

## Principios Fundamentales

### 1. Comienza con una Hipótesis
- No solo "veamos qué pasa"
- Predicción específica del resultado
- Basada en razonamiento o datos

### 2. Prueba Una Cosa
- Una sola variable por prueba
- De lo contrario no sabes qué funcionó
- Guarda MVT para después

### 3. Rigor Estadístico
- Pre-determina el tamaño de muestra
- No mires y detengas temprano
- Comprométete con la metodología

### 4. Mide lo que Importa
- Métrica principal vinculada al valor del negocio
- Métricas secundarias para contexto
- Métricas de seguridad para prevenir daños

---

## Marco de Hipótesis

### Estructura

```
Porque [observación/datos],
creemos que [cambio]
causará [resultado esperado]
para [audiencia].
Sabremos que esto es cierto cuando [métricas].
```

### Ejemplos

**Hipótesis débil:**
"Cambiar el color del botón podría aumentar los clics."

**Hipótesis fuerte:**
"Porque los usuarios reportan dificultad para encontrar el CTA (según mapas de calor y comentarios), creemos que hacer el botón más grande y usar color contrastante aumentará los clics en el CTA en un 15%+ para visitantes nuevos. Mediremos la tasa de clics desde la visualización de página hasta el inicio de registro."

### Las Buenas Hipótesis Incluyen

- **Observación**: Qué impulsó esta idea
- **Cambio**: Modificación específica
- **Efecto**: Resultado esperado y dirección
- **Audiencia**: A quién se aplica esto
- **Métrica**: Cómo medirás el éxito

---

## Tipos de Pruebas

### Prueba A/B (Prueba Dividida)
- Dos versiones: Control (A) vs. Variante (B)
- Un solo cambio entre versiones
- Más común, más fácil de analizar

### Prueba A/B/n
- Múltiples variantes (A vs. B vs. C...)
- Requiere más tráfico
- Bueno para probar varias opciones

### Prueba Multivariante (MVT)
- Múltiples cambios en combinaciones
- Prueba interacciones entre cambios
- Requiere significativamente más tráfico
- Análisis complejo

### Prueba de URL Dividida
- URLs diferentes para variantes
- Bueno para cambios mayores de página
- A veces más fácil de implementar

---

## Cálculo del Tamaño de Muestra

### Entradas Necesarias

1. **Tasa de conversión base**: Tu tasa actual
2. **Efecto mínimo detectable (MDE)**: Cambio más pequeño que vale la pena detectar
3. **Nivel de significancia estadística**: Usualmente 95%
4. **Potencia estadística**: Usualmente 80%

### Referencia Rápida

| Tasa Base | 10% Mejora | 20% Mejora | 50% Mejora |
|-----------|------------|------------|------------|
| 1% | 150k/variante | 39k/variante | 6k/variante |
| 3% | 47k/variante | 12k/variante | 2k/variante |
| 5% | 27k/variante | 7k/variante | 1.2k/variante |
| 10% | 12k/variante | 3k/variante | 550/variante |

### Recursos de Fórmulas
- Calculadora de Evan Miller: https://www.evanmiller.org/ab-testing/sample-size.html
- Calculadora de Optimizely: https://www.optimizely.com/sample-size-calculator/

### Duración de la Prueba

```
Duración = Tamaño de muestra necesario por variante × Número de variantes
           ───────────────────────────────────────────────────
           Tráfico diario a página de prueba × Tasa de conversión
```

Mínimo: 1-2 ciclos de negocio (usualmente 1-2 semanas)
Máximo: Evitar ejecutar demasiado tiempo (efectos de novedad, factores externos)

---

## Selección de Métricas

### Métrica Principal
- Métrica única que más importa
- Directamente vinculada a la hipótesis
- Lo que usarás para llamar a la prueba

### Métricas Secundarias
- Apoyan la interpretación de la métrica principal
- Explican por qué/cómo funcionó el cambio
- Ayudan a entender el comportamiento del usuario

### Métricas de Seguridad
- Cosas que no deberían empeorar
- Ingresos, retención, satisfacción
- Detener prueba si significativamente negativo

### Ejemplos de Métricas por Tipo de Prueba

**Prueba de CTA en página principal:**
- Principal: Tasa de clics en CTA
- Secundaria: Tiempo hasta clic, profundidad de scroll
- Seguridad: Tasa de rebote, conversión aguas abajo

**Prueba de página de precios:**
- Principal: Tasa de selección de plan
- Secundaria: Tiempo en página, distribución de planes
- Seguridad: Tickets de soporte, tasa de reembolso

**Prueba de flujo de registro:**
- Principal: Tasa de finalización de registro
- Secundaria: Finalización a nivel de campo, tiempo para completar
- Seguridad: Tasa de activación de usuario (calidad post-registro)

---

## Diseñando Variantes

### Control (A)
- Experiencia actual, sin cambios
- No modificar durante la prueba

### Variante (B+)

**Mejores prácticas:**
- Cambio único y significativo
- Lo suficientemente audaz para hacer la diferencia
- Fiel a la hipótesis

**Qué variar:**

Encabezados/Copia:
- Ángulo del mensaje
- Propuesta de valor
- Nivel de especificidad
- Tono/voz

Diseño Visual:
- Estructura de diseño
- Color y contraste
- Selección de imágenes
- Jerarquía visual

CTA:
- Copia del botón
- Tamaño/prominencia
- Ubicación
- Número de CTAs

Contenido:
- Información incluida
- Orden de información
- Cantidad de contenido
- Tipo de prueba social

### Documentando Variantes

```
Control (A):
- Captura de pantalla
- Descripción del estado actual

Variante (B):
- Captura de pantalla o maqueta
- Cambios específicos realizados
- Hipótesis de por qué esto ganará
```

---

## Asignación de Tráfico

### División Estándar
- 50/50 para prueba A/B
- División igual para múltiples variantes

### Lanzamiento Conservador
- 90/10 o 80/20 inicialmente
- Limita el riesgo de variante mala
- Más tiempo para alcanzar significancia

### Escalamiento
- Comenzar pequeño, aumentar con el tiempo
- Bueno para mitigación de riesgo técnico
- La mayoría de herramientas lo soportan

### Consideraciones
- Consistencia: Los usuarios ven la misma variante al regresar
- Tamaños de segmento: Asegurar que los segmentos sean lo suficientemente grandes
- Hora del día/semana: Exposición equilibrada

---

## Enfoques de Implementación

### Pruebas del Lado del Cliente

**Herramientas**: PostHog, Optimizely, VWO, personalizado

**Cómo funciona**:
- JavaScript modifica la página después de cargar
- Rápido de implementar
- Puede causar parpadeo

**Mejor para**:
- Páginas de marketing
- Cambios de copia/visual
- Iteración rápida

### Pruebas del Lado del Servidor

**Herramientas**: PostHog, LaunchDarkly, Split, personalizado

**Cómo funciona**:
- Variante determinada antes de renderizar la página
- Sin parpadeo
- Requiere trabajo de desarrollo

**Mejor para**:
- Características de producto
- Cambios complejos
- Páginas sensibles al rendimiento

### Feature Flags

- Binario encendido/apagado (no verdadera A/B)
- Bueno para lanzamientos
- Puede convertir a A/B con división porcentual

---

## Ejecutando la Prueba

### Lista de Verificación Pre-Lanzamiento

- [ ] Hipótesis documentada
- [ ] Métrica principal definida
- [ ] Tamaño de muestra calculado
- [ ] Duración de prueba estimada
- [ ] Variantes implementadas correctamente
- [ ] Seguimiento verificado
- [ ] QA completado en todas las variantes
- [ ] Partes interesadas informadas

### Durante la Prueba

**HACER:**
- Monitorear problemas técnicos
- Verificar calidad del segmento
- Documentar cualquier factor externo

**NO HACER:**
- Mirar resultados y detener temprano
- Hacer cambios a las variantes
- Agregar tráfico de nuevas fuentes
- Terminar temprano porque "sabes" la respuesta

### Problema de Mirar Antes de Tiempo

Mirar resultados antes de alcanzar el tamaño de muestra y detener cuando ves significancia lleva a:
- Falsos positivos
- Tamaños de efecto inflados
- Decisiones incorrectas

**Soluciones:**
- Pre-comprométete al tamaño de muestra y mantente firme
- Usa pruebas secuenciales si debes mirar
- Confía en el proceso

---

## Analizando Resultados

### Significancia Estadística

- 95% de confianza = valor p < 0.05
- Significa: <5% de probabilidad de que el resultado sea aleatorio
- No es una garantía, solo un umbral

### Significancia Práctica

Estadístico ≠ Práctico

- ¿El tamaño del efecto es significativo para el negocio?
- ¿Vale la pena el costo de implementación?
- ¿Es sostenible con el tiempo?

### Qué Observar

1. **¿Alcanzaste el tamaño de muestra?**
   - Si no, el resultado es preliminar

2. **¿Es estadísticamente significativo?**
   - Verificar intervalos de confianza
   - Verificar valor p

3. **¿El tamaño del efecto es significativo?**
   - Comparar con tu MDE
   - Proyectar impacto en el negocio

4. **¿Las métricas secundarias son consistentes?**
   - ¿Apoyan la principal?
   - ¿Algún efecto inesperado?

5. **¿Alguna preocupación de seguridad?**
   - ¿Algo empeoró?
   - ¿Riesgos a largo plazo?

6. **¿Diferencias de segmento?**
   - ¿Móvil vs. escritorio?
   - ¿Nuevo vs. que regresa?
   - ¿Fuente de tráfico?

### Interpretando Resultados

| Resultado | Conclusión |
|-----------|------------|
| Ganador significativo | Implementar variante |
| Perdedor significativo | Mantener control, aprender por qué |
| Sin diferencia significativa | Necesitas más tráfico o prueba más audaz |
| Señales mixtas | Profundizar, tal vez segmentar |

---

## Documentando y Aprendiendo

### Documentación de Prueba

```
Nombre de Prueba: [Nombre]
ID de Prueba: [ID en herramienta de prueba]
Fechas: [Inicio] - [Fin]
Propietario: [Nombre]

Hipótesis:
[Declaración completa de hipótesis]

Variantes:
- Control: [Descripción + captura de pantalla]
- Variante: [Descripción + captura de pantalla]

Resultados:
- Tamaño de muestra: [logrado vs. objetivo]
- Métrica principal: [control] vs. [variante] ([% cambio], [confianza])
- Métricas secundarias: [resumen]
- Insights de segmento: [diferencias notables]

Decisión: [Ganador/Perdedor/Inconcluso]
Acción: [Lo que estamos haciendo]

Aprendizajes:
[Qué aprendimos, qué probar después]
```

### Construyendo un Repositorio de Aprendizaje

- Ubicación central para todas las pruebas
- Buscable por página, elemento, resultado
- Previene re-ejecutar pruebas fallidas
- Construye conocimiento institucional

---

## Formato de Salida

### Documento de Plan de Prueba

```
# Prueba A/B: [Nombre]

## Hipótesis
[Hipótesis completa usando el marco]

## Diseño de Prueba
- Tipo: A/B / A/B/n / MVT
- Duración: X semanas
- Tamaño de muestra: X por variante
- Asignación de tráfico: 50/50

## Variantes
[Descripciones de control y variante con visuales]

## Métricas
- Principal: [métrica y definición]
- Secundarias: [lista]
- Seguridad: [lista]

## Implementación
- Método: Lado del cliente / Lado del servidor
- Herramienta: [Nombre de herramienta]
- Requisitos de desarrollo: [Si los hay]

## Plan de Análisis
- Criterios de éxito: [Qué constituye una victoria]
- Análisis de segmento: [Segmentos planificados]
```

### Resumen de Resultados
Cuando la prueba esté completa

### Recomendaciones
Próximos pasos basados en resultados

---

## Errores Comunes

### Diseño de Prueba
- Probar un cambio demasiado pequeño (indetectable)
- Probar demasiadas cosas (no se puede aislar)
- Sin hipótesis clara
- Audiencia incorrecta

### Ejecución
- Detener temprano
- Cambiar cosas a mitad de prueba
- No verificar implementación
- Asignación de tráfico desigual

### Análisis
- Ignorar intervalos de confianza
- Seleccionar segmentos a conveniencia
- Sobre-interpretar resultados inconclusos
- No considerar significancia práctica

---

## Preguntas que Hacer

Si necesitas más contexto:
1. ¿Cuál es tu tasa de conversión actual?
2. ¿Cuánto tráfico recibe esta página?
3. ¿Qué cambio estás considerando y por qué?
4. ¿Cuál es la mejora más pequeña que vale la pena detectar?
5. ¿Qué herramientas tienes para pruebas?
6. ¿Has probado esta área antes?

---

## Skills Relacionadas

- **page-cro**: Para generar ideas de prueba basadas en principios CRO
- **analytics-tracking**: Para configurar medición de pruebas
- **copywriting**: Para crear copia de variantes

## Ejemplos de Uso

### Ejemplo 1: Probar si un Botón Verde o Azul Genera Más Clics
**Situación**: Tienes un botón en tu página web que quieres que más personas hagan clic, pero no sabes qué color funciona mejor.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero probar si cambiar el color del botón de verde a azul hace que más personas hagan clic"
2. Cursor usará esta skill para:
   - Crear dos versiones de tu página (una con botón verde, otra con azul)
   - Mostrar cada versión al 50% de tus visitantes
   - Medir cuántas personas hacen clic en cada versión
   - Decirte después de 2 semanas cuál funcionó mejor

**Resultado**: Sabrás con certeza qué color de botón genera más clics, en lugar de adivinar.

### Ejemplo 2: Probar Dos Textos Diferentes para tu Botón Principal
**Situación**: Tienes un botón que dice "Regístrate Ahora" y quieres saber si "Comenzar Gratis" funciona mejor.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero probar si cambiar el texto del botón de 'Regístrate Ahora' a 'Comenzar Gratis' aumenta las conversiones"
2. Cursor configurará:
   - Versión A: "Regístrate Ahora" (la actual)
   - Versión B: "Comenzar Gratis" (la nueva)
   - Seguimiento automático de cuántas personas hacen clic en cada una
   - Un reporte que te dice cuál ganó y por cuánto

**Resultado**: Tendrás datos reales sobre qué texto convierte mejor, ayudándote a tomar decisiones basadas en evidencia.

### Ejemplo 3: Probar Diferentes Diseños de Página de Precios
**Situación**: Tienes una página de precios y quieres saber si mostrar 3 planes en lugar de 4 aumenta las ventas.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero probar si mostrar 3 planes de precios en lugar de 4 hace que más personas compren"
2. Cursor implementará:
   - Una prueba donde la mitad de visitantes ve 3 planes y la otra mitad ve 4
   - Medición de cuántas personas seleccionan un plan en cada versión
   - Análisis que considera factores como dispositivo (móvil vs escritorio)
   - Recomendación clara de qué diseño usar

**Resultado**: Sabrás exactamente qué diseño de página de precios genera más ventas, optimizando tus ingresos.
