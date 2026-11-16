# Parte 3: Las secciones de Portify

> Esta versión pública conserva las explicaciones y omite fragmentos que reproducen o adaptan la plantilla comercial.

Esta parte reconstruye, una por una, las secciones de Portify sobre el
esqueleto de la Parte 2: el hero con el retrato y las ondas, el enlace
«Next chapter» que cierra cada sección y, en el camino, el control del
scroll cuando una URL lleva fragmento. Cada módulo deja un componente de
Angular con su plantilla y su hoja de estilos, traducidos del SCSS global de
la plantilla.

**Si llegaste aquí desde un buscador.** Esta página es una parte de la guía
«Cómo se construye este sitio», escrita sobre el repositorio de
janioisacura.com, un portfolio hecho con Angular que se publica como HTML
estático. El punto de partida visual es Portify, una plantilla HTML con
Bootstrap 5. Cada módulo explica el problema, muestra el código completo y lo
que enseña (jerarquía de texto, utilidades de orden de Bootstrap, iconos SVG
inline, scroll por fragmento con el router de Angular) sirve para cualquier
sitio Angular.

**Proyecto:** `src/app/home/components/`, `src/app/home/pages/`,
`src/app/shared/components/`, `src/app/shared/pipes/`,
`src/app/shared/utils/` y `src/app/app.config.ts`. **Sitio publicado:**
[janioisacura.com](https://janioisacura.com/en/). Este capítulo recorre las seis
secciones adaptadas de Portify. Las animaciones y el fondo se explican en la
[Parte 4](04-animaciones.md). La galería, que desde el 14 de noviembre de 2026
es una séptima sección entre Proyectos y Contacto, está en la
[Parte 5](05-galeria.md#módulo-g5-la-entrada-en-la-portada).

**Qué vas a aprender:**

- [Módulo S1](#módulo-s1-el-hero-jerarquía-de-texto-retrato-y-ondas): **El
  hero.** Qué va en el `<h1>` cuando la plantilla pone el rol gigante y el
  nombre pequeño, el retrato redondo con las ondas de Portify y cómo ponerlo
  primero en móvil sin cambiar el HTML.
- [Módulo S2](#módulo-s2-el-enlace-next-chapter-como-componente-compartido):
  **«Next chapter».** Un componente que calcula «01/07» y el destino desde
  la lista de secciones, con la flecha de Phosphor como SVG en lugar de la
  fuente de iconos, y un contraste que cumple WCAG AA.
- [Módulo S3](#módulo-s3-scroll-por-fragmento-sin-saltos): **Scroll por
  fragmento.** Por qué cambiar de idioma corría la página 12 px y la hacía
  saltar, y cómo un scroll propio reemplaza al `anchorScrolling` del router
  para poder omitirlo en una navegación concreta.
- [Módulo S4](#módulo-s4-el-título-de-sección-compartido-y-sobre-mí): **El
  título de sección y Sobre mí.** La línea vertical, el texto gigante de
  fondo y el `<h2>` como un componente con entradas opcionales, y la primera
  sección que lo usa: párrafos de Markdown sin tarjetas ni cifras.
- [Módulo S5](#módulo-s5-habilidades-filas-numeradas-y-lista-con-regla): **Habilidades.**
  Filas numeradas `01.-` con el título enmarcado, una lista con una regla de
  2 px en lugar de porcentajes y etiquetas, y un `featured` por idioma en el
  YAML, validado por el script de contenido.
- [Módulo S6](#módulo-s6-experiencia-y-los-pipes-month-y-serial): **Experiencia
  y los pipes.** La cronología con sus dos líneas, `MonthPipe` con
  `Intl.DateTimeFormat` en UTC y `SerialPipe` para numerar, con la regla
  «pipe o función» y sus pruebas.
- [Módulo S7](#módulo-s7-proyectos-tarjetas-y-página-de-detalle): **Proyectos.**
  La tarjeta con el efecto de Portify y dos enlaces accesibles, y el modal
  de la plantilla convertido en una página con barra lateral, `ViewEncapsulation.None`
  para el cuerpo en Markdown y las rutas que salen del contenido.
- [Módulo S8](#módulo-s8-contacto-sin-formulario-ni-correo): **Contacto.**
  Los ítems con icono redondo y los iconos sociales de Portify sin el
  formulario ni el correo, el nombre accesible de un enlace que es sólo un
  icono, y cómo ocultar un dato del contenido sin tocar el componente.
- [Módulo S9](#módulo-s9-el-pie-de-página-sin-crédito-y-con-volver-arriba):
  **El pie.** La banda de Portify con el copyright, una línea sobre el
  stack y «Volver arriba» como enlace del router; qué ve cada lector de un
  año calculado con `new Date()` en un sitio prerenderizado.

Cada módulo sigue el mismo orden: el problema que resuelve, la decisión tomada
en este sitio, el procedimiento o el código completo, cómo funciona por
dentro, errores comunes y preguntas de entrevista con su respuesta.

Esta página es una parte de la guía [Cómo se construye este sitio](como-se-construye.md).
Conviene haber leído antes la [Parte 2](02-cimientos-de-estilo.md), de donde
salen `tools`, los tokens, el esqueleto y la constante `SECTIONS`, y la
anatomía del hero original en
[Secciones y contenido](secciones-y-contenido.md#secciones-elegidas-para-el-mvp).

---

<!-- study-guide:section:sections-s1-hero -->
## Módulo S1: El hero: jerarquía de texto, retrato y ondas

Fuente: `src/app/home/components/hero/` y `src/app/home/pages/home-page/`
del repositorio.

### El problema que resuelve

El hero de Portify tiene un saludo pequeño en un `<h4>`, el rol en un `<h1>`
gigante que escribe un efecto máquina de escribir, una línea de descripción,
dos botones y un retrato redondo rodeado de ondas. Traducido tal cual, el
`<h1>` de la página diría «Senior Frontend Engineer» y el nombre de Janio
quedaría en un encabezado secundario: mal para buscadores, para lectores de
pantalla y para la pestaña, que ya se titula con el nombre. Además el
`<h1>` original está vacío en el HTML hasta que el JavaScript lo escribe. Y
en móvil Portify muestra primero el texto y después la foto; aquí se quería
al revés.

### La decisión en este sitio

- El `<h1>` sigue siendo el nombre, en Barlow Condensed **Light Italic** (300,
  `-0.05em`) a 22/40 px: discreto, pero es el encabezado. El rol va en un
  `<p>` con la **SemiBold Italic** a 40/70/100 px, que es donde está el peso
  visual, como en la plantilla. La intro es la descripción. Son los dos
  estilos de título de la pizarra de marca (Parte 1, Módulo M5).
- Sin efecto máquina de escribir: el rol es texto en el HTML prerenderizado.
- Un solo botón, «View projects», en esta primera etapa. Los botones de descarga
  del CV llegaron después, cuando existieron los PDF (ver «Después: los botones de
  descarga del CV», más abajo): un botón a un PDF inexistente es peor que no
  tenerlo.
- Retrato en `public/images/hero.jpg`, cuadrado de 416 × 416 como el de
  Portify, redondo con borde de 2 px y las ondas en CSS. Por debajo de `md`
  va primero y centrado; desde `md`, a la derecha del texto.
- El enlace «01/07 Next chapter» es un componente compartido (Módulo S2). El
  total sale de `SECTIONS`: eran seis secciones cuando se escribió este módulo
  («01/06») y son siete con la Galería de la Parte 5.

### El código

`hero.component.ts` recibe el perfil y el idioma:

```ts
import { Component, input } from '@angular/core'
import { RouterLink } from '@angular/router'
import { Profile } from '@interfaces/profile.interface'
import { NextChapterComponent } from '@shared/components/next-chapter/next-chapter.component'
import { Locale } from '@shared/interfaces/shared.interface'

@Component({
  selector: 'home-hero',
  imports: [RouterLink, NextChapterComponent],
  templateUrl: './hero.component.html',
  styleUrl: './hero.component.scss',
})
export class HeroComponent {
  readonly profile = input.required<Profile>()
  readonly locale = input.required<Locale>()
}
```

La portada lo usa con `<home-hero [profile]="profile" [locale]="locale" />`.

`hero.component.html`:


`hero.component.scss`:


`img-fluid` viene del parcial `images` de Bootstrap, que se añadió a
`_bootstrap.scss` en este paso (Parte 2, Módulo E1).

### Cómo funciona por dentro

- **El rol toma la fuente de título sin ser título.** `$headings-font-family`
  es la variable de Bootstrap que `_tools.scss` fija a Barlow Condensed
  (Parte 2, Módulo E2); usarla en el `<p>` del rol garantiza que si la
  familia cambia, cambia en los dos sitios. `line-height: 1` evita el aire
  entre líneas a 100 px.
- **Las ondas** son cuatro `<span>` absolutos que ocupan el círculo entero
  (`inset: 0`, `border-radius: 50%`), con sólo el borde superior o inferior
  pintado. La animación los desplaza 4 rem hacia arriba o hacia abajo
  mientras se desvanecen, y los retardos de 0,5 s escalonan los cuatro: la
  sensación es de ondas que salen de la foto. Al pasar el ratón, el
  contenedor baja su opacidad a 0 con una transición de 300 ms.
- **`order-first` y `order-md-0`, no `order-md-last`.** Para poner la foto
  antes del texto en móvil sin tocar el HTML, su columna recibe
  `order-first` (`order: -1`). Desde `md` hay que devolverla a su sitio, y
  lo intuitivo es `order-md-last`, pero eso la manda **después** de la
  tercera columna de la fila, la de «Next chapter» (orden 0 y ancho
  completo), y aparece debajo del enlace. `order-md-0` la deja con orden 0,
  igual que las otras, y gana el orden del HTML: texto, foto, enlace.
- **`mx-auto` / `mx-md-0`** centran el `.img-wrapper` (de 416 px como
  máximo) dentro de su columna sólo cuando está apilado.
- **`alt=""`** en el retrato: está junto al nombre, que ya lo identifica, y
  un lector de pantalla no gana nada oyendo «foto de Janio». El
  `aria-labelledby` del `<section>` apunta al `<h1>`.
- **`[routerLink]="[]"` con `fragment="projects"`** navega a la ruta actual
  con el fragmento; `queryParamsHandling="preserve"` conserva una query como
  `?ref=portfolio`, y una prueba de `app.spec.ts` lo comprueba buscando ese
  enlace como el primer `<a>` del hero.

### Después: los botones de descarga del CV

Esta subsección es una etapa posterior (14 de noviembre de 2026). El primer hero tenía un
solo botón; este es el que se le sumó.

**El problema.** Quien visita el sitio quiere llevarse el CV, y hay dos: uno en inglés y
otro en español. Un reclutador que lee el sitio en un idioma puede necesitar el CV en el
otro, así que ofrecer solo el del idioma de la página no basta.

**La decisión.** Dos botones iguales en cada página, escritos cada uno en el idioma de su
PDF («Download CV (EN)» y «Descargar CV (ES)»), en el hero y en Contacto. Los archivos
viven en `public/cv/` con nombres en minúsculas, y la lista, en un archivo de contenido
(`content/cv.yml`). Son **enlaces normales** a los PDF, así que funcionan en el HTML
prerenderizado y sin JavaScript.

La lista de contenido:

```yaml
# The downloadable CVs, one PDF per language. The files live in public/cv/ and are served
# from /cv/. `filename` is the name the visitor's browser suggests when saving.
downloads:
  - locale: en
    file: /cv/janio-isacura-cv-en.pdf
    filename: JanioIsacura-CV-EN.pdf
  - locale: es
    file: /cv/janio-isacura-cv-es.pdf
    filename: JanioIsacura-CV-ES.pdf
```

El componente que dibuja los dos botones, usado por el hero y por Contacto:

```ts
import { Component } from '@angular/core'
import { CV_DOWNLOADS } from '@generated/cv'
import { PROFILE } from '@generated/profile'

// The two CVs, one button each, the same on every page whatever its language: a visitor who
// reads the site in one language may need the CV in the other. Each button is written in the
// language of its PDF and says so to a screen reader (`lang`), so it is pronounced right.
// They are plain links to the files: they work in the prerendered HTML and without JavaScript.
@Component({
  selector: 'home-cv-downloads',
  templateUrl: './cv-downloads.component.html',
  styleUrl: './cv-downloads.component.scss',
})
export class CvDownloadsComponent {
  protected readonly downloads = CV_DOWNLOADS.map((download) => ({
    ...download,
    label: PROFILE[download.locale].actions.cv,
  }))
}
```



La fila de acciones del hero:


Y lo que comprueba el build para que un botón nunca apunte a nada:

```js
// Tells what is wrong with the bytes of a PDF, or returns null when they look like a whole one.
// It is not a PDF reader: it checks what a partial export loses. A truncated file keeps its
// "%PDF-" signature but not its end, so it must finish with a cross-reference offset and
// "%%EOF", the offset must point at the table, and the file must declare at least one page.
export function describePdfProblem(bytes) {
  const text = bytes.toString('latin1')
  if (!text.startsWith('%PDF-')) return 'it is not a PDF file.'

  const end = /startxref\s+(\d+)\s*%%EOF\s*$/.exec(text.slice(-1024))
  if (!end) return 'it is incomplete: it does not end with a cross-reference offset and %%EOF.'
  const offset = Number(end[1])
  if (offset >= bytes.length || !/^(xref|\d+\s+\d+\s+obj)/.test(text.slice(offset, offset + 24)))
    return 'it is damaged: its cross-reference offset points at nothing.'

  // Page objects can only be counted when they are stored in the clear. A PDF that packs its
  // objects in streams (/ObjStm) is accepted on its structure alone.
  const packed = /\/Type\s*\/ObjStm/.test(text)
  const pages = (text.match(/\/Type\s*\/Page(?![A-Za-z])/g) ?? []).length
  if (pages === 0 && !packed) return 'it has no pages.'
  return null
}

// Every listed file must exist under public/, be a PDF and look whole (see describePdfProblem).
export async function checkCvFiles(downloads, publicDirectory) {
  for (const { file } of downloads) {
    const path = join(publicDirectory, file)
    let bytes
    try {
      bytes = await readFile(path)
    } catch {
      throw new Error(`${file}: the file is missing from public/. Copy the PDF to ${path}.`)
    }
    const problem = describePdfProblem(bytes)
    if (problem) throw new Error(`${file}: ${problem}`)
  }
}
```

**Cómo funciona.**

- **`download` y el nombre.** El atributo `download` hace que el navegador guarde el
  archivo en lugar de abrirlo, con el nombre sugerido (`JanioIsacura-CV-EN.pdf`),
  distinto del nombre en el servidor. Solo funciona para archivos del mismo sitio.
- **El idioma del botón.** `lang` indica a un lector de pantalla en qué idioma leerlo;
  sin él, «Descargar CV (ES)» se leería con la pronunciación del idioma de la página.
- **El nombre accesible** es el texto visible más «(PDF)»: empieza por lo que se ve,
  como pide la regla de que el nombre contenga el texto visible.
- **El par viaja junto.** El componente es una fila que se parte por sí misma: si en el
  hero no caben los tres botones, los dos CV pasan juntos a la línea siguiente.
- **Un PDF cortado conserva la firma.** Una exportación interrumpida deja el encabezado
  `%PDF-` pero no el final. Por eso el build exige que el archivo termine en `startxref`,
  un desplazamiento y `%%EOF`, que ese desplazamiento apunte a la tabla de referencias y que
  declare al menos una página. No es un lector de PDF: no revisa el texto de dentro.
- **El servidor** entrega los `.pdf` como `application/pdf` con `Cache-Control: no-cache`:
  el navegador pregunta si cambió, así que reemplazar el archivo basta.

**Errores comunes.**

- **Un botón que apunta a un PDF que todavía no está.** Por eso el build lo comprueba y
  falla si falta, en vez de publicar un enlace roto.
- **Nombres con espacios o mayúsculas** en `public/cv/`: dan direcciones que se rompen al
  copiarlas. El build exige minúsculas y guiones.
- **Dos idiomas con el mismo PDF.** Un botón entregaría el CV del otro idioma. El build
  rechaza dos entradas con el mismo archivo o el mismo nombre al guardar.
- **Dejar un PDF de otra versión en la carpeta.** Todo lo que está en `public/` se
  despliega y tiene una dirección pública: solo van los dos vigentes.
- **Publicar el CV con datos que el sitio decidió no mostrar.** Las páginas no llevan
  correo, pero un CV sí suele llevarlo, y un PDF público lo copian los buscadores y los
  bots. Es una decisión consciente, anotada en `docs/cv.md`.

### Errores comunes

- **Copiar la jerarquía de Portify** (rol en `<h1>`, nombre en `<h4>`) o
  dejar el `<h1>` vacío para rellenarlo con JavaScript. El HTML prerenderizado
  tiene que decir quién es la persona sin ejecutar nada.
- **`order-md-last`** con una tercera columna en la fila: la foto cae al
  final. Se vio en la revisión a 900 px.
- **`font-weight: 500` en la descripción**, como en Portify: con
  `font-synthesis: none` y sólo el peso 300 cargado no cambia nada (Parte 2,
  Módulo E4).
- **Un botón a un recurso que no existe** («Download CV» sin PDF): se añade
  cuando el archivo esté, y el build comprueba que esté (ver la subsección de los
  botones del CV).
- **Olvidar `images` en `_bootstrap.scss`:** `img-fluid` no existe y la foto
  no escala.

### Preguntas de entrevista (senior)

#### 1. La plantilla pone el rol en el `<h1>` y el nombre en un `<h4>`. ¿Lo respetas?

**Respuesta:**

No. El `<h1>` es el encabezado del documento: lo primero que anuncia un
lector de pantalla y lo que los buscadores toman como tema de la página. En
un portfolio personal eso es el nombre, y además coincide con el `<title>`.
La plantilla eligió así por la jerarquía **visual**, no por la semántica, y
las dos cosas se separan: el nombre en el `<h1>` con un estilo discreto y el
rol en un párrafo con la fuente y el tamaño de título. Es un caso típico de
«el CSS decide cómo se ve, el HTML decide qué es».

#### 2. ¿Cómo cambias el orden visual de las columnas en móvil sin cambiar el orden del HTML, y qué cuidado tiene?

**Respuesta:**

Con la propiedad `order` de flexbox, que Bootstrap expone como utilidades
(`order-first`, `order-md-0`, `order-md-last`…). El HTML conserva el orden
de lectura, que es el que usan lectores de pantalla y el tabulador, y el
CSS reordena sólo la presentación. El cuidado: `order` ordena **todos** los
hermanos del contenedor flex, no sólo los dos que uno tiene en mente; con
una tercera columna, `order-last` la adelanta sin querer. Y si el orden
visual se aleja mucho del de lectura, el foco del teclado salta de forma
confusa, así que conviene limitarlo a casos como este, donde el elemento
movido es decorativo.

#### 3. ¿Por qué un retrato con `alt=""` y no con el nombre de la persona?

**Respuesta:**

`alt=""` marca la imagen como decorativa y el lector de pantalla la salta.
Aquí es lo correcto porque el nombre está en el `<h1>` contiguo: con
`alt="Janio Isacura"` la persona oiría el nombre dos veces seguidas. La regla
general es preguntarse qué pierde quien no ve la imagen; si la respuesta es
«nada que el texto de al lado no diga», va vacío. Si la foto estuviera sola
(una tarjeta de contacto sin nombre visible), sí llevaría el nombre.

<!-- /study-guide:section:sections-s1-hero -->

---

<!-- study-guide:section:sections-s2-next-chapter -->
## Módulo S2: El enlace «Next chapter» como componente compartido

Fuente: `src/app/shared/components/next-chapter/` del repositorio.

### El problema que resuelve

Cada sección de Portify termina con el mismo enlace: «01/11 Next Chapter» y
una flecha, con el número escrito a mano en cada sección. Al quitar cinco
secciones hay que renumerar los once; si se añade una, otra vez. Y la flecha
es un icono de la fuente Phosphor, que pesa 4 MB en base64 dentro del CSS
de la plantilla.

### La decisión en este sitio

- Un componente `shared-next-chapter` que recibe el idioma y el `id` de la
  sección que lo aloja, y calcula el número, el total y el destino desde
  `SECTIONS`, la misma lista que alimenta el menú (Parte 2, Módulo E6). La
  última sección no renderiza nada.
- La flecha es el SVG de Phosphor `arrow-elbow-right-down`, pegado inline:
  Phosphor es MIT, el archivo pesa unos 300 bytes y toma el color del texto
  con `currentColor`.
- El contador «01/07» va en negro al 60 %: al 50 %, como en Portify, el
  contraste sobre el amarillo es de 3,7:1, por debajo del 4,5:1 de WCAG AA.

### El código

`next-chapter.component.ts`:

```ts
import { Component, computed, input } from '@angular/core'
import { RouterLink } from '@angular/router'
import { SerialPipe } from '@shared/pipes/serial.pipe'
import { SECTIONS } from '@shared/constants/sections.constants'
import { Locale } from '@shared/interfaces/shared.interface'

@Component({
  selector: 'shared-next-chapter',
  imports: [RouterLink, SerialPipe],
  templateUrl: './next-chapter.component.html',
  styleUrl: './next-chapter.component.scss',
})
export class NextChapterComponent {
  readonly locale = input.required<Locale>()
  // Id of the section that hosts the link; the target is the following section.
  readonly current = input.required<string>()

  protected readonly chapter = computed(() => {
    const index = SECTIONS.findIndex((section) => section.id === this.current())
    return { index, target: SECTIONS[index + 1]?.id ?? null }
  })
  // Index of the last section, so the counter reads "01/06".
  protected readonly lastIndex = SECTIONS.length - 1

  protected readonly label = computed(() =>
    this.locale() === 'es' ? 'Siguiente capítulo' : 'Next chapter',
  )
}
```

`next-chapter.component.html`:


`next-chapter.component.scss`:


Uso en una sección: `<shared-next-chapter [locale]="locale()" current="home" />`.

### Cómo funciona por dentro

- **`input.required`** declara entradas obligatorias como señales: si una
  sección olvida pasar `current`, el compilador de plantillas avisa.
- **`computed`** deriva la posición y el destino de `SECTIONS` y de las
  entradas; se recalcula solo si cambia la sección. El «01/07» lo escribe el
  `SerialPipe` en la plantilla, desde esa posición y desde `lastIndex`
  (Módulo S6; al principio era un `padStart(2, '0')` dentro del `computed`).
  `SECTIONS[index + 1]?.id ?? null` devuelve `null` en la última sección, y
  el `@if` de la plantilla no pinta nada.
- **`@if (...; as target)`** guarda el valor en una variable de plantilla
  para no volver a leer `chapter().target` dentro del bloque.
- **El enlace navega a `/${locale}` con `fragment`**, como los del menú, así
  que funcionaría también desde otra página; el scroll lo hace el Módulo S3.
- **El SVG inline con `aria-hidden="true"`**: es decorativo (el texto ya dice
  «Next chapter»); `fill="currentColor"` lo pinta del color del enlace;
  `viewBox` lo hace escalable y el tamaño lo fija el CSS en 24 px.
- **La animación `updown`** del icono al pasar el ratón es la de Portify,
  `alternate-reverse infinite`, un rebote de 7 px.
- **Contraste**: con `rgba(var(--black), 0.6)` sobre `#ffdb67` el color
  resultante es aproximadamente `#665836`, unos 5,2:1 de contraste. El
  umbral AA para texto normal es 4,5:1; para texto grande (más de 24 px, o
  19 px en negrita) bastaría 3:1, pero el contador hereda los 16 px del
  cuerpo.

### Errores comunes

- **Escribir el número en cada sección**, como la plantilla. Se desincroniza
  en cuanto cambia la lista.
- **Meter la fuente de iconos** para una sola flecha: 4 MB de CSS. Un SVG
  inline o un sprite de los iconos usados pesa casi nada.
- **Un SVG decorativo sin `aria-hidden`**: algunos lectores anuncian
  «imagen» o leen el `<title>` del SVG.
- **Fiarse del contraste de la plantilla.** Portify usa negro al 50 % sobre
  amarillo; no cumple AA para texto pequeño. Comprobarlo con la herramienta
  de contraste del navegador o cualquier calculadora WCAG.

### Preguntas de entrevista (senior)

#### 1. ¿Cuándo un icono va como SVG inline, como `<img>` o como fuente de iconos?

**Respuesta:**

Inline cuando hay pocos iconos y necesitan tomar el color del texto o
animarse por partes: va en el HTML, sin petición extra, y `currentColor` lo
pinta solo. Como `<img src="icono.svg">` cuando son muchos o grandes y
conviene cachearlos aparte; pierden el color heredado. La fuente de iconos
fue la solución de hace diez años: un archivo con cientos de glifos, de los
que se usan diez, bloquea el render hasta que se descarga y falla con
`font-display` o con fuentes del sistema forzadas. Hoy la opción intermedia
es un sprite SVG con `<use>`: un archivo con sólo los iconos usados y color
heredado.

#### 2. ¿Cómo calculas si un color cumple WCAG AA y qué umbral aplica?

**Respuesta:**

Se calcula la luminancia relativa de los dos colores (texto y fondo, con la
transparencia ya mezclada sobre el fondo) y el contraste es
`(L1 + 0,05) / (L2 + 0,05)`. AA exige 4,5:1 para texto normal y 3:1 para
texto grande (18 pt o 14 pt en negrita, unos 24 px o 19 px) y para
componentes de interfaz; AAA sube a 7:1 y 4,5:1. Un color con opacidad no se
puede evaluar sin el fondo: negro al 50 % cumple sobre blanco y no cumple
sobre este amarillo. Las herramientas de desarrollo del navegador lo muestran
al inspeccionar el color.

#### 3. ¿Por qué `input.required` y `computed` en vez de un `@Input()` y un getter?

**Respuesta:**

`input.required` es una señal: el compilador exige que se pase y el valor se
lee con `current()`, sin ciclos de vida ni `ngOnChanges`. `computed` guarda
el resultado y sólo lo recalcula cuando cambia una señal de la que depende;
un getter se evaluaría en cada detección de cambios y con `findIndex` en
cada ciclo no importa aquí, pero sí en listas grandes. Además los dos juntos
hacen el componente compatible con la detección de cambios sin Zone.js,
hacia donde va Angular.

<!-- /study-guide:section:sections-s2-next-chapter -->

---

<!-- study-guide:section:sections-s3-fragment-scrolling -->
## Módulo S3: Scroll por fragmento sin saltos

Fuente: `src/app/app.config.ts`, `src/app/app.scss`,
`src/app/shared/utils/fragment-scrolling.utils.ts`,
`src/app/shared/constants/scrolling.constants.ts` y
`src/app/shared/components/language-switcher/` del repositorio.

### El problema que resuelve

Con el hero publicado apareció un fallo al cambiar de idioma estando en
`/en#home`: la página saltaba hacia abajo y, a partir de 1400 px, se corría
12 px a la izquierda, comiéndose el margen del contenido hasta que se
redimensionaba la ventana. Eran dos problemas:

1. **El corrimiento.** La fila principal usa `gx-xxl-6`, un gutter de 72 px:
   sus márgenes de -36 px desbordan por 24 px un contenedor con 12 px de
   padding, y el documento queda con scroll horizontal. No se ve porque
   `body` tiene `overflow-x: hidden`, pero `hidden` sólo oculta: los scripts
   pueden seguir desplazando. El `anchorScrolling` del router llama a
   `scrollTo(x, y)` con la posición del elemento del fragmento, y x era 12.
2. **El salto.** El selector de idioma conserva el fragmento (para no perder
   un enlace a un encabezado de un proyecto), y `anchorScrolling` lleva la
   vista al inicio de esa sección aunque la persona estuviera leyendo más
   abajo. Janio decidió que cambiar de idioma no debe mover la página.

### La decisión en este sitio

- `main { overflow-x: clip }`: elimina el desborde en vez de ocultarlo, así
  no hay a dónde desplazarse. En el `body` no sirve: aplicado al viewport,
  `clip` se comporta como `hidden`.
- El router deja de hacer el scroll al fragmento. `withInMemoryScrolling()`
  queda sólo para que emita sus eventos `Scroll`, y un inicializador propio
  decide cuándo usarlos: salta al fragmento salvo que la navegación lleve
  `KEEP_SCROLL` o venga del historial (atrás/adelante traen su propia
  posición).
- El selector de idioma envía `KEEP_SCROLL` como `info` del `routerLink`.
- El fragmento de la **primera sección** (`#home`, el del menú y el de «Volver
  arriba» del pie) lleva al tope de la ventana, no a la sección: `<section
  id="home">` empieza 68 px por debajo del borde porque la barra del logo
  queda encima, y «arriba» tiene que mostrar la barra.

### El código

`src/app/app.scss`:


`src/app/shared/constants/scrolling.constants.ts`:

```ts
// Navigation `info` that asks the fragment scrolling to leave the viewport where it is.
export interface ScrollInfo {
  keepScroll?: boolean
}

export const KEEP_SCROLL: ScrollInfo = { keepScroll: true }
```

`src/app/shared/utils/fragment-scrolling.utils.ts`:

```ts
import { ViewportScroller } from '@angular/common'
import { inject, provideEnvironmentInitializer } from '@angular/core'
import { Router, Scroll } from '@angular/router'
import { filter } from 'rxjs'
import { ScrollInfo } from '@shared/constants/scrolling.constants'

// Scrolls to the URL fragment once a navigation has rendered, unless the navigation
// carries `KEEP_SCROLL` (the language switcher: same page, other language) or restores
// a history entry (back/forward bring their own position). It replaces the router's
// `anchorScrolling`, which cannot skip a single navigation.
export function provideFragmentScrolling() {
  return provideEnvironmentInitializer(() => {
    const router = inject(Router)
    const scroller = inject(ViewportScroller)

    router.events.pipe(filter((event) => event instanceof Scroll)).subscribe((event) => {
      const info = router.lastSuccessfulNavigation()?.extras.info as ScrollInfo | undefined
      if (event.anchor && !event.position && !info?.keepScroll) {
        scroller.scrollToAnchor(event.anchor)
      }
    })
  })
}
```

`src/app/app.config.ts`:

```ts
import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core'
import { provideRouter, withInMemoryScrolling } from '@angular/router'
import { provideClientHydration } from '@angular/platform-browser'
import { provideFragmentScrolling } from '@shared/utils/fragment-scrolling.utils'

import { routes } from './app.routes'

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    // In-memory scrolling only emits the router's Scroll events; the fragment scrolling
    // below decides when to use them.
    provideRouter(routes, withInMemoryScrolling()),
    provideFragmentScrolling(),
    provideClientHydration(),
  ],
}
```

Y en el selector de idioma, el enlace lleva `[info]="keepScroll"`, con
`protected readonly keepScroll = KEEP_SCROLL` en el componente.

### Cómo funciona por dentro

- **`overflow: hidden` frente a `overflow: clip`.** Los dos ocultan lo que
  sobresale, pero `hidden` convierte al elemento en un contenedor de scroll
  que sólo la persona no puede desplazar; `scrollTo`, `scrollIntoView` o el
  foco de un elemento sí lo mueven. `clip` no crea contenedor de scroll: el
  contenido se recorta y punto. En el viewport (el `<html>` o el `<body>`
  cuando propaga) la especificación convierte `clip` en `hidden`, por eso
  hubo que aplicarlo a `main`, que es donde está el desborde.
- **Los eventos `Scroll` del router.** Tras cada navegación, el
  `RouterScroller` emite un evento `Scroll` con el `anchor` (el fragmento de
  la URL) y, si la navegación viene del historial, la `position` guardada.
  Lo emite después de un `setTimeout` y un `requestAnimationFrame`, cuando
  la vista nueva ya está pintada; por eso el elemento del fragmento existe
  al llegar al manejador. Con `withInMemoryScrolling()` sin opciones el
  router emite los eventos pero no actúa: `anchorScrolling` y
  `scrollPositionRestoration` quedan desactivados.
- **`info` en la navegación.** `NavigationExtras.info` (y la entrada `info`
  de `routerLink`) lleva un dato cualquiera junto a la navegación, sin
  tocar la URL ni el `state` del historial. `router.lastSuccessfulNavigation()`
  es una señal con la última navegación completada; de ahí se lee `extras.info`
  cuando llega el evento `Scroll`.
- **`provideEnvironmentInitializer`** registra una función que corre una vez
  al crear el inyector de la aplicación; es el sitio para una suscripción
  que debe vivir mientras viva la app. En el prerenderizado también corre,
  pero el `ViewportScroller` del servidor no hace nada.
- **Por qué no se restaura la posición del historial.** Con
  `scrollPositionRestoration` desactivado, Angular no toca el scroll en
  atrás/adelante y el navegador aplica su propia restauración. El manejador
  sólo evita pisarla con un salto al fragmento.

### Después: una página nueva empieza arriba

Esta subsección es una etapa posterior (14 de noviembre de 2026), cuando se sumó la
galería como página. El código de arriba es el de cuando el módulo se construyó;
este es el archivo actual.

**El problema.** Al ir de la portada, ya desplazada, a la galería, la página nueva
se abría en el mismo desplazamiento y el visitante quedaba dentro de la
cuadrícula. El router de este sitio no restaura posiciones, y este inicializador
descartaba las navegaciones sin fragmento.

**La decisión.** Recordar la página de la navegación anterior. Si la nueva es otra
página y no trae fragmento, ir al tope. Las páginas se siguen con `NavigationEnd`,
que siempre se emite, y no con `Scroll`: con hidratación el router no emite `Scroll`
en la primera navegación, y entonces la primera navegación real (de la portada a la
galería) se tomaría por la primera página y conservaría el desplazamiento. Se deja en paz la primera carga (la decide
el navegador), un cambio solo de parámetros, el historial (que trae su posición) y
el cambio de idioma, que pide conservarla. El enlace de volver de la galería
apunta a `#gallery`, para caer en la sección.

```ts
import { ViewportScroller } from '@angular/common'
import { DOCUMENT, inject, provideEnvironmentInitializer } from '@angular/core'
import { NavigationEnd, Router, Scroll } from '@angular/router'
import { filter } from 'rxjs'
import { ScrollInfo } from '@shared/constants/scrolling.constants'
import { SECTIONS } from '@shared/constants/sections.constants'

// The first section is the top of the page: its link and the footer's "back to top"
// go to the very top of the window, not to the section, which starts below the header.
const TOP_SECTION = SECTIONS[0].id

// Scrolls to the URL fragment once a navigation has rendered, unless the navigation
// carries `KEEP_SCROLL` (the language switcher: same page, other language) or restores
// a history entry (back/forward bring their own position). It replaces the router's
// `anchorScrolling`, which cannot skip a single navigation. The fragment of the first
// section scrolls to the top of the window instead of to the section. A navigation to another
// page without a fragment (the homepage to the gallery, or to a project) starts at the top too:
// the router does not restore positions here, so the new page would otherwise open at the
// offset the visitor had on the previous one.
export function provideFragmentScrolling() {
  return provideEnvironmentInitializer(() => {
    const router = inject(Router)
    const scroller = inject(ViewportScroller)
    const document = inject(DOCUMENT)

    // `scrollToAnchor` ignores the CSS `scroll-padding-top` (it scrolls the window to the element's
    // position minus its own offset), so a section reached from the menu would stop behind the
    // sticky header bar. The offset is read from that same CSS property when it is needed: the
    // height of the bar below `xl` (`$header-height`), nothing above it.
    scroller.setOffset(() => {
      const padding = document.defaultView
        ?.getComputedStyle(document.documentElement)
        .getPropertyValue('scroll-padding-top')
      return [0, parseFloat(padding ?? '') || 0]
    })

    // Which page each navigation ended on comes from NavigationEnd, which always fires. The
    // router's Scroll event does not: with hydration it skips the first navigation, so
    // tracking the pages from Scroll would take the first real navigation for the first page.
    let currentPath: string | null = null
    let changedPage = false

    router.events
      .pipe(filter((event): event is NavigationEnd => event instanceof NavigationEnd))
      .subscribe((end) => {
        const path = end.urlAfterRedirects.split(/[?#]/)[0]
        // Null before the first navigation, so the page a visitor lands on is left to the browser.
        changedPage = currentPath !== null && path !== currentPath
        currentPath = path
      })

    router.events.pipe(filter((event) => event instanceof Scroll)).subscribe((event) => {
      // Used once: a Scroll that follows no navigation of its own must not repeat it.
      const goesToAnotherPage = changedPage
      changedPage = false

      const info = router.lastSuccessfulNavigation()?.extras.info as ScrollInfo | undefined
      if (event.position || info?.keepScroll) return
      if (!event.anchor) {
        if (goesToAnotherPage) scroller.scrollToPosition([0, 0])
        return
      }
      if (event.anchor === TOP_SECTION) scroller.scrollToPosition([0, 0])
      else scroller.scrollToAnchor(event.anchor)
    })
  })
}
```

### Después: las secciones paran bajo el encabezado fijo

Otra etapa posterior (15 de noviembre de 2026). El encabezado se quedó fijo
arriba en móvil (el [Módulo E7 de la Parte 2](02-cimientos-de-estilo.md#módulo-e7-los-estilos-del-menú-de-portify-traducidos-a-un-componente), que explica los estilos del menú) y el archivo actual de arriba cambió en
las primeras líneas del inicializador.

**El problema.** `ViewportScroller.scrollToAnchor` desplaza la ventana a la
posición del elemento menos un `offset` propio, cero por defecto; no lee la
propiedad CSS `scroll-padding-top`, que sí respetan los saltos nativos y el
foco. Con la barra fija, un enlace del menú dejaba la sección con su borde
superior en 0 px, tapada por la barra.

**La decisión.** Registrar el `offset` con `ViewportScroller.setOffset` y
leerlo de la propia hoja de estilos, no de una constante: la función consulta
`scroll-padding-top` de `<html>` cada vez que se necesita. Así hay una sola
fuente de verdad (`html` en `_base.scss`, que a su vez sigue la altura medida
de la barra), vale cero donde el encabezado no es fijo (`auto` se convierte en
0) y se actualiza sola si la barra cambia de altura. En el servidor no se
llama nunca: el `ViewportScroller` del servidor no hace nada.

### Errores comunes

- **Poner `overflow-x: clip` en el `body`** esperando bloquear el scroll
  horizontal del documento: en el viewport vale lo mismo que `hidden`.
- **Quitar el fragmento del selector** para evitar el salto: funciona en la
  portada, pero en una página de proyecto pierde el enlace al encabezado.
- **Hacer el scroll en `NavigationEnd`** en vez de en `Scroll`: la vista
  nueva puede no estar pintada todavía y el elemento no existe.
- **Ignorar `event.position`:** en atrás/adelante el salto al fragmento pisa
  la posición de lectura.
- **Leer `router.getCurrentNavigation()`** dentro del manejador: al llegar el
  evento `Scroll` la navegación ya terminó y devuelve `null`; hay que usar
  `lastSuccessfulNavigation()`.
- **Fiarse de `scroll-padding-top` con `scrollToAnchor`.** Los saltos nativos lo
  respetan; el método de Angular no. Con un encabezado fijo, la sección queda
  tapada. Se registra un `offset` con `setOffset` que lee la propiedad.

### Preguntas de entrevista (senior)

#### 1. La página «se corre» unos píxeles al navegar y vuelve al redimensionar. ¿Qué sospechas?

**Respuesta:**

Que el documento tiene scroll horizontal oculto y algo lo desplazó por
código. `overflow-x: hidden` en el `body` esconde un desborde (una fila con
margen negativo, un elemento transformado, una palabra larga) pero no impide
que `scrollTo`, `scrollIntoView` o el foco muevan el documento; el router de
Angular, al ir a un fragmento, llama a `scrollTo` con la x del elemento. Al
redimensionar, el navegador recalcula y vuelve a 0. Se confirma comparando
`document.documentElement.scrollWidth` con `clientWidth` y mirando
`scrollX` tras la navegación. La solución es quitar el desborde, no
esconderlo mejor.

#### 2. ¿Cómo evitas que una navegación concreta haga scroll al fragmento, manteniéndolo en las demás?

**Respuesta:**

El `anchorScrolling` del router es todo o nada, así que se reemplaza:
`withInMemoryScrolling()` sin opciones mantiene los eventos `Scroll` y un
inicializador los escucha y llama a `ViewportScroller.scrollToAnchor` (o
`scrollToPosition([0, 0])` para el fragmento de la primera sección) sólo
cuando corresponde. Para marcar la navegación que no debe saltar se usa
`info` en el `routerLink` o en `navigate`, un dato que viaja con la
navegación sin cambiar la URL, y se lee de
`router.lastSuccessfulNavigation().extras.info` al llegar el evento. También
se respeta `event.position`, que indica atrás/adelante.

#### 3. ¿Qué diferencia hay entre `state` e `info` en una navegación de Angular?

**Respuesta:**

`state` se guarda en la entrada del historial del navegador
(`history.state`): sobrevive a atrás/adelante y a una recarga, y tiene que
ser serializable. `info` vive sólo en el objeto `Navigation` de esa
navegación: no se persiste, admite cualquier valor y desaparece al terminar.
Para una instrucción puntual como «esta vez no hagas scroll», `info` es lo
correcto; `state` dejaría la marca en el historial y, al volver atrás, la
navegación la traería de nuevo.

<!-- /study-guide:section:sections-s3-fragment-scrolling -->

---

<!-- study-guide:section:sections-s4-section-title-about -->
## Módulo S4: El título de sección compartido y Sobre mí

Fuente: `src/app/shared/components/section-title/` y
`src/app/home/components/about/` del repositorio.

### El problema que resuelve

Todas las secciones de Portify abren igual: un `<span>` con el nombre de la
sección en gigante y casi transparente detrás, y un bloque `.section-title`
con una línea vertical a la izquierda, un `<h4>` pequeño arriba («Some Word
About me») y el `<h2>` grande. En la plantilla ese bloque está copiado en
cada sección, el `<h4>` va antes que el `<h2>` (los niveles de encabezado
saltan hacia atrás) y la línea la anima GSAP con una variable CSS. Sobre mí,
además, trae en Portify una fila de pares etiqueta/valor (correo, fecha de
nacimiento) y una tarjeta con «10 años de experiencia» en tres copias
giradas: cifras y datos que este sitio no publica.

### La decisión en este sitio

- Un componente `shared-section-title` con cinco entradas: `title`
  (obligatoria), `subtitle` (la línea pequeña, opcional), `overlay` (el
  texto de fondo; si no se pasa, repite el título), `headingId` (el `id`
  del encabezado, para que la sección pueda apuntarlo con `aria-labelledby`)
  y `level` (1 o 2; por defecto 2). `level` llegó con la página de la galería
  ([Parte 5, Módulo G3](05-galeria.md#módulo-g3-filtros-y-página)): la portada
  usa `<h2>` y esa página, cuyo primer encabezado es este, necesita un `<h1>`.
- El subtítulo es un `<p>`, no un `<h4>`: visualmente va encima, pero no es
  un encabezado de nivel 4 antes de un nivel 2.
- El texto de fondo lleva `aria-hidden="true"`: es decoración que repite el
  título.
- La línea vertical sigue siendo `--height: 100%`, lista para que GSAP la
  haga crecer después.
- Sobre mí es sólo texto: el cuerpo de `about.md` partido en párrafos, en
  una columna de ocho doceavos desde `lg`. Sin tarjeta de años ni datos de
  contacto: no se inventan cifras y el contacto tiene su sección.

### El código

`section-title.component.ts`:

```ts
import { Component, computed, input } from '@angular/core'

// Portify's section opener: a vertical line, an optional small line above the title and
// a huge faded copy of the title behind it. The hosting section stays `position: relative`
// so the overlay can sit at its top-left corner.
@Component({
  selector: 'shared-section-title',
  templateUrl: './section-title.component.html',
  styleUrl: './section-title.component.scss',
})
export class SectionTitleComponent {
  readonly title = input.required<string>()
  // Short line above the title, Portify's "Some Word About me". Omitted when empty.
  readonly subtitle = input<string>()
  // Text of the faded overlay; defaults to the title.
  readonly overlay = input<string>()
  // Id for the heading, so the section can point to it with aria-labelledby.
  readonly headingId = input<string>()
  // A section of the homepage is an <h2>; a page whose first heading is this one needs an <h1>.
  readonly level = input<1 | 2>(2)

  protected readonly overlayText = computed(() => this.overlay() ?? this.title())
}
```

`section-title.component.html`:


`section-title.component.scss`:


`about.component.ts`:

```ts
import { Component, computed, input } from '@angular/core'
import { ABOUT } from '@generated/about'
import { NextChapterComponent } from '@shared/components/next-chapter/next-chapter.component'
import { SectionTitleComponent } from '@shared/components/section-title/section-title.component'
import { Locale } from '@shared/interfaces/shared.interface'

@Component({
  selector: 'home-about',
  imports: [SectionTitleComponent, NextChapterComponent],
  templateUrl: './about.component.html',
  styleUrl: './about.component.scss',
})
export class AboutComponent {
  readonly locale = input.required<Locale>()
  protected readonly about = computed(() => ABOUT[this.locale()])
  protected readonly paragraphs = computed(() => this.about().body.split(/\n{2,}/))
}
```

`about.component.html`:


`about.component.scss`:


### Cómo funciona por dentro

- **`:host { display: block; position: relative }`.** El elemento
  `<shared-section-title>` no existe para el CSS del navegador: es `inline`
  y sin posición. Con `display: block` ocupa su fila y con
  `position: relative` el `.overlay-text` absoluto se coloca en su esquina,
  no en la de la página. La sección que lo aloja también es
  `position: relative` para que el texto gigante quede dentro de ella.
- **`input<string>()` sin `required`** declara una entrada opcional que vale
  `undefined` si no se pasa. `@if (subtitle(); as subtitle)` no pinta el
  `<p>` cuando no hay subtítulo, y `[attr.id]="headingId()"` no escribe el
  atributo cuando es `undefined`: un `id=""` vacío sería inválido.
- **`computed(() => this.overlay() ?? this.title())`**: el texto de fondo
  repite el título salvo que la sección pida otro.
- **Un solo `<h2>` por sección.** El subtítulo es un párrafo; así la
  jerarquía del documento es `<h1>` (nombre) y un `<h2>` por sección (seis
  aquí, siete con la Galería), y
  dentro de cada una los `<h3>` que hagan falta.
- **Los párrafos salen del Markdown.** El script de contenido deja el cuerpo
  de `about.md` como texto y el componente lo parte por líneas en blanco
  (`/\n{2,}/`). Para que eso funcione, el script normaliza los finales de
  línea de Windows (`\r\n`) a `\n` al leer: sin eso, la expresión no
  encontraba dos `\n` seguidos y toda la sección salía como un único
  párrafo.
- **`track $index`** vale aquí porque la lista no se reordena ni se edita:
  cambia entera al cambiar de idioma.

### Errores comunes

- **Olvidar `position: relative` en `:host`**: el texto gigante aparece en
  la esquina superior izquierda de la página, encima del logo.
- **Copiar el `<h4>` + `<h2>` de Portify.** Un `<h4>` antes del `<h2>` de la
  sección rompe el orden de encabezados que usan los lectores de pantalla
  para navegar.
- **`aria-labelledby` hacia un `id` que no se renderiza.** Si la sección
  pasa `aria-labelledby="about-heading"` pero olvida `headingId`, el
  atributo apunta a nada y la sección se anuncia sin nombre.
- **Párrafos pegados.** Un archivo Markdown con `\r\n` partía mal; se
  corrigió en el script, no en el componente, porque el problema es del
  contenido que entra, no de cómo se muestra.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué el texto de fondo lleva `aria-hidden` y el subtítulo no es un encabezado?

**Respuesta:**

El texto de fondo repite el título al 5 % de opacidad: quien no ve la
pantalla no gana nada oyéndolo dos veces, así que se oculta del árbol de
accesibilidad con `aria-hidden="true"`. El subtítulo sí se lee, pero no es
un encabezado: un encabezado define una sección del documento, y «Case
studies and personal projects» no abre una sección, introduce el título. Si
fuera `<h4>`, el orden sería `h4` y después `h2`, un salto hacia atrás que
confunde a quien navega por encabezados. La regla: el nivel lo decide la
estructura del documento, el tamaño lo decide el CSS.

#### 2. ¿Qué es `:host` en los estilos de un componente de Angular y cuándo hace falta?

**Respuesta:**

`:host` selecciona el elemento del propio componente (`<shared-section-title>`)
desde su hoja encapsulada; sin él, los estilos del componente sólo alcanzan a
su plantilla, no a su etiqueta. Hace falta cuando el componente necesita
comportarse como una caja: ser `display: block` (los elementos personalizados
nacen `inline`), establecer un contexto de posición para sus hijos absolutos,
o recibir un margen. La alternativa de ponerle una clase desde fuera obliga a
cada uso a recordarlo; con `:host` el componente se trae su propia caja.

#### 3. Un texto en Markdown se muestra como un único párrafo largo. ¿Qué sospechas y dónde lo arreglas?

**Respuesta:**

Que los finales de línea no son los que espera el código que parte el texto:
Windows guarda `\r\n` y una expresión que busca `\n\n` no encuentra nada. Se
confirma mirando los bytes del archivo o el resultado de `split`. Se arregla
en la entrada, normalizando a `\n` al leer el archivo, no en cada componente
que consuma el texto: el pipeline de contenido es el único sitio que sabe de
dónde vienen los archivos, y así ningún consumidor repite el parche.

<!-- /study-guide:section:sections-s4-section-title-about -->

---

<!-- study-guide:section:sections-s5-skills -->
## Módulo S5: Habilidades: filas numeradas y lista con regla

Fuente: `src/app/home/components/skills/`,
`src/app/home/interfaces/skills.interface.ts`, `content/en/skills.yml` y
`scripts/prepare-content.mjs` (`validateSkills`) del repositorio.

### El problema que resuelve

La sección de habilidades de Portify es la más rígida de la plantilla: tres
filas con gráficos radiales de ApexCharts cuyos porcentajes viven en
`app.js`, barras de progreso con el valor escrito dos veces (`<span>90%</span>`
y `data-width="90%"`) y una fila de idiomas que reutiliza las clases de la
primera y muestra los mismos números. Un «85 % en diseño» no significa nada
y no se puede justificar en una entrevista. Lo que sí vale de la plantilla
es la composición de cada fila: a la izquierda un título enmarcado con un
número girado (`01.-`), a la derecha el contenido.

### La decisión en este sitio

- Una fila por grupo de `skills.yml` más una fila de idiomas, numeradas en
  orden de lectura con el `SerialPipe` (`01.-`, `02.-`…).
- Cada habilidad es un `<li>` con una regla de 2 px debajo, en lugar de
  etiquetas con fondo: Janio las descartó porque parecen botones.
- Lo destacado (Angular, el inglés) sale en Barlow Condensed a mayor tamaño.
  Qué se destaca lo dice el contenido, con `featured: true` en el YAML de
  cada idioma; el componente no sabe de nombres concretos.
- Sin porcentajes, sin gráficos y, por ahora, sin iconos: los iconos de cada
  tecnología son un paso aparte.

### El código

Un fragmento de `content/en/skills.yml`: un ítem es una cadena o un objeto
con `text` y `featured`.

```yaml
groups:
  - id: frontend
    title: Frontend
    items:
      - text: Angular
        featured: true
      - text: TypeScript
        featured: true
      - RxJS
languages:
  - id: english
    name: English
    level: Professional working proficiency
    featured: true
```

`skills.interface.ts`:

```ts
export interface Skills {
  groups: SkillGroup[]
  languages: SkillLanguage[]
}

// Content shape, as generated from skills.yml; `featured` marks what the site highlights.
export interface SkillTag {
  text: string
  featured: boolean
}

export interface SkillGroup {
  id: string
  title: string
  items: SkillTag[]
}

export interface SkillLanguage {
  id: string
  name: string
  level: string
  featured: boolean
}
```

En `scripts/prepare-content.mjs`, `validateSkills` normaliza cada ítem a
`{ text, featured }` (una cadena pasa a `featured: false`), rechaza campos
desconocidos, un `featured` que no sea booleano y un `featured` puesto en el
grupo en vez de en el ítem. Dos pruebas de `prepare-content.test.mjs` lo
cubren.

`skills.component.ts`:

```ts
import { Component, computed, input } from '@angular/core'
import { SerialPipe } from '@shared/pipes/serial.pipe'
import { SKILLS } from '@generated/skills'
import { SkillGroup } from '@interfaces/skills.interface'
import { NextChapterComponent } from '@shared/components/next-chapter/next-chapter.component'
import { SectionTitleComponent } from '@shared/components/section-title/section-title.component'
import { Locale } from '@shared/interfaces/shared.interface'

@Component({
  selector: 'home-skills',
  imports: [SectionTitleComponent, NextChapterComponent, SerialPipe],
  templateUrl: './skills.component.html',
  styleUrl: './skills.component.scss',
})
export class SkillsComponent {
  readonly locale = input.required<Locale>()
  protected readonly skills = computed(() => SKILLS[this.locale()])

  protected readonly labels = computed(() =>
    this.locale() === 'es'
      ? { title: 'Habilidades', languages: 'Idiomas' }
      : { title: 'Skills', languages: 'Languages' },
  )

  // One row per group, then the languages, numbered in reading order like Portify's "01.-".
  protected readonly rows = computed<SkillGroup[]>(() => {
    const { groups, languages } = this.skills()
    const languageRow = {
      id: 'languages',
      title: this.labels().languages,
      items: languages.map((language) => ({
        text: `${language.name} · ${language.level}`,
        featured: language.featured,
      })),
    }
    return [...groups, languageRow].map((group) => ({
      id: group.id,
      title: group.title,
      items: group.items,
    }))
  })
}
```

`skills.component.html`:


`skills.component.scss`:


### Cómo funciona por dentro

- **`rows` une dos listas distintas en una sola forma.** Los grupos ya
  tienen `items` con `text` y `featured`; los idiomas no, así que el
  `computed` fabrica una fila más con `«English · Professional working proficiency»` como texto.
  La plantilla sólo conoce `SkillGroup` y pinta todas las filas igual.
- **`[class.featured]="item.featured"`** añade la clase cuando el valor es
  `true`. El dato viene del YAML, pasado por el validador: si alguien
  escribe `featured: yes`, el script falla antes de llegar aquí.
- **`$index | serial: '.-'`** numera cada fila desde su posición en el
  `@for`; el argumento tras los dos puntos es el sufijo (Módulo S6).
  `aria-hidden` en el número: es decoración, el título ya identifica la
  fila.
- **La regla de 2 px** es `border-bottom` en cada `<li>`; `gap-3`
  (utilidad de Bootstrap, 16 px) separa los ítems sin margen en el último.
  La lista lleva `list-style: none` y `padding: 0` escritos a mano porque
  `list-unstyled` vive en el parcial `type` de Bootstrap, que este sitio no
  importa (Parte 2, Módulo E1).
- **El número girado** usa `rotate(-90deg)` con una traslación para
  alinearlo con el marco del título; `display: inline-block` es necesario
  porque un `<span>` en línea no acepta `transform`.
- **El `featured` por idioma.** Una primera versión destacaba comparando el
  texto con una lista de nombres en inglés y en español se perdía todo. La
  marca en el contenido de cada idioma evita acoplar el componente a
  cadenas concretas.

### Errores comunes

- **Destacar por texto** («si el ítem dice Angular…»): funciona en un idioma
  y falla en el otro, o al corregir una mayúscula.
- **Poner `featured` en el grupo.** El validador lo rechaza con un mensaje
  claro: pertenece a los ítems.
- **Usar `list-unstyled`** y ver viñetas: la clase no existe sin el parcial
  `type`. Pasó otra vez con las etiquetas de Proyectos (Módulo S7).
- **Inventar porcentajes** para parecerse a la plantilla. No se pueden
  defender y los lectores de pantalla los anuncian como datos.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué un porcentaje de habilidad es mala idea, más allá del gusto?

**Respuesta:**

Porque no mide nada: no hay escala ni referencia, y «90 % en TypeScript»
no distingue a quien lleva un año de quien lleva diez. Un reclutador técnico
lo lee como relleno y, si pregunta de dónde sale, no hay respuesta. Además
tiene coste de accesibilidad: una barra de progreso anuncia un valor que no
significa nada y los gráficos de la plantilla ni siquiera llevan texto
alternativo. Es más útil decir qué se hizo con cada tecnología (eso va en
Experiencia y Proyectos) y marcar la especialidad.

#### 2. Un dato como `featured` ¿vive en el contenido o en el componente?

**Respuesta:**

En el contenido, cuando decide **qué** se muestra; en el componente, cuando
decide **cómo**. «Angular es la especialidad» es editorial: puede cambiar
con el tiempo y cambia con el idioma, así que va en el YAML, por idioma, y
el componente sólo aplica una clase. Si la lista de destacados estuviera en
TypeScript, cambiarla sería un cambio de código y habría que mantener dos
listas, una por idioma. La contrapartida es validar: un valor que viene de
un archivo tiene que comprobarse al leerlo, no confiarse al tipo.

#### 3. ¿Cuándo `track $index` es aceptable en un `@for` y cuándo no?

**Respuesta:**

`track` le dice a Angular cómo reconocer cada elemento entre dos renders
para reutilizar su DOM. Con `$index`, el tercer elemento siempre es «el
tercero»: si la lista se reordena o se borra uno del medio, Angular
reescribe el contenido de los nodos en vez de moverlos, y se pierde estado
local (un foco, una animación en curso, un `<input>` escrito). Es aceptable
cuando la lista es estática o se reemplaza entera (cambiar de idioma) y los
elementos no tienen estado. Con identidad propia, como las filas con `id`,
se usa esa identidad.

<!-- /study-guide:section:sections-s5-skills -->

---

<!-- study-guide:section:sections-s6-experience-pipes -->
## Módulo S6: Experiencia y los pipes month y serial

Fuente: `src/app/home/components/experience/`, `src/app/shared/pipes/` y
`src/app/app.spec.ts` del repositorio.

### El problema que resuelve

La cronología de Portify es una lista con una línea gris de toda la altura
y un tramo negro por entrada, los dos dibujados con variables CSS que GSAP
anima al hacer scroll. El contenido ya existía (`experience.yml`, con
`startDate` y `endDate` como `YYYY-MM`), pero las fechas se mostraban tal
cual, «2026-05», desde el primer pipeline de contenido. Y la numeración
`01`, `02` se repetía en tres sitios (el menú, el contador «Next chapter» y
las filas de Habilidades), primero con `padStart` en cada componente y
después con una función `serial()` compartida que cada plantilla tenía que
llamar desde TypeScript.

### La decisión en este sitio

- La cronología es un `<ol>` (el orden importa) con dos variables:
  `--height` en la lista y `--item-height` en cada entrada, al 100 % hasta
  que GSAP las anime. Cada entrada muestra período, rol (`<h3>`),
  organización y las contribuciones como lista.
- `MonthPipe` formatea `YYYY-MM` con `Intl.DateTimeFormat` del navegador en
  el idioma de la página («Jan 2025», «ene 2025»), en UTC.
- `SerialPipe` sustituye a la función: `{{ $index | serial }}` da «01» y
  `{{ $index | serial: '.-' }}` da «01.-».
- Regla acordada con Janio: **pipe** cuando un valor se transforma sólo para
  mostrarse; **función** cuando TypeScript consume el resultado, necesita
  inyección de dependencias o corre fuera de Angular (el script de
  contenido).
- Sin botón de descarga del CV en esta etapa; llegó después, con los PDF (Módulo S1,
  «Después: los botones de descarga del CV»).
- Pruebas: una por pipe y un caso en `app.spec.ts` que renderiza la portada
  en cada idioma y comprueba los períodos.

### El código

`month.pipe.ts`:

```ts
import { Pipe, PipeTransform } from '@angular/core'
import { Locale } from '@shared/interfaces/shared.interface'

// Formats a content date ('YYYY-MM') as month and year in the given locale:
// '2025-01' -> 'Jan 2025' in English, 'ene 2025' in Spanish. UTC avoids the
// previous-day shift that a local midnight would cause west of Greenwich.
@Pipe({ name: 'month' })
export class MonthPipe implements PipeTransform {
  transform(yearMonth: string, locale: Locale): string {
    const [year, month] = yearMonth.split('-').map(Number)
    return new Intl.DateTimeFormat(locale, {
      month: 'short',
      year: 'numeric',
      timeZone: 'UTC',
    }).format(Date.UTC(year, month - 1, 1))
  }
}
```

`serial.pipe.ts`:

```ts
import { Pipe, PipeTransform } from '@angular/core'

// Two-digit ordinal for a zero-based index: 0 -> "01", or "01.-" with a suffix.
// Portify numbers the menu links, the "Next chapter" counter and the skill rows this way.
@Pipe({ name: 'serial' })
export class SerialPipe implements PipeTransform {
  transform(index: number, suffix = ''): string {
    return `${String(index + 1).padStart(2, '0')}${suffix}`
  }
}
```

Sus pruebas, `month.pipe.spec.ts` y `serial.pipe.spec.ts`:

```ts
import { MonthPipe } from './month.pipe'

describe('MonthPipe', () => {
  const pipe = new MonthPipe()

  it('formats a content month per locale', () => {
    expect(pipe.transform('2025-01', 'en')).toBe('Jan 2025')
    expect(pipe.transform('2025-01', 'es')).toBe('ene 2025')
  })

  it('does not slip to the previous month west of Greenwich', () => {
    expect(pipe.transform('2026-05', 'en')).toBe('May 2026')
    expect(pipe.transform('2017-10', 'es')).toBe('oct 2017')
  })
})
```

```ts
import { SerialPipe } from './serial.pipe'

describe('SerialPipe', () => {
  const pipe = new SerialPipe()

  it('pads a zero-based index to two digits', () => {
    expect(pipe.transform(0)).toBe('01')
    expect(pipe.transform(5)).toBe('06')
    expect(pipe.transform(9)).toBe('10')
  })

  it('appends the suffix used by the skill rows', () => {
    expect(pipe.transform(0, '.-')).toBe('01.-')
  })
})
```

`experience.component.ts`:

```ts
import { Component, computed, input } from '@angular/core'
import { EXPERIENCE } from '@generated/experience'
import { NextChapterComponent } from '@shared/components/next-chapter/next-chapter.component'
import { SectionTitleComponent } from '@shared/components/section-title/section-title.component'
import { Locale } from '@shared/interfaces/shared.interface'
import { MonthPipe } from '@shared/pipes/month.pipe'

@Component({
  selector: 'home-experience',
  imports: [SectionTitleComponent, NextChapterComponent, MonthPipe],
  templateUrl: './experience.component.html',
  styleUrl: './experience.component.scss',
})
export class ExperienceComponent {
  readonly locale = input.required<Locale>()
  protected readonly experience = computed(() => EXPERIENCE[this.locale()])

  protected readonly labels = computed(() =>
    this.locale() === 'es'
      ? { title: 'Experiencia', present: 'Actualidad' }
      : { title: 'Experience', present: 'Present' },
  )
}
```

`experience.component.html`:


`experience.component.scss`:


El caso de `app.spec.ts` que cubre los períodos:

```ts
it.each([
  ['en', 'May 2026 – Present', 'Oct 2017 – Aug 2021'],
  ['es', 'may 2026 – Actualidad', 'oct 2017 – ago 2021'],
])('renders the experience timeline with readable periods in %s', async (locale, first, last) => {
  const fixture = TestBed.createComponent(App)
  const router = TestBed.inject(Router)
  fixture.detectChanges()
  await router.navigateByUrl(`/${locale}`)
  fixture.detectChanges()

  const periods = [
    ...(fixture.nativeElement as HTMLElement).querySelectorAll('home-experience .period'),
  ].map((period) => period.textContent?.replace(/\s+/g, ' ').trim())
  expect(periods).toHaveLength(4)
  expect(periods[0]).toBe(first)
  expect(periods[3]).toBe(last)
})
```

### Cómo funciona por dentro

- **Un pipe es una clase con `transform`.** `@Pipe({ name: 'month' })` le da
  el nombre que se usa en la plantilla; como es *standalone*, cada componente
  lo añade a sus `imports`. Los argumentos tras los dos puntos
  (`serial: '.-'`) llegan como parámetros adicionales de `transform`.
- **Los pipes son puros por defecto**: Angular guarda el último resultado y
  sólo vuelve a llamar a `transform` si cambian las entradas. Por eso
  `{{ item.startDate | month: locale() }}` no cuesta nada en cada detección
  de cambios, aunque cree un `Intl.DateTimeFormat` por llamada.
- **`Intl.DateTimeFormat(locale, { month: 'short', year: 'numeric' })`** usa
  los datos de idioma del navegador (o de Node en el prerenderizado): «Jan»
  en inglés y «ene» en español, en minúscula, porque así lo escribe el
  español. No hace falta registrar datos de locale ni empaquetarlos.
- **Por qué UTC.** `'2026-05'` no se convierte con `new Date(...)`: esa
  cadena se interpreta como medianoche UTC, y si después se formatea en la
  zona local de Buenos Aires (UTC-3) son las 21:00 del 30 de abril, o sea
  «Apr». El pipe construye la fecha con `Date.UTC` y formatea con
  `timeZone: 'UTC'`, así el resultado no depende de dónde corra. La segunda
  prueba del pipe existe para esto.
- **Por qué no el `DatePipe` de Angular.** Funcionaría en inglés, pero para
  «ene 2025» exige `registerLocaleData(localeEs)` y meter los datos de
  locale en el paquete. `Intl` ya está en el navegador.
- **`<ol>` y no `<div>`**: una cronología es una lista ordenada. El estilo
  quita las viñetas (`list-style: none`) y Bootstrap el margen.
- **La regla «pipe o función».** `MonthPipe` y `SerialPipe` producen texto
  para mostrar: pipe. `localeFromUrl` produce un valor que usa TypeScript
  para decidir rutas: función. El validador del contenido corre en Node, sin
  Angular: función. Si mañana hace falta la fecha formateada en TypeScript
  (para un `title`), se instancia el pipe o se extrae la lógica a una función
  que el pipe llame.
- **La prueba de los períodos** renderiza `App` entera, navega a `/en` y
  lee los `.period` con los espacios normalizados (`replace(/\s+/g, ' ')`),
  porque la plantilla parte el texto en varias líneas. Antes de este cambio
  ninguna prueba tocaba las fechas; se comprobó que falla rompiendo a
  propósito la expresión de espacios.

### Errores comunes

- **`new Date('2026-05')` y formatear en local**: un mes de menos al oeste
  de Greenwich. Se ve en la máquina de quien vive en América y no en la CI
  en UTC, o al revés.
- **Una función `serial()` llamada desde TypeScript** para cada plantilla:
  obliga a preparar listas intermedias (`SkillRow`) sólo para numerar. Con
  el pipe, la plantilla numera desde `$index` y las listas intermedias
  desaparecen.
- **`DatePipe` sin registrar el locale**: lanza un error en tiempo de
  ejecución al pedir `'es'`.
- **Dar por hecho que una prueba de integración cubre los formatos de fecha.**
  Abre las aserciones y comprueba qué casos verifican. Las pruebas de los pipes
  y la prueba que renderiza la portada responden preguntas distintas.

### Preguntas de entrevista (senior)

#### 1. ¿Cuándo escribes un pipe y cuándo una función?

**Respuesta:**

Un pipe cuando el valor se transforma únicamente para mostrarse en una
plantilla: formato de fecha, número, mayúsculas, un sufijo. Gana en
legibilidad (`valor | month: locale`), se memoriza solo y se declara una
vez. Una función cuando el resultado lo consume TypeScript (una decisión,
una ruta, un cálculo que alimenta otro), cuando necesita inyección de
dependencias con más contexto o cuando tiene que correr fuera de Angular,
como en un script de Node. Si las dos cosas pasan, la lógica va en una
función pura y el pipe la envuelve: nunca al revés, porque un pipe no se
puede llamar desde Node.

#### 2. ¿Por qué una fecha puede salir con un día o un mes de menos y cómo lo evitas?

**Respuesta:**

Porque una fecha sin hora se interpreta como medianoche en alguna zona
(`'2026-05'` o `'2026-05-01'` en UTC según la especificación) y se muestra
en otra. Al oeste de Greenwich, medianoche UTC es la noche del día anterior,
y el 1 de mayo se convierte en 30 de abril. Se evita decidiendo una zona en
los dos pasos: construir con `Date.UTC` y formatear con `timeZone: 'UTC'`,
o trabajar con año y mes como números sin pasar por `Date`. Y se cubre con
una prueba cuyo resultado dependería de la zona si el código estuviera mal.

#### 3. ¿Qué es un pipe puro y qué implica para el rendimiento?

**Respuesta:**

Un pipe puro (`pure: true`, el valor por defecto) promete que para las
mismas entradas devuelve el mismo resultado, así que Angular guarda la
última entrada y la última salida y sólo llama a `transform` cuando una
entrada cambia por referencia o por valor primitivo. Es barato aunque se use
en listas largas. Un pipe impuro se ejecuta en cada detección de cambios,
como `async`, y conviene reservarlo para cuando la salida depende de algo
externo a sus argumentos. La trampa es mutar un objeto que se pasa a un pipe
puro: la referencia no cambia y el pipe no se entera.

<!-- /study-guide:section:sections-s6-experience-pipes -->

---

<!-- study-guide:section:sections-s7-projects -->
## Módulo S7: Proyectos: tarjetas y página de detalle

Fuente: `src/app/home/components/projects/`,
`src/app/home/pages/project-page/`,
`src/app/home/constants/project.constants.ts`, `src/app/app.routes.ts` y
`content/en/projects/` del repositorio. Para publicar un proyecto nuevo
sigue [Agregar un proyecto](agregar-un-proyecto.md).

### El problema que resuelve

Portify muestra tres tarjetas con imagen vertical, un efecto al pasar el
ratón (la imagen encoge, dos marcos inclinados aparecen y una flecha
redonda surge en el centro) y debajo título, categoría y etiquetas. Las tres
abren **el mismo modal** a pantalla completa: `app.js` cambia el título y la
imagen grande y todo lo demás (objetivos, ficha de cliente, galería,
resultado y un segundo formulario) es texto fijo. Este sitio ya tenía
páginas por proyecto con rutas `/en/projects/<slug>` generadas desde el
contenido (Markdown con front matter), pero sin estilo; y, con un solo
proyecto, una rejilla de tres columnas dejaba la tarjeta sola en un tercio
de la fila.

### La decisión en este sitio

- **Tarjeta como fila**: la imagen en `col-md-5 col-xl-4` y el texto al
  lado (título, tipo, tecnologías y resumen); por debajo de `md` la imagen
  ocupa todo el ancho y el texto baja. Con más proyectos, una fila por
  proyecto separada 60 px.
- **El efecto de Portify** en el enlace de la imagen, y también con el foco
  del teclado (`:focus-visible`). La flecha es el SVG de Phosphor
  `arrow-up-right` inline, como en el Módulo S2.
- **Dos enlaces al mismo destino**: la imagen, nombrada por su `coverAlt`,
  y el título en un `<h3>`. Pasar el ratón por el texto también encoge la
  imagen, como en la plantilla.
- **La página de detalle traduce el modal**: la portada como franja ancha
  arriba, el título, el resumen y el cuerpo del Markdown en
  `col-md-7 col-xl-9`, y una barra lateral pegajosa con tipo, rol,
  tecnologías y enlaces en `col-md-5 col-xl-3`. Sin ficha de cliente ni
  fechas: no se piden campos que un proyecto personal no tiene.
- **Los `h2` del cuerpo en Barlow Condensed Italic 400**, un peso menos que
  los títulos de sección, por decisión de Janio.
- **Las etiquetas por idioma** (`PROJECT_TYPE_LABELS`, `PROJECT_LABELS`) en
  un archivo de constantes del módulo `home`, compartido por la tarjeta y la
  página.
- **Portada**: `public/images/projects/<slug>.jpg` a 830 × 956 (el doble de
  los 415 × 478 de Portify), declarada con `cover` y `coverAlt` en el front
  matter de cada idioma.

### El código

`project.constants.ts`:

```ts
import { InjectionToken } from '@angular/core'
import { PROJECTS } from '@generated/projects'
import type { Project, ProjectLabel } from '@interfaces/project.interface'
import { Locale } from '@shared/interfaces/shared.interface'

export const PROJECT_TYPE_LABELS: Record<Locale, Record<Project['type'], string>> = {
  en: { professional: 'Professional', personal: 'Personal', learning: 'Learning' },
  es: { professional: 'Profesional', personal: 'Personal', learning: 'Aprendizaje' },
}

export const PROJECT_LABELS: Record<Locale, Record<ProjectLabel, string>> = {
  en: { back: 'Back to projects', type: 'Type', role: 'Role', stack: 'Stack', links: 'Links' },
  es: {
    back: 'Volver a proyectos',
    type: 'Tipo',
    role: 'Rol',
    stack: 'Tecnologías',
    links: 'Enlaces',
  },
}

// The generated index behind the cards. A token so a test can supply projects the
// content does not have, such as one without a cover.
export const PROJECT_CATALOG = new InjectionToken<Record<Locale, Project[]>>('PROJECT_CATALOG', {
  providedIn: 'root',
  factory: () => PROJECTS,
})
```

`ProjectLabel` es un tipo de `project.interface.ts`:
`'back' | 'type' | 'role' | 'stack' | 'links'`.

`projects.component.ts`:

```ts
import { Component, computed, inject, input } from '@angular/core'
import { RouterLink } from '@angular/router'
import { PROJECT_CATALOG, PROJECT_TYPE_LABELS } from '@home/constants/project.constants'
import { NextChapterComponent } from '@shared/components/next-chapter/next-chapter.component'
import { SectionTitleComponent } from '@shared/components/section-title/section-title.component'
import { Locale } from '@shared/interfaces/shared.interface'

@Component({
  selector: 'home-projects',
  imports: [RouterLink, SectionTitleComponent, NextChapterComponent],
  templateUrl: './projects.component.html',
  styleUrl: './projects.component.scss',
})
export class ProjectsComponent {
  readonly locale = input.required<Locale>()
  private readonly catalog = inject(PROJECT_CATALOG)

  protected readonly labels = computed(() =>
    this.locale() === 'es'
      ? { title: 'Proyectos', subtitle: 'Casos de estudio y proyectos personales' }
      : { title: 'Projects', subtitle: 'Case studies and personal projects' },
  )

  protected readonly projects = computed(() => {
    const locale = this.locale()
    return this.catalog[locale].map((project) => ({
      ...project,
      typeLabel: PROJECT_TYPE_LABELS[locale][project.type],
    }))
  })
}
```

`projects.component.html`:


`projects.component.scss`:


`project-page.component.ts`:

```ts
import { Component, inject, ViewEncapsulation } from '@angular/core'
import { ActivatedRoute, RouterLink } from '@angular/router'
import { PROJECT_BODIES } from '@generated/project-bodies'
import { PROJECT_LABELS, PROJECT_TYPE_LABELS } from '@home/constants/project.constants'
import { Project } from '@interfaces/project.interface'
import { Locale } from '@shared/interfaces/shared.interface'

@Component({
  selector: 'home-project-page',
  imports: [RouterLink],
  templateUrl: './project-page.component.html',
  styleUrl: './project-page.component.scss',
  // The Markdown body arrives through [innerHTML], so its headings and paragraphs carry
  // no Angular scoping attribute. The styles are global and nested under .project-page.
  encapsulation: ViewEncapsulation.None,
})
export class ProjectPageComponent {
  private readonly route = inject(ActivatedRoute).snapshot
  protected readonly locale = this.route.data['locale'] as Locale
  protected readonly project = this.route.data['project'] as Project
  protected readonly body = PROJECT_BODIES[this.locale][this.project.slug]
  protected readonly labels = PROJECT_LABELS[this.locale]
  protected readonly typeLabel = PROJECT_TYPE_LABELS[this.locale][this.project.type]
  protected readonly stack = this.project.stack.join(', ')
}
```

`project-page.component.html`:


`project-page.component.scss`:


Las rutas ya existían (`src/app/app.routes.ts`): por cada idioma y cada
proyecto del índice generado se crea una ruta `${locale}/projects/${slug}`
con `loadComponent` perezoso y los datos del proyecto en `data`; el
prerenderizado las recorre y escribe un `index.html` por ruta.

### Cómo funciona por dentro

- **El efecto de la tarjeta sin JavaScript.** `.project-card` es un `<a>`
  en `display: flex` con la imagen centrada; `::before` y `::after` son dos
  marcos del mismo tamaño (`inset: 0`) con opacidad 0 que, al pasar el
  ratón, giran 3,5° en sentidos opuestos y aparecen. `.card-inner` es un
  fondo amarillo entre los marcos y la imagen, para que los marcos se lean
  como hojas detrás. La flecha usa la propiedad `scale` (no la función
  `transform: scale()`), que se anima aparte del giro. `:focus-visible`
  activa lo mismo con el teclado: el enlace de la imagen no puede ser
  invisible para quien navega con Tab.
- **El `scale(0.97)` de toda la tarjeta** se dispara desde el `<article>`
  (`.single-project:hover .project-card`), así que pasar el ratón por el
  texto también encoge la imagen, como en Portify.
- **Dos enlaces, dos nombres.** La imagen enlaza con el nombre accesible de
  su `alt` (el `coverAlt` del contenido) y el `<h3>` con el título. Son
  destinos iguales con nombres distintos y descriptivos; un lector de
  pantalla los lista como «Portada de la guía…» y «De comentarios en el
  código…», ambos útiles. La flecha va con `aria-hidden`.
- **`@if (project.cover)` envuelve la columna entera de la imagen.** Una
  primera versión dejaba el `<a class="project-card">` siempre y sólo
  condicionaba el `<img>`: para un proyecto sin portada quedaba un enlace
  enfocable sin nombre accesible ni contenido visible. Ahora, sin portada no
  hay enlace de imagen y el título sigue
  enlazando. El validador exige `cover` y `coverAlt` juntos; hoy todos los
  proyectos llevan portada.
- **`PROJECT_CATALOG`** es un `InjectionToken` cuyo valor por defecto es el
  índice generado. El componente lo inyecta en vez de importar `PROJECTS`,
  y así `projects.component.spec.ts` puede darle dos proyectos de prueba,
  uno sin portada, y comprobar los enlaces de cada tarjeta.
- **Las etiquetas de tecnologías** son un `<ul>` con `list-style: none` y
  `padding: 0` escritos (otra vez, `list-unstyled` no existe sin el parcial
  `type`) y un guion generado con `li + li::before`, el separador de
  Portify. Con `flex-wrap`, cuando la lista salta de línea el guion queda al
  principio de la segunda; es aceptable.
- **La franja de la página.** La portada es vertical (830 × 956) y el modal
  de Portify usa una imagen de 1199 × 505. En vez de pedir dos imágenes,
  `aspect-ratio: 1199 / 505` fija la caja, `object-fit: cover` recorta y
  `object-position: top` deja la parte superior, que es donde está lo
  importante en una captura. Los atributos `width`/`height` del `<img>`
  siguen evitando el salto de diseño mientras carga.
- **`ViewEncapsulation.None`.** El cuerpo llega por `[innerHTML]`: Angular
  lo inserta ya como HTML, sin el atributo `_ngcontent-xxx` que pone a los
  elementos de la plantilla, así que una regla encapsulada
  `.body h2[_ngcontent-xxx]` no lo alcanza. Con `None` los estilos del
  componente se inyectan tal cual, globales; para que no pisen nada, todos
  cuelgan de `.project-page`, una clase que sólo usa esta página. Es la
  alternativa a `::ng-deep`, que está en desuso.
- **`[innerHTML]` pasa por el sanitizador** de Angular: el HTML viene de
  Marked a partir del Markdown del repositorio, pero igual se eliminan
  `<script>` y atributos `on*`. No se desactiva con `bypassSecurityTrust…`.
- **`<dl>` para la barra lateral.** Pares etiqueta/valor son una lista de
  definiciones: `<dt>` es el nombre («Role») y `<dd>` el valor. En Portify
  eran `<p>` y `<h6>`; un `<h6>` ahí sería un encabezado sin sección.
- **`position: sticky` dentro de una columna de Bootstrap.** La columna
  derecha se estira a la altura de la fila (flex por defecto), así que la
  barra tiene recorrido para quedarse a 24 px del borde mientras el cuerpo
  hace scroll. Por debajo de `md` va apilada y no es pegajosa.
- **Las etiquetas en constantes.** `PROJECT_TYPE_LABELS` la usan la tarjeta
  y la página; sacarla de `projects.component.ts` a
  `home/constants/project.constants.ts` evitó una copia. El alias es
  `@home/...`, no `@app/home/...` (Parte 2, Módulo E5).
- **El cuerpo en Barlow Italic 400.** Los `h2` ya salían en Barlow Condensed
  por las variables de Bootstrap, en SemiBold 600; `font-weight: 400` los
  baja al peso regular cargado en la Parte 1, un escalón por debajo del
  título de la página.

### Después: las aplicaciones publicadas de un proyecto

Esta subsección es una etapa posterior (14 de noviembre de 2026). El código de
arriba es el de cuando el módulo se construyó; esto es lo que se le sumó.

**El problema.** El proyecto de la guía de Angular viene con ocho aplicaciones
de práctica, cada una publicada en su propia dirección. El detalle contaba que
existían, pero quien lo leía no tenía cómo abrirlas sin buscar sus direcciones
por otro lado.

**La decisión.** Una lista en el detalle, con el nombre de cada aplicación como
enlace y una descripción breve. Los datos viven en el **front matter** del
proyecto, en un campo opcional `deployments`, y no como una lista dentro del
cuerpo en Markdown. Así el script puede validarlos (nombre, descripción y una
dirección `https://` o `http://` en cada entrada) y los dos idiomas tienen que
listar las mismas direcciones.

El campo, en el archivo en inglés (las descripciones van entre comillas porque
llevan dos puntos):

```yaml
deployments:
  - name: Bases
    url: https://angular-basics.reskyon.com
    description: "The basics of Angular in one small app: standalone components, signals, inputs and outputs, lazy routes and a service that keeps its state in the browser."
  - name: GifsApp
    url: https://angular-gifs.reskyon.com
    description: "A GIF browser built on the Giphy API, with a service that keeps its state in signals."
  ...
```

Lo que comprueba el script:

```js
  // Published apps of the project: a name, a short description and an address each.
  if (
    data.deployments !== undefined &&
    (!Array.isArray(data.deployments) ||
      data.deployments.length === 0 ||
      !data.deployments.every(
        (deployment) =>
          isText(deployment?.name) &&
          isText(deployment?.description) &&
          isText(deployment?.url) &&
          ['https:', 'http:'].includes(URL.parse(deployment.url)?.protocol),
      ))
  ) {
    fail('"deployments" must be a non-empty list of names, descriptions and HTTP or HTTPS URLs.')
  }
```

La plantilla de la página, justo después del cuerpo, y solo si hay aplicaciones:


Y sus estilos, dentro de `.project-page`:


El título de la lista sale de `PROJECT_LABELS` («Apps online» / «Aplicaciones en
línea»), con un valor más en `ProjectLabel`. La lista sale a dos columnas desde
el ancho de escritorio. El número que anunciaba el texto del proyecto («siete
aplicaciones») pasó a ocho al comprobar cuántas había publicadas.

### Errores comunes

- **Dejar la rejilla de tres columnas** con un solo proyecto: la tarjeta
  queda sola en un tercio de la fila y el resumen no cabe.
- **`list-unstyled`** en las etiquetas: viñetas. Se vio al aplicar el paso
  a paso.
- **`@app/home/...`** como ruta de importación cuando existe `@home/...`;
  funciona, pero rompe la convención de alias.
- **Duplicar `PROJECT_TYPE_LABELS`** en la tarjeta y la página: la segunda
  copia apareció al crear la constante compartida sin borrar la local.
- **Usar `::ng-deep`** para llegar al `innerHTML`: funciona hoy, pero está
  marcado como obsoleto y el selector se cuela fuera del componente igual.
- **Estirar la portada vertical** a la franja sin `object-fit`: la imagen se
  deforma; con `object-fit: cover` pero sin `object-position`, se centra y
  recorta la cabecera.
- **Un `<a>` dentro de otro `<a>`** para hacer clicable toda la tarjeta con
  el título también enlazado: HTML inválido. Por eso son dos enlaces
  hermanos.

### Preguntas de entrevista (senior)

#### 1. Un bloque de HTML que viene de `[innerHTML]` no toma los estilos del componente. ¿Por qué y qué opciones hay?

**Respuesta:**

La encapsulación emulada de Angular reescribe los selectores del componente
con un atributo (`h2[_ngcontent-xxx]`) y añade ese atributo a los elementos
de la plantilla al compilarla. Lo que entra por `innerHTML` se inserta en
tiempo de ejecución como HTML plano, sin atributos, y los selectores no
coinciden. Opciones: `::ng-deep` (obsoleto y se filtra fuera del
componente), una hoja global (pierde la cercanía con el componente), o
`ViewEncapsulation.None` con todas las reglas anidadas bajo una clase raíz
propia, que es lo mismo que una hoja global pero viviendo con el componente
y sin riesgo de colisión si la clase es única. Aquí se eligió la última.

#### 2. Una tarjeta con imagen y título que llevan al mismo sitio: ¿un enlace que envuelve todo o dos?

**Respuesta:**

Dos enlaces hermanos. Un solo `<a>` que envuelva imagen y texto es válido en
HTML5, pero su nombre accesible es todo el texto interior (título, tipo,
tecnologías, resumen) y se anuncia como un párrafo entero; y si el título
también tiene que ser enlace, un `<a>` dentro de otro es inválido. Con dos
enlaces, cada uno tiene un nombre corto y descriptivo: el de la imagen, su
`alt`; el del título, el título. El coste es una parada de tabulador más
por tarjeta, aceptable para pocas tarjetas. Si fueran muchas, haría la
imagen decorativa (`alt=""`, `tabindex="-1"`) y dejaría un solo enlace en el
título.

#### 3. ¿Cómo aparecen las rutas de cada proyecto si nadie las escribe en el router?

**Respuesta:**

El script de contenido genera un índice (`PROJECTS`) por idioma a partir de
los archivos Markdown, y `app.routes.ts` lo recorre al definir `routes`:
una ruta por idioma y `slug`, con `loadComponent` para cargar la página de
detalle de forma perezosa y los datos del proyecto en `data`, de donde la
página los lee por `ActivatedRoute`. Como `routes` se evalúa al arrancar,
cualquier archivo nuevo en `content/` se convierte en ruta en el siguiente
`npm start` o `npm run build`. El prerenderizado descubre esas rutas y
escribe un `index.html` por cada una, que Nginx sirve como archivo estático
sin pasar por la aplicación.

<!-- /study-guide:section:sections-s7-projects -->

---

<!-- study-guide:section:sections-s8-contact -->
## Módulo S8: Contacto sin formulario ni correo

Fuente: `src/app/home/components/contact/`, `content/en/profile.yml` y
`scripts/prepare-content.mjs` (`validateProfile`) del repositorio.

### El problema que resuelve

La sección de contacto de Portify tiene cuatro ítems con icono redondo
(teléfono, correo, dirección y redes) y un formulario que envía por EmailJS
con tres claves escritas en `app.js`. Este sitio decidió en noviembre de
2026 no publicar correo ni formulario: el contacto es por LinkedIn, y la
validación del contenido exige un enlace con `id: linkedin`. De la plantilla
sirven la composición de los ítems (círculo con icono y texto al lado) y los
iconos sociales redondos que se rellenan de negro al pasar el ratón; el
resto se descarta. Además el sitio de Reskyon está en construcción y su
enlace tenía que desaparecer sin borrarlo del contenido.

### La decisión en este sitio

- Título compartido con subtítulo («Let's get in touch» / «Hablemos»), y el
  título de la sección desde `profile.yml` como hasta ahora.
- Dos ítems de Portify: ubicación y disponibilidad, con los iconos de
  Phosphor `map-pin` y `globe-hemisphere-west` inline en un círculo de 60 px
  (80 desde `lg`), decorativos (`aria-hidden`).
- El mensaje y la llamada a la acción como botón `btn btn-secondary`, el
  mismo del hero, con `rel="me"`: es el enlace a un perfil propio. Todos los
  enlaces de la sección abren en una pestaña nueva (`target="_blank"` con
  `noopener`).
- Los enlaces del perfil como círculos con icono: `linkedin-logo`,
  `github-logo` y `briefcase` para Reskyon; un enlace sin icono propio
  muestra su etiqueta dentro del círculo en vez de un símbolo que no lo
  represente. Cada uno lleva `title` con el nombre y un `aria-label` con el
  nombre más «(abre en una pestaña nueva)».
- El enlace a Reskyon queda **comentado** en los dos `profile.yml` con una
  nota para restaurarlo; el componente no sabe nada de Reskyon.
- Sin formulario, correo ni mapa; sin «Next chapter», porque es la última
  sección y el componente compartido no pinta nada en ella (Módulo S2).

### El código

`contact.component.ts`:

```ts
import { Component, computed, input } from '@angular/core'
import { CvDownloadsComponent } from '@home/components/cv-downloads/cv-downloads.component'
import { Profile } from '@interfaces/profile.interface'
import { SectionTitleComponent } from '@shared/components/section-title/section-title.component'
import { Locale } from '@shared/interfaces/shared.interface'

// Contact has no email address on purpose: visitors are sent to LinkedIn.
// The content validation guarantees a link with id "linkedin".
@Component({
  selector: 'home-contact',
  imports: [SectionTitleComponent, CvDownloadsComponent],
  templateUrl: './contact.component.html',
  styleUrl: './contact.component.scss',
})
export class ContactComponent {
  readonly locale = input.required<Locale>()
  readonly contact = input.required<Profile['contact']>()
  readonly links = input.required<Profile['links']>()

  protected readonly subtitle = computed(() =>
    this.locale() === 'es' ? 'Hablemos' : "Let's get in touch",
  )
  // Every link of the section opens in a new tab: say so in its accessible name, since
  // the icon-only links have no other text for a screen reader to read.
  protected readonly newTab = computed(() =>
    this.locale() === 'es' ? 'abre en una pestaña nueva' : 'opens in a new tab',
  )
  protected readonly linkedin = computed(
    () => this.links().find((link) => link.id === 'linkedin') ?? this.links()[0],
  )
}
```

La portada lo usa con
`<home-contact [locale]="locale" [contact]="profile.contact" [links]="profile.links" />`.

> **Nota:** el componente de contacto de arriba y la plantilla de abajo ya
> incluyen los botones de descarga del CV (`<home-cv-downloads />`, junto al
> botón de LinkedIn, dentro de un `div.actions`). Ese componente se explica en
> [Después: los botones de descarga del CV](#después-los-botones-de-descarga-del-cv),
> en el Módulo S1.

`contact.component.html` (los `<path>` de Phosphor se omiten; están en el
repositorio):


`contact.component.scss`:


En `content/en/profile.yml`, la entrada oculta:

```yaml
links:
  - id: linkedin
    label: LinkedIn
    url: https://www.linkedin.com/in/janio-isacura-84256733/
  - id: github
    label: GitHub
    url: https://github.com/Yanioconjota
  # Reskyon is hidden while its site is under construction; restore the entry when it launches.
  # - id: reskyon
  #   label: Reskyon
  #   url: https://reskyon.com/
```

`contact.component.spec.ts` renderiza el componente con tres enlaces
(`linkedin`, `reskyon` y un `website` sin icono) y comprueba que todos
llevan un `aria-label` con el sufijo de pestaña nueva, que los dos primeros
tienen SVG y que el tercero muestra «Blog» como texto; otra prueba, en inglés
y en español, comprueba el nombre del botón y de los círculos. La prueba de `app.spec.ts` sigue comprobando que
el primer `a[rel~="me"]` es el botón a LinkedIn y que la sección no contiene
`mailto:` ni `@`.

### Cómo funciona por dentro

- **`@switch` en la plantilla** elige el icono por el `id` del enlace, que
  es un dato del contenido: el componente no tiene lista de redes. El
  `@default` es la red de seguridad para un `id` nuevo: la validación del
  perfil admite cualquiera con etiqueta y URL, así que sin ese caso un
  enlace nuevo saldría con un icono equivocado o sin nada.
- **Nombre accesible de un enlace que es sólo un icono.** El SVG va con
  `aria-hidden`, así que el enlace no tendría nombre; `aria-label` se lo da
  y `title` muestra el mismo texto al pasar el ratón. Con el `@default` de
  texto, el `aria-label` sigue valiendo y coincide con lo que se ve.
  Como todos los enlaces de la sección abren una pestaña nueva, el nombre
  lo dice con un sufijo por idioma (`newTab`: «abre en una pestaña nueva» /
  «opens in a new tab»), también en el botón de LinkedIn, cuyo nombre
  empieza por el texto visible: así sigue cumpliendo «la etiqueta en el
  nombre» (WCAG 2.5.3) y un lector de pantalla avisa de que el foco va a
  pasar a otra pestaña (técnica G201).
- **`rel="me"`** marca el enlace a un perfil de la misma persona; es la
  forma estándar de decir «esta URL también soy yo» y la usa la prueba para
  encontrar la llamada a la acción.
- **`target="_blank"` con `rel="noopener"`.** Los enlaces de contacto salen del
  sitio, así que se abren en una pestaña nueva y la persona no pierde el
  portfolio. `noopener` impide que la página abierta alcance a la tuya
  mediante `window.opener`; los navegadores actuales ya lo aplican con
  `_blank`, pero escribirlo no cuesta nada. Como `rel` ahora lleva dos
  valores (`me noopener`), el selector de la prueba es `a[rel~="me"]`
  (contiene la palabra) y no `a[rel="me"]` (igual al texto completo).
- **`:focus-visible` comparte las reglas de `:hover`**: el relleno negro
  aparece también al llegar con Tab. Es lo mismo que en las tarjetas de
  Proyectos (Módulo S7): un estado que sólo existe con ratón deja fuera al
  teclado.
- **Ocultar con un comentario YAML** en vez de borrar: el dato sigue en el
  archivo, con el motivo al lado, y volver es quitar tres almohadillas. El
  componente itera lo que llega, así que no hay condición en el código ni
  nada que recordar en TypeScript. La contrapartida es la documentación:
  `docs/site-structure.md` y [Secciones y contenido](secciones-y-contenido.md)
  anotan el enlace oculto para que no digan lo contrario que el sitio.
- **Sin «Next chapter».** `shared-next-chapter` calcula el destino desde
  `SECTIONS` y en la última sección devuelve `null`; aquí ni se incluye.

### Errores comunes

- **Copiar el formulario de Portify** con EmailJS: tres claves en el
  JavaScript del cliente y un correo que los rastreadores recogen igual.
- **Enlaces de icono sin `aria-label`:** un lector de pantalla anuncia
  «enlace» tres veces seguidas.
- **Un icono por defecto que representa algo concreto** (el maletín) para
  cualquier enlace nuevo: parece una decisión y es un olvido.
- **Borrar la entrada de Reskyon** para ocultarla: al volver hay que
  recordar la URL y la etiqueta en dos idiomas.
- **`:hover` sin `:focus-visible`** en el relleno de los círculos.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué un portfolio sin formulario de contacto, si la plantilla lo trae?

**Respuesta:**

Porque un formulario estático necesita un servicio que envíe el correo
(EmailJS, un endpoint propio, un Worker) con claves en el cliente o un
backend que mantener, más protección contra spam, y todo eso para un canal
que la persona ya tiene mejor resuelto: LinkedIn identifica a las dos
partes y filtra solo. Publicar el correo tampoco: lo recogen los
rastreadores. La decisión reduce superficie (no hay nada que proteger ni
que pueda fallar en producción) a cambio de un paso más para quien no usa
LinkedIn. Ese paso adicional es el coste de la decisión.

#### 2. ¿Cómo le das nombre accesible a un enlace que sólo muestra un icono?

**Respuesta:**

Con `aria-label` en el propio enlace y el icono marcado como decorativo
(`aria-hidden="true"` en el SVG), para que el lector de pantalla anuncie
«LinkedIn, enlace» y no «imagen, enlace». Alternativas: texto visualmente
oculto dentro del enlace (una clase tipo `visually-hidden`), que además
sirve a buscadores, o un `<title>` dentro del SVG con `aria-labelledby`,
más frágil. `title` en el enlace no es un sustituto: no todos los lectores
lo anuncian y no aparece con el teclado; aquí es un extra para el ratón.

#### 3. Un dato del contenido tiene que desaparecer temporalmente. ¿Dónde lo ocultas?

**Respuesta:**

En el contenido, nunca en el componente. Si el componente filtra «todo menos
Reskyon», el código conoce un dato editorial, hay que tocarlo para volver y
la regla se pierde entre el resto de la lógica. Comentar la entrada en el
YAML (o un campo `hidden: true` validado, si fuera a repetirse) deja el dato
donde vive, con el motivo al lado, y el cambio lo hace quien edita
contenido. La documentación que describe el sitio tiene que decir lo mismo,
o alguien restaurará el enlace creyendo que falta por error.

<!-- /study-guide:section:sections-s8-contact -->

---

<!-- study-guide:section:sections-s9-footer -->
## Módulo S9: El pie de página sin crédito y con «Volver arriba»

Fuente: `src/app/shared/components/footer/` del repositorio.

### El problema que resuelve

La variante `dots-bg` de Portify no trae pie en la portada; sólo las
páginas de blog tienen uno: una banda gris al 6 % con «Copyright @ 2026
Portify | Designed By Pixelaxis», centrado, con el año escrito por
JavaScript en un `<span id="year">`. Este sitio ya tenía la banda con el
nombre y nada más. Janio no quiere crédito al template (la licencia
Regular no lo exige) y la portada es larga, sobre todo en móvil: hacía
falta algo útil en el pie, no un adorno.

### La decisión en este sitio

- La banda de Portify se conserva (negro al 6 %, 32 px de relleno, 14 px).
- A la izquierda, «© 2026 Janio Isacura» y, en gris al 60 %, una línea
  verdadera sobre lo que hay debajo: «Built with Angular, prerendered and
  served by Nginx» / «Hecho con Angular, prerenderizado y servido con Nginx».
- A la derecha, «Back to top» / «Volver arriba»: un `routerLink` a
  `/${locale}#home` con la flecha `arrow-up` de Phosphor inline, el mismo
  mecanismo que los enlaces del menú (Parte 2, Módulo E6) y el scroll por
  fragmento del Módulo S3.
- El idioma sale de la URL con `injectCurrentUrl` y `localeFromUrl`, como
  en el encabezado: el pie vive fuera de las páginas y no recibe entradas.
- El año se calcula con `new Date()`, al prerenderizar y otra vez en el
  navegador.

### El código

`footer.component.ts`:

```ts
import { Component, computed } from '@angular/core'
import { RouterLink } from '@angular/router'
import { injectCurrentUrl, localeFromUrl } from '@shared/utils/current-locale.utils'

@Component({
  selector: 'shared-footer',
  imports: [RouterLink],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.scss',
})
export class FooterComponent {
  private readonly url = injectCurrentUrl()
  protected readonly locale = computed(() => localeFromUrl(this.url()) ?? 'en')
  // Computed at prerender time and again in the browser: the prerendered HTML carries
  // the build year until hydration, then the visitor's clock takes over.
  protected readonly year = new Date().getFullYear()

  protected readonly labels = computed(() =>
    this.locale() === 'es'
      ? { stack: 'Hecho con Angular, prerenderizado y servido con Nginx', top: 'Volver arriba' }
      : { stack: 'Built with Angular, prerendered and served by Nginx', top: 'Back to top' },
  )
}
```

`footer.component.html`:


`footer.component.scss`:


`App` lo coloca después de `<main>` en `app.html`: `<shared-footer />`.

### Cómo funciona por dentro

- **El año en dos momentos.** `new Date().getFullYear()` corre en Node al
  prerenderizar, y ese número queda en el HTML que sirve Nginx y que leen
  los rastreadores. Cuando el navegador hidrata, el componente se crea otra
  vez y vuelve a calcularlo con el reloj de quien visita. Si el sitio se
  construyó en diciembre y alguien lo abre en enero, ve el año nuevo tras
  la hidratación; la diferencia dura lo que tarda en cargar el JavaScript.
  Angular no compara el texto de los nodos al hidratar, así que no hay
  error de hidratación por eso.
- **«Volver arriba» es un enlace del router, no un `scrollTo`.** Navega a
  `/${locale}#home`; el scroll por fragmento (Módulo S3) trata ese fragmento
  como un caso especial y lleva la vista al tope de la ventana (`scrollY` 0),
  no a `<section id="home">`, que empieza 68 px más abajo porque la barra del
  logo queda encima. Desde una página de proyecto vuelve a la portada y sube. Con la URL ya en `#home` también funciona: se comprobó
  con dos clics seguidos desde el final de la página.
- **`column-gap-3`** es una utilidad de Bootstrap 5.3 para el hueco
  horizontal entre los dos párrafos; cuando se apilan en móvil no deja
  margen vertical, que es lo que se quiere.
- **`flex-wrap` y `gap-3`** en el contenedor: en móvil el enlace baja a su
  propia línea sin scroll horizontal.
- **Sin pruebas propias.** El pie no tiene lógica más allá de las etiquetas
  por idioma y el enlace; se comprobó en el navegador en los dos idiomas.

### Errores comunes

- **Poner el crédito del template por costumbre.** Es una decisión de
  marca: aquí se prefirió una línea sobre el stack, que además es cierta.
- **Escribir el año a mano** (`© 2026`): queda viejo en silencio.
- **Un botón con `window.scrollTo(0, 0)`** en vez del enlace: no deja URL,
  no funciona sin JavaScript y no sirve desde otra página.
- **Confiar en que un clic antes de la hidratación** haga lo mismo: durante
  el primer arranque de `ng serve` el enlace actúa como `<a>` normal y
  puede no subir; en el sitio publicado la ventana es mínima.

### Preguntas de entrevista (senior)

#### 1. Un valor calculado con `new Date()` en un sitio prerenderizado, ¿qué ve cada quien?

**Respuesta:**

Tres lectores distintos. El rastreador y quien tiene JavaScript desactivado
ven el valor del momento del build, grabado en el HTML. Quien visita con
JavaScript ve ese mismo valor hasta que la aplicación hidrata y lo
recalcula con su reloj. Y las pruebas lo ven con el reloj de la máquina de
CI. Para un año de copyright da igual; para algo sensible (una oferta
«hasta hoy», un contador) habría que decidir una sola fuente de verdad y
pasarla como dato, o aceptar y documentar el parpadeo.

#### 2. ¿Por qué «Volver arriba» es un enlace y no un botón?

**Respuesta:**

Porque navega: cambia la URL a `#home`, funciona sin JavaScript, se puede
abrir en otra pestaña y desde una página de proyecto lleva a la portada.
Un botón con `scrollTo` sólo mueve la vista de la página actual y, en
accesibilidad, un botón promete una acción en la página, no un destino. La
regla: si el resultado es «estar en otro sitio», enlace; si es «cambiar
algo aquí», botón.

#### 3. Un componente fuera de las páginas necesita saber el idioma. ¿Cómo lo obtiene sin que nadie se lo pase?

**Respuesta:**

Leyéndolo de la única fuente de verdad, la URL. Una función compartida
convierte los eventos del router en una señal con la URL actual y otra
saca el idioma del primer segmento; el componente deriva sus etiquetas con
`computed` y cambia solo al navegar. Alternativas: un servicio de idioma
con estado propio (otra fuente que mantener sincronizada) o pasar el
idioma por entradas desde `App` (acopla el esqueleto a cada componente). La
señal derivada de la URL no tiene estado que pueda quedar viejo.

<!-- /study-guide:section:sections-s9-footer -->

---

## Qué sigue en esta parte

Las seis secciones de Portify y el pie están construidos; la Galería, que
llega en la [Parte 5](05-galeria.md), se suma entre Proyectos y Contacto: siete
secciones en total. Las animaciones de GSAP,
el lienzo de puntos del fondo y el interruptor de animaciones están en la
[Parte 4](04-animaciones.md). Para seguir el comportamiento del menú, consulta
[Navegación y movimiento](learn-navigation.md).
