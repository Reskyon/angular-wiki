# Parte 5: La galería

> Esta versión pública conserva las explicaciones y omite fragmentos que reproducen o adaptan la plantilla comercial.

Esta parte construye la galería de trabajo creativo del portfolio: fotografías,
identidad corporativa, ilustraciones y diseño UI/UX, sin escribir un texto por
imagen. Parte de una carpeta de archivos y llega a una página con filtros, una
pantalla de carga que no deja huecos, un visor que se maneja con el teclado y
una entrada en la portada que la mantiene dentro del recorrido de lectura.
Cada módulo deja código real del repositorio y un error que costó encontrar: los
ocho títulos «Brand» que salían iguales, la imagen que sin JavaScript no se
veía, el visor que no se podía probar.

**Si llegaste aquí desde un buscador.** Esta página es una parte de la guía
«Cómo se construye este sitio», escrita sobre el repositorio de
janioisacura.com, un portfolio hecho con Angular y prerenderizado a HTML
estático. Lo que enseña (generar los datos de una galería a partir de una
carpeta de imágenes, una pantalla de carga con forma de la imagen
(*skeleton*), filtros accesibles y un visor modal con el foco bien manejado)
sirve para cualquier sitio Angular con muchas imágenes.

**Proyecto:** `content/en/gallery.yml`, `content/es/gallery.yml`,
`scripts/gallery-content.mjs`, `src/app/home/components/gallery-item/`,
`gallery-category/`, `gallery-viewer/` y `gallery-teaser/`, y
`src/app/home/pages/gallery-page/`.
**Sitio publicado:** la galería vive en `/en/gallery` y `/es/gallery`; aparece
en [janioisacura.com](https://janioisacura.com/en/gallery) (ya está publicada en
`main`) y en la portada. Para verla en local, `npm start` y abrir `/en/gallery`.
**Comportamiento:** el filtro elegido no se guarda en la dirección de la
página.

**Qué vas a aprender:**

