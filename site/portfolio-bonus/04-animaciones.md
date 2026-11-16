# Parte 4: Animaciones y fondo

> Esta versión pública conserva las explicaciones y omite fragmentos que reproducen o adaptan la plantilla comercial.

Esta parte reconstruye en Angular lo que Portify hace con GSAP y un `<canvas>`:
la coreografía de entrada y de scroll, el fondo de puntos que sigue al ratón y,
porque el movimiento continuo necesita una salida, un interruptor para apagarlo
todo. Cada módulo deja código real del repositorio y un error que costó
encontrar: la pestaña de entrada que se quedaba oculta, el scroll que no
disparaba nada en la carga inicial, el menú que seguía en el orden de
tabulación con las animaciones apagadas.

**Si llegaste aquí desde un buscador.** Esta página es una parte de la guía
«Cómo se construye este sitio», escrita sobre el repositorio de
janioisacura.com, un portfolio hecho con Angular y prerenderizado a HTML
estático. Lo que enseña (GSAP con ScrollTrigger dentro de Angular, un
inicializador de entorno en lugar de código en cada componente, un campo de
puntos en un canvas con pantallas de alta densidad y un interruptor de
movimiento que gobierna JavaScript y CSS a la vez) sirve para cualquier sitio
Angular con animaciones.

