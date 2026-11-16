# Parte 2: Cimientos de estilo

> Esta versión pública conserva las explicaciones y omite fragmentos que reproducen o adaptan la plantilla comercial.

Esta parte deja la base sobre la que se construye toda la interfaz: Bootstrap
instalado por partes en vez de entero, una carpeta `src/styles/` con las
variables, los tokens de color, las fuentes y las reglas base, un único
archivo `src/styles.scss` que los ordena, los alias de importación y el
esqueleto de página de Portify (encabezado, navegación vertical y columna de
contenido). Cada sección que se estilice después importa estas piezas y se
coloca dentro de ese esqueleto; por eso van primero.

**Si llegaste aquí desde un buscador.** Esta página es una parte de la guía
«Cómo se construye este sitio», escrita sobre el repositorio de
janioisacura.com, un portfolio hecho con Angular que se publica como HTML
estático. El punto de partida visual es Portify, una plantilla HTML con
Bootstrap 5 y SCSS que aquí se reconstruye en Angular. Cada módulo explica el
problema, muestra el código completo y lo que enseña sirve para cualquier
proyecto que use Bootstrap con Sass, con Angular o sin él. Para seguirla
necesitas Node.js y el CLI de Angular.

**Proyecto:** `src/styles/`, `src/styles.scss`, el bloque `"styles"` de
`angular.json`, `tsconfig.json` y `src/app/shared/`. **Sitio publicado:**
[janioisacura.com](https://janioisacura.com/en/); el fondo amarillo, la
navegación vertical y el menú móvil son lo que esta parte construye (si aún no
se ven, la rama de trabajo no se ha publicado).

**Qué vas a aprender:**

- [Módulo E1](#módulo-e1-bootstrap-por-partes-y-la-carpeta-srcstyles):
  **Bootstrap por partes.** Por qué el CSS de Portify pesa 4 MB, qué partes de
  Bootstrap usa el sitio, cómo queda la carpeta `src/styles/` y en qué orden
  las importa `styles.scss`.
- [Módulo E2](#módulo-e2-variables-sin-css-y-por-qué-import-y-no-use):
  **Variables sin CSS.** El archivo `_tools.scss` que los componentes importan
  sin duplicar Bootstrap, el mixin de *breakpoints* y la pregunta que siempre
  aparece: por qué `@import` y no `@use`.
- [Módulo E3](#módulo-e3-tokens-de-color-como-tripletas-rgb): **Tokens de
  color.** El truco de Portify de guardar el color como tripleta RGB, para qué
  sirve y por qué los colores de marca todavía no son tokens.
- [Módulo E4](#módulo-e4-fuentes-y-reglas-base): **Fuentes y reglas base.**
  Dónde quedaron los `@font-face` de la Parte 1, qué parte del *reset* de
  Portify se convirtió en variables de Bootstrap y qué reglas globales quedan.
- [Módulo E5](#módulo-e5-alias-de-importación-en-tsconfig): **Alias de
  importación.** `@shared`, `@home`, `@generated` e `@interfaces` en
  `tsconfig.json`, quién los resuelve y por qué el script de contenido los
  escribe también.
- [Módulo E6](#módulo-e6-el-esqueleto-de-página-encabezado-navegación-y-columna-de-contenido):
  **El esqueleto de página.** `App` dueña del `<main>`, el encabezado con el
  menú móvil gobernado por una señal, las secciones de la portada en una constante y
  los enlaces por fragmento que funcionan desde cualquier página.
- [Módulo E7](#módulo-e7-los-estilos-del-menú-de-portify-traducidos-a-un-componente):
  **Los estilos del menú.** El SCSS de Portify traducido a un componente
  encapsulado: panel deslizante, overlay por combinador de hermanos, línea
  animable y el error de la barra de scroll.

Cada módulo sigue el mismo orden: el problema que resuelve, la decisión tomada
en este sitio, el procedimiento o el código completo, cómo funciona por
dentro, errores comunes y preguntas de entrevista con su respuesta.

Esta página es una parte de la guía [Cómo se construye este sitio](como-se-construye.md);
allí están el mapa y la ruta recomendada. Conviene haber leído antes
[Estilos y animaciones](estilos-y-animaciones.md), que describe los tres archivos
SCSS de Portify que aquí se traducen, y la [Parte 1](01-marca-y-recursos.md), de
donde vienen las fuentes que esta parte carga.

---

<!-- study-guide:section:styles-e1-bootstrap-subset -->
## Módulo E1: Bootstrap por partes y la carpeta src/styles

Fuente: `package.json`, `angular.json`, `src/styles.scss` y
`src/styles/_bootstrap.scss` del repositorio.

### El problema que resuelve

El HTML de Portify está escrito con Bootstrap: la rejilla (`row`, `col-xl-9`),
los utilitarios (`d-flex`, `gap-4`, `mb-4`, `d-xl-none`) y los botones
(`btn`, `btn-secondary`). Para reconstruir sus pantallas en Angular hace falta
ese mismo CSS. Pero la plantilla importa Bootstrap **entero** y le suma la
fuente de iconos Phosphor en base64; su `index.css` compilado pesa 4 MB sin
minificar. El sitio no usa el modal, el carrusel, los *tooltips* ni el
JavaScript de Bootstrap, y Angular tiene un presupuesto (`budgets` en
`angular.json`) que avisa cuando el paquete inicial pasa de 600 kB.

### La decisión en este sitio

- Bootstrap 5.3 se instala por npm y se importa **sólo por partes**: `root`,
  `reboot`, `images`, `containers`, `grid`, `buttons`, `utilities` y
  `utilities/api`.
  Nada de componentes (modal, nav, dropdown) y nada de JavaScript, así que
  tampoco hace falta Popper.
- Los estilos globales viven en una carpeta `src/styles/` con cinco archivos
  parciales, uno por responsabilidad, y `src/styles.scss` sólo los importa en
  orden.
- Las versiones de Bootstrap en el `package.json` llevan acento circunflejo
  (`^5.3.9`), como el resto de dependencias: acepta parches y versiones
  menores, no una 6.

### El procedimiento

Instalar Bootstrap desde la raíz del repositorio:

```bash
npm install bootstrap@5.3
```

Crear la carpeta y los archivos. Los nombres que empiezan por guion bajo son
parciales de Sass: no se compilan por su cuenta, sólo cuando otro archivo los
importa.


`src/styles/_bootstrap.scss`:


`src/styles.scss`, el archivo que `angular.json` declara en `"styles"`:


Y en `angular.json`, dentro de `architect.build.options`, debajo de
`"styles"`:

```json
"stylePreprocessorOptions": {
  "includePaths": ["src/styles"],
  "sass": { "silenceDeprecations": ["import"] }
}
```

Comprobar con `npm run build`. La tabla que imprime Angular muestra el peso
del CSS global:


106 kB sin comprimir y unos 10 a 15 kB comprimidos, frente a los 4 MB de la
plantilla. El presupuesto de 600 kB queda lejos.

### Cómo funciona por dentro

- **Bootstrap son muchos archivos pequeños.** `node_modules/bootstrap/scss/`
  tiene un parcial por pieza: `_grid.scss`, `_buttons.scss`, etc. El archivo
  `bootstrap.scss` que importa la plantilla no es más que una lista que los
  importa todos. Escribir la lista uno mismo es la forma oficial de usar sólo
  una parte; Bootstrap lo documenta como «importar por partes».
- **El orden importa.** Las partes que emiten CSS necesitan que antes se
  hayan cargado las funciones, las variables, los mapas y los mixins; eso lo
  hace `_tools.scss` (Módulo E2), y por eso `styles.scss` lo importa primero.
  Dentro de `_bootstrap.scss`, `utilities` tiene que ir antes de
  `utilities/api`: el primero define el mapa `$utilities` (qué clases
  existen) y el segundo lo recorre y genera las clases.
- **`root` y `reboot`.** `root` escribe las variables CSS `--bs-*` en
  `:root`; `reboot` es el *reset* de Bootstrap (márgenes, `box-sizing`,
  tipografía base del `body`, enlaces). Las reglas del `body` que Portify
  escribía a mano salen de aquí a partir de variables (Módulo E4).
- **Angular resuelve `bootstrap/scss/...`** buscando en `node_modules`, igual
  que haría webpack. No hace falta ruta relativa ni el prefijo `~` de otros
  proyectos.
- **`includePaths`** añade `src/styles/` a las carpetas donde Sass busca lo
  que se importa sin ruta. Así un componente en
  `src/app/shared/components/header/` escribe `@import 'tools';` en vez de
  `@import '../../../../styles/tools';`.
- **`silenceDeprecations: ["import"]`** calla el aviso de Sass por usar
  `@import`. El Módulo E2 explica por qué se usa igual.

### Errores comunes

- **Importar `bootstrap/scss/bootstrap` «para ir rápido».** Trae los 30 y
  pico componentes y multiplica el CSS; después cuesta saber qué se usa.
  Mejor empezar por lo mínimo y añadir un parcial cuando una pantalla lo
  pida.
- **`utilities/api` sin `utilities`.** Falla con «undefined variable
  `$utilities`»: el mapa que recorre la API no existe.
- **Usar clases que necesitan el JavaScript de Bootstrap.** `data-bs-toggle`,
  `data-bs-spy` o `collapse` no hacen nada sin el *bundle* de JS, que aquí no
  se incluye a propósito. El menú móvil y el resaltado de la sección activa
  se hacen con Angular.
- **Olvidar `includePaths` y mover la carpeta.** Si `src/styles/` cambia de
  sitio (por ejemplo a `src/app/styles/`), hay que actualizar `includePaths`
  y las rutas de `styles.scss`; los dos apuntan a la carpeta por su ruta.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué importar Bootstrap por partes en lugar de importarlo entero y quitar lo que sobra con PurgeCSS?

**Respuesta:**

PurgeCSS borra las clases que no encuentra en el HTML, pero trabaja a
ciegas: una clase que Angular añade en tiempo de ejecución (`[class.open]`)
o que viene de una variable no aparece en el HTML y se borra igual, y hay que
mantener una lista de excepciones. Importar por partes es explícito: se sabe
exactamente qué hay en el CSS, no depende de un escaneo y no tiene falsos
positivos. Las dos cosas se pueden combinar; aquí la primera alcanza, el CSS
queda en unos 15 kB comprimidos.

#### 2. ¿Qué hace `reboot` y en qué se diferencia de un *reset* como `normalize.css`?

**Respuesta:**

Los dos parten de la misma idea: igualar los estilos por defecto de los
navegadores. `normalize.css` corrige diferencias entre navegadores y conserva
los valores útiles (por ejemplo, el tamaño de los títulos). `reboot` es
`normalize` más las opiniones de Bootstrap: `box-sizing: border-box` en
todo, márgenes sólo hacia abajo, la tipografía base del `body` y los enlaces
tomados de variables de Sass, y los `<h1>` a `<h6>` con los tamaños de
`$h1-font-size` y compañía. Como todo sale de variables, cambiar la fuente
del sitio es cambiar una variable antes de importar `reboot`, no escribir una
regla que lo pise.

#### 3. ¿Cómo sabes cuánto pesa el CSS que publica Angular y si entra en el presupuesto?

**Respuesta:**

La tabla que imprime `ng build` da el tamaño en crudo y el «estimated
transfer size», una estimación comprimida. Los presupuestos están en
`angular.json`, en `budgets`: el de tipo `initial` suma JavaScript y CSS de la
primera carga (aquí avisa a 600 kB y falla a 1 MB) y el de
`anyComponentStyle` limita el CSS de cada componente (4 kB y 8 kB). Si un
componente de estilos grandes pasa el límite, se sube el presupuesto a
conciencia o se mueve parte del estilo a los globales; la decisión queda
escrita en el `angular.json`.

<!-- /study-guide:section:styles-e1-bootstrap-subset -->

---

<!-- study-guide:section:styles-e2-tools-import -->
## Módulo E2: Variables sin CSS y por qué import y no use

Fuente: `src/styles/_tools.scss` del repositorio.

### El problema que resuelve

Los componentes de Angular tienen sus propios archivos de estilo, y van a
necesitar las mismas herramientas que los globales: el mixin de *breakpoints*
de Portify (`min-width(xl)`), los colores (`$black`) y los mapas de Bootstrap
(`$grid-breakpoints`). Si un componente importara `_bootstrap.scss` para
tenerlas, Angular copiaría todo el CSS de Bootstrap dentro del estilo de ese
componente, una vez por componente. Hace falta un archivo que dé las
variables y los mixins **sin emitir una sola regla CSS**.

### La decisión en este sitio

- `_tools.scss` importa de Bootstrap sólo `functions`, `variables`,
  `variables-dark`, `maps` y `mixins`: definiciones, no CSS. Cualquier archivo
  puede importarlo tantas veces como haga falta sin engordar el resultado.
- Antes de las variables de Bootstrap van los valores de Portify (colores,
  botones, el mapa de `gutters` hasta 10) y la tipografía de marca de la Parte
  1 expresada como variables de Bootstrap.
- El mixin `min-width` de Portify se copia con una corrección: usa `map.get`
  del módulo `sass:map` en lugar de la función global `map-get`, que Sass ha
  desaprobado.
- Se mantiene `@import` para cargar Bootstrap, con el aviso de Sass
  silenciado, y la razón queda escrita en un comentario al principio del
  archivo para que no se pierda.
- `$header-height` (69 px) es la altura de la barra del encabezado cuando es fija
  por debajo de `xl`. Vive aquí porque la usan `_base.scss` y, como valor
  inicial, el componente (el [Módulo E7](#módulo-e7-los-estilos-del-menú-de-portify-traducidos-a-un-componente)).

### El código

`src/styles/_tools.scss` completo:


Desde un componente se usa así:


### Cómo funciona por dentro

- **`!default` es la clave de los *overrides*.** Cada variable de Bootstrap
  está declarada como `$primary: $blue !default;`, que significa «asigna este
  valor sólo si la variable no existe todavía». Por eso los valores propios van
  **antes** de `@import 'bootstrap/scss/variables'`: cuando Bootstrap llega a
  `$primary`, ya vale `$yellow` y respeta ese valor. Puestos después, ya no
  cambian nada de lo que Bootstrap calculó con ellos (los colores de los
  botones, por ejemplo).
- **`@import` comparte un único ámbito global.** Todo lo que define un archivo
  importado (variables, funciones, mixins) queda visible para los archivos
  siguientes. Bootstrap 5 cuenta con eso: `_variables.scss` llama a funciones
  de `_functions.scss` sin cargarlas, porque da por hecho que alguien las
  importó antes. Y `_mixins.scss` usa variables de `_variables.scss` de la
  misma forma.
- **`@use` aísla cada archivo en un módulo.** Lo que define un archivo cargado
  con `@use` sólo se ve con prefijo (`tools.$black`, `@include
  tools.min-width(xl)`), y las variables se configuran con `with (...)`. Es el
  diseño correcto para código nuevo, pero no sirve para Bootstrap 5:
  `@use 'bootstrap/scss/variables' with ($primary: $yellow)` falla porque, ya
  dentro de su módulo, `_variables.scss` no encuentra las funciones que
  necesita. Bootstrap migrará al sistema de módulos en la versión 6; hasta
  entonces su documentación sigue mostrando `@import`.
- **Por qué no mezclar.** Los componentes podrían hacer `@use 'tools'` y
  escribir todo con prefijo, pero `_tools.scss` seguiría cargando Bootstrap
  con `@import` por dentro, así que el aviso de Sass aparecería igual y el
  proyecto tendría dos sintaxis. Mejor una sola, y el cambio completo cuando
  Bootstrap 6 lo permita: `_tools.scss` pasa a `@use ... with (...)`, los
  componentes a `@use 'tools'`, y se borra `silenceDeprecations`.
- **`@use 'sass:map'` sí.** Los módulos integrados de Sass (`sass:map`,
  `sass:math`, `sass:color`) se cargan con `@use` sin ese problema, y las
  funciones globales equivalentes (`map-get`, `map-keys`) están desaprobadas
  y desaparecerán en Dart Sass 3. La regla `@use` tiene que ir al principio
  del archivo, antes de cualquier `@import`; sólo los comentarios pueden
  precederla.
- **Importar `tools` dos veces no cuesta nada.** `styles.scss` lo importa una
  vez para los globales y cada componente otra vez para sí mismo. Como no
  emite CSS, el resultado no crece; Sass sólo vuelve a calcular variables.

### Errores comunes

- **Poner los valores propios después de importar `variables`.** No da
  error: Bootstrap simplemente ya decidió todo con sus valores por defecto y
  los tuyos no se usan donde importaba.
- **Importar `_bootstrap.scss` (el que emite CSS) desde un componente.**
  Funciona, pero cada componente que lo haga lleva una copia entera de la
  rejilla y los utilitarios, y el presupuesto `anyComponentStyle` avisa.
- **Usar `map-get` en vez de `map.get`.** Angular muestra el aviso «Global
  built-in functions are deprecated» en cada compilación. Se corrige con
  `@use 'sass:map'` al principio y `map.get` / `map.keys` en el código.
- **Colocar `@use` después de un `@import` o de una regla.** Sass lo rechaza:
  «@use rules must be written before any other rules».
- **Pedir un *breakpoint* que no existe** (`min-width(xxxl)`). El mixin no
  falla, pero emite el `@warn` con la lista de nombres válidos: `xs`, `sm`,
  `md`, `lg`, `xl`, `xxl`.

### Preguntas de entrevista (senior)

#### 1. ¿Qué diferencia hay entre `@import` y `@use` en Sass, y por qué este proyecto usa `@import` si está desaprobado?

**Respuesta:**

`@import` vuelca todo lo que define el archivo importado en un ámbito global
compartido, se puede repetir y las variables se pisan por orden de carga.
`@use` carga el archivo una sola vez como módulo con espacio de nombres, sus
miembros se leen con prefijo y se configuran con `with (...)`; evita
colisiones y hace explícito de dónde viene cada cosa. Es la sintaxis
recomendada, pero una dependencia escrita para el ámbito global, como
Bootstrap 5, no se puede cargar con `@use` sin romperse: sus archivos cuentan
con ver las funciones y variables de los anteriores. La decisión es seguir la
sintaxis que la dependencia soporta, silenciar ese único aviso y documentar
en el código el momento de migrar (Bootstrap 6).

#### 2. ¿Cómo permite `!default` «tematizar» una librería sin tocar su código?

**Respuesta:**

`!default` asigna un valor sólo si la variable no estaba definida. La librería
declara todos sus ajustes así, y quien la usa define los suyos antes de
importarla: la librería respeta los que existen y rellena el resto. Es una
inversión del orden habitual (primero mis valores, después la librería) y
exige disciplina en el orden de los `@import`. El equivalente con módulos es
`@use 'lib' with ($primary: ...)`, que hace lo mismo pero verificado: si pasas
una variable que la librería no declara, Sass da error en vez de ignorarla.

#### 3. Un componente necesita un *breakpoint* de Bootstrap. ¿Cómo lo haces sin duplicar el CSS de Bootstrap en ese componente?

**Respuesta:**

Separando «definiciones» de «CSS»: un parcial que sólo importa `functions`,
`variables`, `maps` y `mixins` de Bootstrap no emite reglas, así que cada
componente puede importarlo sin coste. El componente escribe `@import 'tools'`
(con `includePaths` para no escribir la ruta) y usa `@include
media-breakpoint-up(xl)` de Bootstrap o el mixin propio `min-width(xl)`. El
CSS que sí pesa, rejilla y utilitarios, se importa una sola vez en los
estilos globales.

<!-- /study-guide:section:styles-e2-tools-import -->

---

<!-- study-guide:section:styles-e3-color-tokens -->
## Módulo E3: Tokens de color como tripletas RGB

Fuente: `src/styles/_tokens.scss` del repositorio y la sección
[Cómo se define el color](estilos-y-animaciones.md#cómo-se-define-el-color) de la
referencia de Portify.

### El problema que resuelve

El mismo color aparece decenas de veces en Portify con distintas opacidades:
el negro sólido en el texto, el negro al 30 % en la línea del menú, al 15 % en
el fondo del enlace activo, al 6 % en el pie. Con una variable de Sass
(`$black`) eso se resuelve en tiempo de compilación, pero el color queda
«horneado» en el CSS y no se puede cambiar en el navegador. Con una variable
CSS (`--black: #000`) se puede cambiar en vivo, pero `rgba(var(--black), 0.3)`
no es válido: `rgba()` espera tres números, no un color.

### La decisión en este sitio

- Se conserva el mecanismo de Portify: tres variables CSS en `:root` cuyo valor
  es la **tripleta RGB sin `rgb()`**. El color se usa siempre a través de
  `rgb(var(--x))` o `rgba(var(--x), alpha)`.
- Los valores son los de Portify: amarillo `#ffdb67`, negro y blanco. La paleta
  de marca de Janio (morado `#563d7c`, violeta, amarillo, verde azulado y
  verde) está documentada en `docs/site-structure.md` y **no** se convierte en
  tokens todavía; Janio decide cuándo, con los bocetos.
- El amarillo existe en dos sitios y hay que cambiarlo en los dos: aquí como
  `--primary` para los estilos propios, y en `_tools.scss` como `$primary`
  para lo que Bootstrap compila (los botones).

### El código

`src/styles/_tokens.scss`:


Uso en cualquier regla, global o de componente:


### Cómo funciona por dentro

- **`var()` sustituye texto.** Una variable CSS puede contener cualquier cosa,
  no sólo un color. `--black: 0, 0, 0` guarda literalmente «0, 0, 0», y
  `rgba(var(--black), 0.3)` se convierte en `rgba(0, 0, 0, 0.3)` antes de que
  el navegador lo interprete. Por eso funciona aunque `rgba()` no acepte un
  color como primer argumento.
- **Cambiar un token cambia todo en vivo.** Portify lo aprovecha en su
  selector de color de demostración:
  `document.documentElement.style.setProperty('--primary', '255, 0, 0')`
  repinta la página entera. Aquí no hay selector, pero el mecanismo queda
  disponible para un modo oscuro o para aplicar la marca más adelante.
- **Dos mundos: Sass y CSS.** `$primary` (Sass) se evalúa al compilar y ya no
  existe en el navegador; Bootstrap lo usa para generar `.btn-secondary` y sus
  estados. `--primary` (CSS) vive en el navegador y lo leen las reglas
  propias. Portify mezcla los dos y por eso un cambio de paleta exige tocar
  `_tools.scss` y `_tokens.scss`.
- **La alternativa moderna.** CSS tiene hoy `color-mix(in srgb, var(--black)
  30%, transparent)` y la sintaxis de color relativo
  `rgb(from var(--black) r g b / 0.3)`, que permiten guardar el color completo
  (`--black: #000`) y derivar opacidades. Funcionan en los navegadores
  actuales; se conserva la tripleta porque es lo que usa todo el SCSS de
  Portify que se va a traducir, y cambiarlo sería reescribir cada regla.

### Errores comunes

- **Escribir `color: var(--black)`.** El resultado es `color: 0, 0, 0`, que
  no es un color válido, y la regla se ignora sin aviso. Siempre dentro de
  `rgb()` o `rgba()`.
- **Guardar la tripleta con `rgb()` incluido** (`--black: rgb(0, 0, 0)`).
  Entonces `rgb(var(--black))` se convierte en `rgb(rgb(0, 0, 0))` y falla.
- **Cambiar sólo `--primary` y esperar que cambien los botones.** Los
  botones salen de `$primary` y `$secondary` compilados; hay que cambiar
  también `_tools.scss`.
- **Convertir la paleta de marca en tokens «porque ya está documentada».**
  En esta etapa los tokens mantienen los valores de la plantilla a propósito.

### Preguntas de entrevista (senior)

#### 1. ¿Cuándo usas una variable de Sass y cuándo una variable CSS?

**Respuesta:**

Variable de Sass para lo que se decide al compilar y no cambia después:
*breakpoints*, espaciados que alimentan mapas y bucles, configurar una
librería como Bootstrap. Variable CSS para lo que puede cambiar en el
navegador o depende del contexto: colores de tema, modo oscuro, un valor que
JavaScript o una clase en un contenedor ajustan, y todo lo que un componente
quiere exponer para que el padre lo sobrescriba. Las dos conviven: la de
Sass puede escribir el valor inicial de la de CSS.

#### 2. ¿Por qué Portify guarda los colores como «255, 219, 103» y no como `#ffdb67`? ¿Lo harías igual hoy?

**Respuesta:**

Porque necesitaba el mismo color con varias opacidades y cambiarlo en vivo
desde JavaScript; `rgba(var(--x), 0.3)` sólo funciona si la variable guarda
los tres números. Hoy, en un proyecto nuevo, guardaría el color completo y
derivaría las opacidades con `color-mix()` o la sintaxis de color relativo,
que además permiten mezclar colores y trabajar en `oklch`. En este sitio se
mantiene la tripleta porque la base de estilos que se traduce ya está escrita
así y la coherencia pesa más que la novedad.

#### 3. Tienes la paleta de marca definida. ¿Por qué no la aplicas ya como tokens?

**Respuesta:**

Porque un token es una decisión de diseño con nombre (`--primary` es «el color
principal de la interfaz»), y asignar un color de marca a ese papel sin
bocetos es adivinar: el morado puede ser fondo, acento o sólo el color del
logo. Mientras no esté decidido, los tokens llevan los valores de la plantilla,
que ya funcionan con contraste suficiente, y la paleta vive en la
documentación. Cuando la decisión exista, el cambio es local: dos archivos.

<!-- /study-guide:section:styles-e3-color-tokens -->

---

<!-- study-guide:section:styles-e4-fonts-base -->
## Módulo E4: Fuentes y reglas base

Fuente: `src/styles/_fonts.scss` y `src/styles/_base.scss` del repositorio.

### El problema que resuelve

La Parte 1 dejó los `@font-face` y la tipografía base en `src/styles.scss`.
Ahora ese archivo es sólo el orquestador, así que las fuentes necesitan su
propio parcial. Y el *reset* de Portify (`body` amarillo, enlaces sin
subrayado, títulos y párrafos sin margen) hay que repartirlo: parte se expresa
mejor como variables de Bootstrap, antes de que `reboot` genere su CSS, y
parte sigue siendo reglas globales que Bootstrap no cubre.

### La decisión en este sitio

- `_fonts.scss` contiene las cuatro reglas `@font-face` del
  [Módulo M5](01-marca-y-recursos.md#módulo-m5-cargar-las-fuentes-con-font-face),
  sin cambios.
- Lo que Portify escribía como reglas y Bootstrap ya genera desde variables
  pasa a `_tools.scss`: la familia y el peso del `body`, la familia, el
  estilo y el peso de los títulos, los márgenes a cero de títulos y párrafos,
  y los enlaces negros sin subrayado.
- `_base.scss` guarda lo que no tiene variable: `font-synthesis`, el fondo
  amarillo con el token, `overflow-x: hidden`, el tracking de los títulos,
  los botones más grandes en pantallas `xxl`, el ancho máximo del contenedor
  en pantallas de 1750 px y, desde la Parte 4, la regla del interruptor de
  animaciones (`:root[data-motion='off']`), que sustituyó a una de movimiento
  reducido que Portify no traía. Y, por debajo de `xl`, el `scroll-padding-top`
  que deja las secciones justo bajo el encabezado fijo (el [Módulo E7](#módulo-e7-los-estilos-del-menú-de-portify-traducidos-a-un-componente)).

### El código

`src/styles/_base.scss`:


Las variables que sustituyen al *reset* de Portify, ya vistas en `_tools.scss`:

| Regla de Portify | Variable de Bootstrap en `_tools.scss` |
| --- | --- |
| `body { font-family: "Poppins" }` | `$font-family-sans-serif: 'Mozilla Text', system-ui, sans-serif` |
| `html { font-weight: 300 }` (Parte 1) | `$font-weight-base: 300` |
| `h1…h6 { font-family; font-style; font-weight }` (Parte 1) | `$headings-font-family`, `$headings-font-style: italic`, `$headings-font-weight: 600` |
| `h1…h6, p { margin-bottom: 0 }` | `$headings-margin-bottom: 0`, `$paragraph-margin-bottom: 0` |
| `a { color: black; text-decoration: none }` | `$link-color`, `$link-hover-color`, `$link-decoration: none` |

### Cómo funciona por dentro

- **`reboot` escribe el `body` y los títulos a partir de las variables.**
  `$font-family-base` toma por defecto `$font-family-sans-serif`, así que
  cambiar esta última cambia la fuente de todo el sitio; `$headings-font-style`
  existe en Bootstrap 5.3 justamente para casos como el nuestro, en que los
  títulos van en cursiva. El resultado compilado es el mismo que escribir las
  reglas a mano, pero coherente con el resto de Bootstrap (los `.btn`, por
  ejemplo, heredan `$font-weight-base` donde corresponde).
- **`font-synthesis: none` sigue en `html`.** Bootstrap no tiene variable
  para ello. Sólo hay cargado un peso de Mozilla Text (Light, 300); si alguna
  regla pide 500 o 700, el navegador no inventa una negrita y usa el 300. Es
  visible y se corrige cargando el peso que falte (Parte 1, Módulo M5).
- **El tracking no va en variable.** Bootstrap no tiene `letter-spacing` para
  títulos; queda como regla, con el valor de Illustrator convertido a `em`.
- **`min-width(xxl)` funciona aquí** porque `styles.scss` importó `tools`
  antes que `base`: el mixin y `$grid-breakpoints` ya existen en el ámbito
  global cuando Sass llega a este archivo.
- **Movimiento: de la preferencia del sistema al interruptor.** Esta etapa
  nació con una regla bajo `@media (prefers-reduced-motion: reduce)` que
  acortaba animaciones y transiciones a 0,01 ms. Se retiró cuando se
  construyó el interruptor de animaciones (Parte 4, Módulo A4): el sitio anima
  por defecto y **no consulta la preferencia del sistema** (decisión del 13 de
  noviembre de 2026), y la regla pasó a depender de un atributo,
  `:root[data-motion='off']`, que pone el servicio del interruptor. La nueva
  regla acorta las animaciones y **quita** las transiciones (`transition:
  none`), porque una transición acortada conserva su retraso (el del menú
  móvil dejaba sus enlaces en el orden de tabulación). GSAP y el lienzo de
  puntos dependen del mismo servicio.
- **1750 px y 1740 px.** Portify limita el ancho del `container-fluid` en
  pantallas muy anchas para que las líneas de texto no se alarguen de más;
  es el mismo valor que usa después para colocar la navegación vertical.

### Errores comunes

- **Dejar los `@font-face` y las variables en archivos que se importan en el
  orden equivocado.** Las fuentes pueden declararse en cualquier punto, pero
  las variables de tipografía tienen que estar antes de
  `bootstrap/scss/variables` (Módulo E2). Si `reboot` sale con la fuente por
  defecto de Bootstrap, el orden es la causa.
- **Repetir en `_base.scss` lo que ya hace una variable** (por ejemplo,
  volver a escribir `a { text-decoration: none }`). No rompe nada, pero
  duplica reglas y la próxima persona no sabe cuál manda.
- **Quitar el movimiento con `animation: none !important`.** Deja esperando
  al código que escucha el final de la animación. Acortar la duración es más
  seguro.
- **Esperar una negrita en un `<strong>`.** Con `font-synthesis: none` y
  sólo el peso 300 cargado, se verá igual que el texto normal hasta que se
  cargue un peso más.

### Preguntas de entrevista (senior)

#### 1. ¿Cómo respetas la preferencia de movimiento reducido en un sitio con animaciones de CSS y de JavaScript?

**Respuesta:**

En CSS, con una regla global bajo `@media (prefers-reduced-motion: reduce)`
que acorte animaciones y transiciones a casi cero, sin quitarlas, para no
romper los eventos de fin. En JavaScript, leyendo la misma preferencia con
`matchMedia('(prefers-reduced-motion: reduce)')` y, si es cierta, saltando a
los estados finales en vez de animar (GSAP tiene `gsap.matchMedia()` para
registrar animaciones sólo cuando la preferencia lo permite). Y, en los dos
casos, comprobar que el contenido es legible y usable sin ninguna animación:
las animaciones son un adorno sobre un estado final que tiene que funcionar
solo.

En este sitio se tomó otra decisión de producto: no consultar la preferencia
del sistema y ofrecer, en su lugar, un interruptor propio que gobierna CSS,
GSAP y el lienzo a la vez (Parte 4, Módulo A4). Lo anterior sigue siendo la
respuesta general; lo que cambia es de dónde viene el estado.

#### 2. ¿Por qué expresar el *reset* de Portify como variables de Bootstrap en vez de copiar sus reglas tal cual?

**Respuesta:**

Porque Bootstrap ya va a emitir reglas para `body`, los títulos y los
enlaces desde `reboot`; copiar las de Portify debajo las pisaría y el CSS
tendría dos versiones de cada regla, con la segunda ganando por orden. Al
expresarlas como variables, `reboot` escribe directamente el valor deseado,
una sola vez, y el resto de Bootstrap que depende de esas variables (botones,
formularios si llegan) es coherente con él. Lo que Bootstrap no cubre
(`font-synthesis`, el tracking, el ancho a 1750 px) sí se escribe como regla,
en un archivo separado y pequeño.

#### 3. Un estilo nuevo: ¿va en `_base.scss` o en el componente?

**Respuesta:**

Depende de a quién afecta. Si describe el documento entero o un elemento
HTML sin clase (`body`, `a`, `h2`, un `@media` global), va en los globales.
Si pertenece a una pieza con nombre propio (`.navigation`, `.hero`), va en el
archivo de estilos de ese componente, que Angular encapsula para que no se
filtre. La prueba práctica: si al borrar el componente la regla deja de tener
sentido, es del componente. Los componentes importan `tools` para compartir
variables y mixins sin duplicar CSS.

<!-- /study-guide:section:styles-e4-fonts-base -->

---

<!-- study-guide:section:styles-e5-path-aliases -->
## Módulo E5: Alias de importación en tsconfig

Fuente: `tsconfig.json` y `scripts/prepare-content.mjs` del repositorio.

### El problema que resuelve

Con las carpetas `home/` y `shared/` y sus subcarpetas, los imports relativos
se vuelven escaleras: `'../../../shared/constants/locales.constants'`. Son
difíciles de leer, se rompen al mover un archivo de carpeta y no dicen a
simple vista si lo importado es de `shared`, de `home` o un módulo generado.
El esqueleto de página (Módulo E6) importa desde las tres zonas a la vez, así
que es el momento de fijar la convención.

### La decisión en este sitio

| Alias | Carpeta | Para qué |
| --- | --- | --- |
| `@app/*` | `src/app/*` | Lo que no encaja en los otros (hoy no se usa) |
| `@shared/*` | `src/app/shared/*` | Componentes, constantes, interfaces y utilidades compartidas |
| `@home/*` | `src/app/home/*` | Componentes y páginas de la portada |
| `@generated/*` | `src/app/home/generated/*` | Los módulos que genera el script de contenido |
| `@interfaces/*` | `src/app/home/interfaces/*`, y si no está ahí, `src/app/shared/interfaces/*` | Interfaces de datos |

- Un import que cruza carpetas usa alias; uno de la misma carpeta sigue
  relativo (`'./app.routes'`).
- El script de contenido escribe los módulos generados con los mismos alias,
  así que un archivo generado y uno escrito a mano se leen igual.
- `@shared/*` sigue la convención de la skill `ng-setup`, que crea el mismo
  alias en los proyectos de `angular-ufh`.

### El código

En `tsconfig.json`, dentro de `compilerOptions`:

```json
"paths": {
  "@app/*": ["./src/app/*"],
  "@shared/*": ["./src/app/shared/*"],
  "@home/*": ["./src/app/home/*"],
  "@generated/*": ["./src/app/home/generated/*"],
  "@interfaces/*": ["./src/app/home/interfaces/*", "./src/app/shared/interfaces/*"]
}
```

Antes y después, en `src/app/home/pages/project-page/project-page.component.ts`:

```ts
// Antes
import { Project } from '../../interfaces/project.interface'
import { PROJECT_BODIES } from '../../generated/project-bodies'
import { Locale } from '../../../shared/constants/locales.constants'

// Después
import { Project } from '@interfaces/project.interface'
import { PROJECT_BODIES } from '@generated/project-bodies'
import { Locale } from '@shared/interfaces/shared.interface'
```

Y en `scripts/prepare-content.mjs`, la plantilla de los módulos generados:

```js
const imports = ["import type { Locale } from '@shared/interfaces/shared.interface'"]
if (interfaceName) {
  const symbol = type.replace('[]', '')
  imports.push(`import type { ${symbol} } from '@interfaces/${interfaceName}.interface'`)
}
```

### Cómo funciona por dentro

- **`paths` es de TypeScript, pero alguien tiene que resolverlo al
  empaquetar.** TypeScript sólo lo usa para comprobar tipos; no reescribe los
  imports. Angular lee `paths` del `tsconfig` y se lo pasa a su empaquetador
  (esbuild), que resuelve cada alias a un archivo real al compilar. El
  ejecutor de pruebas (`@angular/build:unit-test`, con Vitest) construye con
  la misma cadena, así que las pruebas ven los alias sin configurar nada más.
  También funcionan en un `import()` dinámico, como el de la página de
  proyecto en `app.routes.ts`.
- **Sin `baseUrl`.** Desde TypeScript 4.1 las rutas de `paths` pueden ser
  relativas al propio `tsconfig.json` (por eso empiezan por `./src`), y
  `baseUrl` ya no hace falta. `tsconfig.app.json` y `tsconfig.spec.json`
  extienden `tsconfig.json`, así que los alias se declaran una sola vez.
- **La lista de `@interfaces/*` es un orden de búsqueda.** TypeScript y
  esbuild prueban cada carpeta en orden y se quedan con el primer archivo que
  existe. Vale porque los nombres no se repiten entre `home/interfaces/` y
  `shared/interfaces/`; si se repitieran, ganaría `home` en silencio.
- **Los módulos generados no están en Git** (`src/app/home/generated/` está
  en `.gitignore`), pero sí se compilan con Angular; por eso pueden usar los
  alias. El propio script corre en Node sin empaquetador, así que **sus**
  imports siguen siendo relativos: `paths` no existe para Node.

### Errores comunes

- **Cambiar un nombre de archivo y olvidar el script.** Al renombrar
  `locales.ts` a `locales.constants.ts`, los módulos generados siguieron
  apuntando al nombre viejo hasta que se actualizó la plantilla del script y
  se volvió a ejecutar `npm run content:prepare`. Lo generado es código: si
  cambia la fuente, se regenera.
- **Dos alias para la misma carpeta.** `@app/shared/...` y `@shared/...`
  llevan al mismo sitio; mezclarlos hace que buscar usos de un archivo
  devuelva la mitad. Uno por carpeta.
- **Un alias que parece un paquete.** `shared/*` sin `@` se confundiría con
  un paquete de npm llamado `shared`; el `@` al inicio evita la colisión.
- **El editor no se entera.** Tras editar `paths`, VS Code a veces sigue
  marcando los imports en rojo hasta reiniciar el servidor de TypeScript
  (*TypeScript: Restart TS Server*).

### Preguntas de entrevista (senior)

#### 1. ¿Qué hace `paths` en `tsconfig.json` y por qué a veces compila pero falla al ejecutar?

**Respuesta:**

`paths` le dice al comprobador de tipos dónde buscar un import que no es
relativo ni un paquete. No transforma el código: el JavaScript emitido sigue
diciendo `from '@shared/...'`. Si quien ejecuta ese código no conoce los alias
(Node a secas, por ejemplo), falla con «módulo no encontrado» aunque `tsc`
haya pasado. Funciona cuando el empaquetador los resuelve (esbuild, webpack,
Vite, el CLI de Angular) o cuando se añade un paso que reescribe las rutas.
Por eso en este sitio los alias viven en lo que Angular compila y el script
de Node usa rutas relativas.

#### 2. ¿Qué riesgo tiene un alias con varias carpetas de respaldo, como `@interfaces/*`?

**Respuesta:**

Que la resolución depende del orden y de qué archivos existan: si aparece un
`profile.interface.ts` en las dos carpetas, el import resuelve al primero sin
avisar, y un cambio en el otro no se ve. Es cómodo mientras los nombres sean
únicos; la alternativa segura es un alias por carpeta (`@home/interfaces/...`
y `@shared/interfaces/...`), que es más largo pero no tiene ambigüedad.
Conviene revisarlo si las interfaces crecen.

#### 3. ¿Cómo evitas que vuelvan a aparecer imports relativos profundos con el tiempo?

**Respuesta:**

Con una regla de ESLint, `no-restricted-imports` con un patrón como
`../*` (o `../../*` si se tolera un nivel), que marca el import en el editor
y falla en el `lint` del CI. El alias por sí solo es una convención; la regla
la hace exigible. En este sitio el `lint` se ejecuta en la integración
continua, así que la regla también se aplica al código nuevo.

<!-- /study-guide:section:styles-e5-path-aliases -->

---

<!-- study-guide:section:styles-e6-page-shell -->
## Módulo E6: El esqueleto de página: encabezado, navegación y columna de contenido

Fuente: `src/app/app.html`, `src/app/shared/components/header/`,
`src/app/shared/constants/sections.constants.ts`,
`src/app/shared/interfaces/shared.interface.ts` y
`src/app/shared/utils/current-locale.utils.ts` del repositorio.

### El problema que resuelve

Portify organiza la página en tres piezas fijas: un encabezado con el logo y
el botón de menú, una navegación vertical numerada que en escritorio queda
fija a la derecha y en móvil entra desde la izquierda sobre un fondo oscuro, y
un `<main class="container-fluid">` cuya columna `col-xl-9` deja sitio a la
navegación. Todo el comportamiento del menú lo hace `app.js` a mano:
`classList.toggle('open')` en el icono, `classList.toggle('opened')` en el
`<nav>`, y el enlace activo lo marca el ScrollSpy de Bootstrap. En Angular hay
que decidir dónde vive ese estado, cómo se escriben los enlaces en dos
idiomas sin repetir plantilla y cómo se llega a una sección desde la página
de un proyecto, no sólo desde la portada.

### La decisión en este sitio

- `App` es dueña del `<main>`: el esqueleto se escribe una vez en `app.html`
  y las páginas (`home-page`, `project-page`, `not-found-page`) ya no llevan
  `<main>` propio. Un documento con dos `<main>` anidados es HTML inválido.
- Un solo componente, `shared-header`, renderiza la barra, el `<nav>` y el
  overlay, porque los tres comparten un estado: `menuOpen`, una señal.
- Las secciones de la portada viven en una constante `SECTIONS` con `id` y
  etiqueta por idioma. Hoy son ocho: las seis de Portify más la Galería y la
  guía DIY, que llegan en las Partes 5 y 7, arriba de Contacto (el snippet de abajo ya las incluye). El `id` es a la vez el atributo del `<section>` y el fragmento
  del enlace. El número (`01` a `08`) lo escribe el `SerialPipe` en la
  plantilla desde la posición en el `@for` (Parte 3, Módulo S6).
- Cada enlace es un `routerLink` a `/${locale}` con `fragment`, no un
  `href="#about"`: así funciona desde `/en/projects/angular-guide`, que
  navega a `/en#about`.
- El idioma sale de la URL con dos funciones compartidas con el selector de
  idioma: `injectCurrentUrl` y `localeFromUrl`.
- El selector de idioma va al pie del panel de navegación, donde Portify
  muestra el correo y el teléfono; este sitio no publica correo. Al principio
  estuvo en la barra del encabezado y se movió al panel para cambiar de idioma
  sin volver arriba de la página; el contenedor cierra el menú móvil al elegir
  uno.
- Accesibilidad desde el primer día: el botón declara `aria-controls`,
  `aria-expanded` y `aria-label`; el `<nav>` tiene `aria-label`; el menú se
  cierra con Escape, con el overlay y al elegir un enlace.
- En esta adaptación, Angular construye los enlaces; Bootstrap aporta los
  estilos del menú. El enlace activo según el scroll no forma parte del ejemplo.

### El código

`src/app/app.html`:


> **Después:** el `app.html` actual añade `<shared-background />` como primera
> línea, el campo de puntos de fondo que se construye en la Parte 4
> ([Módulo A3](04-animaciones.md#módulo-a3-el-campo-de-puntos-en-un-canvas)). El
> resto es igual.

`src/app/shared/constants/locales.constants.ts` e
`src/app/shared/interfaces/shared.interface.ts`:

```ts
export const LOCALES = ['en', 'es'] as const
```

```ts
import { LOCALES } from '@shared/constants/locales.constants'

export type Locale = (typeof LOCALES)[number]
export interface Section {
  id: string
  label: Record<Locale, string>
}
```

`src/app/shared/constants/sections.constants.ts`:

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
  { id: 'diy', label: { en: 'DIY guide', es: 'Guía DIY' } },
  { id: 'contact', label: { en: 'Contact', es: 'Contacto' } },
]
```

`src/app/shared/utils/current-locale.utils.ts`:

```ts
import { inject, Signal } from '@angular/core'
import { toSignal } from '@angular/core/rxjs-interop'
import { NavigationEnd, Router } from '@angular/router'
import { filter, map } from 'rxjs'
import { Locale } from '@shared/interfaces/shared.interface'
import { LOCALES } from '@shared/constants/locales.constants'

// The URL is the source of truth for the language: /en/... or /es/...
export function injectCurrentUrl(): Signal<string> {
  const router = inject(Router)
  return toSignal(
    router.events.pipe(
      filter((event) => event instanceof NavigationEnd),
      map((event) => event.urlAfterRedirects),
    ),
    { initialValue: router.url },
  )
}

export function localeFromUrl(url: string): Locale | null {
  return LOCALES.find((locale) => new RegExp(`^/${locale}(?=[/?#]|$)`).test(url)) ?? null
}
```

`src/app/shared/components/header/header.component.ts` (así quedó en este
módulo; la nota de después está al final de la plantilla):

```ts
import { Component, computed, signal } from '@angular/core'
import { LanguageSwitcherComponent } from '@shared/components/language-switcher/language-switcher.component'
import { SECTIONS } from '@shared/constants/sections.constants'
import { injectCurrentUrl, localeFromUrl } from '@shared/utils/current-locale.utils'
import { SerialPipe } from '@shared/pipes/serial.pipe'
import { RouterLink } from '@angular/router'

@Component({
  selector: 'shared-header',
  imports: [LanguageSwitcherComponent, RouterLink, SerialPipe],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
  // host is a way to bind host element events to component methods
  // In this case, pressing the Escape key will trigger the closeMenu() method
  host: { '(document:keydown.escape)': 'closeMenu()' },
})
export class HeaderComponent {
  private readonly url = injectCurrentUrl()
  protected readonly locale = computed(() => localeFromUrl(this.url()) ?? 'en')
  protected readonly menuOpen = signal(false)

  protected readonly links = computed(() =>
    SECTIONS.map((section) => ({
      id: section.id,
      label: section.label[this.locale()],
    })),
  )

  protected readonly labels = computed(() =>
    this.locale() === 'es'
      ? { home: 'Ir al inicio', menu: 'Menú', sections: 'Secciones' }
      : { home: 'Go to the homepage', menu: 'Menu', sections: 'Sections' },
  )

  protected toggleMenu() {
    this.menuOpen.update((open) => !open)
  }

  protected closeMenu() {
    this.menuOpen.set(false)
  }
}
```

`src/app/shared/components/header/header.component.html`:


> **Después:** el interruptor de animaciones de la Parte 4
> ([Módulo A4](04-animaciones.md#módulo-a4-el-interruptor-de-animaciones)) toca
> estos dos archivos. En `header.component.ts` se importa
> `MotionToggleComponent` (desde `@shared/components/motion-toggle/motion-toggle.component`)
> y se añade a `imports`, que queda
> `[LanguageSwitcherComponent, MotionToggleComponent, RouterLink, SerialPipe]`.
> En `header.component.html` se pone `<shared-motion-toggle />` justo antes del
> `<button>` del menú, dentro del `div` de la barra. Nada más cambia.

> **Después (encabezado fijo en móvil):** el [Módulo E7](#módulo-e7-los-estilos-del-menú-de-portify-traducidos-a-un-componente) explica por qué por
> debajo de `xl` el encabezado se queda arriba al hacer scroll. Esto cambia
> también estos dos archivos. En `header.component.html` la barra lleva la
> referencia `#bar` y los huecos pasan de `gap-4` a `gap-3 gap-sm-4`:
>
> ```html
> <header #bar class="header">
>   <div
>     class="container-fluid d-flex flex-wrap align-items-center justify-content-between gap-3 gap-sm-4"
>   >
>     <div class="d-flex align-items-center gap-3 gap-sm-4 ms-auto">
> ```
>
> En `header.component.ts` el componente mide la barra y publica su altura real
> como `--header-height` (el código del constructor, y los imports nuevos de
> `@angular/core`: `afterNextRender`, `DestroyRef`, `DOCUMENT`, `ElementRef`,
> `inject` y `viewChild`):
>
> ```ts
>   private readonly bar = viewChild.required<ElementRef<HTMLElement>>('bar')
>
>   constructor() {
>     const root = inject(DOCUMENT).documentElement
>     const destroyRef = inject(DestroyRef)
>
>     // Below `xl` the bar is sticky and the anchors stop under it (`scroll-padding-top`, see
>     // `_base.scss`). Its height is not a constant: the bar wraps onto a second row on a very
>     // narrow screen or with larger text, so the real height is published as `--header-height`.
>     afterNextRender(() => {
>       if (typeof ResizeObserver === 'undefined') return
>       const bar = this.bar().nativeElement
>       const observer = new ResizeObserver(() =>
>         root.style.setProperty('--header-height', `${bar.getBoundingClientRect().height}px`),
>       )
>       observer.observe(bar)
>       destroyRef.onDestroy(() => {
>         observer.disconnect()
>         root.style.removeProperty('--header-height')
>       })
>     })
>   }
> ```

Y cada componente de sección lleva su `id`, por ejemplo en
`hero.component.html`:


### Cómo funciona por dentro

- **Una señal en lugar de `classList.toggle`.** `menuOpen` es la única
  fuente de verdad; la plantilla la refleja en tres sitios (`[class.open]`
  en el icono, `[class.opened]` en el `<nav>`, `[attr.aria-expanded]` en el
  botón) y el CSS hace el resto, incluido el overlay, que se muestra con el
  selector `.navigation.opened + .nav-overlay` (Módulo E7). No hay código que
  busque elementos en el DOM.
- **`host: { '(document:keydown.escape)': 'closeMenu()' }`** declara un
  oyente sobre `document` en los metadatos del componente; es la forma
  actual de Angular, que sustituye al decorador `@HostListener`. Angular lo
  registra al crear el componente y lo quita al destruirlo.
- **`computed` recalcula cuando cambia el idioma.** `injectCurrentUrl`
  convierte los eventos del router en una señal con la URL tras cada
  navegación (`NavigationEnd`, con `urlAfterRedirects` para que `/` ya se lea
  como `/en`); `localeFromUrl` saca el idioma del primer segmento. `links` y
  `labels` dependen de `locale`, así que al pulsar «Español» se reescriben
  solos. El `initialValue: router.url` hace que la señal tenga valor desde el
  primer render, también durante el prerenderizado.
- **`[fragment]` y el scroll.** Un `routerLink` con `fragment="about"`
  navega a `/en#about`. En esta etapa `app.config.ts` activaba
  `withInMemoryScrolling({ anchorScrolling: 'enabled' })`, con lo que Angular
  buscaba el elemento con ese `id` y hacía scroll hasta él; desde el Módulo
  S3 de la Parte 3 ese scroll lo hace un inicializador propio, para poder
  omitirlo al cambiar de idioma. Desde la portada sólo cambia el fragmento;
  desde una página de proyecto vuelve a la portada y después hace el scroll.
- **`d-xl-none`** es un utilitario de Bootstrap (Módulo E1): oculta el botón,
  el isotipo y el overlay a partir de 1200 px, donde la navegación es fija y
  siempre visible. Una sola plantilla sirve para los dos tamaños.
- **`flex-wrap` y `ms-auto` en la barra.** Cuando el selector de idioma
  estaba en la barra, a 320 px el logo, los dos idiomas y el botón no cabían
  en una fila; sin `flex-wrap` el botón quedaba fuera de
  la pantalla y, con `overflow-x: hidden` en el `body`, no se podía alcanzar.
  Con `flex-wrap` los controles bajan a una segunda fila y `ms-auto` los
  mantiene pegados a la derecha.
- **`aria-expanded` como atributo, no como propiedad.** `[attr.aria-expanded]`
  escribe `"true"` o `"false"` en el HTML, que es lo que leen los lectores de
  pantalla; `[aria-expanded]` sin `attr.` intentaría asignar una propiedad
  que el elemento no tiene.
- **El espacio entre `01` y `HOME` no existe.** Angular elimina por defecto
  los nodos de texto que son sólo espacios entre elementos
  (`preserveWhitespaces: false`), así que el espacio escrito entre los dos
  `<span>` desaparece y se leía «01HOME». La separación se da con un margen
  en CSS (Módulo E7).
- **`alt="Janio Isacura"` en el logo y `alt=""` en el isotipo.** El primero
  es el enlace a la portada y necesita nombre; el segundo es decorativo
  dentro de un menú que ya tiene etiqueta.

### Errores comunes

- **Dos `<main>`.** Las páginas venían con `<main>` de la etapa anterior;
  dejarlas así al añadir el de `App` produce `<main>` dentro de `<main>`.
  Las pruebas no lo detectan; sólo se ve en el HTML.
- **Enlaces sin destino.** Si se escribe el menú antes de poner los `id` en
  las secciones, los enlaces navegan a `/en#home` y no pasa nada, sin error
  en consola. Es fácil creer que falla el scroll del router.
- **`[routerLink]="[]"` con fragmento.** Significa «la ruta actual»; desde la
  página de un proyecto daría `/en/projects/angular-guide#about`, que no
  tiene esa sección. Por eso el enlace lleva `['/', locale()]` explícito.
- **Confiar en los `data-bs-*` de Portify.** `data-bs-spy` o
  `data-bs-toggle` no hacen nada sin el JavaScript de Bootstrap, que aquí no
  se incluye.
- **Volver a pulsar el enlace de la sección en la que ya estás.** El router
  ignora una navegación a la misma URL (`onSameUrlNavigation: 'ignore'` por
  defecto), así que si la persona hizo scroll y pulsa el mismo enlace, no
  vuelve a subir.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué guardar el estado del menú en una señal y no alternar clases en el DOM como hace la plantilla?

**Respuesta:**

Porque con una señal el estado existe en un solo sitio y la vista es una
función de él: si el menú está abierto, el icono, el panel, el overlay y
`aria-expanded` lo reflejan sin que nadie tenga que acordarse de actualizar
cuatro cosas. Alternar clases a mano funciona hasta que un segundo camino
cambia el estado (Escape, el overlay, un enlace) y uno de los cuatro se
queda desincronizado. Además la señal es comprobable en una prueba sin
mirar el DOM, y Angular sólo vuelve a pintar lo que depende de ella.

#### 2. ¿Cómo haces que un enlace a una sección funcione desde cualquier página de la aplicación, y qué falta para que sea perfecto?

**Respuesta:**

Navegando a la ruta de la portada con un fragmento (`['/', locale]` más
`fragment`), no con `href="#id"`, y activando `anchorScrolling` en el router
para que, al terminar la navegación, Angular haga scroll al elemento con ese
`id`. Faltan dos cosas: el router ignora una navegación a la misma URL, así
que repetir el enlace no vuelve a subir (se cambia con `onSameUrlNavigation:
'reload'` o haciendo el scroll a mano), y el enlace activo según la posición
del scroll, que en la plantilla hacía el ScrollSpy de Bootstrap y aquí se
hará con `IntersectionObserver`.

#### 3. ¿Qué hace accesible a este menú móvil y qué le falta todavía?

**Respuesta:**

Es un `<button>` real (teclado y lector de pantalla lo entienden sin más),
con `aria-label` porque no tiene texto, `aria-controls` apuntando al `<nav>`
y `aria-expanded` que cambia con el estado; el `<nav>` tiene su `aria-label`;
Escape, el overlay y los propios enlaces lo cierran. Le falta gestionar el
foco: al abrir, llevar el foco al primer enlace y, al cerrar, devolverlo al
botón; y mientras está abierto, impedir que el tabulador salga del panel.

<!-- /study-guide:section:styles-e6-page-shell -->

---

<!-- study-guide:section:styles-e7-shell-styles -->
## Módulo E7: Los estilos del menú de Portify traducidos a un componente

Fuente: `src/app/shared/components/header/header.component.scss`,
`src/app/shared/components/language-switcher/language-switcher.component.scss`
y `src/app/shared/components/footer/footer.component.scss` del repositorio.

### El problema que resuelve

Los bloques `.header`, `.navigation` y `.nav-overlay` de Portify ocupan unas
250 líneas de la hoja global, con reglas para escritura de derecha a
izquierda (`:dir(rtl)`), prefijos de navegador de hace diez años y una
consulta `@media (max-width: 1200px)` que se solapa con el *breakpoint* `xl`
de Bootstrap (que empieza justo en 1200 px). En Angular esos estilos
pertenecen al componente que pinta el menú, encapsulados, y con el
presupuesto `anyComponentStyle` de 4 kB vigilando.

### La decisión en este sitio

- Los estilos van en `header.component.scss`, que importa `tools` (Módulo
  E2) para el mixin `min-width` y el de Bootstrap `media-breakpoint-down`.
- Se eliminan las reglas RTL, los prefijos y el bloque `.contact` (correo y
  teléfono) que no existe en este sitio.
- `media-breakpoint-down(xl)` sustituye a `max-width: 1200px`: compila a
  `max-width: 1199.98px` y no se solapa con `min-width(xl)`.
- La línea vertical sigue siendo una variable `--height`, fijada al 100 %
  hasta que GSAP la anime, pero en móvil se acorta 100 px: tal como estaba
  desbordaba el panel y aparecía una barra de scroll.
- El hueco entre el número y la etiqueta se da con `margin-left`, porque el
  espacio de la plantilla no llega al DOM (Módulo E6).
- El selector de idioma y el pie tienen hojas propias y pequeñas.
- **El encabezado se queda arriba en móvil.** Se añadió tras probar el sitio en un
  teléfono: para cambiar de sección o de idioma había que volver al principio de
  la página. Por debajo de `xl` el elemento fijo (`position: sticky`) es el
  anfitrión del componente (`:host`), y el desenfoque del fondo
  (`backdrop-filter`) va en la barra. El menú lateral y su capa son
  `position: fixed`; si el anfitrión tuviera `transform`, `filter` o
  `backdrop-filter`, esas dos piezas dejarían de medirse contra la ventana y se
  medirían contra él.
- **El menú lateral es `fixed` abierto y cerrado.** Cerrado era `absolute`; con un
  anfitrión fijo su caja de referencia pasaba a ser los 69 px del anfitrión y el
  panel se encogía mientras se deslizaba hacia fuera.
- **La barra cabe en una fila en cualquier teléfono, y su altura se mide.** Se
  probó a 320 y 360 px y la barra se partía en dos filas (120,7 px): el logo, la
  etiqueta del interruptor de animaciones, el botón del menú y los huecos no
  cabían. Ahora los huecos son de 16 px por debajo de `sm` (`gap-3 gap-sm-4`) y la
  etiqueta se oculta por debajo de 370 px (el [Módulo A4 de la Parte 4](04-animaciones.md#módulo-a4-el-interruptor-de-animaciones), que explica el interruptor). Aun así, la
  altura no se da por supuesta: el componente la publica como `--header-height`
  con un `ResizeObserver`, y `html` la usa como `scroll-padding-top`
  (`$header-height`, 69 px, sólo vale hasta que el encabezado se pinta).

### El código

`src/app/shared/components/header/header.component.scss`:


`language-switcher.component.scss` y `footer.component.scss`:



> **Después:** esta es la banda del pie tal como quedó en este módulo. El
> archivo actual, `footer.component.scss`, usa la clase `.footer` en lugar del
> selector `footer`, le añade `position: relative` (para quedar por encima del
> lienzo de fondo fijo de la Parte 4) y `font-size: 14px`, y anida las reglas
> de `p`, `.stack` y `.top-link` que construye la Parte 3, Módulo S9. El
> `padding: 32px 0` y el fondo `rgba(var(--black), 0.06)` siguen igual.

### Cómo funciona por dentro

- **Cerrado y abierto en móvil.** Cerrado, el panel está fuera de la
  pantalla por la izquierda (`translateX(-100%)`); con `.opened` pasa a
  `position: fixed`, vuelve a `translateX(0)` y recibe el fondo amarillo. La
  transición es sobre `transform`, que el navegador anima en el compositor
  sin recalcular el diseño de la página; animar `left` obligaría a
  recalcularlo en cada fotograma.
- **El overlay depende del hermano.** `.navigation.opened + .nav-overlay`
  usa el combinador de hermano adyacente: el overlay se muestra sólo si el
  elemento inmediatamente anterior es el `<nav>` abierto. Por eso en la
  plantilla el `<div class="nav-overlay">` va justo después del `</nav>`.
- **Escritorio.** A partir de `xl` el panel es fijo a 100 px del borde
  superior y pegado a la derecha, con la lista de 300 px, y limitado a
  `calc(100vh - 100px)` con `overflow-y: auto`: en una ventana baja (1280 ×
  360 px) los últimos enlaces quedaban fuera de la pantalla y, al ser un panel
  fijo sin botón, no había forma de llegar a ellos. Desde 1750 px se
  calcula su `left` para alinearlo con el contenedor de 1740 px que fija
  `_base.scss` (Módulo E4): los dos números van juntos.
- **La línea vertical es una variable CSS** para que GSAP pueda animarla
  (`gsap.to(nav, { '--height': '100%' })`) sin tocar el CSS. En móvil empieza
  100 px más abajo y mide `calc(var(--height) - 100px)`; con `height:
  var(--height)` sobresalía 100 px por debajo del panel y, como el panel
  tiene `overflow-y: auto` para pantallas bajas, aparecía la barra de scroll.
- **El relleno del enlace** es el pseudoelemento `::after`: una franja negra
  al 15 % que crece de 0 al 100 % de ancho con la animación `grow` al pasar
  el ratón o con la clase `.active`, que queda reservada para el enlace
  activo del scroll.
- **El icono hamburguesa** son tres `<span>` absolutos a 0, 12 y 24 px. Con
  `.open`, el primero y el tercero se juntan a 12 px y giran 135° y -135°
  formando la X; el segundo se desvanece hacia la izquierda.
- **Escalera de `z-index`:** encabezado 10, overlay 12, panel 100. El overlay
  tapa la página y el encabezado; el panel queda encima del overlay.
- **El bloque `.language`** al pie del panel aloja el selector de idioma con
  el mismo sangrado de 34 px que los enlaces. El `(click)` del contenedor
  cierra el panel porque el evento burbujea desde el enlace de idioma; el
  selector no necesita saber que vive dentro de un menú.
- **Encapsulación.** Angular añade un atributo a cada elemento de la
  plantilla y a cada selector del componente (`.navigation[_ngcontent-xxx]`),
  así que estas reglas no alcanzan a ningún otro `.navigation` ni los estilos
  globales rompen las suyas; `@keyframes grow` también queda dentro del
  componente. Las clases de Bootstrap (`d-xl-none`, `container-fluid`) son
  globales y se aplican igual. El CSS compilado del componente queda por
  debajo del aviso de 4 kB; si crece, el presupuesto se ajusta a conciencia.

- **`position: sticky` y sus ancestros.** Un elemento `sticky` se pega a la
  ventana mientras ningún ancestro entre él y la ventana tenga un `overflow`
  distinto de `visible`. Aquí el `overflow-x: hidden` del `body` se propaga a la
  ventana (no crea un contenedor propio) y el `overflow-x: clip` está en `main`,
  que es un hermano del encabezado, no un ancestro.
- **El contexto de apilamiento del anfitrión.** Con `z-index: 10`, el
  anfitrión forma un contexto: dentro, la barra (10), la capa oscura (12) y el
  panel (100) conservan su orden de siempre; fuera, nada se interpone entre 10
  y 100. El visor de la galería (100, en la raíz) queda por encima de todo.
- **`scroll-padding-top` frente a `scrollToAnchor`.** La propiedad CSS hace que
  los saltos nativos a un `#fragmento` y el foco de un elemento se detengan
  debajo de la barra. Pero `ViewportScroller.scrollToAnchor` de Angular no la
  usa: desplaza la ventana a la posición del elemento menos su propio
  `offset`. Por eso el inicializador de scroll registra ese `offset` leyendo la
  misma propiedad (el [Módulo S3 de la Parte 3](03-secciones-de-portify.md#después-las-secciones-paran-bajo-el-encabezado-fijo), que explica el scroll por fragmento).
- **`--header-height`.** `ResizeObserver` avisa cuando la barra cambia de
  tamaño (se parte en dos filas con un texto del sistema más grande, por
  ejemplo) y el componente escribe la altura real en `<html>`. `scroll-padding-top`
  la lee con `var(--header-height, 69px)`, así que los enlaces siguen cayendo
  justo bajo la barra aunque cambie.

### Errores comunes

- **`@media (max-width: 1200px)` junto a `min-width: 1200px`.** A 1200 px
  exactos se cumplen las dos y el panel recibe reglas de móvil y de
  escritorio a la vez. `media-breakpoint-down(xl)` resta 0,02 px y lo evita.
- **La línea que desborda.** `top: 100px` y `height: 100%` suman más que el
  panel. Con `overflow-y: auto`, el síntoma es una barra de scroll en el
  menú abierto aunque sobre espacio.
- **Mover el overlay de sitio** en la plantilla: el selector `+` deja de
  coincidir y el overlay nunca aparece, sin error.
- **`font-weight: 500` en los enlaces**, como en Portify. Con
  `font-synthesis: none` y sólo el peso 300 de Mozilla Text cargado, no
  cambia nada; se quitó para no dejar una regla que no hace lo que dice.
- **Olvidar `@import 'tools'`** al principio: Sass falla con «Undefined
  mixin» en la primera `@include`.
- **Poner el desenfoque en el anfitrión `sticky`.** El panel y la capa de
  `position: fixed` pasan a medirse contra el anfitrión (69 px de alto) y no
  contra la ventana: el menú se abre mal o no se ve. Una prueba de contenido
  falla si el anfitrión recibe `transform`, `filter` o `backdrop-filter`.
- **Dar la altura de la barra por supuesta.** Con 69 px en una constante, a 320 y
  360 px los enlaces dejaban 52 px de la sección bajo la barra. Se encontró
  midiendo, y no con las pruebas: ninguna mide la altura en un navegador.
- **Dejar el panel cerrado como `absolute`.** Su caja de referencia pasa a ser el
  anfitrión y el panel se encoge al cerrarse.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué animar `transform` y no `left` para deslizar un panel?

**Respuesta:**

Porque `transform` (y `opacity`) se animan en el compositor: el navegador ya
tiene el panel pintado en una capa y sólo lo desplaza, sin recalcular diseño
ni volver a pintar el resto de la página en cada fotograma. `left` cambia la
geometría, obliga a recalcular el diseño y repintar, y en móvil se nota como
tirones. La regla del interruptor de animaciones de `_base.scss` quita igualmente
la transición para quien apaga el movimiento (Parte 4, Módulo A4).

#### 2. ¿Cómo afecta la encapsulación de vistas de Angular a un selector como `.navigation.opened + .nav-overlay` y a una clase global como `d-xl-none`?

**Respuesta:**

Angular reescribe cada selector del componente añadiendo un atributo único
(`[_ngcontent-xxx]`) a cada parte, y pone ese atributo en los elementos de
la plantilla. `.navigation.opened + .nav-overlay` sigue funcionando porque
los dos elementos están en la misma plantilla y reciben el atributo. Una
clase global como `d-xl-none` viene de la hoja global, que no se reescribe,
así que se aplica a cualquier elemento que la lleve. La encapsulación
protege en las dos direcciones: los estilos del componente no se escapan, y
una regla global sólo entra si el componente usa esa clase a propósito.

#### 3. ¿Para qué sirve que la altura de la línea sea una variable CSS si hoy vale siempre 100 %?

**Respuesta:**

Para separar el «qué» del «cuánto»: el CSS describe que la línea mide
`var(--height)` y cómo se coloca; quien anime sólo tiene que cambiar un
número, desde JavaScript (GSAP) o desde otra regla, sin saber nada del
diseño. Es el mismo patrón de los tokens de color (Módulo E3). Si la
transición se hiciera en CSS puro, habría que declarar la propiedad con
`@property` para que el navegador sepa interpolarla; con GSAP no hace falta,
porque GSAP calcula cada valor intermedio y lo escribe.

#### 4. Un encabezado `position: sticky` con un menú lateral `position: fixed` dentro. ¿Dónde pones el desenfoque de fondo y por qué?

**Respuesta:**

En la barra, no en el elemento que es `sticky`. `transform`, `filter`,
`backdrop-filter`, `perspective` y `contain` crean un bloque contenedor para
los descendientes `position: fixed`: si el elemento con esos estilos es el
anfitrión, el panel y la capa oscura dejan de medirse contra la ventana y se
miden contra él, que sólo mide lo que la barra (69 px). El menú se ve
recortado o desplazado. Con el desenfoque en la barra, que no contiene al
panel, el panel sigue siendo relativo a la ventana. Es un fallo silencioso: no
hay error, sólo un menú que se comporta distinto, y por eso conviene una
prueba que vigile esa regla.

#### 5. Tienes un encabezado fijo y los enlaces a secciones dejan el título tapado. ¿Basta con `scroll-padding-top`?

**Respuesta:**

Con los saltos nativos a un `#fragmento` y con el foco, sí: el navegador se
detiene a esa distancia. Pero Angular, cuando hace el salto él mismo con
`ViewportScroller.scrollToAnchor`, no consulta esa propiedad: desplaza la
ventana a la posición del elemento menos un `offset` propio (por defecto, cero).
En este sitio, como el inicializador de scroll es quien salta, hay que
registrar un `offset` con `ViewportScroller.setOffset`. Para no repetir el
número, la función lee `scroll-padding-top` de `<html>` en el momento de
saltar: una sola fuente de verdad, cero donde el encabezado no es fijo, y
siempre al día si la altura cambia (`--header-height`).

<!-- /study-guide:section:styles-e7-shell-styles -->

---

## Qué sigue

Con los estilos y el esqueleto listos, sigue con [las secciones de Portify](03-secciones-de-portify.md).
El lienzo de puntos y las animaciones de entrada con GSAP se explican en
[Animaciones y fondo](04-animaciones.md).
