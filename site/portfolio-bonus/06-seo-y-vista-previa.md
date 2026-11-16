# Parte 6: Metadatos para compartir y buscadores

Esta parte construye lo que ve una persona cuando pega el enlace del sitio en
WhatsApp o LinkedIn, y lo que lee un buscador antes de decidir qué páginas
indexar. Parte de un problema concreto: el enlace se compartía con una
miniatura cuadrada diminuta y con el tipo de página equivocado. Llega a unas
etiquetas escritas desde Angular, una imagen pensada para recortes distintos,
una dirección canónica por página, un `robots.txt` y un `sitemap.xml`. Cada
módulo deja código real del repositorio y un error que costó encontrar: el
título que llegaba un paso tarde, la imagen que LinkedIn recorta por los
lados, el `Disallow` que no bloquea a nadie.

**Si llegaste aquí desde un buscador.** Esta página es una parte de la guía
«Cómo se construye este sitio», escrita sobre el repositorio de
janioisacura.com, un portfolio hecho con Angular y prerenderizado a HTML
estático. Lo que enseña (etiquetas Open Graph para las vistas previas, un
`TitleStrategy` de Angular que escribe las etiquetas con el título ya
resuelto, direcciones canónicas y de idioma (*hreflang*), páginas fuera del
índice, `robots.txt` y un `sitemap.xml` generado en el build) sirve para
cualquier sitio Angular con renderizado en el servidor o prerenderizado.

