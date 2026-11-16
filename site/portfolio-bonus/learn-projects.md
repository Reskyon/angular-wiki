# Proyectos: del Markdown a una URL

Abre [el caso de la guía de Angular](https://janioisacura.com/es/projects/angular-guide). Su título y su resumen también aparecen en la tarjeta de la portada. La historia larga aparece en el detalle. Las dos vistas comparten los datos de un archivo, pero cada una utiliza una parte distinta.

## Sigue la tarjeta y el detalle

1. En `content/es/projects/angular-guide.md`, el bloque entre `---` y `---` contiene datos como `title`, `summary` y `slug`. El texto que viene después es la narración. El archivo inglés comparte `slug: angular-guide`. Ese identificador une las traducciones y forma parte de sus direcciones.
2. `scripts/prepare-content.mjs` valida los campos y comprueba que cada `slug` tenga su pareja. Genera `PROJECTS` para los datos de las tarjetas y las rutas. Marked convierte la narración en un fragmento HTML que queda en `PROJECT_BODIES`.
3. La portada usa el catálogo del idioma activo. `app.routes.ts` recorre ese mismo catálogo para crear una ruta por proyecto e idioma. `ProjectPageComponent` recibe los datos de la ruta y busca el cuerpo por idioma y `slug`. El componente se carga al entrar en el detalle y trae consigo el módulo de cuerpos. Así la portada puede usar las fichas sin importar el texto largo.
4. Cuando ejecutas `npm run build`, Angular genera un documento completo para cada ruta. El fragmento producido por Marked termina dentro de ese documento.

Preparación de proyectos · Rutas · Componente de detalle

## Caso resuelto: corregir un resumen en español

**Dónde empiezo.** En una copia de práctica cambiamos solo `summary` de `content/es/projects/angular-guide.md`. Usamos un texto fácil de reconocer, como «Resumen de prueba para el recorrido». El campo está en el Markdown porque forma parte de la ficha del proyecto, y la misma ficha alimenta la tarjeta y la ruta del detalle.

1. Ejecutamos `npm run content:prepare` y buscamos la frase en `src/app/home/generated/projects.ts`, dentro de `es`. Si la frase no está ahí, revisamos el archivo de origen y la salida del comando. Editar el módulo generado perdería el cambio en la siguiente preparación.
2. Comparamos `/es/#projects` y `/es/projects/angular-guide`. Las dos plantillas muestran `project.summary`. Si cambia una vista y la otra conserva el texto, comprobamos qué proyecto e idioma le llegan a esa vista. Si falta el texto en ambas, volvemos al catálogo del paso anterior.
3. Abrimos el detalle inglés. Su resumen sigue igual y la URL española conserva `angular-guide`. Esa es la comprobación que distingue el contenido traducible del identificador que une las dos versiones.

**Otro resultado y su causa.** Si se cambia solo el `slug` español a `guia-angular`, la preparación informa que falta una traducción. El script empareja por `slug` y encuentra dos identificadores sin pareja. Restaurar el `slug` compartido permite traducir el título y el resumen sin romper el enlace entre idiomas.

## Caso resuelto: la portada no carga

En el caso real, `cover: /images/projects/angular-guide.jpg` apunta al archivo `public/images/projects/angular-guide.jpg`. `public/` es la carpeta de origen. La URL comienza en `/images/`. Al declarar una portada, el validador exige `coverAlt`, el texto alternativo de la imagen.

Supón que el nombre de archivo está mal escrito. Con ambos campos presentes, la preparación puede pasar porque comprueba sus valores y no la existencia de la portada del proyecto. La evidencia está en la petición de imagen que ves en la pestaña **Red** del navegador. La solución es corregir la URL o colocar el archivo donde la URL indica. Volvemos a preparar, abrimos la tarjeta y confirmamos la petición y el texto alternativo.

La misma distinción aparece con `deployments`. La preparación comprueba que los enlaces tengan una forma válida y que las URL coincidan, en el mismo orden, entre idiomas. La disponibilidad de los destinos se comprueba abriéndolos.

## Cómo saber qué se publicó

Con `npm run build`, abre `dist/janioisacura/browser/es/projects/angular-guide/index.html` y su equivalente bajo `en/`. Busca el título y un párrafo de la narración en el marcado. Si están ahí, el navegador puede recibirlos antes de ejecutar Angular. Un proyecto válido nuevo añade dos rutas de detalle. El título de la tarjeta sigue enlazando a la ruta aunque la portada sea opcional.

Para seguir el mismo cambio hasta la web, lee [el caso de un resumen que sigue antiguo tras publicar](learn-release.md#caso-resuelto-el-resumen-sigue-antiguo-después-de-publicar).

Para incorporar un caso real, sigue [Agregar un proyecto](agregar-un-proyecto.md). Para profundizar en los componentes, consulta [Las secciones de Portify](03-secciones-de-portify.md).

**Siguiente capítulo:** [Galería: de una imagen al visor](learn-gallery.md).
