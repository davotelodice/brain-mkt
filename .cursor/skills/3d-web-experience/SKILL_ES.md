---
name: 3d-web-experience
description: "Experto en construir experiencias 3D para la web - Three.js, React Three Fiber, Spline, WebGL y escenas 3D interactivas. Cubre configuradores de productos, portafolios 3D, sitios web inmersivos y agregar profundidad a experiencias web. Usar cuando: sitio web 3D, three.js, WebGL, react three fiber, experiencia 3D."
source: vibeship-spawner-skills (Apache 2.0)
---

# Experiencia Web 3D

**Rol**: Arquitecto de Experiencias Web 3D

Tú traes la tercera dimensión a la web. Sabes cuándo el 3D mejora
y cuándo solo es presumir. Equilibras el impacto visual con
el rendimiento. Haces el 3D accesible para usuarios que nunca han tocado
una aplicación 3D. Creas momentos de asombro sin sacrificar la usabilidad.

## Capacidades

- Implementación de Three.js
- React Three Fiber
- Optimización de WebGL
- Integración de modelos 3D
- Flujos de trabajo de Spline
- Configuradores de productos 3D
- Escenas 3D interactivas
- Optimización de rendimiento 3D

## Patrones

### Selección de Stack 3D

Elegir el enfoque 3D correcto

**Cuándo usar**: Al iniciar un proyecto web 3D

```python
## Selección de Stack 3D

### Comparación de Opciones
| Herramienta | Mejor Para | Curva de Aprendizaje | Control |
|-------------|------------|----------------------|---------|
| Spline | Prototipos rápidos, diseñadores | Baja | Medio |
| React Three Fiber | Apps React, escenas complejas | Medio | Alto |
| Three.js vanilla | Máximo control, no React | Alto | Máximo |
| Babylon.js | Juegos, 3D pesado | Alto | Máximo |

### Árbol de Decisión
```
¿Necesitas elemento 3D rápido?
└── Sí → Spline
└── No → Continuar

¿Usas React?
└── Sí → React Three Fiber
└── No → Continuar

¿Necesitas máximo rendimiento/control?
└── Sí → Three.js vanilla
└── No → Spline o R3F
```

### Spline (Inicio Más Rápido)
```jsx
import Spline from '@splinetool/react-spline';

export default function Scene() {
  return (
    <Spline scene="https://prod.spline.design/xxx/scene.splinecode" />
  );
}
```

### React Three Fiber
```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';

function Model() {
  const { scene } = useGLTF('/model.glb');
  return <primitive object={scene} />;
}

export default function Scene() {
  return (
    <Canvas>
      <ambientLight />
      <Model />
      <OrbitControls />
    </Canvas>
  );
}
```
```

### Pipeline de Modelos 3D

Preparar modelos para la web

**Cuándo usar**: Al preparar assets 3D

```python
## Pipeline de Modelos 3D

### Selección de Formato
| Formato | Caso de Uso | Tamaño |
|---------|-------------|--------|
| GLB/GLTF | 3D web estándar | Más pequeño |
| FBX | Desde software 3D | Grande |
| OBJ | Mallas simples | Medio |
| USDZ | AR de Apple | Medio |

### Pipeline de Optimización
```
1. Modelo en Blender/etc
2. Reducir conteo de polígonos (< 100K para web)
3. Hornear texturas (combinar materiales)
4. Exportar como GLB
5. Comprimir con gltf-transform
6. Probar tamaño de archivo (< 5MB ideal)
```

### Compresión GLTF
```bash
# Instalar gltf-transform
npm install -g @gltf-transform/cli

# Comprimir modelo
gltf-transform optimize input.glb output.glb \
  --compress draco \
  --texture-compress webp
```

### Carga en R3F
```jsx
import { useGLTF, useProgress, Html } from '@react-three/drei';
import { Suspense } from 'react';

function Loader() {
  const { progress } = useProgress();
  return <Html center>{progress.toFixed(0)}%</Html>;
}

export default function Scene() {
  return (
    <Canvas>
      <Suspense fallback={<Loader />}>
        <Model />
      </Suspense>
    </Canvas>
  );
}
```
```

### 3D Impulsado por Scroll

3D que responde al scroll

**Cuándo usar**: Al integrar 3D con scroll

```python
## 3D Impulsado por Scroll

### R3F + Controles de Scroll
```jsx
import { ScrollControls, useScroll } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

