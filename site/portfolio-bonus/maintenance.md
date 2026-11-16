# Tareas y diagnóstico de fallos

Si ya sabes qué quieres cambiar, entra por la tarea. Si estás investigando un fallo, empieza por la primera capa donde el resultado deja de coincidir con lo esperado.

## Tareas frecuentes

| Quiero cambiar | Dónde empiezo | Qué compruebo |
| --- | --- | --- |
| Texto o datos de un puesto | `content/en/experience.yml` o `content/es/experience.yml`. [Recorrido de Experiencia](learn-experience.md). | Regenero si el servidor estaba abierto y confirmo el idioma y la entrada. |
| Un proyecto | [Agregar un proyecto](agregar-un-proyecto.md). | Las dos tarjetas y los dos detalles coinciden con sus fuentes. Los detalles funcionan al entrar directamente. |
| Imágenes de la galería | [Agregar imágenes al portfolio](agregar-imagenes-al-portfolio.md). | La cuadrícula carga la imagen y el visor devuelve el foco al cerrarse. |
| PDF del CV | Procedimiento del CV. | Abro el PDF de cada idioma y reviso el destino y los enlaces dentro del PDF. La validación comprueba su estructura, no su texto. |
| Publicar un cambio | [Compilación y publicación](learn-release.md). | Reviso la compilación, el HTML de la ruta afectada y la versión publicada. |

## Averigua en qué capa se rompe

| Lo que ves | Primera comprobación |
| --- | --- |
| `npm start` o `npm run build` se detiene con un error YAML | Ejecuta `npm run content:prepare` y lee el archivo y el campo del error. [Caso de una fecha](learn-experience.md#caso-resuelto-el-contenido-falla-por-una-fecha). |
| Cambiaste un texto y el navegador muestra el anterior | Regenera el contenido y busca el texto nuevo en `src/app/home/generated/`. Si aparece ahí, revisa el idioma y la plantilla. |
| La tarjeta se ve, pero la imagen no carga | Compara la URL en **Red** con la ubicación real bajo `public/`. [Caso de la portada](learn-projects.md#caso-resuelto-la-portada-no-carga). |
| El detalle funciona al hacer clic, pero falla al recargar | Busca el `index.html` de la ruta en la salida compilada y después comprueba la versión que sirve Nginx. [Caso de la recarga](learn-release.md#caso-resuelto-al-hacer-clic-funciona-y-al-recargar-falla). |
| El título de una sección queda detrás del encabezado | Inspecciona la altura de la barra y el espacio que usa el desplazamiento en móvil. [Caso del encabezado](learn-navigation.md#caso-resuelto-el-encabezado-tapa-el-título). |

Si pides ayuda a la IA, puedes mostrarle el error completo, el fragmento de código y lo que ya comprobaste. Una consulta concreta sería: «El YAML cambió y el valor ya está en `generated/experience.ts`. ¿Qué seguirías en Angular para saber por qué la página conserva el texto anterior? Dame una comprobación». Usa la respuesta para decidir qué mirar y verifica el resultado en el proyecto.
