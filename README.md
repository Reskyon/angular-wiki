# Angular Wiki

Guía de estudio de Angular en español: teoría de cada tema, una hoja de atajos
y preguntas de entrevista de nivel senior con su respuesta.

**El contenido está en la [wiki de este repositorio](https://github.com/Reskyon/angular-wiki/wiki).**

- [Guía de estudio](https://github.com/Reskyon/angular-wiki/wiki/study-guide): índice y ruta recomendada.
- [Parte 1: TypeScript sin framework](https://github.com/Reskyon/angular-wiki/wiki/01-typescript-intro)
- [Parte 2: Angular](https://github.com/Reskyon/angular-wiki/wiki/02-bases)
- [Hoja de atajos de Angular](https://github.com/Reskyon/angular-wiki/wiki/cheatsheet)

Versión web: [angular-wiki.reskyon.com](https://angular-wiki.reskyon.com/).
La aplicación de ejemplo está publicada en
[angular-basics.reskyon.com](https://angular-basics.reskyon.com).

## Cómo se actualiza

Esta wiki es una **copia de sólo lectura**. Se escribe en un repositorio
privado de estudio y una GitHub Action la copia aquí cada vez que cambia, así
que cualquier edición hecha directamente en esta wiki se pierde en la
siguiente copia. Sólo los colaboradores de Reskyon pueden escribir en este
repositorio y en su wiki.

## Cómo se construye el sitio web

La versión web es un sitio estático generado con
[MkDocs](https://www.mkdocs.org/) y el tema
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), servido
por Nginx en Coolify. La interfaz (barra lateral, buscador, modo claro y
oscuro, botón de copiar código) es la del tema; `site/mkdocs.yml` sólo la
configura.

```text
Reskyon/angular-wiki
├── Dockerfile            ← lo usa Coolify
├── wiki-ref              ← commit de la wiki a publicar (lo actualiza la Action)
├── README.md
└── site/
    ├── mkdocs.yml        ← configuración del sitio y del tema
    ├── nginx.conf        ← cómo se sirve el sitio
    └── scripts/
        └── prepare.py    ← convierte los .md de la wiki al formato de MkDocs
```

### De la wiki al HTML

Todo pasa durante el `docker build`, no cuando alguien visita la página:

```text
wiki-ref (commit de la wiki)
   │
   ▼
git clone de la wiki pública ──► checkout de ese commit exacto
   │
   ▼
scripts/prepare.py ──► docs/
   │   Home.md → index.md (portada)
   │   [texto](02-bases#ancla) → [texto](02-bases.md#ancla)
   ▼
mkdocs build --strict ──► HTML estático
   │   lee docs/*.md + mkdocs.yml
   │   convierte Markdown → HTML con la plantilla de Material
   │   genera el índice del buscador (JSON)
   │   falla si un enlace o ancla no existe
   ▼
nginx:alpine sirve el sitio en angular-wiki.reskyon.com
```

- **`prepare.py` es el puente entre los dos formatos.** La wiki de GitHub
  enlaza páginas por su nombre, sin extensión; MkDocs necesita el archivo
  `.md` para resolver el enlace. El script sólo reescribe esos enlaces y
  renombra la portada: el contenido no cambia. Corre únicamente en la etapa
  de build; la imagen final de Nginx sólo lleva el HTML generado.
- **El menú se genera solo.** `prepare.py` reescribe el bloque `nav:` de
  `mkdocs.yml`: Inicio y Guía de estudio primero, después cada página
  `NN-nombre.md` ordenada por número (con su primer `# ` como título) y la
  Hoja de atajos al final. Una página nueva `NN-nombre.md` aparece sin tocar
  nada; una página con otro nombre hace fallar el build.
- **Las anclas son las mismas que en GitHub** (`#módulo-8-…`, en minúsculas y
  con acentos), así que los enlaces a secciones funcionan igual en la wiki y
  en el sitio.
- **El buscador no necesita servidor:** MkDocs genera un índice en JSON y la
  búsqueda corre en el navegador.
- **El build es estricto:** si una edición de la wiki deja un enlace o un ancla
  rota, el deploy falla y queda publicada la versión anterior.

### Cuándo se publica

```text
edición en la wiki privada
   │  (GitHub Action)
   ├──► copia a la wiki de este repositorio
   └──► actualiza wiki-ref en main ──► Coolify redespliega el sitio
```

### Versiones fijadas

El `Dockerfile` fija `mkdocs==1.6.1` y `mkdocs-material==9.7.7`. MkDocs 2.0
no es compatible con Material ni con sus plugins, así que antes de subir de
versión hay que revisar en qué quedó esa transición.

### Probar en local

```bash
docker build -t angular-wiki .
docker run --rm -p 8080:80 angular-wiki
# abrir http://localhost:8080/
```
