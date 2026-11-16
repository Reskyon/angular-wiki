# Agregar imágenes al portfolio

Procedimiento para preparar las imágenes de la galería de janioisacura.com:
copiar los originales a una carpeta del repositorio, convertirlos con un
comando y confirmar solo los archivos ligeros. La galería está en
`/en/gallery` y `/es/gallery`, y cómo se construyó está en la
[Parte 5: La galería](05-galeria.md). Lo que muestra y cómo (categorías, filtros,
pantalla de carga) está en
`docs/gallery.md`
del repositorio, que es la fuente de las decisiones; esta página lo aplica paso
a paso.

## Antes de empezar

- **Una carpeta por categoría** dentro de `public/images/portfolio/`:
  `branding`, `illustration`, `photography` y `web-ui-ux`. El nombre de la
  carpeta es el identificador de la categoría.
- **Un solo archivo por imagen.** Cada foto o ilustración se guarda una vez, en
  WebP, con el lado largo de hasta 1800 px. No hay miniaturas: la galería usa
  el mismo archivo en la cuadrícula y al abrirlo en grande, y mientras llega
  cada imagen muestra un esqueleto (*skeleton*), un recuadro gris con un
  brillo que se desplaza, del tamaño exacto que va a ocupar. Así el repositorio
  no guarda dos copias de lo mismo.
- **Los originales no se suben a Git.** Se copian a la carpeta, se convierten
  ahí mismo y Git los ignora (`.jpg`, `.jpeg` y `.png`, también en mayúsculas).
  Lo que se confirma son los `.webp` y los `.svg`, porque el despliegue se
  construye desde Git. Guarda tus originales en otro lugar (por ejemplo, una
  carpeta de OneDrive): son lo único que permite volver a convertir con otros
  números.
- **Una de las imágenes es la portada de la portada.** La entrada de la galería
  en la página de inicio usa una imagen de la galería como portada (el campo
  `teaser.cover` de `gallery.yml`). Si la cambias o la borras, el build avisa.
- **Requisito:** `npm install` ya hecho. El script usa `sharp`, una librería de
  Node que redimensiona y convierte imágenes.

## 1. Prepara los originales