**Proyecto:** `src/app/shared/utils/seo.utils.ts`,
`src/app/shared/constants/site.constants.ts`,
`src/app/shared/services/seo-title-strategy.service.ts`,
`src/app/app.routes.ts`, `src/app/app.config.ts`,
`scripts/seo-content.mjs`, `public/robots.txt` y
`public/images/og-image.jpg`, con sus pruebas (`seo.utils.spec.ts`,
`seo-title-strategy.service.spec.ts`, `app.routes.spec.ts` y
`seo-content.test.mjs`).
**Sitio publicado:** [janioisacura.com](https://janioisacura.com/en/); si
abres el código fuente de la página (*view source*) o pegas el enlace en el
Post Inspector de LinkedIn, ves las etiquetas de esta parte.
Las vistas previas pueden conservar una imagen o un título anterior en caché.
El [módulo V6](#módulo-v6-comprobar-antes-y-después-de-publicar) explica cómo
comprobarlas después de publicar.

**Qué vas a aprender:**

- [Módulo V1](#módulo-v1-qué-lee-una-vista-previa): **Qué lee una vista previa.**
  Qué son las etiquetas Open Graph, cuáles escribe este sitio y por qué tienen
  que estar en el HTML que se sirve y no añadirse con JavaScript.
- [Módulo V2](#módulo-v2-la-imagen-para-compartir): **La imagen para compartir.**
  Tamaño, formato y peso de la imagen, cómo se hizo con el fondo de puntos del
  sitio y por qué LinkedIn la recorta por los lados.
- [Módulo V3](#módulo-v3-las-etiquetas-al-fijar-el-título): **Las etiquetas al
  fijar el título.** Por qué un `TitleStrategy` y no un manejador de
  `NavigationEnd`, y cómo escribe las etiquetas sin duplicarlas.
- [Módulo V4](#módulo-v4-canonical-idiomas-y-páginas-fuera-del-índice): **Canonical,
  idiomas y páginas fuera del índice.** La dirección única de cada página, las
  alternativas por idioma y cómo se aparta la página 404 del índice.
- [Módulo V5](#módulo-v5-robotstxt-y-sitemapxml): **`robots.txt` y `sitemap.xml`.**
  Qué pide cada archivo, por qué `Disallow` no es una puerta cerrada y cómo se
  genera el mapa del sitio en el build.
- [Módulo V6](#módulo-v6-comprobar-antes-y-después-de-publicar): **Comprobar antes
  y después de publicar.** Qué cubren las pruebas, cómo mirar el HTML
  construido y qué herramientas usar con el sitio ya publicado.

Cada módulo sigue el mismo orden: el problema que resuelve, la decisión tomada
en este sitio, el procedimiento o el código completo, cómo funciona por
dentro, errores comunes y preguntas de entrevista con su respuesta.

Esta página es una parte de la guía [Cómo se construye este sitio](como-se-construye.md).
La anterior es la [Parte 5: La galería](05-galeria.md), cuya página aparece en el
mapa del sitio de esta parte. Esta es, por ahora, la última parte.

---

<!-- study-guide:section:seo-v1-preview -->
## Módulo V1: Qué lee una vista previa

Fuente: `src/app/shared/utils/seo.utils.ts` y
`src/app/shared/constants/site.constants.ts`.

### El problema que resuelve

Cuando alguien pega un enlace en WhatsApp o LinkedIn, el programa descarga la
página, lee unas etiquetas del `<head>` y dibuja una tarjeta. Antes de esta
parte, el sitio no tenía esas etiquetas y el resultado fue malo en los dos
sitios:

- **WhatsApp** mostraba el título y la descripción, pero con una miniatura
  cuadrada pequeña. Sin una imagen declarada, tomó el icono de aplicación
  (`apple-touch-icon.png`, de 180 por 180 píxeles).
- **LinkedIn**, en su herramienta Post Inspector, eligió una imagen cualquiera
  de la página, avisó de que «The title should be between 15 and 250 characters
  long» (el título que leyó tenía 13 caracteres) y clasificó la página como
  artículo (*Article*).

El sitio no estaba roto: cada programa adivinaba porque nadie le había dicho
qué mostrar.

### La decisión en este sitio

**Declarar todo con Open Graph.** Open Graph es un conjunto de etiquetas
`<meta property="og:...">` que inventó Facebook y que hoy leen también
LinkedIn, WhatsApp y muchos más. Para que la tarjeta sea grande se añade
`twitter:card` con el valor `summary_large_image`; ese nombre viene de X
(antes Twitter), pero otros programas también lo entienden.

Las etiquetas que escribe el sitio:

| Etiqueta | Para qué sirve |
| --- | --- |
| `og:type` | El tipo de página; aquí siempre `website` |
| `og:site_name` | El nombre del sitio |
| `og:title` y `og:description` | Los textos de la tarjeta |
| `og:url` | La dirección de la página |
| `og:locale` | El idioma, en formato `idioma_TERRITORIO` (`en_US`, `es_ES`) |
| `og:image`, `og:image:width`, `og:image:height`, `og:image:alt` | La imagen, su tamaño y su texto alternativo |
| `twitter:card` | Pide la tarjeta grande |

**Las etiquetas tienen que estar en el HTML que se sirve.** Los programas que
generan vistas previas (los *crawlers*) leen la respuesta del servidor y casi
nunca ejecutan JavaScript. Si Angular añadiera las etiquetas en el navegador,
el crawler no las vería. Por eso el sitio es prerenderizado: Angular ejecuta la
aplicación al compilar y deja las etiquetas escritas en cada archivo `.html`.

### El código

Las constantes, en `site.constants.ts`:

```ts
import { Locale } from '@shared/interfaces/shared.interface'

// Keep in sync with SITE_URL in scripts/seo-content.mjs (the sitemap).
export const SITE_URL = 'https://janioisacura.com'
export const SITE_NAME = 'Janio Isacura'

export const OG_IMAGE = { path: '/images/og-image.jpg', width: 1200, height: 630 }

// Describe what the image shows, one sentence per language.
export const OG_IMAGE_ALT: Record<Locale, string> = {
  en: 'Janio Isacura | Software Engineer',
  es: 'Janio Isacura | Ingeniero de Software',
}

// Open Graph wants language_TERRITORY, not the bare code.
export const OG_LOCALE: Record<Locale, string> = { en: 'en_US', es: 'es_ES' }
```

La parte de `applySeo` que escribe las etiquetas Open Graph, en `seo.utils.ts`:

```ts
  const url = publicUrl(seo.path)
  const image = SITE_URL + OG_IMAGE.path
  const tags: MetaDefinition[] = [
    { property: 'og:type', content: 'website' },
    { property: 'og:site_name', content: SITE_NAME },
    { property: 'og:title', content: seo.title },
    { property: 'og:description', content: seo.description },
    { property: 'og:url', content: url },
    { property: 'og:locale', content: OG_LOCALE[seo.locale] },
    { property: 'og:image', content: image },
    { property: 'og:image:width', content: String(OG_IMAGE.width) },
    { property: 'og:image:height', content: String(OG_IMAGE.height) },
    { property: 'og:image:alt', content: OG_IMAGE_ALT[seo.locale] },
    { name: 'twitter:card', content: 'summary_large_image' },
  ]
  for (const tag of tags) meta.updateTag(tag)
```

### Cómo funciona por dentro

- **`Meta` es el servicio de Angular para las etiquetas `<meta>`.** Su método
  `updateTag` busca una etiqueta que ya exista y la cambia; si no existe, la
  crea. Para saber cuál buscar usa el atributo `name` y, cuando no hay `name`,
  usa `property`. Por eso `og:title` (que lleva `property`) y `twitter:card`
  (que lleva `name`) se escriben con la misma llamada.
- **Las direcciones son absolutas.** `og:image` lleva
  `https://janioisacura.com/images/og-image.jpg`, no `/images/og-image.jpg`.
  Quien genera la vista previa no sabe en qué sitio vive la etiqueta, así que
  una ruta relativa no le sirve.
- **El texto alternativo describe lo que se ve** y cambia con el idioma, igual
  que `og:locale`.
- **`MetaDefinition[]` evita un error de TypeScript.** Sin esa anotación,
  TypeScript infiere una unión de objetos donde unos tienen `name` y otros
  `property`, y no la acepta como argumento de `updateTag`. Escribir el tipo
  del arreglo lo resuelve.
- **Las herramientas para ver el resultado:** el *Post Inspector* de LinkedIn
  (pide iniciar sesión, solo abre direcciones públicas y actualiza su caché
  cada vez que pulsas «Inspect»); el *Sharing Debugger* de Facebook (lee las
  mismas etiquetas Open Graph que usa WhatsApp, y su botón «Scrape Again»
  fuerza una lectura nueva); y WhatsApp, que no tiene inspector: se comparte el
  enlace contigo mismo añadiendo un sufijo como `?v=2`, porque las vistas
  previas se guardan en caché y el mismo enlace mostraría la anterior.
- **El servidor de pruebas de este proyecto está detrás de Cloudflare Access**
  (un control de acceso que pide identificarse). Los crawlers no pueden
  entrar, así que las vistas previas solo se comprueban después de publicar en
  producción.

### Errores comunes

- **Esperar que el crawler ejecute JavaScript.** Una etiqueta añadida en el
  navegador no existe para él. Si el sitio no se prerenderiza ni se renderiza
  en el servidor, hay que generar el `<head>` en otro sitio.
- **Poner direcciones relativas** en `og:image` o `og:url`.
- **Usar `og:locale: en`.** El formato esperado es `en_US`, idioma y
  territorio.
- **Corregir las etiquetas y no ver cambios.** Casi siempre es una caché
  antigua, no un fallo (ver el Módulo V6).
- **No poner `twitter:card`.** Las tarjetas salen en formato pequeño en las
  plataformas que lo leen.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué las etiquetas de vista previa funcionan con un sitio prerenderizado y pueden fallar en una aplicación que se dibuja solo en el navegador?

**Respuesta:**

Porque quienes generan vistas previas leen el HTML que reciben y casi nunca
ejecutan JavaScript. En un sitio prerenderizado, las etiquetas ya están
escritas en el archivo que el servidor entrega. En una aplicación que solo se
dibuja en el navegador, el HTML inicial no las trae y un crawler que no ejecuta
JavaScript ve la página sin título ni imagen.

#### 2. ¿Qué diferencia hay entre `og:image` y el icono de aplicación, y qué pasa si no declaras la primera?

**Respuesta:**

`og:image` es la imagen pensada para la tarjeta al compartir; el icono de
aplicación (`apple-touch-icon`) es el que usa un móvil para el acceso directo.
Si no declaras `og:image`, cada programa decide por su cuenta: WhatsApp usó el
icono de 180 por 180 y LinkedIn tomó una imagen cualquiera de la página.
Declararla quita la adivinanza.

#### 3. ¿Por qué `og:locale` usa `en_US` y no `en`?

**Respuesta:**

El protocolo Open Graph define el formato `idioma_TERRITORIO`, así que un
valor como `en` no sigue la especificación. Las dos constantes del sitio
(`en_US` y `es_ES`) son una elección: no afirman que el contenido sea de un
país, solo usan el valor que el formato acepta.

<!-- /study-guide:section:seo-v1-preview -->

---

<!-- study-guide:section:seo-v2-image -->
## Módulo V2: La imagen para compartir

Fuente: `public/images/og-image.jpg` y `src/app/shared/animations/dots.ts`.

### El problema que resuelve

Una imagen para compartir se ve en lugares muy distintos: una tarjeta ancha en
LinkedIn, una miniatura en WhatsApp, una vista previa en un chat. Cada
plataforma tiene sus reglas de formato, de peso y de recorte. Una imagen mal
pensada sale cortada o ni aparece.

### La decisión en este sitio

**Una sola imagen de 1200 por 630 píxeles**, una proporción de 1,91 a 1, que
es la que todas las plataformas aceptan como tarjeta ancha. Más decisiones:

- **Formato JPG.** WebP y SVG, que el sitio usa para todo lo demás, no los
  leen con fiabilidad LinkedIn ni WhatsApp.
- **Peso menor de unos 300 KB.** Las plataformas descartan las imágenes
  pesadas. Esta pesa 215 KB.
- **Dirección absoluta** en la etiqueta (Módulo V1).
- **Sin correo ni teléfono en la imagen.** Un archivo que se comparte y se
  guarda en cachés ajenas no se puede retirar después. Los datos de contacto
  están en los PDF del CV, que sí los llevan por decisión de Janio (ver
  [Parte 3: Las secciones de Portify](03-secciones-de-portify.md), subsección
  «Después: los botones de descarga del CV»).

La imagen se hizo en Photoshop con el mismo fondo de puntos del sitio, para que
una tarjeta compartida se reconozca como parte del sitio:

1. Un lienzo de 45 por 45 píxeles con fondo transparente y un punto negro de
   4 píxeles de diámetro, centrado. Los números salen de `dots.ts`, el
   archivo que dibuja el campo de puntos de la portada.
2. *Edit > Define Pattern* (Edición > Definir motivo) guarda ese lienzo como
   un motivo repetible.
3. En el lienzo de 1200 por 630, una capa de relleno con ese motivo al 16 %
   de opacidad sobre el amarillo de la marca, `#ffdb67` (el valor de la
   variable `--primary`).
4. Encima, el logo y el texto.

### El código

Los valores que Photoshop copia, en `src/app/shared/animations/dots.ts`:

```ts
const POINT_DISTANCE = 45
const POINT_RADIUS = 2
```

Y el color de la marca, en `src/styles/_tokens.scss`:

```scss
  --primary: 255, 219, 103;
```

La distancia entre puntos (45) es el lado del lienzo; el radio (2) da el
diámetro de 4 píxeles. `255, 219, 103` en hexadecimal es `#ffdb67`.

### Cómo funciona por dentro

- **LinkedIn recorta la tarjeta.** En el Post Inspector, la imagen que
  guardan se llama `articleshare-shrink_1280_800`: la tarjeta tiene una
  proporción de 1,6 a 1, más cuadrada que 1,91 a 1. Para llegar a 1,6 se
  cortan unos 96 píxeles por cada lado del archivo de 1200 píxeles de ancho.
  Lo que importa debe caber en el **80 % central**.
- **WhatsApp y Facebook** muestran la proporción completa, así que la misma
  imagen se ve distinta según dónde se comparta. Se diseña para el peor caso
  (el recorte de LinkedIn).
- **El logo, a partir de unos 110 píxeles desde el borde izquierdo.** En la
  primera versión empezaba a unos 70 píxeles y en LinkedIn quedaba pegado al
  borde.
- **El fondo de puntos puede ocupar todo el ancho:** que se recorte no importa,
  porque es un patrón.

### Errores comunes

- **Exportar en WebP porque «es mejor».** Para el sitio sí; para las vistas
  previas, algunas plataformas no lo leen.
- **Poner el texto importante en los bordes.** El recorte de LinkedIn lo
  corta sin avisar.
- **Subir la imagen pesada.** Más de unos 300 KB puede no mostrarse.
- **Cambiar la imagen sin cambiar su nombre y esperar verla** en las
  plataformas: sus cachés guardan la anterior (Módulo V6).

### Preguntas de entrevista (senior)

#### 1. ¿Por qué se usa una imagen JPG si el resto del sitio usa WebP y SVG?

**Respuesta:**

El formato lo elige quien lee la imagen, no quien la sirve. Los crawlers de
LinkedIn y WhatsApp no leen WebP ni SVG de forma fiable para las tarjetas. El
sitio usa WebP porque los navegadores lo entienden y pesa menos; para este
caso concreto, la compatibilidad pesa más que el tamaño del archivo.

#### 2. ¿Qué es una «zona segura» en una imagen para compartir y cómo se calcula?

**Respuesta:**

Es la región central que se ve en todas las plataformas aunque recorten los
lados. Se calcula con el peor caso: LinkedIn pasa de 1,91 a 1 a 1,6 a 1, y en
una imagen de 1200 píxeles de ancho eso corta unos 96 píxeles por lado, así
que lo importante va dentro del 80 % central. Es mejor dejar margen que
descubrir el recorte en producción.

#### 3. ¿Por qué no poner el correo o el teléfono en la imagen?

**Respuesta:**

Porque una imagen compartida se copia a cachés y vistas previas de otras
plataformas que no controlas, y no se puede retirar después. Un dato de
contacto en un PDF se cambia sustituyendo el archivo; en una imagen de tarjeta
ya compartida, no.

<!-- /study-guide:section:seo-v2-image -->

---

<!-- study-guide:section:seo-v3-title-strategy -->
## Módulo V3: Las etiquetas al fijar el título

Fuente: `src/app/shared/services/seo-title-strategy.service.ts`,
`src/app/app.config.ts` y `src/app/shared/utils/seo.utils.ts`.

### El problema que resuelve

Las etiquetas Open Graph repiten el título de la página, así que hay que leerlo
en el momento justo. La idea evidente es escuchar el evento `NavigationEnd` del
router (el que avisa de que la navegación terminó) y escribir las etiquetas
ahí. Pero el router emite `NavigationEnd` **antes** de actualizar el título
(en el código de Angular, primero `events.next(new NavigationEnd(...))` y
después `titleStrategy.updateTitle(...)`). Quien lea el título dentro de ese
manejador obtiene el de la página anterior: la vista previa de una página
mostraría el título de la otra.

### La decisión en este sitio

**Un `TitleStrategy` propio.** Angular tiene una pieza, `TitleStrategy`, cuyo
trabajo es fijar el título del documento al terminar cada navegación. El sitio
la sustituye por `SeoTitleStrategy`, que fija el título igual que la original
y después escribe las etiquetas con el título ya calculado. Se ejecuta
también durante el prerenderizado, que es donde importa. Los datos que
necesita (idioma y descripción) los trae la ruta en su campo `data`
(`locale`, `description`, y `noindex` en las páginas que no deben indexarse;
ver Módulo V4).

### El código

El servicio, completo:

```ts
import { DOCUMENT, inject, Injectable } from '@angular/core'
import { Meta, Title } from '@angular/platform-browser'
import { RouterStateSnapshot, TitleStrategy } from '@angular/router'
import { Locale } from '@shared/interfaces/shared.interface'
import { applySeo } from '@shared/utils/seo.utils'

// The router fires NavigationEnd before it updates the title, so the title is not ready
// there. This strategy runs when the title is set, with the resolved route snapshot, and
// it also runs while prerendering. It replaces the default strategy: it sets the title
// exactly as before and then writes the social and search tags.
@Injectable({ providedIn: 'root' })
export class SeoTitleStrategy extends TitleStrategy {
  private readonly title = inject(Title)
  private readonly meta = inject(Meta)
  private readonly document = inject(DOCUMENT)

  override updateTitle(snapshot: RouterStateSnapshot): void {
    const title = this.buildTitle(snapshot)
    if (title === undefined) return
    this.title.setTitle(title)

    // The deepest route carries the locale and the description (see app.routes.ts).
    let leaf = snapshot.root
    while (leaf.firstChild) leaf = leaf.firstChild
    const data = leaf.data as { locale: Locale; description: string; noindex?: boolean }

    applySeo(this.document, this.meta, {
      locale: data.locale,
      path: snapshot.url.split(/[?#]/)[0],
      title,
      description: data.description,
      indexable: !data.noindex,
    })
  }
}
```

El tipo de lo que recibe `applySeo`, en `shared.interface.ts`:

```ts
export interface PageSeo {
  locale: Locale
  path: string // router path without query or fragment: '/en', '/es/projects/angular-guide'
  title: string
  description: string
  indexable: boolean
}
```

Y el registro, en `app.config.ts`:

```ts
    { provide: TitleStrategy, useClass: SeoTitleStrategy },
```

La función que quita los enlaces de la página anterior, en `seo.utils.ts`:

```ts
function replaceLinks(doc: Document, links: Record<string, string>[]): void {
  doc.head
    .querySelectorAll('link[rel="canonical"], link[rel="alternate"][hreflang]')
    .forEach((link) => link.remove())
  for (const attributes of links) {
    const link = doc.createElement('link')
    for (const [name, value] of Object.entries(attributes)) link.setAttribute(name, value)
    doc.head.appendChild(link)
  }
}
```

### Cómo funciona por dentro

- **`updateTitle` recibe el estado resuelto de la navegación**
  (`RouterStateSnapshot`). `buildTitle` es un método de la clase base que
  recorre las rutas y devuelve el título de la más profunda; si ninguna lo
  define, devuelve `undefined` y no se toca nada.
- **La ruta más profunda manda.** El bucle `while (leaf.firstChild)` baja hasta
  la ruta hoja, que es la que tiene los datos de la página.
- **El camino sin consulta ni fragmento.** `snapshot.url.split(/[?#]/)[0]`
  corta en el primer `?` o `#`. Una página como
  `/en/projects/angular-guide?utm=1#notes` tiene una sola dirección
  canónica: sin el `?utm=1` ni el `#notes`.
- **`provide: TitleStrategy, useClass: SeoTitleStrategy`** le dice a Angular
  que, cuando alguien pida `TitleStrategy`, entregue la clase propia.
- **`replaceLinks` evita la acumulación.** Cuando la persona navega dentro de
  la aplicación sin recargar, el `<head>` es el mismo: sin borrar los enlaces
  `canonical` y `alternate` anteriores, cada página nueva añadiría los suyos y
  quedarían varios `canonical` a la vez. Los borra todos y escribe los nuevos.
- **`updateTag` ya evita duplicados en las `<meta>`**, así que solo los
  `<link>` necesitan esta función.

### Errores comunes

- **Leer el título en `NavigationEnd`.** Da el título anterior. La prueba que
  lo detecta navega de una página a otra y compara.
- **Olvidar el registro en `app.config.ts`.** La clase existe pero Angular
  sigue usando la de por defecto, y las etiquetas no aparecen.
- **Usar la dirección del navegador** (`window.location`) para el camino. En
  el prerenderizado no existe; se usa la del snapshot del router.
- **Dejar un título asíncrono sin esperar** (como el de la galería, que se
  carga bajo demanda). El router espera a que se resuelva antes de llamar a
  `updateTitle`, así que no hace falta nada extra; lo cubre una prueba.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué un `TitleStrategy` en lugar de un `subscribe` a `router.events`?

**Respuesta:**

Por el orden. El router emite `NavigationEnd` antes de pedir a la estrategia
que fije el título, así que desde el evento se lee el título viejo. La
estrategia se ejecuta justo cuando el título ya está resuelto y recibe el
estado de la ruta, sin depender de una suscripción ni de su orden. Además es
el punto de extensión que Angular ofrece para esto y también se ejecuta al
prerenderizar.

#### 2. ¿Qué pasaría si `applySeo` solo agregara los enlaces y no borrara los anteriores?

**Respuesta:**

En el prerenderizado no se nota: cada archivo parte de un documento limpio. Pero
en el navegador, al navegar sin recargar, el `<head>` se conserva y cada
página añadiría su `canonical` y sus `alternate`. Quedarían varias direcciones
canónicas contradictorias, que es justo lo que el `canonical` debe evitar.
La prueba «replaces the links on the next page instead of adding more» lo
fija.

#### 3. ¿Por qué `updateTag` y no `addTag` para las `<meta>`?

**Respuesta:**

`addTag` siempre añade una etiqueta nueva; si la función se llama una vez por
navegación, se acumulan. `updateTag` busca por `name` o por `property` y
cambia la existente, o crea una si no hay. Es idempotente: llamarla dos veces
con lo mismo deja el mismo resultado, que es lo que se quiere cuando algo se
ejecuta tantas veces.

<!-- /study-guide:section:seo-v3-title-strategy -->

---

<!-- study-guide:section:seo-v4-canonical -->
## Módulo V4: Canonical, idiomas y páginas fuera del índice

Fuente: `src/app/shared/utils/seo.utils.ts`, `src/app/app.routes.ts` y
`src/app/app.routes.spec.ts`.

### El problema que resuelve

Un mismo contenido puede llegar por varias direcciones (`/en`, `/en/`, con
`?utm=1`...) y existe en dos idiomas. Sin ayuda, un buscador puede indexar la
variante equivocada o tratar el inglés y el español como copias. Y hay páginas
que no deben aparecer en los resultados, como la de «página no encontrada».

### La decisión en este sitio

Tres señales en el `<head>`:

- **`canonical`:** la única dirección que cada página quiere que se indexe.
- **`alternate` con `hreflang`:** las versiones de la misma página en otros
  idiomas (`en`, `es`) y `x-default`, la que se muestra cuando ningún idioma
  coincide. En este sitio es el inglés.
- **`noindex`:** pide que la página no se indexe, y entonces no lleva
  `canonical` ni alternativas.

Un detalle de dirección: el router de Angular quita la barra final, pero
Nginx sirve la portada en `/en/` (y redirige `/en` a `/en/`). Por eso la
dirección canónica de la portada **lleva barra** (`/en/`) y las demás
páginas no (`/en/projects/<nombre>`, `/en/gallery`).

### El código

Las direcciones, en `seo.utils.ts`:

```ts
// The router drops the trailing slash, but the homepage is served at `/en/`.
function publicUrl(path: string): string {
  return SITE_URL + (/^\/(en|es)$/.test(path) ? `${path}/` : path)
}

// The same page in every language: swap the first segment.
export function localizedUrls(path: string): { locale: Locale; url: string }[] {
  const rest = path.replace(/^\/(en|es)/, '')
  return LOCALES.map((locale) => ({ locale, url: publicUrl(`/${locale}${rest}`) }))
}
```

Y `applySeo`, con las dos ramas (indexable y no indexable):

```ts
export function applySeo(doc: Document, meta: Meta, seo: PageSeo): void {
  if (!seo.indexable) {
    meta.updateTag({ name: 'robots', content: 'noindex' })
    replaceLinks(doc, [])
    return
  }
  meta.removeTag('name="robots"')

  const url = publicUrl(seo.path)
  const image = SITE_URL + OG_IMAGE.path
  const tags: MetaDefinition[] = [
    { property: 'og:type', content: 'website' },
    { property: 'og:site_name', content: SITE_NAME },
    { property: 'og:title', content: seo.title },
    { property: 'og:description', content: seo.description },
    { property: 'og:url', content: url },
    { property: 'og:locale', content: OG_LOCALE[seo.locale] },
    { property: 'og:image', content: image },
    { property: 'og:image:width', content: String(OG_IMAGE.width) },
    { property: 'og:image:height', content: String(OG_IMAGE.height) },
    { property: 'og:image:alt', content: OG_IMAGE_ALT[seo.locale] },
    { name: 'twitter:card', content: 'summary_large_image' },
  ]
  for (const tag of tags) meta.updateTag(tag)

  const alternates = localizedUrls(seo.path)
  replaceLinks(doc, [
    { rel: 'canonical', href: url },
    ...alternates.map(({ locale, url: href }) => ({ rel: 'alternate', hreflang: locale, href })),
    // English is the default language of the site.
    { rel: 'alternate', hreflang: 'x-default', href: alternates[0].url },
  ])
}
```

Las rutas de «no encontrado», en `app.routes.ts`:

```ts
const setPageMetadata: ResolveFn<void> = (route) => {
  const locale = route.data['locale'] as Locale
  inject(DOCUMENT).documentElement.lang = locale
  inject(Meta).updateTag({ name: 'description', content: route.data['description'] as string })
}
```

```ts
// The not-found page carries the same localized metadata whether it is the
// prerendered `/en/404` file or an in-app navigation to an unknown URL.
const notFoundRoute = (locale: Locale, path: string): Route => ({
  path,
  component: NotFoundPageComponent,
  title: NOT_FOUND_TITLE[locale],
  data: { locale, description: NOT_FOUND_TITLE[locale], noindex: true },
  resolve: { pageMetadata: setPageMetadata },
})
```

Y la prueba que fija qué rutas pueden llevar `noindex`, en `app.routes.spec.ts`:

```ts
  it('asks to be kept out of the index on the not-found routes and nowhere else', () => {
    expect(routes.filter((route) => route.data?.['noindex']).map((route) => route.path)).toEqual([
      ...LOCALES.flatMap((locale) => [`${locale}/404`, `${locale}/**`]),
      '**',
    ])
  })
```

### Cómo funciona por dentro

- **`publicUrl`** añade la barra solo cuando el camino es exactamente `/en` o
  `/es`. Con `/en/gallery` no hace nada.
- **`localizedUrls` cambia solo el primer segmento.** `/es/projects/angular-guide`
  pasa a `/en/projects/angular-guide` y `/es/projects/angular-guide`. El resto
  del camino se conserva, porque los nombres de los proyectos son iguales en
  los dos idiomas.
- **`x-default` apunta al inglés** (`alternates[0]`, el primer idioma de
  `LOCALES`).
- **Una página que no se indexa no lleva `canonical`.** Decirle al buscador
  «no me indexes» y «esta es mi dirección oficial» a la vez se contradice. Por
  eso `replaceLinks(doc, [])` deja el `<head>` sin ningún enlace.
- **`noindex` se retira** con `meta.removeTag('name="robots"')` al llegar a
  la siguiente página indexable. Si no, una visita a la página 404 dentro de la
  aplicación dejaría `noindex` pegado a todas las demás hasta recargar.
- **El 404 está en tres rutas** (`<idioma>/404`, `<idioma>/**` y `**`) y todas
  salen de `notFoundRoute`, así que ninguna se olvida de `noindex`. La
  prueba de rutas lista exactamente las cinco permitidas: si alguien añade
  `noindex` a otra página por error (o una ruta de «no encontrado» nueva
  lo olvida), falla.

### Errores comunes

- **Canonical con barra en un sitio y sin barra en otro.** El buscador trata
  `/en` y `/en/` como direcciones distintas. Hay que usar la que el servidor
  sirve de verdad.
- **Incluir `?utm=...` o `#fragmento` en el canonical.** Se corta antes
  (`split(/[?#]/)`).
- **`noindex` más `canonical` en la misma página.** Mensajes contradictorios.
- **`hreflang` en un solo sentido.** Cada versión debe enlazar a todas, incluida
  ella misma; aquí cada página escribe la lista completa.
- **Dejar el `noindex` pegado** en una navegación posterior: lo cubre una
  prueba.

### Preguntas de entrevista (senior)

#### 1. ¿Qué es una URL canónica y por qué importa en un sitio con varios idiomas?

**Respuesta:**

Es la dirección que una página declara como la oficial cuando su contenido
puede alcanzarse por varias. Evita que el buscador reparta la relevancia entre
variantes (con y sin barra, con parámetros de seguimiento). En un sitio con
varios idiomas, cada versión tiene su propio `canonical` (no apunta a otro
idioma) y las demás se declaran con `hreflang`, que dice «esto es la misma
página en otro idioma», no «esto es una copia».

#### 2. ¿Por qué la portada lleva barra final en el canonical y el resto de páginas no?

**Respuesta:**

Porque el canonical debe coincidir con lo que el servidor sirve. Aquí Nginx
sirve la portada en `/en/` (y redirige `/en` con un 301) y sirve cada página
interior directamente sin barra. Un canonical que apunte a una dirección que
redirige pide al buscador que la abandone. El router de Angular no distingue
las dos, así que esa diferencia se codifica en `publicUrl`.

#### 3. ¿Por qué una página con `noindex` no debe llevar `canonical` ni `alternate`?

**Respuesta:**

Porque son señales opuestas: `canonical` dice «indexa esta dirección» y
`noindex` dice «no la indexes». Los buscadores resuelven la contradicción a su
manera, que no controlas. Además, anunciar las versiones en otros idiomas de una
página que no debe estar en el índice no tiene sentido. Dejar solo `noindex` es
la señal más clara.

<!-- /study-guide:section:seo-v4-canonical -->

---

<!-- study-guide:section:seo-v5-robots-sitemap -->
## Módulo V5: robots.txt y sitemap.xml

Fuente: `public/robots.txt`, `scripts/seo-content.mjs`,
`scripts/prepare-content.mjs` y `scripts/seo-content.test.mjs`.

### El problema que resuelve

Los buscadores necesitan dos cosas que las etiquetas del `<head>` no dan:
una lista de qué páginas existen (para no depender de seguir enlaces) y una
forma de pedir que no entren en ciertas carpetas. Para eso hay dos archivos
en la raíz del sitio: `sitemap.xml` y `robots.txt`.

### La decisión en este sitio

- **`robots.txt` es un archivo estático** que se escribe a mano. Permite
  todo, pide no rastrear `/cv/` y señala el mapa del sitio.
- **`sitemap.xml` se genera en el build.** Lo escribe el paso que prepara el
  contenido, `prepare-content`, a partir de la lista de proyectos. Un
  proyecto nuevo entra solo, sin tocar el mapa. El archivo no se guarda en el
  repositorio (está en `.gitignore`) porque siempre se puede regenerar.

**`Disallow` no bloquea a nadie.** Es lo más importante de este módulo.
`Disallow: /cv/` es una petición que los rastreadores bien portados respetan;
no es una barrera. Nginx sigue sirviendo los PDF del CV a cualquiera: se
comprobó en el sitio real con la identidad de un navegador y con la de
Googlebot, y las dos recibieron un 200. Los PDF llevan correo y teléfono por
decisión de Janio, y los botones de descarga tienen que seguir funcionando. Un
archivo que aparece en un `Disallow` puede incluso salir en los resultados si
otros sitios lo enlazan. Si algo debe ser privado, no se enlaza ni se publica.

### El código

`public/robots.txt`, completo:

```
User-agent: *
Allow: /

Disallow: /cv/

Sitemap: https://janioisacura.com/sitemap.xml
```

`scripts/seo-content.mjs`, completo:

```js
import { writeFile } from 'node:fs/promises'

// Keep in sync with SITE_URL in src/app/shared/constants/site.constants.ts.
export const SITE_URL = 'https://janioisacura.com'

const escapeXml = (text) =>
  text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')

// Public pages without the locale prefix. The homepage is served at `/<locale>/`.
export function listPages(projectSlugs) {
  return ['/', '/gallery', ...projectSlugs.map((slug) => `/projects/${slug}`)]
}

export function buildSitemap(locales, projectSlugs) {
  const urlOf = (locale, page) =>
    escapeXml(`${SITE_URL}/${locale}${page === '/' ? '/' : page}`)
  const entries = []
  for (const page of listPages(projectSlugs)) {
    for (const locale of locales) {
      entries.push(
        [
          '  <url>',
          `    <loc>${urlOf(locale, page)}</loc>`,
          ...locales.map(
            (other) =>
              `    <xhtml:link rel="alternate" hreflang="${other}" href="${urlOf(other, page)}"/>`,
          ),
          // English is the default language of the site.
          `    <xhtml:link rel="alternate" hreflang="x-default" href="${urlOf(locales[0], page)}"/>`,
          '  </url>',
        ].join('\n'),
      )
    }
  }
  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ...entries,
    '</urlset>',
    '',
  ].join('\n')
}

export async function writeSitemap(filePath, locales, projectSlugs) {
  await writeFile(filePath, buildSitemap(locales, projectSlugs), 'utf8')
}
```

La llamada, en `scripts/prepare-content.mjs`:

```js
    // The slugs are the same in every language (checked above).
  await writeSitemap(
    fileURLToPath(contentUrl('public/sitemap.xml')),
    locales,
    projects[locales[0]].map(({ slug }) => slug),
  )
```

Y las pruebas del contenido, en `scripts/seo-content.test.mjs`:

```js
test('the site address is the same here and in the Angular constants', async () => {
  const constants = await readFile(
    new URL('../src/app/shared/constants/site.constants.ts', import.meta.url),
    'utf8',
  )
  assert.ok(constants.includes(`SITE_URL = '${SITE_URL}'`))
})

// `Disallow` only asks well-behaved crawlers not to crawl a path; it blocks nobody. These checks
// keep it that way: the CV buttons must keep working while search engines are asked to stay out.
test('robots.txt keeps crawlers out of the CVs while nginx still serves them to everyone', async () => {
  const robots = await readFile(new URL('../public/robots.txt', import.meta.url), 'utf8')
  const nginx = await readFile(new URL('../nginx.conf', import.meta.url), 'utf8')
  const cv = await readFile(new URL('../content/cv.yml', import.meta.url), 'utf8')

  assert.ok(robots.split(/\r?\n/).includes('Disallow: /cv/'))
  const files = [...cv.matchAll(/file:\s*(\S+)/g)].map((match) => match[1])
  assert.ok(files.length > 0 && files.every((file) => file.startsWith('/cv/')))
  // No server rule may deny or special-case those files: the download must not depend on robots.txt.
  assert.doesNotMatch(nginx, /\bdeny\b|location[^{\n]*\/cv/)
})
```

### Cómo funciona por dentro

- **`sitemap.xml` tiene una entrada `<url>` por página y por idioma**: con
  las dos lenguas, la portada, la galería y un proyecto, son 6 direcciones.
  Cada entrada lista, con `xhtml:link`, las versiones en todos los idiomas
  y `x-default`. Es la misma información que los `<link rel="alternate">`
  del `<head>`, escrita en el mapa.
- **La página de la galería** (la de la [Parte 5](05-galeria.md)) y cada proyecto
  entran en `listPages`; el 404 no, porque no se indexa (Módulo V4).
- **`escapeXml`** cambia los caracteres que XML no admite dentro de un texto
  (`&`, `<`, `>`, `"`). Un nombre de proyecto con `&` rompería el archivo sin
  ese paso; una prueba lo comprueba con `a&b`.
- **No hay `lastmod`.** La fecha de cambio es opcional y una fecha inventada
  es peor que ninguna.
- **La dirección del sitio está en dos sitios** (`site.constants.ts` para
  Angular y `seo-content.mjs` para el script, que no puede importar TypeScript).
  Una prueba falla si difieren.
- **El `robots.txt` publicado puede no ser solo el tuyo.** Cloudflare, el
  servicio que está delante del sitio como proxy y CDN (otros CDN hacen algo
  parecido), puede servir un `robots.txt` administrado. En esta zona, el
  archivo en producción empieza con un bloque de Cloudflare (señales de
  contenido y los rastreadores de entrenamiento de IA que bloquea, entre
  `# BEGIN Cloudflare Managed content` y `# END Cloudflare Managed Content`) y
  después trae el archivo del proyecto. Por eso un 200 en `/robots.txt` no
  prueba que el tuyo esté publicado: hay que buscar `Disallow: /cv/` y
  `Sitemap:`.

### Errores comunes

- **Creer que `Disallow` protege un archivo.** Solo pide; no impide. Si el
  archivo no debe ser público, no debe estar en el servidor.
- **Bloquear con `Disallow` una página que quieres sacar del índice.** El
  buscador no la rastrea, no ve el `noindex` y puede dejarla en los
  resultados. Para sacar una página del índice, déjala rastreable con
  `noindex`.
- **Escribir una dirección relativa en `Sitemap:`.** Tiene que ser absoluta.
- **Editar a mano un mapa que se genera.** El siguiente build lo pisa.
- **Añadir una regla `deny` en Nginx «para reforzar» el `Disallow`.** Rompería
  los botones de descarga del CV; la prueba de arriba lo impide.

### Preguntas de entrevista (senior)

#### 1. ¿`Disallow` en `robots.txt` es una medida de seguridad?

**Respuesta:**

No. Es una petición educada que respetan los rastreadores que cumplen el
estándar; cualquiera puede ignorarla, y el propio archivo, que es público,
anuncia las rutas que menciona. Además, una dirección bloqueada puede aparecer
en los resultados si otros sitios la enlazan. Para restringir acceso hay que
usar autenticación o no publicar el archivo; para dejarlo fuera del índice,
`noindex` en una página rastreable.

#### 2. ¿Por qué el mapa del sitio se genera en el build y no se escribe a mano?

**Respuesta:**

Porque la lista de páginas cambia cada vez que se añade un proyecto, y un
archivo escrito a mano se desactualiza sin que nadie lo note. El script lee los
mismos datos que usa la aplicación para crear las rutas, así que mapa y sitio
no pueden diferir. El coste es una función pequeña y sus pruebas.

#### 3. Tu `robots.txt` responde 200 en producción, pero la regla no parece aplicarse. ¿Qué compruebas?

**Respuesta:**

Si el archivo que sirve el sitio es el que escribiste. Un CDN como Cloudflare
puede anteponer un bloque administrado o sustituir el archivo. Se descarga el
`robots.txt` real con `curl` y se busca una línea tuya (`Disallow: /cv/`,
`Sitemap:`). Un 200 solo dice que existe un archivo con ese nombre.

<!-- /study-guide:section:seo-v5-robots-sitemap -->

---

<!-- study-guide:section:seo-v6-verify -->
## Módulo V6: Comprobar antes y después de publicar

Fuente: las pruebas de las partes anteriores de este módulo y el HTML que
genera `npm run build`.

### El problema que resuelve

Las etiquetas de esta parte fallan en silencio: la página se ve igual y nadie
recibe un error. Una etiqueta que falta, una duplicada o una `noindex` en la
página equivocada se descubren semanas después, cuando el buscador no indexa
lo que debía. Hay que comprobarlo en tres momentos: con pruebas automáticas,
en el HTML construido y en el sitio publicado.

### La decisión en este sitio

**Tres capas de comprobación**, de la más barata a la más cara:

1. **Pruebas automáticas** que se ejecutan en cada cambio (el check `test`).
2. **Mirar el HTML construido** con `grep`, sin servidor ni navegador.
3. **Herramientas de las plataformas sobre el sitio publicado**, con la
   precaución de las cachés.

### El código

**1. Las pruebas.** Qué cubre cada archivo:

| Archivo | Qué comprueba |
| --- | --- |
| `seo.utils.spec.ts` | El `canonical`, un `alternate` por idioma y `x-default`; las etiquetas Open Graph con direcciones absolutas; que las etiquetas se sustituyen y no se acumulan; que `noindex` aparece y desaparece; `localizedUrls` |
| `seo-title-strategy.service.spec.ts` | La estrategia sobre las **rutas reales**: una página de proyecto sin consulta ni fragmento, la barra final de la portada, el título asíncrono de la galería y que cada URL de «no encontrado» lleva `noindex` |
| `app.routes.spec.ts` | La lista exacta de rutas que pueden llevar `noindex` |
| `seo-content.test.mjs` | El mapa del sitio, `robots.txt` y que Nginx no bloquea los PDF |

Un ejemplo, la prueba de la estrategia sobre las rutas reales
(`seo-title-strategy.service.spec.ts`):

```ts
  it('keeps every not-found page out of the index and clears it on the next page', async () => {
    for (const url of ['/en/404', '/es/404', '/en/does-not-exist', '/nope']) {
      await router.navigateByUrl(url)
      expect(content('meta[name="robots"]'), url).toBe('noindex')
      expect(canonical(), url).toBeUndefined()
    }

    await router.navigateByUrl('/en')
    expect(content('meta[name="robots"]')).toBeNull()
    expect(canonical()).toBe('https://janioisacura.com/en/')
  })
```

Una **comprobación de mutación** (cambiar el código a propósito para ver que
las pruebas se quejan): al quitar `noindex: true` de las rutas de «no
encontrado», fallan dos pruebas (la de la lista de rutas y la de la
estrategia). Si las pruebas siguieran en verde, no estarían protegiendo nada.

**2. El HTML construido.** Después de `npm run build`, el resultado está en
`dist/janioisacura/browser/`. Con `grep` se ve lo que recibirá un crawler:

```bash
grep -o '<meta property="og:[^>]*>' dist/janioisacura/browser/en/index.html
grep -o '<link rel="\(canonical\|alternate\)"[^>]*>' dist/janioisacura/browser/en/index.html
```

Se repite con la portada, una página de proyecto en español, la galería y el
404. Lo esperado: la portada, el proyecto y la galería con sus etiquetas y un
`canonical` cada uno; el 404 con `<meta name="robots" content="noindex">` y
**cero** `canonical`.

**3. Ya publicado.** Con `curl`:

```bash
curl -s https://janioisacura.com/sitemap.xml
curl -s https://janioisacura.com/robots.txt
curl -sI https://janioisacura.com/images/og-image.jpg
```

Lo esperado: el mapa con 6 direcciones (3 páginas por 2 idiomas), un
`robots.txt` que contiene `Disallow: /cv/` y la línea `Sitemap:`, la imagen
con un 200 y los dos PDF del CV con un 200. Después, las herramientas de la
plataforma: Post Inspector de LinkedIn, Sharing Debugger de Facebook y
WhatsApp compartiendo el enlace con `?v=2`.

### Cómo funciona por dentro

- **Probar con las rutas reales** (`provideRouter(routes)`) y no con unas
  inventadas evita que una prueba pase mientras el sitio real falla: si
  alguien cambia el título de una ruta o su `data`, la prueba lo ve.
- **El documento de las pruebas se comparte** entre todas, así que
  `beforeEach` borra las etiquetas del `<head>` antes de cada una. Sin eso,
  una prueba pasaría por culpa de la etiqueta que dejó la anterior.
- **El `grep` lee lo mismo que un crawler**: el archivo que sirve Nginx. Si la
  etiqueta no está ahí, no está para nadie, aunque en el navegador la veas
  aparecer.
- **Las cachés explican casi todos los «no se ve el arreglo».** LinkedIn,
  Facebook y WhatsApp guardan la tarjeta de cada enlace. Se vuelve a leer con
  el botón «Inspect» (LinkedIn), «Scrape Again» (Facebook) o cambiando el
  enlace con `?v=2` (WhatsApp).
- **Sin servidor público de pruebas.** El entorno de pruebas del proyecto
  está detrás de Cloudflare Access, así que las vistas previas solo se
  verifican después de publicar. Por eso las capas 1 y 2 importan tanto: son
  lo único que se puede comprobar antes.

### Errores comunes

- **Comprobar solo en el navegador.** Las herramientas de desarrollo
  muestran el `<head>` después de ejecutar JavaScript; el crawler ve el HTML
  sin ejecutar. Se mira el archivo (`view-source:` o `curl`).
- **Dar por buena una prueba que nunca vio fallar.** Se rompe el código a
  propósito una vez para comprobarlo.
- **Creer que un 200 en `/robots.txt` basta** (Módulo V5).
- **Olvidar comprobar los PDF** después de tocar `robots.txt` o Nginx: la
  regla se pensó para no romperlos.
- **Cambiar la imagen y no ver el cambio** en las plataformas: caché.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué comprobar el HTML construido con `grep` si ya hay pruebas unitarias?

**Respuesta:**

Porque las pruebas unitarias comprueban funciones y rutas por separado, y el
crawler recibe el archivo final. Un fallo de integración (la estrategia no
registrada, una ruta que no se prerenderiza) pasa las pruebas y rompe el
resultado. El `grep` mira exactamente lo que se publica, sin ejecutar nada.

#### 2. ¿Qué es una comprobación de mutación y qué aprendiste de ella aquí?

**Respuesta:**

Es romper el código a propósito para ver si las pruebas fallan. Aquí se quitó
`noindex: true` de las rutas de «no encontrado» y fallaron dos pruebas: la de
la lista de rutas y la de la estrategia. Eso confirma que protegen lo que
dicen proteger. Una prueba que sigue en verde con el código roto da una
seguridad falsa.

#### 3. Arreglas la imagen de la vista previa, publicas y LinkedIn sigue mostrando la anterior. ¿Qué haces?

**Respuesta:**

Descartar primero que sea caché. Compruebo con `curl` que la etiqueta y la
imagen publicadas son las nuevas (un 200 y el tamaño esperado). Si lo son,
abro el Post Inspector y pulso «Inspect» para que LinkedIn vuelva a leer la
página; en Facebook, «Scrape Again»; en WhatsApp, comparto el enlace con
`?v=2`. Solo si con la caché limpia sigue mal, busco el fallo en la etiqueta
o en el recorte de la imagen.

<!-- /study-guide:section:seo-v6-verify -->
