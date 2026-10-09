# Static site for the wiki, served at https://angular-wiki.reskyon.com/
# The wiki version to publish is in wiki-ref (written by the Reskyon/angular-ufh
# Action every time it copies the wiki).

FROM python:3.13-slim AS build
RUN apt-get update \
 && apt-get install -y --no-install-recommends git \
 && rm -rf /var/lib/apt/lists/*
# mkdocs pinned to 1.x: Material is not compatible with MkDocs 2 yet.
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
# Replaces the default Nginx welcome page.
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build /out /usr/share/nginx/html
EXPOSE 80
