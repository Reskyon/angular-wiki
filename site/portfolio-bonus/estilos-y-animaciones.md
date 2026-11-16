# Estilos y animaciones

> Esta versión pública conserva las explicaciones y omite fragmentos que reproducen o adaptan la plantilla comercial.

> Referencia de la plantilla original, no lista de funciones obligatorias del
> sitio. Consultar las [seis secciones elegidas](secciones-y-contenido.md#secciones-elegidas-para-el-mvp)
> y la [adaptación para el MVP](personalizacion.md): sin porcentajes de habilidades,
> formulario ni mapa. Sólo se trasladan los estilos y dependencias necesarios.
> El sitio publicado tiene hoy siete secciones: las seis del MVP más Galería.

Todo el aspecto de Portify sale de tres archivos SCSS y de un `app.js`. Esta
página explica los mecanismos que vale la pena conservar al reconstruir el
front: cómo se define el color, cómo se logran el grano, las ondas, los
títulos con línea, los números con contorno y las animaciones de scroll.

## Los archivos

| Archivo | Líneas | Qué tiene |
| --- | --- | --- |
| `src/assets/scss/bootstrap.scss` | 32 | Variables de Bootstrap (`$primary`, `$secondary`, radios y tamaños de botón, mapa de `$gutters` hasta 10) y el `@import "bootstrap/scss/bootstrap"` |
| `src/assets/scss/mixins.scss` | 13 | `@mixin min-width($breakpoint)`: un `@media (min-width)` con los *breakpoints* de Bootstrap (`sm`, `md`, `lg`, `xl`, `xxl`) |
| `src/assets/scss/styles.scss` | 2 524 | Todo lo demás, en el orden del índice que trae al inicio: reset, header, navegación, hero, una sección por bloque, componentes (`.next-chapter`, `.section-title`, ondas), utilidades, animaciones, modal y blog |

`styles.scss` empieza importando Poppins, `bootstrap.scss`, los iconos
Phosphor, el CSS de Swiper y el de GLightbox. Nada de Tailwind: los
utilitarios (`d-flex`, `gap-4`, `mb-3`…) son de Bootstrap.

En el sitio, estos tres archivos se tradujeron a la carpeta `src/styles/` de
Angular, con Bootstrap importado por partes: ver la
[Parte 2 de la guía de construcción](02-cimientos-de-estilo.md).

## Cómo se define el color

Bootstrap recibe los colores en tiempo de compilación:


Pero los estilos propios **no usan `$primary`**: usan variables CSS con el
color en forma de **tripleta RGB sin `rgb()`**:


La tripleta permite usar el mismo color con opacidad (`rgba(var(--black),
0.3)`), y cambiar `--primary` en tiempo de ejecución desde JavaScript, que es
lo que hace el selector de color. Los botones de Bootstrap (`btn-secondary`,
`btn-outline-secondary`) sí usan `$secondary` compilado: por eso un cambio de
paleta exige tocar los dos sitios.

Para nuestro front conviene mantener la idea (tokens como tripletas o, mejor,
colores `oklch`/hex en variables CSS) y declarar la paleta del logo en un solo
lugar. Lo implementado, y por qué se conservó la tripleta, está en el
[Módulo E3 de la Parte 2](02-cimientos-de-estilo.md#módulo-e3-tokens-de-color-como-tripletas-rgb).

## El selector de color

El engranaje flotante `.color-switcher` es una demo para el comprador. Lo que
hace cada control, en `app.js`:

- Cada `.color-btn` lleva `data-color="255, 219, 103"`. Al pulsarlo:
  `document.documentElement.style.setProperty("--primary", color)` y lo guarda
  en `localStorage` con la clave `bg`.
- `LTR`/`RTL` cambian `document.documentElement.dir` y lo guardan en la clave
  `dir`. El SCSS tiene reglas `&:dir(ltr)` / `&:dir(rtl)` para las líneas,
  los paddings y la posición del texto de fondo.
- *Grained BG* añade o quita la clase `grain` al `<div id="grain">`.

Al cargar, `app.js` lee las dos claves y las vuelve a aplicar.

## El grano


Es una capa fija sobre toda la página, con una imagen de ruido más grande que
la ventana que se desplaza a saltos (`steps(2)`) con `@keyframes noise`
(diez posiciones con `translate3d`). La imagen **se descarga de Wikimedia**:
en el front hay que servir una textura propia (un PNG pequeño o un SVG con
`feTurbulence`).

## Las ondas

Las ondas que rodean la foto del hero, los botones redondos y los números de
los servicios son cuatro `<span>` vacíos dentro de un contenedor absoluto:



Cada `span` es un círculo con sólo el borde superior (o inferior, en
`.waves-bottom`) que crece y se desvanece; los retardos escalonados dan la
sensación de ondas. Hay tres tamaños: `.waves-top`/`.waves-bottom` (hero),
`-md` (botones redondos de 132 px) y `-sm` (círculos de los servicios y fotos
de testimonios), que sólo cambian la duración y los retardos.

## El título de sección


La línea vertical de la izquierda empieza con altura 0 y GSAP la lleva a
`100%` cuando el título entra en pantalla:


El texto gigante `.section-title-overlay-text` (de 35 px en móvil a 160 px
en pantallas de 1800 px, `opacity: 0.05`, `position: absolute`) tiene un
efecto *parallax*: GSAP lo mueve de `y: 50%` a `y: -50%` mientras la sección
cruza la pantalla, con `scrub: true` (ligado al scroll, no al tiempo).

## Los números con contorno


El número se escribe tres veces; las dos copias de contorno van giradas y se
desplazan con el ratón (`mousemove` en `app.js`: `offsetX = (clientX - ancho/2) * 0.01`,
la primera copia a la mitad de ese desplazamiento). La tarjeta `.experience-card`
tiene además dos marcos (`::before` y `::after`) girados ±2,5° que se alinean
al pasar el ratón.

## Animaciones con GSAP

La versión construida en Angular (una coreografía central, el fondo de puntos y un
interruptor) está en la [Parte 4](04-animaciones.md); lo que sigue describe el
`app.js` original.

Todas están al final de `app.js`, dentro de `if (document.getElementById("about_me"))`
(sólo en la página principal). Las de entrada, sin ScrollTrigger:

| Elemento | Animación |
| --- | --- |
| `.nav-link` | Aparecen una a una (`stagger: 0.1`, `scale: 0`, `opacity: 0`) |
| `.img-wrapper` (foto) | Entra desde `scale: 1.5` con `ease: "back"` |
| `.work-btn`, `.contact-btn` | Rebotan desde `scale: 0` (`ease: "bounce"`) |
| `.freelancer`, `.description` | SplitType parte el texto en letras; cada letra gira (`rotateX: 180` / `rotateY: 180`) con `stagger: 0.05` |
| `.navigation` | `--height` de 0 a 100 % (la línea del menú) |

Las de scroll usan `scrollTrigger: { trigger, start: "top 60%", end: "top 20%" }`
(por defecto, se disparan cuando el elemento llega al 80 % de la altura de la
ventana): `.about-desc` (fade), `.experience-card` (elastic),
`.service-card` (suben desde `y: 500`), `.fun-fact`, `.experience-item`,
`.single-project`, `.process` (elastic de 2,8 s), `.testimonial-card`,
`.contact-item`, `.more-info`, `.download-cv`; más las dos líneas de la
experiencia (`--height` del wrapper y `--item-height` de cada ítem).

En RTL las animaciones de letras se sustituyen por un desplazamiento simple
(`y: 200, scale: 0`) porque SplitType no respeta la dirección.

## Observadores sin GSAP

Dos efectos usan `IntersectionObserver` directo:

- Los gráficos radiales de ApexCharts se crean cuando su `div` es visible al
  70 % (`threshold: 0.7`) y luego dejan de observarse. La configuración
  (`type: "radialBar"`, 250 × 250, `hollow.size: "80%"`, color negro,
  etiqueta `85%` a 44 px) está repetida tres veces en `app.js`.
- Las barras `.skill .progress-bar` empiezan con `width: 0` y reciben el
  `data-width` al 50 % de visibilidad.

## Lo que se puede reutilizar tal cual

- El SCSS de componentes (`.next-chapter`, `.section-title`, ondas, números,
  tarjetas, línea de tiempo) traducido a estilos por componente.
- Las variables CSS de color como tokens.
- Las configuraciones de Swiper y de ApexCharts (o su equivalente con un
  anillo SVG, que pesa mucho menos que ApexCharts).
- Las animaciones de GSAP, que funcionan igual en cualquier framework:
  GSAP es gratis desde 2025, incluidos los plugins.