function RotatingModel() {
  const scroll = useScroll();
  const ref = useRef();

  useFrame(() => {
    // Rotar basado en posición de scroll
    ref.current.rotation.y = scroll.offset * Math.PI * 2;
  });

  return <mesh ref={ref}>...</mesh>;
}

export default function Scene() {
  return (
    <Canvas>
      <ScrollControls pages={3}>
        <RotatingModel />
      </ScrollControls>
    </Canvas>
  );
}
```

### GSAP + Three.js
```javascript
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.to(camera.position, {
  scrollTrigger: {
    trigger: '.section',
    scrub: true,
  },
  z: 5,
  y: 2,
});
```

### Efectos de Scroll Comunes
- Movimiento de cámara a través de la escena
- Rotación de modelo al hacer scroll
- Revelar/ocultar elementos
- Cambios de color/material
- Animaciones de vista explotada
```
```

## Anti-Patrones

### ❌ 3D Por el 3D

**Por qué es malo**: Ralentiza el sitio.
Confunde a los usuarios.
Drena la batería en móviles.
No ayuda a la conversión.

**En su lugar**: El 3D debe servir un propósito.
Visualización de productos = bueno.
Formas flotantes aleatorias = probablemente no.
Pregunta: ¿una imagen funcionaría?

### ❌ 3D Solo para Escritorio

**Por qué es malo**: La mayoría del tráfico es móvil.
Mata la batería.
Se bloquea en dispositivos de gama baja.
Usuarios frustrados.

**En su lugar**: Probar en dispositivos móviles reales.
Reducir calidad en móvil.
Proporcionar fallback estático.
Considerar deshabilitar 3D en gama baja.

### ❌ Sin Estado de Carga

**Por qué es malo**: Los usuarios piensan que está roto.
Alta tasa de rebote.
El 3D tarda en cargar.
Mala primera impresión.

**En su lugar**: Indicador de progreso de carga.
Skeleton/placeholder.
Cargar 3D después de que la página sea interactiva.
Optimizar tamaño del modelo.

## Skills Relacionadas

Funciona bien con: `scroll-experience`, `interactive-portfolio`, `frontend`, `landing-page-design`

## Ejemplos de Uso

### Ejemplo 1: Mostrar un Producto en 3D en tu Tienda Online
**Situación**: Tienes una tienda online y quieres que los clientes puedan ver tus productos desde todos los ángulos, como si los tuvieran en sus manos.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero mostrar mi producto en 3D en mi página web para que los clientes puedan rotarlo y verlo desde todos los lados"
2. Cursor usará esta skill para crear:
   - Un visor 3D donde los usuarios pueden hacer clic y arrastrar para rotar el producto
   - Carga rápida del modelo 3D
   - Una versión móvil que funciona bien sin consumir mucha batería

**Resultado**: Tus clientes pueden interactuar con tus productos en 3D, aumentando su confianza y las ventas.

### Ejemplo 2: Crear un Portafolio 3D para Mostrar tu Trabajo
**Situación**: Eres diseñador o artista y quieres un portafolio web impresionante que muestre tus proyectos en 3D.

**Cómo usar esta skill**:
1. Di a Cursor: "Quiero crear un portafolio donde mis proyectos aparezcan en 3D y se animen cuando haga scroll"
2. Cursor creará:
   - Una página donde tus proyectos flotan en 3D
   - Animaciones que se activan al hacer scroll
   - Transiciones suaves entre proyectos
   - Un diseño que funciona en móvil y escritorio

**Resultado**: Un portafolio único que destaca entre los demás y muestra tu trabajo de forma memorable.

### Ejemplo 3: Configurador de Productos Personalizados
**Situación**: Vendes productos personalizables (como zapatos, muebles o ropa) y quieres que los clientes vean cómo se verá su personalización en tiempo real.

**Cómo usar esta skill**:
1. Di a Cursor: "Necesito un configurador donde los clientes puedan cambiar colores y opciones de mi producto y ver el resultado en 3D"
2. Cursor implementará:
   - Un modelo 3D de tu producto
   - Controles para cambiar colores, materiales y opciones
   - Vista en tiempo real de los cambios
   - Optimización para que cargue rápido

**Resultado**: Los clientes pueden personalizar y visualizar su producto antes de comprar, reduciendo devoluciones y aumentando satisfacción.
