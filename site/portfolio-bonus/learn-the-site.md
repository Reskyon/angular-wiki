# Aprende el sitio por dentro

Abre [la portada en español](https://janioisacura.com/es/) y elige un texto que puedas reconocer. La forma más rápida de orientarte en este repositorio es seguir ese texto hacia atrás. En el código, una sección de Angular decide cómo mostrarlo. Antes, un script de Node leyó el archivo de contenido y preparó los datos para Angular.

```text
content/                    → script de preparación → módulos generados
módulos generados y rutas   → Angular compila       → HTML, CSS y JavaScript
archivos compilados         → Nginx los sirve       → navegador
```

Parte del texto de la interfaz vive en el código, como «Actualidad». Las descripciones de cada puesto viven en YAML. El primer capítulo enseña a encontrar esa diferencia sin tener que memorizar todas las carpetas.

## Abrir el proyecto

Con el repositorio en tu equipo y Node.js disponible, `npm ci` instala las dependencias indicadas en el archivo de versiones. `npm start` prepara el contenido y arranca el servidor de desarrollo en `http://localhost:4200/`. Los comandos están en el README. Lee los casos completos aunque prefieras seguir el código y el sitio publicado sin montar un entorno local.

## Recorrido recomendado

| Capítulo | Qué podrás explicar |
| --- | --- |
| [1. Experiencia](learn-experience.md) | De dónde sale un dato visible y por qué una fecha inválida detiene la preparación. |
| [2. Proyectos](learn-projects.md) | Cómo dos archivos Markdown producen dos URLs y cómo verificar una entrada directa. |
| [3. Galería](learn-gallery.md) | Cómo un archivo de imagen llega al visor y por qué se devuelve el foco a la miniatura que lo abrió. |
| [4. Navegación y movimiento](learn-navigation.md) | Qué conecta el encabezado móvil con un enlace de sección y cuándo se aplica la preferencia de movimiento. |
| [5. Compilación y publicación](learn-release.md) | Qué comprueba cada etapa desde tu equipo hasta el sitio servido por Nginx. |

Los ejemplos describen `main` en la revisión `58cd92d`. Los cambios propuestos dentro de un ejemplo se identifican como tales. La [guía de construcción](como-se-construye.md) amplía las decisiones y muestra etapas anteriores.