- **Vectores (logos, identidad):** exporta el SVG desde Illustrator y límpialo
  con SVGO, como en los
  [módulos M1 y M2 de la Parte 1](01-marca-y-recursos.md#módulo-m1-exportar-svg-desde-illustrator).
  Los SVG no se convierten: se usan tal cual. Su nombre tiene que estar ya en
  minúsculas con guiones (`brand-01.svg`), sin espacios.
- **Fotos e ilustraciones (JPG o PNG):** no hace falta redimensionarlas antes.
  El script las reduce y nunca las agranda, así que una imagen pequeña se queda
  como está.
- **Orden:** las imágenes se listan por el nombre de su archivo. Para fijar un
  orden, empieza el nombre con un número (`0003-goku.jpg`). Si exportas desde
  Photoshop con «Capas en archivos», el prefijo que pone
  (`illustration-_0003_goku.jpg`) se convierte solo en `0003-goku`.
- **Grupos (solo en `photography`):** una categoría puede tener botones de
  filtro. El grupo de cada imagen sale del principio de su nombre:
  `landscape-sunset001` va al grupo `landscape`. Después del nombre del grupo
  va **siempre un guion** (`food-n-drink-001`, no `food-n-drink001`). Si más
  adelante quieres filtros en otra categoría, el procedimiento está en
  `docs/gallery.md`.

## 2. Copia y convierte

1. Copia los archivos a `public/images/portfolio/<categoría>/`. Copia solo las
   imágenes, no una subcarpeta como `optimized/`.
2. Desde la raíz del repositorio:

```bash
npm run optimize:images
```

Al lado de cada JPG o PNG aparece un `.webp` con el mismo nombre, ya en
minúsculas y con guiones. El comando dice al final cuántas imágenes convirtió y
cuántas ya estaban al día. Si lo ejecutas otra vez, salta las que ya tienen su
WebP, así que puedes agregar imágenes poco a poco.

3. Para borrar además los originales una vez convertidos:

```bash
npm run optimize:images:clean
```

**El borrado no se puede deshacer**, y Git no los guarda para recuperarlos,
porque los ignora. Úsalo solo si tienes una copia de los originales fuera del
repositorio. Este modo vuelve a convertir cada imagen desde su original y solo
lo borra cuando terminó de escribir el WebP.

## 3. Comprueba antes de confirmar

```bash
git ls-files --others --exclude-standard public/images/portfolio
```

Debe listar solo archivos `.webp` y `.svg`. Si aparece un `.jpg` o `.png`, algo
no se está ignorando: no lo confirmes. Revisa también que ninguna foto pese de
más (el conjunto actual ronda los 9 MB en total).

Después valida el contenido de la galería:

```bash
npm run content:prepare
```

Lee las carpetas, comprueba que cada una tenga su categoría en
`content/en/gallery.yml` y `content/es/gallery.yml`, que cada imagen de una
categoría con grupos empiece por el nombre de uno de ellos y que no sobre ningún
grupo, y calcula el ancho y el alto reales de cada imagen. Si algo no cuadra,
falla y dice el archivo y el campo. Una carpeta nueva necesita su categoría en
los dos archivos, y las dos listas tienen que coincidir.

El título que verá el visitante sale del nombre del archivo:
`landscape-sunset001` pasa a «Sunset 1» y `0001-muhamad-ali`, a «Muhamad Ali».
Si alguno sale mal, se corrige en el `gallery.yml` de su categoría con un mapa
`titles` (por ejemplo `brand-01: Logo principal`), sin renombrar el archivo.

## 4. Confirma

Incluye los WebP y SVG aprobados para que la compilación pueda servirlos.
Después de publicar, abre la galería y comprueba que el navegador recibe los archivos.

## Por qué hay un esqueleto de carga

Sin un marcador, una cuadrícula de imágenes grandes tiene dos problemas:

- **Celdas vacías mientras llegan los archivos.** Cada imagen es un archivo de
  hasta 1800 px. Hasta que termina de descargarse, su celda se ve en blanco, y
  quien visita no sabe si la conexión es lenta o si la foto no existe.
- **La página salta.** Si la celda no reserva su tamaño, todo lo que está
  debajo se mueve cada vez que carga una imagen, y el visitante pierde el
  punto donde estaba leyendo. Se llama desplazamiento de diseño (*layout
  shift*).

El esqueleto (el [Módulo G2](05-galeria.md#módulo-g2-la-pantalla-de-carga-skeleton)
explica cómo está hecho) reserva el tamaño exacto de la celda y muestra un recuadro gris con
brillo hasta que llega la imagen. Por eso la galería necesita el ancho y el
alto reales de cada una. **No acelera la descarga ni baja el peso**: solo
cambia lo que se ve mientras tanto. El peso lo cuidan la carga diferida (solo se
descargan las imágenes que aparecen en pantalla) y el tamaño del archivo.

## Cómo funciona por dentro

El script `scripts/optimize-images.mjs` recorre las subcarpetas de
`public/images/portfolio/`, y en cada una:

1. Revisa todos los nombres **antes de escribir nada**. Si dos archivos darían
   el mismo resultado, se detiene.
2. Reduce cada imagen para que su lado largo mida como máximo 1800 px, sin
   agrandarla, y respeta la orientación con la que la guardó la cámara (así una
   foto vertical no sale acostada).
3. La guarda como WebP con calidad 82.

WebP pesa menos que JPG con calidad parecida, y todos los navegadores actuales
lo abren. Por eso no hace falta guardar un JPG de respaldo.

## Errores frecuentes

- **Dos archivos con el mismo nombre** (`ron.jpg` y `ron.png`): darían el mismo
  `ron.webp`, así que el script se detiene y nombra los dos. Deja solo uno.
- **Un SVG con espacios o mayúsculas** (`Brand 01.svg`): el script se detiene y
  dice a qué nombre renombrarlo.
- **Copiar la carpeta `optimized/` dentro de una categoría:** Git ve cada SVG
  dos veces. Copia solo los archivos, y los ya limpios con SVGO.
- **Un grupo sin guion** (`food-n-drink001`): no coincide con su grupo y el build de
  la galería se detiene (`groupOf` en `scripts/gallery-content.mjs` no encuentra
  el grupo). Renómbralo con el guion.
- **Usar `optimize:images:clean` sin copia de los originales:** no hay vuelta
  atrás.
- **Querer cambiar el tamaño o la calidad después de borrar los originales:**
  el WebP ya salió comprimido, y volver a comprimirlo pierde calidad. Hay que
  empezar desde los originales.

## Qué sigue

Guardar el filtro elegido en la dirección de la página y probar el visor en un
navegador real están anotados al final de la
[Parte 5: La galería](05-galeria.md#qué-sigue-en-esta-parte).
