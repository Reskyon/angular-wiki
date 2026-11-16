# Agregar un proyecto

Procedimiento para publicar un proyecto nuevo en janioisacura.com: la tarjeta
en la portada y su página de detalle, en inglés y en español. No hay que tocar
rutas ni componentes: el script de contenido lee los archivos, los valida y
genera el índice del que salen las rutas y el prerenderizado.

Cómo se construyó esta parte del sitio está en el
[Módulo S7 de la Parte 3](03-secciones-de-portify.md#módulo-s7-proyectos-tarjetas-y-página-de-detalle)
de la guía. El esquema canónico de los campos vive en
`docs/architecture.md`
del repositorio; esta página lo aplica paso a paso.

## Antes de empezar

- **Un proyecto, dos archivos.** Cada proyecto es un archivo Markdown por
  idioma con el **mismo `slug`**: `content/en/projects/<slug>.md` y
  `content/es/projects/<slug>.md`. Si falta uno, el script falla con
  `missing translation for "<slug>"`.
- **El `slug` es la URL** (`/en/projects/<slug>` y `/es/projects/<slug>`) y
  no cambia entre idiomas: minúsculas, números y guiones
  (`angular-guide`, `teslo-shop`). Cambiarlo después rompe los enlaces que
  alguien haya guardado; para reordenar está `order`.
- **No inventar.** Rol, tecnologías y resultados salen del CV o de lo que se
  hizo de verdad. `type` distingue `professional`, `personal` y `learning`;
  un ejercicio de un curso es `learning`, aunque esté publicado.

## 1. La portada del proyecto

La tarjeta muestra la imagen a 415 × 478 px (vertical) y la página de detalle
la recorta a una franja ancha (1199 × 505) anclada arriba. Por eso:

1. Prepara una imagen de **830 × 956 px** (el doble, para pantallas de alta
   densidad) con lo importante en la parte **superior**: es lo único que se
   ve en la franja de la página.
2. Guárdala como `public/images/projects/<slug>.jpg` (JPEG para capturas y
   fotos; PNG si hay texto fino o transparencia). Para la guía de Angular es
   una captura de su portada.
3. Anota un texto alternativo por idioma que describa lo que se ve
   («Portada de la guía de Angular, con el índice de módulos y el buscador»).
   Es el nombre accesible del enlace de la imagen, así que tiene que decir
   qué es, no «imagen del proyecto».

`cover` y `coverAlt` van juntos: el script rechaza uno sin el otro
(`"cover" and "coverAlt" must be supplied together`). Hoy todos los proyectos
llevan portada; una tarjeta sin imagen se vería vacía.

## 2. El archivo en inglés

Crea `content/en/projects/<slug>.md` con este front matter (todos los campos
salvo `cover`, `coverAlt`, `links` y `deployments` son obligatorios):

```md
---
title: From code comments to an Angular guide
slug: angular-guide
summary: One or two sentences for the card and the page description (also the meta description).
type: personal
role: What Janio actually did in the project
stack:
  - Angular
  - MkDocs
  - Docker
featured: true
order: 1
cover: /images/projects/angular-guide.jpg
coverAlt: Home page of the Angular guide, with the module index and the search box
links:
  - label: Read the guide (in Spanish)
    url: https://angular-wiki.reskyon.com/study-guide/
deployments:
  - name: GifsApp
    url: https://angular-gifs.reskyon.com
    description: "A GIF browser built on the Giphy API."
---

Opening paragraph: context in one or two sentences.

## A heading per part of the story

Paragraphs. Blank line between paragraphs: the body is Markdown and `marked`
converts it to HTML during preparation.

## Another heading

...
```

Qué hace cada campo en pantalla:

| Campo | Tarjeta | Página de detalle |
| --- | --- | --- |
| `title` | Título (`<h3>`, enlace) | `<h1>` y `<title>` de la pestaña |
| `summary` | Párrafo bajo las etiquetas | Párrafo destacado bajo el título y `meta description` |
| `type` | Etiqueta «Personal» / «Professional» / «Learning» | Fila «Type» de la barra lateral |
| `role` | No se muestra | Fila «Role» |
| `stack` | Etiquetas en mayúsculas separadas por guiones | Fila «Stack», separadas por comas |
| `order` | Posición en la lista (menor primero; a igual `order`, por `slug`) | No se muestra |
| `featured` | Reservado; hoy se muestran todos los proyectos | No se muestra |
| `cover`, `coverAlt` | Imagen con el efecto de Portify | Franja superior |
| `links` | No se muestran | Fila «Links», un enlace por entrada |
| `deployments` | No se muestran | Sección «Apps online» bajo el cuerpo: cada aplicación publicada con su enlace y su descripción |

Reglas que comprueba el script, con el error que muestra:

- `title`, `slug`, `summary` y `role` no vacíos (`"<campo>" must be a non-empty string.`).
- `slug` en minúsculas con guiones (`"slug" is invalid.`), único en su idioma
  (`duplicate slug`).
- `type` uno de los tres valores (`"type" is invalid.`).
- `stack` con al menos una tecnología (`"stack" must be a non-empty list of strings.`).
- `featured` booleano y `order` numérico.
- `links` con `label` y `url` `https://` o `http://`
  (`"links" must contain labels and valid HTTP or HTTPS URLs.`).
- `deployments` (opcional): una lista que no esté vacía, con `name`, `description` y
  una `url` `https://` o `http://` en cada entrada
  (`"deployments" must be a non-empty list of names, descriptions and HTTP or HTTPS URLs.`).
  Los dos idiomas tienen que listar las mismas direcciones, en el mismo orden.
  Entre comillas las descripciones que lleven dos puntos.
- Cuerpo no vacío (`the body must not be empty.`).

El cuerpo admite el Markdown habitual: encabezados `##`, párrafos, listas,
negritas y enlaces. La página tiene estilos propios para `h2` y párrafos; las
listas y las imágenes salen con el estilo base de Bootstrap. Si una sección
nueva necesita algo más (una galería, una cita), se añade en
`project-page.component.scss` como parte del trabajo de esa sección.

## 3. El archivo en español

Copia el anterior a `content/es/projects/<slug>.md` y traduce todo salvo
`slug`, `type`, `order`, `featured`, `cover` y las URL. Traduce también
`coverAlt` y las etiquetas de `links`. Si el destino de un enlace está sólo
en un idioma, dilo en la etiqueta del otro («Read the guide (in Spanish)»).

El sitio es inglés por defecto: conviene escribir primero el archivo en
inglés y traducirlo después, para que los dos cuenten lo mismo.

## 4. Generar y mirar

Si quieres seguir el dato hasta la tarjeta, la ruta o el HTML, consulta
[Proyectos: del Markdown a una URL](learn-projects.md).

```bash
npm start
```

`prestart` ejecuta `npm run content:prepare`, que valida los archivos y
escribe `src/app/home/generated/projects.ts` y `project-bodies.ts` (carpeta
ignorada por Git). Si algo falla, el error dice el archivo y el campo; el
servidor no arranca hasta corregirlo. Con el servidor ya corriendo, un cambio
en `content/` necesita volver a ejecutar `npm run content:prepare` o
reiniciar `npm start`.

Comprueba en el navegador:

1. `/en/#projects` y `/es/#projects`: la tarjeta aparece en su posición, con
   la imagen a la izquierda desde 768 px y arriba en móvil; al pasar el ratón
   salen los marcos inclinados y la flecha.
2. `/en/projects/<slug>` y `/es/projects/<slug>`: franja superior, título,
   resumen, cuerpo y barra lateral con tipo, rol, tecnologías y enlaces.
3. El selector de idioma de la página de detalle lleva a la misma página en
   el otro idioma, y «Back to projects» vuelve a `/en#projects`.

## 5. Comprobar y publicar

```bash
npm run test:content
npm test -- --watch=false
npm run lint
npm run format:check
npm run build
```

La última línea del build dice cuántas rutas se prerenderizaron: con un
proyecto nuevo suben **dos** (una por idioma). Las rutas salen de
`src/app/app.routes.ts`, que recorre `PROJECTS[locale]` y crea una ruta
perezosa por `slug`; no hay nada que registrar a mano.

Al publicar una versión con el proyecto nuevo, Coolify reconstruye la imagen
y Nginx sirve `/en/projects/<slug>/index.html`. [Compilación y publicación](learn-release.md)
muestra cómo comprobar que esa versión llegó a la web.

## Errores frecuentes

- **Slugs distintos por idioma** (`guia-angular` en español): el script
  falla con `missing translation`. El `slug` es el mismo en los dos.
- **Portada vertical con lo importante abajo:** en la página de detalle la
  franja muestra sólo la parte superior.
- **Cuerpo con los párrafos pegados** (sin línea en blanco): Markdown los
  une en uno solo.
- **Enlaces `http://` sin certificado o rutas relativas en `links`:** el
  script sólo admite URL absolutas con protocolo.
- **Olvidar `coverAlt` al añadir `cover`**, o un `coverAlt` genérico:
  el primero rompe la preparación; el segundo deja un enlace que se anuncia
  como «imagen».
- **Editar `content/` con `ng serve` corriendo** y no ver cambios: hay que
  volver a preparar el contenido.
