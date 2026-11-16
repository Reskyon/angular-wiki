# Parte 7: La guía DIY

> Esta versión pública conserva las explicaciones y omite fragmentos que reproducen o adaptan la plantilla comercial.

Esta parte construye la guía DIY del portfolio. DIY viene del inglés *do it
yourself*, «hazlo tú mismo». Es una versión corta de esta guía de construcción,
en inglés y en español, para quien quiere convertir una plantilla en su propio
portfolio y CV con Angular. Tiene seis pasos, y cada uno dice qué cambiar, qué
archivo abrir y cómo comprobar el resultado. El repositorio es el del portfolio
de janioisacura.com, un sitio Angular con el contenido en Markdown y YAML,
prerenderizado a HTML estático. Para seguir esta parte en tu proyecto necesitas
una aplicación Angular con rutas y un paso que prepare el contenido antes de
compilar, como el de la galería. Llega al final porque se sumó al sitio terminado:
reutiliza el patrón de la [Parte 5](05-galeria.md) (una página propia que se carga
bajo demanda, con su entrada en la portada), el scroll por fragmento de la
[Parte 3](03-secciones-de-portify.md) y los metadatos de la
[Parte 6](06-seo-y-vista-previa.md). Cada módulo deja código real del repositorio y
un problema que hubo que resolver: la guía que quedaba fuera del hilo de la
portada, el cambio de idioma que caía en otro paso, el historial que se llenaba
de pasos.

