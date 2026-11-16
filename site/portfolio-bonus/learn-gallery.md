# Galería: de una imagen al visor

Abre [la galería](https://janioisacura.com/es/gallery), enfoca una miniatura con el teclado y ábrela. Al cerrar el visor con Escape, el foco debe volver al botón que lo abrió. Vamos a seguir dos cosas distintas: de dónde salió la imagen y quién recuerda ese botón.

## De la carpeta a la cuadrícula

Las imágenes se guardan bajo `public/images/portfolio/`. Cada subcarpeta representa una categoría. Los archivos `content/en/gallery.yml` y `content/es/gallery.yml` aportan la configuración y el texto por idioma. La preparación escanea las imágenes y genera `GALLERY`. Un raster optimizado se sirve como un WebP. La cuadrícula y el visor usan esa misma imagen.

En `GalleryPageComponent`, abre la lectura del catálogo. El componente obtiene el idioma de la ruta, toma su galería y delega la cuadrícula de cada categoría. Cuando alguien abre una imagen, el evento entrega la imagen seleccionada y la referencia al botón que la abrió. El componente recuerda ese botón y guarda en un `signal` el estado actual del visor. Un `signal` es un valor cuyos cambios Angular puede usar para actualizar la vista.

Contrato de la galería · Página de la galería

## Caso resuelto: una foto de Naturaleza no aparece

Supón que `nature-koi.webp` no se ve al abrir la galería. **Empieza por Fotografía y selecciona Naturaleza.** Esa categoría abre en su primer grupo, Arquitectura. `GalleryCategoryComponent` guarda el grupo activo y `visible` filtra las imágenes del catálogo. Si la foto aparece al cambiar de grupo, su ausencia inicial está explicada por el filtro.

Si en **Todos** sigue faltando, busca `nature-koi.webp` en `src/app/home/generated/gallery.ts`. El archivo público del ejemplo está en `public/images/portfolio/photography/`. Si el catálogo no lo contiene, revisa la carpeta, el nombre y la salida de `npm run content:prepare`. Si el catálogo sí lo contiene pero la celda muestra un error, inspecciona la petición de la imagen en **Red**. En este punto ya sabemos que la preparación encontró la imagen y podemos investigar qué recibió el navegador.

`GalleryItemComponent` separa esos estados. Antes de conectar la interfaz, deja al navegador cargar la imagen. Luego consulta si ya terminó y mira `naturalWidth` para distinguir una imagen disponible de una que falló. Si sigue pendiente, los eventos `load` y `error` cierran el caso. La miniatura conserva su espacio y, si falla, deja visible el título de la imagen.

**Qué confirma la causa.** Si la imagen aparece al seleccionar Naturaleza, era el filtro. Si tras regenerar aparece en el catálogo, faltaba actualizar los datos o corregir el archivo de origen. Si el catálogo era correcto y la petición falla, la próxima comprobación es la URL del recurso o el archivo que sirve el entorno.

Componente de categoría · Componente de miniatura

## Caso resuelto: el visor se cierra y el teclado pierde su lugar

Abrimos una miniatura, pulsamos Escape y miramos qué elemento queda enfocado. Si el cuadro desaparece y el siguiente Tab comienza en otro sitio, la parte por investigar es la devolución de foco. En `close()`, el componente pone el estado del visor en `null` y llama a `focus()` sobre el botón que guardó en `open()`. Conservar la referencia permite reconocer el botón incluso cuando un clic lo activó sin enfocarlo.

La comprobación separa los dos componentes:

1. Al abrir con Enter, el foco pasa al botón de cierre. Tab y Shift+Tab se quedan dentro del visor. Si el foco escapa mientras está abierto, miramos `keepFocusInside` en `GalleryViewerComponent`.
2. Si hay varias fotos en el grupo, pulsamos una flecha para mostrar otra y cerramos con Escape. La miniatura **que abrió** el visor debe recuperar el foco. Si el visor se cierra y el foco vuelve a otra parte, revisamos qué `opener` recibió `open()` y qué elemento usa `close()` en `GalleryPageComponent`.
3. En `gallery-page.component.spec.ts` hay un caso que abre con clic sin enfocar primero el botón. Sirve para comprobar que la devolución no depende del elemento que el navegador tuviera enfocado. Una pasada en el navegador permite comprobar también el recorrido real de Tab.

La evidencia es el botón que conserva el foco al final, no solo que el diálogo desapareció. Componente del visor · Pruebas de la página

Para incorporar un archivo sigue [Agregar imágenes al portfolio](agregar-imagenes-al-portfolio.md). La [guía de construcción de la galería](05-galeria.md) explica los filtros, el recuadro de carga y los detalles del visor.

**Siguiente capítulo:** [Navegación y movimiento](learn-navigation.md).
