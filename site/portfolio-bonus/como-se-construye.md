# Cómo se construye este sitio

Índice de la guía de construcción de **janioisacura.com**, el portfolio de
Janio Isacura: un sitio Angular con contenido en Markdown y YAML, prerenderizado
a HTML estático y servido con Nginx. La guía explica, paso a paso y en el orden
en que se hizo, cada pieza del sitio: qué problema resuelve, qué decisión se
tomó, el código o los comandos exactos y qué errores evitar. Está escrita para
que alguien que nunca vio este repositorio, o el propio Janio en otro proyecto,
pueda repetir cada paso en un sitio distinto. La [referencia de arquitectura](arquitectura.md)
explica las decisiones del sistema. Esta guía las lleva a cambios concretos.

> Regla de lectura: primero mira el resultado en el sitio publicado
> ([janioisacura.com](https://janioisacura.com/en/)), después lee el módulo y
> al final intenta responder las preguntas de entrevista sin mirar la respuesta.

Si es tu primera vez en el repositorio y quieres modificar el sitio existente,
empieza por el [recorrido para aprender el sitio](learn-the-site.md). Esta guía
conserva el orden de construcción para estudiar cómo se desarrolló cada pieza.

## Cómo usar esta guía

**Partes y páginas.** La guía se divide en **partes**, y cada parte cubre una
pieza del sitio de principio a fin. Cada parte tiene su propia página en esta
wiki, numerada en el orden en que conviene leerla. Las páginas de referencia de
la plantilla ([Plantilla Portify](plantilla-portify.md),
[Estilos y animaciones](estilos-y-animaciones.md), [Personalización](personalizacion.md))
no son partes: describen el punto de partida, no los pasos.

**Módulos.** Cada página se divide en **módulos**, y cada módulo es un paso con
el mismo orden: el problema que resuelve, la decisión tomada en este sitio, el
procedimiento o el código completo, cómo funciona por dentro, errores comunes y
preguntas de entrevista con su respuesta visible. Cada parte tiene su propia
letra, para poder citar un módulo desde cualquier página sin confundirlo:

| Prefijo | Página                                        | Ejemplo                                       |
| ------- | --------------------------------------------- | --------------------------------------------- |
| M       | Parte 1: Marca y recursos (`01-marca-y-recursos`) | M3: por qué las fuentes van en `.woff2`   |
| E       | Parte 2: Cimientos de estilo (`02-cimientos-de-estilo`) | E2: por qué `@import` y no `@use`     |
| S       | Parte 3: Las secciones de Portify (`03-secciones-de-portify`) | S3: scroll por fragmento sin saltos |
| A       | Parte 4: Animaciones y fondo (`04-animaciones`) | A2: por qué un `from()` con retraso dejaba un elemento invisible |
| G       | Parte 5: La galería (`05-galeria`) | G2: por qué la imagen es visible sin JavaScript y el recuadro de carga queda detrás; G5: por qué la galería también es una sección de la portada |
| V       | Parte 6: Metadatos para compartir y buscadores (`06-seo-y-vista-previa`) | V3: por qué las etiquetas se escriben en un `TitleStrategy` y no al terminar la navegación |
| D       | Parte 7: La guía DIY (`07-guia-diy`) | D3: por qué en la guía el cambio de idioma lleva al mismo paso y no conserva el desplazamiento |

Cuando una página dice «el Módulo M3 de la Parte 1», es eso: la página
`01-marca-y-recursos`, sección «Módulo M3».

**Preguntas de entrevista.** Cada módulo termina con preguntas de nivel senior,
cada una con su respuesta debajo. Intenta responder antes de leerla.

**Cómo reproducirlo.** Cada módulo muestra los comandos y el código completos.
Para seguirlos en otro proyecto hace falta Node.js (la integración continua usa la versión 24 y el `Dockerfile` compila con `node:22-alpine`),
el CLI de Angular y, para la parte de marca, Illustrator o cualquier editor
vectorial que exporte SVG.

## Mapa de la guía

| Parte | Página | Qué construye |
| --- | --- | --- |
| 1 | [Marca y recursos](01-marca-y-recursos.md) | Logos en SVG limpios, fuentes web autoalojadas en `.woff2` con `@font-face`, favicons e iconos de aplicación |
| 2 | [Cimientos de estilo](02-cimientos-de-estilo.md) | Bootstrap por partes, la carpeta `src/styles/` con variables sin CSS, tokens de color, fuentes y reglas base, alias de importación y el esqueleto de página (encabezado fijo en móvil, navegación vertical y menú móvil) |
| 3 | [Las secciones de Portify](03-secciones-de-portify.md) | El hero con retrato y ondas, el enlace «Next chapter» compartido, el scroll por fragmento sin saltos, el título de sección, Sobre mí, Habilidades, Experiencia con los pipes `month` y `serial`, Proyectos con su página de detalle, Contacto sin formulario ni correo y el pie |
| 4 | [Animaciones y fondo](04-animaciones.md) | La coreografía de GSAP en un solo archivo con su inicializador, los reveals que no se quedan ocultos, el campo de puntos en un canvas y el interruptor que apaga JavaScript y CSS a la vez y que se aplica antes del primer pintado |
| 5 | [La galería](05-galeria.md) | Los datos de la galería generados desde una carpeta de imágenes, la pantalla de carga con la forma de cada imagen, los filtros accesibles, el visor con el foco bien manejado y la entrada en la portada que la suma a la serie de secciones |
| 6 | [Metadatos para compartir y buscadores](06-seo-y-vista-previa.md) | Las etiquetas Open Graph y la imagen para compartir, un `TitleStrategy` que las escribe con el título ya resuelto, direcciones canónicas y de idioma, las páginas fuera del índice, `robots.txt` y un `sitemap.xml` generado en el build |
| 7 | [La guía DIY](07-guia-diy.md) | Una guía corta en dos idiomas desde un YAML validado en el build, su página y su entrada en la portada arriba de Contacto, la URL que sigue el paso que se lee, el cambio de idioma que lleva al mismo paso y el cierre hacia el Bonus |

## Ruta recomendada

1. Lee [Plantilla Portify](plantilla-portify.md) para saber de qué punto parte el
   sitio: una plantilla comprada que se usa como referencia visual.
2. Sigue la [Parte 1: Marca y recursos](01-marca-y-recursos.md) en orden: primero
   los SVG, después las fuentes, al final los favicons. Cada módulo deja
   archivos en `public/` que el siguiente usa.
3. Lee [Estilos y animaciones](estilos-y-animaciones.md) y sigue la
   [Parte 2: Cimientos de estilo](02-cimientos-de-estilo.md): Bootstrap por
   partes, las variables compartidas, los tokens y las reglas base que todos
   los componentes importan, los alias de importación y el esqueleto de
   página con su menú.
4. Sigue la [Parte 3: Las secciones de Portify](03-secciones-de-portify.md),
   que construye cada sección sobre ese esqueleto, empezando por el hero.
5. Sigue con la [Parte 4: Animaciones y fondo](04-animaciones.md): la
   coreografía de GSAP, el campo de puntos y el interruptor de movimiento.
6. Sigue con la [Parte 5: La galería](05-galeria.md): los datos que salen de una
   carpeta de imágenes, la pantalla de carga, los filtros, el visor y su entrada en la portada.
7. Sigue con la [Parte 6: Metadatos para compartir y buscadores](06-seo-y-vista-previa.md):
   las etiquetas de vista previa, la imagen para compartir, las direcciones
   canónicas, `robots.txt`, el mapa del sitio y cómo comprobarlo todo.
8. Termina con la [Parte 7: La guía DIY](07-guia-diy.md): la versión corta de esta
   guía como una sección más del sitio, con su contenido validado, su página y un
   cambio de idioma que conserva el paso.
9. Para seguir el contenido desde su origen hasta producción, abre [Experiencia](learn-experience.md), [Proyectos](learn-projects.md) y [Compilación y publicación](learn-release.md).