**Proyecto:** `content/en/diy.yml`, `content/es/diy.yml`,
`scripts/diy-content.mjs`, `src/app/home/pages/diy-page/`,
`src/app/home/components/diy-teaser/`,
`src/app/home/constants/diy-teaser.constants.ts` y `diy-labels.constants.ts`,
`src/app/home/utils/diy-active-step.utils.ts`,
`src/app/shared/components/language-switcher/` y
`src/app/shared/constants/sections.constants.ts`, con sus pruebas
(`diy-content.test.mjs`, `diy-page.component.spec.ts`,
`diy-active-step.utils.spec.ts`, `diy-teaser.component.spec.ts` y
`language-switcher.component.spec.ts`).
**Sitio publicado:** la guía vive en
[janioisacura.com/en/diy](https://janioisacura.com/en/diy) y
[janioisacura.com/es/diy](https://janioisacura.com/es/diy), y su entrada está en
la portada, arriba de Contacto. Para verla en local, `npm start` y abrir
`/en/diy`.

**Qué vas a aprender:**

- [Módulo D1](#módulo-d1-el-contenido-en-yaml-y-su-validación): **El contenido
  en YAML y su validación.** Un archivo por idioma con los pasos, qué campos
  tiene cada paso y qué detiene el build antes de que un error llegue a la página.
- [Módulo D2](#módulo-d2-la-página-y-la-entrada-en-la-portada): **La página y la
  entrada en la portada.** Por qué la guía es una sección más arriba de Contacto,
  cómo se queda fuera del paquete de la portada y por qué sus estilos son
  globales.
- [Módulo D3](#módulo-d3-la-url-que-sigue-el-paso-y-el-cambio-de-idioma): **La URL
  que sigue el paso y el cambio de idioma.** Cómo la dirección guarda el paso que
  se está leyendo sin mover la página ni llenar el historial, y cómo el cambio de
  idioma lleva al mismo paso.
- [Módulo D4](#módulo-d4-el-cierre-hacia-el-bonus): **El cierre hacia el Bonus.**
  Un enlace externo que abre en otra pestaña y lo anuncia, y una guía que se lee
  sin el repositorio privado.

Cada módulo sigue el mismo orden: el problema que resuelve, la decisión tomada
en este sitio, el procedimiento o el código completo, cómo funciona por
dentro, errores comunes y preguntas de entrevista con su respuesta.

Esta página es una parte de la guía [Cómo se construye este sitio](como-se-construye.md).
La anterior es la [Parte 6: Metadatos para compartir y buscadores](06-seo-y-vista-previa.md).
Esta es, por ahora, la última parte; para volver al principio, abre el
[índice de la guía](como-se-construye.md).

---

<!-- study-guide:section:diy-d1-content -->
## Módulo D1: El contenido en YAML y su validación

Fuente: `content/en/diy.yml`, `content/es/diy.yml`, `scripts/diy-content.mjs`,
`scripts/prepare-content.mjs` y `scripts/diy-content.test.mjs`.

### El problema que resuelve

Una guía de seis pasos en dos idiomas es mucho texto, con bloques de código,
listas de archivos y comprobaciones. Si ese texto vive dentro de los componentes,
cambiar una frase obliga a tocar código, y nada impide que una versión tenga un
paso menos que la otra. Hacía falta lo mismo que en el resto del sitio: el texto
en archivos de contenido, y una comprobación que falle al compilar si algo no
encaja.

### La decisión en este sitio

- **Un YAML por idioma**, `content/<idioma>/diy.yml`: título, subtítulo,
  introducción, la lista de pasos y un cierre.
- **Cada paso tiene siempre los mismos campos.** Un `id`, un `title`, el cambio
  con que empieza (`change`), los archivos que hay que abrir (`files`, cada uno
  con su `why`), el cuerpo (`body`) y la comprobación (`check`) en Markdown, y dos
  textos cortos que separan lo que da Angular (`angular`) de lo que añade este
  portfolio (`added`).
- **El build valida antes de generar nada.** Un campo de más o de menos, un texto
  vacío, un `id` que no sirve como fragmento de URL o que se repite, o un cierre
  sin HTTPS detienen la preparación con el archivo y el campo.
- **Los dos idiomas se comparan.** Tienen que tener los mismos `id`, en el mismo
  orden, y el mismo enlace de cierre.
- **El Markdown se convierte una vez**, al preparar el contenido, y el resultado
  se escribe en `src/app/home/generated/diy.ts`.

### El código

La forma del YAML en inglés, recortada a un paso (los `…` marcan el texto que se
omite aquí):

```yaml
title: DIY guide
subtitle: How to turn a template into your own portfolio and CV with Angular
intro: >-
  This guide follows how this site was built, in six steps you can repeat in your own
  project. …
steps:
  - id: styles
    title: Separate global styles, shared assets and component styles
    change: >-
      Move colors and page rules out of the section, and decide where each style lives:
      global, shared or inside the component.
    files:
      - path: src/styles.scss
        why: The only global entry. It imports five partials in a fixed order.
    body: |
      The global file only lists the partials, and the order matters: …
    check: |
      1. Run `npm run build`. …
    angular: >-
      Component styles scoped by emulated view encapsulation, …
    added: >-
      The tools, tokens, Bootstrap, fonts and base split; …
closing:
  text: >-
    That is the whole route: base, styles, data, projects, images and build. …
  cta: Read the full Bonus (in Spanish)
  url: https://angular-wiki.reskyon.com/portfolio-bonus/
```

La validación, en `scripts/diy-content.mjs`, recortada a las reglas de los pasos
y del cierre:

```js
const STEP_FIELDS = ['id', 'title', 'change', 'files', 'body', 'check', 'angular', 'added']

// Inside validateDiy, for every step:
if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(step.id))
  fail(`${label}: "id" must use lowercase letters, numbers, and hyphens.`)
if (ids.has(step.id)) fail(`${label}: duplicate id "${step.id}".`)

// And for the closing:
if (URL.parse(data.closing.url)?.protocol !== 'https:')
  fail('the closing: "url" must be an HTTPS URL.')
```

La comparación entre idiomas y la conversión del Markdown:

```js
// The Markdown fields become HTML here, once, so Angular only has to insert them.
export function buildDiy(data) {
  return {
    ...data,
    steps: data.steps.map((step) => ({
      ...step,
      ...Object.fromEntries(
        MARKDOWN_FIELDS.map((field) => [field, marked.parse(step[field], { async: false })]),
      ),
    })),
  }
}

// Both languages list the same steps in the same order and close on the same page.
export function checkSameDiy(diys, locales) {
  const [first, ...others] = locales
  const signature = (locale) =>
    JSON.stringify({ ids: diys[locale].steps.map(({ id }) => id), url: diys[locale].closing.url })
  for (const locale of others) {
    if (signature(locale) !== signature(first))
      throw new Error(
        `content/${locale}/diy.yml: the steps (ids and order) and the closing "url" must match content/${first}/diy.yml.`,
      )
  }
}
```

### Cómo funciona por dentro

- **Dónde corre.** `prepare-content.mjs` lee los dos YAML, llama a
  `validateDiy` con la ruta de cada archivo (para que el error la nombre), después
  a `checkSameDiy`, y escribe el módulo generado con `buildDiy`. Ese script corre
  antes de `npm start`, `npm run build` y `npm test`.
- **Por qué el `id` es un *slug*.** El `id` será el fragmento de la URL
  (`/en/diy#styles`) y el `id` del `<article>`. Con minúsculas, números y guiones
  no hace falta codificar nada y no hay dos formas de escribir el mismo paso.
- **La firma de cada idioma.** `checkSameDiy` resume cada idioma en un texto con
  la lista de `id` y la URL de cierre, y los compara. Un paso de más, uno
  traducido o el orden cambiado dan firmas distintas.
- **Markdown a HTML en el build.** `marked` convierte `body` y `check`. El
  navegador recibe HTML ya hecho, sin descargar un conversor, y el texto está en
  la página prerenderizada.
- **Las pruebas.** `diy-content.test.mjs` prueba cada regla con datos pequeños y,
  al final, los archivos reales: seis pasos en los dos idiomas y el cierre en el
  Bonus público.

### Errores comunes

- **Traducir los `id`.** `/es/diy#estilos` no existe en inglés. La comparación lo
  detiene en el build.
- **Validar en el componente.** El error aparecería en la pantalla de quien
  visita, no al compilar.
- **Dejar un campo vacío «para después».** Un `check` vacío dejaría un título
  «Cómo comprobarlo» sin nada debajo. La validación exige texto en todos.
- **Escribir HTML a mano en el YAML.** El Markdown ya cubre listas, código y
  enlaces, y queda legible en el archivo.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué validar el contenido en un script antes del build y no con tipos de TypeScript?

**Respuesta:**

Porque los tipos solo existen al compilar el código, y el YAML no es código: se
lee como datos. TypeScript no puede saber si un archivo tiene un campo vacío o un
`id` repetido. El script lee los datos reales y falla con el archivo y el campo.
Después escribe un módulo con tipos, así el componente sí trabaja con datos
tipados y ya comprobados.

#### 2. ¿Por qué comparar los dos idiomas y no validar cada uno por separado?

**Respuesta:**

Porque cada archivo puede ser válido por su cuenta y la pareja estar rota. Si el
inglés tiene seis pasos y el español cinco, o un `id` distinto, el cambio de
idioma lleva a un paso que no existe. Esa regla solo se ve mirando los dos
archivos juntos.

#### 3. ¿Por qué convertir el Markdown al preparar el contenido y no en el navegador?

**Respuesta:**

Porque así el navegador no descarga un conversor de Markdown y el HTML ya está en
la página prerenderizada, que es lo que leen los buscadores. La conversión se
hace una vez por compilación, no en cada visita. La seguridad no cambia: el HTML
se inserta con `[innerHTML]` y Angular lo sigue limpiando.

<!-- /study-guide:section:diy-d1-content -->

---

<!-- study-guide:section:diy-d2-page-entry -->
## Módulo D2: La página y la entrada en la portada

Fuente: `src/app/shared/constants/sections.constants.ts`,
`src/app/home/components/diy-teaser/`,
`src/app/home/constants/diy-teaser.constants.ts`,
`src/app/home/constants/diy-labels.constants.ts`, `src/app/app.routes.ts` y
`src/app/home/pages/diy-page/`.

### El problema que resuelve

La primera versión puso la guía como un enlace más del menú, después de
Contacto. Rompía dos reglas del sitio: Contacto es siempre la última sección, y
todo lo que tiene página propia tiene también su entrada en la portada. Quien
leía la portada de arriba abajo, siguiendo «Siguiente capítulo», nunca llegaba a
la guía. Además, la página tenía que cargarse solo al visitarla: la portada no
debe descargar seis pasos de texto.

### La decisión en este sitio

- **Una sección más, arriba de Contacto.** `diy` entra en `SECTIONS` entre
  `gallery` y `contact`. El menú, los contadores y «Siguiente capítulo» se
  recalculan solos: la galería apunta a la guía, la guía a Contacto, y los
  contadores pasan a «x/08».
- **La entrada no lleva imagen.** Es como una tarjeta de proyecto sin portada:
  título de sección, un encabezado, una descripción y un botón a
  `/<idioma>/diy`. Sus textos están en `diy-teaser.constants.ts` y el título es la
  etiqueta de `SECTIONS`.
- **La página se carga bajo demanda** (`loadComponent`) y se prerenderiza en
  `/en/diy` y `/es/diy`. El título sale de un *resolver* que importa el módulo
  generado solo al visitarla, y la descripción, de `diy-labels.constants.ts`.
- **El enlace de volver apunta a `#diy`**, para caer en la sección de la portada.

### El código

La constante de secciones, con `diy` antes de `contact`:

```ts
export const SECTIONS: readonly Section[] = [
  { id: 'home', label: { en: 'Home', es: 'Inicio' } },
  { id: 'about', label: { en: 'About', es: 'Sobre mí' } },
  { id: 'skills', label: { en: 'Skills', es: 'Habilidades' } },
  { id: 'experience', label: { en: 'Experience', es: 'Experiencia' } },
  { id: 'projects', label: { en: 'Projects', es: 'Proyectos' } },
  { id: 'gallery', label: { en: 'Gallery', es: 'Galería' } },
  { id: 'diy', label: { en: 'DIY guide', es: 'Guía DIY' } },
  { id: 'contact', label: { en: 'Contact', es: 'Contacto' } },
]
```

La entrada de la portada:

```ts
// The DIY guide's place in the homepage reading order, above Contact. Every page of the site
// that is not a section also has an entry here, so the navigation and the "Next chapter" series
// stay the same on the homepage. Like Projects, a title and a description, without a cover.
@Component({
  selector: 'home-diy-teaser',
  imports: [RouterLink, SectionTitleComponent, NextChapterComponent],
  templateUrl: './diy-teaser.component.html',
  styleUrl: './diy-teaser.component.scss',
})
export class DiyTeaserComponent {
  readonly locale = input.required<Locale>()

  protected readonly teaser = computed(() => DIY_TEASER[this.locale()])
  protected readonly title = computed(
    () => SECTIONS.find((section) => section.id === 'diy')!.label[this.locale()],
  )
}
```


La ruta de cada idioma, en `src/app/app.routes.ts`:

```ts
// Same for the DIY guide.
const diyTitle: ResolveFn<string> = async (route) => {
  const { DIY } = await import('@generated/diy')
  return `${DIY[route.data['locale'] as Locale].title} | Janio Isacura`
}
```

```ts
    {
      path: `${locale}/diy`,
      title: diyTitle,
      data: { locale, description: DIY_LABELS[locale].description },
      resolve: { pageMetadata: setPageMetadata },
      loadComponent: () =>
        import('@home/pages/diy-page/diy-page.component').then((module) => module.DiyPageComponent),
    },
```

La página inserta el HTML de cada paso y declara sus estilos como globales:

```ts
@Component({
  selector: 'home-diy-page',
  imports: [RouterLink, SectionTitleComponent, SerialPipe],
  templateUrl: './diy-page.component.html',
  styleUrl: './diy-page.component.scss',
  // The step bodies arrive through [innerHTML] and carry no Angular scoping attribute. The styles
  // are global and nested under .diy-page.
  encapsulation: ViewEncapsulation.None,
})
```

### Cómo funciona por dentro

- **El contador sale de la posición en `SECTIONS`.** Con `diy` en la séptima
  posición, el enlace de la galería apunta a la guía y el de la guía, a Contacto.
  Ningún componente cambió para eso.
- **Qué viaja en el paquete de la portada.** La entrada lee `DIY_TEASER`, cuatro
  textos por idioma. La ruta lee `DIY_LABELS` para la descripción. El módulo
  generado con los seis pasos solo se importa dentro del *resolver* y de la
  página, que se cargan al visitar la guía.
- **Por qué estilos globales.** Angular aísla los estilos de un componente
  agregando un atributo a cada elemento de su plantilla. El HTML que llega por
  `[innerHTML]` no lo lleva, así que reglas como `.body pre` no lo alcanzarían.
  Con `ViewEncapsulation.None` las reglas son globales, y todas cuelgan de
  `.diy-page` para no afectar al resto del sitio.
- **Un solo `<h1>`.** En la página, el título de la guía es el `<h1>` y cada paso
  un `<h2>`; en la portada, la entrada usa el `<h2>` de sección como las demás.
- **Metadatos y mapa del sitio.** Las dos páginas tienen título, descripción,
  canonical y su pareja de idioma, y están en `sitemap.xml`, como explica la
  [Parte 6](06-seo-y-vista-previa.md).

### Errores comunes

- **Poner la sección después de Contacto o solo en el menú.** El hilo de
  «Siguiente capítulo» se rompe y la lectura de la portada no llega a la guía.
- **Importar `DIY` en la entrada o en las rutas.** La portada descargaría los seis
  pasos aunque nadie abra la guía.
- **Estilos con el aislamiento normal para HTML de `[innerHTML]`.** Los bloques de
  código y las listas del Markdown quedarían sin estilo.
- **Estilos globales sin un contenedor.** Una regla `pre { … }` suelta cambiaría
  todos los bloques de código del sitio. Todo va dentro de `.diy-page`.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué la guía es una sección de la portada y no solo un enlace del menú?

**Respuesta:**

Porque la portada se lee como una serie: cada sección termina con «Siguiente
capítulo» y un contador. Una página que solo está en el menú queda fuera de esa
serie, y quien lee de arriba abajo no se entera de que existe. Al sumarla a
`SECTIONS`, el menú, los contadores y los enlaces se derivan de la misma lista y
no pueden discrepar.

#### 2. ¿Por qué el título de la página sale de un *resolver* con `import()` y no de un texto fijo en la ruta?

**Respuesta:**

Porque el título está en el contenido, que puede cambiar, y repetirlo en la ruta
dejaría dos copias. Pero importar el módulo generado en el archivo de rutas lo
metería en el paquete principal, que descarga cualquier visitante. Un *resolver*
con `import()` dinámico lee el título del contenido y lo descarga solo al visitar
la guía.

#### 3. ¿Cuándo está bien usar `ViewEncapsulation.None`?

**Respuesta:**

Cuando el componente muestra HTML que no está en su plantilla, como el que llega
por `[innerHTML]`, y ese HTML necesita estilos. Sin aislamiento, las reglas son
globales, así que hay que encerrarlas bajo una clase propia del componente. Para
un componente normal, el aislamiento por defecto es mejor: evita que sus estilos
se filtren al resto de la página.

<!-- /study-guide:section:diy-d2-page-entry -->

---

<!-- study-guide:section:diy-d3-step-fragment -->
## Módulo D3: La URL que sigue el paso y el cambio de idioma

Fuente: `src/app/home/pages/diy-page/diy-page.component.ts`,
`src/app/home/utils/diy-active-step.utils.ts`,
`src/app/shared/components/language-switcher/language-switcher.component.ts` y
`src/app/shared/utils/fragment-scrolling.utils.ts`.

### El problema que resuelve

En el resto del sitio, cambiar de idioma no mueve la página: así lo decidió el
[Módulo S3 de la Parte 3](03-secciones-de-portify.md#módulo-s3-scroll-por-fragmento-sin-saltos),
que construye el scroll por fragmento. En la guía eso no sirve. Cada paso es un
texto largo, y los dos idiomas no miden lo mismo: el mismo desplazamiento cae en
otro paso. Lo que hay que conservar es el paso, no los píxeles. Y el paso tiene
que estar en algún sitio que el selector de idioma pueda leer: la URL.

### La decisión en este sitio

- **Cada paso es un fragmento de la URL**, igual en los dos idiomas
  (`/en/diy#styles` y `/es/diy#styles`).
- **La página escribe en la URL el paso que se está leyendo** mientras la
  persona se desplaza, sin mover la página y sin sumar entradas al historial.
- **El selector de idioma conserva el fragmento.** Solo en la guía, y solo si hay
  un paso en la URL, la navegación no lleva `KEEP_SCROLL`, y el scroll por
  fragmento baja hasta ese paso en el otro idioma.

### El código

El paso activo, en `src/app/home/utils/diy-active-step.utils.ts`:

```ts
export interface StepPosition {
  id: string
  /** Distance of the top of the step from the top of the viewport, in pixels. */
  top: number
}

// The step being read is the last one whose top has reached the reading line (just under the
// sticky header). Above the first step there is none: the visitor is still on the introduction.
export function activeStepId(steps: readonly StepPosition[], line: number): string | null {
  let active: string | null = null
  for (const step of steps) {
    if (step.top <= line) active = step.id
  }
  return active
}
```

La página escucha el desplazamiento y escribe el resultado en la URL (recortado a
lo que hace eso):

```ts
// The reading line sits a few pixels below the anchor offset: scrolling to a fragment leaves the
// step exactly at the offset, and rounding must not make the previous step the active one.
const LINE_TOLERANCE = 8

  constructor() {
    const destroyRef = inject(DestroyRef)
    afterNextRender(() => {
      const view = this.document.defaultView
      if (!view) return
      const onScroll = () => this.followReading()
      view.addEventListener('scroll', onScroll, { passive: true })
      destroyRef.onDestroy(() => view.removeEventListener('scroll', onScroll))
    })
  }

  // Writes the step being read into the URL fragment without moving the page.
  private followReading() {
    const root = this.document.documentElement
    const padding = this.document.defaultView?.getComputedStyle(root).scrollPaddingTop
    const line = (parseFloat(padding ?? '') || 0) + LINE_TOLERANCE
    const active = activeStepId(
      this.diy.steps.map(({ id }) => ({
        id,
        top: this.document.getElementById(id)?.getBoundingClientRect().top ?? Infinity,
      })),
      line,
    )
    if (active === (this.router.parseUrl(this.router.url).fragment ?? null)) return
    void this.router.navigate([], {
      relativeTo: this.route,
      fragment: active ?? undefined,
      queryParamsHandling: 'preserve',
      replaceUrl: true,
      info: KEEP_SCROLL,
    })
  }
```

El selector de idioma decide, por dirección, si conserva el desplazamiento:

```ts
// Switching language keeps the reader where they are instead of jumping to the fragment. The DIY
// guide is the exception: its page keeps the fragment on the step being read, and the two languages
// are not the same height, so the other language scrolls to that step.
function scrollInfoFor(suffix: string): ScrollInfo {
  return /^\/diy#./.test(suffix) ? {} : KEEP_SCROLL
}
```

Cada opción del selector lleva su propio `info: scrollInfoFor(suffix)`, y el
enlace usa `[info]="option.info"`.

### Cómo funciona por dentro

- **La línea de lectura.** Es el `scroll-padding-top` de `<html>` (la altura de
  la barra fija en móvil, cero en escritorio) más 8 px de margen. El paso activo
  es el último cuyo borde superior ya pasó esa línea. Por encima del primer paso
  no hay ninguno, y la URL se queda sin fragmento.
- **Escribir en la URL sin mover nada.** `router.navigate([], …)` con
  `replaceUrl: true` reemplaza la entrada del historial en lugar de sumar una por
  paso, así el botón Atrás sale de la guía. `info: KEEP_SCROLL` le dice al scroll
  por fragmento que no lleve el paso al borde superior. Si el paso no cambió, no
  navega.
- **Solo en el navegador.** `afterNextRender` no corre en el prerenderizado, así
  que el servidor no escucha ningún desplazamiento. El oyente es pasivo (no
  bloquea el desplazamiento) y se quita al salir de la página.
- **El cambio de idioma.** Desde `/en/diy#styles`, el sufijo es `/diy#styles` y
  la opción va sin `KEEP_SCROLL`. La navegación llega a `/es/diy` con el
  fragmento, y el scroll por fragmento baja hasta `#styles`. Desde `/en/diy` sin
  paso (todavía en la introducción) y en el resto del sitio, el selector sigue
  conservando el desplazamiento.
- **El paso es el mismo en los dos idiomas** porque el
  [Módulo D1](#módulo-d1-el-contenido-en-yaml-y-su-validación) exige los mismos
  `id` en el mismo orden.

### Errores comunes

- **Escribir el fragmento sin `replaceUrl`.** Cada paso leído sería una entrada
  del historial, y Atrás recorrería la guía paso por paso.
- **Escribir el fragmento sin `KEEP_SCROLL`.** El scroll por fragmento llevaría
  el paso al borde superior mientras la persona lee: la página saltaría.
- **Medir con una línea exacta, sin margen.** Al llegar a un paso desde la lista,
  el borde queda justo en la línea; un redondeo de medio píxel marcaría el paso
  anterior.
- **Quitar `KEEP_SCROLL` del selector en todo el sitio.** En la portada, cambiar
  de idioma volvería a saltar al título de la sección.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué la URL sigue el paso que se está leyendo y no solo el que se eligió en la lista?

**Respuesta:**

Porque la mayoría de la gente llega a un paso desplazándose, no haciendo clic.
Si la URL solo cambiara con la lista, al cambiar de idioma o al copiar el enlace
se perdería el lugar. Al seguir la lectura, la URL siempre dice dónde está la
persona. El coste es una navegación por cada cambio de paso, que se mantiene
barata: reemplaza la entrada del historial (`replaceUrl`), no mueve la página
(`KEEP_SCROLL`) y no se hace si el paso no cambió.

#### 2. En el resto del sitio el cambio de idioma conserva el desplazamiento. ¿Por qué en la guía va al paso?

**Respuesta:**

Porque conservar el desplazamiento solo sirve si el mismo número de píxeles
señala el mismo contenido en los dos idiomas. En la portada se decidió que
cambiar de idioma no mueva la página: quien lee ve las mismas secciones con otras
etiquetas. En la guía, cada paso es un texto largo y los dos idiomas no miden lo
mismo: el mismo desplazamiento cae en otro paso. Por eso el selector quita
`KEEP_SCROLL` solo cuando la dirección es la guía con un paso, y deja que el
scroll por fragmento lleve a ese paso.

#### 3. ¿Por qué `replaceUrl` y no `history.replaceState` directamente?

**Respuesta:**

Porque el enrutador de Angular tiene su propio registro de la URL actual. Si
cambias la dirección por fuera con `history.replaceState`, el enrutador no se
entera: `router.url` sigue con el fragmento anterior y el selector de idioma, que
lee la URL del enrutador, construiría el enlace con el paso viejo. Con
`router.navigate` y `replaceUrl: true`, la dirección y el enrutador cambian
juntos.

<!-- /study-guide:section:diy-d3-step-fragment -->

---

<!-- study-guide:section:diy-d4-bonus-link -->
## Módulo D4: El cierre hacia el Bonus

Fuente: `src/app/home/pages/diy-page/diy-page.component.html`,
`src/app/home/constants/diy-labels.constants.ts`, `scripts/diy-content.mjs` y
`scripts/diy-content.test.mjs`.

### El problema que resuelve

La guía DIY es la versión corta. La completa es esta guía de construcción, que
se publica, revisada, como Bonus de la Guía de Angular
(`https://angular-wiki.reskyon.com/portfolio-bonus/`). Hacía falta un cierre que
lleve allí sin sacar a nadie de la guía por sorpresa. Y como la guía es pública,
nada en ella puede depender del repositorio privado ni copiar el código de la
plantilla comprada.

### La decisión en este sitio

- **Un cierre con su propio título** («Go further» / «Ve más a fondo»), un texto
  y un botón al Bonus.
- **El enlace abre en una pestaña nueva y lo dice.** Su nombre accesible suma
  «(opens in a new tab)» o «(abre en una pestaña nueva)».
- **El Bonus está en español**, y el botón en inglés lo avisa: «Read the full
  Bonus (in Spanish)».
- **El mismo enlace en los dos idiomas, con HTTPS**, comprobado por la
  validación y por una prueba con los archivos reales.
- **Ningún enlace al repositorio privado.** La validación falla si el contenido lo
  menciona. Los ejemplos son del propio proyecto, no de la plantilla.
- **El enlace se agregó después de publicar el Bonus**, para no enlazar una
  página que todavía no existía.

### El código


La regla que mantiene la guía independiente del repositorio privado:

```js
// The guide has to be readable without access to the private repository.
const PRIVATE_REPOSITORY = /github\.com\/Reskyon\/janioisacura/i

if (PRIVATE_REPOSITORY.test(JSON.stringify(data)))
  fail('it links to the private portfolio repository; the guide must not depend on it.')
```

### Cómo funciona por dentro

- **`href` y no `routerLink`.** El Bonus está en otro sitio, así que el enlace es
  un `<a>` normal. `routerLink` es para rutas de la propia aplicación.
- **`rel="noopener"`.** La pestaña nueva no recibe una referencia a esta
  (`window.opener`), así que no puede cambiar la página de origen.
- **El aviso de pestaña nueva.** Quien usa lector de pantalla oye el nombre
  completo, con «(opens in a new tab)». Quien ve la página lee el botón y el
  idioma del destino.
- **Comprobar todo el contenido de una vez.** `JSON.stringify(data)` convierte la
  guía entera en un texto, y una sola expresión regular revisa todos los campos,
  incluidos los bloques de código.
- **De dónde sale el Bonus.** Es una exportación revisada de esta guía. Cómo se
  revisa y se publica está en
  [Tareas y diagnóstico de fallos](maintenance.md#publicar-el-bonus-a-partir-de-la-wiki).

### Errores comunes

- **`target="_blank"` sin avisar.** Quien no ve la pantalla no sabe que cambió de
  pestaña, y el botón Atrás no hace nada.
- **Un enlace distinto en cada idioma.** La comparación entre idiomas del
  [Módulo D1](#módulo-d1-el-contenido-en-yaml-y-su-validación) lo detiene.
- **Enlazar antes de publicar.** Un 404 en el cierre de la guía es lo último que
  ve quien la terminó.
- **Ejemplos que solo funcionan con el repositorio.** La guía es para otros
  proyectos: un archivo privado en un ejemplo la deja a medias.

### Preguntas de entrevista (senior)

#### 1. ¿Cuándo conviene abrir un enlace en una pestaña nueva?

**Respuesta:**

Pocas veces, porque le quita a la persona la decisión. Aquí se justifica: el
cierre lleva a otro sitio, largo y en otro idioma, y quien termina la guía puede
querer volver a ella. Si se hace, hay que avisarlo en el nombre del enlace y usar
`rel="noopener"`, para que la página nueva no pueda tocar la de origen.

#### 2. ¿Por qué una prueba con los archivos reales, si ya hay pruebas de cada regla?

**Respuesta:**

Porque las pruebas de reglas usan datos inventados y demuestran que la regla
funciona, no que el contenido publicado la cumple. La prueba con los archivos
reales fija lo que importa del producto: seis pasos en los dos idiomas y el
cierre en el Bonus público. Si alguien cambia la URL por error, falla en la
integración continua y no en producción.

<!-- /study-guide:section:diy-d4-bonus-link -->
