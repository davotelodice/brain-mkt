---
name: skill-creator
description: Guía para crear skills efectivas. Esta skill debe usarse cuando los usuarios quieren crear una nueva skill (o actualizar una skill existente) que extienda las capacidades de Claude con conocimiento especializado, flujos de trabajo o integraciones de herramientas.
license: Términos completos en LICENSE.txt
---

# Creador de Skills

Esta skill proporciona guía para crear skills efectivas.

## Acerca de las Skills

Las skills son paquetes modulares y autocontenidos que extienden las capacidades de Claude proporcionando
conocimiento especializado, flujos de trabajo y herramientas. Piensa en ellas como "guías de incorporación" para dominios
o tareas específicos—transforman a Claude de un agente de propósito general en un agente especializado
equipado con conocimiento procedural que ningún modelo puede poseer completamente.

### Lo que Proporcionan las Skills

1. Flujos de trabajo especializados - Procedimientos de múltiples pasos para dominios específicos
2. Integraciones de herramientas - Instrucciones para trabajar con formatos de archivo o APIs específicos
3. Experiencia de dominio - Conocimiento específico de la empresa, esquemas, lógica de negocio
4. Recursos agrupados - Scripts, referencias y assets para tareas complejas y repetitivas

## Principios Fundamentales

### La Concisión es Clave

La ventana de contexto es un bien público. Las skills comparten la ventana de contexto con todo lo demás que Claude necesita: system prompt, historial de conversación, metadata de otras Skills y la solicitud real del usuario.

**Suposición por defecto: Claude ya es muy inteligente.** Solo agrega contexto que Claude no tiene ya. Desafía cada pieza de información: "¿Claude realmente necesita esta explicación?" y "¿Este párrafo justifica su costo en tokens?"

Prefiere ejemplos concisos sobre explicaciones verbosas.

### Establecer Grados Apropiados de Libertad

Coincidir el nivel de especificidad con la fragilidad y variabilidad de la tarea:

**Alta libertad (instrucciones basadas en texto)**: Usar cuando múltiples enfoques son válidos, las decisiones dependen del contexto o heurísticas guían el enfoque.

**Libertad media (pseudocódigo o scripts con parámetros)**: Usar cuando existe un patrón preferido, alguna variación es aceptable o la configuración afecta el comportamiento.

**Baja libertad (scripts específicos, pocos parámetros)**: Usar cuando las operaciones son frágiles y propensas a errores, la consistencia es crítica o debe seguirse una secuencia específica.

Piensa en Claude como explorando un camino: un puente estrecho con acantilados necesita barandillas específicas (baja libertad), mientras que un campo abierto permite muchas rutas (alta libertad).

### Anatomía de una Skill

Cada skill consiste en un archivo SKILL.md requerido y recursos agrupados opcionales:

```
skill-name/
├── SKILL.md (requerido)
│   ├── Metadata frontmatter YAML (requerido)
│   │   ├── name: (requerido)
│   │   └── description: (requerido)
│   └── Instrucciones Markdown (requerido)
└── Recursos Agrupados (opcional)
    ├── scripts/          - Código ejecutable (Python/Bash/etc.)
    ├── references/       - Documentación destinada a cargarse en contexto según se necesite
    └── assets/           - Archivos usados en salida (plantillas, iconos, fuentes, etc.)
```

#### SKILL.md (requerido)

Cada SKILL.md consiste en:

- **Frontmatter** (YAML): Contiene campos `name` y `description`. Estos son los únicos campos que Claude lee para determinar cuándo se usa la skill, por lo tanto es muy importante ser claro y completo al describir qué es la skill y cuándo debe usarse.
- **Cuerpo** (Markdown): Instrucciones y guía para usar la skill. Solo se carga DESPUÉS de que la skill se activa (si es que se activa).

#### Recursos Agrupados (opcional)

##### Scripts (`scripts/`)

Código ejecutable (Python/Bash/etc.) para tareas que requieren confiabilidad determinística o se reescriben repetidamente.

- **Cuándo incluir**: Cuando el mismo código se reescribe repetidamente o se necesita confiabilidad determinística
- **Ejemplo**: `scripts/rotate_pdf.py` para tareas de rotación de PDF
- **Beneficios**: Eficiente en tokens, determinístico, puede ejecutarse sin cargar en contexto
- **Nota**: Los scripts aún pueden necesitar ser leídos por Claude para parches o ajustes específicos del entorno

