# Arquitectura del portfolio

El portfolio reúne el CV, los proyectos y la galería en un sitio Angular bilingüe. El contenido vive en archivos Markdown y YAML. El diseño toma Portify como punto de partida y usa componentes de Angular para adaptar las secciones y sus interacciones.

## Del contenido al navegador

1. **Contenido.** Los textos están bajo `content/en/` y `content/es/`. Un proyecto usa la misma clave `slug` en los dos idiomas, aunque se traduzcan su título y su cuerpo.
2. **Preparación.** Node lee y valida el contenido antes de que Angular lo use. Escribe módulos de datos para la portada, los proyectos, la galería y el CV. Cuando un dato cambia, la preparación lo vuelve a generar.
3. **Páginas.** Angular construye las rutas a partir del idioma y el catálogo. En la compilación genera HTML para cada ruta. El navegador puede mostrar el contenido inicial y Angular conecta las interacciones al arrancar.
4. **Publicación.** Docker compila el sitio y Nginx sirve los archivos resultantes. Coolify gestiona el despliegue. Así basta con servir archivos estáticos para estas páginas.

La preparación separa la edición de contenido de los componentes. Si cambia un resumen, se edita el Markdown y se vuelve a compilar. Si cambia el diseño de la tarjeta, se modifica el componente y se conservan los datos de los proyectos.

## Dónde profundizar

- [Secciones y contenido](secciones-y-contenido.md) explica qué aporta cada sección y cómo se adaptó la plantilla.
- [Proyectos: del Markdown a una URL](learn-projects.md) sigue un dato por el catálogo, la tarjeta y el detalle.
- [Compilación y publicación](learn-release.md) muestra cómo comprobar qué versión llegó a producción.
