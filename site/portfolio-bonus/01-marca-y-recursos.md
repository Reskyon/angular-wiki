# Parte 1: Marca y recursos

> Esta versión pública conserva las explicaciones y omite fragmentos que reproducen o adaptan la plantilla comercial.

Esta parte deja en el repositorio todo lo que el sitio necesita de la marca
antes de escribir una sola línea de Angular: los logos como SVG limpios, las
fuentes web alojadas en el propio sitio y los favicons e iconos de aplicación.
Son archivos estáticos que no cambian con el código, así que conviene
resolverlos primero y bien, una sola vez.

**Si llegaste aquí desde un buscador.** Esta página es una parte de la guía
«Cómo se construye este sitio», escrita sobre el repositorio de
janioisacura.com, un portfolio hecho con Angular que se publica como HTML
estático. No hace falta conocer el repositorio: cada módulo explica el
problema, muestra los comandos y el código completos, y lo que enseña sirve
para cualquier sitio web, con Angular o sin él. Para seguirla en tu proyecto
necesitas Node.js, un editor vectorial que exporte SVG (aquí, Illustrator) y
un navegador. Va al principio de la guía porque los módulos siguientes dan por
hecho que los logos, las fuentes y los favicons ya existen.

**Proyecto:** la raíz del repositorio; los archivos quedan en `public/`.
**Sitio publicado:** [janioisacura.com](https://janioisacura.com/en/). Ábrelo
mientras lees: la pestaña muestra el favicon y los títulos usan la fuente que
se carga aquí.

**Qué vas a aprender:**

- [Módulo M1](#módulo-m1-exportar-svg-desde-illustrator): **Exportar un SVG
  que sirva para la web.** Las siete opciones del cuadro de exportación de
  Illustrator, por qué cada una, y cómo se ve el archivo que sale.
- [Módulo M2](#módulo-m2-limpiar-el-svg-con-svgo): **Quitar lo que sobra con
  SVGO.** Qué deja Illustrator en el archivo, el comando, cuánto pesa después
  y cómo hacer que un logo de un solo color tome el color del CSS.
- [Módulo M3](#módulo-m3-por-qué-las-fuentes-van-en-woff2): **Por qué las
  fuentes van en woff2.** Qué es cada formato, cuánto pesa, qué navegadores lo
  leen, y por qué este sitio aloja las fuentes en vez de usar Adobe Fonts o
  Google Fonts.
- [Módulo M4](#módulo-m4-convertir-ttf-y-otf-a-woff2-con-un-script): **Un
  script que convierte una carpeta entera.** `ttf2woff2` desde la terminal y
  el script de Bash completo, con sus trampas en Windows.
- [Módulo M5](#módulo-m5-cargar-las-fuentes-con-font-face): **Cargar las
  fuentes.** Las reglas `@font-face`, la tipografía base, la precarga en el
  `<head>` y cómo comprobar en el navegador que de verdad se usan.
- [Módulo M6](#módulo-m6-favicons-con-realfavicongenerator): **Favicons e
  iconos de aplicación.** Por qué un logo no se puede usar tal cual, el
  recorrido completo por RealFaviconGenerator con las opciones elegidas, y el
  bloque del `<head>`.

Cada módulo sigue el mismo orden: el problema que resuelve, la decisión tomada
en este sitio, el procedimiento o el código completo, cómo funciona por
dentro, errores comunes y preguntas de entrevista con su respuesta.

Esta página es una parte de la guía [Cómo se construye este sitio](como-se-construye.md);
allí están el mapa y la ruta recomendada. Conviene haber leído antes
[Plantilla Portify](plantilla-portify.md), el punto de partida visual.

---

<!-- study-guide:section:brand-m1-illustrator-svg -->
## Módulo M1: Exportar SVG desde Illustrator

Fuente: `public/brand/logo/` del repositorio y el cuadro *SVG Options* de
Illustrator.

### El problema que resuelve

Un logo se diseña en un programa vectorial, pero el navegador no abre un
archivo de Illustrator. Hay que exportarlo a **SVG**, un formato de texto que
describe las formas con coordenadas: pesa poco, se ve nítido a cualquier
tamaño y se puede cambiar de color con CSS. El cuadro de exportación de
Illustrator tiene siete opciones y las que vienen por defecto no son las
mejores para la web: generan clases CSS que chocan entre archivos, dependen
de fuentes instaladas y arrastran nombres de capas.

### La decisión en este sitio

Todos los logos del sitio son SVG, diseñados por Janio en Illustrator. Hay
tres piezas (logo completo, isotipo y texto) y cada una en tres versiones
(color, negro y blanco): nueve archivos en `public/brand/logo/`
(`logo_color.svg`, `iso_black.svg`, `type_white.svg`, etc.). El isotipo es el
«ojo» de circuitos con el punto; de él salen también los favicons del
[Módulo M6](#módulo-m6-favicons-con-realfavicongenerator).

### Antes de exportar

- El gráfico tiene que ser vectorial de punta a punta: sin imágenes
  incrustadas ni enlazadas. Un PNG dentro de un SVG pierde todas las ventajas
  del formato.
- Si el logo lleva texto, puede seguir siendo texto hasta el momento de
  exportar; la opción *Convert To Outlines* lo convierte en trazados, así el
  SVG no depende de que la fuente esté instalada en la máquina que lo abre.
- Renombra la capa (`Layer 1`) con un nombre corto, o déjala vacía:
  Illustrator escribe el nombre de la capa como atributo `data-name` y SVGO no
  lo quita.

### El procedimiento

Archivo → Exportar → Exportar como…, formato **SVG**. En el cuadro
*SVG Options*:

| Opción | Valor | Por qué |
| --- | --- | --- |
| Styling | **Presentation Attributes** | Escribe `fill="#a261bc"` en cada forma. *Internal CSS* genera clases `.cls-1`, `.cls-2` que chocan entre sí cuando dos SVG se incrustan en la misma página |
| Font | **Convert To Outlines** | El texto pasa a trazados; el SVG no depende de fuentes instaladas |
| Images | **Preserve** (o Embed) | Sólo importa si hay imágenes rasterizadas; *Preserve* las deja como archivos enlazados que no existen en la web. Lo correcto es que no haya ninguna |
| Object IDs | **Minimal** | *Layer Names* mete los nombres de capas y objetos como `id` y engorda el archivo |
| Decimal | **2** | Dos decimales bastan para un logo; con 1 pueden aparecer escalones en curvas pequeñas |
| Minify | marcado | Quita espacios y saltos de línea. SVGO lo hace igual, así que no es decisivo |
| Responsive | **marcado** | Quita `width` y `height` y deja sólo `viewBox`: el SVG escala con el CSS que lo use |

**Show Code** abre el resultado en un editor de texto sin guardar nada; sirve
para revisar que los colores sean los de la marca y que no haya etiquetas
`<image>` ni `<text>`.

### Cómo se ve el archivo que sale

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 306.39 99.04">
  <g>
    <path d="M52.75,25.79c1.28,0,…" fill="#a261bc"/>
    …
  </g>
  <path d="M60.23,43.98c0-4.13,…" fill="#6cb0a3"/>
</svg>
```

Lo importante está en la primera etiqueta: `viewBox` (el sistema de
coordenadas del dibujo) y ningún `width` ni `height`. Cada forma lleva su
`fill` como atributo, que es lo que permite cambiarlo desde CSS. Sobran dos
cosas para la web: el prólogo `<?xml …?>` y el `id="Layer_1"`; las quita el
módulo siguiente.

### Cómo funciona por dentro

`viewBox="0 0 306.39 99.04"` significa «este dibujo ocupa un rectángulo de
306,39 por 99,04 unidades». Cuando el SVG se muestra a 150 píxeles de ancho,
el navegador escala todas las coordenadas en proporción; por eso no pierde
nitidez. Si el archivo trajera además `width="306.39"`, ese tamaño fijo
ganaría por defecto y habría que anularlo desde CSS. Al exportar con
*Responsive*, el tamaño queda en manos de quien lo usa.

### Errores comunes

- **Exportar con *Internal CSS* e incrustar dos SVG en la misma página:** el
  segundo toma las clases `.cls-1` del primero y cambia de color.
- **Dejar texto como texto:** se ve bien en tu máquina, que tiene la fuente, y
  con otra fuente en la de los demás.
- **Usar *Save As* en vez de *Export As*:** el cuadro *Save As → SVG* es otro,
  pensado para volver a abrir el archivo en Illustrator, y guarda metadatos
  del programa que la web no necesita.

### Preguntas de entrevista (senior)

#### 1. ¿Cuándo conviene un SVG y cuándo un PNG o un WebP?

**Respuesta:**

SVG para todo lo que sea formas: logos, iconos, ilustraciones planas,
gráficos. Pesa poco, escala sin perder nitidez y se puede animar o recolorear
con CSS. PNG o WebP para fotografías y para cualquier imagen con degradados
complejos o mucho detalle, donde el SVG se vuelve enorme o directamente no
puede representarla. Si un «logo» es una foto o una textura, no es un caso de
SVG.

#### 2. ¿Qué diferencia hay entre poner el color como atributo y ponerlo en una clase CSS dentro del SVG?

**Respuesta:**

El atributo (`fill="#a261bc"`) vive en la forma y no choca con nada. La clase
(`.cls-1 { fill: #a261bc }`) vive en un `<style>` dentro del SVG, y cuando
el SVG se incrusta en el HTML ese `<style>` pasa a ser global de la página:
si otro SVG define también `.cls-1`, el último que se carga gana y los dos
cambian de color. Por eso para la web se exporta con *Presentation
Attributes*. Si el SVG se usa como `<img src>`, el problema no aparece, porque
cada imagen vive en su propio documento, pero tampoco se puede cambiar su
color desde fuera.

#### 3. Te entregan un SVG con `width` y `height` fijos y en la página se ve diminuto o gigante. ¿Qué haces?

**Respuesta:**

Comprobar que tenga `viewBox`; si lo tiene, quitar `width` y `height` del
archivo (o anularlos con `width: 100%; height: auto` en CSS) y dar el tamaño
desde la hoja de estilos. Si no tiene `viewBox`, hay que añadirlo con las
dimensiones originales del dibujo, porque sin él el navegador no sabe cómo
escalar las coordenadas y recorta.

<!-- /study-guide:section:brand-m1-illustrator-svg -->

---

<!-- study-guide:section:brand-m2-svgo -->
## Módulo M2: Limpiar el SVG con SVGO

Fuente: el logo exportado en el módulo anterior y la pasada de SVGO sobre él.

### El problema que resuelve

Illustrator exporta un SVG correcto pero con restos: el prólogo XML, el `id`
de la capa, grupos vacíos, atributos repetidos en cada forma y números con
más decimales de los necesarios. Nada de eso cambia el dibujo y todo suma
bytes. En un sitio con nueve logos y varios iconos, limpiarlos a mano no es
una opción.

### La decisión en este sitio

Cada SVG pasa una vez por [SVGO](https://github.com/svg/svgo), una
herramienta de Node que limpia el archivo sin tocar el dibujo, antes de entrar
en `public/brand/logo/`. Se ejecuta con `npx`, así que no hace falta
instalarla en el proyecto ni en la máquina.

### El procedimiento

1. Abre una terminal en la carpeta donde está el archivo exportado (en el
   Explorador de Windows: botón derecho sobre la carpeta, «Abrir en
   Terminal»). No hace falta estar dentro del repositorio.
2. Ejecuta, con el nombre real del archivo:

   ```bash
   npx svgo logo.svg
   ```

   La primera vez pregunta si instala el paquete: responde `y`. Sobrescribe el
   archivo. Para conservar el original y escribir otro:

   ```bash
   npx svgo logo.svg -o logo.min.svg
   ```

3. Lee el resumen. En el logo de este sitio:

   ```
   logo.svg:
   Done in 13 ms!
   2.436 KiB - 32.4% = 1.646 KiB
   ```

### Qué cambió

Antes, 2,4 KB con el prólogo, el `id` y un `fill` por forma. Después, 1,6 KB
en una sola línea:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 306.39 99.04"><g fill="#a261bc"><path d="M52.75 25.79c1.28 0 2.53.14 3.73.39V0h-7.47v26.18c1.21-.25 2.46-.39 3.74-.39"/>…</g>…</svg>
```

SVGO quitó el prólogo y el `id`, agrupó las formas que comparten `fill` en un
`<g fill="…">` y reescribió los trazados con menos caracteres. Queda el
`data-name="Layer 1"` si no se renombró la capa; se borra a mano o se deja,
no afecta al dibujo.

### Cómo funciona por dentro

SVGO aplica una lista de *plugins*, cada uno con una transformación segura:
quitar comentarios y metadatos, fusionar atributos iguales en el grupo padre,
redondear números, convertir `polygon` en `path` cuando ahorra bytes. Las
transformaciones por defecto no cambian lo que se ve; las que podrían hacerlo
(como quitar el `viewBox`) vienen desactivadas en las versiones actuales.

### Comprobar

- Arrastra el SVG al navegador: tiene que verse igual que en Illustrator.
- Ábrelo en un editor y confirma que empieza por `<svg xmlns=… viewBox=…>` y
  que los `fill` son los colores de la marca.
- Incrustado en una página o como `<img>`, el tamaño lo decide el CSS; sin
  `width`/`height` propios y sin CSS, algunos navegadores lo muestran a
  300 × 150.

### Variantes de un solo color

Para las versiones monocromas (negro, blanco, gris) no hacen falta varios
archivos: se exporta una y se cambia cada `fill="#…"` por
`fill="currentColor"`. Así el color lo decide el CSS del sitio
(`color: #606060`) y el mismo archivo sirve en fondo claro y oscuro. La
versión a color, con dos tonos de marca, sí se mantiene como archivo propio.
En este sitio se guardaron las tres versiones como archivos separados por
decisión de Janio; `currentColor` queda como alternativa para los iconos.

### Errores comunes

- **Pasar SVGO con una configuración vieja que quita el `viewBox`:** el SVG
  deja de escalar. Si usas un `svgo.config.js` de otro proyecto, revisa que
  `removeViewBox` esté desactivado.
- **Optimizar antes de terminar el diseño:** SVGO fusiona y simplifica, y el
  archivo optimizado es peor para seguir editando. Guarda el original de
  Illustrator aparte y optimiza sólo la copia que va al sitio.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué optimizar un SVG si Nginx ya lo comprime con gzip o Brotli?

**Respuesta:**

Porque la compresión reduce bytes en el cable pero no el trabajo del
navegador: cada nodo, atributo y decimal se sigue analizando y dibujando. Un
SVG limpio se transfiere menos, se analiza más rápido y, si se incrusta en el
HTML, no arrastra `id` y clases que puedan chocar. Además, la compresión del
servidor no aplica cuando el SVG va dentro del HTML o del CSS.

#### 2. ¿Qué es `currentColor` y qué problema resuelve?

**Respuesta:**

Es una palabra clave de CSS que vale «el color de texto actual del elemento».
Un SVG con `fill="currentColor"` toma el `color` que tenga donde se incruste,
así un mismo icono sirve en claro y oscuro, en un botón o en un enlace, sin
duplicar archivos. Sólo funciona con SVG incrustado en el HTML (o en un
componente); como `<img src>` el navegador no le pasa el color de fuera.

<!-- /study-guide:section:brand-m2-svgo -->

---

<!-- study-guide:section:brand-m3-why-woff2 -->
## Módulo M3: Por qué las fuentes van en woff2

Fuente: `public/brand/fonts/` del repositorio y `docs/site-structure.md`,
sección «Brand and typography».

### El problema que resuelve

Una fuente que no está instalada en la máquina de quien visita el sitio hay
que enviársela. Eso se puede hacer de dos formas: cargarla desde un servicio
externo (Google Fonts, Adobe Fonts) o alojarla en el propio sitio. Y en el
segundo caso hay que elegir el formato, porque el archivo que se descarga de
Google Fonts (`.ttf`) no es el que conviene publicar.

### La decisión en este sitio

- **Autoalojadas.** Las fuentes viven en `public/brand/fonts/` y se sirven
  desde el propio dominio. Sin peticiones a terceros, sin depender de que un
  servicio siga existiendo o de una suscripción.
- **Barlow Condensed** para títulos (sólo las itálicas Light, Regular y
  SemiBold) y **Mozilla Text Light** para el texto de lectura. Las dos tienen
  licencia SIL Open Font License (OFL), que permite usarlas, convertirlas y
  publicarlas en un sitio con una sola condición: el archivo `OFL.txt` viaja
  con la fuente.
- **Gazzetta se descartó.** Era la fuente de la pizarra de marca, pero es de
  Adobe Fonts: no se puede descargar ni alojar, sólo cargar desde el CDN de
  Adobe mientras la suscripción de Creative Cloud siga activa. Para un sitio
  público eso es una dependencia externa en cada carga y un riesgo de licencia
  si la suscripción cambia.
- **Formato `.woff2`**, un archivo por peso que se usa de verdad.

Los archivos quedan así:

```
public/brand/fonts/
  barlow_condensed/
    BarlowCondensed-LightItalic.woff2
    BarlowCondensed-Italic.woff2
    BarlowCondensed-SemiBoldItalic.woff2
    OFL.txt
  mozilla_text/
    MozillaText-Light.woff2
    OFL.txt
```

### Los formatos

| Formato | Qué es | Para qué sirve |
| --- | --- | --- |
| TTF / OTF | La fuente «de escritorio»: contornos, métricas y tablas sin comprimir | Instalarla en el sistema; es lo que descargan Google Fonts y las fundiciones |
| WOFF | TTF u OTF envuelto y comprimido con zlib (como un zip) | Formato web de 2010; ya no hace falta |
| **WOFF2** | Lo mismo, comprimido con Brotli y con las tablas reordenadas para comprimir mejor | El formato web actual; los navegadores lo leen desde 2016–2018 |

En este sitio, `MozillaText-Light.ttf` pesa 65 KB y el `.woff2` 25 KB: un
39 % del original. Las itálicas de Barlow quedaron en unos 40 KB cada una.
Un `.woff2` suele pesar entre el 30 y el 50 % del TTF.

### Cómo funciona por dentro

Una fuente es un conjunto de tablas: contornos de cada letra, anchos,
*kerning*, nombres. WOFF2 no cambia esas tablas; las comprime con Brotli, el
mismo algoritmo que usan los servidores web, y antes transforma la tabla de
contornos a una forma que se comprime mejor. El navegador la descomprime al
cargarla y a partir de ahí es la misma fuente. Por eso convertir a `.woff2`
no pierde calidad: es un envoltorio, no una reducción.

### Fuente variable o archivos estáticos

Mozilla Text se descarga como fuente **variable** (un archivo con todos los
pesos en un eje `wght`) y como archivos **estáticos** (uno por peso). Un
archivo estático sólo trae un peso: si cargas sólo `MozillaText-Light` y
pones `font-weight: 700`, el navegador «engorda» la Light artificialmente y
se ve borrosa. Las opciones:

1. **Un archivo por peso que uses de verdad.** Light para lectura y Bold para
   negritas. Dos archivos pequeños, dos reglas `@font-face`.
2. **La variable.** Un solo archivo con los seis pesos, más grande que uno
   estático pero más pequeño que tres juntos. Compensa a partir de tres pesos.

Este sitio usa la opción 1: sólo el peso Light por ahora, y `font-synthesis:
none` en el CSS ([Módulo M5](#módulo-m5-cargar-las-fuentes-con-font-face))
para que el navegador nunca invente un peso que no existe.

### Errores comunes

- **Publicar el `.ttf`:** funciona, pero pesa el doble o el triple y tarda
  más en mostrar el texto.
- **Subir la variable completa para usar un peso:** descargas seis pesos para
  pintar uno.
- **Cargar la fuente recta y «inclinarla» con `font-style: oblique`:** el
  navegador sintetiza la inclinación por transformación, sin corregir curvas
  ni espaciado, y el ángulo cambia según el navegador. La itálica real está
  dibujada; si todos los títulos van en itálica, carga sólo las itálicas.
- **Olvidar el `OFL.txt`:** la condición 2 de la OFL exige que cada copia
  distribuida lleve el aviso de copyright y la licencia, y publicar el
  `.woff2` en el sitio es distribuir una copia. No hace falta crédito visible
  en el sitio ni cambiar el nombre: convertir a `.woff2` cuenta como «versión
  modificada», pero ni Barlow ni Mozilla Text declaran un *Reserved Font
  Name*.

### Preguntas de entrevista (senior)

#### 1. ¿Autoalojar las fuentes o cargarlas desde Google Fonts? ¿Qué cambia?

**Respuesta:**

Desde Google Fonts el navegador hace dos peticiones a dominios ajenos (el CSS
y la fuente), con sus conexiones y su latencia, y envía la IP de cada visita
a Google, lo que en Europa ya ha costado sanciones. Autoalojadas, las fuentes
salen del mismo dominio y la misma conexión que el HTML, se pueden precargar,
y el sitio no depende de que el servicio siga existiendo o cambie su CSS. La
caché compartida entre sitios que justificaba Google Fonts ya no existe:
los navegadores particionan la caché por sitio desde 2020. Hoy, autoalojar
es la opción por defecto.

#### 2. Un diseñador te pide usar una fuente de Adobe Fonts en un sitio público. ¿Qué le explicas?

**Respuesta:**

Que Adobe Fonts no entrega el archivo: la fuente se carga desde el CDN de
Adobe con un `<link>` a `use.typekit.net`, ligado a la suscripción de
Creative Cloud. Si la suscripción caduca, el sitio pierde la fuente; cada
carga hace una petición a Adobe; y no se puede precargar ni servir desde el
propio dominio. Es viable para un sitio que acepte esa dependencia; para un
portfolio que tiene que seguir funcionando solo, conviene una fuente con
licencia OFL o comprada con licencia de *webfont* y autoalojada.

#### 3. ¿Por qué `.woff2` y no `.woff` con `.ttf` de respaldo, como se hacía antes?

**Respuesta:**

Porque ya no hay navegador relevante que no lea `.woff2`: Chrome desde 2014,
Firefox desde 2015, Safari desde 2016 y Edge desde 2017. El respaldo en
`.woff` o `.ttf` sólo añade archivos que nadie descarga y una lista `src` más
larga. Un solo `src: url(…) format("woff2")` basta.

<!-- /study-guide:section:brand-m3-why-woff2 -->

---

<!-- study-guide:section:brand-m4-convert-script -->
## Módulo M4: Convertir TTF y OTF a woff2 con un script

Fuente: el script `convert-fonts-to-woff2.sh` usado para preparar las fuentes
de este sitio (se guarda junto a los originales, fuera del repositorio).

### El problema que resuelve

Google Fonts y las fundiciones entregan `.ttf` u `.otf`. Para publicar
`.woff2` hay que convertirlos, y conviene hacerlo con un comando repetible y
no con un conversor web cada vez que se añade un peso.

### La herramienta

`ttf2woff2` es un paquete de npm con línea de comandos. Lee el TTF (u OTF)
por la **entrada estándar** y escribe el WOFF2 por la **salida estándar**; no
acepta nombres de archivo como argumentos. En Git Bash, desde la carpeta de la
fuente:

```bash
npx ttf2woff2 < MozillaText-Light.ttf > MozillaText-Light.woff2
```

En PowerShell el `<` no existe; se pasa por `cmd`:

```bash
cmd /c "npx ttf2woff2 < MozillaText-Light.ttf > MozillaText-Light.woff2"
```

La primera vez `npx` descarga el paquete y tarda un poco: intenta compilar un
módulo nativo y, si no puede, usa su versión en WebAssembly; el resultado es
el mismo. Un aviso sobre una versión vieja de `glob` durante la instalación
es inofensivo.

### El script

Convierte todos los `.ttf` y `.otf` de una carpeta y deja el `.woff2` al
lado, con el mismo nombre. Salta los que ya tienen `.woff2`, así se puede
volver a ejecutar sin rehacer nada, y si una conversión falla borra el archivo
a medias.

```bash
#!/usr/bin/env bash
# Convert every .ttf and .otf font in a folder to .woff2, next to the original.
# Existing .woff2 files are left alone, so the script can be run again safely.
#
# Usage: ./convert-fonts-to-woff2.sh [folder]   (default: current folder)
# Requires Node.js; the ttf2woff2 package is fetched by npx on first use.

set -euo pipefail

dir="${1:-.}"

if [ ! -d "$dir" ]; then
  echo "Error: '$dir' is not a folder." >&2
  exit 1
fi

shopt -s nullglob nocaseglob
fonts=("$dir"/*.ttf "$dir"/*.otf)
shopt -u nocaseglob

if [ ${#fonts[@]} -eq 0 ]; then
  echo "No .ttf or .otf fonts found in '$dir'." >&2
  exit 1
fi

converted=0
skipped=0
failed=0

for font in "${fonts[@]}"; do
  out="${font%.*}.woff2"
  name="$(basename "$font")"

  if [ -e "$out" ]; then
    echo "skip  $name (woff2 already exists)"
    skipped=$((skipped + 1))
    continue
  fi

  if npx --yes ttf2woff2 < "$font" > "$out"; then
    in_size=$(wc -c < "$font")
    out_size=$(wc -c < "$out")
    echo "ok    $name -> $(basename "$out") (${in_size} -> ${out_size} bytes)"
    converted=$((converted + 1))
  else
    rm -f "$out"
    echo "FAIL  $name" >&2
    failed=$((failed + 1))
  fi
done

echo
echo "Converted: $converted, skipped: $skipped, failed: $failed"
[ "$failed" -eq 0 ]
```

Uso, desde la carpeta de las fuentes o pasando la carpeta:

```bash
bash convert-fonts-to-woff2.sh .
```

```bash
bash convert-fonts-to-woff2.sh "C:/ruta/a/las/fuentes"
```

### Cómo funciona por dentro

- `set -euo pipefail` hace que el script pare en el primer error en vez de
  seguir con archivos a medias.
- `shopt -s nullglob nocaseglob` hace que `*.ttf` no coincida con nada si no
  hay archivos (en vez de quedarse como texto) y que valga para `.TTF`.
- `"${font%.*}.woff2"` quita la extensión y pone la nueva.
- La conversión va con redirecciones (`<` y `>`) porque `ttf2woff2` sólo
  habla por entrada y salida estándar.
- Después de convertir, `wc -c` mide los dos archivos para mostrar el ahorro.

### Después de convertir

1. Copia sólo los `.woff2` y el `OFL.txt` a `public/brand/fonts/<familia>/`.
   Los `.ttf` se quedan con los originales, fuera del repositorio.
2. Comprueba que el `.woff2` pese entre el 30 y el 50 % del TTF. Si pesa
   igual, no se convirtió: probablemente el comando se ejecutó con el nombre
   del archivo como argumento y se quedó esperando la entrada.

### Errores comunes

- **`npx ttf2woff2 fuente.ttf fuente.woff2`:** no da error; se queda colgado
  esperando datos por la entrada estándar. Córtalo con `Ctrl+C` y usa las
  redirecciones.
- **`bash convert-fonts-to-woff2.sh` desde otra carpeta:** «No such file or
  directory». El script hay que llamarlo con su ruta (`bash
  ../../convert-fonts-to-woff2.sh .`) o copiarlo a la carpeta de las fuentes.
- **Convertir en una carpeta y copiar desde otra:** termina con el `.ttf` en
  `public/`. Antes de hacer el commit, lista la carpeta y confirma que sólo
  hay `.woff2` y `OFL.txt`.

### Preguntas de entrevista (senior)

#### 1. ¿Por qué un script de Bash para esto y no una tarea de npm en el proyecto?

**Respuesta:**

Porque la conversión ocurre una vez por fuente y fuera del ciclo de build: el
repositorio guarda ya el `.woff2`, y el build de Angular no tiene que saber
de TTF ni instalar `ttf2woff2`. Una tarea de npm tendría sentido si las
fuentes se generaran en cada build (por ejemplo, subconjuntos por idioma); con
cuatro archivos fijos sería una dependencia más para nada. El script vive con
los originales y se ejecuta cuando aparece un peso nuevo.

#### 2. ¿Qué hace `set -euo pipefail` y por qué importa en un script que escribe archivos?

**Respuesta:**

`-e` para en el primer comando que falle; `-u` trata una variable sin definir
como error, en vez de expandirla a vacío (y, por ejemplo, borrar en la carpeta
equivocada); `pipefail` hace que una tubería falle si falla cualquiera de sus
comandos, no sólo el último. En un script que crea y borra archivos, seguir
después de un error significa dejar archivos a medias o borrar lo que no
tocaba.

<!-- /study-guide:section:brand-m4-convert-script -->

---

<!-- study-guide:section:brand-m5-font-face -->
## Módulo M5: Cargar las fuentes con font-face

Fuente: `src/styles.scss` y `src/index.html` del repositorio.

### El problema que resuelve

Tener los `.woff2` en `public/` no hace nada: el navegador necesita saber
que existe una familia llamada «Barlow Condensed», en qué archivo está cada
peso y qué hacer mientras se descarga. Eso lo declara `@font-face`. Y una
vez declaradas, hay que asignarlas: qué elementos usan cuál.

### La decisión en este sitio

- Una regla `@font-face` por archivo, con `font-display: swap`.
- `html` en Mozilla Text Light (300) con `font-synthesis: none`.
- Los títulos (`h1` a `h6`) en Barlow Condensed SemiBold Italic (600) con
  `letter-spacing: -0.04em`. La pizarra de marca define tres estilos de título
  (Light -50, Regular -30 y SemiBold -40 de tracking). En esta etapa se aplica
  el mismo estilo a todos los niveles de título.
- Precarga en el `<head>` de las dos fuentes que se usan de verdad.

### El código

`src/styles.scss`, el archivo de estilos globales de Angular (lo declara
`angular.json` en `"styles"`), **tal como quedó en este módulo**:


> **Después:** este archivo único es la etapa de este módulo. En el repositorio
> actual `src/styles.scss` sólo contiene cinco `@import` (`styles/tools`,
> `styles/tokens`, `styles/bootstrap`, `styles/fonts` y `styles/base`). Las
> reglas `@font-face` se movieron tal cual a `src/styles/_fonts.scss`; la
> familia, el peso, el estilo y el tracking de `html` y de `h1` a `h6` pasaron
> a variables de Bootstrap en `src/styles/_tools.scss`, y `font-synthesis:
> none` quedó en `src/styles/_base.scss`. Ese traslado se explica en la
> [Parte 2, Módulo E4](02-cimientos-de-estilo.md#módulo-e4-fuentes-y-reglas-base).

Y en el `<head>` de `src/index.html`, la precarga:

```html
<link
  rel="preload"
  href="/brand/fonts/barlow_condensed/BarlowCondensed-SemiBoldItalic.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
<link
  rel="preload"
  href="/brand/fonts/mozilla_text/MozillaText-Light.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

### Cómo funciona por dentro

- **Tres reglas con el mismo `font-family`** no se pisan: cada una declara
  un `font-weight` y un `font-style` distintos, y el navegador elige el
  archivo que coincide con lo que pide el CSS. Si un título pide `font-weight:
  300`, carga la Light; si pide 600, la SemiBold. Y sólo descarga el archivo
  cuando algún elemento lo usa: las itálicas Light y Regular están declaradas
  pero hoy no se descargan.
- **`font-display: swap`** dice qué hacer mientras llega la fuente: mostrar el
  texto con la fuente de respaldo (`system-ui`, `Arial Narrow`) y cambiarla
  cuando termine la descarga. Sin esto, algunos navegadores dejan el texto
  invisible hasta tres segundos.
- **`font-synthesis: none`** prohíbe al navegador inventar negritas o
  cursivas que no estén cargadas. Si un `<strong>` pide 700 y sólo existe
  300, se verá en 300; eso es mejor que una negrita falsa, porque se nota
  enseguida y se corrige cargando el peso.
- **Las rutas empiezan por `/`** porque `public/` se sirve en la raíz del
  sitio: `public/brand/fonts/...` es `/brand/fonts/...`. Angular copia
  `public/` tal cual al compilar.
- **`letter-spacing: -0.04em`** es el tracking de Illustrator pasado a CSS:
  Illustrator mide en milésimas de em, así que -40 es -0,04 em. En `em` y no
  en píxeles para que escale con el tamaño del título.
- **La precarga** (`rel="preload"`) hace que el navegador pida las dos
  fuentes en cuanto lee el `<head>`, sin esperar a descargar y analizar el
  CSS; el texto aparece antes con la fuente definitiva. `crossorigin` es
  obligatorio aunque la fuente sea del mismo dominio: el navegador pide las
  fuentes en modo anónimo, y sin ese atributo la precarga no coincide con la
  petición real y se descarga dos veces. Sólo se precarga lo que se usa en la
  primera pantalla; precargar las cuatro sería descargar dos de más.

### Comprobar que se usan

Con el sitio abierto (`npm start`, `http://localhost:4200/en/`), en la
consola del navegador:

```js
await document.fonts.ready;
[...document.fonts].map(f => `${f.family} ${f.style} ${f.weight}: ${f.status}`);
```

Devuelve el estado de cada `@font-face`. En este sitio:

```
Barlow Condensed italic 300: unloaded
Barlow Condensed italic 400: unloaded
Barlow Condensed italic 600: loaded
Mozilla Text normal 300: loaded
```

`unloaded` en las dos itálicas que nadie usa es lo esperado. Para un elemento
concreto, `getComputedStyle(document.querySelector("h1")).fontFamily` tiene que
devolver la familia de marca, y en la pestaña Red del navegador cada `.woff2`
tiene que responder 200.

### Errores comunes

- **Usar `font-variation-settings: "wght" 600` en vez de `font-weight`.**
  Con una fuente variable funciona, pero no hereda bien y pisa cualquier otro
  ajuste; `font-weight` es la propiedad que entienden la cascada y las reglas
  `@font-face`. Reserva `font-variation-settings` para ejes sin propiedad
  CSS propia.
- **Precargar sin `crossorigin`:** la fuente se descarga dos veces y la
  consola avisa de que la precarga no se usó.
- **Rutas relativas (`url("brand/fonts/…")`):** funcionan en la portada y
  fallan en `/en/projects/algo/`, porque se resuelven desde la página. Con
  la barra inicial se resuelven desde la raíz.
- **Declarar una regla por familia sin peso ni estilo:** el navegador aplica
  el mismo archivo a todo y sintetiza el resto.

### Preguntas de entrevista (senior)

#### 1. ¿Qué diferencia hay entre `font-display: swap`, `block` y `optional`, y cuál eliges?

**Respuesta:**

`block` oculta el texto hasta que llega la fuente (hasta unos tres segundos)
y después la cambia; `swap` muestra el texto con la fuente de respaldo desde
el primer momento y la cambia cuando llega, con un «salto» visible; `optional`
da a la fuente unos 100 ms y, si no llegó, se queda con la de respaldo para
esa carga y usa la fuente de marca en la siguiente. Para la fuente de marca de
un portfolio, `swap` (que se vea el texto, y se vea con la marca aunque
salte). Para una fuente secundaria, `optional` evita el salto. `block` casi
nunca: texto invisible es peor que texto con otra fuente.

#### 2. El cliente se queja de que el texto «salta» cuando carga la fuente. ¿Qué haces?

**Respuesta:**

Primero, precargar la fuente para que llegue antes que el CSS y el salto sea
mínimo o no ocurra. Después, ajustar la fuente de respaldo para que ocupe lo
mismo que la de marca: con `size-adjust`, `ascent-override` y
`descent-override` en un `@font-face` de respaldo (hay herramientas que
calculan esos valores para pares como Arial y la fuente elegida). Y, si el
salto sigue molestando en títulos grandes, `font-display: optional` en esa
fuente concreta.

#### 3. ¿Por qué `font-synthesis: none` si lo normal es que el navegador «ayude» con una negrita sintética?

**Respuesta:**

Porque la negrita sintética es un engrosado mecánico del contorno: se ve
borrosa, cambia el ancho del texto y no coincide con la negrita real cuando
se añade más tarde. Con `font-synthesis: none` el fallo es visible en
desarrollo (la negrita no aparece) y la solución es cargar el peso; sin
él, el sitio se publica con negritas falsas sin que nadie lo note.

<!-- /study-guide:section:brand-m5-font-face -->

---

<!-- study-guide:section:brand-m6-favicons -->
## Módulo M6: Favicons con RealFaviconGenerator

Fuente: los archivos de iconos en la raíz de `public/`, `site.webmanifest` y
el `<head>` de `src/index.html`.

### El problema que resuelve

El favicon es el icono de la pestaña, de los marcadores, de la pantalla de
inicio del móvil y de la vista previa en algunos chats. Cada sitio lo pide en
un formato y tamaño distinto: Windows e Internet Explorer quieren `.ico`,
Safari en iOS un PNG de 180 píxeles, Android un *manifest* con PNG de 192 y
512, y los navegadores modernos aceptan SVG. Y el logo completo no sirve: el
de este sitio mide 306 × 99, y a 16 × 16 píxeles es una mancha.

### La decisión en este sitio

- El favicon es el **isotipo** (la «J» con el círculo), no el logo completo.
- Se generan todos los formatos con
  [RealFaviconGenerator](https://realfavicongenerator.net) a partir de un
  SVG del isotipo, y van en la raíz de `public/`.
- En iOS y Android, el isotipo va sobre un **fondo liso del morado de marca**
  (`#563d7c`) con márgenes, porque esas plataformas pintan el icono sobre
  blanco y una transparencia se vería mal.
- `theme-color` también en el morado de marca.

Los archivos que quedan en `public/`:

```
public/
  favicon.svg                      # navegadores modernos, escala nítido
  favicon.ico                      # 16, 32 y 48 px; Windows y navegadores viejos
  favicon-96x96.png                # PNG de respaldo
  apple-touch-icon.png             # 180 × 180, iOS
  site.webmanifest                 # nombre, colores e iconos para Android
  web-app-manifest-192x192.png
  web-app-manifest-512x512.png
```

### El procedimiento

1. **Prepara el isotipo.** En Illustrator, mesa de trabajo cuadrada con sólo
   la «J» y el círculo; exporta con las opciones del
   [Módulo M1](#módulo-m1-exportar-svg-desde-illustrator) y limpia con SVGO
   ([Módulo M2](#módulo-m2-limpiar-el-svg-con-svgo)). Comprueba que se lea a
   16 píxeles; si las líneas finas se pierden, simplifícalo para esta versión.
2. **Sube el SVG** en realfavicongenerator.net. La herramienta muestra una
   vista previa por plataforma.
3. **Favicon for Desktop:** deja el icono tal cual. Para la pestaña, el
   isotipo sobre transparente funciona en tema claro y oscuro.
4. **Apple Touch Icon (iOS):** *Add a plain background and margins*, color
   `#563d7c`. Sube el deslizador *Image size* hacia el 60 %: con el valor por
   defecto el isotipo queda pequeño dentro del icono. *App name*: «Janio
   Isacura»; *Use the main icon*.
5. **Web app manifest (Android):** lo mismo, *Add a plain background and
   margins* con `#563d7c` e *Image size* hacia el 60 % (en la vista previa de
   la pantalla de inicio se ve enseguida si quedó pequeño). *Background
   color* y *Theme color* en `#563d7c`. *Name* «Janio Isacura»; *Short name*
   lo mismo (Android corta a unos 12 caracteres, así que «Janio Isacura» no
   cabría entera). El `site.webmanifest` publicado usa
   `"short_name": "janioisacura"` y `"name": "Janio Isacura"`.
6. **Favicon path:** `/`, porque los archivos van en la raíz de `public/` y
   los navegadores piden `/favicon.ico` por su cuenta cuando una página no
   declara icono (por ejemplo, la 404). *Version*: sin marcar la primera vez;
   sirve para romper la caché cuando se cambia un favicon ya publicado. *Skip
   metadata injection*: marcado, para que los PNG no lleven la firma de la
   herramienta.
7. **Descarga el paquete** y copia los archivos a `public/`. El `favicon.ico`
   reemplaza al que trae Angular por defecto. Guarda el ZIP y el SVG de origen
   fuera del repositorio, para regenerarlo si cambia el isotipo.
8. **Reemplaza la línea del icono** en el `<head>` de `src/index.html` por el
   bloque que da la herramienta, más el `theme-color`:

   ```html
   <link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96" />
   <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
   <link rel="shortcut icon" href="/favicon.ico" />
   <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
   <meta name="apple-mobile-web-app-title" content="Janio Isacura" />
   <link rel="manifest" href="/site.webmanifest" />
   <meta name="theme-color" content="#563d7c" />
   ```

9. **Compila y comprueba.** `npm run build` tiene que dejar los siete archivos
   en `dist/<proyecto>/browser/`; en `npm start`, la pestaña muestra el
   isotipo. Si sigue el icono viejo, es caché: recarga con `Ctrl+F5`.

### Cómo funciona por dentro

- El navegador recorre los `<link rel="icon">` y elige el mejor que entiende:
  los modernos toman el SVG, que escala nítido en cualquier densidad de
  pantalla; los que no lo soportan toman el PNG o el `.ico`.
- `rel="apple-touch-icon"` es lo único que mira iOS al añadir el sitio a la
  pantalla de inicio; por eso lleva fondo: iOS no admite transparencia ahí.
- `site.webmanifest` es un JSON con el nombre, los colores y los iconos que
  usa Android (y los navegadores de escritorio al «instalar» el sitio). Sus
  iconos van marcados como `maskable`: Android los recorta con la forma que
  elija el fabricante (círculo, cuadrado redondeado), y por eso el isotipo
  necesita margen alrededor.
- `theme-color` tiñe la barra del navegador en Android y Safari; en el resto
  no hace nada.
- Angular copia `public/` a la raíz del sitio compilado, así que
  `public/favicon.ico` se sirve como `/favicon.ico` sin configurar nada.

### Errores comunes

- **Usar el logo completo:** ilegible a 16 píxeles. Siempre el isotipo o una
  letra.
- **Fondo transparente en iOS y Android:** el sistema lo pinta sobre blanco o
  lo recorta, y el icono queda flotando o cortado.
- **Dejar la línea `<link rel="icon" href="favicon.ico">` de Angular sin
  más:** funciona, pero sólo con el `.ico`; sin SVG se ve borroso en pantallas
  de alta densidad y sin *manifest* Android muestra una letra genérica.
- **Cambiar el favicon y no ver el cambio:** los navegadores cachean el
  favicon con mucha insistencia. Recarga sin caché, o regenera con la casilla
  *Version* marcada para que las rutas cambien.
- **Poner los archivos en una subcarpeta sin cambiar *Favicon path*:** las
  etiquetas y el *manifest* apuntan a la raíz y devuelven 404.

### Preguntas de entrevista (senior)

#### 1. ¿Hace falta de verdad un archivo .ico hoy?

**Respuesta:**

Casi no, pero cuesta nada. Los navegadores actuales toman el SVG o el PNG.
El `.ico` sigue siendo lo que piden algunos clientes de correo, lectores
RSS, accesos directos de Windows y cualquier petición automática a
`/favicon.ico` de una herramienta que no lee el HTML. Un `.ico` de 15 KB en
la raíz evita un 404 en el registro del servidor y un icono roto en esos
sitios.

#### 2. ¿Qué es un icono maskable y por qué pide márgenes?

**Respuesta:**

Es un icono del *manifest* que Android puede recortar con la máscara que use
el lanzador (círculo, lágrima, cuadrado redondeado). La zona segura que
siempre queda visible es el 80 % central; todo lo que esté en el borde puede
desaparecer. Por eso se genera con fondo liso y el dibujo al 60–70 % del
tamaño: el fondo rellena cualquier forma de máscara y el dibujo queda entero.

#### 3. ¿Cómo haces que el favicon cambie con el tema claro u oscuro?

**Respuesta:**

Sólo con el SVG: dentro del archivo se puede poner un `<style>` con una regla
`@media (prefers-color-scheme: dark)` que cambie el `fill`. Los navegadores
que usan el favicon SVG (Chrome, Firefox, Edge) la respetan; Safari no usa
favicons SVG y seguirá con el PNG. Para los iconos de iOS y Android no hay
mecanismo: por eso se les da un fondo de marca fijo, que funciona en los dos
temas.

<!-- /study-guide:section:brand-m6-favicons -->