##### References (`references/`)

Documentación y material de referencia destinado a cargarse según se necesite en contexto para informar el proceso y pensamiento de Claude.

- **Cuándo incluir**: Para documentación que Claude debe referenciar mientras trabaja
- **Ejemplos**: `references/finance.md` para esquemas financieros, `references/mnda.md` para plantilla NDA de la empresa, `references/policies.md` para políticas de la empresa, `references/api_docs.md` para especificaciones de API
- **Casos de uso**: Esquemas de base de datos, documentación de API, conocimiento de dominio, políticas de empresa, guías de flujo de trabajo detalladas
- **Beneficios**: Mantiene SKILL.md delgado, cargado solo cuando Claude determina que se necesita
- **Mejor práctica**: Si los archivos son grandes (>10k palabras), incluir patrones de búsqueda grep en SKILL.md
- **Evitar duplicación**: La información debe vivir en SKILL.md o archivos de referencias, no en ambos. Preferir archivos de referencias para información detallada a menos que sea verdaderamente central para la skill—esto mantiene SKILL.md delgado mientras hace la información descubrible sin acaparar la ventana de contexto. Mantener solo instrucciones procedurales esenciales y guía de flujo de trabajo en SKILL.md; mover material de referencia detallado, esquemas y ejemplos a archivos de referencias.

##### Assets (`assets/`)

Archivos no destinados a cargarse en contexto, sino usados dentro de la salida que produce Claude.

- **Cuándo incluir**: Cuando la skill necesita archivos que se usarán en la salida final
- **Ejemplos**: `assets/logo.png` para assets de marca, `assets/slides.pptx` para plantillas de PowerPoint, `assets/frontend-template/` para boilerplate HTML/React, `assets/font.ttf` para tipografía
- **Casos de uso**: Plantillas, imágenes, iconos, código boilerplate, fuentes, documentos de muestra que se copian o modifican
- **Beneficios**: Separa recursos de salida de documentación, permite a Claude usar archivos sin cargarlos en contexto

#### Qué NO Incluir en una Skill

Una skill debe contener solo archivos esenciales que apoyen directamente su funcionalidad. NO crear documentación extra o archivos auxiliares, incluyendo:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

La skill debe contener solo la información necesaria para que un agente de IA haga el trabajo en cuestión. No debe contener contexto auxiliar sobre el proceso que llevó a crearla, procedimientos de configuración y prueba, documentación orientada al usuario, etc. Crear archivos de documentación adicionales solo agrega desorden y confusión.

### Principio de Diseño de Divulgación Progresiva

Las skills usan un sistema de carga de tres niveles para gestionar el contexto eficientemente:

1. **Metadata (name + description)** - Siempre en contexto (~100 palabras)
2. **Cuerpo de SKILL.md** - Cuando la skill se activa (<5k palabras)
3. **Recursos agrupados** - Según lo necesite Claude (Ilimitado porque los scripts pueden ejecutarse sin leer en la ventana de contexto)

#### Patrones de Divulgación Progresiva

Mantener el cuerpo de SKILL.md en lo esencial y bajo 500 líneas para minimizar la hinchazón de contexto. Dividir contenido en archivos separados al acercarse a este límite. Al dividir contenido en otros archivos, es muy importante referenciarlos desde SKILL.md y describir claramente cuándo leerlos, para asegurar que el lector de la skill sepa que existen y cuándo usarlos.

**Principio clave:** Cuando una skill soporta múltiples variaciones, frameworks u opciones, mantener solo el flujo de trabajo central y la guía de selección en SKILL.md. Mover detalles específicos de variante (patrones, ejemplos, configuración) a archivos de referencia separados.

**Patrón 1: Guía de alto nivel con referencias**

```markdown
# Procesamiento de PDF

## Inicio rápido

Extraer texto con pdfplumber:
[ejemplo de código]

## Características avanzadas

- **Llenado de formularios**: Ver [FORMS.md](FORMS.md) para guía completa
- **Referencia de API**: Ver [REFERENCE.md](REFERENCE.md) para todos los métodos
- **Ejemplos**: Ver [EXAMPLES.md](EXAMPLES.md) para patrones comunes
```

Claude carga FORMS.md, REFERENCE.md o EXAMPLES.md solo cuando se necesita.

