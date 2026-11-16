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
| La guía DIY | `content/en/diy.yml` y `content/es/diy.yml`, con los mismos `id` de paso en el mismo orden. [Cómo se construyó](07-guia-diy.md). | `npm run content:prepare` pasa, y al cambiar de idioma con un paso en la URL llego al mismo paso. |
| Esta guía pública (el Bonus) | [Publicar el Bonus a partir de la wiki](#publicar-el-bonus-a-partir-de-la-wiki). | El candidato revisado coincide con lo que quiero publicar antes de aprobar su huella. |

## Averigua en qué capa se rompe

| Lo que ves | Primera comprobación |
| --- | --- |
| `npm start` o `npm run build` se detiene con un error YAML | Ejecuta `npm run content:prepare` y lee el archivo y el campo del error. [Caso de una fecha](learn-experience.md#caso-resuelto-el-contenido-falla-por-una-fecha). |
| Cambiaste un texto y el navegador muestra el anterior | Regenera el contenido y busca el texto nuevo en `src/app/home/generated/`. Si aparece ahí, revisa el idioma y la plantilla. |
| La tarjeta se ve, pero la imagen no carga | Compara la URL en **Red** con la ubicación real bajo `public/`. [Caso de la portada](learn-projects.md#caso-resuelto-la-portada-no-carga). |
| El detalle funciona al hacer clic, pero falla al recargar | Busca el `index.html` de la ruta en la salida compilada y después comprueba la versión que sirve Nginx. [Caso de la recarga](learn-release.md#caso-resuelto-al-hacer-clic-funciona-y-al-recargar-falla). |
| El título de una sección queda detrás del encabezado | Inspecciona la altura de la barra y el espacio que usa el desplazamiento en móvil. [Caso del encabezado](learn-navigation.md#caso-resuelto-el-encabezado-tapa-el-título). |

Si pides ayuda a la IA, puedes mostrarle el error completo, el fragmento de código y lo que ya comprobaste. Una consulta concreta sería: «El YAML cambió y el valor ya está en `generated/experience.ts`. ¿Qué seguirías en Angular para saber por qué la página conserva el texto anterior? Dame una comprobación». Usa la respuesta para decidir qué mirar y verifica el resultado en el proyecto.

## Publicar el Bonus a partir de la wiki

La wiki del portfolio es privada y es la fuente. Una parte de ella se publica como
Bonus en la Guía de Angular (`https://angular-wiki.reskyon.com/portfolio-bonus/`).
La copia pública nunca se actualiza sola: alguien revisa cada versión y aprueba
exactamente esa.

**Qué páginas salen.** Las que lista el manifiesto
`scripts/wiki/portfolio-bonus.json` del repositorio, en dos grupos: «Aprende el
sitio» y «Referencia técnica», además de la portada de la wiki. Las páginas de
planificación y seguimiento quedan fuera. El manifiesto también puede omitir un
módulo concreto de una página (`omit_modules`, por el id de su marcador) o los
bloques de código de ciertos lenguajes (`omit_fence_languages`), para no copiar
fragmentos de la plantilla comprada.

**Qué detiene la exportación.** El script `scripts/wiki/export-portfolio-bonus.py`
falla, con el nombre de la página, si encuentra:

- un número de historia o de PR suelto en el texto, como `#12` (los bloques y
  fragmentos de código no se revisan, así que un color como `#333` escrito como
  código no molesta; escrito en el texto, sí);
- un enlace a las issues, los PR o el tablero del proyecto, o una mención de los
  documentos de seguimiento (el traspaso y el plan de desarrollo) o de la página
  de planificación;
- un enlace a una página de la wiki que no está en el manifiesto;
- un enlace al repositorio privado que no sea a un archivo o carpeta. Los enlaces
  a archivos se publican como texto, sin enlace.

**Los nombres de esta sección.** Los nombres del flujo, del entorno, del secreto,
del artefacto y del campo de la huella van aquí como marcadores, al estilo de un
`.env.template`: `<FLUJO_DE_EXPORTACIÓN>`, `<ENTORNO_DE_PUBLICACIÓN>`,
`<TOKEN_DE_PUBLICACIÓN>`, `<ARTEFACTO_CANDIDATO>` y `<CAMPO_DE_HUELLA>`. Los
nombres reales están en `docs/portfolio-bonus.md`, en el repositorio privado.

**Antes de la primera publicación.** En el repositorio del portfolio tiene que
existir un entorno (*environment*) de GitHub, `<ENTORNO_DE_PUBLICACIÓN>`, con las
ramas de despliegue limitadas a `main`, y dentro de él un secreto,
`<TOKEN_DE_PUBLICACIÓN>`: un token de acceso con permiso solo sobre el
repositorio público de la Guía de Angular, para subir una rama y abrir un PR. Solo
el trabajo que publica nombra ese entorno, así que ningún otro flujo, ni uno
agregado en otra rama, puede leer el token. El entorno se crea antes de la
primera ejecución con huella: si un flujo nombra un entorno que no existe, GitHub
lo crea en el momento sin ninguna restricción. El valor del token no se escribe
nunca en un archivo ni en la wiki; se guarda con
`gh secret set <TOKEN_DE_PUBLICACIÓN> --env <ENTORNO_DE_PUBLICACIÓN>`, que lo
pide sin mostrarlo.

**El procedimiento.**

1. **Ejecuta el flujo sin huella.** En la pestaña *Actions* del repositorio del
   portfolio, abre `<FLUJO_DE_EXPORTACIÓN>` y pulsa *Run workflow* con el campo
   `<CAMPO_DE_HUELLA>` vacío. El flujo también corre solo cuando cambia la wiki y
   una vez al día; esas ejecuciones solo preparan candidatos.
2. **Revisa el candidato privado.** El resumen de la ejecución muestra el commit
   de la wiki y la huella SHA-256 del candidato. Descarga el artefacto
   `<ARTEFACTO_CANDIDATO>` y lee todas las páginas: no puede haber código de la
   plantilla, recursos privados ni datos de seguimiento. Si algo sobra, corrige la
   wiki y vuelve al paso 1.
3. **Ejecuta el flujo con la huella.** Vuelve a *Run workflow* y pega en
   `<CAMPO_DE_HUELLA>` la huella que revisaste. Si la wiki cambió entre medias, la
   exportación falla, guarda el candidato nuevo para revisarlo y la publicación no
   empieza. Si coincide, el flujo abre (o reutiliza) un PR en la Guía de Angular;
   si lo publicado ya es igual, no abre ninguno.
4. **Revisa y fusiona ese PR** en la Guía de Angular. Su compilación comprueba el
   Bonus antes de publicarlo.

También puedes exportar en local para ver si la wiki pasa las reglas, con
`Markdown>=3.8,<4` instalado en un entorno virtual:
`python scripts/wiki/export-portfolio-bonus.py <checkout-de-la-wiki> scripts/wiki/portfolio-bonus.json <carpeta-vacía>`.
El script imprime la huella. El detalle técnico está en
el procedimiento del Bonus.
