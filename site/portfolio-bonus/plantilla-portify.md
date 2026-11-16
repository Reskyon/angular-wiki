# Plantilla Portify

> Esta versión pública conserva las explicaciones y omite fragmentos que reproducen o adaptan la plantilla comercial.

> Referencia de la plantilla original, no lista de funciones obligatorias del
> sitio. Consultar las [seis secciones elegidas](secciones-y-contenido.md#secciones-elegidas-para-el-mvp)
> y la [adaptación para el MVP](personalizacion.md): sin porcentajes de habilidades,
> formulario ni mapa. Sólo se trasladan los estilos y dependencias necesarios.
> El sitio publicado tiene hoy siete secciones: las seis del MVP más Galería.

**Portify** es una plantilla HTML de portfolio personal de una sola página,
vendida en ThemeForest por Pixelaxis (el encabezado de `styles.scss` dice
«Author: SOFTIVUS»). Versión comprada: **1.0.2**. Es la misma plantilla que
usa [alexperezortuno.pro](https://alexperezortuno.pro/en/), en su variante
`dots-bg`.

No es un proyecto de Angular ni de Vue: es HTML estático con Bootstrap 5,
SCSS y un puñado de librerías de JavaScript, empaquetado con webpack 5. Para
nuestro front sirve como **diseño de referencia y fuente de estilos**; la
lógica se reescribe.

## Dónde está

Todo vive en OneDrive, fuera del repositorio:


Cada variante es un **proyecto webpack completo e independiente** (su propio
`package.json`, `src/` y `dist/`). Comparten casi todo el código: cambian la
navegación y el fondo.

## Las ocho variantes

| Variante | Navegación | Fondo | Notas |
| --- | --- | --- | --- |
| `left-bar` | Menú horizontal *sticky* debajo del hero; barra fija a la izquierda con redes y un icono de correo | Liso | Contenedor `container` (no fluido) |
| `topbar` | Menú en la cabecera, arriba, con el correo al lado | Liso | |
| `sticky-menu` | Menú horizontal *sticky* con el logo, debajo del hero | Liso | |
| `clean-bg` | Columna vertical a la derecha con números (`01 top`, `02 about me`…) | Liso | Base de las cuatro siguientes |
| `dots-bg` | Igual que `clean-bg` | `<canvas id="background-canvas">`: malla de puntos unidos por líneas que reacciona al ratón (GSAP ticker) | **La que usa alexperezortuno.pro** |
| `gradiant-bg` | Igual que `clean-bg` | SVG `.area` con cuatro manchas de color animadas por CSS | «gradiant» es la grafía del autor |
| `shape-bg` | Igual que `clean-bg` | `ul.circles` con diez cuadrados flotantes animados por CSS | |
| `snowfall-bg` | Igual que `clean-bg` | `#bg-area` con `div.snowflake` cayendo por CSS | |

Las variantes de menú vertical (`clean-bg` y sus derivadas) usan
`<main class="container-fluid">` con el contenido en `col-xl-9` y el `<nav>`
ocupando el resto; además animan el texto de cada enlace del menú con un
efecto de letras aleatorias (`animateNavLabel`) al activarse. Las otras tres
(`left-bar`, `topbar`, `sticky-menu`) importan `shuffle-letters` para lo
mismo, pero la llamada está comentada.

## Qué hay dentro de una variante


`dist/` se puede abrir directamente en el navegador (`dist/index.html`)
porque las rutas son relativas (`./assets/...`). Hacen falta dos recursos de
internet: la fuente Poppins (Google Fonts) y la textura del grano, que se
carga desde Wikimedia (ver [Estilos y animaciones](estilos-y-animaciones.md#el-grano)).

## Cómo se compila

Dentro de la carpeta de la variante:


Lo que hace `webpack.config.js`:

- Entrada única: `src/assets/js/app.js`. La primera línea de ese archivo es
  `import "../scss/styles.scss"`, así que **el CSS entra por el JavaScript**.
- `HtmlWebpackPlugin` tres veces: genera `index.html`, `blogs.html` y
  `blog-details.html` a partir de `src/` e inyecta `<script>` y `<link>`
  (por eso los HTML de `src/` no tienen etiquetas de CSS ni JS).
- `MiniCssExtractPlugin` saca el CSS a `assets/css/index.css`.
- `CopyPlugin` copia `src/assets/images` a `dist/assets/images`.
- Cadena SCSS: `sass-loader`, `postcss-loader` (autoprefixer), `css-loader`.
- `PurgeCSSPlugin` está instalado pero **comentado**, y `optimization.minimize`
  es `false`: el build no minifica. Por eso `index.css` pesa 4 MB (la mayor
  parte es la fuente de iconos Phosphor incrustada en base64).

## Librerías

| Paquete | Versión | Para qué | Dónde se usa |
| --- | --- | --- | --- |
| `bootstrap` + `@popperjs/core` | 5.3.3 | Grid, utilidades, modal, ScrollSpy | Todo el HTML; `data-bs-spy`, `data-bs-toggle="modal"` |
| `gsap` + `ScrollTrigger` | 3.12 | Animaciones de entrada y al hacer scroll | Bloque `// animations` de `app.js` |
| `split-type` | 0.3 | Parte un texto en letras para animarlas una a una | `.freelancer` y `.description` del hero |
| `typewriter-effect` | 2.21 | Efecto máquina de escribir | `#typewriter` del hero (`["Developer", "Designer"]`) |
| `swiper` | 11 | Carruseles | Servicios (`.service-swiper`) y testimonios (`.testimonial-swiper`) |
| `apexcharts` | 3.49 | Gráficos radiales de porcentaje | Sección *Attainments* (`.design-chart`, `.branding-chart`, `.ecommerce-chart`) |
| `phosphor-icons` | 1.4 | Iconos como fuente (`<i class="ph ph-envelope">`) | Toda la página |
| `glightbox` | 3.3 | Popup de vídeo de YouTube | `.youtube` en `blog-details.html` |
| `@emailjs/browser` | 4.3 | Envía el formulario de contacto a un correo sin backend | Final de `app.js` |
| `shuffle-letters` | 1.1 | Letras aleatorias en el menú | Importado y comentado (sólo variantes de menú horizontal) |
| `grained` | 0.0.2 | Textura de grano | **Declarado pero no se usa**: el grano es CSS puro |
| `purgecss-webpack-plugin` | 6 | Quitar CSS sin usar | Comentado en webpack |

Dependencias de desarrollo: `webpack`, `webpack-cli`, `webpack-dev-server`,
`sass`, `sass-loader`, `postcss-loader`, `autoprefixer`, `css-loader`,
`style-loader`, `mini-css-extract-plugin`, `html-webpack-plugin`,
`copy-webpack-plugin`, `prettier`.

La tipografía es **Poppins** (pesos 400 a 900), importada desde Google Fonts
en la primera línea de `styles.scss`.

## La documentación del autor

`html/documentation/index.html` es una página corta: instalación
(`npm install`, `npm run dev`, `npm run build`), cambiar el logo
(`src/assets/images/logo.png`), cambiar colores (`$yellow` en
`bootstrap.scss`) y configurar EmailJS (clave pública, *service id* y
*template id* al final de `app.js`). Todo eso está ampliado en
[Personalización](personalizacion.md).

## El archivo de Figma

`figma/Portify.fig` es el diseño original. Sirve para sacar medidas, colores
y espaciados exactos cuando reconstruyamos los componentes en el front, y
para diseñar secciones nuevas con el mismo lenguaje visual. Se abre
importándolo en Figma (*Import file*).