**Patrón 2: Organización específica de dominio**

Para Skills con múltiples dominios, organizar contenido por dominio para evitar cargar contexto irrelevante:

```
bigquery-skill/
├── SKILL.md (resumen y navegación)
└── reference/
    ├── finance.md (métricas de ingresos, facturación)
    ├── sales.md (oportunidades, pipeline)
    ├── product.md (uso de API, características)
    └── marketing.md (campañas, atribución)
```

Cuando un usuario pregunta sobre métricas de ventas, Claude solo lee sales.md.

Similarmente, para skills que soportan múltiples frameworks o variantes, organizar por variante:

```
cloud-deploy/
├── SKILL.md (flujo de trabajo + selección de proveedor)
└── references/
    ├── aws.md (patrones de despliegue AWS)
    ├── gcp.md (patrones de despliegue GCP)
    └── azure.md (patrones de despliegue Azure)
```

Cuando el usuario elige AWS, Claude solo lee aws.md.

**Patrón 3: Detalles condicionales**

Mostrar contenido básico, enlazar a contenido avanzado:

```markdown
# Procesamiento DOCX

## Crear documentos

Usar docx-js para documentos nuevos. Ver [DOCX-JS.md](DOCX-JS.md).

## Editar documentos

Para ediciones simples, modificar el XML directamente.

**Para cambios rastreados**: Ver [REDLINING.md](REDLINING.md)
**Para detalles OOXML**: Ver [OOXML.md](OOXML.md)
```

Claude lee REDLINING.md o OOXML.md solo cuando el usuario necesita esas características.

**Guías importantes:**

- **Evitar referencias profundamente anidadas** - Mantener referencias un nivel profundo desde SKILL.md. Todos los archivos de referencia deben enlazar directamente desde SKILL.md.
- **Estructurar archivos de referencia más largos** - Para archivos más largos que 100 líneas, incluir una tabla de contenidos en la parte superior para que Claude pueda ver el alcance completo al previsualizar.

## Proceso de Creación de Skill

La creación de skill involucra estos pasos:

1. Entender la skill con ejemplos concretos
2. Planificar contenidos reutilizables de skill (scripts, referencias, assets)
3. Inicializar la skill (ejecutar init_skill.py)
4. Editar la skill (implementar recursos y escribir SKILL.md)
5. Empaquetar la skill (ejecutar package_skill.py)
6. Iterar basado en uso real

Seguir estos pasos en orden, omitiendo solo si hay una razón clara por la que no son aplicables.

### Paso 1: Entender la Skill con Ejemplos Concretos

Omitir este paso solo cuando los patrones de uso de la skill ya están claramente entendidos. Sigue siendo valioso incluso al trabajar con una skill existente.

Para crear una skill efectiva, entender claramente ejemplos concretos de cómo se usará la skill. Esta comprensión puede venir de ejemplos directos del usuario o ejemplos generados que se validan con retroalimentación del usuario.

Por ejemplo, al construir una skill de editor de imágenes, preguntas relevantes incluyen:

- "¿Qué funcionalidad debe soportar la skill de editor de imágenes? ¿Edición, rotación, algo más?"
- "¿Puedes dar algunos ejemplos de cómo se usaría esta skill?"
- "Puedo imaginar usuarios pidiendo cosas como 'Quita el efecto de ojos rojos de esta imagen' o 'Rota esta imagen'. ¿Hay otras formas en que imaginas que se use esta skill?"
- "¿Qué diría un usuario que debería activar esta skill?"

Para evitar abrumar a los usuarios, evitar hacer demasiadas preguntas en un solo mensaje. Comenzar con las preguntas más importantes y hacer seguimiento según sea necesario para mejor efectividad.

Concluir este paso cuando haya un sentido claro de la funcionalidad que la skill debe soportar.

### Paso 2: Planificar los Contenidos Reutilizables de la Skill

Para convertir ejemplos concretos en una skill efectiva, analizar cada ejemplo por:

1. Considerar cómo ejecutar el ejemplo desde cero
2. Identificar qué scripts, referencias y assets serían útiles al ejecutar estos flujos de trabajo repetidamente

Ejemplo: Al construir una skill `pdf-editor` para manejar consultas como "Ayúdame a rotar este PDF", el análisis muestra:

