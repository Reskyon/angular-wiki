"""Turns the GitHub wiki into the docs/ folder that MkDocs uses.

- Home.md becomes index.md (the site's home page).
- Links between wiki pages have no extension ([text](02-bases#anchor));
  MkDocs needs the file name (02-bases.md#anchor).
- Special wiki pages (_Sidebar, _Footer) are not published.
"""

import re
import shutil
import sys
from pathlib import Path

wiki = Path(sys.argv[1])
docs = Path(sys.argv[2])

pages = {p.stem: p for p in wiki.glob('*.md') if not p.stem.startswith('_')}
target = {name: ('index' if name == 'Home' else name) for name in pages}

# [text](page) or [text](page#anchor); URLs and paths with an extension are left alone.
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
