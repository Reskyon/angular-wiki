# Guion para presentar el sitio

Puedes presentar el portfolio recorriendo una página visible, un dato que la alimenta y la forma en que se publica. Con tres paradas enseñas arquitectura y mantenimiento con el código abierto delante.

| Parada | Qué mostrar | Cómo contarlo |
| --- | --- | --- |
| **Un dato visible** | En `/es/#experience`, muestra Reskyon. Abre `content/es/experience.yml` y busca el mismo dato. Luego muestra `validateExperience` y la plantilla. | «Puedo editar el contenido en archivos bilingües. Un script comprueba sus reglas, genera los datos y el componente elige qué lista mostrar». [Recorrido de Experiencia](learn-experience.md). |
| **Una URL bilingüe** | Abre `/es/projects/angular-guide` y cambia de idioma. Muestra el `slug` compartido y el bucle de rutas en `app.routes.ts`. | «El título se traduce y el identificador se conserva. Cada idioma tiene una URL y Angular genera su HTML al compilar». [Recorrido de Proyectos](learn-projects.md). |
| **Una verificación** | Si tienes una compilación local, abre el `index.html` del detalle y busca un párrafo del caso. En el navegador, compara la respuesta del documento con una ruta inexistente. | «Compruebo el contenido en el HTML inicial y el estado HTTP de una ruta inexistente. Así sé qué recibe alguien que entra directamente». [Compilación y publicación](learn-release.md). |

Para profundizar, cuenta uno de los casos resueltos de Experiencia: un dato inválido se encuentra leyendo el error y siguiendo la comprobación correspondiente. El campo `location` y la regla que alinea los `id` entre idiomas son ejemplos de ampliación en la wiki. Puedes explicar cómo los implementarías a partir del código publicado.

Si te preguntan por el trabajo con IA, describe tu participación con tus palabras. Por ejemplo: «Usé IA para avanzar rápido durante la construcción. Para revisar el resultado seguí los datos hasta el HTML y localicé qué comprueba cada etapa». Ajusta esa frase a lo que hayas comprobado tú. La demo gana precisión cuando cada afirmación tiene una pantalla, un archivo o una prueba detrás.
