# Sitio estático de la wiki, servido en https://angular-basics.reskyon.com/wiki/
# La versión de la wiki que se publica está en wiki-ref (la escribe la Action
# de Reskyon/angular-ufh cada vez que copia la wiki).

FROM python:3.13-slim AS build
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*
# mkdocs fijado en 1.x: Material todavía no es compatible con MkDocs 2.
RUN pip install --no-cache-dir mkdocs==1.6.1 mkdocs-material==9.7.7
WORKDIR /site
COPY site/ .
COPY wiki-ref .
RUN git clone --quiet https://github.com/Reskyon/angular-wiki.wiki.git /wiki \
 && git -C /wiki checkout --quiet "$(cat wiki-ref)" \
 && python scripts/prepare.py /wiki docs \
 && NO_MKDOCS_2_WARNING=1 mkdocs build --strict -d /out

FROM nginx:alpine
COPY site/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /out /usr/share/nginx/html/wiki
EXPOSE 80
