# Personalización

> Esta versión pública conserva las explicaciones y omite fragmentos que reproducen o adaptan la plantilla comercial.

Guía para adaptar Portify al sitio acordado: Angular con contenido Markdown/YAML,
prerenderizado estático y versiones en español e inglés. La plantilla se usa como
referencia visual; no se publica directamente como producto final.

Las seis secciones elegidas para el MVP (el sitio publicado suma dos más,
Galería y la guía DIY, hasta llegar a ocho) están en [Secciones y contenido](secciones-y-contenido.md#secciones-elegidas-para-el-mvp).
La [referencia de arquitectura](arquitectura.md) explica cómo se conectan las piezas del sitio.

## Puesta en marcha

Estos pasos sirven únicamente para explorar la plantilla original en local.
No son los comandos del frontend Angular de este sitio, que son los scripts de su
`package.json` (`npm start`, `npm run build`, `npm test`, `npm run lint`).

1. Copiar la variante elegida (`dots-bg`) a una carpeta de trabajo fuera de
   OneDrive; `node_modules` dentro de OneDrive sincroniza miles de archivos.
2. `npm install` y `npm run dev`; abrir `http://localhost:8080`.
3. Editar `src/index.html`; el servidor recarga solo.
4. `npm run build` y subir el contenido de `dist/`.

## Lista de pasos

| # | Adaptación para el sitio | Criterio |
| --- | --- | --- |
| 1 | Marca y recursos | Usar logos y recursos propios en SVG ([Parte 1 de la guía de construcción](01-marca-y-recursos.md)); optimizar imágenes y fuentes |
| 2 | Navegación | Inicio, Sobre mí, Habilidades, Experiencia, Proyectos y Contacto (más Galería en el sitio publicado); selector ES / EN |
| 3 | Inicio y Sobre mí | Perfil real, rol, presentación y acciones; no copiar cifras ni datos del personaje de ejemplo |
| 4 | Habilidades | Grupos e iconos sin gráficos de porcentaje; niveles reales para idiomas |
| 5 | Experiencia y CV | Cronología y contribuciones basadas en el CV; el texto inglés está cerrado y los PDF en inglés y en español ya están construidos en `public/cv/` |
| 6 | Proyectos | Tarjetas y páginas propias prerenderizadas; Markdown con front matter y datos de cada proyecto |
| 7 | Contacto | Invitación a escribir por LinkedIn y enlaces a redes; sin correo publicado, formulario, EmailJS, captcha ni mapa |
| 8 | Contenido | YAML/Markdown en el repositorio y validación durante el build; no editar textos dentro del HTML de Portify como solución final |
| 9 | Idiomas | `/es/` y `/en/`, interfaz, contenido, metadatos y textos accesibles traducidos |
| 10 | Renderizado | Angular estático; probar temprano las dependencias que usan APIs del navegador |
| 11 | Accesibilidad y movimiento | Teclado, foco, contraste, encabezados y un interruptor de animaciones propio (el sitio no consulta la preferencia del sistema); contenido visible sin animaciones |
| 12 | Publicación | Docker y Nginx en Coolify; rutas directas, metadatos, HTTPS y 404 real |

No trasladar servicios, cifras, proceso, blog ni testimonios al MVP. El selector
de color de demostración no cumple la función del selector de idioma. Las
bibliotecas de la plantilla se incorporan cuando resuelven una necesidad del sitio.

## Localización de elementos en la plantilla original

Referencia técnica conservada para encontrar recursos en Portify. Esta tabla
describe el original; no autoriza incorporar las funciones excluidas del MVP
ni sustituye la lista de adaptación anterior.

| # | Qué | Dónde |
| --- | --- | --- |
| 1 | Título, descripción y favicon | `<title>` y `<link rel="shortcut icon">` en los tres HTML; no trae `<meta name="description">` ni Open Graph: añadirlos (este sitio ya los tiene: [Parte 6](06-seo-y-vista-previa.md)) |
| 2 | Logo | `src/assets/images/logo.png` (menú móvil) e `icon.png` (barra lateral). El logo en el `dots-bg` sólo se ve en el menú del móvil |
| 3 | Foto | `src/assets/images/hero.png`, cuadrada (415 × 416); se muestra redonda |
| 4 | Hero | Saludo en `.freelancer`, roles en `app.js` (`strings: [...]` del Typewriter), ubicación en `.description`, textos y destinos de los dos botones |
| 5 | Menú | Un `<li>` por sección en `#navigation`; si se quita una sección, quitar también su `<li>` y renumerar los `NN/11` de todos los `.next-chapter` |
| 6 | Sobre mí | `<h2>`, `.desc`, los tres pares de `.contact` (corregir la etiqueta repetida «Email:») y el número de `.experience-card` (tres veces) |
| 7 | Servicios | Un `.swiper-slide` por servicio |
| 8 | Habilidades | Porcentajes de los gráficos radiales en `app.js` (`series` y `labels`, tres bloques); barras en el HTML (`<span>90%</span>` y `data-width`) |
| 9 | Cifras | Cada número tres veces |
| 10 | Experiencia | `.experience-item` por puesto; reemplazar `src/assets/resume.pdf` |
| 11 | Proyectos | Miniaturas, `data-title`, `data-img` (nombre del PNG grande sin extensión) y el texto fijo del modal |
| 12 | Proceso | Seis `.process` |
| 13 | Blog | Las dos tarjetas de `index.html`, `blogs.html` y un `blog-details.html` por artículo (la plantilla sólo trae uno) |
| 14 | Testimonios | Un `.swiper-slide` por testimonio, o quitar la sección |
| 15 | Contacto | Teléfono, correo, dirección, enlaces de redes (`href="#"` en todos) |
| 16 | EmailJS | `PUBLIC_KEY`, `SERVICE_ID` y `TEMPLATE_ID` al final de `app.js`; la plantilla de EmailJS debe usar `{{user_name}}`, `{{user_email}}` y `{{message}}` |
| 17 | Colores | `--primary` en `:root` de `styles.scss` (tripleta RGB) **y** `$primary`/`$secondary` en `bootstrap.scss`; los seis `data-color` del selector, o quitar el selector |
| 18 | Pie | «Designed By Pixelaxis»: la licencia *Regular* permite quitar el crédito |
| 19 | Grano | Cambiar la URL de Wikimedia por una textura local o quitar el grano |
| 20 | Idioma | Todo el texto está en inglés; `<html lang="en">` |

## Errores y limitaciones de la plantilla

- **Porcentajes en el JavaScript.** Los tres gráficos radiales tienen el
  valor en `app.js`, y la fila de idiomas reutiliza las mismas clases que la
  de diseño, así que muestra los mismos tres porcentajes. Para que cada
  gráfico tuviera su valor habría que adaptar el original. En nuestro sitio
  se elimina este comportamiento: las habilidades no llevan porcentajes.
- **Un solo modal para todos los proyectos.** Sólo cambian título e imagen;
  el resto del texto es común.
- **Etiquetas del formulario.** `<label for="name">` y `for="email"` del
  formulario de contacto apuntan a los campos del formulario del modal.
- **«Email:» repetido** en la fila de datos de «Sobre mí».
- **`<h1>` vacío** en el HTML (lo escribe el Typewriter): mal para SEO y
  para lectores de pantalla.
- **Textura del grano externa** (Wikimedia): si cae ese enlace, el grano
  desaparece; además es una petición a un tercero en cada carga.
- **CSS de 4 MB sin minificar**: el build no activa `minimize` ni PurgeCSS, y
  la fuente de iconos Phosphor va en base64 dentro del CSS. Con PurgeCSS
  activado y los iconos como SVG el peso baja a una fracción.
- **Sin metadatos sociales**: no hay `description`, Open Graph ni Twitter
  Card. Las vistas previas de LinkedIn o WhatsApp salen vacías. Esto es cierto de la
  plantilla; este sitio ya tiene `description`, Open Graph, canonical y hreflang,
  `robots.txt` y un sitemap, explicados en la
  [Parte 6](06-seo-y-vista-previa.md).
- **Accesibilidad**: los botones de color del selector no tienen texto ni
  `aria-label`, las imágenes decorativas llevan `alt=""` pero la foto del
  hero también; los enlaces de redes son `href="#"`.
- **EmailJS en el cliente**: forma parte del formulario original. No se
  integra en el MVP porque el contacto se resuelve por LinkedIn y los enlaces
  a redes, sin correo publicado, formulario ni backend de mensajes.
- **`shuffle-letters` y `grained`** están instalados y no se usan
  (`shuffle-letters` sólo en las tres variantes de menú horizontal).

## Qué significa esto para el front

Se adaptan los estilos y mecanismos visuales pertinentes de
[Estilos y animaciones](estilos-y-animaciones.md), no el orden completo ni todas las
funciones de la plantilla. Angular está elegido, sin Analog ni Django. El contenido
vive en Git, se prepara con Node y alimenta páginas estáticas servidas por Nginx.