- [Módulo G1](#módulo-g1-de-carpetas-a-datos): **De carpetas a datos.** Cómo una
  carpeta de imágenes y un archivo YAML pequeño producen los títulos, los
  grupos y los tamaños de 98 imágenes, y qué comprueba el build para que nada
  quede huérfano.
- [Módulo G2](#módulo-g2-la-pantalla-de-carga-skeleton): **La pantalla de carga.**
  Un recuadro del tamaño exacto de cada imagen que se ve incluso sin
  JavaScript, y los cuatro estados de una imagen que llega por la red.
- [Módulo G3](#módulo-g3-filtros-y-página): **Filtros y página.** Botones de
  filtro que se anuncian bien con un lector de pantalla, la ruta con carga
  perezosa y por qué los datos de la galería no van en el paquete principal.
- [Módulo G4](#módulo-g4-el-visor): **El visor.** Una ventana modal que toma el
  foco, lo devuelve, deja pasar solo el teclado que debe y por qué no usa la
  etiqueta `<dialog>`.
- [Módulo G5](#módulo-g5-la-entrada-en-la-portada): **La entrada en la portada.**
  Por qué la galería también es una sección de la portada, cómo se suma a la
  serie de «Siguiente capítulo» sin tocar el menú ni los contadores y por qué
  sus textos van en un módulo generado aparte.

Cada módulo sigue el mismo orden: el problema que resuelve, la decisión tomada
en este sitio, el procedimiento o el código completo, cómo funciona por
dentro, errores comunes y preguntas de entrevista con su respuesta.

Esta página es una parte de la guía [Cómo se construye este sitio](como-se-construye.md).
La anterior es la [Parte 4: Animaciones y fondo](04-animaciones.md); las imágenes
que alimentan esta galería se preparan con el procedimiento
[Agregar imágenes al portfolio](agregar-imagenes-al-portfolio.md). La siguiente es la
[Parte 6: Metadatos para compartir y buscadores](06-seo-y-vista-previa.md).

---

<!-- study-guide:section:gallery-g1-data -->
## Módulo G1: De carpetas a datos

Fuente: `content/en/gallery.yml`, `content/es/gallery.yml` y
`scripts/gallery-content.mjs`.

### El problema que resuelve

La galería tiene 98 imágenes. Cada una necesita un título, un grupo (si su
categoría tiene filtros) y su tamaño real para que el navegador reserve el
espacio. Escribir esos datos a mano, imagen por imagen, es trabajo que nadie
quiere hacer y que se queda desactualizado en cuanto agregas una foto.

### La decisión en este sitio

**La carpeta es la fuente de la verdad.** Las imágenes están en
`public/images/portfolio/<categoría>/` y el script lo deduce todo de ahí. El
archivo YAML solo lleva lo que **no** puede salir de una carpeta: el título de
cada categoría en cada idioma, la forma de las celdas de la cuadrícula y la
lista de grupos. El título de cada imagen sale de su nombre de archivo, y el
grupo, del principio de ese nombre.

### El código

El archivo en inglés (el español tiene los mismos identificadores con los
títulos traducidos):

```yaml
title: Gallery
teaser:
  subtitle: Photography, identity and illustration
  heading: Creative work, before and beyond code
  description: >-
    My path started in graphic design, and the habit of looking carefully never
    left. This gallery brings together some of that creative work over the
    years: photographs I took as an amateur, corporate identity, digital
    illustration, UI/UX design and social media campaigns. Come in and take a
    look.
  cta: Visit the gallery
  cover: /images/portfolio/photography/architecture-monument.webp
  coverAlt: Stone column topped with a bull, against a deep blue sky
categories:
  - id: branding
    title: Corporate identity
    ratio: '1 / 1'
  - id: illustration
    title: Digital illustration
    ratio: '1 / 1'
  - id: photography
    title: Photography
    ratio: '3 / 2'
    groups:
      - { id: architecture, title: Architecture }
      - { id: food-n-drink, title: Food & drink }
      - { id: landscape, title: Landscape }
      - { id: light, title: Light }
      - { id: nature, title: Nature }
      - { id: object, title: Objects }
      - { id: people, title: People }
  - id: web-ui-ux
    title: Web and UI/UX design
    ratio: '4 / 3'
```

Y lo que decide el título y el grupo de una imagen, en `gallery-content.mjs`:

```js
        if (!isText(title)) fail(`${where}: "titles" entry "${slug}" must be a non-empty string.`)
      }
    }
  }
  return data
}

// Turns a slug into a display title: the group prefix and the order number are
// dropped, hyphens become spaces, each word starts with a capital, and a trailing
// counter stays as a plain number so titles stay different:
// "landscape-sunset001" -> "Sunset 1", "0001-muhamad-ali" -> "Muhamad Ali".
// When nothing but a counter is left ("food-n-drink-001"), the group title leads.
// A title that comes out wrong is fixed with "titles" in gallery.yml.
export function titleFromSlug(slug, group) {
  let rest = group ? slug.slice(group.id.length + 1) : slug
  rest = rest.replace(/^\d+-/, '')
  const counter = /^(.*?)-?(\d+)$/.exec(rest)
  const words = (counter ? counter[1] : rest)
    .split('-')
    .filter(Boolean)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
  const label = words || (group?.title ?? '')
  if (!counter) return label || slug
  return `${label} ${Number(counter[2])}`.trim()
}
```

### Cómo funciona por dentro

- **El grupo es un prefijo.** `landscape-sunset001` pertenece a `landscape`
  porque su nombre empieza por ese identificador seguido de un guion. Si un
  identificador tiene guiones (`food-n-drink`), gana el más largo que
  coincida.
- **El título sale del nombre.** Se quitan el grupo y el número de orden,
  los guiones pasan a espacios y cada palabra empieza en mayúscula:
  `0001-muhamad-ali` es «Muhamad Ali». Si el nombre termina en un número, se
  conserva como número: `landscape-sunset001` es «Sunset 1».
- **El tamaño viene del archivo.** Para una imagen WebP lo lee `sharp` (una
  librería de Node que procesa imágenes); para un SVG, de su atributo
  `viewBox`. Los originales ya no existen en el repositorio, así que solo se
  puede medir lo que se publica.
- **Un título que sale mal se corrige en el YAML**, sin renombrar el archivo:
  cada categoría admite un mapa opcional `titles` con la forma
  `brand-01: Logo principal`.
- **El build comprueba todo antes de generar nada.** Falla, diciendo el
  archivo y el campo, si una carpeta no tiene categoría, si una categoría no
  tiene imágenes, si una imagen no coincide con ningún grupo, si un grupo se
  queda sin imágenes, si un título corregido nombra una imagen que no existe o
  si el español y el inglés describen cosas distintas.
- El resultado es un módulo TypeScript generado, `GALLERY`, con un objeto por
  idioma. Angular lo consume como cualquier otro dato del sitio.

### Errores comunes

- **Quitar el número final del título.** La primera especificación lo
  descartaba para que `landscape-sunset001` fuera «Sunset». Al repasar los
  datos reales se vio que las ocho piezas de identidad (`brand-01` a
  `brand-08`) quedarían todas como «Brand»: ocho títulos iguales, y también
  ocho textos alternativos iguales para un lector de pantalla. Por eso el
  número se conserva.
- **Olvidar el guion después del grupo.** `food-n-drink001` no coincide con el
  grupo `food-n-drink`, porque el separador es obligatorio. Se renombró a
  `food-n-drink-001`.
- **Agregar una carpeta sin declarar su categoría** en los dos archivos YAML. El
  build lo avisa con el nombre de la carpeta.
- **Aceptar un `viewBox` que no es un tamaño.** `0 0 0 100` y `0 0 . 100` cumplen
  el patrón pero dan ancho cero o un número inválido, que el JSON convierte en
  `null`. El visor calcula su tamaño con esos datos. Se exige que ancho y alto
  sean finitos y mayores que cero.
- **Leer imágenes con `sharp` en Windows y luego intentar borrarlas o
  reescribirlas.** `sharp` guarda un caché de archivos que deja el archivo
  bloqueado. El módulo lo apaga al cargarse (`sharp.cache(false)`).

### Preguntas de entrevista (senior)

#### 1. ¿Por qué el ancho y el alto de cada imagen están en los datos y no se leen en el navegador?

**Respuesta:**

Porque el navegador necesita esos números **antes** de descargar la imagen,
para reservar su espacio y no mover el contenido cuando llegue. Si se leyeran
al cargar, el dato llegaría tarde, que es justo lo que se quiere evitar. Calcularlos
en el build cuesta una vez y deja el HTML prerenderizado con `width` y `height`
correctos.

#### 2. ¿Por qué validar el contenido en el build y no en el componente?

**Respuesta:**

Un error de contenido (una imagen sin grupo, un idioma que no coincide con el
otro) es del autor, no del visitante. En el build se detecta antes de publicar,
con el archivo y el campo en el mensaje. En el componente solo se descubriría
cuando alguien visite la página, y el visitante no puede arreglarlo.

#### 3. ¿Por qué el grupo de una imagen sale del prefijo de su nombre y no de un campo por imagen?

**Respuesta:**

Porque agregar una foto debe ser copiar un archivo y ejecutar un comando, sin
editar nada más. Un campo por imagen obliga a tocar el YAML en cada foto y se
desincroniza con facilidad. El precio es una convención de nombres, que el
build comprueba: una imagen que no sigue la convención no llega a publicarse.

<!-- /study-guide:section:gallery-g1-data -->

---

<!-- study-guide:section:gallery-g2-skeleton -->
## Módulo G2: La pantalla de carga (skeleton)

Fuente: `src/app/home/components/gallery-item/`.

### El problema que resuelve

Cada imagen es un archivo de hasta 1800 px. Mientras llega, su celda está en
blanco, y quien visita no sabe si la conexión es lenta o si la foto no existe.
Y si la celda no reserva su tamaño, todo lo que hay debajo salta cada vez que
carga una imagen (lo que se llama desplazamiento de diseño, *layout shift*), y
el lector pierde el punto donde estaba.

### La decisión en este sitio

Una pantalla de carga con la **forma exacta** de la imagen: un recuadro gris con
una banda de luz que lo cruza. Reserva el espacio con `aspect-ratio` y se queda
**detrás** de la imagen, así que funciona incluso sin JavaScript. No hace nada
más rápido: la descarga es la misma. Solo cambia lo que se ve mientras tanto. El
peso lo cuidan la carga diferida (`loading="lazy"`) y el tamaño del archivo.

### El código

```ts
import {
  afterNextRender,
  Component,
  ElementRef,
  input,
  output,
  signal,
  viewChild,
} from '@angular/core'
import { GalleryImage } from '@interfaces/gallery.interface'

// 'pending' is the server render and the moment before hydration: the browser loads the
// image by itself and the CSS skeleton shows until it is painted. Once the page is
// interactive the state is 'loading' until the file arrives, then 'loaded' or 'error'.
type ImageState = 'pending' | 'loading' | 'loaded' | 'error'

// One cell of the grid: a button with the image on top of a skeleton. The cell reserves
// its shape from the category ratio, so nothing moves while images arrive.
@Component({
  selector: 'home-gallery-item',
  templateUrl: './gallery-item.component.html',
  styleUrl: './gallery-item.component.scss',
})
export class GalleryItemComponent {
  readonly image = input.required<GalleryImage>()
  /** Shape of the cell, a CSS aspect-ratio such as "3 / 2". */
  readonly ratio = input.required<string>()
  /** Above the fold: the browser loads it right away instead of waiting to see it scroll near. */
  readonly eager = input(false)
  /** The button that was activated, so the page can give it the focus back. */
  readonly selected = output<HTMLElement>()

  private readonly picture = viewChild.required<ElementRef<HTMLImageElement>>('picture')
  protected readonly state = signal<ImageState>('pending')
  // True only when the file arrived after the page was interactive: that is the one case
  // that fades in. An image the browser already had must not blink.
  protected readonly arrivedLate = signal(false)

  constructor() {
    afterNextRender(() => {
      const element = this.picture().nativeElement
      // A file the browser already has (a second visit, an image seen in the viewer) is
      // complete before hydration: skip the skeleton so there is no flicker.
      if (element.complete) this.state.set(element.naturalWidth > 0 ? 'loaded' : 'error')
      else this.state.set('loading')
    })
  }

  protected onLoad() {
    this.arrivedLate.set(this.state() === 'loading')
    this.state.set('loaded')
  }

  protected onError() {
    this.state.set('error')
  }
}
```

La plantilla:


Y los estilos:


### Cómo funciona por dentro

- **El recuadro vive detrás de la imagen.** En el HTML prerenderizado ya están
  la `<img>` y el recuadro. El navegador no pinta la imagen hasta que llega, y
  mientras tanto se ve el recuadro; cuando llega, la imagen lo tapa. Sin
  JavaScript, eso es todo.
- **Cuatro estados.** `pending` es el servidor y el momento antes de que
  Angular tome el control: el navegador lo resuelve solo. Ya con la página
  activa pasa a `loading` mientras llega el archivo, y de ahí a `loaded` o
  `error`.
- **`complete` evita el parpadeo.** Si el navegador ya tiene la imagen (una
  segunda visita, o la que acabas de ver en el visor), `img.complete` es
  verdadero antes de que Angular tome el control. Se salta la pantalla de carga
  y no hay un destello.
- **La imagen nunca queda oculta por un estado.** Se pinta en cuanto el
  navegador la tiene. El desvanecido (`is-fresh`) solo se reproduce cuando el
  archivo llega después de que la página ya estaba activa; una imagen que ya
  estaba allí no parpadea.
- **Lo que está a la vista no espera.** La primera categoría de la página se
  descarga sin diferir (`loading="eager"`), porque ya está en pantalla al
  entrar. El resto sigue siendo diferido.
- **El interruptor de animaciones lo apaga sin código extra.** La regla global
  de `_base.scss` deja las animaciones en 0,01 ms y quita las transiciones. El
  recuadro queda plano y la imagen aparece de golpe.
- **Un archivo roto no rompe la cuadrícula.** En `error` el brillo se detiene y
  la celda muestra el título de la imagen.

### Errores comunes

- **Ocultar la imagen hasta recibir su evento `load`.** La primera versión la
  dejaba transparente mientras el estado era `loading`. Si ese evento se
  pierde (llega antes de que Angular tome el control, o el navegador tarda en
  pintar la ventana), una imagen que ya está cargada se queda invisible y la
  celda parece vacía. Un estado no debe poder esconder un archivo que ya
  llegó: ahora la imagen siempre es visible y el estado solo mueve el
  recuadro de carga y el desvanecido.
- **Diferir lo que ya está a la vista.** `loading="lazy"` espera a que el
  navegador decida que la imagen se acerca; con la ventana sin foco puede tardar.
  Para lo que aparece al entrar, mejor `eager`.
- **No reservar el tamaño.** Sin `aspect-ratio` la celda mide cero hasta que
  llega la imagen, y todo se mueve.
- **Olvidar la imagen que ya estaba en caché.** Sin la comprobación de
  `complete`, esa imagen pasa por `loading` y hace un destello de recuadro y
  desvanecido que no tiene sentido.
- **Dar a la imagen un texto alternativo vacío dentro de un botón.** El botón
  quedaría sin nombre. Aquí el `alt` es el título de la imagen y es lo que
  anuncia el lector de pantalla.

### Preguntas de entrevista (senior)

#### 1. ¿Un *skeleton* hace que la página cargue más rápido?

**Respuesta:**

No. La descarga tarda lo mismo. Lo que cambia es la **percepción** y la
estabilidad: la pantalla no queda en blanco y nada se mueve cuando llegan los
datos. Para cargar menos se usan otras herramientas: la carga diferida, un
formato más ligero (WebP) y un tamaño de archivo adecuado.

#### 2. ¿Por qué `loading="lazy"` y `decoding="async"`?

**Respuesta:**

`loading="lazy"` hace que el navegador descargue solo las imágenes que se
acercan a la pantalla, así que una galería de 98 imágenes no baja todo de
golpe. `decoding="async"` permite que decodificar la imagen no bloquee el hilo
principal. Juntas hacen que entrar a la página sea barato y que las imágenes
aparezcan mientras haces scroll.

#### 3. ¿Cómo pruebas una imagen que "ya estaba en caché" si en tu entorno de pruebas no hay red?

**Respuesta:**

Se simula la propiedad. `complete` y `naturalWidth` son lecturas de la imagen;
una prueba las sustituye con valores fijos (con un espía sobre el prototipo de
`HTMLImageElement`) antes de crear el componente y comprueba que salta el
estado `loading`. Otra prueba dispara a mano los eventos `load` y `error` para
los otros caminos.

<!-- /study-guide:section:gallery-g2-skeleton -->

---

<!-- study-guide:section:gallery-g3-filters -->
## Módulo G3: Filtros y página

Fuente: `src/app/home/components/gallery-category/`,
`src/app/home/pages/gallery-page/` y `src/app/app.routes.ts`.

### El problema que resuelve

Fotografía tiene 52 imágenes. Todas seguidas son una pared larga. Hace falta
poder quedarse solo con la arquitectura o solo con la naturaleza, sin que la
página recargue y de forma que un lector de pantalla sepa qué pasó. Además, la
galería pesa en datos (98 imágenes en dos idiomas) y no debe engordar la
página de inicio.

### La decisión en este sitio

- **Cada categoría es un componente** con su título, sus botones de filtro (solo
  si declara grupos) y su cuadrícula. Los botones son los grupos y, al final,
  «Todas». La categoría abre en su **primer** grupo (Arquitectura en
  fotografía), para no cargar las 52 fotos de golpe; el botón activo es negro con
  el amarillo del sitio en el texto. Activar filtros en otra categoría no
  requiere tocar el componente: basta con declarar `groups` en el YAML.
- **Los filtros son botones que se pulsan y se sueltan** (`aria-pressed`), no
  enlaces ni pestañas. Una región con `aria-live="polite"` avisa cuántas
  imágenes quedan.
- **Las imágenes viven en una página aparte**, `/en/gallery` y `/es/gallery`:
  98 imágenes en la portada la harían pesada. La portada tiene una entrada que
  la enlaza (el [Módulo G5](#módulo-g5-la-entrada-en-la-portada)).
- **Los datos se cargan solo cuando se visita la página.** El título de la ruta
  sale de una función que importa los datos bajo demanda.

### El código

La categoría:

```ts
import { Component, computed, input, linkedSignal, output } from '@angular/core'
import { GalleryImage, GalleryCategory } from '@interfaces/gallery.interface'
import { GalleryLabels } from '@home/constants/gallery-labels.constants'
import { GalleryItemComponent } from '../gallery-item/gallery-item.component'

/** What the page needs to open the viewer: the images on screen, the one clicked and its button. */
export interface ViewerRequest {
  images: GalleryImage[]
  index: number
  /** The cell to give the focus back to when the viewer closes. */
  opener: HTMLElement
}

// One category: its title, the filter buttons (only when it declares groups) and the grid.
@Component({
  selector: 'home-gallery-category',
  imports: [GalleryItemComponent],
  templateUrl: './gallery-category.component.html',
  styleUrl: './gallery-category.component.scss',
})
export class GalleryCategoryComponent {
  readonly category = input.required<GalleryCategory>()
  readonly labels = input.required<GalleryLabels>()
  /** The first category of the page is above the fold: its images are not deferred. */
  readonly eager = input(false)
  readonly opened = output<ViewerRequest>()

  /**
   * Id of the group being shown, or null for all of them. A category with groups starts on its
   * first one, so the page does not open with every image at once; "All" is the last button.
   */
  protected readonly activeGroup = linkedSignal<string | null>(
    () => this.category().groups?.[0]?.id ?? null,
  )
  protected readonly headingId = computed(() => `gallery-${this.category().id}`)

  protected readonly filters = computed(() => {
    const { groups = [], images } = this.category()
    return groups.map((group) => ({
      ...group,
      count: images.filter((image) => image.group === group.id).length,
    }))
  })

  protected readonly visible = computed(() => {
    const { images } = this.category()
    const group = this.activeGroup()
    return group === null ? images : images.filter((image) => image.group === group)
  })

  protected select(group: string | null) {
    this.activeGroup.set(group)
  }

  // The viewer walks through what is on screen, so a filter also limits the arrows.
  protected open(index: number, opener: HTMLElement) {
    this.opened.emit({ images: this.visible(), index, opener })
  }
}
```


La página, que guarda el visor y a quién devolver el foco:

```ts
import { Component, inject, signal } from '@angular/core'
import { ActivatedRoute, RouterLink } from '@angular/router'
import { GALLERY_CATALOG } from '@home/constants/gallery.constants'
import { GALLERY_LABELS } from '@home/constants/gallery-labels.constants'
import { SectionTitleComponent } from '@shared/components/section-title/section-title.component'
import { Locale } from '@shared/interfaces/shared.interface'
import {
  GalleryCategoryComponent,
  ViewerRequest,
} from '../../components/gallery-category/gallery-category.component'
import { GalleryViewerComponent } from '../../components/gallery-viewer/gallery-viewer.component'

// The gallery page: every category with its grid, and the viewer over the page.
@Component({
  selector: 'home-gallery-page',
  imports: [RouterLink, SectionTitleComponent, GalleryCategoryComponent, GalleryViewerComponent],
  templateUrl: './gallery-page.component.html',
  styleUrl: './gallery-page.component.scss',
})
export class GalleryPageComponent {
  private readonly route = inject(ActivatedRoute).snapshot
  protected readonly locale = this.route.data['locale'] as Locale
  protected readonly gallery = inject(GALLERY_CATALOG)[this.locale]
  protected readonly labels = GALLERY_LABELS[this.locale]

  protected readonly viewer = signal<ViewerRequest | null>(null)
  // The cell that opened the viewer gets the focus back when it closes. It comes with the
  // request instead of being read from the focused element: a click can activate a button
  // without focusing it (Safari does not), and then the focus would be somewhere else.
  private opener: HTMLElement | null = null

  protected open(request: ViewerRequest) {
    this.opener = request.opener
    this.viewer.set(request)
  }

  protected move(index: number) {
    this.viewer.update((request) => request && { ...request, index })
  }

  protected close() {
    this.viewer.set(null)
    this.opener?.focus()
    this.opener = null
  }
}
```

Y la ruta, con el título que carga los datos bajo demanda:

```ts
// The title comes from the generated gallery, loaded on demand so its data stays out of the
// main bundle.
const galleryTitle: ResolveFn<string> = async (route) => {
  const { GALLERY } = await import('@generated/gallery')
  return `${GALLERY[route.data['locale'] as Locale].title} | Janio Isacura`
}
```

```ts
    {
      path: `${locale}/gallery`,
      title: galleryTitle,
      data: { locale, description: GALLERY_LABELS[locale].description },
      resolve: { pageMetadata: setPageMetadata },
      loadComponent: () =>
        import('@home/pages/gallery-page/gallery-page.component').then(
          (module) => module.GalleryPageComponent,
        ),
    },
```

### Cómo funciona por dentro

- **El grupo elegido es un `linkedSignal`.** Empieza en el primer grupo de la
  categoría y el visitante lo cambia al pulsar; si la categoría cambiara, volvería a su
  valor inicial. Una señal normal no puede nacer de una entrada
  (`input`) porque todavía no tiene valor al crearse.
- **`visible` es un valor derivado** (`computed`): depende del grupo elegido
  y de las imágenes de la categoría, y se recalcula solo cuando cambia alguno.
  El `@for` repinta únicamente las celdas que entran o salen, gracias a
  `track image.slug`.
- **El visor recibe lo que está en pantalla.** Al abrirlo se le pasa la lista
  filtrada, así que las flechas también respetan el filtro.
- **La carga diferida son dos cosas.** `loadComponent` separa el componente de la
  página en su propio paquete. Y la función del título hace un `import()`
  dinámico de los datos generados, que viven en otro paquete aparte: si la
  ruta los importara de forma estática, los 98 registros irían en el paquete
  principal que descarga toda la gente que visita la portada.
- **La página tiene un `<h1>` y las categorías son `<h2>`.** El título de sección
  de la portada es un `<h2>`; aquí es lo primero de la página, así que el
  componente admite un nivel (`level`, 1 o 2), y las categorías, que son
  secciones de la página, pasan a `<h2>` justo debajo. Saltar de `<h1>` a `<h3>`
  deja un hueco en el esquema que usan los lectores de pantalla.
- **Una página nueva empieza arriba.** El router de este sitio no restaura
  posiciones, así que entrar a la galería desde la portada ya desplazada la
  dejaba en el mismo desplazamiento. El inicializador de scroll lleva al tope toda
  navegación a otra página sin fragmento (no la primera carga, ni el historial,
  ni el cambio de idioma que pide conservar la posición). Sigue las páginas con
  `NavigationEnd` y no con `Scroll`, porque con hidratación el router no emite
  `Scroll` en la primera navegación. El enlace de volver
  apunta a `#gallery`, para caer en la sección y no en el inicio.
- **El idioma sale de la ruta**: la página lo lee de los datos de la ruta, y el
  cambio de idioma conserva el resto de la dirección (`/en/gallery` pasa a
  `/es/gallery`).

### Errores comunes

- **Saltarse un nivel de encabezado.** Un `<h1>` seguido de `<h3>`. Las
  categorías son `<h2>`.
- **Una página sin `<h1>`.** Lectores de pantalla y buscadores esperan uno.
  Reutilizar el título de sección tal cual deja la página sin encabezado
  principal, porque ese componente pinta un `<h2>`.
- **Importar los datos generados en el archivo de rutas.** Funciona, pero los
  datos pasan a formar parte del paquete inicial. El título con `import()` los
  deja fuera.
- **Filtrar con `display: none` en una lista fija.** Se descargan imágenes que
  el visitante no ve y las celdas ocultas siguen en el orden de tabulación.
  Aquí se quitan del DOM.
- **Abrir con «Todas».** Con 52 fotos, la categoría arranca descargando
  muchas más de las que se ven. Abrir en el primer grupo reparte el trabajo.
- **Olvidar anunciar el cambio.** Un filtro que cambia la página sin avisar es
  mudo para quien usa un lector de pantalla.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué `aria-pressed` y no `role="tab"` o botones de radio para los filtros?

**Respuesta:**

Porque cada botón es un interruptor sobre el mismo contenido: pulsar uno lo
activa y suelta el anterior, y la página es la misma. Las pestañas cambian entre
paneles distintos y piden una navegación con flechas; los botones de radio son
para formularios. `aria-pressed` dice la verdad de un botón que se queda
pulsado, y se maneja con Tab, Intro y Espacio sin trabajo extra.

#### 2. ¿Qué pasa con el tamaño del paquete inicial si importas datos generados en el archivo de rutas?

**Respuesta:**

Que se incluyen en el paquete que descarga todo el mundo, aunque nunca visite
esa ruta. Para una página lejana y grande, conviene separarlos: el componente con
`loadComponent`, y cualquier dato que use una función de la ruta (como el
título) con un `import()` dinámico dentro de la función. El presupuesto del
paquete inicial del repositorio (600 kB) es la alarma que avisa cuando un cambio
lo desordena.

#### 3. ¿Por qué `track image.slug` en el `@for` y no el índice?

**Respuesta:**

Con el índice, al filtrar, la celda 0 pasa a mostrar otra imagen y Angular
reutiliza el componente, con el estado de carga de la imagen anterior. Con un
identificador estable (el `slug`), Angular conserva la celda de cada imagen y
solo agrega o quita las que cambian, así que una imagen ya cargada no vuelve a
mostrar la pantalla de carga.

<!-- /study-guide:section:gallery-g3-filters -->

---

<!-- study-guide:section:gallery-g4-viewer -->
## Módulo G4: El visor

Fuente: `src/app/home/components/gallery-viewer/`.

### El problema que resuelve

Una miniatura recortada no muestra la foto. El visor abre la imagen completa
sobre la página. Una ventana así tiene reglas que, si faltan, la hacen
inutilizable para parte de la gente: el foco tiene que entrar en ella, no debe
escaparse al contenido de atrás, hay que poder salir con el teclado, y al
cerrar, el foco tiene que volver a donde estaba.

### La decisión en este sitio

- **Es un `div` con `role="dialog"` y `aria-modal="true"`**, no la etiqueta
  `<dialog>`. La etiqueta haría casi todo sola (`showModal()` pone el foco y
  cierra con Escape), pero el entorno de pruebas del proyecto (jsdom) no la
  implementa, así que no se podría probar. Un componente que no se prueba es un
  componente que se rompe sin avisar.
- **Recorre lo que se ve.** Recibe la lista filtrada, así que
  las flechas respetan el filtro, y da la vuelta en los extremos.
- **Descarga a las vecinas por adelantado**, para que pasar de una imagen a la
  siguiente sea inmediato.

### El código

```ts
import {
  afterNextRender,
  Component,
  computed,
  DestroyRef,
  DOCUMENT,
  effect,
  ElementRef,
  inject,
  input,
  output,
  viewChild,
} from '@angular/core'
import { GalleryImage } from '@interfaces/gallery.interface'
import { GalleryLabels, galleryPosition } from '@home/constants/gallery-labels.constants'
import { Locale } from '@shared/interfaces/shared.interface'

// Full-size view of one image, over the page. It is a plain dialog and not <dialog>.showModal()
// so it behaves the same everywhere and can be tested: it takes the focus, keeps Tab inside,
// closes with Escape or a click outside the image, and walks through the images with the
// arrow keys. The page gives the focus back to the cell that opened it.
@Component({
  selector: 'home-gallery-viewer',
  templateUrl: './gallery-viewer.component.html',
  styleUrl: './gallery-viewer.component.scss',
  host: { '(document:keydown)': 'onKeydown($event)' },
})
export class GalleryViewerComponent {
  readonly images = input.required<GalleryImage[]>()
  readonly index = input.required<number>()
  readonly labels = input.required<GalleryLabels>()
  readonly locale = input.required<Locale>()
  readonly closed = output<void>()
  /** Index of the image to show next. */
  readonly moved = output<number>()

  private readonly host = inject<ElementRef<HTMLElement>>(ElementRef)
  private readonly closeButton = viewChild.required<ElementRef<HTMLButtonElement>>('closeButton')

  protected readonly image = computed(() => this.images()[this.index()])
  protected readonly many = computed(() => this.images().length > 1)
  protected readonly position = computed(() =>
    galleryPosition(this.locale(), this.index() + 1, this.images().length),
  )

  // What the live region says each time the image changes: its title and its position.
  protected readonly announcement = computed(() =>
    this.many() ? `${this.image().title}, ${this.position()}` : this.image().title,
  )

  constructor() {
    // The page behind the viewer must not scroll while it is open.
    const root = inject(DOCUMENT).documentElement
    const previousOverflow = root.style.overflow
    root.style.overflow = 'hidden'
    inject(DestroyRef).onDestroy(() => (root.style.overflow = previousOverflow))

    afterNextRender(() => this.closeButton().nativeElement.focus())

    // Download the neighbours ahead of the arrows so moving between images feels instant.
    effect(() => {
      const images = this.images()
      for (const offset of [-1, 1]) {
        const neighbour = images[(this.index() + offset + images.length) % images.length]
        if (neighbour && neighbour !== this.image()) new Image().src = neighbour.src
      }
    })
  }

  protected previous() {
    this.moved.emit((this.index() - 1 + this.images().length) % this.images().length)
  }

  protected next() {
    this.moved.emit((this.index() + 1) % this.images().length)
  }

  protected onKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      this.closed.emit()
    } else if (event.key === 'ArrowLeft' && this.many()) {
      this.previous()
    } else if (event.key === 'ArrowRight' && this.many()) {
      this.next()
    } else if (event.key === 'Tab') {
      this.keepFocusInside(event)
    }
  }

  // Tab and Shift+Tab loop over the viewer's buttons instead of reaching the page behind.
  private keepFocusInside(event: KeyboardEvent) {
    const buttons = [...this.host.nativeElement.querySelectorAll<HTMLElement>('button')]
    if (buttons.length === 0) return
    const first = buttons[0]
    const last = buttons[buttons.length - 1]
    const active = this.host.nativeElement.ownerDocument.activeElement
    if (event.shiftKey && active === first) {
      event.preventDefault()
      last.focus()
    } else if (!event.shiftKey && active === last) {
      event.preventDefault()
      first.focus()
    } else if (!buttons.includes(active as HTMLElement)) {
      event.preventDefault()
      first.focus()
    }
  }
}
```

Cómo se reparte el tamaño. La figura toma su ancho de los datos de la imagen
(`--w` y `--ratio`, puestos en la plantilla):


El principio de la plantilla (los tres botones con sus iconos siguen el mismo
patrón y se omiten):


### Cómo funciona por dentro

- **El foco entra y sale.** Al abrirse, el botón «Cerrar» toma el foco. La celda
  que se pulsó viaja con la petición de abrir (`opener`) y la página se lo
  devuelve al cerrar. No se lee de `document.activeElement`: un clic puede
  activar un botón sin enfocarlo (Safari no enfoca los botones al pulsarlos) y
  entonces el foco estaría en otro control.
- **Las flechas se anuncian.** El pie con el título y la posición está oculto a
  los lectores de pantalla (`aria-hidden`) y una región con `aria-live="polite"`,
  siempre presente, dice «título, 3 / 18» cada vez que cambia la imagen. El foco
  se queda en el botón que se está usando.
- **Tab no se escapa.** Con Tab en el último botón el foco pasa al primero, y
  con Mayús+Tab en el primero, al último. Sin eso, el teclado llegaría al
  contenido que está tapado detrás.
- **Un solo escuchador de teclado en el documento**, declarado en `host`:
  Escape cierra, las flechas mueven. Las flechas no hacen nada con una sola
  imagen.
- **Clic fuera cierra, clic dentro no.** Un clic en la zona oscura cierra; un
  clic sobre la imagen o los botones detiene la propagación (`stopPropagation`) para que no
  llegue a la zona oscura.
- **La página de atrás no se desplaza** mientras está abierto: el visor pone
  `overflow: hidden` en `<html>` al crearse y lo restaura al destruirse.
- **Las flechas dan la vuelta**: de la primera imagen, hacia atrás, va a la
  última, con una operación de módulo.

### Errores comunes

- **Cerrar el visor y dejar el foco perdido.** El teclado vuelve al principio de
  la página, y quien navega con él tiene que recorrerla de nuevo.
- **No restaurar el desplazamiento al cerrar.** Si el visor se destruye por otra
  vía (se cambia de ruta con él abierto), la página queda bloqueada. Por eso la
  restauración vive en `onDestroy` y no solo en el botón de cerrar.
- **Una flecha que mueve el visor sin comprobar cuántas imágenes hay.** Con una
  sola, la división del módulo no daría error, pero el visor haría ruido sin
  motivo; aquí no hace nada.
- **Dejar que la `<img>` se dimensione sola con un SVG.** Un SVG que solo
  tiene `viewBox` no trae un tamaño propio, así que con `width: auto` el navegador
  lo dibuja pequeño. Por eso el visor calcula el ancho a partir del ancho y la
  forma que ya están en los datos, y la imagen solo llena la figura.
- **Un clic en la imagen que cierra el visor.** Es la queja más frecuente de un
  visor mal hecho: se quiere ver la imagen, no cerrarla sin querer.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué no usar la etiqueta `<dialog>`, si ya hace casi todo?

**Respuesta:**

Es la mejor opción cuando se puede probar. Maneja el foco, el Escape y el fondo
bloqueado. Aquí el entorno de pruebas no la implementa por completo, y un visor
que no se prueba pierde sus garantías (el foco, la trampa de Tab, las flechas)
en cuanto alguien toca el código. La decisión fue un `div` accesible y
probado, y reconsiderarlo cuando las pruebas corran en un navegador real.

#### 2. ¿Qué es una trampa de foco (*focus trap*) y por qué es necesaria en una ventana modal?

**Respuesta:**

Es hacer que Tab y Mayús+Tab circulen solo dentro de la ventana. Una ventana
modal tapa el resto de la página: si el foco pudiera salir, quien usa teclado o
lector de pantalla estaría interactuando con controles que no ve. La trampa
recoge los botones del visor y, al llegar al último o al primero, mueve el foco
al otro extremo.

#### 3. ¿Cómo se prueba que el visor devuelve el foco a quien lo abrió?

**Respuesta:**

Con la página real: se deja el foco en otro control (el enlace de volver), se
hace clic en una celda **sin enfocarla antes** y se cierra con Escape; entonces se
comprueba que `document.activeElement` es esa celda. Se prueba en la página y no
en el visor, porque quien devuelve el foco es la página. El caso sin enfoque previo
importa: es justo el que falla si el elemento se lee de `document.activeElement`.

<!-- /study-guide:section:gallery-g4-viewer -->

---

<!-- study-guide:section:gallery-g5-teaser -->
## Módulo G5: La entrada en la portada

Fuente: `src/app/home/components/gallery-teaser/`,
`src/app/shared/constants/sections.constants.ts`,
`src/app/shared/animations/choreography.ts` y `content/en/gallery.yml`.

### El problema que resuelve

La portada se lee de arriba abajo, y al final de cada sección hay un enlace
«Siguiente capítulo» con un contador (01/07, 02/07...). Una galería que solo
existe en el menú rompe ese hilo: la serie salta de Proyectos a Contacto, la
numeración queda alterada y quien llega leyendo nunca se entera de que hay una
galería. Es una inconsistencia de experiencia, no de código.

### La decisión en este sitio

- **La galería también es una sección de la portada**, entre Proyectos y
  Contacto, con la misma tarjeta que un proyecto: portada, título, texto y un
  botón que lleva a la página.
- **Un único lugar manda sobre las secciones.** La constante `SECTIONS` define
  el orden, el menú, los contadores y los enlaces al siguiente capítulo. Agregar
  `gallery` ahí corrige todo a la vez.
- **Los textos y la portada están en el YAML** (un bloque `teaser`), en los dos
  idiomas. La portada debe ser una de las imágenes de la propia galería, y el
  build lo comprueba.
- **Los textos de la entrada son un módulo generado aparte**, para que la
  portada no importe los 98 registros de la galería.

### El código

El bloque del YAML:

```yaml
teaser:
  subtitle: Photography, identity and illustration
  heading: Creative work, before and beyond code
  description: >-
    My path started in graphic design, and the habit of looking carefully never
    left. This gallery brings together some of that creative work over the
    years: photographs I took as an amateur, corporate identity, digital
    illustration, UI/UX design and social media campaigns. Come in and take a
    look.
  cta: Visit the gallery
  cover: /images/portfolio/photography/architecture-monument.webp
  coverAlt: Stone column topped with a bull, against a deep blue sky
```

La constante que ordena la portada, el menú y los contadores:

```ts
import { Section } from '@shared/interfaces/shared.interface'

// Homepage sections in reading order. The id is the `id` attribute of each
// <section> and the fragment of its navigation link.
export const SECTIONS: readonly Section[] = [
  { id: 'home', label: { en: 'Home', es: 'Inicio' } },
  { id: 'about', label: { en: 'About', es: 'Sobre mí' } },
  { id: 'skills', label: { en: 'Skills', es: 'Habilidades' } },
  { id: 'experience', label: { en: 'Experience', es: 'Experiencia' } },
  { id: 'projects', label: { en: 'Projects', es: 'Proyectos' } },
  { id: 'gallery', label: { en: 'Gallery', es: 'Galería' } },
  { id: 'contact', label: { en: 'Contact', es: 'Contacto' } },
]
```

El componente:

```ts
import { Component, computed, inject, input } from '@angular/core'
import { RouterLink } from '@angular/router'
import { GALLERY_TEASER_CATALOG } from '@home/constants/gallery-teaser.constants'
import { NextChapterComponent } from '@shared/components/next-chapter/next-chapter.component'
import { SectionTitleComponent } from '@shared/components/section-title/section-title.component'
import { Locale } from '@shared/interfaces/shared.interface'

// The gallery's place in the homepage reading order: after Projects and before Contact, with
// the same card as a project (cover, title, text) leading to the gallery page. Without it
// the gallery would be reachable from the menu only, and the "Next chapter" series would
// jump from Projects to Contact.
@Component({
  selector: 'home-gallery-teaser',
  imports: [RouterLink, SectionTitleComponent, NextChapterComponent],
  templateUrl: './gallery-teaser.component.html',
  styleUrl: './gallery-teaser.component.scss',
})
export class GalleryTeaserComponent {
  readonly locale = input.required<Locale>()
  private readonly catalog = inject(GALLERY_TEASER_CATALOG)

  protected readonly teaser = computed(() => this.catalog[this.locale()])
}
```


Y su entrada animada, junto a la de las tarjetas de proyecto:

```ts
  // Gallery: its card pops in like a project card. Its links accept Tab focus while it waits,
  // hidden, so the entrance also finishes when one of them is focused.
  const galleryCard = gsap.fromTo(
    '.gallery-card',
    { opacity: 0, scale: 0 },
    {
      ...VISIBLE,
      duration: 0.5,
      scrollTrigger: { trigger: '.gallery-card', start: 'top 80%', end: 'top 20%' },
    },
  )
  const galleryElement = document.querySelector<HTMLElement>('.gallery-card')
  const finishGalleryEntrance = () => galleryCard.progress(1)
  galleryElement?.addEventListener('focusin', finishGalleryEntrance, { once: true })
```

### Cómo funciona por dentro

- **El contador sale de la posición en `SECTIONS`.** Con `gallery` en la sexta
  posición, el enlace de Proyectos apunta a ella y el de la galería, a Contacto.
  El contador pasa de «x/06» a «x/07» sin tocar ninguno de los componentes.
- **La imagen se recorta a la forma de la tarjeta.** La portada es una foto
  vertical; con `object-fit: cover` y `object-position: center 20%` se ve la
  parte alta de la columna, que es lo que importa.
- **Dos enlaces al mismo destino.** La imagen (con su texto alternativo) y el
  botón. Los proyectos hacen lo mismo con la imagen y el título.
- **Los textos son un módulo propio**, `GALLERY_TEASER`, con su propio token de
  inyección en un archivo aparte. Si el token viviera junto a los datos de la
  galería, importar uno arrastraría al otro al paquete de la portada.
- **La animación termina al enfocar.** Los enlaces de la tarjeta aceptan Tab
  mientras la tarjeta espera, oculta, su disparador; por eso el evento
  `focusin` completa la entrada, igual que en los proyectos. Al revertir la
  coreografía se quita el oyente.

### Errores comunes

- **Agregar la sección solo al menú.** La serie de «Siguiente capítulo» queda
  alterada y la lectura de arriba abajo no llega a la galería.
- **Importar `GALLERY` en el componente de la portada.** La portada descargaría
  todos los datos de la galería aunque nadie la visite. Hay un módulo con los
  pocos textos que hacen falta.
- **Una portada que no es de la galería.** Si el archivo no existe o no se
  optimizó, la tarjeta sale rota. El build exige que sea una imagen de la
  galería.
- **Poner la portada sin texto alternativo.** El enlace de la imagen quedaría
  sin nombre. El YAML exige `coverAlt`.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué una sola constante para las secciones y no listas separadas en el menú y en cada enlace?

**Respuesta:**

Porque el orden de lectura es un dato, no un detalle de cada componente. Con
listas separadas hay que acordarse de tocar todas al agregar una sección, y una
se olvida: el menú muestra una cosa y los contadores otra. Con una constante, el
menú, los contadores y el siguiente capítulo se derivan de ella y no pueden
discrepar.

#### 2. ¿Por qué los textos de la entrada van en un módulo generado aparte de los de la galería?

**Respuesta:**

Por el tamaño del paquete inicial. Todo lo que importa la portada viaja en el
paquete que descarga cualquier visitante. Los datos de la galería (98 imágenes en
dos idiomas) solo hacen falta en su página, que se carga bajo demanda. La
entrada necesita seis textos: se generan por separado para no arrastrar el resto.

#### 3. La tarjeta tiene dos enlaces al mismo lugar. ¿Es un problema de accesibilidad?

**Respuesta:**

No necesariamente, si cada uno tiene un nombre que tenga sentido por separado:
la imagen se anuncia con su texto alternativo y el botón con su etiqueta. Es el
mismo patrón de las tarjetas de proyecto. La alternativa, para quitar la
repetición a quien usa lector de pantalla, es ocultar el enlace de la imagen
(`aria-hidden` y `tabindex="-1"`) y dejar solo el botón; se prefirió mantener la
coherencia con los proyectos.

<!-- /study-guide:section:gallery-g5-teaser -->

---

## Qué sigue en esta parte

- Guardar el filtro elegido en la dirección de la página (`?group=nature`), para
  que una recarga o un enlace conserven el filtro.
- Probar el visor en un navegador real, que permitiría reconsiderar la etiqueta
  `<dialog>`.
