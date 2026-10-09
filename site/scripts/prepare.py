"""Convierte la wiki de GitHub en la carpeta docs/ que usa MkDocs.

- Home.md pasa a ser index.md (la portada del sitio).
- Los enlaces entre páginas de la wiki no llevan extensión
  ([texto](02-bases#ancla)); MkDocs necesita el archivo (02-bases.md#ancla).
- Las páginas especiales de la wiki (_Sidebar, _Footer) no se publican.
"""

import re
import shutil
import sys
from pathlib import Path

wiki = Path(sys.argv[1])
docs = Path(sys.argv[2])

pages = {p.stem: p for p in wiki.glob('*.md') if not p.stem.startswith('_')}
target = {name: ('index' if name == 'Home' else name) for name in pages}

# [texto](pagina) o [texto](pagina#ancla); no toca URLs ni rutas con extensión.
link = re.compile(r'\]\(([A-Za-z0-9._-]+?)(#[^)\s]*)?\)')


def fix(match: re.Match) -> str:
    name, anchor = match.group(1), match.group(2) or ''
    if name not in target:
        return match.group(0)
    return f']({target[name]}.md{anchor})'


if docs.exists():
    shutil.rmtree(docs)
docs.mkdir(parents=True)

for name, path in pages.items():
    text = link.sub(fix, path.read_text(encoding='utf-8'))
    (docs / f'{target[name]}.md').write_text(text, encoding='utf-8')
    print(f'{path.name} -> {target[name]}.md')
