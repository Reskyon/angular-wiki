# Secciones y contenido

> Esta versión pública conserva las explicaciones y omite fragmentos que reproducen o adaptan la plantilla comercial.

Esta página distingue las decisiones del sitio de Janio de la anatomía de la
plantilla original. Portify incluye once secciones; el MVP se acordó con **seis**
y el sitio publicado tiene hoy **siete** (se suma Galería, ver más abajo), en
español e inglés. La [referencia de arquitectura](arquitectura.md) explica cómo
se prepara y se publica ese contenido.

## Secciones elegidas para el MVP

| Orden | Sección | Adaptación de Portify |
| --- | --- | --- |
| 1 | Inicio | Nombre, rol, presentación breve, proyectos y descarga del CV |
| 2 | Sobre mí | Recorrido de diseño a frontend y relación con Reskyon; sin repetir todo el CV |
| 3 | Habilidades | Grupos, iconos y etiquetas sin porcentajes; Angular como especialidad |
| 4 | Experiencia | Cronología inversa, cargos, fechas y contribuciones; tecnologías secundarias |
| 5 | Proyectos | Tarjetas y páginas de detalle propias; no un modal común |
| 6 | Contacto | Invitación a escribir por LinkedIn, enlaces a LinkedIn y GitHub (el de Reskyon queda oculto mientras su sitio esté en construcción), y ubicación general; sin correo publicado, formulario ni mapa |