1. Rotar un PDF requiere reescribir el mismo código cada vez
2. Un script `scripts/rotate_pdf.py` sería útil para almacenar en la skill

Ejemplo: Al diseñar una skill `frontend-webapp-builder` para consultas como "Construye una app de tareas" o "Construye un dashboard para rastrear mis pasos", el análisis muestra:

1. Escribir una webapp frontend requiere el mismo boilerplate HTML/React cada vez
2. Una plantilla `assets/hello-world/` que contenga los archivos del proyecto boilerplate HTML/React sería útil para almacenar en la skill

Ejemplo: Al construir una skill `big-query` para manejar consultas como "¿Cuántos usuarios han iniciado sesión hoy?", el análisis muestra:

1. Consultar BigQuery requiere redescubrir los esquemas de tabla y relaciones cada vez
2. Un archivo `references/schema.md` documentando los esquemas de tabla sería útil para almacenar en la skill

Para establecer los contenidos de la skill, analizar cada ejemplo concreto para crear una lista de los recursos reutilizables a incluir: scripts, referencias y assets.

### Paso 3: Inicializar la Skill

En este punto, es hora de crear realmente la skill.

Omitir este paso solo si la skill que se está desarrollando ya existe y se necesita iteración o empaquetado. En este caso, continuar al siguiente paso.

Al crear una skill nueva desde cero, siempre ejecutar el script `init_skill.py`. El script genera convenientemente un directorio de skill de plantilla nuevo que incluye automáticamente todo lo que una skill requiere, haciendo el proceso de creación de skill mucho más eficiente y confiable.

Uso:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

El script:

- Crea el directorio de skill en la ruta especificada
- Genera una plantilla SKILL.md con frontmatter apropiado y placeholders TODO
- Crea directorios de recursos de ejemplo: `scripts/`, `references/` y `assets/`
- Agrega archivos de ejemplo en cada directorio que pueden personalizarse o eliminarse

Después de la inicialización, personalizar o eliminar el SKILL.md generado y los archivos de ejemplo según sea necesario.

### Paso 4: Editar la Skill

Al editar la skill (recién generada o existente), recordar que la skill se está creando para que otra instancia de Claude la use. Incluir información que sería beneficiosa y no obvia para Claude. Considerar qué conocimiento procedural, detalles específicos de dominio o assets reutilizables ayudarían a otra instancia de Claude a ejecutar estas tareas más efectivamente.

#### Aprender Patrones de Diseño Probados

Consultar estas guías útiles basadas en las necesidades de tu skill:

- **Procesos de múltiples pasos**: Ver references/workflows.md para flujos de trabajo secuenciales y lógica condicional
- **Formatos de salida específicos o estándares de calidad**: Ver references/output-patterns.md para patrones de plantilla y ejemplo

Estos archivos contienen mejores prácticas establecidas para diseño efectivo de skills.

#### Comenzar con Contenidos Reutilizables de Skill

Para comenzar la implementación, comenzar con los recursos reutilizables identificados arriba: archivos `scripts/`, `references/` y `assets/`. Notar que este paso puede requerir entrada del usuario. Por ejemplo, al implementar una skill `brand-guidelines`, el usuario puede necesitar proporcionar assets de marca o plantillas para almacenar en `assets/`, o documentación para almacenar en `references/`.

Los scripts agregados deben probarse ejecutándolos realmente para asegurar que no hay errores y que la salida coincide con lo esperado. Si hay muchos scripts similares, solo una muestra representativa necesita probarse para asegurar confianza de que todos funcionan mientras se equilibra el tiempo hasta completar.

Cualquier archivo y directorio de ejemplo no necesarios para la skill debe eliminarse. El script de inicialización crea archivos de ejemplo en `scripts/`, `references/` y `assets/` para demostrar estructura, pero la mayoría de las skills no necesitarán todos ellos.

#### Actualizar SKILL.md

**Guías de Escritura:** Siempre usar forma imperativa/infinitiva.

##### Frontmatter

Escribir el frontmatter YAML con `name` y `description`:

