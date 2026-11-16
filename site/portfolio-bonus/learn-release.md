# Compilación y publicación: qué llega a producción

Abre un detalle de proyecto directamente en una pestaña nueva. Esa primera petición llega al servidor, aunque nunca hayas pasado por la portada. En este sitio Angular prepara el HTML al compilar. Nginx recibe la petición y busca el archivo que corresponde a la ruta. Generar una página de antemano se llama *prerenderizado*.

## Qué comprueba cada etapa

| Etapa | Qué evidencia deja |
| --- | --- |
| `npm run content:prepare` | El contenido se pudo leer y cumple las reglas que conoce el script. Escribe los datos que consume Angular. |
| `npm run test:content`, `npm run test:images` y `npm test -- --watch=false` | Prueban reglas de contenido, optimización de imágenes y comportamiento de Angular. El flujo de integración también ejecuta `npm run lint` y `npm run build`. |
| `npm run build` | Vuelve a preparar el contenido y genera archivos en `dist/janioisacura/browser/`. Para comprobar una página, busca su título y su texto en el `index.html` correspondiente. |
| Docker y Nginx | Docker ejecuta la compilación en una etapa con Node y copia la salida a una imagen final con Nginx. Nginx sirve los archivos y devuelve un estado HTTP 404 para una ruta inexistente. |
| Coolify y sitio publicado | Coolify construye y despliega la imagen. La comprobación de salud del contenedor inspecciona la portada inglesa. Una visita directa al detalle, al otro idioma y al CV aporta evidencia adicional. |

Comandos del proyecto · Flujo de integración · Dockerfile · Nginx

## Caso resuelto: el resumen sigue antiguo después de publicar

Partimos de un cambio concreto: una frase nueva en `summary` de `content/es/projects/angular-guide.md`. El identificador `angular-guide` se mantiene. Podemos seguir esa misma frase en cada etapa para encontrar dónde se quedó atrás.

1. **Fuente y preparación.** En la revisión que quieres comprobar, confirma que el Markdown español tiene la frase. Después de `npm run content:prepare`, búscala en `src/app/home/generated/projects.ts`. Si falta en el catálogo generado, lee la salida del comando y verifica qué copia del repositorio estás usando.
2. **HTML local.** Ejecuta **`npm run build`** y abre `dist/janioisacura/browser/es/projects/angular-guide/index.html`. Busca la frase dentro del resumen del detalle. Si el catálogo la contiene pero el HTML no, comprueba que el build terminó y que abriste la ruta española de esa compilación. El módulo generado demuestra que llegó el dato. El archivo HTML demuestra que Angular lo escribió en la página.
3. **Revisión desplegada.** Consulta en Coolify el despliegue de la aplicación correspondiente. El entorno de vista previa sigue `development` y el público sigue `main`. Compara el commit del despliegue con la rama que contiene el cambio. Si solo está en la vista previa, el resultado público puede seguir siendo el anterior.
4. **Respuesta pública.** Abre directamente `/es/projects/angular-guide`. En **Red**, selecciona la petición del documento y busca la frase en su respuesta. Comprueba también el estado HTTP. Si el build local contiene la frase y la respuesta pública no, compara primero el commit y el resultado del despliegue. Si coinciden, revisa a qué aplicación apunta el dominio y si interviene la caché. Si la respuesta ya contiene la frase y la pantalla muestra otra, el siguiente paso es inspeccionar lo que Angular presenta después de arrancar.

**Qué confirma la publicación.** El commit que contiene el cambio se desplegó en la aplicación pública y la petición directa devuelve el resumen nuevo en el documento español. El inglés conserva su texto si el cambio fue solo en español. Un check verde de la portada inglesa aporta información sobre esa portada. La respuesta del detalle confirma el cambio que veníamos siguiendo.

[Origen del resumen en Proyectos](learn-projects.md#caso-resuelto-corregir-un-resumen-en-español)

## Caso resuelto: al hacer clic funciona y al recargar falla

Una navegación desde la portada usa el router de Angular en el navegador. Una recarga solicita la URL al servidor. Si solo falla la recarga, busca primero `dist/janioisacura/browser/<idioma>/projects/<slug>/index.html`. Si falta el archivo, comprueba el catálogo y la ruta que entraron en la compilación. Si el archivo existe, compara el artefacto que compilaste con la versión que está sirviendo Nginx. Una página de error visible tampoco demuestra que el servidor haya respondido con HTTP 404: verifica el estado de la petición del documento en **Red**.

## Caso resuelto: la compilación falla al publicar

En el entorno de pruebas se documentó un fallo de compilación provocado por una clave YAML duplicada. La preparación se detuvo antes de construir la imagen y Coolify mantuvo el contenedor anterior. Esa observación explica qué puede pasar cuando falla el build. Si la compilación acaba pero hay una página incorrecta, revisa el artefacto y las páginas afectadas por separado. El chequeo de la portada inglesa puede seguir pasando.

[Verificar HTML, metadatos y sitio publicado](06-seo-y-vista-previa.md)

**Para continuar:** [Tareas y diagnóstico de fallos](maintenance.md) o [Guion para presentar el sitio](showcase.md).