Servicios, cifras, proceso, blog y testimonios quedan fuera del MVP. Recursos no
tiene sección propia: la guía de Angular se enlaza desde su proyecto y el pie.
La tabla recoge las seis secciones acordadas para el MVP. La navegación las sigue (desde el 14 de noviembre de 2026 se
suma Galería entre Proyectos y Contacto, ver
[Parte 5](05-galeria.md#módulo-g5-la-entrada-en-la-portada)); si se conserva «Next Chapter», sus
etiquetas y numeración deben corresponder al recorrido real, no a los once pasos
originales.

El selector ES / EN conecta las rutas `/es/` y `/en/`. Se traducen interfaz,
contenido y metadatos. Los detalles de proyectos usan `/es/projects/:slug` y
`/en/projects/:slug`. La guía externa puede mantenerse en español.

Hay un PDF en inglés y otro en español en `public/cv/`, con sus botones de
descarga. El procedimiento está en [Tareas y diagnóstico de fallos](maintenance.md).

## Cómo leer la referencia de Portify

Lo que sigue describe el `index.html` original de `dots-bg`, sus once secciones,
IDs y campos. Se conserva para localizar estilos y entender qué adaptar, no como
especificación de once secciones obligatorias. Los campos descritos aquí son los
de la plantilla original. Para ver cómo se usan los datos en Angular, consulta
[Experiencia](learn-experience.md) y [Proyectos](learn-projects.md).

## El esqueleto de una sección


Tres cosas se repiten en todas: el `id` (lo usa el menú y el ScrollSpy de
Bootstrap), la clase `section` (la usa GSAP para animar el título y el texto
de fondo) y el `next-chapter` (hay que renumerarlo a mano si se quita una
sección).

Campos comunes a todas las secciones: `id`, `overlayText`, `subtitle`,
`title`, `order` (el número del capítulo).

## El orden y el menú

| # | `id` | Texto del menú | Clase CSS | Qué muestra |
| --- | --- | --- | --- | --- |
| 01 | `top` | top | `.hero` | Saludo, rol con efecto máquina de escribir, foto, dos botones |
| 02 | `about_me` | about me | `.about` | Presentación, datos de contacto, tarjeta «años de experiencia» |
| 03 | `services` | my services | `.services` | Carrusel de tarjetas de servicio |
| 04 | `attainments` | skills | `.attainments` | Tres filas: gráficos radiales, barras de progreso, idiomas |
| 05 | `fun_facts` | facts | `.fun_facts` | Cuatro cifras grandes |
| 06 | `experience` | experiences | `.experience` | Línea de tiempo y botón de descarga del CV |
| 07 | `projects` | projects | `.projects` | Tres tarjetas que abren un modal |
| 08 | `how_i_work` | how i work | `.how-i-work` | Seis pasos del proceso |
| 09 | `blogs` | Blogs | `.blogs` | Dos artículos y enlace a `blogs.html` |
| 10 | `testimonials` | testimonials | `.testimonials` | Carrusel de testimonios |
| 11 | `contact` | contact | `.contact` | Datos de contacto, redes y formulario |

El `<nav class="navigation" id="navigation">` tiene un `<li class="nav-link">`
por sección, con `<a href="#id">`. Bootstrap marca el enlace activo con
`data-bs-spy="scroll" data-bs-target="#navigation"` en el contenedor del
contenido. En el móvil el menú se abre con el botón `.nav-icon` (tres
líneas) y se cierra con `.nav-overlay` o al tocar un enlace.

## 01 · Hero (`#top`)


- El `<h1>` está **vacío en el HTML**: lo rellena `typewriter-effect` con
  las palabras de `app.js` (`strings: ["Developer", "Designer"]`). Para el
  SEO conviene que el front deje una palabra escrita en el HTML inicial.
- La foto es redonda (`rounded-circle`) con las ondas `.waves-top` y
  `.waves-bottom` alrededor (cuatro `<span>` vacíos cada una).
- `.freelancer` y `.description` se parten en letras con SplitType para la
  animación de entrada; si el texto lleva etiquetas dentro, se rompe.

Campos: `greeting`, `roles[]` (las palabras del efecto), `location`,
`primaryButton{text, href}`, `secondaryButton{text, href}`, `photo`.

La versión construida en el sitio, con el nombre en el `<h1>` y sin efecto
máquina de escribir, está en el
[Módulo S1 de la Parte 3](03-secciones-de-portify.md#módulo-s1-el-hero-jerarquía-de-texto-retrato-y-ondas).

## 02 · Sobre mí (`#about_me`)

Dos columnas: a la izquierda `.about-desc` (un `<h2>` con el nombre y el
rol, un párrafo `.desc` y una fila `.contact` con tres pares etiqueta/valor);
a la derecha `.experience-card`, la tarjeta con el número grande.


El número se escribe **tres veces**: dos copias con `-webkit-text-stroke`
(sólo contorno) giradas, que se mueven con el ratón (`mousemove` en
`app.js`), y la copia principal. Al pasar el ratón por la tarjeta, los
contornos y los dos marcos girados (`::before`/`::after`) se alinean y
desaparecen.

La plantilla trae un error: las tres etiquetas de la fila `.contact` dicen
«Email:», «Date of Birth:» y otra vez «Email:» (la tercera debería ser
«Location:»).

Campos: `headline`, `bio`, `facts[]{label, value, href?}` (tres),
`highlight{number, label}`.

## 03 · Servicios (`#services`)

Fuera del MVP. La descripción siguiente es referencia de la plantilla.

Un Swiper (`.service-swiper`) con un `.swiper-slide` por servicio. Cada
tarjeta `.service-card` tiene un `.number-circle` con el número (`01`, `02`…)
rodeado de ondas pequeñas (`.waves-top-sm`/`.waves-bottom-sm`), un `<h4>` y
una lista `.service-list` de cinco ítems con el icono `ph-caret-double-right`.

Configuración del carrusel (en `app.js`): 1 tarjeta en móvil, 2 desde 768 px,
3 desde 1550 px; autoplay cada 5 s; paginación con puntos (`.swiper-pagination`).
El contenedor lleva `dir="ltr"` fijo para que el carrusel no se invierta en RTL.

Campos: `services[]{number, title, items[]}`.

## 04 · Habilidades (`#attainments`)

No usa el título estándar (no hay `.section-title`): tiene tres filas, cada
una con un `.section-title-sm` a la izquierda (`<h2>` + subtítulo + número
`01.-`) y el contenido a la derecha.

| Fila | Clase | Contenido | Dónde está el valor |
| --- | --- | --- | --- |
| Design Skills | `.design-row` | Tres gráficos radiales de ApexCharts con un botón debajo (Design, Branding, Ecommerce) | **En `app.js`**, no en el HTML: `series: ["85"]` para `.design-chart`, `["85"]` para `.branding-chart`, `["80"]` para `.ecommerce-chart` |
| Developer Skills | `.developer-row` | Seis barras `.skill` con nombre y porcentaje | En el HTML: `<span>90%</span>` y `data-width="90%"` en `.progress-bar` (hay que escribirlo dos veces) |
| Language Skills | `.language-row` | Tres gráficos radiales (French, English, Dutch) | Reutiliza las **mismas clases** `.design-chart`, `.branding-chart`, `.ecommerce-chart`, así que salen los mismos porcentajes que la fila de diseño |

Los gráficos se dibujan cuando entran en pantalla (IntersectionObserver al
70 %) y las barras se animan al 50 %. Esta es la sección más rígida de la
plantilla. En el sitio de Janio estos gráficos y barras de porcentaje se
sustituyen por grupos, iconos y etiquetas; los idiomas muestran niveles del CV.

Campos de la plantilla original, que no se trasladan como requisitos al MVP: `skillGroups[]{title, subtitle, kind: 'radial' | 'bar', skills[]{name, percent}}`.

## 05 · Cifras (`#fun_facts`)

Fuera del MVP. No se requieren métricas para completar el contenido.

Cuatro `.fun-fact` repartidos en dos filas desplazadas (la segunda fila lleva
`offset-md-2 offset-xl-5` para quedar escalonada). Cada cifra usa el mismo
truco de tres copias que la tarjeta de «Sobre mí» (`.number-outline-one`,
`.number-outline-two`, `.number-main`).

Campos: `facts[]{number, label}` (cuatro).

## 06 · Experiencia (`#experience`)


La línea vertical de la izquierda se dibuja con dos variables CSS que GSAP
anima al hacer scroll: `--height` en `.experience-wrapper` (la línea gris
completa) y `--item-height` en cada `.experience-item` (el tramo negro de
cada entrada). El botón redondo descarga `src/assets/resume.pdf`.

Campos: `experience[]{period, title, description}`, `resumeFile`.

## 07 · Proyectos (`#projects`)

Tres tarjetas `.single-project` en una fila (`col-sm-6 col-xl-4`). Cada una
abre el **mismo modal** `#project-details` (Bootstrap, `modal-fullscreen`):


Al hacer clic, `app.js` sólo cambia **dos cosas** del modal: el título
(`#project-title` = `data-title`) y la imagen grande
(`.project-details-img` = `./assets/images/${data-img}.png`). Todo el resto
del modal (descripción, objetivos, ficha de cliente/categoría/fechas/
herramientas, «Challenges and Solutions», dos imágenes, «Key Features»,
«Outcome» y un segundo formulario de contacto) es texto fijo, igual para los
tres proyectos. En Angular se usarán páginas propias por proyecto, con Markdown
y front matter para su contenido, y rutas localizadas. No se incorpora el
formulario del modal ni se exige un cliente para proyectos personales.

La versión construida (tarjeta con el efecto de Portify y página de detalle
con barra lateral) está en el
[Módulo S7 de la Parte 3](03-secciones-de-portify.md#módulo-s7-proyectos-tarjetas-y-página-de-detalle);
el procedimiento para publicar un proyecto nuevo, en
[Agregar un proyecto](agregar-un-proyecto.md).

Campos del modal original (no el esquema final del sitio): `slug`, `title`, `subtitle`, `tags[]`, `thumbnail`,
`cover`, `client`, `category`, `startDate`, `endDate`, `tools`,
`summary`, `goals[]`, `challenges`, `gallery[]`, `features[]`, `outcome`.

## 08 · Cómo trabajo (`#how_i_work`)

Fuera del MVP como sección independiente.

Seis `.process` (idea, sketch, design, develop, text, launch), cada uno con
un `<span class="circle">` o `.circle-even` detrás (alternan la forma) y dos
párrafos: número y nombre. Debajo, el bloque `.more-info` con un texto, una
línea y la flecha redonda hacia `#contact`.

Campos: `steps[]{number, label}`, `callToAction{text, href}`.

## 09 · Blog (`#blogs`)

Fuera del MVP. Las páginas de artículos se conservan aquí sólo como referencia.

Dos `<a class="blog-card" href="blog-details.html">` con imagen, título,
fecha (`ph-calendar`), tiempo de lectura (`ph-clock`), extracto `.details` y
etiquetas. Debajo, `.more-info` con «View All Articles» hacia `blogs.html`.

Campos por artículo: `slug`, `title`, `date`, `readingTime`, `excerpt`,
`image`, `tags[]`. El cuerpo del artículo es Markdown (ver
[las páginas de blog](#las-páginas-de-blog)).

## 10 · Testimonios (`#testimonials`)

Fuera del MVP. No se incorporan testimonios de ejemplo.

Swiper `.testimonial-swiper` con una `.testimonial-card` por slide: foto
redonda con ondas, nombre, cargo, web y texto `.desc`. Navegación con los
botones `.testi-prev`/`.testi-next` y una barra `.s-scrollbar`. Muestra 1
tarjeta en móvil y 1,4 desde 1024 px; autoplay cada 5 s.

Campos: `testimonials[]{name, role, website, text, photo}`.

## 11 · Contacto (`#contact`)

En el MVP el contacto es por LinkedIn: un texto breve invita a escribir por
ahí y un enlace lleva al perfil, seguido de los enlaces a LinkedIn y GitHub
(el de Reskyon está comentado en `profile.yml` mientras su sitio esté en
construcción), la ciudad y la disponibilidad remota. **No se publica el correo**
para evitar que lo
recojan los rastreadores y deja la conversación en un perfil que ya identifica
a las dos partes. Tampoco hay formulario, EmailJS, mapa ni dirección física.
En `profile.yml` los campos son `contact.message` y `contact.cta`, y la
validación exige un enlace con id `linkedin`. Lo siguiente describe el
original.

Cuatro `.contact-item` (teléfono, correo, dirección, redes) y el formulario
`#contact-form` con `user_name`, `user_email` y `message`. Los `name` de los
campos **tienen que coincidir** con las variables de la plantilla de EmailJS.
El envío lo hace `emailjs.sendForm(SERVICE_ID, TEMPLATE_ID, form)`; sin las
tres claves rellenas en `app.js`, sale un `alert`.

Los `<label for="name">` y `for="email"` del formulario apuntan a los `id`
del formulario **del modal** (`id="name"`, `id="email"`), no a los suyos
(`user_name`, `user_email`): error de accesibilidad de la plantilla.

Campos: `phone`, `email`, `address`, `social[]{network, href}`.

## El pie y el selector de color

El `<footer>` tiene el año (`#year`, lo escribe `app.js`) y el crédito
«Designed By Pixelaxis». El `.color-switcher` (engranaje flotante) ofrece
seis colores de fondo, LTR/RTL y el grano; es una demo para el comprador y
no hace falta conservarlo. Detalle en
[Estilos y animaciones](estilos-y-animaciones.md#el-selector-de-color).

## Las páginas de blog

No se implementan en el MVP. Esta sección documenta los archivos originales.

**`blogs.html`** (listado): cabecera `header.header-blog`, hero `.blog-hero`,
sección `.topics` con filtros (`.topic` activa/desactiva con un clic, sin
filtrar nada de verdad), la lista de `.blog-card`, una `.pagination`
decorativa, la sección `.newsletter` y el pie.

**`blog-details.html`** (artículo): dos columnas. A la izquierda,
`.details-left` con la tabla de contenidos (`#blog-index`, un ScrollSpy
sobre los `id` de los encabezados del artículo). A la derecha,
`.details-container > .details-content` con: fila de título (imagen +
`<h3>` + fecha), párrafos `.text-lg`, encabezados `<h4>`/`<h5>` con `id`,
un bloque `.blog-video` (imagen + enlace `.youtube` que abre GLightbox),
una cita `.quote`, imágenes, `.share` (redes) y `.next-prev` (artículo
anterior y siguiente). Debajo, `.newsletter` y el pie.

Esa estructura (encabezados con ancla, párrafos, imágenes, cita, vídeo) es
exactamente lo que produce un archivo Markdown: título y metadatos en el
*front matter*, cuerpo en Markdown, y la tabla de contenidos generada a partir
de los `##`.

## Imágenes que trae la plantilla

| Archivo | Uso | Tamaño de referencia |
| --- | --- | --- |
| `hero.png` | Foto del hero y de los testimonios | 415 × 416 (se muestra redonda) |
| `logo.png`, `icon.png` | Logo del menú móvil y de la barra lateral | |
| `favicon.ico` | Favicon | |
| `project-one/two/three.png` | Miniaturas de las tarjetas de proyecto | |
| `techshop-big.png`, `edumaster-big.png`, `quickbite-big.png` | Imagen grande del modal (`data-img` + `.png`) | |
| `project-details-1.png`, `project-details-2.png` | Galería del modal | |
| `blog-1…4.png`, `blog-details.png`, `blog-video.png`, `youtube.png` | Blog | |
| `arrow.png`, `arrow.svg` | Flecha decorativa | |
| `fb.png`, `tt.png`, `x.png`, `sp.png` | Iconos de redes en `.share` | |