- `name`: El nombre de la skill
- `description`: Este es el mecanismo de activación principal para tu skill y ayuda a Claude a entender cuándo usar la skill.
  - Incluir tanto lo que hace la Skill como activadores/contextos específicos para cuándo usarla.
  - Incluir toda la información de "cuándo usar" aquí - No en el cuerpo. El cuerpo solo se carga después de la activación, por lo que las secciones "Cuándo Usar Esta Skill" en el cuerpo no son útiles para Claude.
  - Ejemplo de descripción para una skill `docx`: "Creación, edición y análisis comprehensivo de documentos con soporte para cambios rastreados, comentarios, preservación de formato y extracción de texto. Usar cuando Claude necesita trabajar con documentos profesionales (archivos .docx) para: (1) Crear documentos nuevos, (2) Modificar o editar contenido, (3) Trabajar con cambios rastreados, (4) Agregar comentarios, o cualquier otra tarea de documento"

No incluir ningún otro campo en el frontmatter YAML.

##### Cuerpo

Escribir instrucciones para usar la skill y sus recursos agrupados.

### Paso 5: Empaquetar una Skill

Una vez que el desarrollo de la skill esté completo, debe empaquetarse en un archivo .skill distribuible que se comparta con el usuario. El proceso de empaquetado valida automáticamente la skill primero para asegurar que cumple todos los requisitos:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Especificación opcional de directorio de salida:

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

El script de empaquetado:

1. **Validará** la skill automáticamente, verificando:

   - Formato de frontmatter YAML y campos requeridos
   - Convenciones de nomenclatura de skill y estructura de directorio
   - Completitud y calidad de descripción
   - Organización de archivos y referencias de recursos

2. **Empaquetará** la skill si la validación pasa, creando un archivo .skill nombrado después de la skill (p. ej., `my-skill.skill`) que incluye todos los archivos y mantiene la estructura de directorio apropiada para distribución. El archivo .skill es un archivo zip con extensión .skill.

Si la validación falla, el script reportará los errores y saldrá sin crear un paquete. Arreglar cualquier error de validación y ejecutar el comando de empaquetado de nuevo.

### Paso 6: Iterar

Después de probar la skill, los usuarios pueden solicitar mejoras. A menudo esto sucede justo después de usar la skill, con contexto fresco de cómo funcionó la skill.

**Flujo de trabajo de iteración:**

1. Usar la skill en tareas reales
2. Notar luchas o ineficiencias
3. Identificar cómo SKILL.md o recursos agrupados deben actualizarse
4. Implementar cambios y probar de nuevo

## Ejemplos de Uso

### Ejemplo 1: Crear una Skill para Procesar PDFs
**Situación**: Trabajas frecuentemente con PDFs y quieres crear una skill que enseñe a los agentes cómo rotar, extraer texto y llenar formularios en PDFs.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear una skill para procesar PDFs que incluya rotación, extracción de texto y llenado de formularios"
2. Cursor usará esta skill para:
   - Preguntarte ejemplos concretos de cómo usarías la skill
   - Identificar qué scripts serían útiles (como rotate_pdf.py)
   - Crear la estructura de la skill con init_skill.py
   - Escribir el SKILL.md con instrucciones claras
   - Empaquetar la skill para que puedas usarla

**Resultado**: Una skill completa y reutilizable que los agentes pueden usar para trabajar con PDFs, con scripts incluidos y documentación clara.

### Ejemplo 2: Crear una Skill de Referencia para tu API Interna
**Situación**: Tienes una API interna de tu empresa y quieres que los agentes sepan cómo usarla correctamente.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear una skill de referencia para nuestra API interna de facturación"
2. Cursor creará:
   - Una skill con estructura clara
   - Archivos de referencia con documentación detallada de la API
   - Ejemplos de uso en el SKILL.md principal
   - Organización que permite a Claude cargar solo la información relevante cuando se necesite

**Resultado**: Una skill de referencia que los agentes pueden encontrar fácilmente cuando trabajan con tu API, con toda la documentación organizada eficientemente.

### Ejemplo 3: Crear una Skill con Plantillas Reutilizables
**Situación**: Cada vez que creas una nueva aplicación frontend, usas la misma estructura base y quieres automatizarlo.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear una skill que incluya una plantilla de proyecto React con nuestra configuración estándar"
2. Cursor implementará:
   - Una skill con una carpeta assets/ que contiene tu plantilla completa
   - Instrucciones en SKILL.md sobre cómo usar la plantilla
   - La plantilla lista para copiar y personalizar cada vez que se necesite

**Resultado**: Una skill que acelera el inicio de nuevos proyectos, con tu configuración estándar lista para usar en cada proyecto nuevo.