**Proyecto:** `src/app/shared/animations/`, `src/app/shared/services/`,
`src/app/shared/components/background/`,
`src/app/shared/components/motion-toggle/` y `src/styles/_base.scss`.
**Sitio publicado:** [janioisacura.com](https://janioisacura.com/en/).
**Alcance:** animaciones, fondo de puntos e interruptor de movimiento.

**Qué vas a aprender:**

- [Módulo A1](#módulo-a1-la-coreografía-central-y-su-inicializador): **La
  coreografía central.** Todas las animaciones de Portify en un solo archivo
  que busca sus elementos por clase, un inicializador que las ejecuta una vez
  por ruta y las revierte al cambiar de página, y por qué el router no sirve
  para la carga inicial.
- [Módulo A2](#módulo-a2-reveals-que-no-se-quedan-ocultos): **Reveals que no
  se quedan ocultos.** Por qué un `from()` con retraso dejaba el retrato y el
  menú en opacidad 0, la sintaxis de `start` de ScrollTrigger, el foco en
  elementos todavía invisibles y cómo distinguir un fallo de GSAP de una
  ventana que no pinta.
- [Módulo A3](#módulo-a3-el-campo-de-puntos-en-un-canvas): **El campo de
  puntos.** La cuadrícula de `dots-bg` en una clase, con vecinos por celdas,
  pantallas de alta densidad y un puntero que distingue ratón de dedo.
- [Módulo A4](#módulo-a4-el-interruptor-de-animaciones): **El interruptor.** Un
  servicio, un atributo en `<html>` y una regla de CSS para apagar GSAP, el
  lienzo y las transiciones juntos, y la decisión de no consultar la
  preferencia del sistema.

Cada módulo sigue el mismo orden: el problema que resuelve, la decisión tomada
en este sitio, el procedimiento o el código completo, cómo funciona por
dentro, errores comunes y preguntas de entrevista con su respuesta.

Esta página es una parte de la guía [Cómo se construye este sitio](como-se-construye.md).
Conviene haber leído antes la [Parte 3](03-secciones-de-portify.md), de donde salen
las secciones que se animan, el scroll por fragmento (Módulo S3) y el
`KEEP_SCROLL` del selector de idioma. La anatomía de las animaciones originales
está en [Estilos y animaciones](estilos-y-animaciones.md#animaciones-con-gsap).

---

<!-- study-guide:section:animations-a1-choreography -->
## Módulo A1: La coreografía central y su inicializador

Fuente: `src/app/shared/animations/choreography.ts`,
`src/app/shared/animations/animations.utils.ts` y `src/app/app.config.ts` del
repositorio.

### El problema que resuelve

Portify anima con unas cien líneas de `app.js`: cada `gsap.from(...)` busca sus
elementos por selector en la página entera y se ejecuta una vez, al cargar. En
Angular la tentación es repartirlas: una directiva o un `afterNextRender` en
cada componente, con su `ElementRef`, su `DestroyRef` y su `gsap.context`. Son
diez archivos que conocen una librería de animación, y una secuencia que en
Portify es una sola (el menú entra a los 0,5 s, el retrato a los 0,3 s, las
líneas crecen desde 0) queda dispersa y sin dueño.

Además hay tres detalles de plataforma:

1. El router de Angular **no emite el evento `Scroll` en la navegación
   inicial**, sólo en las siguientes. El inicializador del scroll por fragmento
   (Parte 3, Módulo S3) funciona con él, pero una coreografía que dependiera
   de ese evento no arrancaría al abrir la página.
2. Cambiar de fragmento (`/en#about`) o de idioma no debe repetir la
   entrada: la página es la misma.
3. GSAP toca `window` y el DOM: no puede correr al prerenderizar ni en las
   pruebas de jsdom.

### La decisión en este sitio

- **Una función, `choreography()`**, con todos los tweens, que encuentra sus
  elementos por las clases que los componentes ya pintan. Los componentes no
  saben que existe GSAP. Un elemento que no está en la página actual (el hero
  en la página de un proyecto) simplemente se salta.
- **Un inicializador de entorno, `provideScrollAnimations()`**, registrado en
  `app.config.ts` junto al del scroll por fragmento. Sólo en el navegador.
- **El momento**: tras `NavigationEnd` y el siguiente render
  (`afterNextRender`), no tras `Scroll`. Una vez por **ruta** (la URL sin
  fragmento ni consulta): navegar a otra página revierte la ejecución anterior
  antes de empezar la nueva.
- **`gsap.context`** envuelve la ejecución: revertirlo devuelve todos los
  elementos a su estado de CSS y mata los ScrollTrigger.
- No anima cuando la navegación lleva `KEEP_SCROLL` (el cambio de idioma) ni
  en jsdom (sin `matchMedia`).
- El interruptor de animaciones (Módulo A4) apaga y enciende esta misma
  ejecución desde el mismo inicializador.

### El código

`src/app/shared/animations/animations.utils.ts`:


`src/app/shared/animations/choreography.ts`:


El bloque de la galería (la tarjeta `.gallery-card`) llegó con la Parte 5 y repite
el mismo patrón de las tarjetas de Proyectos, con un solo elemento; se explica
en el [Módulo G5](05-galeria.md#módulo-g5-la-entrada-en-la-portada).

`src/app/app.config.ts`:


La última línea (`TitleStrategy`) no es de animaciones: la estrategia escribe las
etiquetas para compartir y para buscadores al fijar el título, y se explica en la
Parte 6, en el [Módulo V3 de la Parte 6](06-seo-y-vista-previa.md#módulo-v3-las-etiquetas-al-fijar-el-título).

### Cómo funciona por dentro

- **`provideEnvironmentInitializer`** corre una vez al crear el inyector de la
  aplicación y es el sitio de una suscripción que debe vivir lo que vive la
  app (el mismo patrón que el scroll por fragmento). Con
  `isPlatformBrowser` se evita en el servidor, donde ni existe `window`.
- **`NavigationEnd` más `afterNextRender`.** `NavigationEnd` dice que la ruta
  nueva está activada; `afterNextRender` espera a que Angular la haya pintado,
  y sólo entonces existen los elementos que la coreografía busca. Hace falta
  el `Injector` porque se llama fuera de un contexto de inyección.
- **El contador `request`** descarta un render ya programado si llega una
  petición más nueva (por ejemplo, apagar el interruptor justo después de
  navegar): sin él, dos ejecuciones podían solaparse.
- **`path`, sin fragmento ni consulta.** `urlAfterRedirects.split(/[?#]/)[0]`
  compara páginas, no URLs: `/en#about` después de `/en` no repite nada.
- **`gsap.context(choreography, body)`** ejecuta la función con `body` como
  ámbito: los selectores de texto (`'.hero .btn'`) se resuelven dentro de él y
  todo lo creado queda registrado en el contexto. Si la función **devuelve
  otra función**, GSAP la llama al revertir: así la coreografía limpia sus
  oyentes de foco (Módulo A2).
- **`gsap.config({ nullTargetWarn: false })`** silencia el aviso por
  selectores sin elementos, que aquí es lo normal (la portada y la página de
  un proyecto no comparten elementos).
- **Los ScrollTrigger** viven dentro de los tweens (`scrollTrigger: {...}`);
  GSAP los registra en el contexto y los destruye al revertir.
- **La traducción de Portify** es casi literal, con tres diferencias. No hay
  SplitType: parte el texto en letras reescribiendo el DOM, algo que choca con
  la hidratación, así que el bloque del hero entra entero. Las animaciones de
  secciones fuera del MVP (servicios, cifras, testimonios) no existen. Y todo
  son `fromTo` (Módulo A2).

### Errores comunes

- **Esperar el evento `Scroll` del router para la primera ejecución.** En la
  carga inicial no llega: la página se abría sin una sola animación. Se vio
  con un registro de eventos del router.
- **Ejecutar en cada `NavigationEnd`.** Pulsar un enlace del menú (misma ruta,
  otro fragmento) reiniciaba el menú, el hero y todas las líneas.
- **No revertir al cambiar de página.** Al volver a la portada, los tweens
  de la vez anterior seguían vivos sobre elementos nuevos.
- **Importar GSAP y llamarlo en un componente que también se prerenderiza.**
  Fallaba en el servidor.
- **Un `console.log` o un objeto en `window` olvidado tras depurar.** El
  diagnóstico de este módulo expuso `gsap` y el contexto en `window`; no
  llegó al repositorio.

### Preguntas de entrevista (senior)

#### 1. ¿Dónde pondrías el código de animación de una aplicación Angular y por qué no en cada componente?

**Respuesta:**

Depende de si las animaciones son locales o forman una secuencia. Una
animación que pertenece a un componente (un acordeón, un botón) va en el
propio componente o en una directiva. Pero una coreografía de página, donde
el orden y los retrasos de elementos de distintos componentes importan, es
una sola pieza: dispersarla en diez sitios oculta la secuencia y obliga a
cada componente a conocer la librería. Aquí vive en un archivo, se ejecuta
desde un inicializador y los componentes sólo pintan clases. El precio es un
acoplamiento por nombre de clase entre la coreografía y las plantillas; es el
mismo que tiene el `app.js` original, concentrado en un solo sitio.

#### 2. ¿Por qué `NavigationEnd` más `afterNextRender` y no `ngAfterViewInit` ni el evento `Scroll` del router?

**Respuesta:**

`ngAfterViewInit` pertenece a un componente y no sabe de rutas: no cubre una
navegación que reutiliza el componente. El evento `Scroll` del router llega
después de pintar, pero no se emite en la primera navegación. `NavigationEnd`
es la señal de «ruta activada» en todas las navegaciones, incluida la
inicial, y `afterNextRender` añade la garantía de que el DOM ya está pintado.
La combinación se ejecuta en el navegador, una vez por cambio de página, y se
puede cancelar con un contador si llega otra petición antes.

#### 3. ¿Qué aporta `gsap.context` frente a crear los tweens sueltos?

**Respuesta:**

Agrupa todo lo creado dentro de una función (tweens, ScrollTrigger,
temporizadores) bajo un objeto que se puede revertir de una vez: los
elementos vuelven a su estado original y los disparadores se destruyen. En
una aplicación de una página con rutas eso es imprescindible, porque la
portada se destruye y se vuelve a crear al navegar y los tweens de la vez
anterior seguirían apuntando a nodos que ya no existen o duplicarían el
efecto. Además limita los selectores de texto a un ámbito y, si la función
devuelve otra función, la ejecuta al revertir, lo que sirve para quitar
oyentes propios.

<!-- /study-guide:section:animations-a1-choreography -->

---

<!-- study-guide:section:animations-a2-reveals -->
## Módulo A2: Reveals que no se quedan ocultos

Fuente: `src/app/shared/animations/choreography.ts`,
`src/app/shared/animations/animations.utils.ts` y
`src/app/shared/animations/choreography.spec.ts` del repositorio.

### El problema que resuelve

La primera versión de la coreografía, traducida de Portify con `gsap.from`,
dejaba la página casi vacía: el retrato del hero y los enlaces del menú
aparecían un instante y se quedaban en **opacidad 0**; después, las
secciones nunca se mostraban. Los elementos sin retraso (el botón, el texto
del hero) sí funcionaban. Había además tres problemas vecinos:

1. Una fila de Habilidades que tenía que aparecer «antes» y un `start` mal
   escrito que la habría dejado sin animar.
2. Las tarjetas de Proyectos, ocultas hasta que su disparador se activa,
   aceptan el foco del teclado: una persona con Tab podía llegar a un enlace
   invisible.
3. Una ventana de Chrome en la que ningún tween avanzaba, lo que hizo dudar
   del código durante un buen rato.

### La decisión en este sitio

- **Todos los reveals son `fromTo` con los dos extremos explícitos**, y el
  extremo final es el que el CSS ya declara (`opacity: 1`, `scale: 1`).
- **`gsap.defaults({ lazy: false })`** en el inicializador.
- **`start` con la sintaxis de ScrollTrigger**: `'top 60%'` o
  `'top bottom+=100'`, nunca una mezcla inventada.
- **La entrada de las tarjetas termina en cuanto una recibe el foco**, y la
  coreografía devuelve la limpieza de ese oyente.
- **Antes de culpar a GSAP, medir `requestAnimationFrame`.**

### El código

El problema, con el `from` de Portify:


y su arreglo, que es el que está en el repositorio:


El reveal de Habilidades, con el `start` corregido:


Las tarjetas de Proyectos, con el foco (el resto del archivo está en el
Módulo A1):


La prueba que lo cubre, `choreography.spec.ts`:


### Cómo funciona por dentro

- **Qué hace un `from()` con retraso.** GSAP aplica de inmediato los valores
  de partida (`opacity: 0`) y, cuando el tween se inicializa, lee del
  elemento los valores **finales**. Si el tween tiene `delay` o un
  ScrollTrigger, se inicializa **después** de haber aplicado sus propios
  valores de partida, y lee «opacidad 0» como el destino. Resultado: anima de
  0 a 0. Se vio en las propiedades internas del tween del retrato (`opacity`
  con inicio 0 y cambio 0). Los tweens sin retraso se inicializan antes y no
  tienen el problema. Con `fromTo` no se lee nada del elemento.
- **Por qué los valores finales en CSS.** El HTML prerenderizado, sin
  JavaScript o con el interruptor apagado, muestra el estado final de todo.
  La coreografía sólo añade el camino desde un estado anterior, así que
  nada que falle puede dejar contenido oculto para siempre.
- **`lazy: false`.** GSAP «aplaza» la escritura de valores de algunos tweens
  hasta el siguiente frame. Un tween que empieza y termina dentro de un único
  frame largo (una carga lenta, una pestaña limitada) escribía primero sus
  valores de partida y terminaba sin ejecutarse hasta el final. Se reprodujo
  con un salto artificial de 1,2 s: sin `lazy: false` el elemento se quedaba
  en opacidad 0; con él, en 1.
- **La sintaxis de `start`.** Son dos posiciones separadas por un espacio: la
  primera del **elemento** (`top`, `center`, `bottom`) y la segunda de la
  **ventana** (`60%`, `bottom`, `bottom+=100`). `'top 60%'` significa «cuando
  el borde superior del elemento llegue al 60 % de la altura de la ventana»;
  `'top bottom+=100'`, «100 píxeles antes de que entre por abajo». Una cadena
  como `'top-bottom 95%'` no existe y el disparador no se crea. Un porcentaje
  mayor dispara antes.
- **El foco y lo invisible.** `opacity: 0` y `scale: 0` no quitan un enlace
  del orden de tabulación. Una tarjeta ya visible en la ventana (por debajo
  del 60 %) recibe el foco sin que haya scroll que active el disparador, y
  quedaba enfocada pero invisible. El oyente `focusin` (que sube desde el
  enlace) lleva el tween a su final con `progress(1)`, una sola vez
  (`{ once: true }`), y se quita al revertir.
- **Probar con GSAP en jsdom.** ScrollTrigger lee `matchMedia`, que jsdom no
  trae: la prueba lo sustituye por una función sin coincidencias. Sirve para
  comprobar el estado inicial de los reveals y el oyente de foco, no el
  movimiento.
- **La ventana que no pinta.** En una ventana de Chrome tapada por otra
  aplicación, `requestAnimationFrame` corre a una vez por segundo: se midió
  con 4 frames en 3 s, también en sitios sin GSAP. GSAP tiene un suavizado de
  retrasos: si un frame llega con más de 500 ms de retraso, avanza su reloj
  sólo 33 ms. Con un frame por segundo, los tweens avanzan 0,03 s cada
  segundo y parecen congelados. No era un fallo del código.

### Errores comunes

- **Traducir `gsap.from` de una plantilla sin pensar en el estado inicial.**
  Funciona en la demo porque todo arranca de golpe; falla en cuanto un `delay`
  o un disparador lo retrasa.
- **Escribir un `start` de memoria.** Si el disparador no se crea, no hay
  error: el elemento se queda como estaba (visible o invisible).
- **Ocultar con opacidad lo que se puede enfocar.** El mismo problema se da
  con cualquier menú o tarjeta con enlaces; la salida es completar el reveal
  al enfocar o no ocultar lo que tiene enlaces.
- **Diagnosticar animaciones en una ventana que no se pinta.** Antes de leer
  tweens, medir `requestAnimationFrame` (la comprobación de A3 en la consola
  sirve) ahorra horas.
- **Olvidar quitar el oyente al revertir.** Quedaba un `focusin` apuntando a
  una tarjeta ya destruida.

### Preguntas de entrevista (senior)

#### 1. Un `gsap.from` con `delay` deja un elemento invisible. ¿Qué pasó y cómo lo arreglas?

**Respuesta:**

`from` aplica de inmediato los valores de partida y lee del elemento los
finales cuando el tween se inicializa. Con `delay` o con ScrollTrigger la
inicialización ocurre después de que ya se aplicaron los valores de partida,
así que lee «opacidad 0» como destino y anima de 0 a 0. Se arregla con
`fromTo`, que declara los dos extremos y no consulta el DOM. Además
conviene que el estado final coincida con el CSS: así, sin JavaScript, el
contenido sigue visible.

#### 2. ¿Cómo se lee `start: 'top 60%'` en ScrollTrigger y por qué `'top-bottom 95%'` no funciona?

**Respuesta:**

Son dos posiciones: la primera es un punto del elemento disparador y la
segunda, un punto de la ventana. `'top 60%'` activa el efecto cuando el
borde superior del elemento alcanza el 60 % de la altura de la ventana. La
segunda posición admite porcentajes, palabras (`top`, `center`, `bottom`) y
desplazamientos en píxeles (`bottom+=100`). `'top-bottom'` no es ninguna de
ellas, así que el disparador no se crea y el tween no se enlaza al scroll,
sin error visible.

#### 3. Un contenido oculto con opacidad 0 contiene un enlace. ¿Qué problema de accesibilidad hay y cómo lo resuelves?

**Respuesta:**

La opacidad no saca el enlace del orden de tabulación ni del árbol de
accesibilidad: una persona con teclado puede enfocar algo que no ve, y un
lector de pantalla lo anuncia. Si el elemento ya está en pantalla, el foco
no produce scroll y el disparador no se activa. Hay tres salidas: completar
el reveal cuando el elemento recibe el foco (la elegida), no ocultar los
elementos con enlaces, o ocultarlos con `visibility: hidden` y mostrarlos al
disparar, lo que los quita del orden de tabulación mientras esperan.

<!-- /study-guide:section:animations-a2-reveals -->

---

<!-- study-guide:section:animations-a3-dots -->
## Módulo A3: El campo de puntos en un canvas

Fuente: `src/app/shared/animations/dots.ts`,
`src/app/shared/components/background/` y
`src/app/shared/animations/dots.spec.ts` del repositorio.

### El problema que resuelve

La variante `dots-bg` de Portify dibuja un campo de puntos: una cuadrícula
cada 45 px en la que cada punto deriva alrededor de su origen, se une con sus
cinco vecinos más cercanos y se ilumina según su distancia al ratón. El código
original son variables globales y funciones sueltas, y tiene cuatro problemas
para un sitio real:

1. Para cada punto ordena **todos los demás** por distancia: unos cuatrocientos
   puntos son más de cien mil comparaciones en cada cambio de tamaño.
2. Cada línea es un trazo independiente.
3. En pantallas de alta densidad (`devicePixelRatio` de 1,5 o 2) el canvas se
   ve borroso.
4. Decide si seguir al ratón con `'ontouchstart' in window`: un portátil con
   pantalla táctil deja de seguir al ratón.

### La decisión en este sitio

- **Una clase, `DotsField`**, sin estado global: recibe el canvas y la
  ventana, y expone `start()` y `stop()`, ambos idempotentes.
- **Vecinos por celdas**: en una cuadrícula regular, los cinco más cercanos
  están siempre a dos pasos; se buscan sólo ahí.
- **Un trazo por punto** (las cinco líneas en un mismo camino) y comparación
  por distancia al **cuadrado**, sin raíces.
- **Alta densidad**: el bitmap se escala por `devicePixelRatio`; el dibujo no.
- **`pointermove` y se ignora el toque** (`pointerType === 'touch'`).
- **Opacidad de los puntos al 20 %** (Portify usa 50 %), con la misma caída
  por distancia.
- **Un componente `shared-background`** con el canvas fijo, sin
  eventos de puntero, detrás del contenido; arranca con `afterNextRender` y
  sigue al interruptor de animaciones (Módulo A4).

### El código

`src/app/shared/animations/dots.ts`:


`src/app/shared/components/background/background.component.ts`:


`src/app/shared/components/background/background.component.scss`:


`App` lo coloca antes del encabezado (`<shared-background />` en `app.html`), y
`main` y el pie son `position: relative` para quedar por encima del canvas
(`z-index: 0`).

La prueba, `dots.spec.ts`:


### Cómo funciona por dentro

- **`gsap.ticker`.** Es el bucle de GSAP sobre `requestAnimationFrame`;
  `add` y `remove` registran y quitan la función de dibujo. Con el mismo reloj
  que los tweens, el dibujo y la deriva de los puntos no se desincronizan.
- **La deriva es una cadena de tweens.** `shift` mueve cada punto hasta media
  celda de su origen y, al terminar (`onComplete`), se llama a sí misma: nunca
  acaba. Al cambiar de tamaño hay que matar esos tweens
  (`gsap.killTweensOf`) antes de crear otros, o se acumulan.
- **Alta densidad.** `canvas.width = ancho * ratio` crea más píxeles;
  `setTransform(ratio, 0, 0, ratio, 0, 0)` hace que el dibujo siga en píxeles
  CSS. El tamaño visible lo fija el CSS (`width: 100%`, `height: 100%`).
- **Distancia al cuadrado.** `(dx² + dy²)` se compara con umbrales ya
  elevados al cuadrado (4000, 20000, 40000): no hace falta `Math.sqrt`.
- **Tres tramos de opacidad.** Cerca del ratón los puntos y las líneas están
  más marcados; lejos, casi invisibles. Las líneas sólo se trazan si su
  opacidad es mayor que cero.
- **`pointermove`.** Un ratón, un lápiz y un dedo generan eventos de
  puntero; el `pointerType` los distingue. En un teléfono el campo queda
  «despierto» en el centro de la ventana; en un portátil con pantalla
  táctil sigue al ratón.
- **`start()` sin contexto 2D.** `canvas.getContext('2d')` es `null` en jsdom
  o en un navegador muy antiguo: no hay fondo y tampoco error.
- **`stop()` limpia.** Quita el ticker y los oyentes, mata los tweens y borra
  el canvas, porque puede volver a arrancar cuando se reactiva el interruptor.
- **El componente.** `viewChild.required` da el `<canvas>`; el `effect` del
  componente llama a `start()` o `stop()` según el interruptor, y
  `DestroyRef` detiene el campo al destruirse. `aria-hidden` y
  `pointer-events: none` lo hacen puramente decorativo.
- **Probar sin canvas.** La prueba entrega un contexto falso que acepta
  cualquier llamada y comprueba el destino interno del campo (el único estado
  observable) tras eventos de puntero sintéticos.

### Errores comunes

- **Decidir con `ontouchstart`.** Es una propiedad que existe en muchos
  portátiles; el campo dejaba de seguir al ratón sin que nadie lo notara.
- **Olvidar matar los tweens al redimensionar.** Cada cambio de tamaño
  sumaba una cadena de deriva por punto.
- **Poner el canvas encima del contenido.** Sin `z-index: 0` y con el
  resto en `position: relative`, el canvas tapa los clics; sin
  `pointer-events: none` los bloquea aunque quede detrás.
- **Un canvas con el tamaño del CSS y sin escalar el bitmap.** Se ve
  borroso en pantallas de alta densidad.
- **Ordenar todos los puntos para cada punto.** Cuadrático y, en un campo
  de unos cientos de puntos, innecesario.

### Preguntas de entrevista (senior)

#### 1. ¿Cómo haces nítido un canvas en una pantalla de alta densidad?

**Respuesta:**

Con dos tamaños: el atributo `width`/`height` del canvas (el bitmap) se
multiplica por `devicePixelRatio`, y el tamaño visible lo fija el CSS. Después
se aplica `setTransform(ratio, 0, 0, ratio, 0, 0)` al contexto para seguir
dibujando en píxeles CSS. Sin eso, el navegador estira un bitmap de baja
resolución y todo sale borroso. Conviene recalcularlo al redimensionar, y el
coste de memoria crece con el cuadrado del ratio.

#### 2. ¿Por qué `pointermove` y no `mousemove` o una comprobación de soporte táctil?

**Respuesta:**

Comprobar `'ontouchstart' in window` mide lo que el dispositivo *puede*
hacer, no lo que la persona *está* haciendo: muchos portátiles con
pantalla táctil la tienen y por eso nunca recibían el ratón. Los eventos de
puntero unifican ratón, lápiz y dedo y traen `pointerType`, así que se
escucha siempre y se decide por evento. Es el patrón general: reaccionar a
la entrada real en lugar de adivinar la capacidad del dispositivo.

#### 3. ¿Por qué comparar distancias al cuadrado?

**Respuesta:**

Porque ordenar o comparar por distancia da el mismo resultado con o sin raíz
cuadrada: si `a < b` entonces `a² < b²` para valores no negativos. Se evita
una operación costosa en un bucle que corre en cada frame para cientos de
puntos, y los umbrales se escriben ya elevados al cuadrado. El truco sólo
vale para comparar; si hubiera que mostrar la distancia, habría que calcular
la raíz.

<!-- /study-guide:section:animations-a3-dots -->

---

<!-- study-guide:section:animations-a4-motion-switch -->
## Módulo A4: El interruptor de animaciones

Fuente: `src/app/shared/services/motion.service.ts`,
`src/app/shared/components/motion-toggle/`, `src/styles/_base.scss` y
`src/app/shared/components/header/` del repositorio.

### El problema que resuelve

El fondo de puntos se mueve sin parar, y un movimiento que dura más de cinco
segundos exige, según la pauta WCAG 2.2.2 (nivel A), una forma de pausarlo u
ocultarlo. Portify no la trae. El sitio necesitaba un control para apagar el
movimiento, pero el movimiento tiene **tres fuentes distintas**: los reveals
de GSAP, el lienzo y las animaciones y transiciones de CSS (las ondas del
retrato, el relleno de los enlaces). Un interruptor que sólo apagara una dejaba
el sitio a medias.

Hubo además una decisión de producto. La primera idea, nacida de un plan de
desarrollo, era respetar `prefers-reduced-motion` del sistema por defecto. En la
máquina de Janio Windows tiene esa preferencia activa y el sitio se veía
congelado sin que él lo hubiera pedido. Decidió el 13 de noviembre de 2026:
**manda la app, no la máquina**.

### La decisión en este sitio

- **Un servicio, `MotionService`**, con una señal `enabled` (por defecto
  encendida), una elección que se recuerda en `localStorage` y un atributo
  `data-motion="off"` en `<html>` cuando está apagado.
- **Las tres fuentes dependen de él**: el inicializador de la coreografía
  (Módulo A1) y el fondo (Módulo A3) leen la señal; el CSS lee el atributo.
- **No se consulta `prefers-reduced-motion`**, ni en JavaScript ni en CSS. La
  regla que lo hacía se sustituyó por una regla sobre el atributo.
- **Con el interruptor apagado se quitan las transiciones** (`transition:
  none`) en vez de acortarlas.
- **Un botón `role="switch"`** a la derecha de la barra del encabezado, con
  nombre fijo («Animations» / «Animaciones») y el estado en `aria-checked`.
- **En pantallas de menos de 370 px la etiqueta no se dibuja.** Con el
  encabezado fijo (el [Módulo E7 de la Parte 2](02-cimientos-de-estilo.md#módulo-e7-los-estilos-del-menú-de-portify-traducidos-a-un-componente), que explica los estilos del menú) la barra tiene que caber en una fila, y
  en un teléfono estrecho la etiqueta («Animations» mide 142 px, «Animaciones»
  153 px) empujaba el botón del menú a una segunda fila. Se oculta sólo a la
  vista (`clip-path`, tamaño de 1 px): sigue en el DOM, así que el interruptor
  conserva su nombre accesible.
- **La elección guardada se aplica antes del primer pintado.** Si sólo la
  aplicara el servicio, quien apagó el movimiento vería un instante las ondas
  del hero, porque Angular tarda en arrancar y en hidratar. Un script pequeño
  en línea, al principio del `<head>` de `src/index.html`, lo evita:


  Repite a propósito la clave (`motion`), el valor (`off`) y el atributo del
  servicio, porque corre antes que Angular. Si el almacenamiento falla (una
  ventana privada, datos del sitio bloqueados) la página se queda con el
  movimiento encendido. Una prueba de contenido
  (`scripts/motion-first-paint.test.mjs`) ejecuta ese script contra una página
  falsa y comprueba que las tres cosas coinciden con `motion.service.ts`.

### El código

`src/app/shared/services/motion.service.ts`:


`src/app/shared/components/motion-toggle/motion-toggle.component.ts`:


`src/app/shared/components/motion-toggle/motion-toggle.component.html`:


`src/app/shared/components/motion-toggle/motion-toggle.component.scss`:


La regla de CSS, al final de `src/styles/_base.scss`:


En `header.component.html`, el botón va dentro del grupo de la derecha, antes del
botón del menú: `<shared-motion-toggle />`. Las pruebas están en
`motion.service.spec.ts` y `motion-toggle.component.spec.ts`.

### Cómo funciona por dentro

- **Una señal para JavaScript, un atributo para CSS.** El estado vive en la
  señal `enabled`; `apply` lo refleja en el atributo `data-motion` de
  `<html>`. JavaScript reacciona a la señal; CSS, al selector
  `:root[data-motion='off']`. Una sola fuente de verdad con dos lectores.
- **El estado inicial.** En el servidor (prerenderizado) el servicio no toca
  nada: la página siempre sale encendida. En el navegador, el constructor lee
  `localStorage` y, si encuentra `'off'`, aplica el apagado. Todo acceso a
  `localStorage` va en `try/catch`: puede lanzar en ventanas privadas o con
  los datos del sitio bloqueados, y el interruptor debe seguir funcionando
  para esa visita.
- **Cómo reacciona la coreografía.** Un `effect` en el inicializador del Módulo
  A1 observa `motion.enabled()`. Su primera ejecución sólo registra el
  estado inicial; las siguientes llaman a `refresh(false)`: se revierte el
  contexto de GSAP y, si el movimiento está encendido, se vuelve a ejecutar la
  coreografía tras el siguiente render. Apagar devuelve todo al estado de CSS;
  encender reproduce las entradas desde el principio.
- **Cómo reacciona el fondo.** Un `effect` del componente llama a
  `field.start()` o `field.stop()`; `stop()` borra el canvas.
- **Quitar frente a acortar las transiciones.** Una transición acortada a
  0,01 ms conserva su **retraso**. El menú móvil usa
  `visibility 0s linear 500ms` para seguir visible durante la salida y
  desaparecer después; con el retraso intacto, al cerrarlo el panel salía de
  pantalla pero sus enlaces seguían en el orden de tabulación medio segundo.
  `transition: none` elimina duración y retraso. Las animaciones sí se acortan
  (0,01 ms y una iteración) porque su estado final es el que importa.
- **El botón.** `role="switch"` y `aria-checked` hacen que un lector de
  pantalla anuncie «Animaciones, interruptor, activado». El nombre **no
  cambia** con el estado: la regla es que el nombre dice qué es y el estado
  dice cómo está. El indicador visual (una píldora con un círculo) tiene
  `aria-hidden`.
- **Por qué `data-motion` y no una clase.** Es un dato, no un estilo; y un
  atributo de datos en `<html>` no choca con las clases de ningún componente.
- **Pruebas.** El servicio se comprueba con y sin valor guardado, y se
  verifica que **no consulta `matchMedia`**. El botón, que cambia de estado
  con cada clic y se etiqueta en cada idioma.

### Errores comunes

- **Apagar sólo una fuente.** Un interruptor que detiene GSAP pero no el
  canvas ni el CSS deja moverse cosas que la persona quería quietas.
- **Medio respetar el sistema.** Mantener la regla CSS de
  `prefers-reduced-motion` y no que JavaScript la mire (o al revés) da
  un sitio con ondas quietas y tarjetas animadas, según la máquina.
- **Acortar en vez de quitar transiciones con retraso.** Deja una ventana en
  la que algo ya fuera de pantalla sigue en el orden de tabulación.
- **`aria-pressed` con una etiqueta que cambia («Activar»/«Desactivar»).**
  Se anuncia dos veces el estado y confunde; el nombre debe ser fijo.
- **Leer `localStorage` sin `try/catch`.** Lanza en ventanas privadas.
- **Apagar el movimiento sólo desde el servicio.** Angular tarda en arrancar y
  en hidratar; hasta entonces la página ya se pintó con las ondas. El script
  del `<head>` corre antes del primer pintado y el servicio sigue siendo la
  fuente de verdad después.
- **Cambiar la clave, el valor o el atributo en un sitio y no en el otro.** El
  script y el servicio repiten `motion`, `off` y `data-motion`. La prueba
  `scripts/motion-first-paint.test.mjs` lee `motion.service.ts` y falla si
  dejan de coincidir.
- **Ocultar la etiqueta con `display: none`.** El botón se queda sin nombre
  accesible. Se oculta con `clip-path` y un tamaño de 1 px.

### Preguntas de entrevista (senior)

#### 1. El sistema operativo ya tiene una preferencia de movimiento. ¿Por qué un interruptor propio, y por qué no consultar la preferencia?

**Respuesta:**

La preferencia del sistema es un buen valor por defecto para la mayoría de los
sitios, y respetarla es lo recomendable. Aquí hubo una razón de producto: en la
máquina del autor estaba activa de fábrica y el sitio se veía congelado sin
que lo hubiera pedido, así que decidió que mande la aplicación. El interruptor
propio cubre la necesidad de accesibilidad (poder detener un movimiento
continuo) sin depender de lo que diga el equipo, y recuerda la elección por
navegador. La contrapartida, que hay que decir en voz alta, es que quien ya
había pedido menos movimiento al sistema lo ve activo hasta que lo apague.

#### 2. Hay movimiento hecho con JavaScript (GSAP y un canvas) y con CSS. ¿Cómo mantienes un único control?

**Respuesta:**

Con una única fuente de verdad y dos lectores. El estado vive en una señal de
un servicio; JavaScript reacciona a ella con `effect` (revertir y volver a
ejecutar, detener y limpiar el canvas). Para CSS, el servicio refleja el
estado como un atributo en `<html>` y una regla `:root[data-motion='off']`
con `!important` detiene animaciones y transiciones en todos los
elementos. Así no hay que tocar ningún componente: añadir un efecto nuevo,
sea de GSAP o de CSS, queda cubierto sin pensar.

#### 3. ¿Qué diferencia hay entre acortar una transición a 0,01 ms y eliminarla, y cuándo importa?

**Respuesta:**

Acortar la duración deja intactas las demás propiedades de la transición, en
particular el retraso (`transition-delay`). Una transición de `visibility` con
un retraso de 500 ms (un patrón habitual para ocultar un panel después de que
termine de deslizarse) sigue esperando medio segundo, y durante ese tiempo
un panel cerrado conserva sus enlaces en el orden de tabulación. `transition:
none` elimina duración y retraso a la vez. En animaciones (`@keyframes`) lo
habitual es acortar la duración, porque lo que importa es que lleguen al
estado final; en transiciones con retraso, quitarlas.

#### 4. La elección guardada ya la lee el servicio. ¿Por qué además un script en línea en el `<head>`?

**Respuesta:**

Porque el servicio corre cuando Angular arranca, y para entonces el navegador
ya pintó la página con el movimiento encendido: quien lo apagó vería un instante
las ondas del hero en cada visita. Un script síncrono al principio del `<head>`
se ejecuta antes del primer pintado y pone `data-motion="off"` en `<html>`, que
es lo que lee el CSS. No sustituye al servicio: éste sigue guardando la
elección y sincronizando la señal que usan GSAP y el fondo de puntos.

El precio es repetir la clave, el valor y el atributo en dos sitios, y por eso
una prueba compara el script con el código del servicio. Dentro del script,
todo va en un `try/catch`: si el almacenamiento falla, la página sigue con el
movimiento encendido y nada se rompe. El servidor no lo ejecuta: el HTML
prerenderizado es siempre el de «encendido».

<!-- /study-guide:section:animations-a4-motion-switch -->

---

## Qué sigue en esta parte

El grano de Portify (una textura fija con mezcla de color) no se
implementó: pesa y no aporta al contenido. El interruptor de movimiento y el
comportamiento del menú se pueden recorrer juntos en [Navegación y movimiento](learn-navigation.md).
